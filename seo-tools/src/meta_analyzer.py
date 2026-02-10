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
import sys
from bs4 import BeautifulSoup
import pandas as pd

def analyze_meta_tags(directory):
    results = []
    print(f"Анализирую директорию: {directory}")
    
    for root, dirs, files in os.walk(directory):
        # Пропускаем папки seo-tools, node_modules и т.д.
        if 'seo-tools' in root or 'node_modules' in root or '.git' in root:
            continue
            
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        soup = BeautifulSoup(f.read(), 'lxml')
                        
                        title = soup.title.string if soup.title else ''
                        desc = soup.find('meta', {'name': 'description'})
                        desc_content = desc['content'] if desc else ''
                        keywords = soup.find('meta', {'name': 'keywords'})
                        keywords_content = keywords['content'] if keywords else ''
                        
                        results.append({
                            'page': file,
                            'path': filepath,
                            'title': title,
                            'title_len': len(title),
                            'description': desc_content,
                            'desc_len': len(desc_content),
                            'keywords': keywords_content,
                            'has_keywords': bool(keywords),
                            'title_status': 'OK' if 50 <= len(title) <= 160 else 'TOO_SHORT' if len(title) < 50 else 'TOO_LONG',
                            'desc_status': 'OK' if 120 <= len(desc_content) <= 320 else 'TOO_SHORT' if len(desc_content) < 120 else 'TOO_LONG'
                        })
                except Exception as e:
                    print(f"Ошибка при обработке {file}: {e}")
    
    if not results:
        print("Не найдено HTML страниц для анализа!")
        return None
    
    df = pd.DataFrame(results)
    
    # Проверяем дубли title
    duplicate_titles = df[df.duplicated(['title'], keep=False) & (df['title'] != '')]
    duplicate_descs = df[df.duplicated(['description'], keep=False) & (df['description'] != '')]
    
    print("\n" + "="*60)
    print("РЕЗУЛЬТАТЫ АНАЛИЗА META-ТЕГОВ")
    print("="*60)
    print(f"Проанализировано страниц: {len(df)}")
    print(f"Дубликатов title: {len(duplicate_titles)}")
    print(f"Дубликатов description: {len(duplicate_descs)}")
    print(f"Страниц без keywords: {len(df[~df['has_keywords']])}")
    print(f"Слишком коротких title (<50): {len(df[df['title_len'] < 50])}")
    print(f"Слишком длинных title (>160): {len(df[df['title_len'] > 160])}")
    print(f"Слишком коротких description (<120): {len(df[df['desc_len'] < 120])}")
    print(f"Слишком длинных description (>320): {len(df[df['desc_len'] > 320])}")
    
    # Показываем примеры проблем
    if len(duplicate_titles) > 0:
        print("\n⚠️ Дубли title:")
        for idx, row in duplicate_titles.head(5).iterrows():
            print(f"  {row['page']}: {row['title'][:80]}...")
    
    if len(duplicate_descs) > 0:
        print("\n⚠️ Дубли description:")
        for idx, row in duplicate_descs.head(5).iterrows():
            print(f"  {row['page']}: {row['description'][:80]}...")
    
    # Создаем папку для отчетов если нет
    os.makedirs('output/reports', exist_ok=True)
    
    # Сохраняем отчеты
    df.to_csv('output/reports/meta_analysis.csv', index=False, encoding='utf-8')
    duplicate_titles.to_csv('output/reports/duplicate_titles.csv', index=False, encoding='utf-8')
    duplicate_descs.to_csv('output/reports/duplicate_descs.csv', index=False, encoding='utf-8')
    
    print("\n✅ Отчеты сохранены:")
    print("  - output/reports/meta_analysis.csv")
    print("  - output/reports/duplicate_titles.csv")
    print("  - output/reports/duplicate_descs.csv")
    print("\n" + "="*60)
    
    return df

if __name__ == "__main__":
    # Анализируем директорию выше (корень сайта)
    result = analyze_meta_tags('..')
    
    if result is not None:
        # Возвращаем код для CI/CD
        issues_count = len(result[result['title_status'] != 'OK']) + len(result[result['desc_status'] != 'OK'])
        if issues_count > 0:
            print(f"\n❌ Найдено {issues_count} проблем с meta-тегами")
            sys.exit(1)
        else:
            print("\n✅ Все meta-теги в порядке!")
            sys.exit(0)