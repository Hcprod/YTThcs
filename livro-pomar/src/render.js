// Converte build/interior.html e build/capa.html em PDF (Chromium via Playwright).
const { chromium } = require('playwright');
const path = require('path');
const build = path.join(__dirname, '..', 'build');

(async () => {
  const browser = await chromium.launch();
  for (const name of ['interior', 'capa']) {
    const page = await browser.newPage();
    await page.goto('file://' + path.join(build, name + '.html'));
    await page.evaluate(() => document.fonts.ready);
    await page.pdf({
      path: path.join(build, name + '.pdf'),
      preferCSSPageSize: true,
      printBackground: true,
    });
    console.log('ok', name + '.pdf');
  }
  await browser.close();
})();
