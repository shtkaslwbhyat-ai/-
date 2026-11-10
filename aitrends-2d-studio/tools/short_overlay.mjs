// Renders a transparent 1080x1920 PNG overlay for a Short: hook text on top, CTA at the bottom.
// Usage: node tools/short_overlay.mjs "<hook>" "<cta>" out.png
import { chromium } from 'playwright';
import path from 'node:path';
import fs from 'node:fs';
import { fileURLToPath } from 'node:url';

const [hook, cta, out] = process.argv.slice(2);
const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const font = (f) => 'data:font/woff2;base64,' + fs.readFileSync(path.join(ROOT, 'node_modules/@fontsource/cairo/files', f)).toString('base64');
const html = `<!doctype html><html dir="rtl"><head><meta charset="utf-8"><style>
@font-face{font-family:Cairo;font-weight:900;src:url(${font('cairo-arabic-900-normal.woff2')});unicode-range:U+0600-06FF,U+FB50-FDFF,U+FE70-FEFF}
@font-face{font-family:Cairo;font-weight:900;src:url(${font('cairo-latin-900-normal.woff2')});unicode-range:U+0000-00FF,U+2000-206F}
html,body{margin:0;width:1080px;height:1920px;background:transparent;font-family:Cairo;}
.hook{position:absolute;top:150px;left:60px;right:60px;text-align:center;font-weight:900;font-size:92px;line-height:1.25;color:#fff;
  -webkit-text-stroke:14px #000;paint-order:stroke fill;text-shadow:0 8px 24px rgba(0,0,0,.6)}
.hook b{color:#FFD400}
.cta{position:absolute;bottom:230px;left:120px;right:120px;text-align:center;font-weight:900;font-size:54px;color:#111;
  background:#FFD400;border-radius:60px;padding:22px 30px;box-shadow:0 10px 30px rgba(0,0,0,.5)}
</style></head><body><div class="hook">${hook}</div><div class="cta">${cta}</div></body></html>`;
const b = await chromium.launch(process.env.CHROME_PATH ? { executablePath: process.env.CHROME_PATH } : {});
const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
await p.setContent(html, { waitUntil: 'load' }); await p.evaluate(async () => { await document.fonts.load('900 92px Cairo', 'abc 0123456789'); await document.fonts.load('900 92px Cairo', 'عربي'); await document.fonts.ready; });
await p.screenshot({ path: out, omitBackground: true });
await b.close();
