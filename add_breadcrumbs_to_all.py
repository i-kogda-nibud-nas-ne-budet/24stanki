#!/usr/bin/env python3
"""
Скрипт для добавления хлебных крошек на все HTML-страницы сайта 24stanki.ru
"""

import os
import re
from pathlib import Path

def add_breadcrumbs_to_file(filepath):
    """Добавляет хлебные крошки в HTML-файл"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Проверяем, есть ли уже хлебные крошки
        if 'class="breadcrumbs"' in content:
            print(f"  Пропущено (уже есть): {filepath.name}")
            return False
        
        # Ищем </header> и добавляем после него хлебные крошки
        # Используем регулярное выражение для поиска </header> перед <main>
        pattern = r'(</header>\s*)(<main>)'
        replacement = r'\1\n\n<!-- Хлебные крошки -->\n<nav class="breadcrumbs" aria-label="Навигация по сайту"></nav>\n\n\2'
        
        new_content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
        
        if new_content == content:
            # Пробуем другой паттерн - просто после </header>
            pattern2 = r'(</header>)(\s*\n)'
            replacement2 = r'\1\2\n<!-- Хлебные крошки -->\n<nav class="breadcrumbs" aria-label="Навигация по сайту"></nav>\n'
            new_content = re.sub(pattern2, replacement2, content, flags=re.IGNORECASE)
        
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"  ✓ Обновлено: {filepath.name}")
            return True
        else:
            print(f"  ⚠ Не удалось обновить: {filepath.name}")
            return False
            
    except Exception as e:
        print(f"  ✗ Ошибка при обработке {filepath.name}: {e}")
        return False

def main():
    """Основная функция"""
    # Директория с HTML файлами
    base_dir = Path('c:/Projects/24stanki')
    
    # Список файлов для обработки (исключая вспомогательные)
    exclude_files = {
        'google1e0151116e608a2e.html',
        'yandex_32e5528f50fd0785.html',
        'preview.html',
        'CNAME',
        'README.md',
        'robots.txt',
        'sitemap.xml',
        'price-list.xml',
        'price-list-template.xml'
    }
    
    # Находим все HTML файлы
    html_files = []
    for file in base_dir.glob('*.html'):
        if file.name not in exclude_files:
            html_files.append(file)
    
    print(f"Найдено {len(html_files)} HTML файлов для обработки\n")
    
    updated_count = 0
    for filepath in sorted(html_files):
        if add_breadcrumbs_to_file(filepath):
            updated_count += 1
    
    print(f"\n{'='*50}")
    print(f"Итого обновлено: {updated_count} из {len(html_files)} файлов")
    print(f"{'='*50}")
    
    # Создаем инструкцию
    print("\n⚠ ВАЖНО: Теперь нужно добавить подключение breadcrumb.js в каждый файл!")
    print("Найдите строку <script src=\"script.js\"></script>")
    print("И добавьте перед ней: <script src=\"breadcrumb.js\"></script>")

if __name__ == '__main__':
    main()
