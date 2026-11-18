// sets/places.js — every location of the story. Each set: fn(g, t, cam, o) -> { GY, CX, M }.
// Value structure: walls in shadow, 1–3 bright accents (window / lamp / screen), floor dark with a light pool.
import { E, V, mood, layer, backdrop, rr, seg, circle, ring, poly, linGrad, radGrad, glow, alpha, shade, mix, text, FONTS } from '/engine/core.js';
import * as FX from '/engine/fx2d.js';

export const ground = () => E.H * V(0.8, 0.68);

function wallAndFloor(g, M, GY, o = {}) {
  const wall = shade(M.wall, o.wallK ?? -0.25);
  g.fillStyle = linGrad(g, 0, -E.H, 0, GY, [shade(wall, -0.5), wall, shade(wall, 0.05)]); g.fillRect(-E.W * 1.5, -E.H, E.W * 4, GY + E.H);
  g.fillStyle = shade(wall, -0.45); g.fillRect(-E.W * 1.5, GY - 26, E.W * 4, 26);            // skirting
}
function floor(g, M, GY, poolX, poolC, a = 0.22) {
  g.fillStyle = linGrad(g, 0, GY, 0, GY + 500, [shade(M.floor, 0.05), shade(M.dark, -0.2)]); g.fillRect(-E.W * 1.5, GY, E.W * 4, E.H * 2);
  FX.floorLines(g, GY, GY + 600, 'rgba(0,0,0,.22)', 0.07);
  if (poolX != null) FX.pool(g, poolX, GY + 30, 460, 70, poolC || M.key, a);
}
function picture(g, x, y, w, h, M, inner) {
  rr(g, x - 6, y - 6, w + 12, h + 12, 4); g.fillStyle = shade(M.wall, -0.6); g.fill();
  g.fillStyle = inner || shade(M.practical, -0.5); g.fillRect(x, y, w, h);
  circle(g, x + w * 0.4, y + h * 0.45, h * 0.18, shade(M.wall, -0.5)); circle(g, x + w * 0.62, y + h * 0.5, h * 0.15, shade(M.wall, -0.5));
}
function lamp(g, x, GY, M, h = 300) {
  seg(g, [[x, GY], [x, GY - h]], 6, shade(M.wall, -0.7));
  poly(g, [[x - 50, GY - h], [x + 50, GY - h], [x + 34, GY - h - 70], [x - 34, GY - h - 70]], shade(M.practical, -0.15));
  glow(g, x, GY - h - 20, 260, M.practical, 0.45);
}
function couch(g, x, GY, w, c) {
  rr(g, x, GY - 150, w, 70, 26); g.fillStyle = shade(c, -0.15); g.fill();
  rr(g, x - 20, GY - 100, w + 40, 80, 20); g.fillStyle = c; g.fill();
  rr(g, x - 34, GY - 130, 50, 120, 20); g.fill(); rr(g, x + w - 16, GY - 130, 50, 120, 20); g.fill();
  seg(g, [[x, GY - 20], [x, GY]], 8, shade(c, -0.6)); seg(g, [[x + w, GY - 20], [x + w, GY]], 8, shade(c, -0.6));
}
export function table(g, x, GY, w = 260, c = '#1e1418', h = 150) {
  const top = GY - h; seg(g, [[x - w / 2 + 20, top], [x - w / 2 + 26, GY]], 9, c); seg(g, [[x + w / 2 - 20, top], [x + w / 2 - 26, GY]], 9, c);
  rr(g, x - w / 2, top - 12, w, 16, 7); g.fillStyle = c; g.fill(); g.fillStyle = 'rgba(255,210,150,.25)'; g.fillRect(x - w / 2 + 6, top - 12, w - 12, 3);
  return top - 12;
}
export function cup(g, x, y, s = 1, col = '#f2ece4', tea = '#8a4a20', leaf = false) {
  g.save(); g.translate(x, y); g.scale(s, s);
  rr(g, -16, -30, 32, 30, 6); g.fillStyle = col; g.fill(); seg(g, [[16, -24], [24, -18], [16, -10]], 4, col);
  g.fillStyle = tea; g.fillRect(-14, -30, 28, 5); if (leaf) { g.fillStyle = '#4fa35a'; g.beginPath(); g.ellipse(4, -33, 8, 4, -0.5, 0, 7); g.fill(); }
  g.fillStyle = 'rgba(0,0,0,.18)'; g.fillRect(4, -26, 12, 26); g.restore();
}
function skyWin(g, M, x, y, w, h, t, o = {}) {
  g.fillStyle = linGrad(g, 0, y, 0, y + h, M.sky); g.fillRect(x, y, w, h);
  if (o.moon) { FX.stars(g, t, { area: [x, y, w, h * 0.7], count: 30 }); FX.moon(g, x + w * 0.7, y + h * 0.3, 34); }
  else FX.sun(g, x + w * (o.sunX ?? 0.6), y + h * (o.sunY ?? 0.72), 50, '#fff3dc', M.key, 4);
  FX.skyline(g, { x, y: y + h, w, maxH: h * 0.55, color: alpha(shade(M.wall, -0.55), 0.92), windowColor: alpha(M.practical, 0.8), lit: o.moon ? 0.35 : 0.15, seed: o.seed || 4 });
}

// ---------- HOME: living room + kitchen corner, warm evening window ----------
export function home(g, t, cam, o = {}) {
  const M = mood(o.mood || 'interiorWarm'), GY = ground(), CX = E.W / 2;
  layer(g, cam, 0.45, (g) => {
    wallAndFloor(g, M, GY);
    const wx = CX - 360, wy = GY - 620, ww = 720, wh = 380;
    FX.windowFrame(g, { x: wx, y: wy, w: ww, h: wh, cols: 3, frame: shade(M.wall, -0.6), bar: 12 }, (g, x, y, w, h) => skyWin(g, mood(o.sky || 'dusk'), x, y, w, h, t, { moon: o.night, seed: 9 }));
    glow(g, CX, wy + wh / 2, 700, mood(o.sky || 'dusk').key, o.night ? 0.08 : 0.16);
    picture(g, CX - 820, GY - 560, 150, 110, M); picture(g, CX - 630, GY - 600, 110, 150, M);
    FX.clock(g, CX + 640, GY - 600, 40, 17 * 3600 + 42 * 60 + t, { face: '#efe6da' });
    // kitchen corner on the right
    FX.counter(g, { x: CX + 760, y: GY - 10, w: 900, h: 140, color: shade(M.wall, -0.5), top: shade(M.wall, -0.2), doors: 6 });
    rr(g, CX + 800, GY - 520, 380, 150, 10); g.fillStyle = shade(M.wall, -0.45); g.fill();
    seg(g, [[CX + 1000, GY - 150], [CX + 1000, GY - 210], [CX + 1050, GY - 230]], 6, '#9a9aa8');
    glow(g, CX + 980, GY - 300, 200, M.practical, 0.25);
  });
  layer(g, cam, 0.8, (g) => {
    couch(g, CX - 900, GY, 420, shade('#6a3a4a', -0.2));
    lamp(g, CX - 1060, GY, M, 320);
    floor(g, M, GY, CX, mood(o.sky || 'dusk').key, 0.2);
  });
  return { GY, CX, M };
}

// ---------- CLASSROOM: blinds window, chalkboard, desks ----------
export function classroom(g, t, cam, o = {}) {
  const M = mood('interiorCool'), GY = ground(), CX = E.W / 2;
  layer(g, cam, 0.45, (g) => {
    wallAndFloor(g, M, GY, { wallK: -0.1 });
    rr(g, CX - 520, GY - 640, 1040, 360, 10); g.fillStyle = '#1f3a32'; g.fill(); g.strokeStyle = shade(M.wall, -0.6); g.lineWidth = 14; g.stroke();
    g.strokeStyle = 'rgba(230,240,230,.55)'; g.lineWidth = 4; g.beginPath(); g.moveTo(CX - 420, GY - 520); for (let i = 0; i < 12; i++) g.lineTo(CX - 420 + i * 40, GY - 520 + Math.sin(i) * 20); g.stroke();
    ring(g, CX + 220, GY - 480, 60, 4, 'rgba(230,240,230,.5)'); seg(g, [[CX + 120, GY - 380], [CX + 380, GY - 380]], 4, 'rgba(230,240,230,.5)');
    const wx = CX + 700, wy = GY - 640, ww = 520, wh = 380;
    FX.windowFrame(g, { x: wx, y: wy, w: ww, h: wh, cols: 2, frame: shade(M.wall, -0.6), bar: 12, blinds: 7 }, (g, x, y, w, h) => skyWin(g, mood('day'), x, y, w, h, t, { sunX: 0.3, sunY: 0.4, seed: 12 }));
    FX.godRays(g, wx + 100, wy + 100, { count: 8, angle: 2.4, spread: 0.6, len: 1400, a: 0.05, t });
    FX.clock(g, CX - 760, GY - 620, 36, 10 * 3600 + 5 * 60 + t, { face: '#e9eef2' });
  });
  layer(g, cam, 0.8, (g) => {
    for (const dx of [-760, -380, 380, 760]) { rr(g, CX + dx - 110, GY - 120, 220, 16, 6); g.fillStyle = shade(M.wall, -0.55); g.fill(); seg(g, [[CX + dx - 90, GY - 110], [CX + dx - 90, GY]], 7, shade(M.wall, -0.7)); seg(g, [[CX + dx + 90, GY - 110], [CX + dx + 90, GY]], 7, shade(M.wall, -0.7)); }
    floor(g, M, GY, CX + 400, mood('day').key, 0.16);
  });
  return { GY, CX, M };
}

// ---------- BAKERY: golden street shopfront ----------
export function bakery(g, t, cam, o = {}) {
  const M = mood('golden'), GY = ground(), CX = E.W / 2;
  layer(g, cam, 0.15, (g) => { backdrop(g, M.sky); FX.sun(g, CX - 600, GY - 640, 60, '#fff3dc', M.key, 5);
    FX.skyline(g, { x: -E.W, y: GY - 480, w: E.W * 3, minH: 80, maxH: 300, color: mix(M.sky[1], '#2a1814', 0.75), windowColor: alpha(M.practical, 0.5), lit: 0.15, seed: 31 }); });
  layer(g, cam, 0.55, (g) => {
    const wall = shade(M.wall, -0.3), top = GY - 600;
    g.fillStyle = linGrad(g, 0, top, 0, GY, [shade(wall, 0.05), wall, shade(wall, -0.4)]); g.fillRect(CX - 1600, top, 3200, GY - top);
    const sx = CX - 520, sy = GY - 420, sw = 1040, sh = 300;
    rr(g, sx, sy, sw, sh, 8); g.fillStyle = linGrad(g, 0, sy, 0, sy + sh, [M.practical, shade(M.practical, -0.4)]); g.fill();
    for (let i = 0; i < 3; i++) { g.fillStyle = shade(wall, -0.5); g.fillRect(sx, sy + 90 + i * 80, sw, 10);
      for (let k = 0; k < 9; k++) { g.fillStyle = k % 2 ? '#c8873e' : '#e0a55a'; g.beginPath(); g.ellipse(sx + 70 + k * 110, sy + 76 + i * 80, 40, 18, 0, 0, 7); g.fill(); } }
    glow(g, CX, sy + sh / 2, 700, M.practical, 0.25);
    for (let x = CX - 1600, k = 0; x < CX + 1600; x += 60, k++) { g.fillStyle = k % 2 ? '#e8dcc8' : '#2f6b4a'; g.fillRect(x, sy - 110, 60, 60); g.beginPath(); g.arc(x + 30, sy - 50, 30, 0, Math.PI); g.fill(); }
    rr(g, CX - 140, sy - 200, 280, 70, 12); g.fillStyle = shade(wall, -0.5); g.fill();
    text(g, 'مخبز', CX, sy - 166, { size: 46, color: M.practical, font: FONTS.title, weight: 900, glow: 16, glowColor: alpha(M.practical, 0.7) });
  });
  layer(g, cam, 0.85, (g) => { floor(g, M, GY, CX, M.practical, 0.25); FX.lampPost(g, CX + 820, GY, 380, { light: M.practical }); FX.tree(g, CX - 1000, GY, 1.3, '#2a1a1a'); });
  return { GY, CX, M };
}

// ---------- CLINIC: cool room, scan lightbox, monitor, night window ----------
export function clinic(g, t, cam, o = {}) {
  const M = mood('interiorCool'), GY = ground(), CX = E.W / 2;
  layer(g, cam, 0.45, (g) => {
    wallAndFloor(g, M, GY, { wallK: -0.15 });
    const wx = CX - 900, wy = GY - 640, ww = 480, wh = 360;
    FX.windowFrame(g, { x: wx, y: wy, w: ww, h: wh, cols: 2, frame: shade(M.wall, -0.6), bar: 10, blinds: 5 }, (g, x, y, w, h) => skyWin(g, mood('night'), x, y, w, h, t, { moon: true, seed: 17 }));
    // lightbox with brain scans
    const bx = CX - 140, by = GY - 640, bw = 560, bh = 300; rr(g, bx - 10, by - 10, bw + 20, bh + 20, 10); g.fillStyle = '#0d1020'; g.fill();
    g.fillStyle = '#cfe8ff'; g.fillRect(bx, by, bw, bh); glow(g, bx + bw / 2, by + bh / 2, 600, '#9fe0ff', 0.35);
    for (let i = 0; i < 3; i++) { const cx = bx + 95 + i * 185, cy = by + bh / 2; g.fillStyle = '#20304a'; g.beginPath(); g.ellipse(cx, cy, 80, 100, 0, 0, 7); g.fill();
      g.strokeStyle = '#7fa8d8'; g.lineWidth = 3; for (let k = 0; k < 4; k++) { g.beginPath(); g.ellipse(cx, cy, 64 - k * 14, 84 - k * 18, 0, 0, 7); g.stroke(); }
      glow(g, cx + 14, cy - 20, 50, '#ffd47e', 0.5 + 0.3 * Math.sin(t * 2 + i)); }
  });
  layer(g, cam, 0.8, (g) => {
    rr(g, CX + 520, GY - 170, 520, 20, 6); g.fillStyle = shade(M.wall, -0.5); g.fill(); seg(g, [[CX + 560, GY - 160], [CX + 560, GY]], 8, shade(M.wall, -0.7)); seg(g, [[CX + 1000, GY - 160], [CX + 1000, GY]], 8, shade(M.wall, -0.7));
    FX.screen(g, { x: CX + 600, y: GY - 360, w: 260, h: 170, glowC: '#7fd0d6', a: 0.25 }, (g, x, y, w, h) => { g.strokeStyle = '#7fd0d6'; g.lineWidth = 3; g.beginPath(); for (let i = 0; i < 40; i++) g.lineTo(x + 6 + i * 6.3, y + h / 2 - (i % 8 === 0 ? 40 : Math.sin(i * 1.3 + t * 4) * 8)); g.stroke(); });
    floor(g, M, GY, CX + 140, '#9fe0ff', 0.2);
  });
  return { GY, CX, M };
}

// ---------- BEDROOM: moonlit, bed, desk ----------
export function bedroom(g, t, cam, o = {}) {
  const M = mood('night'), GY = ground(), CX = E.W / 2;
  layer(g, cam, 0.45, (g) => {
    wallAndFloor(g, M, GY, { wallK: -0.2 });
    const wx = CX - 260, wy = GY - 640, ww = 520, wh = 400;
    FX.windowFrame(g, { x: wx, y: wy, w: ww, h: wh, cols: 2, rows: 2, frame: shade(M.wall, -0.6), bar: 12 }, (g, x, y, w, h) => skyWin(g, M, x, y, w, h, t, { moon: true, seed: 23 }));
    FX.godRays(g, CX + 120, wy + 120, { count: 7, angle: 1.9, spread: 0.5, len: 1300, a: 0.05, t });
    picture(g, CX + 560, GY - 560, 130, 100, M, shade('#3a6ea5', -0.4));
    FX.clock(g, CX - 640, GY - 600, 34, 3 * 3600 + t, { face: '#cfd6ee' });
  });
  layer(g, cam, 0.8, (g) => {
    FX.bed(g, { x: CX - 900, y: GY, w: 560, color: '#3a3f78', frame: shade(M.wall, -0.6) });
    rr(g, CX + 520, GY - 160, 380, 18, 6); g.fillStyle = shade(M.wall, -0.55); g.fill(); seg(g, [[CX + 550, GY - 150], [CX + 550, GY]], 7, shade(M.wall, -0.7)); seg(g, [[CX + 870, GY - 150], [CX + 870, GY]], 7, shade(M.wall, -0.7));
    floor(g, M, GY, CX, M.key, 0.18);
  });
  return { GY, CX, M };
}

// ---------- TV STUDIO: spotlights, LED wall of dates, audience ----------
export function studio(g, t, cam, o = {}) {
  const M = mood('night'), GY = ground(), CX = E.W / 2;
  layer(g, cam, 0.3, (g) => {
    backdrop(g, ['#05060f', '#0f1230', '#1a1238']);
    const lx = CX - 700, ly = GY - 700, lw = 1400, lh = 440; rr(g, lx - 10, ly - 10, lw + 20, lh + 20, 12); g.fillStyle = '#050510'; g.fill();
    g.fillStyle = linGrad(g, 0, ly, 0, ly + lh, ['#1c2a6a', '#3a1f6a']); g.fillRect(lx, ly, lw, lh);
    for (let i = 0; i < 7; i++) for (let j = 0; j < 4; j++) { const on = ((i * 3 + j * 5 + Math.floor(t * 3)) % 7) < 3; rr(g, lx + 30 + i * 196, ly + 26 + j * 104, 170, 80, 8); g.fillStyle = on ? 'rgba(255,212,126,.85)' : 'rgba(150,170,255,.18)'; g.fill(); }
    glow(g, CX, ly + lh / 2, 900, '#6a5aff', 0.2);
    for (const sx of [-1, 1]) FX.lightCone(g, CX + sx * 760, -40, { angle: Math.PI / 2 - sx * 0.35, spread: 0.18, len: 1300, color: '#cfd6ff', a: 0.16 });
  });
  layer(g, cam, 0.8, (g) => {
    g.fillStyle = linGrad(g, 0, GY, 0, GY + 400, ['#1a1830', '#06060c']); g.fillRect(-E.W, GY, E.W * 3, E.H * 2);
    FX.pool(g, CX, GY + 20, 420, 70, '#cfd6ff', 0.35);
    rr(g, CX - 420, GY - 120, 260, 20, 8); g.fillStyle = '#2a2650'; g.fill(); seg(g, [[CX - 290, GY - 110], [CX - 290, GY]], 10, '#1a1838');
  });
  return { GY, CX, M };
}
export function audience(g, t, cheer = 0) { FX.crowd(g, t, { y: E.H * 0.86, rows: 4, rowH: 40, size: 2.4, color: '#0c0b18', cheer, seed: 41 }); }

// ---------- CITY: dusk street with market, station, lamp posts ----------
export function city(g, t, cam, o = {}) {
  const M = mood(o.mood || 'dusk'), GY = ground(), CX = E.W / 2;
  layer(g, cam, 0.12, (g) => { backdrop(g, M.sky); FX.sun(g, CX + 500, GY - 300, 70, '#fff1d8', M.key, 6); FX.clouds(g, { y: GY - 860, h: 180, color: '#ffd9c0', a: 0.14, seed: 5 }); });
  layer(g, cam, 0.3, (g) => FX.skyline(g, { x: -E.W, y: GY - 260, w: E.W * 3, minH: 120, maxH: 420, color: mix(M.sky[1], M.dark, 0.7), windowColor: alpha(M.practical, 0.7), lit: 0.25, seed: o.seed || 51 }));
  layer(g, cam, 0.55, (g) => {
    for (let i = -4; i <= 4; i++) FX.facade(g, { x: CX + i * 380 - 180, y: GY, w: 360, h: 380 + ((i * 7 + 20) % 5) * 50, color: shade(M.wall, -0.35 - (i % 2) * 0.1), win: M.practical, dark: shade(M.wall, -0.6), cols: 3, rows: 3, lit: 0.45, seed: 60 + i });
    if (o.station) { rr(g, CX - 260, GY - 520, 520, 90, 10); g.fillStyle = '#1a2440'; g.fill(); text(g, 'محطة القطار', CX, GY - 476, { size: 50, color: '#cfe0ff', weight: 900, glow: 14, glowColor: 'rgba(160,190,255,.7)' }); }
    if (o.market) for (let k = -2; k <= 2; k++) { const x = CX + k * 330; poly(g, [[x - 150, GY - 230], [x + 150, GY - 230], [x + 120, GY - 290], [x - 120, GY - 290]], k % 2 ? '#c0503a' : '#e0b04a'); seg(g, [[x - 140, GY - 230], [x - 140, GY]], 6, M.dark); seg(g, [[x + 140, GY - 230], [x + 140, GY]], 6, M.dark); rr(g, x - 150, GY - 110, 300, 26, 6); g.fillStyle = shade(M.wall, -0.5); g.fill(); for (let q = 0; q < 6; q++) circle(g, x - 110 + q * 44, GY - 124, 16, ['#e0603a', '#7ab04a', '#f0c040'][q % 3]); }
  });
  layer(g, cam, 0.85, (g) => {
    g.fillStyle = linGrad(g, 0, GY, 0, GY + 400, [shade(M.road || M.floor, -0.1), shade(M.dark, -0.3)]); g.fillRect(-E.W, GY, E.W * 3, E.H * 2);
    for (let x = -E.W; x < E.W * 2; x += 220) { g.fillStyle = 'rgba(255,230,180,.25)'; g.fillRect(x, GY + 120, 110, 8); }
    for (const lx of [-700, 0, 700]) FX.lampPost(g, CX + lx, GY, 400, { light: M.practical });
    FX.tree(g, CX - 1150, GY, 1.4, shade(M.dark, -0.2)); FX.tree(g, CX + 1150, GY, 1.2, shade(M.dark, -0.2));
  });
  return { GY, CX, M };
}

// ---------- SEA CAFÉ: café by the sea at sunset, big window, wooden chair ----------
export function seacafe(g, t, cam, o = {}) {
  const M = mood('dusk'), GY = ground(), CX = E.W / 2;
  layer(g, cam, 0.15, (g) => {
    backdrop(g, M.sky); const hy = GY - 300;
    FX.sun(g, CX + 120, hy - 20 - (o.sunset ?? 0) * 60, 80, '#fff1d8', M.key, 6);
    g.fillStyle = linGrad(g, 0, hy, 0, GY + 200, ['#d07a5a', '#5a3a5a', '#231a27']); g.fillRect(-E.W, hy, E.W * 3, E.H);
    for (let i = 0; i < 14; i++) { const y = hy + 12 + i * i * 2.4, w = 240 - i * 10 + Math.sin(t * 0.8 + i) * 30; g.fillStyle = `rgba(255,220,170,${0.5 - i * 0.03})`; g.fillRect(CX + 120 - w / 2 + Math.sin(t + i * 2) * 20, y, w, 4); }
  });
  if (o.outside) { layer(g, cam, 0.85, (g) => { g.fillStyle = shade(M.floor, -0.3); g.fillRect(-E.W, GY, E.W * 3, E.H); }); return { GY, CX, M }; }
  layer(g, cam, 0.5, (g) => {
    const wall = shade(M.wall, -0.4);
    g.fillStyle = wall; g.fillRect(-E.W, -E.H, E.W * 3, GY - 700 + E.H); g.fillRect(-E.W, GY - 120, E.W * 3, 140);
    g.fillRect(-E.W, -E.H, E.W - 500 + E.W, E.H * 3); g.fillRect(CX + 860, -E.H, E.W * 2, E.H * 3);
    for (const mx of [-420, 0, 420]) g.fillRect(CX + mx - 10, GY - 700, 20, 590);
    g.fillRect(-E.W, GY - 420, E.W * 3, 14);
    // string lights
    for (let i = 0; i < 22; i++) { const x = CX - 900 + i * 85, y = GY - 740 + Math.sin(i * 0.6) * 18; circle(g, x, y, 7, '#ffe2a0'); glow(g, x, y, 40, '#ffd59a', 0.5); }
  });
  layer(g, cam, 0.85, (g) => {
    g.fillStyle = linGrad(g, 0, GY, 0, GY + 400, ['#3a2a2c', '#140e12']); g.fillRect(-E.W, GY, E.W * 3, E.H * 2);
    FX.floorLines(g, GY, GY + 500, 'rgba(0,0,0,.3)', 0.07); FX.pool(g, CX + 120, GY + 30, 520, 80, M.key, 0.25);
  });
  return { GY, CX, M };
}

// ---------- ARCHIVE: the memory void, floating glowing memory cards ----------
export function archive(g, t, cam, o = {}) {
  const M = mood('void'), GY = ground(), CX = E.W / 2, ui = { gold: '#ffd47e' };
  layer(g, cam, 0.2, (g) => { backdrop(g, ['#05070f', '#0d1430', '#1a1240']); FX.stars(g, t, { count: 80 }); });
  const n = o.count || 36, speed = o.speed ?? 1;
  for (let k = 0; k < n; k++) {
    const depth = 0.3 + (k % 6) * 0.12, a0 = k * 2.399, r = 300 + (k * 97) % 700;
    layer(g, cam, depth, (g) => {
      const x = CX + Math.cos(a0 + t * 0.05 * speed * (k % 2 ? 1 : -1)) * r * 1.4, y = E.H * 0.45 + Math.sin(a0 * 1.3 + t * 0.07 * speed) * r * 0.45;
      const w = 150 + (k % 4) * 30, h = w * 0.66, lit = o.focus === k ? 1 : 0.35 + 0.25 * Math.sin(t * 1.5 + k);
      g.save(); g.translate(x, y); g.rotate(Math.sin(k) * 0.15);
      rr(g, -w / 2, -h / 2, w, h, 8); g.fillStyle = alpha(['#ffd47e', '#ff9a6a', '#8fb8e8', '#f29ac0'][k % 4], 0.12 + 0.2 * lit); g.fill();
      g.strokeStyle = alpha('#fff1dc', 0.2 + 0.5 * lit); g.lineWidth = 2; g.stroke();
      circle(g, -w * 0.15, h * 0.05, h * 0.16, alpha('#0b0b16', 0.8)); seg(g, [[-w * 0.15, h * 0.2], [-w * 0.15, h * 0.38]], 6, alpha('#0b0b16', 0.8));
      g.restore(); glow(g, x, y, w, '#ffd47e', 0.06 * lit);
    });
  }
  return { GY, CX, M };
}

// ---------- PITCH: football stadium — stands with crowd, floodlights, striped grass, a goal ----------
export function pitch(g, t, cam, o = {}) {
  const M = mood(o.mood || 'dusk'), GY = ground(), CX = E.W / 2, night = o.night;
  layer(g, cam, 0.12, (g) => { backdrop(g, night ? ['#05070f', '#0d1430', '#1a1c3a'] : M.sky); if (!night) FX.clouds(g, { y: GY - 900, h: 160, color: '#ffd9c0', a: 0.12, seed: 9 }); });
  layer(g, cam, 0.3, (g) => {
    g.fillStyle = shade(M.dark, -0.3); poly(g, [[-E.W, GY - 120], [-E.W, GY - 520], [E.W * 2, GY - 520], [E.W * 2, GY - 120]], shade(M.dark, -0.35));
    for (let r = 0; r < 6; r++) { g.fillStyle = alpha(r % 2 ? '#3a2a4a' : '#2a2038', 1); g.fillRect(-E.W, GY - 500 + r * 64, E.W * 3, 60); }
    FX.crowd(g, t, { y: GY - 150, rows: 6, rowH: 60, size: 1.6, color: '#140f1e', cheer: o.cheer ?? 0.2, seed: 77 });
    for (const lx of [-650, 650]) { const x = CX + lx; seg(g, [[x, GY - 480], [x, GY - 980]], 14, '#1a1626'); rr(g, x - 110, GY - 1060, 220, 90, 10); g.fillStyle = '#2a2638'; g.fill(); for (let k = 0; k < 4; k++) circle(g, x - 75 + k * 50, GY - 1015, 18, '#fff8e0'); glow(g, x, GY - 1015, 420, '#fff3d0', night ? 0.55 : 0.3); }
  });
  layer(g, cam, 0.85, (g) => {
    for (let i = -12; i < 24; i++) { g.fillStyle = i % 2 ? '#2f7a3a' : '#2a6e34'; g.fillRect(CX + i * 160 - E.W, GY - 120, 160, E.H * 2); }
    g.fillStyle = 'rgba(0,0,0,.18)'; g.fillRect(-E.W, GY - 120, E.W * 3, 40);
    seg(g, [[-E.W, GY - 40], [E.W * 3, GY - 40]], 5, 'rgba(255,255,255,.55)');
    if (o.goal !== false) { const gx = CX + (o.goalX ?? 620); g.strokeStyle = '#f2f2f2'; g.lineWidth = 12; g.beginPath(); g.moveTo(gx - 220, GY - 40); g.lineTo(gx - 220, GY - 330); g.lineTo(gx + 220, GY - 330); g.lineTo(gx + 220, GY - 40); g.stroke(); g.strokeStyle = 'rgba(255,255,255,.25)'; g.lineWidth = 2; for (let k = -200; k <= 200; k += 34) seg(g, [[gx + k, GY - 330], [gx + k * 0.8, GY - 60]], 2, 'rgba(255,255,255,.25)'); for (let y = GY - 300; y < GY - 40; y += 34) seg(g, [[gx - 210, y], [gx + 210, y]], 2, 'rgba(255,255,255,.2)'); }
    FX.pool(g, CX, GY + 30, 700, 90, '#fff3d0', night ? 0.25 : 0.12);
  });
  return { GY, CX, M };
}
