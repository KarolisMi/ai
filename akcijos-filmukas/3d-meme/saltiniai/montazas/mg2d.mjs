// node mg2d.mjs <segment id> <out.mp4> [bg.png] [stillsOnly t1,t2...]
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import { spawn } from 'child_process';
import fs from 'fs';
import path from 'path';
const here = path.dirname(new URL(import.meta.url).pathname);
const [, , id, out, bg, stills] = process.argv;
const css = fs.readFileSync(path.join(here, '../brand/inter-inline.css'), 'utf8');
const html = fs.readFileSync(path.join(here, 'mg2d.html'), 'utf8').replace('__FONTS__', css);
const durl = (p, mime) => `data:${mime};base64,` + fs.readFileSync(p).toString('base64');
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
p.on('pageerror', e => console.error('PAGEERR', e.message));
await p.setContent(html);
const assets = { mark: durl(path.join(here, '../brand/mark.png'), 'image/png'), site: durl(path.join(here, '../b3d/site.png'), 'image/png') };
if (bg && bg !== '-') assets.bg = durl(bg, 'image/png');
await p.evaluate(async ({ assets, id, screen, tr }) => {
  for (const [k, v] of Object.entries(assets)) await window.mg.load(k, v);
  for (const w of [500, 600, 700, 800, 900]) await document.fonts.load(w + ' 60px Inter');
  window.mg.set(Number(id));
  if (screen) window.SCREEN = screen;
  if (tr) window.TRANSPARENT = true;
}, { assets, id, screen: process.env.SCREEN ? JSON.parse(process.env.SCREEN) : null, tr: !!process.env.TRANSPARENT });
await p.evaluate(() => { const m = IMG.mark; if (!m) return; const c = document.createElement('canvas'); c.width = m.width; c.height = m.height; const x = c.getContext('2d'); x.drawImage(m, 0, 0); x.globalCompositeOperation = 'source-in'; x.fillStyle = '#fff'; x.fillRect(0, 0, c.width, c.height); IMG.markw = c; });
const dur = await p.evaluate(id => window.mg.SEG[id].dur, Number(id));
const grab = t => p.evaluate(t => { window.mg.frame(t); return window.mg.canvas.toDataURL('image/png').split(',')[1]; }, t);
if (stills) {
  for (const t of stills.split(',').map(Number)) fs.writeFileSync(out.replace('.mp4', `_${t}.png`), Buffer.from(await grab(t), 'base64'));
} else {
  const fps = 24, n = Math.round(dur * fps);
  const ff = spawn('ffmpeg', ['-loglevel', 'error', '-y', '-f', 'image2pipe', '-framerate', String(fps), '-i', '-', '-c:v', 'libx264', '-crf', '16', '-pix_fmt', 'yuv420p', out], { stdio: ['pipe', 'ignore', 'inherit'] });
  for (let i = 0; i < n; i++) { const buf = Buffer.from(await grab(i / fps), 'base64'); if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r)); }
  ff.stdin.end(); await new Promise(r => ff.on('close', r));
}
await b.close();
console.log('ok', id, dur);
