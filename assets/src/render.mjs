// Render every element with an id starting with "logo-" or "fig-" in
// the given HTML files to assets/<id>.png, at twice the size.
//
//     node render.mjs logos.html figures.html
//
// Needs Playwright. If FONTS is set to a directory of .woff2 files
// named like IBMPlexMono-600.woff2 or FiraSans-900i.woff2, they are
// used instead of fetching Google Fonts.

import { chromium } from 'playwright';
import { readdirSync, readFileSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const fonts = process.env.FONTS;

function localFontCSS() {
  let css = '';
  for (const f of readdirSync(fonts)) {
    const m = f.match(/^(.+)-(\d+)(i?)\.woff2$/);
    if (!m) continue;
    const family = m[1].replace(/([a-z])([A-Z])/g, '$1 $2').replace('I B M', 'IBM');
    css += `@font-face { font-family: '${family}'; font-weight: ${m[2]}; ` +
           `font-style: ${m[3] ? 'italic' : 'normal'}; src: url(data:font/woff2;base64,` +
           readFileSync(resolve(fonts, f)).toString('base64') + '); }\n';
  }
  return css;
}

const browser = await chromium.launch();
const page = await browser.newPage({ deviceScaleFactor: 2, viewport: { width: 1000, height: 800 } });
if (fonts) {
  const css = localFontCSS();
  await page.route('https://fonts.googleapis.com/**', r => r.fulfill({ contentType: 'text/css', body: css }));
}
for (const file of process.argv.slice(2)) {
  await page.goto('file://' + resolve(here, file));
  await page.addStyleTag({ content: 'body { background: transparent !important; }' });
  await page.evaluate(() => document.fonts.ready);
  const ids = await page.$$eval('[id^="logo-"], [id^="fig-"]', els => els.map(e => e.id));
  for (const id of ids) {
    await page.locator('#' + id).screenshot({ path: resolve(here, '..', id + '.png'), omitBackground: true });
    console.log('assets/' + id + '.png');
  }
}
await browser.close();
