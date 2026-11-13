// Fotografa cada pagina de build/ebook.html e a frente da capa (build/capa.html).
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
const build = path.join(__dirname, '..', 'build');
const out = path.join(build, 'ebook_img');

(async () => {
  fs.rmSync(out, { recursive: true, force: true });
  fs.mkdirSync(out, { recursive: true });
  const browser = await browser_();
  async function browser_() { return chromium.launch(); }
  const scale = 2;
  // paginas
  let page = await browser.newPage({ viewport: { width: 816, height: 1056 }, deviceScaleFactor: scale });
  await page.goto('file://' + path.join(build, 'ebook.html'));
  await page.evaluate(() => document.fonts.ready);
  const secs = await page.$$('section.page');
  for (let i = 0; i < secs.length; i++) {
    await secs[i].screenshot({ path: path.join(out, `p${String(i + 1).padStart(2, '0')}.png`) });
  }
  // capa: recorta so a frente (sem sangria)
  page = await browser.newPage({ viewport: { width: 1700, height: 1100 }, deviceScaleFactor: scale });
  await page.goto('file://' + path.join(build, 'capa.html'));
  await page.evaluate(() => document.fonts.ready);
  // no e-book nao da para colorir: troca o subtitulo da capa
  await page.evaluate(() => {
    for (const t of document.querySelectorAll('text')) {
      if (t.textContent === 'Aventuras para colorir') t.textContent = 'Aventuras do folclore brasileiro';
    }
  });
  const svgBox = await (await page.$('svg')).boundingBox();
  const dpi = 96, bleed = 0.125;
  const frontX = svgBox.x + svgBox.width - (8.5 + bleed) * dpi;
  await page.screenshot({
    path: path.join(out, 'cover.png'),
    clip: { x: frontX, y: svgBox.y + bleed * dpi, width: 8.5 * dpi, height: 11 * dpi },
  });
  console.log('ok', secs.length, 'paginas + capa');
  await browser.close();
})();
