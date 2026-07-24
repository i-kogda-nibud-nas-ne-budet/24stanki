import puppeteer from 'puppeteer';
import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const PAGES = [
  { name: 'index-desktop', file: 'index.html', width: 1440, height: 900 },
  { name: 'index-mobile', file: 'index.html', width: 375, height: 812 },
  { name: 'about-desktop', file: 'about.html', width: 1440, height: 900 },
  { name: 'about-mobile', file: 'about.html', width: 375, height: 812 },
  { name: 'price-desktop', file: 'price.html', width: 1440, height: 900 },
  { name: 'portfolio-desktop', file: 'portfolio.html', width: 1440, height: 900 },
  { name: 'blog-desktop', file: 'blog.html', width: 1440, height: 900 },
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
    await page.goto(url, { waitUntil: 'networkidle2', timeout: 30000 });
    
    // Wait for initial load
    await new Promise(r => setTimeout(r, 1000));
    
    // Force-trigger all animations (bypass IntersectionObserver)
    await page.evaluate(() => {
      // Add 'visible' to ALL animate-able elements
      document.querySelectorAll('.reveal, .reveal-left, .reveal-right, .reveal-scale, .stagger').forEach(el => {
        el.classList.add('visible');
      });
      // Trigger all stagger children
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
    await page.close();
  }

  await browser.close();
  console.log(`Done! ${PAGES.length} screenshots in ${outDir}`);
}

main().catch(err => {
  console.error('Error:', err.message);
});
