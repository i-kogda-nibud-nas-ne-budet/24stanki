#!/usr/bin/env python3
"""Fix orphaned </div> left after CTA was moved outside footer in geo pages."""

import re
import glob
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def fix_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Pattern: </footer>\n\n    </div>\n\n<!-- ===== CTA ===== -->
    # Replace with: </footer>\n\n<!-- ===== CTA ===== -->
    new_content = re.sub(
        r'</footer>\s*\n\s*\n\s*</div>\s*\n\s*\n<!-- ===== CTA ===== -->',
        '</footer>\n\n<!-- ===== CTA ===== -->',
        content,
    )

    if new_content != content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        return True
    return False


def main():
    pattern = os.path.join(ROOT, "remont-*-*.html")
    files = sorted(glob.glob(pattern))
    print(f"Found {len(files)} geo pages")

    fixed = 0
    for filepath in files:
        if fix_file(filepath):
            fixed += 1

    print(f"Fixed {fixed} files")


if __name__ == "__main__":
    main()
