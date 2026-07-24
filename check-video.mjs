import puppeteer from 'puppeteer';

const browser = await puppeteer.launch({ headless: 'new' });
const page = await browser.newPage();
await page.setViewport({ width: 1440, height: 900 });

await page.goto('https://24stanki.ru/', { waitUntil: 'networkidle2' });
await new Promise(r => setTimeout(r, 3000));

await page.screenshot({
  path: 'screenshots-live/hero-video-check.png',
  clip: { x: 0, y: 0, width: 1440, height: 900 }
});

await browser.close();
console.log('Done: screenshots-live/hero-video-check.png');
