"""Measure cross-city text similarity within one geo-page group.

Cleans HTML to plain lowercase text, builds word k-shingles and computes
pairwise Jaccard coefficients for a random sample of pages.

Usage:
    python check_dupl.py [--group trubogibov] [--sample 12] [--shingle 5]
                         [--seed 42] [--root PATH]
"""

import argparse
import html as html_lib
import random
import re
import sys
from itertools import combinations
from pathlib import Path

REPORT_DIR = Path(__file__).resolve().parent / "reports"


def clean_html(raw: str) -> str:
    """HTML -> plain lowercase text, whitespace collapsed."""
    text = re.sub(r"<(script|style)\b[^>]*>.*?</\1>", " ", raw, flags=re.S | re.I)
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", html_lib.unescape(text)).lower()


def make_shingles(text: str, size: int) -> set[str]:
    """Word shingles of given size; whole text as one shingle if shorter."""
    words = text.split()
    if len(words) < size:
        return {" ".join(words)} if words else set()
    return {" ".join(words[i:i + size]) for i in range(len(words) - size + 1)}


def jaccard(a: set[str], b: set[str]) -> float:
    """Jaccard coefficient of two sets; 0.0 if both empty."""
    if not a and not b:
        return 0.0
    return len(a & b) / len(a | b)


def bucket(percent: float) -> str:
    """Histogram bucket label for a similarity percentage."""
    if percent < 70:
        return "<70"
    if percent < 85:
        return "70-85"
    if percent < 95:
        return "85-95"
    return ">95"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    default_root = Path(__file__).resolve().parent.parent
    parser.add_argument("--group", default="trubogibov", help="service group slug")
    parser.add_argument("--sample", type=int, default=12, help="pages to sample")
    parser.add_argument("--shingle", type=int, default=5, help="shingle size in words")
    parser.add_argument("--seed", type=int, default=42, help="random seed")
    parser.add_argument("--root", type=Path, default=default_root, help="site root dir")
    args = parser.parse_args()

    stdout = sys.stdout
    if hasattr(stdout, "reconfigure"):
        stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]

    files = sorted(args.root.glob(f"remont-{args.group}-*.html"))
    picked_count = min(args.sample, len(files))
    picked = sorted(random.Random(args.seed).sample(files, picked_count))

    texts: dict[str, set[str]] = {}
    for path in picked:
        texts[path.name] = make_shingles(clean_html(path.read_text(encoding="utf-8", errors="replace")), args.shingle)

    pairs: list[tuple[float, str, str]] = []
    for (name_a, sh_a), (name_b, sh_b) in combinations(sorted(texts.items()), 2):
        pairs.append((jaccard(sh_a, sh_b) * 100, name_a, name_b))
    pairs.sort(reverse=True)

    avg = sum(p[0] for p in pairs) / len(pairs) if pairs else 0.0
    hist: dict[str, int] = {"<70": 0, "70-85": 0, "85-95": 0, ">95": 0}
    for percent, _, _ in pairs:
        hist[bucket(percent)] += 1

    print(f"Group: {args.group} | files found: {len(files)} | sampled: {picked_count} "
          f"| pairs: {len(pairs)}")
    print(f"Average similarity: {avg:.2f}%")
    if pairs:
        top_pct, top_a, top_b = pairs[0]
        print(f"Max pair ({top_pct:.2f}%): {top_a} <-> {top_b}")
    print("\nTop-5 pairs:")
    for percent, name_a, name_b in pairs[:5]:
        print(f"  {percent:6.2f}%  {name_a} <-> {name_b}")
    print("\nHistogram:")
    for label in ("<70", "70-85", "85-95", ">95"):
        bar = "#" * min(hist[label], 50)
        print(f"  {label:>5}: {hist[label]:>4}  {bar}")

    report_lines = [
        f"DUPLICATION REPORT: group={args.group}",
        f"root: {args.root}",
        f"files in group: {len(files)}, sampled: {picked_count}, "
        f"pairs: {len(pairs)}, avg: {avg:.2f}%",
        f"histogram: {hist}",
        "",
    ]
    report_lines.extend(f"{percent:6.2f}%  {name_a} <-> {name_b}" for percent, name_a, name_b in pairs)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    report = REPORT_DIR / f"check_dupl_{args.group}_report.txt"
    report.write_text("\n".join(report_lines), encoding="utf-8")
    print(f"\nReport: {report}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
