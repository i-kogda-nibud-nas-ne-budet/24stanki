"""Structural integrity audit of all root HTML files.

Checks:
    TAG_BALANCE   - unclosed or stray-closed structural tags          (error)
    BAD_JSONLD    - <script type="application/ld+json"> fails json    (error)
    MISSING_FILE  - internal href/src points to non-existent file     (error)
    NO_VIEWPORT   - no <meta name="viewport">                         (error)

Usage:
    python check_structure.py [--root PATH] [--limit N]
"""

import argparse
import json
import re
import sys
import urllib.parse
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

TRACKED_TAGS = {
    "div", "section", "table", "ul", "nav", "header", "footer", "form",
    "h1", "h2", "h3", "h4", "h5", "h6",
}
EXTERNAL_PREFIXES = ("http://", "https://", "mailto:", "tel:", "#", "//", "javascript:", "data:")

ERROR_TYPES = ("TAG_BALANCE", "BAD_JSONLD", "MISSING_FILE", "NO_VIEWPORT")
REPORT_DIR = Path(__file__).resolve().parent / "reports"


class AuditParser(HTMLParser):
    """Collects tag balance, JSON-LD blocks, internal links, viewport flag."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.open_counts: Counter[str] = Counter()
        self.extra_closes: list[str] = []
        self.ldjson_blocks: list[str] = []
        self.links: list[str] = []
        self.has_viewport = False
        self._in_ldjson = False
        self._buffer: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in TRACKED_TAGS:
            self.open_counts[tag] += 1
        attr_dict = {k: (v or "") for k, v in attrs}
        if tag == "meta" and attr_dict.get("name", "").lower() == "viewport":
            self.has_viewport = True
        if tag == "script" and 'application/ld+json' in attr_dict.get("type", "").lower():
            self._in_ldjson = True
            self._buffer = []
        for key in ("href", "src"):
            value = attr_dict.get(key)
            if value:
                self.links.append(value.strip())

    def handle_data(self, data: str) -> None:
        if self._in_ldjson:
            self._buffer.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag in TRACKED_TAGS:
            if self.open_counts[tag] > 0:
                self.open_counts[tag] -= 1
            else:
                self.extra_closes.append(tag)
        if tag == "script":
            if self._in_ldjson:
                self.ldjson_blocks.append("".join(self._buffer))
                self._in_ldjson = False
                self._buffer = []


def tag_balance_problems(parser: AuditParser) -> str | None:
    """Human-readable balance summary; None when balanced."""
    unclosed = sorted(t for t, n in parser.open_counts.items() if n > 0)
    parts = [f"unclosed <{t}> x{parser.open_counts[t]}" for t in unclosed]
    parts.extend(f"stray </{t}>" for t in parser.extra_closes)
    return "; ".join(parts) if parts else None


def resolve_link(link: str, root: Path) -> Path | None:
    """Internal link -> local file path; None for external/pure-anchor links."""
    if not link or link.startswith(EXTERNAL_PREFIXES):
        return None
    base = urllib.parse.unquote(link.split("#", 1)[0].split("?", 1)[0].strip())
    if not base:
        return None
    candidate = root / base.lstrip("/\\") if base.startswith("/") else root / base
    return candidate


def check_file(path: Path, root: Path) -> list[tuple[str, str]]:
    """All structural checks for one file; returns (type, fragment) pairs."""
    raw = path.read_text(encoding="utf-8", errors="replace")
    parser = AuditParser()
    try:
        parser.feed(raw)
        parser.close()
    except Exception as exc:  # malformed markup that crashes the parser
        return [("TAG_BALANCE", f"parser error: {exc}")]

    found: list[tuple[str, str]] = []

    balance = tag_balance_problems(parser)
    if balance:
        found.append(("TAG_BALANCE", balance))

    for block in parser.ldjson_blocks:
        try:
            json.loads(block)
        except json.JSONDecodeError as exc:
            snippet = re.sub(r"\s+", " ", block)[:80]
            found.append(("BAD_JSONLD", f"{exc.msg} at line {exc.lineno}: {snippet}"))

    seen_links: set[str] = set()
    for link in parser.links:
        target = resolve_link(link, root)
        if target is None or link in seen_links:
            continue
        seen_links.add(link)
        if not target.is_file():
            found.append(("MISSING_FILE", link[:100]))

    if not parser.has_viewport:
        found.append(("NO_VIEWPORT", "no <meta name=\"viewport\">"))

    return found


def main() -> int:
    parser_args = argparse.ArgumentParser(description=__doc__)
    default_root = Path(__file__).resolve().parent.parent
    parser_args.add_argument("--root", type=Path, default=default_root, help="site root dir")
    parser_args.add_argument("--limit", type=int, default=0, help="check only first N files")
    args = parser_args.parse_args()

    stdout = sys.stdout
    if hasattr(stdout, "reconfigure"):
        stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]

    files = sorted(args.root.glob("*.html"))
    if args.limit > 0:
        files = files[: args.limit]

    per_type: dict[str, list[tuple[str, str]]] = {t: [] for t in ERROR_TYPES}
    files_with_errors = 0
    for path in files:
        findings = check_file(path, args.root)
        if findings:
            files_with_errors += 1
            for ftype, frag in findings:
                per_type[ftype].append((path.name, frag))

    print(f"Files checked: {len(files)}")
    print(f"Files with errors: {files_with_errors}")
    print(f"\n{'TYPE':<14}{'COUNT':>7}")
    for ftype in ERROR_TYPES:
        print(f"{ftype:<14}{len(per_type[ftype]):>7}")

    report_lines = [
        "STRUCTURE AUDIT REPORT",
        f"root: {args.root}",
        f"checked: {len(files)}",
        f"files with errors: {files_with_errors}",
        "",
    ]
    print()
    for ftype in ERROR_TYPES:
        hits = per_type[ftype]
        report_lines.append(f"{ftype}: {len(hits)}")
        print(f"[{ftype}] top examples:")
        for fname, frag in hits[:10]:
            print(f"  {fname}: {frag}")
        for fname, frag in hits:
            report_lines.append(f"  {fname}: {frag}")
        report_lines.append("")

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    report = REPORT_DIR / "check_structure_report.txt"
    report.write_text("\n".join(report_lines), encoding="utf-8")
    print(f"Report: {report}")

    total_errors = sum(len(per_type[t]) for t in ERROR_TYPES)
    return 0 if total_errors == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
