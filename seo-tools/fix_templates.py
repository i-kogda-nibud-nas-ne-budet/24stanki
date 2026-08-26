#!/usr/bin/env python3
"""Массовое исправление шаблонов всех HTML-файлов 24stanki.ru"""

import os
import re
from pathlib import Path

BASE = Path('.')
EXCLUDE = {'preview.html', 'google1e0151116e608a2e.html', 'yandex_32e5528f50fd0785.html'}

# Шаблон нового footer
NEW_FOOTER = '''<!-- ===== FOOTER ===== -->
<footer class="footer">
    <div class="container">
        <div class="footer-grid">
            <div class="footer-brand">
                <div class="nav-logo">24<span>STANKI</span></div>
                <p>ИП Горбунов М.А. — ремонт металлообрабатывающего оборудования в Москве и по России. Выезд 24/7.</p>
            </div>
            <div>
                <h4>Услуги</h4>
                <ul>
                    <li><a href="remont-listogibov.html">Ремонт листогибов</a></li>
                    <li><a href="remont-gilotin.html">Ремонт гильотин</a></li>
                    <li><a href="remont-trubogibov.html">Ремонт трубогибов</a></li>
                    <li><a href="remont-lentochnyh-pil.html">Ремонт ленточных пил</a></li>
                </ul>
            </div>
            <div>
                <h4>Компания</h4>
                <ul>
                    <li><a href="price.html">Прайс-лист</a></li>
                    <li><a href="portfolio.html">Портфолио</a></li>
                    <li><a href="blog.html">Блог</a></li>
                </ul>
            </div>
            <div>
                <h4>Контакты</h4>
                <ul>
                    <li><a href="tel:89939089837">8 (993) 908-98-37</a></li>
                    <li><a href="https://wa.me/79939089837">WhatsApp</a></li>
                    <li><a href="https://t.me/servis_stankov">Telegram</a></li>
                    <li><a href="mailto:max.gorbunov.service@yandex.ru">Email</a></li>
                </ul>
            </div>
        </div>
        <div class="footer-bottom">
            <span>© 2026 ИП Горбунов М.А. Все права защищены.</span>
            <a href="sitemap.xml">Карта сайта</a>
        </div>
    </div>
</footer>'''

# Шаблон CTA перед footer
CTA_BEFORE_FOOTER = '''
<!-- ===== CTA ===== -->
<section class="section">
    <div class="container">
        <div class="cta-section">
            <h2>Нужен ремонт оборудования?</h2>
            <p>Бесплатная консультация. Выезд за 2–4 часа по Москве и МО.</p>
            <div class="cta-buttons">
                <a href="tel:89939089837" class="btn btn-primary">📞 8 (993) 908-98-37</a>
                <a href="https://wa.me/79939089837" class="btn btn-outline">💬 WhatsApp</a>
            </div>
        </div>
    </div>
</section>'''

# Новый навбар
NEW_NAV = '''<!-- ===== NAVIGATION ===== -->
<nav class="nav" id="nav">
    <div class="nav-inner">
        <a href="index.html" class="nav-logo">24<span>STANKI</span></a>
        <div class="nav-links">
            <a href="uslugi.html">Услуги</a>
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
    <a href="price.html">Цены</a>
    <a href="portfolio.html">Портфолио</a>
    <a href="blog.html">Блог</a>
    <a href="tel:89939089837" class="btn btn-primary">📞 Позвонить</a>
    <a href="https://wa.me/79939089837" class="btn btn-outline">💬 WhatsApp</a>
</div>'''


def fix_file(filepath):
    """Исправляет один HTML-файл"""
    filename = filepath.name
    content = filepath.read_text(encoding='utf-8')
    original = content
    changes = []
    
    # 1. Убираем <body class="dark-theme"> → <body>
    if '<body class="dark-theme">' in content:
        content = content.replace('<body class="dark-theme">', '<body>')
        changes.append('removed dark-theme')
    
    # 2. Убираем Roboto Condensed font
    if 'Roboto+Condensed' in content:
        content = re.sub(r'<link[^>]*Roboto\+Condensed[^>]*>\s*\n?', '', content)
        changes.append('removed Roboto Condensed')
    
    # 3. Заменяем старый nav (обёрнутый в <header>) на новый
    # Ищем <header> с <nav class="nav" внутри
    old_header_pattern = r'<header>\s*<nav class="nav"[^>]*>.*?</nav>\s*</header>'
    if re.search(old_header_pattern, content, re.DOTALL):
        content = re.sub(old_header_pattern, NEW_NAV, content, flags=re.DOTALL)
        changes.append('replaced header>nav with new nav')
    # Или просто <nav class="nav"> без header
    elif '<nav class="nav"' in content and '<header>' not in content.split('<nav class="nav"')[0][-50:]:
        # Nav без header — оставляем как есть, но добавляем nav-mobile если нет
        if '.nav-mobile' not in content:
            # Добавляем nav-mobile после закрытия nav
            content = re.sub(r'(</nav>)(\s*\n)', r'\1\n<div class="nav-mobile">\n    <a href="index.html">Главная</a>\n    <a href="uslugi.html">Услуги</a>\n    <a href="price.html">Цены</a>\n    <a href="portfolio.html">Портфолио</a>\n    <a href="blog.html">Блог</a>\n    <a href="tel:89939089837" class="btn btn-primary">📞 Позвонить</a>\n    <a href="https://wa.me/79939089837" class="btn btn-outline">💬 WhatsApp</a>\n</div>\2', content, count=1)
            changes.append('added nav-mobile')
    
    # 4. Убираем floating-elements (скрытые SVG)
    floating_pattern = r'<div class="floating-elements">.*?</div>\s*</div>'
    if re.search(floating_pattern, content, re.DOTALL):
        content = re.sub(floating_pattern, '', content, flags=re.DOTALL)
        changes.append('removed floating-elements')
    # Или одиночный floating-elements
    floating_pattern2 = r'\s*<div class="floating-elements">\s*</div>'
    if re.search(floating_pattern2, content):
        content = re.sub(floating_pattern2, '', content)
        changes.append('removed empty floating-elements')
    
    # 5. Заменяем старый footer на новый
    # Ищем bare <footer> без class="footer"
    old_footer_pattern = r'<footer>(?!\s*class="footer")(.*?)</footer>'
    if re.search(old_footer_pattern, content, re.DOTALL):
        # Заменяем всё от <footer> до </footer> на новый footer
        content = re.sub(r'<footer>.*?</footer>', NEW_FOOTER + '\n', content, flags=re.DOTALL)
        changes.append('replaced footer')
    # Или footer с social-links
    elif '<footer>' in content and 'social-links' in content:
        content = re.sub(r'<footer>.*?</footer>', NEW_FOOTER + '\n', content, flags=re.DOTALL)
        changes.append('replaced footer with social-links')
    
    # 6. Добавляем CTA перед footer (если нет)
    if 'cta-section' not in content and '</footer>' in content:
        content = content.replace('</footer>', CTA_BEFORE_FOOTER + '\n\n</footer>')
        changes.append('added CTA before footer')
    
    # 7. Записываем если есть изменения
    if content != original:
        filepath.write_text(content, encoding='utf-8')
        return True, changes
    return False, []


def main():
    print('=' * 60)
    print('МАССОВОЕ ИСПРАВЛЕНИЕ ШАБЛОНОВ')
    print('=' * 60)
    
    # Находим все HTML файлы
    all_files = sorted(BASE.glob('*.html'))
    files_to_fix = [f for f in all_files if f.name not in EXCLUDE]
    
    print(f'\nНайдено файлов: {len(files_to_fix)}')
    
    fixed = 0
    skipped = 0
    errors = []
    
    for f in files_to_fix:
        try:
            was_fixed, changes = fix_file(f)
            if was_fixed:
                fixed += 1
                print(f'  FIX {f.name}: {", ".join(changes)}')
            else:
                skipped += 1
        except Exception as e:
            errors.append(f'{f.name}: {e}')
            print(f'  ERR {f.name}: {e}')
    
    print(f'\n{"=" * 60}')
    print(f'Исправлено: {fixed}')
    print(f'Без изменений: {skipped}')
    print(f'Ошибки: {len(errors)}')
    if errors:
        for e in errors[:5]:
            print(f'  {e}')
    print('=' * 60)


if __name__ == '__main__':
    main()
