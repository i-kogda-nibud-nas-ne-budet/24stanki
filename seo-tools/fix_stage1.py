"""Stage-1 mass fixes for 24stanki static site.

Steps (each idempotent):
    doubled   - h2 «Ремонт X в {Им} и Москва» blocks (moskovskiy/moskva/
                shcherbinka/zelenograd x 8 services = 32 files)
    year      - valtsev group <title> «цены 2025» -> «цены 2026» (+desc scan)
    cjk       - brand placeholder 学徒欧博 -> Stalex, lubricant line,
                valtsev «processing» intro, article-specific repairs
    geo       - city declension after в/по/из/от (pymorphy2 + overrides)
    latin     - JSON-LD latin city slugs -> Cyrillic prepositional
    region    - non-MO cities: «и МО», «Московской области», «и {Обл} область»
                -> correct oblast forms
    warranty  - remove works-warranty phrases site-wide

Usage:
    python fix_stage1.py [--steps all|doubled,year,cjk,geo,latin,region,warranty]
                         [--apply] [--files SUBSTR ...] [--dump-forms]
                         [--rebuild-forms]

Dry run is the default; --apply writes changes.
"""

from __future__ import annotations

import argparse
import inspect
import json
import re
import sys
import warnings
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS = Path(__file__).resolve().parent
FORMS_FILE = TOOLS / "data" / "city_forms.txt"

sys.path.insert(0, str(TOOLS))
from check_geo import discover_geo_files  # noqa: E402

warnings.filterwarnings("ignore")

# pymorphy2 0.9.1 needs inspect.getargspec removed in py3.11+
if not hasattr(inspect, "getargspec"):
    def _getargspec(f):
        spec = inspect.getfullargspec(f)
        return spec.args, spec.varargs, spec.varkw, spec.defaults
    inspect.getargspec = _getargspec

try:
    import pymorphy2  # noqa: E402
    HAS_MORPHY = True
except Exception:
    HAS_MORPHY = False

CYR_SERVICES = ("trubogibov", "profilgebiv", "valtsev", "armaturogiba",
                "gilotin", "listogibov")

# Cities where pymorphy2 picks a wrong homonym parse or wrong part declension.
# slug -> (nom, gen, dat, loc)
OVERRIDES: dict[str, tuple[str, str, str, str]] = {
    "dmitrov": ("Дмитров", "Дмитрова", "Дмитрову", "Дмитрове"),
    "belyov": ("Белёв", "Белёва", "Белёву", "Белёве"),
    "kovrov": ("Ковров", "Коврова", "Коврову", "Коврове"),
    "naro-fominsk": ("Наро-Фоминск", "Наро-Фоминска", "Наро-Фоминску",
                     "Наро-Фоминске"),
    "orekhovo-zuevo": ("Орехово-Зуево", "Орехово-Зуева", "Орехово-Зуеву",
                       "Орехово-Зуеве"),
    "losino-petrovskiy": ("Лосино-Петровский", "Лосино-Петровского",
                          "Лосино-Петровскому", "Лосино-Петровском"),
    "spas-demensk": ("Спас-Деменск", "Спас-Деменска", "Спас-Деменску",
                     "Спас-Деменске"),
    "spas-klepiki": ("Спас-Клепики", "Спас-Клепиков", "Спас-Клепикам",
                     "Спас-Клепиках"),
    "sergiev-posad": ("Сергиев Посад", "Сергиева Посада", "Сергиеву Посаду",
                      "Сергиевом Посаде"),
    # pymorphy2 homonym traps: indeclinable/singular parses of city names
    "konakovo": ("Конаково", "Конакова", "Конакову", "Конакове"),
    "shchyokino": ("Щёкино", "Щёкина", "Щёкину", "Щёкине"),
    "donskoy": ("Донской", "Донского", "Донскому", "Донском"),
    "kotelniki": ("Котельники", "Котельников", "Котельникам", "Котельниках"),
    "petushki": ("Петушки", "Петушков", "Петушкам", "Петушках"),
    "kremyonki": ("Кремёнки", "Кремёнок", "Кремёнкам", "Кремёнках"),
    "lipki": ("Липки", "Липок", "Липкам", "Липках"),
    "demidov": ("Демидов", "Демидова", "Демидову", "Демидове"),
    "efremov": ("Ефремов", "Ефремова", "Ефремову", "Ефремове"),
    "gavrilov-yam": ("Гаврилов-Ям", "Гаврилова-Яма", "Гаврилову-Яму",
                     "Гавриловом-Яме"),
    "ermolino": ("Ермолино", "Ермолина", "Ермолину", "Ермолине"),
}

PLURALIA_TANTUM_NOMS = {"Химки", "Мытищи", "Люберцы", "Озёры", "Луховицы",
                        "Вязники", "Петушки", "Меленки", "Сухиничи",
                        "Котельники", "Бронницы", "Кимры"}

MOTION_RE = re.compile(
    r"\b(?:выезд\w*|приезд\w*|поездк\w*|выезжаем|выезжает|выедем|приезжаем|"
    r"приедет|приедем|ездим|ездит|едем|поедем|отправля\w*|достави\w*|"
    r"добраться|прибытие|прибуде\w*)\b", re.I)

WORD_GUARD = r"(?![\wа-яёА-ЯЁ-])"

# region nominative -> genitive (= prepositional) phrase
REGION_ADJS = ("Московская", "Тверская", "Ярославская", "Владимирская",
               "Рязанская", "Тульская", "Калужская", "Смоленская")
REGION_NOM_RE = re.compile(
    r"(?<![\wа-яёА-ЯЁ-])(и|по всей) (" + "|".join(REGION_ADJS)
    + r") область" + WORD_GUARD)

# Moscow-district cities: their oblast is «Москва», not a separate region
MOSCOW_DISTRICT_SLUGS = {"troitsk", "zelenograd", "shcherbinka", "moskovskiy"}

GLOBAL_CJK_SUBS: list[tuple[str, str]] = [
    ("学徒欧博", "Stalex"),
    ("Проверка润滑 системы", "Проверка системы смазки"),
    ("деформацинного проката, processing проволоки и труб",
     "деформации проката, обработки проволоки и труб"),
]

CJK_RE_SCAN = re.compile(r"[\u4E00-\u9FFF\u3400-\u4DBF\uF900-\uFAFF\u3040-\u30FF\uAC00-\uD7AF]")
MIXED_RE_SCAN = re.compile(r"[а-яёА-ЯЁ]+[a-z]+|[a-z]+[а-яёА-ЯЁ]+")

ARTICLE_SUBS: dict[str, list[tuple[str, str]]] = {
    "blog-kak-opredelit-chto-listogibu-nuzhen-remont.html": [
        ("—失去了 гашения вибраций", "— потеря гашения вибраций"),
        ("На表面ности заготовок остаются следы",
         "На поверхности заготовок остаются следы"),
        ("нет ли новых следов на表面ности", "нет ли новых следов на поверхности"),
    ],
    "blog-remont-chpu-stoyki-delem-instrukciya.html": [
        ("DA-58T定期 появлялась ошибка", "DA-58T регулярно появлялась ошибка"),
        ("gócовые поправки сбрасываются", "угловые поправки сбрасываются"),
        ("нужен терминатор на последнем устройстве",
         "нужен терминатор на последнем устройстве"),
        ("проблема в экране или 연결ении", "проблема в экране или подключении"),
    ],
    "blog-remont-cpu-stoiki.html": [
        ("Параметры осей,温度, напряжения", "Параметры осей, температуры, напряжения"),
        ("Сброс кodes ошибок через меню", "Сброс кодов ошибок через меню"),
    ],
    "blog-remont-gilotiny-cena-realnie-primeri.html": [
        ("первое, что想知道 владельца", "первое, что хочет знать владелец"),
    ],
    "blog-zapchasti-dlya-listogibov-original-ili-analogi.html": [
        (">标准<", ">Стандартный<"),
    ],
    "kakoj-stanok-vybrat-dlya-proizvodstva.html": [
        ("для высокоскоростной резки任何 размер",
         "для высокоскоростной резки любого размера"),
    ],
    "sravnenie-listogibov-i-gilotin.html": [
        ("Гибка металла в的角度", "Гибка металла под углом"),
    ],
}

WARRANTY_SUBS: list[tuple[str, str]] = [
    # geo page body: «Выезд мастера в X, гарантия на все работы 6 месяцев.»
    (", гарантия на все работы 6 месяцев.", "."),
    # geo meta description: «… Выезд мастера в X. Гарантия 6 месяцев. ☎ …»
    (" Гарантия 6 месяцев.", ""),
    # JSON-LD / og descriptions: «Выезд 24/7, гарантия 6 месяцев.»
    (", гарантия 6 месяцев", ""),
    # city-unique enumeration: «…, гарантию 6 месяцев, работу с …»
    (", гарантию 6 месяцев", ""),
    # geo advantage strip: «… Предоставляем гарантию 6 месяцев на работы и запчасти»
    (" Предоставляем гарантию 6 месяцев на работы и запчасти", ""),
    # faq «5. Оплата и гарантия»
    ("<h3>5. Оплата и гарантия</h3>", "<h3>5. Оплата</h3>"),
    (" Вы получаете гарантийный талон на 6 месяцев.", ""),
    # blog CTA
    (" Гарантия на работы!", ""),
]

WARRANTY_BLOCK_RES: list[re.Pattern[str]] = [
    # faq-item «Какая гарантия на ремонт?» целиком
    re.compile(
        r'<div class="faq-item">\s*<div class="faq-question">\s*'
        r'<h3>Какая гарантия на ремонт\?</h3>.*?</div>\s*</div>', re.S),
    # service-card 🛡️ «Гарантия 6 месяцев»
    re.compile(
        r'<div class="service-card">\s*<div class="service-icon">[^<]*</div>'
        r'\s*<h3>Гарантия 6 месяцев</h3>\s*<p>Даем гарантию[^<]*</p>\s*</div>'),
    # uslugi.html li
    re.compile(r'<li>Гарантия на все выполненные работы</li>\s*'),
]


def read_raw(path: Path) -> str:
    with open(path, encoding="utf-8", newline="") as fh:
        return fh.read()


def write_raw(path: Path, text: str) -> None:
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)


def preserve_case(src: str, tgt: str) -> str:
    """Copy per-word capitalization from src onto tgt."""
    out_words = []
    src_words = src.split(" ")
    tgt_words = tgt.split(" ")
    if len(src_words) != len(tgt_words):
        return tgt.capitalize() if src[:1].isupper() else tgt
    for s, t in zip(src_words, tgt_words):
        if s[:1].isupper():
            t = t[:1].upper() + t[1:]
        out_words.append(t)
    return " ".join(out_words)


def decline_word(morph, word: str, case: str) -> str | None:
    """Inflect one word; falls back to plural forms (Химки, Мытищи...)."""
    parses = morph.parse(word.lower())
    best_flex = None
    fallback = None
    for p in parses:
        infl_sing = p.inflect({case, "sing"})
        infl_any = p.inflect({case})
        if infl_sing and p.tag.POS in ("NOUN", "ADJF"):
            return infl_sing.word
        if infl_any and fallback is None:
            fallback = infl_any.word
            best_flex = True
    return fallback


def decline_phrase(morph, nom: str, case: str) -> str | None:
    parts_out = []
    for word in nom.split(" "):
        pieces = []
        for piece in word.split("-"):
            infl = decline_word(morph, piece, case)
            if infl is None:
                return None
            pieces.append(infl)
        restored = "-".join(
            (pc[:1].upper() + pc[1:]) if sp[:1].isupper() else pc
            for sp, pc in zip(word.split("-"), "-".join(pieces).split("-"))
        )
        parts_out.append(restored)
    return " ".join(parts_out)


def extract_nominative(root: Path, slug: str,
                       index: dict[tuple[str, str], list[Path]]) -> str | None:
    """Nominative city name from JSON-LD of a cyrillic-group sibling file."""
    for svc in CYR_SERVICES:
        for path in index.get((slug, svc), []):
            m = re.search(r'"name":\s*"Ремонт[^"]*? в ([^"]+)"', read_raw(path))
            if m:
                cand = m.group(1).strip()
                if re.fullmatch(r"[А-ЯЁ][а-яёА-ЯЁ\- ]+", cand):
                    return cand
    return None


def build_city_forms(root: Path) -> dict[str, tuple[str, str, str, str]]:
    """slug -> (nom, gen, dat, loc); cached in seo-tools/data/city_forms.txt."""
    if FORMS_FILE.is_file():
        forms: dict[str, tuple[str, str, str, str]] = {}
        for line in FORMS_FILE.read_text(encoding="utf-8").splitlines():
            if line.strip():
                parts = line.split("|")
                forms[parts[0]] = (parts[1], parts[2], parts[3], parts[4])
        return forms

    pairs = discover_geo_files(root)
    index: dict[tuple[str, str], list[Path]] = {}
    for path, city in pairs:
        svc = _service_of(path.name)
        if svc:
            index.setdefault((city, svc), []).append(path)

    morph = pymorphy2.MorphAnalyzer() if HAS_MORPHY else None
    forms = {}
    problems = []
    for slug in sorted({c for _, c in pairs}):
        if slug in OVERRIDES:
            forms[slug] = OVERRIDES[slug]
            continue
        nom = extract_nominative(root, slug, index)
        if nom is None:
            problems.append(slug)
            continue
        if morph is None:
            problems.append(slug + " (no pymorphy2)")
            continue
        gen = decline_phrase(morph, nom, "gent")
        dat = decline_phrase(morph, nom, "datv")
        loc = decline_phrase(morph, nom, "loct")
        if not (gen and dat and loc):
            problems.append(f"{slug} ({nom})")
            continue
        forms[slug] = (nom, gen, dat, loc)

    if problems:
        raise SystemExit("Unresolved city forms (add OVERRIDES): "
                         + ", ".join(problems))

    FORMS_FILE.parent.mkdir(parents=True, exist_ok=True)
    FORMS_FILE.write_text(
        "\n".join("|".join((slug, *f)) for slug, f in sorted(forms.items()))
        + "\n", encoding="utf-8")
    return forms


def _service_of(fname: str) -> str | None:
    known = ("ruchnogo-trubogiba", "lentochnyh-pil", "trubogibov",
             "profilgebiv", "valtsev", "armaturogiba", "gilotin",
             "listogibov")
    rest = fname[len("remont-"):-len(".html")]
    for svc in known:
        if rest.startswith(svc + "-"):
            return svc
    return None


def sub_count(pattern, repl, text: str):
    """re.sub that returns (new_text, n_replacements); repl: str or callable."""
    n = 0
    def _count(m):
        nonlocal n
        n += 1
        return m.expand(repl) if isinstance(repl, str) else repl(m)
    return pattern.sub(_count, text), n


# ---------------------------------------------------------------- steps ----

def step_doubled(files, forms, apply: bool, stats: dict) -> int:
    pat = re.compile(r"(<h2>Ремонт [^<]{0,90}? в )([^<]+?)( и Москва</h2>)")
    targets = [p for p, c in files
               if c in ("moskovskiy", "shcherbinka", "zelenograd", "moskva")]
    n_changed = 0
    for path in targets:
        raw = read_raw(path)
        m = pat.search(raw)
        if not m:
            continue
        new = pat.sub(r"\g<1>Москве и Московской области</h2>", raw)
        if new != raw:
            n_changed += 1
            stats["doubled_h2"] = stats.get("doubled_h2", 0) + 1
            if apply:
                write_raw(path, new)
            print(f"  {path.name}: {m.group(0)[:90]} -> "
                  f"{m.group(1)}Москве и Московской области</h2>")
    return n_changed


def step_year(files, forms, apply: bool, stats: dict) -> int:
    n = 0
    for path, city in files:
        if _service_of(path.name) != "valtsev":
            continue
        raw = read_raw(path)
        cnt = raw.count("2025")
        if not cnt:
            continue
        new = raw.replace("2025", "2026")
        stats["year_2025_to_2026"] = stats.get("year_2025_to_2026", 0) + cnt
        n += 1
        if apply:
            write_raw(path, new)
    return n


def step_cjk(scope: list[Path], apply: bool, stats: dict) -> int:
    n = 0
    for path in scope:
        raw = read_raw(path)
        new = raw
        changed = False
        for old, rep in GLOBAL_CJK_SUBS:
            cnt = new.count(old)
            if cnt:
                new = new.replace(old, rep)
                stats[f"cjk:{old[:12]}"] = stats.get(f"cjk:{old[:12]}", 0) + cnt
                changed = True
        arts = ARTICLE_SUBS.get(path.name)
        if arts:
            for old, rep in arts:
                cnt = new.count(old)
                if cnt:
                    new = new.replace(old, rep)
                    stats[f"cjk:{path.name[:24]}"] = \
                        stats.get(f"cjk:{path.name[:24]}", 0) + cnt
                    changed = True
            for old, rep in arts:
                if old.startswith("gócовые"):
                    new, cnt = sub_count(re.compile(r"g[óo]cовые"), rep, new)
                    if cnt:
                        stats[f"cjk:{path.name[:24]}"] = \
                            stats.get(f"cjk:{path.name[:24]}", 0) + cnt
                        changed = True
        if changed:
            n += 1
            if apply:
                write_raw(path, new)
    return n


def make_city_rules(forms_tuple):
    """[(compiled_re, target_form, is_v_prep, tag_aware)] for one city."""
    nom, gen, dat, loc = forms_tuple
    rules = []
    for prep, tgt in (("в", loc), ("по", dat), ("из", gen), ("от", gen),
                      ("по всей", loc)):
        rx = re.compile(
            r"(?<![\wа-яёА-ЯЁ-])(" + prep + r")\s+("
            + re.escape(nom) + r")" + WORD_GUARD, re.I)
        rules.append((rx, tgt, prep == "в", False))
    # «В <strong>{Nom}</strong>» — preposition split from city by a tag
    rx_tag = re.compile(
        r"(?<![\wа-яёА-ЯЁ-])(В|в)(\s*)(<strong>)(" + re.escape(nom)
        + r")(</strong>)", re.I)
    rules.append((rx_tag, loc, True, True))
    return rules


def decline_geo_file(raw: str, rules, pt_noms_lower: set[str], stats: dict):
    changed = False
    for rx, tgt, is_v, tag_aware in rules:
        def _repl(m, tgt=tgt, is_v=is_v, tag_aware=tag_aware):
            src_city = m.group(4) if tag_aware else m.group(2)
            if is_v and src_city.lower() in pt_noms_lower:
                window = raw[max(0, m.start() - 80):m.start()]
                if MOTION_RE.search(window):
                    return m.group(0)
            stats["geo_declined"] = stats.get("geo_declined", 0) + 1
            new_city = preserve_case(src_city, tgt)
            if tag_aware:
                return (m.group(1) + m.group(2) + m.group(3) + new_city
                        + m.group(5))
            return m.group(1) + " " + new_city
        new = rx.sub(_repl, raw)
        if new != raw:
            changed = True
            raw = new
    return raw, changed


def step_geo(files, forms, apply: bool, stats: dict) -> int:
    pt_lower = {n.lower() for n in PLURALIA_TANTUM_NOMS}
    moskva_rules = make_city_rules(forms["moskva"]) if "moskva" in forms else []
    n = 0
    for path, city in files:
        if city not in forms:
            continue
        rules = make_city_rules(forms[city])
        if city != "moskva" and moskva_rules:
            rules += moskva_rules
        raw = read_raw(path)
        new, changed = decline_geo_file(raw, rules, pt_lower, stats)
        if changed:
            n += 1
            if apply:
                write_raw(path, new)
    return n


LATIN_LABELS = {
    "lentochnyh-pil": "Ремонт ленточных пил",
    "ruchnogo-trubogiba": "Ремонт ручных трубогибов",
}


def step_latin(files, forms, apply: bool, stats: dict) -> int:
    n = 0
    for path, city in files:
        svc = _service_of(path.name)
        if svc not in LATIN_LABELS or city not in forms:
            continue
        loc = forms[city][3]
        old = f'"name": "{LATIN_LABELS[svc]} в {city}"'
        new_name = f'"name": "{LATIN_LABELS[svc]} в {loc}"'
        raw = read_raw(path)
        cnt = raw.count(old)
        if cnt:
            raw = raw.replace(old, new_name)
            stats["latin_names"] = stats.get("latin_names", 0) + cnt
            n += 1
            if apply:
                write_raw(path, raw)
    return n


def load_region_gens(root: Path) -> dict[str, str]:
    """city nominative -> oblast genitive phrase («Тверской области»)."""
    data = json.loads((root / "seo-tools" / "data" / "cities.json")
                      .read_text(encoding="utf-8"))
    name2reg = {}
    for d in data:
        name2reg.setdefault(d["name"], d["region"])
    gens: dict[str, str] = {}
    for name, reg in name2reg.items():
        if reg == "Москва":
            gens[name] = "Москве"
        elif reg.endswith("область"):
            adj, _, _ = reg.rpartition(" ")
            gens[name] = adj.replace("ская", "ской") + " области"
    return gens


def step_region(files, forms, root: Path, apply: bool, stats: dict) -> int:
    region_gens = load_region_gens(root)
    mo_introline = re.compile(
        r", Московской области и по всей России")
    mo_short = re.compile(r"(?<![\wа-яёА-ЯЁ-])и МО(?![\wа-яёА-ЯЁ-])")
    mo_by = re.compile(
        r"(?<![\wа-яёА-ЯЁ-])(По|по) Московской области(?![\wа-яёА-ЯЁ-])")
    n = 0
    unknown_regions: set[str] = set()
    for path, city in files:
        if city == "moskva" or city not in forms:
            continue
        nom = forms[city][0]
        if city in MOSCOW_DISTRICT_SLUGS:
            obl_gen = "Москве"
        else:
            obl_gen = region_gens.get(nom)
        if obl_gen is None:
            unknown_regions.add(nom)
            continue
        raw = read_raw(path)
        orig = raw
        if obl_gen != "Московской области":
            raw, c1 = sub_count(mo_introline,
                                f", {obl_gen} и по всей России", raw)
            raw, c2 = sub_count(mo_short, f"и {obl_gen}", raw)
            raw, c4 = sub_count(mo_by,
                                lambda m: f"{m.group(1)} {obl_gen}", raw)
            stats["region_intro"] = stats.get("region_intro", 0) + c1
            stats["region_mo_short"] = stats.get("region_mo_short", 0) + c2
            stats["region_by"] = stats.get("region_by", 0) + c4
        raw, c3 = sub_count(REGION_NOM_RE,
                            lambda m: f"{m.group(1)} "
                                      f"{m.group(2).replace('ская', 'ской')} области",
                            raw)
        stats["region_h2"] = stats.get("region_h2", 0) + c3
        if raw != orig:
            n += 1
            if apply:
                write_raw(path, raw)
    if unknown_regions:
        print(f"  WARN unknown regions for: {sorted(unknown_regions)}")
    return n


def step_warranty(scope: list[Path], apply: bool, stats: dict) -> int:
    targets = scope
    n = 0
    for path in targets:
        raw = read_raw(path)
        orig = raw
        for old, new in WARRANTY_SUBS:
            cnt = raw.count(old)
            if cnt:
                raw = raw.replace(old, new)
                stats["warr:" + old.strip()[:30]] = \
                    stats.get("warr:" + old.strip()[:30], 0) + cnt
        for rx in WARRANTY_BLOCK_RES:
            raw, cnt = sub_count(rx, "", raw)[:2]
            if cnt:
                stats["warr:block"] = stats.get("warr:block", 0) + cnt
        if raw != orig:
            n += 1
            if apply:
                write_raw(path, raw)
    return n


STEPS = ("doubled", "year", "cjk", "geo", "latin", "region", "warranty")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--steps", default="all",
                    help="comma list or 'all': " + ",".join(STEPS))
    ap.add_argument("--apply", action="store_true", help="write changes")
    ap.add_argument("--files", nargs="*", default=[],
                    help="only files whose name contains one of substrings")
    ap.add_argument("--dump-forms", action="store_true",
                    help="print city forms table and exit")
    ap.add_argument("--rebuild-forms", action="store_true")
    args = ap.parse_args()

    out = sys.stdout
    if hasattr(out, "reconfigure"):
        out.reconfigure(encoding="utf-8", errors="replace")

    if args.rebuild_forms and FORMS_FILE.is_file():
        FORMS_FILE.unlink()

    forms = build_city_forms(ROOT)
    if args.dump_forms:
        for slug, f in sorted(forms.items()):
            print("|".join((slug, *f)))
        print(f"total: {len(forms)}", file=sys.stderr)
        return 0

    wanted = STEPS if args.steps == "all" else \
        [s.strip() for s in args.steps.split(",")]
    bad = [s for s in wanted if s not in STEPS]
    if bad:
        raise SystemExit(f"unknown steps: {bad}")

    all_pairs = discover_geo_files(ROOT)
    if args.files:
        all_pairs = [(p, c) for p, c in all_pairs
                     if any(s in p.name for s in args.files)]
    # cjk/warranty operate site-wide; with --files they stay inside the scope
    if args.files:
        wide_scope = sorted(p for p in ROOT.glob("*.html")
                            if any(s in p.name for s in args.files))
    else:
        wide_scope = sorted(ROOT.glob("*.html"))
    print(f"Files in scope: {len(all_pairs)} (wide: {len(wide_scope)}); "
          f"steps: {','.join(wanted)}; "
          f"mode: {'APPLY' if args.apply else 'DRY-RUN'}")

    stats: dict[str, int] = {}
    runners = {
        "doubled": lambda: step_doubled(all_pairs, forms, args.apply, stats),
        "year": lambda: step_year(all_pairs, forms, args.apply, stats),
        "cjk": lambda: step_cjk(wide_scope, args.apply, stats),
        "geo": lambda: step_geo(all_pairs, forms, args.apply, stats),
        "latin": lambda: step_latin(all_pairs, forms, args.apply, stats),
        "region": lambda: step_region(all_pairs, forms, ROOT, args.apply, stats),
        "warranty": lambda: step_warranty(wide_scope, args.apply, stats),
    }
    for step in wanted:
        n = runners[step]()
        print(f"step {step:<9}: {n} files changed")

    if stats:
        print("\nReplacement counts:")
        for k, v in sorted(stats.items()):
            print(f"  {k}: {v}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
