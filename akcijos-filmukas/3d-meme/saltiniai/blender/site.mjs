import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import fs from 'fs';
const css = fs.readFileSync('brand/inter-inline.css', 'utf8');
const b = await chromium.launch(); const p = await b.newPage();
await p.setContent('<html><head><style>' + css + '</style></head><body><canvas id=c width=900 height=1950></canvas></body></html>');
await p.evaluate(async () => { for (const w of [500, 600, 700, 800]) await document.fonts.load(w + ' 40px Inter'); });
const url = await p.evaluate(() => {
  const c = document.getElementById('c'), x = c.getContext('2d'), W = 900, H = 1950;
  const rr = (X, Y, w, h, r) => { x.beginPath(); x.roundRect(X, Y, w, h, r); };
  x.fillStyle = '#FFFDF8'; x.fillRect(0, 0, W, H);
  // status bar + nav
  x.fillStyle = '#1D1B18'; x.font = '600 34px Inter'; x.fillText('9:41', 60, 80);
  x.fillStyle = '#3B2A1E'; x.font = '800 44px Inter'; x.fillText('Sunrise', 60, 190); x.fillStyle = '#C9772F'; x.fillText('Bakery', 238, 190);
  x.fillStyle = '#3B2A1E'; for (let i = 0; i < 3; i++) { rr(780, 150 + i * 18, 60, 7, 4); x.fill(); }
  // hero photo: warm gradient, bread loaves
  const g = x.createLinearGradient(0, 240, 0, 960); g.addColorStop(0, '#F6D9B5'); g.addColorStop(1, '#D99B5B'); rr(40, 240, 820, 720, 40); x.save(); x.clip(); x.fillStyle = g; x.fillRect(40, 240, 820, 720);
  x.fillStyle = 'rgba(255,255,255,0.35)'; x.beginPath(); x.arc(650, 380, 110, 0, 7); x.fill();
  const loaf = (cx, cy, w, h, col) => { x.fillStyle = col; x.beginPath(); x.ellipse(cx, cy, w, h, 0, Math.PI, 0); x.lineTo(cx + w, cy + 30); x.lineTo(cx - w, cy + 30); x.fill(); x.strokeStyle = 'rgba(255,240,210,0.7)'; x.lineWidth = 8; for (let i = -1; i <= 1; i++) { x.beginPath(); x.moveTo(cx + i * w * 0.45 - 30, cy - h * 0.55); x.lineTo(cx + i * w * 0.45 + 30, cy - h * 0.2); x.stroke(); } };
  x.fillStyle = '#8A5A33'; x.fillRect(40, 840, 820, 120);
  loaf(300, 840, 210, 160, '#A9652E'); loaf(600, 860, 170, 120, '#BC7A3C');
  x.restore();
  x.fillStyle = '#2A1E16'; x.font = '800 92px Inter'; x.fillText('Fresh bread,', 60, 1110); x.fillText('every morning.', 60, 1215);
  x.fillStyle = '#6B5A4C'; x.font = '500 40px Inter'; x.fillText('Sourdough, croissants and coffee', 60, 1300); x.fillText('in the heart of Vilnius.', 60, 1352);
  x.fillStyle = '#C9772F'; rr(60, 1420, 420, 120, 60); x.fill(); x.fillStyle = '#fff'; x.font = '700 44px Inter'; x.fillText('Order now', 160, 1495);
  x.strokeStyle = '#3B2A1E'; x.lineWidth = 4; rr(510, 1420, 330, 120, 60); x.stroke(); x.fillStyle = '#3B2A1E'; x.fillText('Menu', 620, 1495);
  ['Sourdough', 'Croissant', 'Cinnamon'].forEach((s, i) => { const X = 60 + i * 270; x.fillStyle = '#F3E6D6'; rr(X, 1610, 240, 260, 28); x.fill(); x.fillStyle = ['#B8743A', '#D99B5B', '#A0582A'][i]; x.beginPath(); x.ellipse(X + 120, 1710, 80, 52, 0, 0, 7); x.fill(); x.fillStyle = '#2A1E16'; x.font = '700 32px Inter'; x.fillText(s, X + 22, 1830); });
  return c.toDataURL('image/png');
});
fs.writeFileSync('b3d/site.png', Buffer.from(url.split(',')[1], 'base64'));
await b.close(); console.log('site.png');
