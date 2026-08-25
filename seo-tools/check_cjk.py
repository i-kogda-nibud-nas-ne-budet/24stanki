"""Scan static site HTML files and sitemap.xml for CJK/Japanese/Korean
characters and fused Cyrillic+Latin words (mixed alphabet typos).

Usage:
    python check_cjk.py [--root PATH] [--verbose]
"""

import argparse
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

CJK_RE = re.compile(r"[\u4E00-\u9FFF\u3400-\u4DBF\uF900-\uFAFF\u3040-\u30FF\uAC00-\uD7AF]")
MIXED_RE = re.compile(r"[а-яёА-ЯЁ]+[a-z]+|[a-z]+[а-яёА-ЯЁ]+")

REPORT = Path(__file__).resolve().parent / "reports" / "check_cjk_report.txt"


@dataclass
class FileFindings:
    """Per-file scan results."""

    path: Path
    cjk_count: int = 0
    mixed: Counter[str] = field(default_factory=Counter)
    examples: list[str] = field(default_factory=list)


def iter_targets(root: Path) -> list[Path]:
    """Return root *.html files plus sitemap.xml if present."""
    targets = sorted(root.glob("*.html"))
    sitemap = root / "sitemap.xml"
    if sitemap.is_file():
        targets.append(sitemap)
    return targets


def collect_examples(text: str, needles: list[str], limit: int = 5) -> list[str]:
    """Return up to `limit` trimmed lines containing any needle."""
    out: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped and any(n in line for n in needles):
            out.append(stripped[:120])
            if len(out) >= limit:
                break
    return out


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def scan_file(path: Path) -> FileFindings | None:
    """Scan one file; return findings or None if clean."""
    text = read_text(path)
    cjk_matches = CJK_RE.findall(text)
    mixed = Counter(MIXED_RE.findall(text))
    if not cjk_matches and not mixed:
        return None
    needles = list(dict.fromkeys(cjk_matches))[:5] + sorted(mixed)[:5]
    return FileFindings(
        path=path,
        cjk_count=len(cjk_matches),
        mixed=mixed,
        examples=collect_examples(text, needles),
    )


def write_report(root: Path, checked: int, findings: list[FileFindings]) -> None:
    """Write the full report file."""
    lines = [
        "CJK / MIXED ALPHABET SCAN REPORT",
        f"root: {root}",
        f"checked files: {checked}",
        f"files with findings: {len(findings)}",
        f"total CJK chars: {sum(f.cjk_count for f in findings)}",
        "",
    ]
    if findings:
        lines.append("TOP FILES BY CJK COUNT")
        top = sorted(findings, key=lambda f: (-f.cjk_count, str(f.path)))[:20]
        for i, f in enumerate(top, 1):
            lines.append(f"{i:>3}. {f.cjk_count:>6}  {f.path.name}")
        lines.append("")
    for f in findings:
        lines.append(f"[FILE] {f.path.name}")
        lines.append(f"  CJK chars: {f.cjk_count}")
        lines.append(f"  MIXED_ALPHABET ({sum(f.mixed.values())} hits, {len(f.mixed)} unique):")
        for word, cnt in sorted(f.mixed.items()):
            lines.append(f"    - {word!r} x{cnt}")
        if f.examples:
            lines.append("  Examples:")
            for ex in f.examples:
                lines.append(f"    | {ex}")
        lines.append("")
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    default_root = Path(__file__).resolve().parent.parent
    parser.add_argument("--root", type=Path, default=default_root, help="site root dir")
    parser.add_argument("--verbose", action="store_true", help="show up to 5 example lines per file")
    args = parser.parse_args()

    stdout = sys.stdout
    if hasattr(stdout, "reconfigure"):
        stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]

    targets = iter_targets(args.root)
    findings: list[FileFindings] = []
    for path in targets:
        result = scan_file(path)
        if result is not None:
            findings.append(result)
            if args.verbose:
                print(f"\n{path.name}: CJK={result.cjk_count}, "
                      f"mixed={len(result.mixed)} unique")
                for ex in result.examples:
                    print(f"  | {ex}")

    total_cjk = sum(f.cjk_count for f in findings)
    total_mixed_hits = sum(sum(f.mixed.values()) for f in findings)

    print(f"Checked files: {len(targets)}")
    print(f"Files with findings: {len(findings)}")
    print(f"Total CJK chars: {total_cjk}")
    print(f"Total mixed-alphabet hits: {total_mixed_hits}")

    by_cjk = sorted(findings, key=lambda f: -f.cjk_count)[:20]
    if by_cjk:
        print("\nTop-20 files by CJK count:")
        for f in by_cjk:
            print(f"  {f.cjk_count:>6}  {f.path.name}")

    write_report(args.root, len(targets), findings)
    print(f"\nReport: {REPORT}")

    return 0 if not findings else 1


if __name__ == "__main__":
    sys.exit(main())
