"""Validate geo landing pages: remont-{service}-{city}.html.

Checks:
    YEAR_2025     - <title> contains "2025"                        (error)
    LATIN_SLUG    - latin city slug inside JSON-LD "name"           (error)
    DOUBLED_WORD  - same word repeated twice in a row               (error)
    CASE_NOM      - nominative city form after preposition          (error)
    PT_WARNING    - motion word + nominative pluralia-tantum city   (warning)
    REGION_MO     - mentions of Moscow region                       (info)
    WARRANTY      - warranty-on-works mentions                      (info)

Usage:
    python check_geo.py [--root PATH] [--limit N] [--type TYPE]
"""

import argparse
import html as html_lib
import re
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

SERVICES = (
    "trubogibov",
    "profilgebiv",
    "ruchnogo-trubogiba",
    "valtsev",
    "armaturogiba",
    "gilotin",
    "lentochnyh-pil",
    "listogibov",
)

ERROR_TYPES = ("YEAR_2025", "LATIN_SLUG", "DOUBLED_WORD", "CASE_NOM")
WARN_TYPES = ("PT_WARNING",)
INFO_TYPES = ("REGION_MO", "WARRANTY")
ALL_TYPES = ERROR_TYPES + WARN_TYPES + INFO_TYPES

# Cities whose nominative form looks plural; «в Химки» after a motion word
# («Выезд мастера в Химки») is grammatically valid -> warning, not error.
PLURALIA_TANTUM = {
    "Мытищи", "Химки", "Люберцы", "Озёры", "Луховицы", "Вязники", "Петушки",
    "Меленки", "Сухиничи", "Котельники", "Бронницы", "Кимры",
}

TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.S | re.I)
LATIN_NAME_RE = re.compile(r'"name":\s*"[^"]*\b(?:в|in) [a-z][a-z-]{2,}')
DOUBLED_RE = re.compile(r"\b([А-ЯЁа-яё]+)\b(?:\s+и\s+|\s+)\1\b", re.IGNORECASE)
WARRANTY_RE = re.compile(
    r"гарантия[^.<]{0,40}(?:месяц|год)|гарантия\s+\d|до\s*12\s*месяцев", re.I
)
# Motion verbs/nouns before which a pluralia-tantum accusative is grammatical.
MOTION_RE = re.compile(
    r"\b(?:выезд\w*|приезд\w*|поездк\w*|выезжаем|выезжает|выедем|приезжаем|"
    r"приедет|приедем|ездим|ездит|едем|поедем|отправля\w*|достави\w*|"
    r"добраться|прибытие|прибуде\w*)\b",
    re.I,
)
GEO_FILE_RE = re.compile(
    r"remont-(" + "|".join(sorted(SERVICES, key=len, reverse=True)) + r")-([a-z0-9-]+)\.html"
)

# slug -> nominative Russian name; used when city_mapping.txt is absent.
FALLBACK_CITIES: dict[str, str] = {
    "moskva": "Москва",
    "sankt-peterburg": "Санкт-Петербург",
    "moskovskiy": "Московский",
    "zelenograd": "Зеленоград",
    "troitsk": "Троицк",
    "mytishchi": "Мытищи",
    "balashikha": "Балашиха",
    "podolsk": "Подольск",
    "khimki": "Химки",
    "korolyov": "Королёв",
    "lyubertsy": "Люберцы",
    "krasnogorsk": "Красногорск",
    "odintsovo": "Одинцово",
    "domodedovo": "Домодедово",
    "shchelkovo": "Щёлково",
    "shchyolkovo": "Щёлково",
    "pushkino": "Пушкино",
    "ramenskoe": "Раменское",
    "ramenskoye": "Раменское",
    "sergiev-posad": "Сергиев Посад",
    "pavlovskiy-posad": "Павловский Посад",
    "naro-fominsk": "Наро-Фоминск",
    "losino-petrovskiy": "Лосино-Петровский",
    "orekhovo-zuevo": "Орехово-Зуево",
    "likino-dulyovo": "Ликино-Дулёво",
    "staraya-kupavna": "Старая Купавна",
    "elektrostal": "Электросталь",
    "kolomna": "Коломна",
    "serpukhov": "Серпухов",
    "dmitrov": "Дмитров",
    "klin": "Клин",
    "vidnoe": "Видное",
    "dzerzhinskiy": "Дзержинский",
    "reutov": "Реутов",
    "fryazino": "Фрязино",
    "ivanteevka": "Ивантеевка",
    "pushchino": "Пущино",
    "protvino": "Протвино",
    "obninsk": "Обнинск",
    "tver": "Тверь",
    "ryazan": "Рязань",
    "tula": "Тула",
    "kaluga": "Калуга",
    "vladimir": "Владимир",
    "smolensk": "Смоленск",
    "yaroslavl": "Ярославль",
    "rybinsk": "Рыбинск",
    "kostroma": "Кострома",
    "ivanovo": "Иваново",
    "kirov": "Киров",
    "kovrov": "Ковров",
    "murom": "Муром",
    "novomoskovsk": "Новомосковск",
    "uzlovaya": "Узловая",
    "aleksin": "Алексин",
    "ozyory": "Озёры",
    "kurovskoe": "Куровское",
    "rybnoe": "Рыбное",
    "belyov": "Белёв",
    "vereya": "Верея",
    "gus-khrustalnyy": "Гусь-Хрустальный",
    "pereslavl-zalesskiy": "Переславль-Залесский",
    "rostov-velikiy": "Ростов Великий",
    "krasnyy-kholm": "Красный Холм",
    "vyshniy-volochyok": "Вышний Волочёк",
    "yurev-polskiy": "Юрьев-Польский",
    "zapadnaya-dvina": "Западная Двина",
    "spassk-ryazanskiy": "Спасск-Рязанский",
    "spas-klepiki": "Спас-Клепики",
    "spas-demensk": "Спас-Деменск",
}

REPORT_DIR = Path(__file__).resolve().parent / "reports"


@dataclass
class Finding:
    """One check hit inside one file."""

    ftype: str
    frag: str


def extract_text(page: str) -> str:
    """Strip script/style/comments/tags; collapse whitespace; unescape."""
    text = re.sub(r"<(script|style)\b[^>]*>.*?</\1>", " ", page, flags=re.S | re.I)
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", html_lib.unescape(text))


def context(text: str, start: int, end: int) -> str:
    """Fragment around a match, max 100 chars."""
    lo = max(0, start - 25)
    return text[lo:max(end, start + 75)][:100]


def discover_geo_files(root: Path) -> list[tuple[Path, str]]:
    """Return (path, city_slug) for all remont-{service}-{city}.html files."""
    pairs: list[tuple[Path, str]] = []
    for path in sorted(root.glob("remont-*.html")):
        match = GEO_FILE_RE.fullmatch(path.name)
        if match:
            pairs.append((path, match.group(2)))
    return pairs


def load_city_names(cities: set[str]) -> dict[str, str]:
    """slug -> nominative name from city_mapping.txt, else fallback/capitalize."""
    names: dict[str, str] = {}
    mapping_file = Path(__file__).resolve().parent / "city_mapping.txt"
    if mapping_file.is_file():
        for line in mapping_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and "|" in line:
                slug, nom = line.split("|", 1)
                names[slug.strip()] = nom.strip()
    for slug in cities:
        if slug not in names:
            names[slug] = FALLBACK_CITIES.get(slug, "-".join(p.capitalize() for p in slug.split("-")))
    return names


def case_nom_patterns(names: dict[str, str]) -> list[tuple[str, re.Pattern[str]]]:
    """(city, regex) pairs matching preposition + undeclined nominative."""
    out: list[tuple[str, re.Pattern[str]]] = []
    seen: set[str] = set()
    for slug, nom in names.items():
        if nom in seen or not nom:
            continue
        seen.add(nom)
        pattern = re.compile(
            r"(?<![\w-])(в|по|из|от)\s+" + re.escape(nom) + r"(?![\w-])", re.I
        )
        out.append((nom, pattern))
    return sorted(out)


def is_pt_motion(text: str, prep: str, pos: int) -> bool:
    """True when «в» + pluralia-tantum city follows a motion word nearby."""
    if prep.lower() != "в":
        return False
    before = text[max(0, pos - 80):pos]
    return bool(MOTION_RE.search(before))


def check_file(path: Path, city: str, nom_patterns: list[tuple[str, re.Pattern[str]]]) -> list[Finding]:
    """Run all checks on one geo page."""
    raw = path.read_text(encoding="utf-8", errors="replace")
    text = extract_text(raw)
    found: list[Finding] = []

    title_match = TITLE_RE.search(raw)
    title = html_lib.unescape(title_match.group(1)).strip() if title_match else ""
    if "2025" in title:
        found.append(Finding("YEAR_2025", title[:100]))

    latin = LATIN_NAME_RE.search(raw)
    if latin:
        found.append(Finding("LATIN_SLUG", latin.group(0)[:100]))

    for word_match in DOUBLED_RE.finditer(text):
        found.append(Finding("DOUBLED_WORD", context(text, word_match.start(), word_match.end())))

    for nom, pattern in nom_patterns:
        for nom_match in pattern.finditer(text):
            ftype = (
                "PT_WARNING"
                if nom in PLURALIA_TANTUM and is_pt_motion(text, nom_match.group(1), nom_match.start())
                else "CASE_NOM"
            )
            found.append(Finding(ftype, context(text, nom_match.start(), nom_match.end())))

    mo_pos = min(
        (text.find(sub) for sub in ("Московской области", "и МО", "по МО") if sub in text),
        default=-1,
    )
    if mo_pos >= 0:
        found.append(Finding("REGION_MO", context(text, mo_pos, mo_pos + 20)))

    warranty = WARRANTY_RE.search(text)
    if warranty:
        found.append(Finding("WARRANTY", context(text, warranty.start(), warranty.end())))
    return found


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    default_root = Path(__file__).resolve().parent.parent
    parser.add_argument("--root", type=Path, default=default_root, help="site root dir")
    parser.add_argument("--limit", type=int, default=0, help="check only first N files")
    parser.add_argument("--type", choices=ALL_TYPES, default=None, help="show only this finding type")
    args = parser.parse_args()

    stdout = sys.stdout
    if hasattr(stdout, "reconfigure"):
        stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]

    geo_files = discover_geo_files(args.root)
    if args.limit > 0:
        geo_files = geo_files[: args.limit]

    names = load_city_names({city for _, city in geo_files})
    nom_patterns = case_nom_patterns(names)

    per_type: dict[str, list[tuple[str, str]]] = {t: [] for t in ALL_TYPES}
    files_with_errors = 0
    for path, city in geo_files:
        findings = check_file(path, city, nom_patterns)
        if not findings:
            continue
        error_here = any(f.ftype in ERROR_TYPES for f in findings)
        files_with_errors += int(error_here)
        for f in findings:
            per_type[f.ftype].append((path.name, f.frag))

    shown_types = [args.type] if args.type else list(ALL_TYPES)

    print(f"Geo pages checked: {len(geo_files)}")
    print(f"Files with errors: {files_with_errors}")
    print("\n{:<14} {:>10} {:>7}  {}".format("TYPE", "HITS", "FILES", "CLASS"))
    for ftype in shown_types:
        hits = per_type[ftype]
        cls = (
            "ERROR"
            if ftype in ERROR_TYPES
            else ("WARNING" if ftype in WARN_TYPES else "INFO")
        )
        n_files = len({fname for fname, _ in hits})
        print("{:<14} {:>10} {:>7}  {}".format(ftype, len(hits), n_files, cls))

    report_lines = [
        "GEO PAGES VALIDATION REPORT",
        f"root: {args.root}",
        f"checked: {len(geo_files)}",
        f"files with errors: {files_with_errors}",
        "",
    ]
    for ftype in shown_types:
        hits = per_type[ftype]
        cls = (
            "ERROR"
            if ftype in ERROR_TYPES
            else ("WARNING" if ftype in WARN_TYPES else "INFO")
        )
        n_files = len({fname for fname, _ in hits})
        report_lines.append(f"{ftype} ({cls}): {len(hits)} hits / {n_files} files")
        for fname, frag in hits[:10]:
            print(f"  [{ftype}] {fname}: {frag}")
        for fname, frag in hits:
            report_lines.append(f"  {fname}: {frag}")
        report_lines.append("")
        print()

    report = REPORT_DIR / "check_geo_report.txt"
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    report.write_text("\n".join(report_lines), encoding="utf-8")
    print(f"Report: {report}")

    active_errors = sum(len(per_type[t]) for t in ERROR_TYPES if t in shown_types)
    return 0 if active_errors == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
