#!/usr/bin/env python3
"""Этап 1: Технические исправления — canonical, OG, breadcrumb, падеж, sitemap, robots"""

import os
import re
from pathlib import Path
from datetime import datetime

BASE = Path('.')
EXCLUDE = {'preview.html', 'google1e0151116e608a2e.html', 'yandex_32e5528f50fd0785.html'}

# Stats
stats = {
    'canonical_added': 0,
    'canonical_skipped': 0,
    'og_added': 0,
    'og_skipped': 0,
    'breadcrumb_added': 0,
    'breadcrumb_skipped': 0,
    'declension_fixed': 0,
    'total_files': 0,
    'errors': []
}


def get_all_html():
    """Get all HTML files, sorted."""
    files = []
    for f in BASE.glob('*.html'):
        if f.name not in EXCLUDE:
            files.append(f)
    return sorted(files)


def fix_declension(content, filename):
    """Fix 'в Московская область' → 'в Московской области'"""
    count = 0
    new_content = content.replace('в Московская область', 'в Московской области')
    count = content.count('в Московская область')
    return new_content, count


def add_canonical(content, filename):
    """Add canonical tag if missing."""
    if 'rel="canonical"' in content:
        return content, False
    
    canonical_url = f'https://24stanki.ru/{filename}'
    canonical_tag = f'<link rel="canonical" href="{canonical_url}" />'
    
    # Try to add before </head>
    if '</head>' in content:
        new_content = content.replace('</head>', f'    {canonical_tag}\n</head>', 1)
        return new_content, True
    
    # Try to add before </title> area as fallback
    if '<title>' in content:
        # Add after first meta description
        pattern = r'(<meta\s+name="description"[^>]*>)'
        match = re.search(pattern, content)
        if match:
            pos = match.end()
            new_content = content[:pos] + f'\n    {canonical_tag}' + content[pos:]
            return new_content, True
    
    return content, False


def add_og_tags(content, filename):
    """Add OG tags if missing."""
    if 'og:title' in content:
        return content, False
    
    # Extract title
    title_match = re.search(r'<title>(.*?)</title>', content, re.DOTALL)
    title = title_match.group(1).strip() if title_match else filename.replace('.html', '').replace('-', ' ').title()
    
    # Extract description
    desc_match = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', content)
    description = desc_match.group(1) if desc_match else title
    
    og_tags = f'''    <meta property="og:type" content="website" />
    <meta property="og:url" content="https://24stanki.ru/{filename}" />
    <meta property="og:title" content="{title}" />
    <meta property="og:description" content="{description}" />
    <meta property="og:image" content="https://24stanki.ru/images/telegram-preview.jpg" />
    <meta property="og:locale" content="ru_RU" />'''
    
    # Add before </head>
    if '</head>' in content:
        new_content = content.replace('</head>', f'{og_tags}\n</head>', 1)
        return new_content, True
    
    return content, False


def add_breadcrumb_script(content, filename):
    """Add breadcrumb.js script if missing."""
    if 'breadcrumb.js' in content:
        return content, False
    
    # Add before script.js
    if '<script src="script.js"></script>' in content:
        new_content = content.replace(
            '<script src="script.js"></script>',
            '<script src="breadcrumb.js"></script>\n<script src="script.js"></script>',
            1
        )
        return new_content, True
    
    # Add before </body> as fallback
    if '</body>' in content:
        new_content = content.replace(
            '</body>',
            '    <script src="breadcrumb.js"></script>\n</body>',
            1
        )
        return new_content, True
    
    return content, False


def process_file(filepath):
    """Process a single HTML file."""
    filename = filepath.name
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        stats['errors'].append(f'{filename}: read error: {e}')
        return
    
    original = content
    changed = False
    
    # 1. Fix declension
    content, decl_count = fix_declension(content, filename)
    if decl_count > 0:
        stats['declension_fixed'] += decl_count
        changed = True
    
    # 2. Add canonical
    content, was_added = add_canonical(content, filename)
    if was_added:
        stats['canonical_added'] += 1
        changed = True
    else:
        stats['canonical_skipped'] += 1
    
    # 3. Add OG tags
    content, was_added = add_og_tags(content, filename)
    if was_added:
        stats['og_added'] += 1
        changed = True
    else:
        stats['og_skipped'] += 1
    
    # 4. Add breadcrumb.js
    content, was_added = add_breadcrumb_script(content, filename)
    if was_added:
        stats['breadcrumb_added'] += 1
        changed = True
    else:
        stats['breadcrumb_skipped'] += 1
    
    if changed:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'  OK {filename}')
        except Exception as e:
            stats['errors'].append(f'{filename}: write error: {e}')
    else:
        print(f'  -- {filename} (no changes)')


def generate_sitemap():
    """Generate complete sitemap.xml"""
    print('\n--- Generating sitemap.xml ---')
    
    all_html = sorted(BASE.glob('*.html'))
    urls = []
    
    priority_map = {
        'index.html': ('1.0', 'daily'),
        'uslugi.html': ('0.9', 'weekly'),
        'about.html': ('0.9', 'monthly'),
        'price.html': ('0.9', 'monthly'),
        'portfolio.html': ('0.8', 'monthly'),
        'blog.html': ('0.8', 'weekly'),
    }
    
    for f in all_html:
        if f.name in EXCLUDE:
            continue
        
        filename = f.name
        
        # Determine priority and changefreq
        if filename in priority_map:
            priority, changefreq = priority_map[filename]
        elif filename.startswith('blog-'):
            priority, changefreq = '0.7', 'monthly'
        elif filename.startswith('sravnenie-') or filename.startswith('kakoj-') or filename.startswith('top-'):
            priority, changefreq = '0.7', 'monthly'
        elif re.match(r'^remont-[a-z]+\.html$', filename):
            priority, changefreq = '0.8', 'weekly'
        elif 'remont-' in filename and '-' in filename.replace('remont-', ''):
            priority, changefreq = '0.6', 'weekly'
        else:
            priority, changefreq = '0.5', 'monthly'
        
        # Get lastmod from file modification time
        mtime = os.path.getmtime(f)
        lastmod = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')
        
        urls.append({
            'loc': f'https://24stanki.ru/{filename}',
            'lastmod': lastmod,
            'changefreq': changefreq,
            'priority': priority,
        })
    
    # Build XML
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    for url in urls:
        xml += '  <url>\n'
        xml += f'    <loc>{url["loc"]}</loc>\n'
        xml += f'    <lastmod>{url["lastmod"]}</lastmod>\n'
        xml += f'    <changefreq>{url["changefreq"]}</changefreq>\n'
        xml += f'    <priority>{url["priority"]}</priority>\n'
        xml += '  </url>\n'
    
    xml += '</urlset>\n'
    
    sitemap_path = BASE / 'sitemap.xml'
    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write(xml)
    
    print(f'  sitemap.xml: {len(urls)} URLs written')
    return len(urls)


def fix_robots():
    """Fix robots.txt"""
    print('\n--- Fixing robots.txt ---')
    
    robots_path = BASE / 'robots.txt'
    content = robots_path.read_text(encoding='utf-8')
    
    # Add Disallow for preview if not present
    if '/preview.html' not in content:
        content = content.replace(
            'Disallow: /seo-tools/',
            'Disallow: /seo-tools/\nDisallow: /preview.html'
        )
        print('  Added Disallow: /preview.html')
    
    with open(robots_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print('  robots.txt updated')


def main():
    print('=' * 60)
    print('ЭТАП 1: ТЕХНИЧЕСКИЕ ИСПРАВЛЕНИЯ')
    print('=' * 60)
    
    files = get_all_html()
    stats['total_files'] = len(files)
    print(f'\nFound {len(files)} HTML files\n')
    
    # Process all files
    for f in files:
        process_file(f)
    
    # Generate sitemap
    sitemap_count = generate_sitemap()
    
    # Fix robots
    fix_robots()
    
    # Print stats
    print('\n' + '=' * 60)
    print('STATS:')
    print(f'  Total files: {stats["total_files"]}')
    print(f'  Declension fixes: {stats["declension_fixed"]}')
    print(f'  Canonical added: {stats["canonical_added"]}, skipped: {stats["canonical_skipped"]}')
    print(f'  OG added: {stats["og_added"]}, skipped: {stats["og_skipped"]}')
    print(f'  Breadcrumb.js added: {stats["breadcrumb_added"]}, skipped: {stats["breadcrumb_skipped"]}')
    print(f'  Sitemap URLs: {sitemap_count}')
    
    if stats['errors']:
        print(f'\n  ERRORS ({len(stats["errors"])}):')
        for e in stats['errors']:
            print(f'    {e}')
    
    print('=' * 60)


if __name__ == '__main__':
    main()
