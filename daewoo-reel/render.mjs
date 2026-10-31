// Frame-accurate renderer: index.html (GSAP timeline) → MP4 via headless Chromium + ffmpeg.
//
//   node render.mjs                         full render → out/daewoo-8-promises.mp4
//   node render.mjs --stills 0,1.5,12,64    PNG stills → out/stills/
//   node render.mjs --from 7 --to 14        partial render (preview)
//   options: --workers 4  --crf 17  --out path.mp4
//
// Every frame is produced with tl.seek(frame / fps), so output is deterministic.
// GSAP and Vazirmatn are served from node_modules (requests to cdnjs / Google Fonts are intercepted),
// so rendering works offline and is reproducible.
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import puppeteer from 'puppeteer-core';

const ROOT = path.dirname(fileURLToPath(import.meta.url));
const argv = process.argv.slice(2);
const arg = (k, d) => { const i = argv.indexOf('--' + k); return i >= 0 ? argv[i + 1] : d; };
const FPS = 30;
const WORKERS = +arg('workers', 4);
const CRF = arg('crf', '17');
const OUT = path.resolve(ROOT, arg('out', 'out/daewoo-8-promises.mp4'));
const STILLS = arg('stills', null);
const CHROME = process.env.CHROME_PATH ||
  ['/opt/pw-browsers/chromium-1243/chrome-linux64/chrome', '/usr/bin/chromium', '/usr/bin/google-chrome']
    .find(p => fs.existsSync(p));

// ---- local static server ---------------------------------------------------
const server = http.createServer((req, res) => {
  const p = path.join(ROOT, decodeURIComponent(new URL(req.url, 'http://x').pathname));
  if (!p.startsWith(ROOT) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { res.writeHead(404); return res.end(); }
  const type = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.woff2': 'font/woff2', '.css': 'text/css' }[path.extname(p)] || 'application/octet-stream';
  res.writeHead(200, { 'content-type': type }); fs.createReadStream(p).pipe(res);
});
await new Promise(r => server.listen(0, '127.0.0.1', r));
const BASE = `http://127.0.0.1:${server.address().port}`;

// ---- offline font / GSAP substitution -------------------------------------
const FONT_DIR = 'node_modules/@fontsource/vazirmatn/files';
const fontCss = ['arabic', 'latin'].flatMap(sub => [300, 500, 800].map(w => `@font-face{font-family:'Vazirmatn';font-style:normal;font-weight:${w};font-display:block;
  src:url(${BASE}/${FONT_DIR}/vazirmatn-${sub}-${w}-normal.woff2) format('woff2');
  unicode-range:${sub === 'arabic' ? 'U+0600-06FF,U+0750-077F,U+0870-088E,U+0890-0891,U+0897-08E1,U+08E3-08FF,U+200C-200E,U+2010-2011,U+204F,U+2E41,U+FB50-FDFF,U+FE70-FE74,U+FE76-FEFC' : 'U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD'};}`)).join('\n');
const GSAP = fs.readFileSync(path.join(ROOT, 'node_modules/gsap/dist/gsap.min.js'));

async function openPage(browser) {
  const page = await browser.newPage();
  await page.setViewport({ width: 1080, height: 1920, deviceScaleFactor: 1 });
  await page.setRequestInterception(true);
  page.on('request', r => {
    const u = r.url();
    if (u.includes('cdnjs.cloudflare.com/ajax/libs/gsap/')) return r.respond({ status: 200, contentType: 'text/javascript', body: GSAP });
    if (u.startsWith('https://fonts.googleapis.com/')) return r.respond({ status: 200, contentType: 'text/css', body: fontCss });
    if (u.startsWith(BASE) || u.startsWith('data:')) return r.continue();
    return r.abort();
  });
  page.on('pageerror', e => console.error('[page]', e.message));
  await page.goto(`${BASE}/index.html?render=1`, { waitUntil: 'load' });
  await page.waitForFunction('window.__ready === true', { timeout: 60000 });
  return page;
}

const browser = await puppeteer.launch({
  executablePath: CHROME, headless: true,
  args: ['--no-sandbox', '--force-color-profile=srgb', '--font-render-hinting=none', '--hide-scrollbars', '--disable-lcd-text']
});
const duration = await (async () => { const p = await openPage(browser); const d = await p.evaluate('CONFIG.duration'); await p.close(); return d; })();
const shot = (page, t) => page.evaluate(t => window.renderAt(t), t).then(() => page.screenshot({ type: 'png', clip: { x: 0, y: 0, width: 1080, height: 1920 }, captureBeyondViewport: false }));

if (STILLS) {
  const dir = path.join(ROOT, 'out/stills'); fs.mkdirSync(dir, { recursive: true });
  const page = await openPage(browser);
  for (const t of STILLS.split(',').map(Number)) {
    fs.writeFileSync(path.join(dir, `t${t.toFixed(2).padStart(6, '0')}.png`), await shot(page, t));
    console.log('still', t);
  }
  await browser.close(); server.close(); process.exit(0);
}

const f0 = Math.round(+arg('from', 0) * FPS);
const f1 = Math.min(Math.round(+arg('to', duration) * FPS), Math.round(duration * FPS));
const total = f1 - f0;
const tmp = path.join(ROOT, 'out/.segments'); fs.rmSync(tmp, { recursive: true, force: true }); fs.mkdirSync(tmp, { recursive: true });
fs.mkdirSync(path.dirname(OUT), { recursive: true });
console.log(`Rendering ${total} frames (${(total / FPS).toFixed(2)}s) with ${WORKERS} workers…`);

let done = 0; const t0 = Date.now();
const chunk = Math.ceil(total / WORKERS);
const segs = [];
await Promise.all(Array.from({ length: WORKERS }, async (_, w) => {
  const a = f0 + w * chunk, b = Math.min(f1, a + chunk);
  if (a >= b) return;
  const file = path.join(tmp, `seg${w}.mp4`); segs[w] = file;
  const page = await openPage(browser);
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'png', '-i', '-',
    '-vf', 'scale=out_color_matrix=bt709:out_range=tv,format=yuv420p',
    '-c:v', 'libx264', '-preset', 'slow', '-crf', CRF, '-profile:v', 'high', '-level', '4.2', '-tune', 'film',
    '-g', '60', '-bf', '2', '-x264-params', 'keyint=60:min-keyint=60:scenecut=0',
    '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv',
    '-r', String(FPS), file], { stdio: ['pipe', 'inherit', 'inherit'] });
  const closed = new Promise((res, rej) => ff.on('close', c => c === 0 ? res() : rej(new Error('ffmpeg ' + c))));
  for (let f = a; f < b; f++) {
    const buf = await shot(page, f / FPS);
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (++done % 60 === 0) { const s = (Date.now() - t0) / 1000; console.log(`  ${done}/${total}  ${(done / s).toFixed(1)} fps  eta ${Math.round((total - done) / (done / s))}s`); }
  }
  ff.stdin.end(); await closed; await page.close();
}));
await browser.close(); server.close();

// concat segments + silent stereo track (Instagram-friendly), faststart
const list = path.join(tmp, 'list.txt');
fs.writeFileSync(list, segs.filter(Boolean).map(f => `file '${f}'`).join('\n'));
await new Promise((res, rej) => spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', list,
  '-f', 'lavfi', '-i', 'anullsrc=channel_layout=stereo:sample_rate=48000',
  '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '128k', '-shortest', '-movflags', '+faststart', OUT],
  { stdio: 'inherit' }).on('close', c => c === 0 ? res() : rej(new Error('concat ' + c))));
fs.rmSync(tmp, { recursive: true, force: true });
console.log(`✔ ${path.relative(process.cwd(), OUT)}  (${((Date.now() - t0) / 1000).toFixed(0)}s)`);
