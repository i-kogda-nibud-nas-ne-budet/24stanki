#!/usr/bin/env python3
"""
Генератор geo-страниц для 24stanki.ru

Создает geo-страницы для всех городов из cities.json
для 8 типов услуг ремонта оборудования.
"""

import json
import os
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('geo_pages_generator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class GeoPagesGenerator:
    """Генератор geo-страниц"""

    def __init__(self, base_dir: str = None):
        """
        Инициализация генератора

        Args:
            base_dir: Базовая директория проекта (по умолчанию - родительская папка src/)
        """
        if base_dir is None:
            # Определяем базовую директорию относительно расположения скрипта
            script_dir = Path(__file__).parent
            self.base_dir = script_dir.parent
        else:
            self.base_dir = Path(base_dir).resolve()
        self.cities_file = self.base_dir / "data" / "cities.json"
        self.output_dir = self.base_dir.parent
        self.sitemap_file = self.output_dir / "sitemap.xml"
        self.robots_file = self.output_dir / "robots.txt"

        # Типы услуг и их базовые страницы
        self.service_types = {
            "remont-listogibov": {
                "base_file": "remont-listogibov.html",
                "name": "листогибов",
                "name_genitive": "листогибов",
                "name_accusative": "листогибы"
            },
            "remont-gilotin": {
                "base_file": "remont-gilotin.html",
                "name": "гильотин",
                "name_genitive": "гильотин",
                "name_accusative": "гильотины"
            },
            "remont-trubogibov": {
                "base_file": "remont-trubogibov.html",
                "name": "трубогибов",
                "name_genitive": "трубогибов",
                "name_accusative": "трубогибы"
            },
            "remont-lentochnyh-pil": {
                "base_file": "remont-lentochnyh-pil.html",
                "name": "ленточных пил",
                "name_genitive": "ленточных пил",
                "name_accusative": "ленточные пилы"
            },
            "remont-profilgebiv": {
                "base_file": "remont-profilgebiv.html",
                "name": "профилегибов",
                "name_genitive": "профилегибов",
                "name_accusative": "профилегибы"
            },
            "remont-valtsev": {
                "base_file": "remont-valtsev.html",
                "name": "вальцевых",
                "name_genitive": "вальцевых",
                "name_accusative": "вальцевые"
            },
            "remont-armaturogiba": {
                "base_file": "remont-armaturogiba.html",
                "name": "арматурогибов",
                "name_genitive": "арматурогибов",
                "name_accusative": "арматурогибы"
            },
            "remont-ruchnogo-trubogiba": {
                "base_file": "remont-ruchnogo-trubogiba.html",
                "name": "ручных трубогибов",
                "name_genitive": "ручных трубогибов",
                "name_accusative": "ручные трубогибы"
            }
        }

        # Цены по городам (базовая цена)
        self.base_prices = {
            "Москва": 15000,
            "Санкт-Петербург": 18000,
            "Новосибирск": 20000,
            "Екатеринбург": 18000,
            "default": 15000
        }

        # Статистика
        self.stats = {
            "total_cities": 0,
            "total_pages": 0,
            "created_pages": 0,
            "skipped_pages": 0,
            "errors": 0
        }

    def load_cities(self) -> List[Dict]:
        """
        Загрузка городов из JSON файла

        Returns:
            Список городов
        """
        try:
            with open(self.cities_file, 'r', encoding='utf-8') as f:
                cities = json.load(f)
                logger.info(f"Загружено {len(cities)} городов")
                return cities
        except Exception as e:
            logger.error(f"Ошибка загрузки городов: {e}")
            return []

    def transliterate(self, text: str) -> str:
        """
        Транслитерация русского текста в латиницу

        Args:
            text: Русский текст

        Returns:
            Транслитерированный текст
        """
        # Словарь транслитерации
        translit_dict = {
            'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
            'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
            'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
            'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
            'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch',
            'ш': 'sh', 'щ': 'shch', 'ъ': '', 'ы': 'y', 'ь': '',
            'э': 'e', 'ю': 'yu', 'я': 'ya',
            'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D',
            'Е': 'E', 'Ё': 'Yo', 'Ж': 'Zh', 'З': 'Z', 'И': 'I',
            'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N',
            'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T',
            'У': 'U', 'Ф': 'F', 'Х': 'Kh', 'Ц': 'Ts', 'Ч': 'Ch',
            'Ш': 'Sh', 'Щ': 'Shch', 'Ъ': '', 'Ы': 'Y', 'Ь': '',
            'Э': 'E', 'Ю': 'Yu', 'Я': 'Ya'
        }

        result = []
        for char in text:
            result.append(translit_dict.get(char, char))
        return ''.join(result)

    def get_city_forms(self, city_name: str) -> Dict[str, str]:
        """
        Получение формы города в разных падежах

        Args:
            city_name: Название города

        Returns:
            Словарь с формами города
        """
        # Простая реализация - в реальном проекте нужно использовать pymorphy2
        forms = {
            "nominative": city_name,
            "genitive": city_name,
            "dative": city_name,
            "accusative": city_name,
            "instrumental": city_name,
            "prepositional": city_name
        }

        # Особые случаи для крупных городов
        special_cases = {
            "Москва": {
                "nominative": "Москва",
                "genitive": "Москвы",
                "dative": "Москве",
                "accusative": "Москву",
                "instrumental": "Москвой",
                "prepositional": "Москве"
            },
            "Санкт-Петербург": {
                "nominative": "Санкт-Петербург",
                "genitive": "Санкт-Петербурга",
                "dative": "Санкт-Петербургу",
                "accusative": "Санкт-Петербург",
                "instrumental": "Санкт-Петербургом",
                "prepositional": "Санкт-Петербурге"
            },
            "Новосибирск": {
                "nominative": "Новосибирск",
                "genitive": "Новосибирска",
                "dative": "Новосибирску",
                "accusative": "Новосибирск",
                "instrumental": "Новосибирском",
                "prepositional": "Новосибирске"
            },
            "Екатеринбург": {
                "nominative": "Екатеринбург",
                "genitive": "Екатеринбурга",
                "dative": "Екатеринбургу",
                "accusative": "Екатеринбург",
                "instrumental": "Екатеринбургом",
                "prepositional": "Екатеринбурге"
            }
        }

        if city_name in special_cases:
            return special_cases[city_name]

        return forms

    def get_city_price(self, city_name: str) -> int:
        """
        Получение цены для города

        Args:
            city_name: Название города

        Returns:
            Цена в рублях
        """
        return self.base_prices.get(city_name, self.base_prices["default"])

    def read_base_page(self, service_type: str) -> str:
        """
        Чтение базовой страницы для типа услуги

        Args:
            service_type: Тип услуги

        Returns:
            Содержимое базовой страницы
        """
        base_file = self.service_types[service_type]["base_file"]
        file_path = self.output_dir / base_file

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                logger.info(f"Прочитана базовая страница: {base_file}")
                return content
        except Exception as e:
            logger.error(f"Ошибка чтения базовой страницы {base_file}: {e}")
            return ""

    def generate_page_content(
        self,
        base_content: str,
        city_name: str,
        city_region: str,
        service_type: str
    ) -> str:
        """
        Генерация контента страницы с заменой плейсхолдеров

        Args:
            base_content: Базовое содержимое страницы
            city_name: Название города
            city_region: Название региона
            service_type: Тип услуги

        Returns:
            Сгенерированное содержимое страницы
        """
        service_info = self.service_types[service_type]
        city_forms = self.get_city_forms(city_name)
        city_price = self.get_city_price(city_name)

        # Транслитерация названия города для URL
        city_url = self.transliterate(city_name).lower().replace(' ', '-')

        # URL страницы
        page_url = f"https://24stanki.ru/{service_type}-{city_url}.html"

        # Замена плейсхолдеров
        content = base_content

        # Замена названия города
        content = re.sub(
            r'в Москве',
            f'в {city_forms["prepositional"]}',
            content
        )
        content = re.sub(
            r'Москве',
            city_forms["prepositional"],
            content
        )
        content = re.sub(
            r'Москву',
            city_forms["accusative"],
            content
        )
        content = re.sub(
            r'Москвы',
            city_forms["genitive"],
            content
        )

        # Замена цены
        content = re.sub(
            r'от 15 000 ₽',
            f'от {city_price:,} ₽'.replace(',', ' '),
            content
        )
        content = re.sub(
            r'15 000 ₽',
            f'{city_price:,} ₽'.replace(',', ' '),
            content
        )

        # Замена URL
        content = re.sub(
            r'https://24stanki.ru/[^"]+\.html',
            page_url,
            content
        )

        # Замена канонического тега
        content = re.sub(
            r'<link rel="canonical" href="[^"]+">',
            f'<link rel="canonical" href="{page_url}">',
            content
        )

        # Замена в мета-тегах
        content = re.sub(
            r'<title>[^<]+</title>',
            f'<title>Ремонт {service_info["name_genitive"]} в {city_forms["prepositional"]} - цены 2025, выезд 24/7 | 24stanki.ru</title>',
            content
        )

        content = re.sub(
            r'<meta name="description" content="[^"]+">',
            f'<meta name="description" content="Профессиональный ремонт {service_info["name_genitive"]} в {city_forms["prepositional"]} от {city_price:,} ₽. Выезд мастера в день обращения. Гарантия 6 месяцев. ☎ 8 (993) 908-98-37">'.replace(',', ' '),
            content
        )

        content = re.sub(
            r'<meta name="keywords" content="[^"]+">',
            f'<meta name="keywords" content="ремонт {service_info["name_genitive"]} {city_forms["genitive"]}, ремонт {service_info["name"]} цена {city_forms["genitive"]}, выезд мастера на ремонт {service_info["name_accusative"]} {city_forms["prepositional"]}, сервис {service_info["name"]} {city_forms["genitive"]}">',
            content
        )

        # Замена в Open Graph тегах
        content = re.sub(
            r'<meta property="og:url" content="[^"]+">',
            f'<meta property="og:url" content="{page_url}">',
            content
        )
        content = re.sub(
            r'<meta property="og:title" content="[^"]+">',
            f'<meta property="og:title" content="Ремонт {service_info["name_genitive"]} в {city_forms["prepositional"]} - цены 2025, выезд 24/7">',
            content
        )
        content = re.sub(
            r'<meta property="og:description" content="[^"]+">',
            f'<meta property="og:description" content="Профессиональный ремонт {service_info["name_genitive"]} в {city_forms["prepositional"]}. Выезд мастера в день обращения. Гарантия 6 месяцев.">',
            content
        )

        # Замена в Twitter Cards
        content = re.sub(
            r'<meta property="twitter:url" content="[^"]+">',
            f'<meta property="twitter:url" content="{page_url}">',
            content
        )
        content = re.sub(
            r'<meta property="twitter:title" content="[^"]+">',
            f'<meta property="twitter:title" content="Ремонт {service_info["name_genitive"]} в {city_forms["prepositional"]} - цены 2025, выезд 24/7">',
            content
        )
        content = re.sub(
            r'<meta property="twitter:description" content="[^"]+">',
            f'<meta property="twitter:description" content="Профессиональный ремонт {service_info["name_genitive"]} в {city_forms["prepositional"]}. Выезд мастера в день обращения. Гарантия 6 месяцев.">',
            content
        )

        # Замена в Schema.org разметке
        content = re.sub(
            r'"name": "Ремонт [^"]+"',
            f'"name": "Ремонт {service_info["name_genitive"]} в {city_forms["prepositional"]}"',
            content
        )
        content = re.sub(
            r'"description": "[^"]+"',
            f'"description": "Профессиональный ремонт {service_info["name_genitive"]} в {city_forms["prepositional"]}. Выезд 24/7, гарантия 6 месяцев."',
            content
        )
        content = re.sub(
            r'"addressLocality": "[^"]+"',
            f'"addressLocality": "{city_name}"',
            content
        )
        content = re.sub(
            r'"name": "[^"]+"',
            f'"name": "{city_name}"',
            content
        )

        # Замена в BreadcrumbList
        content = re.sub(
            r'"name": "Ремонт [^"]+"',
            f'"name": "Ремонт {service_info["name_genitive"]}"',
            content
        )
        content = re.sub(
            r'"item": "https://24stanki.ru/[^"]+"',
            f'"item": "https://24stanki.ru/{service_type}.html"',
            content
        )

        # Замена цены в Schema.org
        content = re.sub(
            r'"priceRange": "[^"]+"',
            f'"priceRange": "от {city_price:,} ₽"'.replace(',', ' '),
            content
        )

        # Добавление уникального city-контента
        unique_content = f'''
<section class="city-unique-content">
<div class="container">
<h2>Ремонт {service_info["name_genitive"]} в {city_name} и {city_region}</h2>
<p><strong>{city_region}</strong> — важный промышленный регион России с развитым машиностроением, металлообрабатывающей и производственной отраслями. Здесь работают десятки предприятий, использующих {service_info["name_accusative"]} в своих производственных процессах.</p>
<p>Наши специалисты имеют обширный опыт работы с оборудованием в {city_region}. Мы понимаем специфику местных производств и готовы предложить оптимальные решения для ремонта и обслуживания {service_info["name_genitive"]}.</p>
<p>В <strong>{city_name}</strong> и по всей {city_region} мы обеспечиваем: срочный выезд в день обращения, диагностику на месте, гарантию 6 месяцев, работу с оригинальными запчастями и качественными аналогами.</p>
<p>Крупные предприятия {city_region}, которые могут нуждаться в ремонте {service_info["name_genitive"]}: машиностроительные заводы, металлообрабатывающие производства, строительные компании, предприятия энергетического сектора.</p>
</div>
</section>
'''

        content = content.replace('<!-- CITY_UNIQUE_CONTENT -->', unique_content)

        return content

    def generate_geo_page(
        self,
        city_name: str,
        city_region: str,
        service_type: str
    ) -> bool:
        """
        Генерация geo-страницы

        Args:
            city_name: Название города
            city_region: Название региона
            service_type: Тип услуги

        Returns:
            True если страница создана успешно, иначе False
        """
        try:
            # Транслитерация названия города для имени файла
            city_url = self.transliterate(city_name).lower().replace(' ', '-')
            filename = f"{service_type}-{city_url}.html"
            filepath = self.output_dir / filename

            # Проверка существования файла
            if filepath.exists():
                logger.info(f"Файл уже существует: {filename}")
                self.stats["skipped_pages"] += 1
                return True

            # Чтение базовой страницы
            base_content = self.read_base_page(service_type)
            if not base_content:
                logger.error(f"Не удалось прочитать базовую страницу для {service_type}")
                return False

            # Генерация контента
            content = self.generate_page_content(
                base_content,
                city_name,
                city_region,
                service_type
            )

            # Запись файла
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

            logger.info(f"Создана страница: {filename}")
            self.stats["created_pages"] += 1
            return True

        except Exception as e:
            logger.error(f"Ошибка создания страницы {service_type}-{city_name}: {e}")
            self.stats["errors"] += 1
            return False

    def update_sitemap(self) -> bool:
        """
        Обновление sitemap.xml

        Returns:
            True если sitemap обновлен успешно, иначе False
        """
        try:
            # Чтение существующего sitemap
            if not self.sitemap_file.exists():
                logger.error("Файл sitemap.xml не существует")
                return False

            with open(self.sitemap_file, 'r', encoding='utf-8') as f:
                sitemap_content = f.read()

            # Поиск всех HTML файлов в директории
            html_files = list(self.output_dir.glob("*.html"))

            # Генерация записей для sitemap
            sitemap_entries = []
            current_date = datetime.now().strftime("%Y-%m-%d")

            for html_file in html_files:
                # Пропускаем базовые страницы (без городов)
                if any(service_type in html_file.name for service_type in self.service_types.keys()):
                    # Это geo-страница
                    url = f"https://24stanki.ru/{html_file.name}"
                    sitemap_entries.append(f""" <url>
 <loc>{url}</loc>
 <lastmod>{current_date}</lastmod>
 <changefreq>monthly</changefreq>
 <priority>0.8</priority>
 </url>""")

            # Обновление sitemap
            urlset_start = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            urlset_end = '\n</urlset>'

            new_sitemap = urlset_start + '\n'.join(sitemap_entries) + urlset_end

            with open(self.sitemap_file, 'w', encoding='utf-8') as f:
                f.write(new_sitemap)

            logger.info(f"Sitemap.xml обновлен: {len(sitemap_entries)} записей")
            return True

        except Exception as e:
            logger.error(f"Ошибка обновления sitemap.xml: {e}")
            return False

    def update_robots(self) -> bool:
        """
        Обновление robots.txt

        Returns:
            True если robots.txt обновлен успешно, иначе False
        """
        try:
            robots_content = """User-agent: *
Allow: /
Disallow: /seo-tools/
Disallow: /images/

Sitemap: https://24stanki.ru/sitemap.xml
"""

            with open(self.robots_file, 'w', encoding='utf-8') as f:
                f.write(robots_content)

            logger.info("robots.txt обновлен")
            return True

        except Exception as e:
            logger.error(f"Ошибка обновления robots.txt: {e}")
            return False

    def generate_all_pages(self, limit: int = None) -> Dict:
        """
        Генерация всех geo-страниц

        Args:
            limit: Ограничение количества городов (для тестирования)

        Returns:
            Статистика генерации
        """
        logger.info("Начало генерации geo-страниц")

        # Загрузка городов
        cities = self.load_cities()
        if not cities:
            logger.error("Не удалось загрузить города")
            return self.stats

        self.stats["total_cities"] = len(cities)
        self.stats["total_pages"] = len(cities) * len(self.service_types)

        # Применение ограничения
        if limit:
            cities = cities[:limit]
            logger.info(f"Применено ограничение: {limit} городов")

        # Генерация страниц для каждого города
        for i, city in enumerate(cities, 1):
            city_name = city["name"]
            city_region = city["region"]

            logger.info(f"Обработка города {i}/{len(cities)}: {city_name}")

            # Генерация страниц для каждого типа услуг
            for service_type in self.service_types.keys():
                success = self.generate_geo_page(city_name, city_region, service_type)
                if not success:
                    logger.error(f"Ошибка создания страницы для {service_type} в {city_name}")

        # Обновление sitemap и robots.txt
        logger.info("Обновление sitemap.xml")
        self.update_sitemap()

        logger.info("Обновление robots.txt")
        self.update_robots()

        # Вывод статистики
        logger.info("=" * 50)
        logger.info("Статистика генерации:")
        logger.info(f"Всего городов: {self.stats['total_cities']}")
        logger.info(f"Всего страниц: {self.stats['total_pages']}")
        logger.info(f"Создано страниц: {self.stats['created_pages']}")
        logger.info(f"Пропущено страниц: {self.stats['skipped_pages']}")
        logger.info(f"Ошибок: {self.stats['errors']}")
        logger.info("=" * 50)

        return self.stats


def main():
    """Главная функция"""
    logger.info("Запуск генератора geo-страниц")

    # Создание генератора
    generator = GeoPagesGenerator()

    # Генерация всех страниц
    # Для тестирования можно использовать limit=10
    stats = generator.generate_all_pages(limit=None)

    logger.info("Генерация завершена")


if __name__ == "__main__":
    main()
