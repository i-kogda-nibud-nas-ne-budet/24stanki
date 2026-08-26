# TODO — Полный аудит и исправление страниц 24stanki.ru

> **Дата:** 26.08.2026
> **Статус:** На согласовании
> **Основная проблема:** inner pages используют другой шаблон чем index.html

---

## Сводная таблица: CSS-классы по страницам

| Страница | Классов | Без CSS | Статус |
|----------|---------|---------|--------|
| index.html | 65 | 0 | ✅ |
| price.html | 43 | 0 | ✅ |
| uslugi.html | 60 | **19** | ❌ |
| portfolio.html | 43 | **3** | ❌ |
| blog.html | 38 | 0 | ✅ |
| remont-listogibov.html | 61 | **4** | ❌ |
| remont-gilotin.html | 61 | **4** | ❌ |
| sravnenie-*.html | 32 | 0 | ✅ |
| blog-remont-listogiba.html | 44 | **13** | ❌ |

**Итого: 43 класса без CSS в 5 страницах**

---

## Детальные проблемы по страницам

### uslugi.html (19 missing classes)

| Класс | Где используется | Нужен CSS? |
|-------|-----------------|------------|
| `step` | Секция "Как мы работаем" | ДА — стилизовать как process-step |
| `gear`, `gear2`, `gear3` | Декоративные SVG-иконки | НЕТ — скрыты через display:none |
| `wrench`, `wrench2`, `wrench3` | Декоративные SVG-иконки | НЕТ — скрыты |
| `spring`, `spring2`, `spring3` | Декоративные SVG-иконки | НЕТ — скрыты |
| `bolt`, `bolt2`, `bolt3` | Декоративные SVG-иконки | НЕТ — скрыты |
| `hammer`, `hammer2`, `hammer3` | Декоративные SVG-иконки | НЕТ — скрыты |
| `drill`, `drill2`, `drill3` | Декоративные SVG-иконки | НЕТ — скрыты |

**Вывод:** 18 из 19 — скрытые декоративные элементы. Нужен CSS только для `.step`.

### portfolio.html (3 missing classes)

| Класс | Где используется | Нужен CSS? |
|-------|-----------------|------------|
| `portfolio-filter` | Обёртка фильтров | ДА |
| `filter-btn` | Кнопки фильтров | ДА |
| `meta-item` | Мета-данные в карточках | ДА |

### remont-listogibov.html (4 missing classes)

| Класс | Где используется | Нужен CSS? |
|-------|-----------------|------------|
| `step` | Секция "Как мы работаем" | ДА |
| `faq` | Секция FAQ | ДА |
| `price` | Цена в карточке | ДА |
| `blog-links` | Ссылки на блог | ДА |

### remont-gilotin.html (4 missing — same)

| Класс | Нужен CSS? |
|-------|------------|
| `step` | ДА |
| `faq` | ДА |
| `price` | ДА |
| `blog-links` | ДА |

### blog-remont-listogiba.html (13 missing classes)

| Класс | Где используется | Нужен CSS? |
|-------|-----------------|------------|
| `blog-article` | Обёртка статьи | ДА |
| `blog-meta` | Мета-данные статьи | ДА |
| `date` | Дата публикации | ДА |
| `category` | Категория статьи | ДА |
| `blog-cta` | CTA-блок в статье | ДА |
| `cta-button` | Кнопка CTA | ДА |
| `faq-section` | Секция FAQ | ДА |
| `gear`, `wrench`, `spring`, `bolt`, `hammer`, `drill` | Декоративные SVG | НЕТ — скрыты |

---

## План исправлений

### Этап 1: Добавить CSS для 7 отсутствующих классов (критично)

**Время:** 1 час
**Ответственный:** @coder

Добавить в styles.css:

```css
/* Step (process steps for inner pages) */
.step {
  text-align: center;
  padding: 1.5rem;
}
.step .step-number {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--c-primary), var(--c-accent));
  border-radius: 50%;
  font-weight: 700;
  font-size: 1.2rem;
  color: var(--c-white);
  margin: 0 auto 1rem;
}

/* Portfolio filter */
.portfolio-filter {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  margin-bottom: 2rem;
}
.filter-btn {
  padding: 0.5rem 1.2rem;
  background: var(--c-bg-card);
  border: 1px solid var(--c-border);
  border-radius: var(--radius-full);
  color: var(--c-text-muted);
  cursor: pointer;
  transition: var(--transition);
  font-size: 0.85rem;
}
.filter-btn:hover, .filter-btn.active {
  background: var(--c-primary);
  color: var(--c-white);
  border-color: var(--c-primary);
}
.meta-item {
  font-size: 0.8rem;
  color: var(--c-text-muted);
}

/* FAQ section */
.faq, .faq-section {
  padding: 3rem 0;
}
.faq h2 {
  margin-bottom: 1.5rem;
}

/* Price in cards */
.price {
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--c-primary);
  margin-top: 0.5rem;
}

/* Blog links */
.blog-links {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  margin-top: 1.5rem;
}
.blog-links a {
  color: var(--c-primary);
  font-weight: 600;
  text-decoration: none;
}

/* Blog article (full page) */
.blog-article {
  max-width: 800px;
  margin: 0 auto;
}
.blog-meta {
  display: flex;
  gap: 1rem;
  font-size: 0.85rem;
  color: var(--c-text-muted);
  margin-bottom: 2rem;
}
.blog-meta .date, .blog-meta .category {
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
}
.blog-meta .category {
  color: var(--c-primary);
  font-weight: 600;
  text-transform: uppercase;
  font-size: 0.75rem;
}

/* Blog CTA */
.blog-cta {
  background: linear-gradient(135deg, rgba(246,9,9,0.08), rgba(227,158,8,0.05));
  border: 1px solid rgba(246,9,9,0.2);
  border-radius: var(--radius-lg);
  padding: 2rem;
  text-align: center;
  margin: 2rem 0;
}
.cta-button {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.8rem 2rem;
  background: linear-gradient(135deg, var(--c-primary), var(--c-accent));
  color: var(--c-white);
  border-radius: var(--radius-full);
  font-weight: 600;
  text-decoration: none;
  transition: var(--transition);
}
.cta-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(246,9,9,0.3);
}
```

**Критерии:** Все 43 отсутствующих класса имеют CSS. `grep` показывает 0 missing.

### Этап 2: Исправить грамматику и опечатки

**Время:** 30 мин
**Ответственный:** @coder

| Файл | Проблема | Исправление |
|------|----------|-------------|
| blog-remont-listogiba.html | `@ya.ru` (2 раза) | `@yandex.ru` |
| remont-listogibov.html | `давлением` | `давление` |
| remont-gilotin.html | `Правильная профилактическое` | `Правильное профилактическое` |

**Критерии:** 0 опечаток, grep показывает 0 вхождений.

### Этап 3: Убрать декоративные SVG (dead code)

**Время:** 15 мин
**Ответственный:** @coder

Убрать скрытые SVG-элементы из uslugi.html и blog-remont-listogiba.html:
- `.floating-elements` div (пустые или скрытые)
- Все `gear`, `wrench`, `spring`, `bolt`, `hammer`, `drill` элементы

**Критерии:** 0 скрытых декоративных элементов.

### Этап 4: Проверка через скрины

**Время:** 30 мин
**Ответственный:** @tester

Запустить screenshots-live.mjs и проверить:
1. Все 9 основных страниц
2. Каждый элемент выглядит стилизованным
3. Нет raw HTML без стилей
4. Нет orphan-элементов

**Критерии:** Все страницы визуальноConsistent с index.html.

---

## Итого

| Этап | Время | Приоритет |
|------|-------|-----------|
| 1. CSS для 7 классов | 1 ч | 🔴 Critical |
| 2. Грамматика/опечатки | 30 мин | 🟡 High |
| 3. Убрать dead SVG | 15 мин | 🟢 Low |
| 4. Проверка через скрины | 30 мин | 🟡 High |
| **ИТОГО** | **2 ч 15 мин** | |

---

## Вопрос

Начинаю? Или есть другие приоритеты?
