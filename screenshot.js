const puppeteer = require('puppeteer-core');

(async () => {
  const browser = await puppeteer.launch({
    headless: true,
    executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    args: ['--no-sandbox', '--disable-gpu']
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 900 });

  // Homepage
  await page.goto('http://127.0.0.1:8000/', { waitUntil: 'networkidle0', timeout: 15000 });
  await page.screenshot({ path: 'screenshot_home.jpg', type: 'jpeg', quality: 90 });
  console.log('Homepage screenshot saved');

  // Product list
  await page.goto('http://127.0.0.1:8000/products/', { waitUntil: 'networkidle0', timeout: 15000 });
  await page.screenshot({ path: 'screenshot_products.jpg', type: 'jpeg', quality: 90 });
  console.log('Product list screenshot saved');

  // Fitment selector
  await page.goto('http://127.0.0.1:8000/fitment/', { waitUntil: 'networkidle0', timeout: 15000 });
  await page.screenshot({ path: 'screenshot_fitment.jpg', type: 'jpeg', quality: 90 });
  console.log('Fitment selector screenshot saved');

  // Product detail
  await page.goto('http://127.0.0.1:8000/products/michelin-pilot-sport-4/', { waitUntil: 'networkidle0', timeout: 15000 });
  await page.screenshot({ path: 'screenshot_detail.jpg', type: 'jpeg', quality: 90 });
  console.log('Product detail screenshot saved');

  await browser.close();
  console.log('All screenshots done!');
})().catch(e => { console.error(e); process.exit(1); });
