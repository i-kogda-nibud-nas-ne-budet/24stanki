# TODO — Аудит текста, структуры и стилей 24stanki.ru

> **Дата:** 25.08.2026
> **Статус:** На согласовании

---

## Найденные проблемы

### 🔴 Critical: Текст

| # | Файл | Проблема | Текст | Исправление |
|---|------|----------|-------|-------------|
| 1 | index.html | Английское слово | "Срочный выезд possible 24/7" | → "Срочный выезд 24/7" |
| 2 | about.html | Опечатка | "диагостическое" | → "диагностическое" |
| 3 | price.html | Английское слово | "для popular марок" | → "для популярных марок" |
| 4 | price.html | Английское слово | "для European станков" | → "для европейских станков" |
| 5 | uslugi.html | Грамматика | "Минимализируем" | → "Минимизируем" |
| 6 | blog-remont-cpu-stoiki.html | Опечатка бренда | "Cebelec" (17 раз) | → "Cybelec" |
| 7 | blog-remont-chpu-stoyki-delem-instrukciya.html | Неверная страна | "Cebelec (Германия)" | → "Cybelec (Швейцария)" |

### 🔴 Critical: Структура контента

| # | Файл | Проблема |
|---|------|----------|
| 8 | sravnenie-listogibov-i-gilotin.html | **Неверный контент!** Title/H1/body = "Какой станок выбрать" вместо "Сравнение листогибов и гильотин" |
| 9 | sravnenie-trubogibov-i-profilgebiv.html | **Неверный контент!** Title/H1/body = "Какой станок выбрать" вместо "Сравнение трубогибов и профилегибов" |
| 10 | blog-remont-chpu-stoyki-delem-instrukciya.html | Дублирующиеся абзацы (2 блока) |

### 🟡 High: CSS — отсутствующие классы (~30)

Основная проблема: **innerHTML-страницы используют CSS-классы, которых нет в styles.css**

| Группа классов | Где используются | Что стилизовать |
|----------------|------------------|-----------------|
| `blog-card-*` (image, content, category, title, excerpt, meta, link) | blog.html, blog-*.html | Карточки блога |
| `service-price` | sravnenie, remont-*.html | Цены в карточках |
| `contact-row`, `phone-widget`, `email-widget` | footer всех inner-страниц | Контакты в футере |
| `social-links`, `quick-links` | footer всех inner-страниц | Ссылки в футере |
| `emergency-notice` | remont-*.html, sravnenie | Банер аварийного ремонта |
| `dropbtn`, `icon`, `whatsapp`, `telegram`, `email` | навигация, contact-cta | Иконки и кнопки |
| `faq-question`, `faq-answer`, `faq-icon` | remont-*.html | Аккордеон FAQ |
| `footer-info` | sravnenie | Информация в футере |

### 🟡 High: Структура HTML

| # | Проблема | Файлы |
|---|----------|-------|
| 11 | Две разные системы навигации | index.html (fixed nav) vs inner pages (header nav) |
| 12 | Отсутствует hamburger на sravnenie | sravnenie-*.html |
| 13 | Битая ссылка | blog.html → blog-remont-gibochnyh-stankov.html (404) |
| 14 | Дублирующий Service schema | uslugi.html (2 одинаковых блока) |
| 15 | Несогласованный FAQ markup | index: `<details>`, inner: `<div class="faq-item">` |
| 16 | Несогласованные шрифты | index: Montserrat 600-800, inner: Montserrat 700 + Roboto Condensed (не используется) |

---

## План исправлений

### Этап 1: Исправление текста (Critical)

**Время:** 30 мин
**Ответственный:** @coder

1. Исправить 7 текстовых ошибок (English слова, опечатки, грамматика)
2. Исправить "Cebelec" → "Cybelec" во всех файлах
3. Удалить дублирующиеся абзацы в blog-remont-chpu-stoyki-delem-instrukciya.html

**Критерии:** 0 English слов в русском тексте, 0 опечаток

### Этап 2: Исправление контента статей (Critical)

**Время:** 2-3 часа
**Ответственный:** @coder

1. Восстановить правильный контент в sravnenie-listogibov-i-gilotin.html (сравнение листогибов и гильотин)
2. Восстановить правильный контент в sravnenie-trubogibov-i-profilgebiv.html (сравнение трубогибов и профилегибов)
3. Убедиться, что title/H1/meta совпадают с содержимым

**Критерии:** Каждая статья содержит уникальный контент, соответствующий title

### Этап 3: CSS для отсутствующих классов (High)

**Время:** 3-4 часа
**Ответственный:** @frontend-developer

1. Добавить стили для `blog-card-*` (карточки блога)
2. Добавить стили для `service-price`, `emergency-notice`
3. Добавить стили для footer: `social-links`, `quick-links`, `footer-info`
4. Добавить стили для contact-cta: `contact-row`, `phone-widget`, `email-widget`
5. Добавить стили для FAQ: `faq-question`, `faq-answer`, `faq-icon`
6. Добавить стили для навигации: `dropbtn`, `icon`, `whatsapp`, `telegram`, `email`
7. Добавить hamburger на sravnenie-*.html

**Критерии:** Все CSS-классы, используемые в HTML, имеют определение в styles.css

### Этап 4: Согласование структуры (High)

**Время:** 2-3 часа
**Ответственный:** @frontend-developer

1. Привести навигацию inner-страниц к виду index.html (fixed nav с .nav-inner)
2. Или: оставить текущую навигацию, но сделать её консистентной
3. Убрать дублирующий Service schema из uslugi.html
4. Исправить битую ссылку в blog.html
5. Согласовать FAQ markup (выбрать один формат)
6. Убрать Roboto Condensed из font-loading (не используется)

**Критерии:** Единый паттерн навигации на всех страницах, 0 битых ссылок

### Этап 5: Финальная проверка

**Время:** 1 час
**Ответственный:** @tester

1. Проверить все исправления
2. Визуально открыть 10 страниц
3. Проверить mobile навигацию
4. Проверить FAQ аккордеон

---

## Автоматические инструменты для CI

| Инструмент | Язык | Что проверяет | Установка |
|------------|------|---------------|-----------|
| **vnu** | Java | Валидация HTML/CSS (W3C) | `npm install vnu-jar` |
| **linkchecker** | Python | Битые ссылки | `pip install linkchecker` |
| **pyspellchecker** | Python | Правописание (русский) | `pip install pyspellchecker` |
| **language-tool-python** | Python | Грамматика (русский) | `pip install language-tool-python` |
| **lighthouse** | Node.js | SEO, производительность, a11y | `npm install -g lighthouse` |
| **pa11y** | Node.js | Доступность (WCAG) | `npm install -g pa11y` |

**Рекомендуемый стек для CI:**
```
vnu (HTML/CSS) + linkchecker (ссылки) + pyspellchecker (правописание) + lighthouse (SEO/perf)
```

---

## Итого

| Этап | Время | Приоритет |
|------|-------|-----------|
| 1. Текст | 30 мин | 🔴 Critical |
| 2. Контент статей | 2-3 ч | 🔴 Critical |
| 3. CSS классы | 3-4 ч | 🟡 High |
| 4. Структура | 2-3 ч | 🟡 High |
| 5. Проверка | 1 ч | 🟡 High |
| **ИТОГО** | **9-12 ч** | |

---

## Вопрос

1. **Навигация:** Заменять inner-страницы на fixed nav из index.html (больше работы, но единообразно) или оставить текущую и просто стилизовать?
2. **Инструменты:** Установить linkchecker + pyspellchecker в seo-tools для автоматических проверок?
