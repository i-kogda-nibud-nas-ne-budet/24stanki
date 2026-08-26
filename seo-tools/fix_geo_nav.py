#!/usr/bin/env python3
"""Fix old nav structure in all geo pages and move CTA outside footer."""

import re
import glob
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

NEW_NAV = """    <!-- ===== NAVIGATION ===== -->
<nav class="nav" id="nav">
    <div class="nav-inner">
        <a href="index.html" class="nav-logo">24<span>STANKI</span></a>
        <div class="nav-links">
            <div class="dropdown">
                <a href="uslugi.html" class="dropbtn">Услуги ▾</a>
                <div class="dropdown-content">
{dropdown_links}
                </div>
            </div>
            <a href="price.html">Цены</a>
            <a href="portfolio.html">Портфолио</a>
            <a href="blog.html">Блог</a>
            <a href="tel:89939089837" class="nav-cta">📞 8 (993) 908-98-37</a>
        </div>
        <button class="hamburger" aria-label="Меню">
            <span></span><span></span><span></span>
        </button>
    </div>
</nav>
<div class="nav-mobile">
    <a href="index.html">Главная</a>
    <a href="uslugi.html">Услуги</a>
{mobile_links}
    <a href="price.html">Цены</a>
    <a href="portfolio.html">Портфолио</a>
    <a href="blog.html">Блог</a>
    <a href="tel:89939089837" class="btn btn-primary">📞 Позвонить</a>
    <a href="https://wa.me/79939089837" class="btn btn-outline">💬 WhatsApp</a>
</div>"""

OLD_NAV_RE = re.compile(
    r'    <header>\s*\n\s*<nav>\s*\n'
    r'.*?'
    r'\s*</nav>\s*\n\s*</header>',
    re.DOTALL,
)

DROPDOWN_LINK_RE = re.compile(
    r'<a\s+href="([^"]+)"[^>]*>([^<]+)</a>'
)

CTA_SECTION_RE = re.compile(
    r'(?P<before>.*?)(?P<footer_open><!-- ===== FOOTER ===== -->\s*\n<footer class="footer">\s*\n\s*<div class="container">\s*\n\s*<div class="footer-grid">.*?<!-- ===== CTA ===== -->\s*\n<section class="section">\s*\n\s*<div class="container">\s*\n\s*<div class="cta-section">.*?</section>\s*\n\s*</footer>)(?P<after>.*)',
    re.DOTALL,
)

CTA_BLOCK_RE = re.compile(
    r'(<!-- ===== CTA ===== -->\s*\n<section class="section">.*?</section>)\s*\n\s*</footer>',
    re.DOTALL,
)

FOOTER_CLOSE_RE = re.compile(
    r'(<!-- ===== CTA ===== -->\s*\n<section class="section">.*?</section>)\s*\n\s*</footer>',
    re.DOTALL,
)

# Simpler: find the CTA block inside footer and move it after </footer>
CTA_IN_FOOTER_RE = re.compile(
    r'(</div>\s*\n\s*</div>\s*\n\s*<!-- ===== CTA ===== -->\s*\n<section class="section">\s*\n\s*<div class="container">\s*\n\s*<div class="cta-section">.*?</section>)\s*\n\s*</footer>',
    re.DOTALL,
)


def extract_dropdown_links(old_nav_html):
    """Extract links from the dropdown-content div in the old nav."""
    dropdown_match = re.search(
        r'<div class="dropdown-content">(.*?)</div>',
        old_nav_html,
        re.DOTALL,
    )
    if not dropdown_match:
        return [], []
    links_html = dropdown_match.group(1)
    links = DROPDOWN_LINK_RE.findall(links_html)

    dropdown_lines = []
    mobile_lines = []
    for href, text in links:
        is_active = 'class="active"' in links_html.split('href="{}"'.format(href))[1].split('</a>')[0] if 'href="{}"'.format(href) in links_html else False
        indent = "                    "
        active_attr = ' class="active"' if is_active else ''
        dropdown_lines.append('{}<a href="{}"{}>{}</a>'.format(indent, href, active_attr, text))
        mobile_style = ' style="padding-left:2rem;font-size:0.9em"' if href.startswith('remont-') else ''
        mobile_prefix = "→ " if href.startswith('remont-') else ""
        mobile_lines.append(f'    <a href="{href}"{mobile_style}>{mobile_prefix}{text}</a>')

    return "\n".join(dropdown_lines), "\n".join(mobile_lines)


def fix_file(filepath):
    """Fix a single geo HTML file."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    changed = False

    # 1. Replace old nav with new nav
    old_nav_match = OLD_NAV_RE.search(content)
    if old_nav_match:
        old_nav = old_nav_match.group(0)
        dropdown_links, mobile_links = extract_dropdown_links(old_nav)
        new_nav = NEW_NAV.format(
            dropdown_links=dropdown_links,
            mobile_links=mobile_links,
        )
        content = content[:old_nav_match.start()] + new_nav + content[old_nav_match.end():]
        changed = True

    # 2. Move CTA outside footer
    # Original: ...</div>\n\n<!-- CTA -->...</section>\n\n</footer>
    # Target:   ...</div>\n\n</footer>\n\n<!-- CTA -->...</section>
    cta_match = re.search(
        r'(    </div>\s*\n\s*\n<!-- ===== CTA ===== -->\s*\n<section class="section">.*?</section>)\s*\n\s*</footer>',
        content,
        re.DOTALL,
    )
    if cta_match:
        cta_block = cta_match.group(1)
        content = content[:cta_match.start()] + "\n</footer>\n\n" + cta_block + "\n" + content[cta_match.end():]
        changed = True

    if changed:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    return False


def main():
    pattern = os.path.join(ROOT, "remont-*-*.html")
    files = sorted(glob.glob(pattern))
    print(f"Found {len(files)} geo pages")

    # Skip the files we already fixed manually
    skip = {"remont-listogibov-moskva.html"}

    fixed = 0
    skipped = 0
    errors = []

    for filepath in files:
        basename = os.path.basename(filepath)
        if basename in skip:
            print(f"  SKIP (already fixed): {basename}")
            skipped += 1
            continue
        try:
            if fix_file(filepath):
                fixed += 1
            else:
                print(f"  NO CHANGE: {basename}")
        except Exception as e:
            errors.append((basename, str(e)))
            print(f"  ERROR: {basename}: {e}")

    print(f"\nDone: {fixed} fixed, {skipped} skipped, {len(errors)} errors")
    if errors:
        print("\nErrors:")
        for name, err in errors:
            print(f"  {name}: {err}")


if __name__ == "__main__":
    main()
