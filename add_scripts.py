#!/usr/bin/env python3
"""Добавляет подключение breadcrumb.js во все HTML файлы"""

import os
import re

exclude = {'google1e0151116e608a2e.html', 'yandex_32e5528f50fd0785.html', 'preview.html'}

for filename in os.listdir('.'):
    if filename.endswith('.html') and filename not in exclude:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'breadcrumb.js' not in content:
            new_content = re.sub(
                r'<script src="script\.js"></script>',
                '<script src="breadcrumb.js"></script>\n<script src="script.js"></script>',
                content
            )
            
            if new_content != content:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f'Подключен: {filename}')
        else:
            print(f'Уже подключен: {filename}')
