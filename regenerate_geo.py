"""Delete existing geo pages and regenerate them."""
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# Base service pages - DO NOT DELETE
BASE_SERVICES = {
    "remont-listogibov.html",
    "remont-gilotin.html", 
    "remont-trubogibov.html",
    "remont-lentochnyh-pil.html",
    "remont-profilgebiv.html",
    "remont-valtsev.html",
    "remont-armaturogiba.html",
    "remont-ruchnogo-trubogiba.html",
}

# Find and delete geo pages (remont-*-<city>.html)
deleted = 0
for f in ROOT.glob("remont-*.html"):
    if f.name in BASE_SERVICES:
        continue
    # Geo pages have pattern: remont-<service>-<city>.html
    # They contain a city name after the service type
    parts = f.stem.split("-", 2)
    if len(parts) >= 3:
        f.unlink()
        deleted += 1

print(f"Deleted {deleted} geo pages")

# Now run the generator
sys.path.insert(0, str(ROOT / "seo-tools" / "src"))
from generate_geo_pages import GeoPagesGenerator

generator = GeoPagesGenerator()
stats = generator.generate_all_pages()

print(f"\nGeneration complete:")
print(f"  Created: {stats['created_pages']}")
print(f"  Skipped: {stats['skipped_pages']}")
print(f"  Errors: {stats['errors']}")
