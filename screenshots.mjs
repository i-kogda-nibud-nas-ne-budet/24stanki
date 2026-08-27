import puppeteer from 'puppeteer';
import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const PAGES = [
  // Index
  { name: 'index-desktop', file: 'index.html', width: 1440, height: 900 },
  { name: 'index-mobile', file: 'index.html', width: 375, height: 812 },
  // Услуги
  { name: 'uslugi-desktop', file: 'uslugi.html', width: 1440, height: 900 },
  { name: 'uslugi-mobile', file: 'uslugi.html', width: 375, height: 812 },
  // Цены
  { name: 'price-desktop', file: 'price.html', width: 1440, height: 900 },
  { name: 'price-mobile', file: 'price.html', width: 375, height: 812 },
  // Портфолио
  { name: 'portfolio-desktop', file: 'portfolio.html', width: 1440, height: 900 },
  { name: 'portfolio-mobile', file: 'portfolio.html', width: 375, height: 812 },
  // Блог
  { name: 'blog-desktop', file: 'blog.html', width: 1440, height: 900 },
  { name: 'blog-mobile', file: 'blog.html', width: 375, height: 812 },
  // Сервисные страницы
  { name: 'remont-listogibov-desktop', file: 'remont-listogibov.html', width: 1440, height: 900 },
  { name: 'remont-listogibov-mobile', file: 'remont-listogibov.html', width: 375, height: 812 },
  { name: 'remont-gilotin-desktop', file: 'remont-gilotin.html', width: 1440, height: 900 },
  { name: 'remont-trubogibov-desktop', file: 'remont-trubogibov.html', width: 1440, height: 900 },
  { name: 'remont-lentochnyh-pil-desktop', file: 'remont-lentochnyh-pil.html', width: 1440, height: 900 },
  { name: 'remont-profilgebiv-desktop', file: 'remont-profilgebiv.html', width: 1440, height: 900 },
  { name: 'remont-valtsev-desktop', file: 'remont-valtsev.html', width: 1440, height: 900 },
  // Блог-статьи (образцы)
  { name: 'blog-remont-listogiba-desktop', file: 'blog-remont-listogiba.html', width: 1440, height: 900 },
  { name: 'blog-remont-gilotin-desktop', file: 'blog-remont-gilotin.html', width: 1440, height: 900 },
  // Geo-страница (образец)
  { name: 'geo-moskva-desktop', file: 'remont-listogibov-moskva.html', width: 1440, height: 900 },
  { name: 'geo-moskva-mobile', file: 'remont-listogibov-moskva.html', width: 375, height: 812 },
];

async function main() {
  const outDir = path.join(__dirname, 'screenshots');
  if (!fs.existsSync(outDir)) fs.mkdirSync(outDir);

  const browser = await puppeteer.launch({ headless: 'new' });

  for (const p of PAGES) {
    const page = await browser.newPage();
    await page.setViewport({ width: p.width, height: p.height });
    
    const url = 'file:///' + path.join(__dirname, p.file).replace(/\\/g, '/');
    
    try {
      await page.goto(url, { waitUntil: 'networkidle2', timeout: 30000 });
      
      // Wait for initial load
      await new Promise(r => setTimeout(r, 1000));
      
      // Force-trigger all animations (bypass IntersectionObserver)
      await page.evaluate(() => {
        document.querySelectorAll('.reveal, .reveal-left, .reveal-right, .reveal-scale, .stagger').forEach(el => {
          el.classList.add('visible');
        });
        document.querySelectorAll('.stagger.visible > *').forEach(el => {
          el.style.opacity = '1';
          el.style.transform = 'translateY(0)';
        });
      });
      
      // Wait for CSS transitions
      await new Promise(r => setTimeout(r, 1500));
      
      const outPath = path.join(outDir, p.name + '.png');
      await page.screenshot({ path: outPath, fullPage: true });
      
      console.log(`OK ${p.name} (${p.width}x${p.height})`);
    } catch (err) {
      console.log(`FAIL ${p.name}: ${err.message}`);
    }
    await page.close();
  }

  await browser.close();
  console.log(`Done! ${PAGES.length} screenshots in ${outDir}`);
}

main().catch(err => {
  console.error('Error:', err.message);
});
