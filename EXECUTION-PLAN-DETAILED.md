# 📋 ДЕТАЛЬНЫЙ ПЛАН ВЫПОЛНЕНИЯ SEO-ОПТИМИЗАЦИИ

** Статус:** ACT MODE - НАЧИНАЕМ РАБОТУ  
**Цель:** 101 новая страница + технические улучшения за 2 недели  
**Бюджет:** 0 руб.

---

## 🎯 ФАЗА 1: НАСТРОЙКА ИНФРАСТРУКТУРЫ (День 1)

### Задача 1.1: Создать Python окружение через uv
```bash
# Создаем папку для SEO-инструментов
mkdir seo-tools
cd seo-tools

# Инициализируем uv проект
uv init

# Создаем pyproject.toml с зависимостями
```

**Файл: seo-tools/pyproject.toml**
```toml
[project]
name = "seo-tools-24stanki"
version = "0.1.0"
description = "SEO optimization tools for 24stanki.ru"
requires-python = ">=3.9"

dependencies = [
    "beautifulsoup4>=4.12.0",
    "lxml>=4.9.0",
    "pandas>=2.0.0",
    "nltk>=3.8.0",
    "scikit-learn>=1.3.0",
    "requests>=2.31.0",
    "urllib3>=2.0.0",
    "python-dotenv>=1.0.0",
    "jinja2>=3.1.0",
    "openpyxl>=3.1.0",
    "reportlab>=4.0.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

**Команды:**
```bash
# Активировать окружение
.venv\Scripts\activate  # Windows
# или source .venv/bin/activate  # Linux/Mac

# Установить зависимости
uv pip install -e .
```

### Задача 1.2: Создать структуру папок
```
seo-tools/
├── src/
│   ├── __init__.py
│   ├── meta_analyzer.py
│   ├── link_checker.py
│   ├── keyword_extractor.py
│   ├── sitemap_generator.py
│   ├── content_analyzer.py
│   ├── geo_pages_generator.py
│   └── seo_reporter.py
├── data/
│   ├── keywords.json
│   ├── cities.json
│   └── competitors.json
├── templates/
│   ├── geo-landing.html
│   ├── comparison.html
│   └── faq.html
├── output/
│   ├── reports/
│   ├── new_pages/
│   └── sitemaps/
├── tests/
├── pyproject.toml
├── README.md
└── .env
```

---

## 🎯 ФАЗА 2: СОЗДАНИЕ ПЕРВЫХ 10 СТРАНИЦ (День 1-2)

### **ПРИОРИТЕТ 1: СРАВНИТЕЛЬНЫЕ СТРАНИЦЫ (4 шт)**

#### 1.1: sravnenie-listogibov-i-gilotin.html
**SEO-ключи:** 
- "листогиб или гильотина что выбрать"
- "чем отличается листогиб от гильотины"
- "сравнение листогибов и гильотин"

**Структура:**
```html
<h1>Листогибы vs Гильотины: что выбрать для вашего производства в 2025</h1>
<p>Детальное сравнение по 12 параметрам: точность, скорость, цена, обслуживание...</p>

<table class="comparison-detailed">
  <thead>
    <tr><th>Параметр</th><th>Листогиб</th><th>Гильотина</th></tr>
  </thead>
  <tbody>
    <tr><td>Точность резки</td><td>±0.1 мм</td><td>±0.05 мм</td></tr>
    <tr><td>Скорость работы</td><td>до 10 м/мин</td><td>до 30 м/мин</td></tr>
    <tr><td>Цена оборудования</td><td>от 500к ₽</td><td>от 300к ₽</td></tr>
    <tr><td>Стоимость ремонта</td><td>от 15 000 ₽</td><td>от 10 000 ₽</td></tr>
    <tr><td>Сложность обслуживания</td><td>Высокая</td><td>Низкая</td></tr>
    <tr><td>Гарантийный срок</td><td>1-2 года</td><td>2-3 года</td></tr>
  </tbody>
</table>

<h2>Когда выбирать листогиб?</h2>
<p>Гибка листового металла сложных профилей...</p>

<h2>Когда выбирать гильотину?</h2>
<p>Резка листов на заготовки...</p>

<h2>Сравнение по брендам</h2>
<p>Таблица: Mogul vs Пластма vs Эффект для каждого типа...</p>

<h2>Наш опыт ремонта</h2>
<p>За 15 лет мы отремонтировали X листогибов и Y гильотин...</p>

<h2>Ремонт листогибов и гильотин в Москве</h2>
<p>Выезд 24/7, гарантия 6 месяцев...</p>
<a href="remont-listogibov.html">Ремонт листогибов</a> | 
<a href="remont-gilotin.html">Ремонт гильотин</a>

<!-- Schema.org -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Листогибы vs Гильотины: что выбрать",
  "author": {"@type": "Organization", "name": "24stanki.ru"},
  "datePublished": "2025-02-10"
}
</script>
```

#### 1.2: sravnenie-trubogibov-i-profilgebiv.html
**SEO-ключи:**
- "трубогиб или профилегиб что выбрать"
- "чем отличается трубогиб от профилегиба"
- "трубогиб vs профилегиб"

**Структура аналогичная, сравнение по параметрам:**
- Диаметр трубы/профиля
- Тип гибки (труба vs профиль)
- Точность
- Производительность
- Цена
- Ремонт

#### 1.3: kakoj-stanok-vybrat-dlya-proizvodstva.html
**SEO-ключи:**
- "какой станок выбрать для производства"
- "выбор металлообрабатывающего станка"
- "станок для металла сравнительный анализ"

**Содержание:**
- Введение: почему выбор правильного станка критичен
- Таблица: тип станка vs применение (листогиб, гильотина, трубогиб,_profileгеб)
- Алгоритм выбора по 5 шагам
- Вопросы, которые нужно задать себе
- Примеры для разных производств (малое, среднее, крупное)
- Калькулятор: подбор станка по параметрам (JS)
- Ссылки на все услуги

#### 1.4: top-10-luchshih-markov-stankov-2025.html
**SEO-ключи:**
- "топ 10 брендов станков 2025"
- "лучшие марки металлообрабатывающих станков"
- "рейтинг станков для металла"

**Структура:**
- Рейтинг по 10 критериям (надежность, цена, сервис, запчасти)
- Таблица с рейтингами 1-10
- Подробный обзор каждой марки (3-4 абзаца)
- Плюсы/минусы
- Приведенные примеры моделей
- Информация о сервисе для каждой марки (у нас есть опыт)
- Call-to-action: "Закажите ремонт вашего станка любой марки"

---

### **ПРИОРИТЕТ 2: ГЕО-ЛЕНДИНГИ (6 шт на старте)**

Начнем с 2 городов × 3 типа оборудования:

#### 1.5: remont-listogibov-moskva.html
**SEO-ключи:**
- "ремонт листогибов Москва"
- "листогиб ремонт цена Москва"
- "выезд мастера на ремонт листогиба Москва"

**Уникальный контент:**
- Заголовок: "Ремонт листогибов в Москве - выезд 24/7, гарантия 6 месяцев"
- Вступление про Москву: "Работаем по всем районам Москвы: ЦАО, САО, ЮАО, ВАО, ЗАО, СЗАО, ЮЗАО, ВАО, Москва-река..."
- Таблица цен с учетом бесплатного выезда по Москве
- Отзывы с указанием районов Москвы
- Карта районов обслуживания (можно статичная картинка)
- Локальный телефон (если есть отдельный для Москвы)
- Фото объектов в Москве (если есть)

#### 1.6: remont-listogibov-spb.html
Аналогично для Санкт-Петербурга

#### 1.7: remont-gilotin-moskva.html
**SEO-ключи:**
- "ремонт гильотин Москва"
- "гильотина ремонт цена Москва"

#### 1.8: remont-gilotin-spb.html

#### 1.9: remont-trubogibov-moskva.html
**SEO-ключи:**
- "ремонт трубогибов Москва"
- "трубогиб ремонт цена Москва"

#### 1.10: remont-trubogibov-spb.html

**Шаблон для всех гео-лендингов:**
- Берем remont-listogibov.html за основу
- Заменяем "Москва и Московская область" на конкретный город
- Добавляем уникальный первый абзац про город
- Модифицируем таблицу цен (выезд может быть платным/бесплатным)
- Добавляем "обслуживаемые районы города"
- Добавляем schema.org с areaServed: City

---

## 🎯 ФАЗА 3: ТЕХНИЧЕСКИЕ УЛУЧШЕНИЯ (День 3)

### Задача 3.1: Добавить breadcrumbs на ВСЕ страницы
**Шаблон breadcrumbs:**
```html
<nav class="breadcrumb" itemscope itemtype="https://schema.org/BreadcrumbList">
  <span itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
    <a itemprop="item" href="index.html"><span itemprop="name">Главная</span></a>
    <meta itemprop="position" content="1" />
  </span> /
  <span itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
    <a itemprop="item" href="uslugi.html"><span itemprop="name">Услуги</span></a>
    <meta itemprop="position" content="2" />
  </span> /
  <span itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
    <span itemprop="name">Ремонт листогибов</span>
    <meta itemprop="position" content="3" />
  </span>
</nav>
```

**Действие:**
- Добавить в header после .hero-text на всех страницах услуг
- На главной: только "Главная"
- На uslugi.html: "Главная / Услуги"
- На каждой странице ремонта: "Главная / Услуги / Ремонт X"

### Задача 3.2: Добавить Open Graph + Twitter Cards
**Добавить в <head> ВСЕХ страниц:**
```html
<!-- Open Graph / Facebook -->
<meta property="og:type" content="website" />
<meta property="og:url" content="https://24stanki.ru/[страница]" />
<meta property="og:title" content="[такой же как title]" />
<meta property="og:description" content="[такой же как description, но можно чуть длиннее]" />
<meta property="og:image" content="https://24stanki.ru/images/telegram-preview.jpg" />
<meta property="og:locale" content="ru_RU" />

<!-- Twitter -->
<meta property="twitter:card" content="summary_large_image" />
<meta property="twitter:url" content="https://24stanki.ru/[страница]" />
<meta property="twitter:title" content="[title]" />
<meta property="twitter:description" content="[description]" />
<meta property="twitter:image" content="https://24stanki.ru/images/telegram-preview.jpg" />
```

### Задача 3.3: Улучшить читаемость текста (styles.css)
**Добавить в styles.css:**
```css
/* Увеличим размер шрифта */
body {
    font-size: 18px;  /* было 16px */
    line-height: 1.6; /* было 1.5 */
}

/* Улучшим контраст для темной темы */
.dark-theme {
    background-color: #121212; /* было #0a0a0a */
    color: #e0e0e0; /* вместо #333 */
}

/* Уменьшим жирность заголовков */
h1, h2, h3 {
    font-weight: 600; /* было 700 */
}

/* Увеличим отступы между секциями */
section {
    padding: 60px 0; /* было 40px */
}

/* Максимальная ширина для читаемости */
.content, .faq-answer {
    max-width: 80ch;
    margin: 0 auto;
}

/* Бордеры таблиц - четче */
table {
    border: 1px solid #444;
}
th, td {
    border: 1px solid #444;
    padding: 12px 16px;
}
```

---

## 🎯 ФАЗА 4: НАПИСАНИЕ PYTHON-СКРИПТОВ (День 4)

### 4.1: meta_analyzer.py
```python
"""
Анализ meta-тегов на всех HTML страницах
Проверяет:
- Длину title (50-160 символов)
- Длину description (120-320 символов)
- Наличие keywords
- Уникальность title/description
- Дубли
"""
import os
from bs4 import BeautifulSoup
import pandas as pd

def analyze_meta_tags(directory):
    results = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    soup = BeautifulSoup(f.read(), 'lxml')
                    
                    title = soup.title.string if soup.title else ''
                    desc = soup.find('meta', {'name': 'description'})
                    desc_content = desc['content'] if desc else ''
                    keywords = soup.find('meta', {'name': 'keywords'})
                    keywords_content = keywords['content'] if keywords else ''
                    
                    results.append({
                        'page': file,
                        'title': title,
                        'title_len': len(title),
                        'description': desc_content,
                        'desc_len': len(desc_content),
                        'keywords': keywords_content,
                        'has_keywords': bool(keywords),
                        'title_status': 'OK' if 50 <= len(title) <= 160 else 'TOO_SHORT' if len(title) < 50 else 'TOO_LONG',
                        'desc_status': 'OK' if 120 <= len(desc_content) <= 320 else 'TOO_SHORT' if len(desc_content) < 120 else 'TOO_LONG'
                    })
    
    df = pd.DataFrame(results)
    
    # Проверяем дубли title
    duplicate_titles = df[df.duplicated(['title'], keep=False)]
    
    print(f"Проанализировано страниц: {len(df)}")
    print(f"Дубликатов title: {len(duplicate_titles[duplicate_titles['title'] != ''])}")
    print(f"Страниц без keywords: {len(df[~df['has_keywords']])}")
    print(f"Слишком коротких title: {len(df[df['title_status'] == 'TOO_SHORT'])}")
    print(f"Слишком длинных title: {len(df[df['title_status'] == 'TOO_LONG'])}")
    
    # Сохраняем отчет
    df.to_csv('output/reports/meta_analysis.csv', index=False, encoding='utf-8')
    duplicate_titles.to_csv('output/reports/duplicate_titles.csv', index=False, encoding='utf-8')
    
    return df

if __name__ == "__main__":
    analyze_meta_tags('..')  # 분석할 директория (корень сайта)
```

### 4.2: link_checker.py
```python
"""
Проверка внутренних и внешних ссылок
- Битые ссылки (404)
- Циклические ссылки
- Статистика inbound/outbound links
"""
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def check_links(base_url, directory):
    broken_links = []
    internal_links = {}
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    soup = BeautifulSoup(f.read(), 'lxml')
                    
                    for link in soup.find_all('a', href=True):
                        href = link['href']
                        
                        # Пропускаем якорные ссылки и mailto/tel
                        if href.startswith(('#', 'mailto:', 'tel:')):
                            continue
                        
                        # Внешние ссылки проверяем один раз
                        if href.startswith('http'):
                            full_url = href
                        else:
                            full_url = urljoin(base_url, href)
                        
                        try:
                            response = requests.head(full_url, timeout=5, allow_redirects=True)
                            if response.status_code >= 400:
                                broken_links.append({
                                    'page': file,
                                    'link': href,
                                    'status': response.status_code
                                })
                        except Exception as e:
                            broken_links.append({
                                'page': file,
                                'link': href,
                                'error': str(e)
                            })
                        
                        # Статистика internal links
                        if not href.startswith('http'):
                            if file not in internal_links:
                                internal_links[file] = []
                            internal_links[file].append(href)
    
    # Сохраняем отчет
    import pandas as pd
    df_broken = pd.DataFrame(broken_links)
    df_broken.to_csv('output/reports/broken_links.csv', index=False, encoding='utf-8')
    
    # Статистика
    print(f"Найдено битых ссылок: {len(broken_links)}")
    print(f"Среднее количество внутренних ссылок на страницу: {sum(len(v) for v in internal_links.values())/len(internal_links):.1f}")
    
    return broken_links

if __name__ == "__main__":
    check_links('https://24stanki.ru', '..')
```

### 4.3: geo_pages_generator.py
```python
"""
Генерация гео-лендингов из шаблона
"""
import json
import os
from jinja2 import Template

def load_template(template_path):
    with open(template_path, 'r', encoding='utf-8') as f:
        return Template(f.read())

def generate_geo_pages(base_template_file, cities, base_page):
    """
    base_template_file: путь к шаблону (например, remont-listogibov.html)
    cities: список городов с ценами
    base_page: название базовой страницы для копирования контента
    """
    with open(base_template_file, 'r', encoding='utf-8') as f:
        base_content = f.read()
    
    template = Template(base_content)
    
    for city in cities:
        # Создаем уникальные title и description
        city_vars = {
            'city': city['name'],
            'base_equipment': 'листогибов',  # или другой тип
            'price_from': city['price_from'],
            'delivery_fee': city['delivery_fee'],
            'emergency_fee': city['emergency_fee']
        }
        
        # Генерируем контент
        output = template.render(**city_vars)
        
        # Сохраняем
        filename = f"remont-listogibov-{city['slug']}.html"
        output_path = os.path.join('output/new_pages', filename)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(output)
        
        print(f"Created: {filename}")

if __name__ == "__main__":
    # Загружаем список городов из JSON
    with open('data/cities.json', 'r', encoding='utf-8') as f:
        cities = json.load(f)
    
    generate_geo_pages('../remont-listogibov.html', cities, 'remont-listogibov')
```

**Файл data/cities.json:**
```json
[
  {
    "name": "Москва",
    "slug": "moskva",
    "price_from": "15 000",
    "delivery_fee": "Бесплатно",
    "emergency_fee": "Без наценки"
  },
  {
    "name": "Санкт-Петербург",
    "slug": "spb",
    "price_from": "18 000",
    "delivery_fee": "от 5 000 ₽",
    "emergency_fee": "+50%"
  },
  {
    "name": "Екатеринбург",
    "slug": "ekb",
    "price_from": "22 000",
    "delivery_fee": "от 8 000 ₽",
    "emergency_fee": "+80%"
  }
]
```

---

## 📊 ФАЗА 5: МОНИТОРИНГ И ОТЧЕТНОСТЬ (День 5+)

### 5.1: seo_reporter.py
```python
"""
Генерация еженедельного SEO-отчета
"""
import pandas as pd
from datetime import datetime

def generate_weekly_report():
    report_date = datetime.now().strftime("%Y-%m-%d")
    
    # Читаем анализы
    meta_report = pd.read_csv('output/reports/meta_analysis.csv')
    broken_links = pd.read_csv('output/reports/broken_links.csv')
    
    total_pages = len(meta_report)
    pages_with_issues = len(meta_report[meta_report['title_status'] != 'OK']) + \
                       len(meta_report[meta_report['desc_status'] != 'OK'])
    
    report = f"""
SEO Report for 24stanki.ru
Date: {report_date}
================================

📊 ИНДЕКСАЦИЯ
- Всего страниц: {total_pages}
- Страниц с ошибками meta: {pages_with_issues}
- Битых ссылок: {len(broken_links)}

⚠️ ПРОБЛЕМЫ
- Дубликатов title: {len(meta_report[meta_report.duplicated(['title'], keep=False)])}
- Слишком коротких title (<50): {len(meta_report[meta_report['title_len'] < 50])}
- Слишком длинных title (>160): {len(meta_report[meta_report['title_len'] > 160])}
- Без keywords: {len(meta_report[~meta_report['has_keywords']])}

📋 РЕКОМЕНДАЦИИ
1. Исправить {pages_with_issues} страниц с meta-тегами
2. Добавить keywords на все страницы
3. Устранить {len(broken_links)} битых ссылок
4. Создать 72 гео-лендинга
5. Написать 10 сравнительных страниц

🎯 ЦЕЛИ НА НЕДЕЛЮ
- Создать 10 новых страниц
- Исправить все meta-теги
- Проверить все внутренние ссылки

---
Сгенерировано автоматически seo_reporter.py
"""
    
    with open('output/reports/weekly_seo_report.txt', 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(report)

if __name__ == "__main__":
    generate_weekly_report()
```

---

## ✅ ЧЕКЛИСТ ВЫПОЛНЕНИЯ (ЕЖЕДНЕВНЫЙ)

### День 1:
- [ ] Установить uv, создать виртуальное окружение
- [ ] Установить зависимости (beautifulsoup4, lxml, pandas, jinja2)
- [ ] Создать структуру папок seo-tools/
- [ ] Написать и протестировать meta_analyzer.py
- [ ] Создать sravnenie-listogibov-i-gilotin.html
- [ ] Создать sravnenie-trubogibov-i-profilgebiv.html

### День 2:
- [ ] Создать kakoj-stanok-vybrat-dlya-proizvodstva.html
- [ ] Создать top-10-luchshih-markov-stankov-2025.html
- [ ] Создать remont-listogibov-moskva.html
- [ ] Создать remont-listogibov-spb.html
- [ ] Создать remont-gilotin-moskva.html
- [ ] Создать remont-gilotin-spb.html

### День 3:
- [ ] Создать remont-trubogibov-moskva.html
- [ ] Создать remont-trubogibov-spb.html
- [ ] Написать и протестировать geo_pages_generator.py
- [ ] Добавить breadcrumbs на 10 существующих страниц
- [ ] Добавить Open Graph на 10 существующих страниц
- [ ] Обновить styles.css (увеличить шрифты, контраст)

### День 4:
- [ ] Написать link_checker.py
- [ ] Написать keyword_extractor.py (если успеем)
- [ ] Запустить полный аудит сайта (meta_analyzer, link_checker)
- [ ] Исправить найденные ошибки (дубли, битые ссылки)
- [ ] Создать sitemap.py для автоматического обновления sitemap

### День 5+:
- [ ] Продолжать создавать гео-лендинги (оставшиеся 8 городов × 6 типов = 48 страниц)
- [ ] Продолжать создавать сравнительные страницы (еще 5-10)
- [ ] Писать инфо-статьи (FAQ, диагностика, ТО)
- [ ] Создать страницы запчастей, диагностики, гарантии

---

## 📈 КРИТЕРИИ УСПЕХА

| Показатель | Цель | Проверка |
|------------|------|----------|
| Количество страниц | 150+ | sitemap.xml |
| Avg слово на страницу | 2000+ | meta_analyzer.py |
| Уникальность title | 100% | meta_analyzer.py |
| Битые ссылки | 0 | link_checker.py |
| Время загрузки | <3 сек | PageSpeed Insights |
| Schema.org | на каждой | ручная проверка |

---

## 🚦 ПРИОРИТЕТЫ НА СЕГОДНЯ (ПЕРВЫЙ ДЕНЬ В ACT MODE)

**Немедленно начать:**

1. ✅ Создать папку `seo-tools` и структуру
2. ✅ Создать `seo-tools/pyproject.toml`
3. ✅ Инициализировать uv виртуальное окружение
4. ✅ Установить зависимости через uv
5. ✅ Написать `meta_analyzer.py` и протестировать
6. ✅ Создать первую сравнительную страницу `sravnenie-listogibov-i-gilotin.html`
7. ✅ Добавить breadcrumbs и OG на index.html как шаблон

**Команды для запуска:**
```bash
# Перейти в папку seo-tools
cd seo-tools

# Создать виртуальное окружение
uv venv .venv

# Активировать (Windows)
.venv\Scripts\activate

# Установить зависимости в Development режиме
uv pip install -e .

# Запустить анализатор meta-тегов
python src/meta_analyzer.py

# Если ошибок нет - начинаем создавать страницы
```

---

**Версия:** 2.0 - Детальный план выполнения  
**Следующий шаг:** Выполнить пункты 1-7 из "Приоритеты на сегодня"