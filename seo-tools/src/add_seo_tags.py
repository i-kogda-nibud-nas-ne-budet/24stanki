#!/usr/bin/env python3
"""
Add Open Graph, Twitter Cards, and Breadcrumb Schema.org to geo-landing pages.
"""

import os
from pathlib import Path
import re

def get_page_config(filename):
    """Extract city and service type from filename."""
    parts = filename.replace('.html', '').split('-')
    if len(parts) >= 3:
        service = parts[1]
        city = parts[2]
        return service, city
    return None, None

def get_title_and_description(service, city):
    """Generate title and description for Open Graph based on service and city."""
    service_names = {
        'listogibov': 'листогибов',
        'gilotin': 'гильотин',
        'trubogibov': 'трубогибов'
    }
    
    city_names = {
        'moskva': 'Москве',
        'spb': 'Санкт-Петербурге'
    }
    
    service_ru = service_names.get(service, service)
    city_ru = city_names.get(city, city)
    
    title = f"Ремонт {service_ru} в {city_ru} - цены 2025, выезд 24/7"
    description = f"Профессиональный ремонт {service_ru} в {city_ru}. Выезд мастера в день обращения. Гарантия 6 месяцев."
    
    return title, description

def get_breadcrumb_script(service, city, filename):
    """Generate Breadcrumb Schema.org script."""
    service_names = {
        'listogibov': 'листогибов',
        'gilotin': 'гильотин',
        'trubogibov': 'трубогибов'
    }
    
    city_names = {
        'moskva': 'Москве',
        'spb': 'Санкт-Петербурге'
    }
    
    service_url_map = {
        'listogibov': 'remont-listogibov.html',
        'gilotin': 'remont-gilotin.html',
        'trubogibov': 'remont-trubogibov.html'
    }
    
    service_ru_page = f"Ремонт {service_names.get(service, service)}"
    service_ru_target = f"Ремонт {service_names.get(service, service)} в {city_names.get(city, city)}"
    
    script = f'''
    <!-- Breadcrumb Schema.org -->
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
            "name": "{service_ru_page}",
            "item": "https://24stanki.ru/{service_url_map.get(service, 'remont-' + service + '.html')}"
        }}, {{
            "@type": "ListItem",
            "position": 3,
            "name": "{service_ru_target}"
        }}]
    }}
    </script>
    '''
    return script

def add_seo_tags_to_file(filepath):
    """Add Open Graph, Twitter Cards, and Breadcrumbs to an HTML file."""
    filepath = Path(filepath)
    
    if not filepath.exists():
        print(f"File not found: {filepath}")
        return False
    
    filename = filepath.name
    service, city = get_page_config(filename)
    
    if not service or not city:
        print(f"Could not parse filename: {filename}")
        return False
    
    print(f"Processing {filename} (service: {service}, city: {city})")
    
    # Read the file
    content = filepath.read_text(encoding='utf-8')
    
    # Check if already processed
    if '<!-- Open Graph / Facebook -->' in content:
        print(f"  Skipping (already has Open Graph tags)")
        return False
    
    # Generate tags
    og_title, og_desc = get_title_and_description(service, city)
    breadcrumb_script = get_breadcrumb_script(service, city, filename)
    
    og_tags = f'''    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://24stanki.ru/{filename}">
    <meta property="og:title" content="{og_title}">
    <meta property="og:description" content="{og_desc}">
    <meta property="og:image" content="https://24stanki.ru/images/telegram-preview.jpg">
    <meta property="og:locale" content="ru_RU">

    <!-- Twitter -->
    <meta property="twitter:card" content="summary_large_image">
    <meta property="twitter:url" content="https://24stanki.ru/{filename}">
    <meta property="twitter:title" content="{og_title}">
    <meta property="twitter:description" content="{og_desc}">
    <meta property="twitter:image" content="https://24stanki.ru/images/telegram-preview.jpg">
'''
    
    # Find insertion point (after keywords meta tag, before first script)
    # Look for the pattern: </script>\n    <script type="application/ld+json">
    pattern = r'(</script>\n)(    <script type="application/ld+json">)'
    
    match = re.search(pattern, content)
    if match:
        # Insert after </script> of Yandex Metrika
        new_content = content[:match.end(1)] + og_tags + '\n' + breadcrumb_script + '\n' + match.group(2) + content[match.start(2):]
    else:
        # Alternative: insert after keywords meta tag
        pattern2 = r'(<meta name="keywords"[^>]*>\n)'
        match2 = re.search(pattern2, content)
        if match2:
            new_content = content[:match2.end()] + og_tags + '\n' + breadcrumb_script + '\n' + content[match2.end():]
        else:
            print(f"  Could not find insertion point")
            return False
    
    # Write back
    filepath.write_text(new_content, encoding='utf-8')
    print(f"  ✓ Added SEO tags")
    return True

def main():
    # List of geo-landing pages to process
    geo_pages = [
        'remont-gilotin-moskva.html',
        'remont-gilotin-spb.html',
        'remont-listogibov-moskva.html',
        'remont-listogibov-spb.html',
        'remont-trubogibov-moskva.html',
        'remont-trubogibov-spb.html'
    ]
    
    base_dir = Path('../')
    seo_tools_dir = Path('../seo-tools')
    
    # Change to project root
    os.chdir(base_dir)
    
    processed = 0
    for page in geo_pages:
        if add_seo_tags_to_file(page):
            processed += 1
    
    print(f"\nCompleted: {processed} pages updated")

if __name__ == '__main__':
    main()