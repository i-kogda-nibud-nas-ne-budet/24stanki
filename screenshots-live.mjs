import puppeteer from 'puppeteer';
import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const PAGES = [
  { name: 'live-index-desktop', url: 'https://24stanki.ru/', width: 1440, height: 900 },
  { name: 'live-index-mobile', url: 'https://24stanki.ru/', width: 375, height: 812 },
  { name: 'live-about', url: 'https://24stanki.ru/about.html', width: 1440, height: 900 },
  { name: 'live-price', url: 'https://24stanki.ru/price.html', width: 1440, height: 900 },
  { name: 'live-portfolio', url: 'https://24stanki.ru/portfolio.html', width: 1440, height: 900 },
  { name: 'live-blog', url: 'https://24stanki.ru/blog.html', width: 1440, height: 900 },
  { name: 'live-geo-desktop', url: 'https://24stanki.ru/remont-listogibov-moskva.html', width: 1440, height: 900 },
  { name: 'live-geo-mobile', url: 'https://24stanki.ru/remont-listogibov-moskva.html', width: 375, height: 812 },
];

async function main() {
  const outDir = path.join(__dirname, 'screenshots-live');
  if (!fs.existsSync(outDir)) fs.mkdirSync(outDir);

  const browser = await puppeteer.launch({ headless: 'new' });

  for (const p of PAGES) {
    const page = await browser.newPage();
    await page.setViewport({ width: p.width, height: p.height });
    
    try {
      await page.goto(p.url, { waitUntil: 'networkidle2', timeout: 30000 });
      
      // Wait for load
      await new Promise(r => setTimeout(r, 2000));
      
      // Force-trigger animations
      await page.evaluate(() => {
        document.querySelectorAll('.reveal, .reveal-left, .reveal-right, .reveal-scale, .stagger').forEach(el => {
          el.classList.add('visible');
        });
        document.querySelectorAll('.stagger.visible > *').forEach(el => {
          el.style.opacity = '1';
          el.style.transform = 'translateY(0)';
        });
      });
      
      await new Promise(r => setTimeout(r, 1500));
      
      const outPath = path.join(outDir, p.name + '.png');
      await page.screenshot({ path: outPath, fullPage: true });
      
      console.log(`OK ${p.name}`);
    } catch (err) {
      console.log(`FAIL ${p.name}: ${err.message}`);
    }
    await page.close();
  }

  await browser.close();
  console.log(`Done! Screenshots in ${outDir}`);
}

main().catch(err => {
  console.error('Error:', err.message);
});
