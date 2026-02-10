#!/usr/bin/env python3
"""
Add Breadcrumb Schema.org to all pages (except geo-landing pages which already have them).
"""

import os
from pathlib import Path

def get_breadcrumb_for_page(filename):
    """Generate breadcrumb script based on page type."""
    
    # Main pages
    if filename == 'index.html':
        return None  # Homepage doesn't need breadcrumbs
    elif filename == 'uslugi.html':
        return '''    <!-- Breadcrumb Schema.org -->
    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [{
            "@type": "ListItem",
            "position": 1,
            "name": "Главная",
            "item": "https://24stanki.ru/"
        }, {
            "@type": "ListItem",
            "position": 2,
            "name": "Услуги"
        }]
    }
    </script>
'''
    elif filename == 'blog.html':
        return '''    <!-- Breadcrumb Schema.org -->
    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [{
            "@type": "ListItem",
            "position": 1,
            "name": "Главная",
            "item": "https://24stanki.ru/"
        }, {
            "@type": "ListItem",
            "position": 2,
            "name": "Блог"
        }]
    }
    </script>
'''
    
    # Blog posts
    if filename.startswith('blog-'):
        post_name = filename.replace('blog-', '').replace('.html', '').replace('-', ' ').title()
        return f'''    <!-- Breadcrumb Schema.org -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [{{
            "@type": "ListItem",
            "position": 1,
            "name": "Главная",
            "item": "https://24stanki.ru/"
        }}, {{
            "@type": "ListItem",
            "position": 2,
            "name": "Блог",
            "item": "https://24stanki.ru/blog.html"
        }}, {{
            "@type": "ListItem",
            "position": 3,
            "name": "{post_name}"
        }}]
    }}
    </script>
'''
    
    # Service pages (remont-*.html but not geo-landing pages)
    if filename.startswith('remont-') and '-moskva' not in filename and '-spb' not in filename:
        service_map = {
            'listogibov': 'Ремонт листогибов',
            'gilotin': 'Ремонт гильотин',
            'lentochnyh-pil': 'Ремонт ленточных пил',
            'profilgebiv': 'Ремонт профилегибов',
            'valtsev': 'Ремонт вальцевых',
            'trubogibov': 'Ремонт трубогибов',
            'stankov-chpu': 'Ремонт станков ЧПУ'
        }
        
        service_key = filename.replace('remont-', '').replace('.html', '')
        service_name = service_map.get(service_key, service_key.replace('-', ' ').title())
        
        return f'''    <!-- Breadcrumb Schema.org -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [{{
            "@type": "ListItem",
            "position": 1,
            "name": "Главная",
            "item": "https://24stanki.ru/"
        }}, {{
            "@type": "ListItem",
            "position": 2,
            "name": "{service_name}"
        }}]
    }}
    </script>
'''
    
    return None

def add_breadcrumbs_to_file(filepath):
    """Add breadcrumbs to an HTML file."""
    filepath = Path(filepath)
    
    if not filepath.exists():
        print(f"File not found: {filepath}")
        return False
    
    filename = filepath.name
    
    # Skip files that already have breadcrumbs
    try:
        content = filepath.read_text(encoding='utf-8')
    except Exception as e:
        print(f"  Error reading file: {e}")
        return False
    
    if 'Breadcrumb Schema.org' in content:
        return False
    
    # Get breadcrumb script
    breadcrumb_script = get_breadcrumb_for_page(filename)
    if not breadcrumb_script:
        return False
    
    print(f"Adding breadcrumbs to {filename}")
    
    # Find insertion point: after Yandex Metrika script (</script> before <link rel="stylesheet")
    lines = content.split('\n')
    
    insert_index = None
    
    # Look for Yandex Metrika closing script followed by stylesheet link
    for i, line in enumerate(lines):
        if '</script>' in line and i+1 < len(lines):
            next_line = lines[i+1]
            if '<link rel="stylesheet"' in next_line:
                insert_index = i + 1
                break
    
    # Alternative: after keywords meta tag
    if insert_index is None:
        for i, line in enumerate(lines):
            if '<meta name="keywords"' in line:
                insert_index = i + 1
                break
    
    # Last resort: before closing </head>
    if insert_index is None:
        for i, line in enumerate(lines):
            if '</head>' in line:
                insert_index = i
                break
    
    if insert_index is None:
        print(f"  Could not find insertion point")
        return False
    
    # Insert breadcrumb script
    lines.insert(insert_index, breadcrumb_script)
    new_content = '\n'.join(lines)
    
    try:
        filepath.write_text(new_content, encoding='utf-8')
        print(f"  ✓ Added breadcrumbs")
        return True
    except Exception as e:
        print(f"  Error writing file: {e}")
        return False

def main():
    # Change to project root (one level up from seo-tools/src)
    base_dir = Path(__file__).parent.parent.parent
    os.chdir(base_dir)
    
    html_files = list(base_dir.glob('*.html'))
    print(f"Found {len(html_files)} HTML files in {base_dir}")
    
    # Exclude files
    exclude_patterns = [
        'remont-gilotin-moskva.html',
        'remont-gilotin-spb.html',
        'remont-listogibov-moskva.html',
        'remont-listogibov-spb.html',
        'remont-trubogibov-moskva.html',
        'remont-trubogibov-spb.html',
        'google1e0151116e608a2e.html',
        'yandex_32e5528f50fd0785.html',
        'preview.html',
        'index.html'
    ]
    
    processed = 0
    for filepath in html_files:
        if filepath.name in exclude_patterns:
            continue
        if add_breadcrumbs_to_file(filepath):
            processed += 1
    
    print(f"\nCompleted: {processed} pages updated with breadcrumbs")

if __name__ == '__main__':
    main()