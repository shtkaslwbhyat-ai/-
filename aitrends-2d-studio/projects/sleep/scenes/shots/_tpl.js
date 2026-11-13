// shots/_tpl.js — parametric shot templates. Every shot in shots.json names a template in params.tpl.
import { E, V, S, mood, layer, blurLayer, veil, backdrop, ease, prog, key, clamp, lerp, shake, talkAmount, wordTime,
  seg, circle, ring, rr, poly, glow, alpha, shade, mix, linGrad, radGrad, text, measure, FONTS } from '/engine/core.js';
import { drawFigure, POSES, posesAt, breathe, walkPose, bigFace } from '/engine/rig2d.js';
import * as FX from '/engine/fx2d.js';
import * as UI from '/engine/ui2d.js';
import * as P from '../sets/places.js';
import { CAST } from '../cast.js';

const SETS = { home: P.home, classroom: P.classroom, bakery: P.bakery, clinic: P.clinic, bedroom: P.bedroom, studio: P.studio, city: P.city, seacafe: P.seacafe, archive: P.archive, pitch: P.pitch };
const GOLD = () => S().ui.gold, CREAM = () => S().ui.cream, CORAL = () => S().ui.accent;
const lit = (setName) => ({ home: [0, -1], classroom: [1, -0.4], bakery: [-0.6, -0.6], clinic: [-0.3, -1], bedroom: [0, -1], studio: [0, -1], city: [0.6, -0.6], seacafe: [0.2, -1], archive: [0, -1], pitch: [0.5, -1] }[setName] || [0, -1]);
const seqVal = (t, v, def) => (Array.isArray(v) && Array.isArray(v[0]) ? (v.filter(([at]) => t >= at).pop() || v[0])[1] : (v ?? def));
const poseSeq = (t, v) => (Array.isArray(v) ? posesAt(t, v.map(([a, p]) => [a, typeof p === 'string' ? POSES[p] || POSES.stand : p])) : POSES[v || 'stand'] || POSES.stand);

export function camOf(t, info) {
  const c = info.cam || {}, d = info.dur, k = ease.inOut(clamp(t / d));
  const z = lerp(c.z0 ?? 1, c.z1 ?? 1.07, k), x = lerp(c.x0 ?? 0, c.x1 ?? -40, k), y = lerp(c.y0 ?? 0, c.y1 ?? 0, k);
  const [sx, sy] = c.shake ? shake(t, c.shake, 1.5) : [0, 0];
  return { z, x: x + sx, y: y + sy, r: c.r ? c.r * Math.sin(t * 0.6) : 0 };
}
export function drawSet(g, t, info, cam) { const fn = SETS[info.set || 'home']; return fn(g, t, cam, info.so || {}); }
function atmos(g, t, info) {
  const s = info.set;
  if (s === 'bedroom' || s === 'clinic') FX.dust(g, t, { count: 30, color: '#cfd8ff', a: 0.25 });
  else if (s === 'studio') FX.dust(g, t, { count: 50, color: '#d8dcff', a: 0.35 });
  else if (s === 'archive') FX.dust(g, t, { count: 60, color: '#ffe2b0', a: 0.3 });
  else FX.dust(g, t, { count: 40, color: '#ffe2bd', a: 0.3 });
  if (info.rain) FX.rain(g, t, { a: 0.25 });
}
function figure(g, t, info, ch, GY, M, i) {
  const o = CAST[ch.c] || CAST.PLAIN; let x = E.W * (ch.x ?? 0.5), pose = poseSeq(t, ch.pose), facing = ch.f ?? 1;
  if (ch.walk) { const [a, b] = ch.walk, sp = ch.run ? 1.6 : 0.9, k = clamp(t / info.dur); x = E.W * lerp(a, b, k); pose = walkPose(t * Math.PI * 2 * sp, { run: ch.run }); facing = b > a ? 1 : -1; }
  else if (!ch.still) pose = breathe(pose, t, 1, i + 1);
  const s = ch.s ?? info.s ?? 1.5, y = (ch.y != null ? E.H * ch.y : GY);
  if (ch.chair) { g.save(); g.translate(x, 0); g.scale(facing, 1); FX.chair(g, -18 * s, y, s, '#1e161c'); g.restore(); }
  drawFigure(g, { x, y, s, facing, outfit: o, pose, expr: seqVal(t, ch.expr, 'neutral'), prop: ch.prop, look: ch.look,
    rim: { color: M.rim, dir: lit(info.set), w: 4 }, blink: (t % (2.7 + i * 0.4)) > (2.6 + i * 0.4), shadow: !ch.chair && ch.y == null,
    talk: ch.talk ? talkAmount(info.globalT, info.shot.start + (ch.talk[0] ?? 0), info.shot.start + (ch.talk[1] ?? 99)) : 0, trail: ch.trail, alpha: ch.alpha, rot: ch.rot });
  if (ch.talk) { const tk = talkAmount(info.globalT, info.shot.start + (ch.talk[0] ?? 0), info.shot.start + (ch.talk[1] ?? 99)); if (tk > 0) FX.rings(g, x + facing * 10 * s, y - 190 * s, t, { count: 2, r0: 40 * s, r1: 90 * s, color: '#fff3e0', a: 0.3 }); }
  return { x, y, s };
}

// ---------- props drawn on the stage (depth 1) ----------
const PROPS = {
  rock: (g, t, GY, p) => { const x = E.W * (p.x ?? 0.6); g.fillStyle = '#2a2026'; g.beginPath(); g.moveTo(x - 260, GY + 10); g.quadraticCurveTo(x - 240, GY - 170, x - 40, GY - 190); g.quadraticCurveTo(x + 200, GY - 200, x + 270, GY + 10); g.closePath(); g.fill(); g.fillStyle = 'rgba(255,190,140,.25)'; g.beginPath(); g.moveTo(x - 200, GY - 120); g.quadraticCurveTo(x - 60, GY - 185, x + 120, GY - 170); g.lineTo(x + 100, GY - 155); g.quadraticCurveTo(x - 60, GY - 165, x - 190, GY - 110); g.fill(); },
  sand: (g, t, GY, p) => { g.fillStyle = linGrad(g, 0, GY - 20, 0, GY + 300, ['#8a6a5a', '#3a2a2a']); g.fillRect(-E.W, GY - 20, E.W * 3, E.H); for (let i = 0; i < 40; i++) circle(g, (i * 157) % (E.W + 400) - 200, GY + 20 + (i * 53) % 200, 3, 'rgba(255,220,180,.25)'); },
  stairs: (g, t, GY, p) => { const x = E.W * (p.x ?? 0.5); for (let i = 0; i < 8; i++) { rr(g, x - 300 + i * 30, GY - i * 46, 600 - i * 60, 50, 6); g.fillStyle = i % 2 ? '#5a4a52' : '#4a3c44'; g.fill(); } },
  bridge: (g, t, GY, p) => { const x = E.W * (p.x ?? 0.5); g.strokeStyle = '#2a2026'; g.lineWidth = 26; g.beginPath(); g.moveTo(x - 700, GY - 40); g.quadraticCurveTo(x, GY - 220, x + 700, GY - 40); g.stroke(); g.lineWidth = 8; for (let i = -6; i <= 6; i++) { const xx = x + i * 100, yy = GY - 40 - (1 - (i / 7) ** 2) * 180; seg(g, [[xx, yy], [xx, yy - 80]], 8, '#2a2026'); } g.strokeStyle = '#2a2026'; g.beginPath(); g.moveTo(x - 700, GY - 120); g.quadraticCurveTo(x, GY - 300, x + 700, GY - 120); g.stroke(); },
  mirror: (g, t, GY, p) => { const x = E.W * (p.x ?? 0.6); rr(g, x - 130, GY - 520, 260, 360, 12); g.fillStyle = '#3a4a5a'; g.fill(); rr(g, x - 115, GY - 505, 230, 330, 8); g.fillStyle = linGrad(g, 0, GY - 505, 0, GY - 175, ['#9fb4cc', '#5a6f89']); g.fill(); for (let i = 0; i < (p.n ?? 3); i++) { g.fillStyle = '#f7e27a'; g.fillRect(x - 90 + (i % 2) * 90, GY - 470 + Math.floor(i / 2) * 100, 70, 60); } },
  notebookBed: (g, t, GY, p) => { const x = E.W * (p.x ?? 0.22); rr(g, x - 60, GY - 110, 120, 22, 4); g.fillStyle = '#2a5aa0'; g.fill(); },

  table: (g, t, GY, p) => { const top = P.table(g, E.W * (p.x ?? 0.5), GY, p.w || 300); if (p.cups) for (const [dx, leaf] of p.cups) P.cup(g, E.W * (p.x ?? 0.5) + dx, top, 1.3, '#f2ece4', '#8a4a20', leaf); if (p.phone) { rr(g, E.W * (p.x ?? 0.5) - 70, top - 10, 60, 10, 3); g.fillStyle = '#101018'; g.fill(); glow(g, E.W * (p.x ?? 0.5) - 40, top - 8, 40, '#9fd0ff', 0.3); } if (p.plate) { g.fillStyle = '#e8e2d8'; g.beginPath(); g.ellipse(E.W * (p.x ?? 0.5), top - 6, 70, 14, 0, 0, 7); g.fill(); g.fillStyle = '#3f7a3a'; g.beginPath(); g.ellipse(E.W * (p.x ?? 0.5) + 18, top - 12, 30, 9, 0, 0, 7); g.fill(); g.fillStyle = '#f2ead8'; g.beginPath(); g.ellipse(E.W * (p.x ?? 0.5) - 20, top - 12, 30, 9, 0, 0, 7); g.fill(); } },
  tv: (g, t, GY, p) => { const x = E.W * (p.x ?? 0.75), y = GY - 360; FX.screen(g, { x: x - 170, y, w: 340, h: 200, glowC: '#8fd08a', a: 0.3 }, (g, X, Y, w, h) => { g.fillStyle = '#2e7a3a'; g.fillRect(X, Y, w, h); seg(g, [[X + w / 2, Y], [X + w / 2, Y + h]], 2, 'rgba(255,255,255,.6)'); ring(g, X + w / 2, Y + h / 2, 30, 2, 'rgba(255,255,255,.6)'); circle(g, X + 60 + (t * 70) % (w - 120), Y + h / 2 + Math.sin(t * 3) * 40, 6, '#fff'); }); seg(g, [[x, y + 210], [x, GY - 120]], 8, '#15121a'); rr(g, x - 160, GY - 130, 320, 130, 8); g.fillStyle = '#1a1418'; g.fill(); },
  desk: (g, t, GY, p) => { const x = E.W * (p.x ?? 0.5); rr(g, x - 130, GY - 120, 260, 16, 6); g.fillStyle = '#2a2a3a'; g.fill(); seg(g, [[x - 110, GY - 110], [x - 110, GY]], 7, '#1a1a26'); seg(g, [[x + 110, GY - 110], [x + 110, GY]], 7, '#1a1a26'); if (p.book) { rr(g, x - 60, GY - 142, 120, 22, 4); g.fillStyle = '#e8e2d0'; g.fill(); } },
  taxi: (g, t, GY, p) => { const x = E.W * (p.x ?? 0.5) + (p.move ? -t * 160 : 0); rr(g, x - 230, GY - 150, 460, 100, 30); g.fillStyle = '#e8b830'; g.fill(); rr(g, x - 140, GY - 220, 280, 90, 30); g.fill(); g.fillStyle = '#1a2440'; rr(g, x - 120, GY - 205, 110, 60, 12); g.fill(); rr(g, x + 10, GY - 205, 110, 60, 12); g.fill(); circle(g, x - 140, GY - 50, 42, '#111'); circle(g, x + 140, GY - 50, 42, '#111'); glow(g, x + 230, GY - 110, 120, '#fff3c0', 0.5); },
  chairEmpty: (g, t, GY, p) => { const x = E.W * (p.x ?? 0.6); FX.chair(g, x, GY, 1.5, '#3a2618'); },
};

// ---------- 1. STAGE: wide / medium shot with characters ----------
export function stage(g, t, info) {
  const cam = camOf(t, info); const { GY, M } = drawSet(g, t, info, cam);
  layer(g, cam, 1, (g) => {
    for (const p of info.props || []) PROPS[p.k]?.(g, t, GY, p);
    (info.chars || []).forEach((ch, i) => figure(g, t, info, ch, GY, M, i));
    if (info.crowd) P.audience(g, t, info.crowd);
  });
  if (info.fg) blurLayer(g, 12, (g) => { const o = CAST[info.fg.c] || CAST.PLAIN; drawFigure(g, { x: E.W * (info.fg.x ?? 0.12), y: E.H * 1.25, s: 3.6, facing: info.fg.f ?? 1, outfit: o, pose: POSES.stand, expr: 'neutral', rim: { color: M.rim, dir: lit(info.set) } }); }, cam, 1.6);
  atmos(g, t, info); overlays(g, t, info);
}

// ---------- 2. FACE: giant face close-up ----------
export function face(g, t, info) {
  const bc = { z: 1.6, x: (info.bx ?? -150) + t * 8, y: -140 };
  blurLayer(g, 14, (g) => drawSet(g, t, info, bc)); veil(g, '#0c0810', 0.38);
  const M = mood(info.moodName || ({ bedroom: 'night', clinic: 'interiorCool', studio: 'night', city: 'dusk', seacafe: 'dusk', pitch: 'dusk', archive: 'void', classroom: 'interiorCool', bakery: 'golden' }[info.set] || 'interiorWarm'));
  const o = CAST[info.who || 'YOU'], r = (info.r ?? 300) * (1 + 0.04 * clamp(t / info.dur)), cx = E.W / 2 + (info.side ?? 0) * 260, cy = E.H * 0.6;
  const talk = info.talk ? talkAmount(info.globalT, info.shot.start + info.talk[0], info.shot.start + info.talk[1]) : 0;
  bigFace(g, cx, cy, r, { outfit: o, expr: seqVal(t, info.expr, 'neutral'), look: seqVal(t, info.look, [0, 0]), talk, rimColor: M.rim, rimSide: info.rimSide ?? -1, blink: (t % 3.2) > 3.08, tilt: info.tilt ?? 0 });
  if (talk > 0) FX.rings(g, cx, cy, t, { count: 3, r0: r * 1.1, r1: r * 1.6, color: '#fff3e0', a: 0.3 });
  if (info.tear) { const k = prog(t, info.tear, info.tear + 1.5); circle(g, cx + r * 0.32, cy - r * 0.05 + k * r * 0.5, r * 0.04, alpha('#bfe0ff', 0.9 * (1 - k * 0.5))); }
  if (info.memories) { for (let k = 0; k < 10; k++) { const a = k * 0.63 + t * 0.25, rr2 = r * 1.5 + (k % 3) * 60, x = cx + Math.cos(a) * rr2, y = cy + Math.sin(a) * rr2 * 0.55; g.save(); g.translate(x, y); rr(g, -60, -40, 120, 80, 8); g.fillStyle = alpha(['#ffd47e', '#ff9a6a', '#8fb8e8'][k % 3], 0.22); g.fill(); g.strokeStyle = alpha('#fff1dc', 0.4); g.lineWidth = 2; g.stroke(); g.restore(); } }
  FX.dust(g, t, { count: 25, a: 0.25 }); overlays(g, t, info);
}

// ---------- 3. INSERTS: object close-ups ----------
const ink = '#0e0b12';
function handArm(g, x, y, s, sleeve, from = 1) { seg(g, [[x, y], [x + from * 900, y + 500]], 70 * s, ink); seg(g, [[x + from * 120 * s, y + 70 * s], [x + from * 900, y + 520]], 96 * s, sleeve); circle(g, x, y, 42 * s, ink); }
const INSERTS = {
  cube: (g, t) => { const cx = E.W / 2, cy = E.H * 0.52, n = 3, sz = 110, colors = ['#e04a3a', '#3fb950', '#2f7fd6', '#f2c21a', '#ff8a3a', '#f2efe6']; g.fillStyle = '#1e1820'; g.fillRect(-E.W, cy + 230, E.W * 3, 600);
    const solved = t > 1.6, rot = solved ? 0 : Math.sin(t * 9) * 0.4; g.save(); g.translate(cx, cy); g.rotate(rot * 0.3);
    for (let i = 0; i < n; i++) for (let j = 0; j < n; j++) { rr(g, -sz * 1.5 + i * sz + 6, -sz * 1.5 + j * sz + 6, sz - 12, sz - 12, 14); g.fillStyle = solved ? colors[0] : colors[(i * 7 + j * 3 + Math.floor(t * 8)) % 6]; g.fill(); }
    g.restore(); rr(g, cx - sz * 1.5 - 14, cy - sz * 1.5 - 14, sz * 3 + 28, sz * 3 + 28, 22); g.strokeStyle = '#0c0a10'; g.lineWidth = 14; g.stroke();
    if (solved) { FX.rings(g, cx, cy, t - 1.6, { count: 2, r0: 200, r1: 500, color: '#fff3e0', a: 0.5 }); UI.readout(g, { label: 'الوقت', value: '3 ث', x: cx, y: E.H * 0.13, align: 'center' }); } },
  exam: (g, t, info = {}) => { const cx = E.W / 2, cy = E.H * 0.56; g.fillStyle = '#2a2230'; g.fillRect(-E.W, -E.H, E.W * 3, E.H * 3); g.save(); g.translate(cx, cy); g.rotate(-0.04); rr(g, -420, -380, 840, 760, 10); g.fillStyle = '#f4efe4'; g.fill();
    for (let i = 0; i < 11; i++) { g.fillStyle = 'rgba(40,40,70,.4)'; g.fillRect(-350, -300 + i * 52, 520 + (i * 41 % 120), 10); const k = prog(t, 0.2 + i * 0.12, 0.35 + i * 0.12); if (k > 0) seg(g, [[230, -305 + i * 52], [250, -290 + i * 52], [290, -325 + i * 52]], 8, alpha('#2fa04a', k)); }
    g.restore(); if (!info.noTimer) UI.readout(g, { label: 'الزمن', value: '7 دقائق من 120', x: E.W / 2, y: E.H * 0.1, align: 'center', a: ease.out(prog(t, 1.2, 1.6)) }); },
  chess: (g, t) => { const cx = E.W / 2, cy = E.H * 0.55; g.fillStyle = '#16121a'; g.fillRect(-E.W, -E.H, E.W * 3, E.H * 3); for (let b = 0; b < 5; b++) { const bx = cx - 760 + b * 380, by = cy - 40 + (b % 2) * 60, s = 36; for (let i = 0; i < 8; i++) for (let j = 0; j < 8; j++) { g.fillStyle = (i + j) % 2 ? '#3a2a22' : '#c8a878'; g.fillRect(bx - s * 4 + i * s, by - s * 4 + j * s, s, s); } circle(g, bx - s * 2 + ((b * 3 + Math.floor(t * 2)) % 6) * s, by, s * 0.35, '#0c0a10'); circle(g, bx + s * 1.5, by - s * 2, s * 0.35, '#f2efe6'); }
    text(g, '20 / 20', E.W / 2, E.H * 0.13, { size: 70, color: GOLD(), weight: 900, font: FONTS.ui, glow: 16, glowColor: alpha(GOLD(), 0.6), alpha: ease.out(prog(t, 0.8, 1.2)) }); },
  filter: (g, t) => { UI.blueprint(g); const c = UI.bpStroke(), cx = E.W / 2, top = E.H * 0.18, bot = E.H * 0.82; rr(g, cx - 160, top, 320, bot - top, 30); g.strokeStyle = c; g.lineWidth = 5; g.stroke();
    const layers = [['ماء ملوث', '#8a6a4a'], ['رمل', '#d8b878'], ['فحم', '#2a2a2a'], ['حصى', '#8a8a96'], ['ماء نظيف', '#5ab0e8']]; layers.forEach(([n, col], i) => { const y = top + 20 + i * (bot - top - 40) / 5, h = (bot - top - 40) / 5 - 8, a = ease.out(prog(t, 0.2 + i * 0.35, 0.5 + i * 0.35)); g.globalAlpha = a; rr(g, cx - 140, y, 280, h, 12); g.fillStyle = col; g.fill(); g.globalAlpha = 1; text(g, n, cx + 230, y + h / 2, { size: 40, color: CREAM(), weight: 900, align: 'left', alpha: a }); });
    for (let k = 0; k < 6; k++) { const yy = top + ((t * 160 + k * 90) % (bot - top)); circle(g, cx - 60 + k * 24, yy, 7, alpha('#9fd8ff', 0.8)); } },
  drawings: (g, t, info) => { const cx = E.W / 2; g.fillStyle = '#2a2026'; g.fillRect(-E.W, -E.H, E.W * 3, E.H * 3); const n = info.n || 1; for (let i = 0; i < n; i++) { const a = ease.outBack(prog(t, 0.1 + i * 0.08, 0.4 + i * 0.08)); if (a <= 0) continue; const x = cx + (n === 1 ? 0 : ((i % 6) - 2.5) * 260), y = E.H * (n === 1 ? 0.52 : 0.28 + Math.floor(i / 6) * 0.32); g.save(); g.translate(x, y); g.rotate(Math.sin(i * 3) * 0.08); g.scale(a * (n === 1 ? 2.2 : 1), a * (n === 1 ? 2.2 : 1));
    rr(g, -110, -80, 220, 160, 6); g.fillStyle = '#fbf8f0'; g.fill(); circle(g, 70, -45, 22, '#f2c21a'); for (let r = 0; r < 8; r++) seg(g, [[70 + Math.cos(r) * 28, -45 + Math.sin(r) * 28], [70 + Math.cos(r) * 38, -45 + Math.sin(r) * 38]], 3, '#f2c21a');
    drawFigure(g, { x: -40, y: 60, s: 0.38, outfit: { top: 'hoodie', color: '#2f7fd6', head: 'none' }, pose: POSES.stand, expr: 'smile' }); drawFigure(g, { x: 0, y: 60, s: 0.38, outfit: { top: 'dress', color: '#f29ac0', head: 'ponytail', headColor: '#f29ac0', kid: true }, pose: POSES.reach, expr: 'happy' });
    if (info.fish) { g.fillStyle = '#ff8a3a'; g.beginPath(); g.ellipse(-60, -40, 22, 12, 0, 0, 7); g.fill(); poly(g, [[-40, -40], [-26, -52], [-26, -28]], '#ff8a3a'); } g.restore(); } },
  fishbowl: (g, t, info) => { const cx = E.W / 2, cy = E.H * 0.55; g.fillStyle = '#2a2230'; g.fillRect(-E.W, -E.H, E.W * 3, E.H * 3); g.fillStyle = '#3a2a2a'; g.fillRect(-E.W, cy + 250, E.W * 3, 600); g.fillStyle = 'rgba(140,200,255,.25)'; g.beginPath(); g.arc(cx, cy, 260, 0, 7); g.fill(); g.strokeStyle = 'rgba(220,240,255,.6)'; g.lineWidth = 6; g.stroke();
    const dead = info.dead; g.save(); g.translate(cx + (dead ? 0 : Math.sin(t * 2) * 80), cy + (dead ? -170 : Math.sin(t * 3) * 30)); if (dead) g.rotate(Math.PI); g.fillStyle = '#ff8a3a'; g.beginPath(); g.ellipse(0, 0, 60, 34, 0, 0, 7); g.fill(); poly(g, [[55, 0], [95, -30], [95, 30]], '#ff8a3a'); circle(g, -30, -8, 7, '#111'); g.restore(); },
  iqcurve: (g, t) => { UI.blueprint(g); const c = UI.bpStroke(), x0 = 260, x1 = E.W - 260, base = E.H * 0.74, k = ease.inOut(prog(t, 0.2, 1.6)); g.strokeStyle = c; g.lineWidth = 6; g.beginPath(); for (let i = 0; i <= 200 * k; i++) { const u = i / 200, x = lerp(x0, x1, u), z = (u - 0.5) * 6, y = base - Math.exp(-z * z / 2) * E.H * 0.45; i ? g.lineTo(x, y) : g.moveTo(x, y); } g.stroke();
    seg(g, [[x0, base], [x1, base]], 3, alpha(c, 0.7)); [[0.5, '100'], [0.75, '130']].forEach(([u, s]) => { const x = lerp(x0, x1, u); seg(g, [[x, base], [x, base + 20]], 3, c); text(g, s, x, base + 55, { size: 40, color: CREAM(), weight: 900, font: FONTS.ui }); });
    const a2 = ease.out(prog(t, 1.4, 1.8)); g.globalAlpha = a2 * 0.5; g.fillStyle = GOLD(); g.fillRect(lerp(x0, x1, 0.75), base - 80, x1 - lerp(x0, x1, 0.75), 80); g.globalAlpha = 1; text(g, '2%', lerp(x0, x1, 0.86), base - 120, { size: 56, color: GOLD(), weight: 900, font: FONTS.ui, alpha: a2 }); },

  notes: (g, t, info) => { const cx = E.W / 2, cy = E.H * 0.5; g.fillStyle = '#2a2a36'; g.fillRect(-E.W, -E.H, E.W * 3, E.H * 3); rr(g, cx - 420, cy - 380, 840, 760, 30); g.fillStyle = '#5a6a80'; g.fill(); rr(g, cx - 390, cy - 350, 780, 700, 20); g.fillStyle = linGrad(g, 0, cy - 350, 0, cy + 350, ['#9fb4cc', '#6a7f99']); g.fill();
    glow(g, cx - 200, cy - 200, 400, '#ffffff', 0.15); const notes = info.notes || ['لا تخف', 'اقرأ هذا أولا']; notes.forEach((n, i) => { const a = ease.outBack(prog(t, 0.2 + i * 0.6, 0.6 + i * 0.6)); if (a <= 0) return; g.save(); g.translate(cx - 150 + (i % 2) * 300, cy - 170 + Math.floor(i / 2) * 260); g.rotate((i % 2 ? 0.06 : -0.05)); g.scale(a, a); g.fillStyle = 'rgba(0,0,0,.25)'; g.fillRect(-122, -102, 250, 210); g.fillStyle = '#f7e27a'; g.fillRect(-130, -110, 250, 210); text(g, n, -5, -5, { size: 46, color: '#2a2a3a', weight: 900 }); g.restore(); }); },
  notebook: (g, t, info) => { const cx = E.W / 2, cy = E.H * 0.58; g.fillStyle = '#1e1a24'; g.fillRect(-E.W, cy + 200, E.W * 3, 800); g.save(); g.translate(cx, cy); g.rotate(-0.05); rr(g, -560, -330, 1120, 660, 18); g.fillStyle = '#2a5aa0'; g.fill(); rr(g, -540, -310, 530, 620, 10); g.fillStyle = '#f2ecdf'; g.fill(); rr(g, 10, -310, 530, 620, 10); g.fill();
    for (let i = 0; i < 13; i++) { g.fillStyle = 'rgba(40,40,70,.35)'; g.fillRect(-500, -250 + i * 42, 380 + (i * 37 % 80), 9); g.fillRect(50, -250 + i * 42, 380 + (i * 53 % 80), 9); } text(g, info.head || 'لا تخف', -280, -275, { size: 40, color: '#2a3a6a', weight: 900 }); const n = Math.round(lerp(1, info.pages || 100, ease.out(prog(t, 0.3, 2)))); text(g, `اليوم ${n}`, 280, -275, { size: 40, color: '#a03a3a', weight: 900 }); g.restore(); },
  bread: (g, t, info) => { const cx = E.W / 2, top = E.H * 0.7; g.fillStyle = '#3a2a22'; g.fillRect(-E.W, top, E.W * 3, E.H); g.fillStyle = 'rgba(255,200,140,.2)'; g.fillRect(-E.W, top, E.W * 3, 6); for (let i = 0; i < 3; i++) { const a = ease.outBack(prog(t, 0.3 + i * 0.35, 0.7 + i * 0.35)); g.save(); g.translate(cx - 360 + i * 360, top - 60); g.scale(a, a); g.fillStyle = '#c8873e'; g.beginPath(); g.ellipse(0, 0, 150, 70, 0, 0, 7); g.fill(); g.strokeStyle = '#a0662a'; g.lineWidth = 8; for (const d of [-60, 0, 60]) { g.beginPath(); g.moveTo(d - 20, -40); g.lineTo(d + 20, 30); g.stroke(); } g.restore(); }
    if (!info?.noQ) text(g, '؟', cx, top - 300, { size: 160, color: GOLD(), weight: 900, alpha: ease.out(prog(t, 1.5, 1.9)) }); },
  piano: (g, t) => { const cx = E.W / 2, y = E.H * 0.55; g.fillStyle = '#141018'; g.fillRect(-E.W, -E.H, E.W * 3, E.H * 3); rr(g, cx - 820, y - 120, 1640, 420, 20); g.fillStyle = '#0c0a10'; g.fill(); for (let i = 0; i < 22; i++) { const x = cx - 790 + i * 72, on = Math.floor(t * 4 + i * 0.7) % 7 === i % 7; rr(g, x, y - 90, 66, 360, 6); g.fillStyle = on ? '#ffe9b0' : '#f2efe6'; g.fill(); if (on) glow(g, x + 33, y + 120, 120, '#ffd47e', 0.35); }
    for (let i = 0; i < 21; i++) if (![2, 6, 9, 13, 16, 20].includes(i % 21)) { rr(g, cx - 790 + i * 72 + 46, y - 90, 42, 220, 4); g.fillStyle = '#121016'; g.fill(); }
    for (const [hx, ph] of [[-250, 0], [250, 1.3]]) { const yy = y - 140 + Math.sin(t * 6 + ph) * 18; seg(g, [[cx + hx, yy], [cx + hx * 1.6, E.H + 200]], 80, '#0e0b12'); seg(g, [[cx + hx * 1.15, yy + 160], [cx + hx * 1.6, E.H + 200]], 104, '#1fa38a'); for (let k = 0; k < 4; k++) seg(g, [[cx + hx - 45 + k * 30, yy], [cx + hx - 50 + k * 32, yy + 60 + Math.abs(Math.sin(t * 8 + k + ph)) * 30]], 18, '#0e0b12'); }
    for (let i = 0; i < 5; i++) text(g, '♪', cx - 400 + i * 200, y - 300 - ((t * 60 + i * 50) % 160), { size: 70, color: alpha(GOLD(), 0.7), weight: 900, font: 'sans-serif' }); },
  star: (g, t, info) => { UI.blueprint(g); const c = UI.bpStroke(), cx = E.W * 0.5, cy = E.H * 0.5, R = 260, k = ease.inOut(prog(t, 0.3, 2.4)); const pts = []; for (let i = 0; i <= 10; i++) { const a = -Math.PI / 2 + i * Math.PI / 5, r = i % 2 ? R * 0.45 : R; pts.push([cx + Math.cos(a) * r, cy + Math.sin(a) * r]); }
    g.strokeStyle = alpha(c, 0.4); g.lineWidth = 34; g.lineJoin = 'round'; g.beginPath(); pts.forEach(([x, y], i) => i ? g.lineTo(x, y) : g.moveTo(x, y)); g.stroke();
    g.strokeStyle = GOLD(); g.lineWidth = 6; g.beginPath(); const n = k * 10; for (let i = 0; i <= n; i++) { const i0 = Math.floor(i), f = Math.min(1, n - i0); const [ax, ay] = pts[i0], [bx, by] = pts[Math.min(10, i0 + 1)]; const jit = Math.sin(i * 7 + t * 3) * (info.messy ? 14 : 2); i ? g.lineTo(lerp(ax, bx, f) + jit, lerp(ay, by, f) - jit) : g.moveTo(ax, ay); } g.stroke();
    text(g, info.timeLabel || '', E.W * 0.5, E.H * 0.13, { size: 60, color: GOLD(), weight: 900, font: FONTS.ui, alpha: ease.out(prog(t, 0.4, 0.8)) }); },
  selfvideo: (g, t) => { const cx = E.W / 2, cy = E.H * 0.55; handArm(g, cx + 160, cy + 280, 1.3, '#1fa38a'); rr(g, cx - 200, cy - 360, 400, 720, 44); g.fillStyle = '#101018'; g.fill(); rr(g, cx - 178, cy - 336, 356, 672, 30); g.fillStyle = '#2a2236'; g.fill();
    g.save(); g.beginPath(); rr(g, cx - 178, cy - 336, 356, 672, 30); g.clip(); bigFace(g, cx, cy + 40, 150, { outfit: CAST.KARIM, expr: 'smile', talk: Math.abs(Math.sin(t * 8)) * 0.8, rimColor: '#ffd47e', rimSide: -1 }); g.restore(); circle(g, cx - 140, cy - 300, 10, '#e04a3a'); text(g, 'REC', cx - 100, cy - 300, { size: 26, color: '#fff', weight: 900, font: FONTS.ui }); },

  plate: (g, t) => { const cx = E.W / 2, cy = E.H * 0.6; g.fillStyle = '#efe8dc'; g.beginPath(); g.ellipse(cx, cy, 520, 190, 0, 0, 7); g.fill(); g.fillStyle = '#d8cfbf'; g.beginPath(); g.ellipse(cx, cy, 420, 145, 0, 0, 7); g.fill();
    for (let i = 0; i < 160; i++) { const a = i * 2.4, r = 30 + (i * 37 % 190); g.fillStyle = '#fbf6ea'; g.beginPath(); g.ellipse(cx - 150 + Math.cos(a) * r * 0.9, cy + Math.sin(a) * r * 0.35, 9, 4, a, 0, 7); g.fill(); }
    g.fillStyle = '#2f6a2a'; g.beginPath(); g.ellipse(cx + 190, cy, 160, 70, 0, 0, 7); g.fill(); g.fillStyle = '#3f8a35'; g.beginPath(); g.ellipse(cx + 180, cy - 10, 120, 45, 0, 0, 7); g.fill();
    for (let k = 0; k < 3; k++) { const a = prog(t, 0.3 + k * 0.2, 1 + k * 0.2); seg(g, [[cx - 60 + k * 60, cy - 220 - a * 60], [cx - 50 + k * 60 + Math.sin(t * 2 + k) * 10, cy - 300 - a * 80]], 6, alpha('#ffffff', 0.25 * (1 - a))); } },
  keys: (g, t) => { const cx = E.W / 2; g.fillStyle = '#4a4a56'; rr(g, cx - 600, 80, 1200, 1100, 60); g.fill(); g.fillStyle = '#3a3a46'; rr(g, cx - 420, 480, 840, 500, 30); g.fill(); g.strokeStyle = '#2a2a34'; g.lineWidth = 6; g.setLineDash([16, 12]); g.strokeRect(cx - 400, 500, 800, 460); g.setLineDash([]);
    const up = ease.out(prog(t, 0.6, 1.6)) * 260; ring(g, cx, 560 - up, 50, 10, '#d8d8e0'); for (const [dx, c] of [[-60, '#e8c050'], [10, '#c8c8d0'], [70, '#e8c050']]) { g.save(); g.translate(cx + dx * 0.4, 600 - up); g.rotate(dx * 0.006); rr(g, -14, 0, 28, 160, 8); g.fillStyle = c; g.fill(); g.restore(); } glow(g, cx, 560 - up, 200, '#ffd47e', 0.25); },
  coin: (g, t) => { const cx = E.W * 0.55, cy = E.H * 0.55; handArm(g, cx + 120, cy + 60, 1.4, '#d64a33'); const k = ease.out(prog(t, 0.4, 1.2)); g.save(); g.translate(cx, cy - k * 30); g.scale(Math.cos(t * 4) * 0.3 + 0.7, 1); circle(g, 0, 0, 90, '#d8b048'); ring(g, 0, 0, 72, 6, '#b08a30'); g.restore(); text(g, '١', cx, cy - k * 30, { size: 80, color: '#7a5a20', weight: 900 }); glow(g, cx, cy, 260, '#ffd47e', 0.3 * k); },
  sock: (g, t) => { const cx = E.W / 2, cy = E.H * 0.55; g.fillStyle = '#120e18'; g.fillRect(-E.W, cy + 60, E.W * 3, 600); g.fillStyle = '#2a2238'; g.fillRect(-E.W, -E.H, E.W * 3, cy + 60 + E.H); for (let i = 0; i < 6; i++) rr(g, cx - 900 + i * 320, cy - 20, 200, 80, 20), g.fillStyle = '#1a1424', g.fill();
    const a = 1 - ease.inOut(prog(t, 0.8, 2.0)); g.save(); g.globalAlpha = a; g.fillStyle = '#3a6ad6'; rr(g, cx - 90, cy - 30, 220, 70, 30); g.fill(); rr(g, cx - 90, cy - 150, 70, 160, 30); g.fill(); g.restore(); g.setLineDash([12, 10]); g.strokeStyle = alpha('#9fc0ff', 0.6 * (1 - a)); g.lineWidth = 4; rr(g, cx - 90, cy - 150, 220, 190, 30); g.stroke(); g.setLineDash([]);
    FX.lightCone(g, cx, cy - 500, { angle: Math.PI / 2, spread: 0.25, len: 700, color: '#cfe0ff', a: 0.15 }); },
  book: (g, t) => { const cx = E.W / 2, cy = E.H * 0.58; g.save(); g.translate(cx, cy); g.rotate(-0.06); g.fillStyle = '#efe7d6'; rr(g, -560, -300, 540, 600, 10); g.fill(); rr(g, 20, -300, 540, 600, 10); g.fill(); g.fillStyle = '#d9cfb8'; g.fillRect(-12, -300, 24, 600);
    for (let i = 0; i < 14; i++) { const w = 380 + (i * 53 % 100); g.fillStyle = 'rgba(40,30,30,.35)'; g.fillRect(-500, -240 + i * 36, w, 10); g.fillRect(80, -240 + i * 36, w, 10); }
    const k = ease.out(prog(t, 0.6, 1.4)); g.fillStyle = `rgba(150,90,40,${0.35 * k})`; g.beginPath(); g.ellipse(430, 190, 90, 70, 0.3, 0, 7); g.fill(); ring(g, 430, 190, 78, 6, `rgba(120,70,30,${0.4 * k})`);
    text(g, '٤٧', -40 - 260, 270, { size: 34, color: 'rgba(40,30,30,.6)', weight: 900 }); g.restore(); },
  phone: (g, t, info) => { const cx = E.W / 2, cy = E.H * 0.55; handArm(g, cx + 160, cy + 260, 1.3, '#3a6ea5'); rr(g, cx - 170, cy - 320, 340, 620, 40); g.fillStyle = '#101018'; g.fill(); rr(g, cx - 150, cy - 290, 300, 560, 26); g.fillStyle = '#1c2438'; g.fill();
    for (let i = 0; i < 6; i++) { rr(g, cx - 130 + (i % 2) * 140, cy - 260 + Math.floor(i / 2) * 150, 120, 130, 12); g.fillStyle = ['#506080', '#7a5a6a', '#3a6a5a'][i % 3]; g.fill(); }
    const k = ease.outBack(prog(t, 0.5, 0.9)); g.save(); g.translate(cx - 60, cy - 120); g.scale(k * 1.8, k * 1.8); rr(g, -60, -65, 120, 130, 12); g.fillStyle = '#5a6a7a'; g.fill(); drawFigure(g, { x: 0, y: 55, s: 0.38, outfit: { top: 'tshirt', color: '#3fb950', head: 'none' }, pose: POSES.cheer, expr: 'happy' }); g.restore();
    if (k > 0.9) ring(g, cx - 60, cy - 120, 140, 6, alpha(GOLD(), 0.8)); },
  tvscore: (g, t) => { FX.screen(g, { x: 260, y: 140, w: 1400, h: 760, glowC: '#8fd08a', a: 0.3 }, (g, X, Y, w, h) => { g.fillStyle = '#2e7a3a'; g.fillRect(X, Y, w, h); for (let i = 0; i < 8; i++) { g.fillStyle = i % 2 ? '#2a7036' : '#318040'; g.fillRect(X + i * w / 8, Y, w / 8, h); } seg(g, [[X + w / 2, Y], [X + w / 2, Y + h]], 4, 'rgba(255,255,255,.7)'); ring(g, X + w / 2, Y + h / 2, 110, 4, 'rgba(255,255,255,.7)');
    const pts = [[0.2, 0.7], [0.4, 0.3], [0.62, 0.55], [0.85, 0.45]], k = clamp(t / 2.8) * 3, i = Math.min(2, Math.floor(k)), f = k - i; g.setLineDash([14, 12]); for (let j = 0; j <= i; j++) seg(g, [[X + w * pts[j][0], Y + h * pts[j][1]], [X + w * lerp(pts[j][0], pts[j + 1][0], j < i ? 1 : f), Y + h * lerp(pts[j][1], pts[j + 1][1], j < i ? 1 : f)]], 5, alpha(GOLD(), 0.9)); g.setLineDash([]);
    for (const p of pts) circle(g, X + w * p[0], Y + h * p[1], 14, '#fff'); rr(g, X + 30, Y + 24, 260, 64, 10); g.fillStyle = 'rgba(0,0,0,.6)'; g.fill(); text(g, '3 - 1   85\'', X + 160, Y + 58, { size: 40, color: '#fff', weight: 900 }); }); },
  film: (g, t) => { FX.screen(g, { x: 260, y: 160, w: 1400, h: 720, glowC: '#ffb070', a: 0.25 }, (g, X, Y, w, h) => { g.fillStyle = linGrad(g, 0, Y, 0, Y + h, ['#e89a6a', '#5a3a5a']); g.fillRect(X, Y, w, h); FX.sun(g, X + w * 0.7, Y + h * 0.55, 80, '#fff1d8', '#ffc68a', 4);
    drawFigure(g, { x: X + w * 0.35, y: Y + h - 40, s: 1.6, facing: 1, outfit: { top: 'suit', color: '#202030', head: 'none' }, pose: POSES.explain, expr: 'determined', talk: Math.abs(Math.sin(t * 9)) });
    g.fillStyle = 'rgba(0,0,0,.6)'; g.fillRect(X, Y + h - 110, w, 80); text(g, 'こんにちは、またね…', X + w / 2, Y + h - 70, { size: 46, color: '#fff', weight: 900, font: 'sans-serif' }); }); },
  plate_number: (g, t) => { const cx = E.W / 2, cy = E.H * 0.55; g.fillStyle = '#1a1424'; g.fillRect(-E.W, -E.H, E.W * 3, E.H * 3); rr(g, cx - 700, cy - 300, 1400, 600, 80); g.fillStyle = '#5a2a3a'; g.fill(); circle(g, cx - 520, cy + 260, 120, '#0a0a0e'); circle(g, cx + 520, cy + 260, 120, '#0a0a0e');
    rr(g, cx - 330, cy - 70, 660, 170, 16); g.fillStyle = '#f2f0e6'; g.fill(); g.strokeStyle = '#1a1a1a'; g.lineWidth = 6; g.stroke(); g.fillStyle = '#3a6ac0'; g.fillRect(cx - 330, cy - 70, 660, 40);
    text(g, 'مصر', cx, cy - 50, { size: 26, color: '#fff', weight: 900 }); text(g, 'ط ق س  ٧ ٣ ٤ ٢', cx, cy + 40, { size: 76, color: '#111', weight: 900 });
    const k = ease.out(prog(t, 0.3, 0.9)); g.strokeStyle = alpha(GOLD(), k); g.lineWidth = 6; rr(g, cx - 360, cy - 100, 720, 230, 20); g.stroke(); glow(g, cx, cy, 500, GOLD(), 0.15 * k); },
  digits: (g, t) => { backdrop(g, ['#05070f', '#0d1430']); const cols = 40, rows = 25; for (let j = 0; j < rows; j++) for (let i = 0; i < cols; i++) { const n = (i * 7 + j * 13 + i * j) % 10, on = (j * cols + i) < t / 2.5 * cols * rows; text(g, String(n), 170 + i * 40, 90 + j * 36, { size: 26, color: on ? GOLD() : 'rgba(150,170,220,.3)', weight: 900, font: FONTS.ui }); } },
  teacups: (g, t) => { const cx = E.W / 2, top = E.H * 0.72; g.fillStyle = '#2a1a16'; g.fillRect(-E.W, top, E.W * 3, E.H); g.fillStyle = 'rgba(255,200,140,.25)'; g.fillRect(-E.W, top, E.W * 3, 6); P.cup(g, cx - 260, top, 6, '#f2ece4', '#8a4a20', true); P.cup(g, cx + 260, top, 6, '#f2ece4', '#8a4a20', true);
    for (const dx of [-260, 260]) for (let k = 0; k < 3; k++) { const a = ((t * 0.4 + k * 0.33) % 1); seg(g, [[cx + dx - 30 + k * 30, top - 190 - a * 160], [cx + dx - 20 + k * 30 + Math.sin(t * 2 + k) * 14, top - 240 - a * 200]], 8, alpha('#ffffff', 0.22 * (1 - a))); } },
  card: (g, t) => { const cx = E.W / 2, cy = E.H * 0.55; g.fillStyle = '#c8a040'; rr(g, cx - 700, cy - 200, 1400, 900, 60); g.fill(); g.fillStyle = '#a8842a'; rr(g, cx - 640, cy - 140, 1280, 140, 30); g.fill();
    const k = ease.out(prog(t, 0.3, 1.4)); g.save(); g.translate(cx, cy - 260 + k * 160); g.rotate(-0.05); rr(g, -300, -170, 600, 340, 24); g.fillStyle = '#f6f2e6'; g.fill(); g.strokeStyle = '#d8cfb8'; g.lineWidth = 4; g.stroke();
    circle(g, -170, -20, 70, '#2a2230'); drawFigure(g, { x: -170, y: 80, s: 0.5, outfit: CAST.LAYLA, pose: POSES.stand, expr: 'smile' });
    text(g, 'ليلى', 110, -70, { size: 54, color: '#222', weight: 900 }); text(g, '010 ••• •••', 110, 20, { size: 40, color: '#444', weight: 900, font: FONTS.ui }); seg(g, [[-10, 90], [260, 90]], 6, '#ddd'); g.restore();
    seg(g, [[cx, cy - 430], [cx, cy - 260 + k * 160 - 170]], 4, '#555'); },
  phonering: (g, t, info) => { const cx = E.W / 2, cy = E.H * 0.6, [sx] = shake(t * 6, 8, 3); g.fillStyle = '#1a1214'; g.fillRect(-E.W, cy + 200, E.W * 3, 600); rr(g, cx - 180 + sx, cy - 330, 360, 640, 40); g.fillStyle = '#101018'; g.fill(); rr(g, cx - 160 + sx, cy - 300, 320, 580, 26); g.fillStyle = '#1e3a2a'; g.fill();
    circle(g, cx + sx, cy - 120, 80, info.callerColor || '#8a5ad6'); text(g, info.caller || 'أمي', cx + sx, cy + 10, { size: 64, color: '#fff', weight: 900 }); circle(g, cx - 80 + sx, cy + 180, 40, '#3fb950'); circle(g, cx + 80 + sx, cy + 180, 40, '#e04a3a'); FX.rings(g, cx, cy - 120, t, { count: 3, r0: 100, r1: 400, color: '#ffffff', a: 0.3, speed: 1.2 }); },
  group: (g, t) => { const cx = E.W / 2, cy = E.H * 0.55; rr(g, cx - 260, cy - 420, 520, 900, 46); g.fillStyle = '#101018'; g.fill(); rr(g, cx - 236, cy - 396, 472, 852, 30); g.fillStyle = '#e8e2d8'; g.fill(); g.fillStyle = '#2f6a5a'; g.fillRect(cx - 236, cy - 396, 472, 90); text(g, 'مجموعة الحي', cx, cy - 350, { size: 40, color: '#fff', weight: 900 });
    const k = ease.outBack(prog(t, 0.4, 0.9)); g.save(); g.translate(cx + 40, cy - 60); g.scale(k, k); rr(g, -170, -190, 340, 380, 18); g.fillStyle = '#d8f2c8'; g.fill(); rr(g, -150, -170, 300, 250, 12); g.fillStyle = '#8a7a6a'; g.fill(); drawFigure(g, { x: 0, y: 70, s: 0.75, outfit: CAST.LAYLA, pose: POSES.stand, expr: 'smile' }); text(g, 'هل رأى أحدكم جدتي؟', 0, 135, { size: 30, color: '#222', weight: 900 }); g.restore();
    for (let i = 0; i < 3; i++) { const a = ease.out(prog(t, 1.2 + i * 0.5, 1.6 + i * 0.5)); rr(g, cx - 200, cy + 180 + i * 80, 260, 60, 14); g.fillStyle = alpha('#ffffff', a); g.fill(); } },
  song: (g, t) => { backdrop(g, ['#120a1a', '#2a1530', '#4a2a2a']); const cx = E.W / 2, cy = E.H / 2; for (let i = 0; i < 9; i++) { const a = t * 0.6 + i * 0.7, x = cx + Math.cos(a) * (200 + i * 40), y = cy + Math.sin(a * 1.3) * 160 - i * 6; text(g, i % 2 ? '♪' : '♫', x, y, { size: 90 + (i % 3) * 30, color: alpha(GOLD(), 0.5 + 0.4 * Math.sin(t * 2 + i)), weight: 900, font: 'sans-serif', glow: 24, glowColor: alpha(GOLD(), 0.8) }); } glow(g, cx, cy, 500, GOLD(), 0.2); },
  stove: (g, t) => { const cx = E.W / 2, cy = E.H * 0.62; g.fillStyle = '#1a1418'; g.fillRect(-E.W, -E.H, E.W * 3, E.H * 3); g.fillStyle = '#2a2228'; g.fillRect(-E.W, cy + 60, E.W * 3, 800);
    for (let i = 0; i < 14; i++) { const a = i / 14 * Math.PI * 2, fl = 30 + Math.abs(Math.sin(t * 9 + i)) * 26; poly(g, [[cx + Math.cos(a) * 150, cy + 70 + Math.sin(a) * 30], [cx + Math.cos(a + 0.12) * 165, cy + 70 + Math.sin(a + 0.12) * 32], [cx + Math.cos(a + 0.06) * 160, cy + 40 - fl]], i % 2 ? '#4aa8ff' : '#ff9a3a'); }
    glow(g, cx, cy + 60, 520, '#ff7a2a', 0.35); g.fillStyle = '#5a5a66'; g.beginPath(); g.ellipse(cx, cy, 330, 80, 0, 0, 7); g.fill(); g.fillStyle = '#2a2a32'; g.beginPath(); g.ellipse(cx, cy - 12, 290, 62, 0, 0, 7); g.fill(); g.strokeStyle = 'rgba(255,170,90,.6)'; g.lineWidth = 4; g.beginPath(); g.ellipse(cx, cy, 330, 80, 0, Math.PI, 2 * Math.PI); g.stroke();
    rr(g, cx - 760, cy - 34, 440, 44, 20); g.fillStyle = '#6a6a76'; g.fill(); const k = ease.out(prog(t, 0.4, 1.0)); const hx = cx - 560 + (1 - k) * -500;
    handArm(g, hx, cy - 30, 1.3, '#e8a020', -1); const red = prog(t, 1.2, 3.0); if (red > 0) { glow(g, hx, cy - 20, 160, '#ff3a2a', 0.45 * red); circle(g, hx, cy - 30, 40 * 1.3, alpha('#c8322a', 0.5 * red)); }
    for (let i = 0; i < 6; i++) { const a = (t * 0.5 + i / 6) % 1; seg(g, [[cx - 150 + i * 60, cy - 60 - a * 200], [cx - 140 + i * 60 + Math.sin(t * 2 + i) * 16, cy - 120 - a * 260]], 8, alpha('#ffffff', 0.2 * (1 - a))); } },
  bell: (g, t, info) => { const cx = E.W / 2, cy = E.H * 0.48, silent = info.silent, sw = silent ? 0 : Math.sin(t * 22) * 0.18; g.save(); g.translate(cx, cy - 220); g.rotate(sw);
    g.fillStyle = '#d8a83a'; g.beginPath(); g.moveTo(-40, 0); g.quadraticCurveTo(-60, 80, -160, 300); g.lineTo(160, 300); g.quadraticCurveTo(60, 80, 40, 0); g.closePath(); g.fill(); circle(g, 0, -10, 50, '#d8a83a'); rr(g, -190, 290, 380, 40, 20); g.fillStyle = '#b8882a'; g.fill(); circle(g, 0, 350, 40, '#8a6420'); g.restore();
    if (!silent) FX.rings(g, cx, cy, t, { count: 4, r0: 260, r1: 700, color: '#ffe9b0', a: 0.45, speed: 1.4 });
    else { const k = ease.out(prog(t, 0.4, 0.8)); seg(g, [[cx - 280, cy - 340], [cx - 280 + 560 * k, cy - 340 + 600 * k]], 26, alpha('#e04a3a', 0.9)); } glow(g, cx, cy, 500, '#ffd47e', silent ? 0.05 : 0.2); },
  icewater: (g, t) => { const cx = E.W / 2, cy = E.H * 0.62; g.fillStyle = '#16202a'; g.fillRect(-E.W, -E.H, E.W * 3, E.H * 3); g.fillStyle = '#1e2a34'; g.fillRect(-E.W, cy + 170, E.W * 3, 800);
    handArm(g, cx + 40, cy + 20, 1.3, '#e8a020', 1); const blue = prog(t, 0.8, 3.5); circle(g, cx + 40, cy + 20, 56, alpha('#6a8ad8', 0.6 * blue));
    g.fillStyle = 'rgba(160,210,255,.35)'; g.beginPath(); g.moveTo(cx - 380, cy - 120); g.lineTo(cx + 380, cy - 120); g.lineTo(cx + 320, cy + 180); g.lineTo(cx - 320, cy + 180); g.closePath(); g.fill(); g.strokeStyle = 'rgba(220,240,255,.7)'; g.lineWidth = 6; g.stroke();
    for (let i = 0; i < 9; i++) { g.save(); g.translate(cx - 300 + i * 75, cy - 100 + Math.sin(t * 2 + i) * 8); g.rotate(i * 0.7); rr(g, -32, -32, 64, 64, 10); g.fillStyle = 'rgba(235,248,255,.85)'; g.fill(); g.restore(); }
    const m = Math.min(5, Math.floor(t * 1.4)); text(g, `${m}:00`, cx, E.H * 0.14, { size: 90, color: GOLD(), weight: 900, font: FONTS.ui, glow: 16, glowColor: alpha(GOLD(), 0.6) }); },
  views: (g, t) => { const cx = E.W / 2, cy = E.H * 0.55; handArm(g, cx + 160, cy + 260, 1.3, '#e04a3a'); rr(g, cx - 200, cy - 360, 400, 720, 44); g.fillStyle = '#101018'; g.fill(); rr(g, cx - 178, cy - 336, 356, 672, 30); g.fillStyle = '#3a3238'; g.fill();
    g.save(); g.beginPath(); rr(g, cx - 178, cy - 336, 356, 672, 30); g.clip(); g.fillStyle = '#4a4248'; g.fillRect(cx - 178, cy + 60, 356, 300); for (let k = 0; k < 8; k++) { g.fillStyle = 'rgba(255,190,90,.12)'; g.fillRect(cx - 178, cy + 80 + k * 30, 356, 2); }
    const step = Math.floor(t * 2.4) % 2; for (const [dx, ph] of [[-40, 0], [40, 1]]) { const up = (step === ph) ? 20 : 0; g.fillStyle = '#0e0b12'; g.beginPath(); g.ellipse(cx + dx, cy + 140 - up, 34, 70, 0, 0, 7); g.fill(); seg(g, [[cx + dx, cy + 80 - up], [cx + dx, cy - 200]], 40, '#0e0b12'); }
    glow(g, cx, cy + 200, 260, '#ff8a3a', 0.25); g.restore(); const n = Math.round(lerp(0, 100000, ease.out(prog(t, 0.3, 2.4)))); rr(g, cx - 170, cy - 320, 340, 70, 14); g.fillStyle = 'rgba(0,0,0,.6)'; g.fill(); text(g, '👁 ' + fmtNum(n), cx, cy - 285, { size: 44, color: '#fff', weight: 900, font: FONTS.ui }); },
  checklist: (g, t, info) => { const cx = E.W / 2, cy = E.H * 0.44; g.fillStyle = '#2a2026'; g.fillRect(-E.W, -E.H, E.W * 3, E.H * 3); g.save(); g.translate(cx, cy); g.rotate(-0.03); g.scale(0.82, 0.82); rr(g, -360, -400, 720, 800, 10); g.fillStyle = '#efe6cf'; g.fill(); g.strokeStyle = '#c8b890'; g.lineWidth = 3; g.stroke();
    const items = info.items || ['القدمان', 'الركبتان', 'اليدان', 'اللسان', 'العينان']; items.forEach((s, i) => { const y = -300 + i * 135, k = prog(t, (info.at ?? 0.4) + i * (info.gap ?? 0.55), (info.at ?? 0.4) + 0.3 + i * (info.gap ?? 0.55)); rr(g, -280, y - 34, 68, 68, 8); g.strokeStyle = '#3a3a4a'; g.lineWidth = 5; g.stroke(); text(g, s, 60, y, { size: 58, color: '#2a2a3a', weight: 900 }); if (k > 0) seg(g, [[-268, y], [-250, y + 22], [-250 + 50 * Math.min(1, k * 1.4), y + 22 - 60 * Math.min(1, k * 1.4)]], 10, info.red ? '#c8322a' : '#2fa04a'); });
    g.restore(); },
  xray: (g, t, info) => { backdrop(g, ['#05080e', '#0a1420']); const cx = E.W / 2, cy = E.H * 0.5; glow(g, cx, cy, 700, '#9fd0ff', 0.12); g.strokeStyle = 'rgba(230,245,255,.85)'; g.lineWidth = 10; g.lineCap = 'round';
    g.fillStyle = 'rgba(220,240,255,.55)'; rr(g, cx - 260, cy - 460, 90, 420, 40); g.fill(); rr(g, cx - 150, cy - 460, 70, 420, 34); g.fill();
    g.beginPath(); g.ellipse(cx - 170, cy + 10, 130, 70, 0, 0, 7); g.fill(); g.beginPath(); g.ellipse(cx + 40, cy + 120, 260, 70, 0.1, 0, 7); g.fill(); for (let k = 0; k < 5; k++) { rr(g, cx + 220 + k * 14, cy + 60 + k * 34, 210, 26, 13); g.fill(); }
    const cracks = [[cx - 215, cy - 60, '#ff3a2a', 0.5, 'كسر جديد'], [cx - 120, cy - 300, GOLD(), 1.4, 'قديم'], [cx + 60, cy + 120, GOLD(), 1.9, 'قديم'], [cx + 330, cy + 120, GOLD(), 2.4, 'قديم']];
    cracks.slice(0, info.n ?? 4).forEach(([x, y, c, at, s]) => { const a = ease.outBack(prog(t, at, at + 0.4)); if (a <= 0) return; seg(g, [[x - 26, y - 14], [x, y + 6], [x + 22, y - 10]], 6, c); ring(g, x, y, 70 * a, 6, alpha(c, 0.9)); text(g, s, x + 90, y - 70, { size: 46, color: c, weight: 900, align: 'left', alpha: clamp(a) }); }); },
  thermo: (g, t) => { const cx = E.W / 2, cy = E.H * 0.52; g.fillStyle = '#1e1620'; g.fillRect(-E.W, -E.H, E.W * 3, E.H * 3); rr(g, cx - 60, cy - 400, 120, 700, 60); g.fillStyle = '#e8eef4'; g.fill(); circle(g, cx, cy + 330, 110, '#e8eef4');
    const k = ease.inOut(prog(t, 0.3, 2.2)), top = lerp(cy + 200, cy - 300, k); rr(g, cx - 28, top, 56, cy + 300 - top, 28); g.fillStyle = '#e0322a'; g.fill(); circle(g, cx, cy + 330, 82, '#e0322a');
    for (let i = 0; i < 9; i++) seg(g, [[cx + 70, cy + 200 - i * 62], [cx + 110, cy + 200 - i * 62]], 4, '#9aa'); const v = lerp(36, 39, k).toFixed(1); text(g, v + '°', cx + 330, cy - 120, { size: 140, color: k > 0.85 ? CORAL() : GOLD(), weight: 900, font: FONTS.ui, glow: 20, glowColor: 'rgba(0,0,0,.5)' }); if (k > 0.95) glow(g, cx, cy + 330, 300, '#ff3a2a', 0.3 + 0.15 * Math.sin(t * 6)); },
  scoreboard: (g, t, info) => { const cx = E.W / 2, cy = E.H * 0.5; backdrop(g, ['#05070f', '#141a33']); rr(g, cx - 640, cy - 260, 1280, 520, 30); g.fillStyle = '#0a0a10'; g.fill(); g.strokeStyle = '#2a2a3a'; g.lineWidth = 12; g.stroke();
    text(g, info.score || '1 - 1', cx, cy - 20, { size: 260, color: '#ffcf4a', weight: 900, font: FONTS.ui, glow: 30, glowColor: 'rgba(255,190,60,.7)' }); text(g, info.min || "45'", cx, cy + 190, { size: 80, color: '#ff6a4a', weight: 900, font: FONTS.ui, glow: 16, glowColor: 'rgba(255,90,60,.6)' });
    for (const lx of [-560, 560]) glow(g, cx + lx, cy - 400, 300, '#fff3d0', 0.25); },
  nerve: (g, t, info) => { UI.blueprint(g); const c = UI.bpStroke(); const hand = [E.W * 0.18, E.H * 0.7], spine = [E.W * 0.55, E.H * 0.62], brain = [E.W * 0.7, E.H * 0.24];
    circle(g, hand[0], hand[1], 60, alpha(c, 0.3)); text(g, '✋', hand[0], hand[1], { size: 80, color: CREAM(), weight: 900, font: 'sans-serif' }); seg(g, [[spine[0], E.H * 0.9], [spine[0], brain[1] + 120]], 16, alpha(c, 0.35)); brainNet(g, t, brain[0], brain[1], 130, 1);
    g.strokeStyle = alpha(c, 0.8); g.lineWidth = 5; g.beginPath(); g.moveTo(hand[0], hand[1]); g.quadraticCurveTo(E.W * 0.36, E.H * 0.8, spine[0], spine[1]); g.lineTo(spine[0], brain[1] + 120); g.stroke();
    const P1 = (u) => { const a = 1 - u; return [a * a * hand[0] + 2 * a * u * E.W * 0.36 + u * u * spine[0], a * a * hand[1] + 2 * a * u * E.H * 0.8 + u * u * spine[1]]; };
    const gate = [E.W * 0.36, E.H * 0.74]; ring(g, gate[0], gate[1], 34, 6, info.broken ? CORAL() : GOLD()); text(g, info.gateLabel || 'البوابة', gate[0], gate[1] - 70, { size: 44, color: info.broken ? CORAL() : GOLD(), weight: 900 });
    const u = (t * 0.7) % 1.4; if (info.broken) { const k = Math.min(u, 0.5); const [x, y] = P1(k); circle(g, x, y, 16, GOLD()); glow(g, x, y, 60, GOLD(), 0.6); if (u > 0.5) { seg(g, [[gate[0] - 40, gate[1] - 40], [gate[0] + 40, gate[1] + 40]], 12, CORAL()); seg(g, [[gate[0] + 40, gate[1] - 40], [gate[0] - 40, gate[1] + 40]], 12, CORAL()); } }
    else if (info.reflex) { const k = Math.min(1, u); const [x, y] = k < 1 ? P1(k) : spine; circle(g, x, y, 16, GOLD()); glow(g, x, y, 60, GOLD(), 0.6); if (u > 1) { FX.rings(g, spine[0], spine[1], t, { count: 2, r0: 40, r1: 160, color: '#ffd47e', a: 0.6 }); text(g, 'اسحب يدك!', spine[0] + 40, spine[1] + 110, { size: 54, color: GOLD(), weight: 900 }); } }
    else { const k = Math.min(1, u); const [x, y] = k < 1 ? P1(k) : [spine[0], lerp(spine[1], brain[1] + 120, clamp((u - 1) / 0.4))]; circle(g, x, y, 16, GOLD()); glow(g, x, y, 60, GOLD(), 0.6); }
    if (info.gene) text(g, info.gene, E.W * 0.2, E.H * 0.18, { size: 70, color: GOLD(), weight: 900, font: FONTS.ui, glow: 16, glowColor: alpha(GOLD(), 0.6) }); },
  medal: (g, t) => { const cx = E.W / 2, cy = E.H * 0.56; backdrop(g, ['#1a1020', '#2a1a2a']); poly(g, [[cx - 140, cy - 520], [cx - 40, cy - 520], [cx + 30, cy - 120], [cx - 70, cy - 120]], '#2f7fd6'); poly(g, [[cx + 140, cy - 520], [cx + 40, cy - 520], [cx - 30, cy - 120], [cx + 70, cy - 120]], '#e04a3a');
    const k = ease.outBack(prog(t, 0.2, 0.8)); g.save(); g.translate(cx, cy + 60); g.scale(k, k); g.rotate(Math.sin(t * 1.5) * 0.06); circle(g, 0, 0, 210, '#d8a83a'); ring(g, 0, 0, 170, 12, '#b8882a'); text(g, '1', 0, 10, { size: 200, color: '#8a6420', weight: 900, font: FONTS.ui }); g.restore();
    glow(g, cx, cy + 60, 500, '#ffd47e', 0.3); FX.rings(g, cx, cy + 60, t, { count: 2, r0: 240, r1: 520, color: '#ffe9b0', a: 0.3 }); },
  bodymap: (g, t, info) => { UI.blueprint(g); const c = UI.bpStroke(), cx = E.W * 0.42, cy = E.H * 0.43; g.strokeStyle = alpha(c, 0.85); g.lineWidth = 6; g.fillStyle = alpha(c, 0.12);
    g.beginPath(); g.arc(cx, cy - 330, 70, 0, 7); g.fill(); g.stroke(); rr(g, cx - 95, cy - 245, 190, 300, 50); g.fill(); g.stroke();
    for (const sx of [-1, 1]) { rr(g, cx + sx * 135 - 25, cy - 230, 50, 280, 25); g.fill(); g.stroke(); rr(g, cx + sx * 50 - 30, cy + 60, 60, 330, 28); g.fill(); g.stroke(); g.beginPath(); g.ellipse(cx + sx * 50 + sx * 20, cy + 400, 50, 22, 0, 0, 7); g.fill(); g.stroke(); }
    for (const [dx, dy, s, at] of (info.spots || [[45, 10, 'الزائدة', 0.4]])) { const a = ease.outBack(prog(t, at, at + 0.4)); if (a <= 0) continue; const x = cx + dx, y = cy + dy; circle(g, x, y, 26 * a, alpha(CORAL(), 0.9)); glow(g, x, y, 120, CORAL(), 0.3 + 0.2 * Math.sin(t * 5)); FX.rings(g, x, y, t, { count: 2, r0: 30, r1: 120, color: '#ff7a5a', a: 0.5 }); seg(g, [[x + 30, y], [cx + 330, y]], 4, alpha(CORAL(), 0.8)); text(g, s, cx + 360, y, { size: 60, color: CORAL(), weight: 900, align: 'left', alpha: clamp(a) }); } },
  waves: (g, t, info) => { const cx = E.W / 2, cy = E.H * 0.52; backdrop(g, ['#0a0814', '#1a1230']); g.strokeStyle = '#f2e6ff'; g.lineWidth = 16; g.lineCap = 'round';
    g.beginPath(); g.moveTo(cx + 40, cy - 170); g.bezierCurveTo(cx - 170, cy - 220, cx - 190, cy + 40, cx - 60, cy + 90); g.bezierCurveTo(cx + 10, cy + 140, cx - 20, cy + 230, cx + 40, cy + 220); g.stroke();
    g.lineWidth = 10; g.beginPath(); g.moveTo(cx + 10, cy - 90); g.bezierCurveTo(cx - 80, cy - 100, cx - 80, cy + 10, cx - 10, cy + 20); g.stroke(); glow(g, cx, cy, 380, '#c8326e', 0.25);
    const src = info.src || ['قلب الجار', 'نملة على الزجاج', 'الثلاجة', 'همس أمك']; src.forEach((s, i) => { const a = i / src.length * Math.PI * 2 + 0.4, R = 560, x = cx + Math.cos(a) * R, y = cy + Math.sin(a) * R * 0.62, k = ease.outBack(prog(t, 0.2 + i * 0.4, 0.6 + i * 0.4)); if (k <= 0) return;
      for (let r = 0; r < 4; r++) { const u = ((t * 0.8 + r / 4) % 1); g.strokeStyle = alpha(GOLD(), 0.6 * (1 - u)); g.lineWidth = 4; g.beginPath(); g.arc(lerp(x, cx, u), lerp(y, cy, u), 30 + 30 * (1 - u), a + Math.PI - 0.6, a + Math.PI + 0.6); g.stroke(); }
      g.save(); g.translate(x, y); g.scale(k, k); rr(g, -150, -42, 300, 84, 16); g.fillStyle = 'rgba(18,14,38,.9)'; g.fill(); g.strokeStyle = alpha(GOLD(), 0.8); g.lineWidth = 3; g.stroke(); text(g, s, 0, 2, { size: 44, color: GOLD(), weight: 900 }); g.restore(); }); },
  heart: (g, t, info) => { backdrop(g, ['#12060c', '#2a0e1a']); const cx = E.W / 2, cy = E.H * 0.4, mode = info.mode || 'calm'; const per = mode === 'fast' ? 0.45 : 0.9, ph = (t % per) / per;
    let beat = Math.exp(-ph * 9); if (mode === 'stumble') beat = (Math.floor(t / 0.7) % 3 === 2) ? 0 : Math.exp(-((t % 0.7) / 0.7) * 9); const s = 1 + 0.12 * beat;
    g.save(); g.translate(cx, cy); g.scale(s * 2.2, s * 2.2); g.fillStyle = '#e0324a'; g.beginPath(); g.moveTo(0, 60); g.bezierCurveTo(-120, -10, -70, -110, 0, -50); g.bezierCurveTo(70, -110, 120, -10, 0, 60); g.fill(); g.restore(); glow(g, cx, cy, 420, '#ff3a5a', 0.2 + 0.3 * beat);
    g.strokeStyle = '#7affb0'; g.lineWidth = 6; g.beginPath(); const y0 = E.H * 0.8; for (let x = 0; x <= E.W; x += 6) { const u = (x / E.W * 4 - t * (mode === 'fast' ? 2 : 1)) % 1, uu = u < 0 ? u + 1 : u; let y = y0; if (uu > 0.45 && uu < 0.55 && !(mode === 'stumble' && Math.floor((x / E.W * 4 - t) ) % 3 === 0)) y -= Math.sin((uu - 0.45) / 0.1 * Math.PI * 2) * 120; x ? g.lineTo(x, y) : g.moveTo(x, y); } g.stroke();
    if (info.label) text(g, info.label, cx, E.H * 0.17, { size: 64, color: GOLD(), weight: 900 }); },
  building: (g, t, info) => { backdrop(g, ['#05070f', '#141a36']); const cx = E.W / 2, w = 760, fh = 130, n = 6, base = E.H * 0.9; rr(g, cx - w / 2, base - n * fh - 20, w, n * fh + 20, 10); g.fillStyle = '#2a2638'; g.fill();
    for (let f = 0; f < n; f++) for (let k = 0; k < 4; k++) { const x = cx - w / 2 + 40 + k * 180, y = base - (f + 1) * fh + 20; rr(g, x, y, 140, 90, 6); g.fillStyle = (f * 3 + k) % 4 === 0 ? '#f2c96a' : '#3a3a52'; g.fill(); }
    if (info.hiss) { const f = 4, y = base - (f + 1) * fh + 65; for (let r = 0; r < 4; r++) { const u = (t * 0.9 + r / 4) % 1; ring(g, cx + 250, y, 40 + u * 260, 5, alpha('#9affc0', 0.7 * (1 - u))); } text(g, 'ششش…', cx + 560, y, { size: 60, color: '#9affc0', weight: 900 }); text(g, 'الطابق 5', cx - 560, y, { size: 50, color: CREAM(), weight: 900 }); }
    if (info.snore) for (let f = 0; f < n; f++) { const y = base - (f + 1) * fh + 40, k = (t * 1.2 + f * 0.3) % 1; text(g, 'Zzz', cx + w / 2 + 70 + k * 40, y - k * 40, { size: 40 + f * 2, color: alpha(CREAM(), 1 - k), weight: 900, font: FONTS.ui }); } },
  cat: (g, t, info) => { const cx = E.W / 2, cy = E.H * 0.58; g.fillStyle = '#2a1e18'; g.fillRect(-E.W, -E.H, E.W * 3, E.H * 3); g.fillStyle = '#3a2a20'; g.fillRect(-E.W, cy - 260, E.W * 3, 80);
    const out = info.out; if (!out) { rr(g, cx - 700, cy - 120, 1400, 240, 120); g.fillStyle = '#4a4a56'; g.fill(); rr(g, cx - 680, cy - 100, 1360, 200, 100); g.fillStyle = '#0c0a10'; g.fill(); const bl = (t % 3) > 2.85; if (!bl) { circle(g, cx - 30, cy, 16, '#c8f05a'); circle(g, cx + 30, cy, 16, '#c8f05a'); } text(g, 'مياو…', cx, cy - 180, { size: 60, color: alpha(CREAM(), 0.6 + 0.4 * Math.sin(t * 3)), weight: 900 }); }
    else { g.save(); g.translate(cx, cy + 60); g.scale(2.4, 2.4); g.fillStyle = '#e8a050'; g.beginPath(); g.ellipse(0, 20, 70, 45, 0, 0, 7); g.fill(); circle(g, 55, -30, 38, '#e8a050'); poly(g, [[30, -55], [40, -85], [55, -60]], '#e8a050'); poly(g, [[62, -62], [80, -88], [85, -55]], '#e8a050'); circle(g, 48, -32, 5, '#111'); circle(g, 68, -32, 5, '#111'); g.strokeStyle = '#e8a050'; g.lineWidth = 10; g.beginPath(); g.moveTo(-65, 20); g.quadraticCurveTo(-120, -10 + Math.sin(t * 3) * 15, -100, -60); g.stroke(); g.restore(); glow(g, cx, cy, 400, '#ffd47e', 0.2); text(g, 'همسة', cx, E.H * 0.14, { size: 80, color: GOLD(), weight: 900 }); } },
  gas: (g, t) => { const cx = E.W / 2, cy = E.H * 0.5; g.fillStyle = '#16141c'; g.fillRect(-E.W, -E.H, E.W * 3, E.H * 3); rr(g, -100, cy - 50, E.W + 200, 100, 30); g.fillStyle = '#c8a040'; g.fill(); g.fillStyle = 'rgba(0,0,0,.25)'; g.fillRect(-100, cy + 20, E.W + 200, 30);
    seg(g, [[cx - 20, cy - 50], [cx + 10, cy - 10], [cx - 10, cy + 20], [cx + 20, cy + 50]], 6, '#111'); for (let i = 0; i < 12; i++) { const u = (t * 0.7 + i / 12) % 1, a = -Math.PI / 2 + (i % 5 - 2) * 0.25; g.strokeStyle = alpha('#9affc0', 0.6 * (1 - u)); g.lineWidth = 5; g.beginPath(); g.arc(cx + Math.cos(a) * u * 400, cy - 50 + Math.sin(a) * u * 400, 20 + u * 30, 0, Math.PI); g.stroke(); }
    text(g, 'ششششش…', cx, E.H * 0.16, { size: 90, color: '#9affc0', weight: 900, glow: 18, glowColor: 'rgba(120,255,180,.5)' }); },
  news: (g, t, info) => { const cx = E.W / 2, cy = E.H * 0.55; g.fillStyle = '#2a2026'; g.fillRect(-E.W, -E.H, E.W * 3, E.H * 3); g.save(); g.translate(cx, cy); g.rotate(-0.04 + 0.04 * ease.out(prog(t, 0, 0.8))); const k = ease.outBack(prog(t, 0, 0.6)); g.scale(k, k);
    rr(g, -560, -380, 1120, 760, 6); g.fillStyle = '#efe9dc'; g.fill(); g.fillStyle = '#1a1a1a'; g.fillRect(-520, -340, 1040, 8); text(g, 'أخبار المدينة', 0, -295, { size: 46, color: '#1a1a1a', weight: 900 }); g.fillRect(-520, -255, 1040, 4);
    text(g, info.head || 'فتى ينقذ عمارة كاملة', 0, -170, { size: 78, color: '#111', weight: 900 }); rr(g, -500, -90, 440, 400, 6); g.fillStyle = '#8a8a8a'; g.fill(); drawFigure(g, { x: -280, y: 290, s: 1.3, outfit: CAST[info.who || 'OMAR'], pose: POSES.stand, expr: 'smile' });
    for (let i = 0; i < 10; i++) { g.fillStyle = 'rgba(30,30,30,.45)'; g.fillRect(-20, -80 + i * 38, 520 - (i % 3) * 60, 12); } g.restore(); },
  headphones: (g, t) => { const cx = E.W / 2, cy = E.H * 0.55; backdrop(g, ['#0c0a14', '#1e1830']); g.strokeStyle = '#1a1a22'; g.lineWidth = 60; g.beginPath(); g.arc(cx, cy, 300, Math.PI * 1.05, Math.PI * 1.95); g.stroke();
    for (const sx of [-1, 1]) { rr(g, cx + sx * 300 - 90, cy - 60, 180, 280, 70); g.fillStyle = '#2a2a36'; g.fill(); rr(g, cx + sx * 300 - 60, cy - 30, 120, 220, 50); g.fillStyle = '#c8326e'; g.fill(); }
    for (let i = 0; i < 6; i++) { const u = (t * 0.6 + i / 6) % 1, a = i * 1.1; text(g, ['بيب', 'زززز', 'طق', 'هووو', 'ترررن', 'شخ'][i], cx + Math.cos(a) * (200 + u * 500), cy + Math.sin(a) * (150 + u * 300) - 100, { size: 50, color: alpha(GOLD(), 1 - u), weight: 900 }); } },
  bubbles: (g, t, info) => { backdrop(g, ['#0a0814', '#1a1230']); const n = info.n || 40, pick = info.pick; for (let i = 0; i < n; i++) { const x = (i * 211) % E.W, y = 120 + (i * 137) % (E.H - 300), sel = false, fade = pick ? 1 - 0.85 * ease.inOut(prog(t, 0.8, 2.5)) : 1;
      g.save(); g.translate(x + Math.sin(t + i) * 10, y); g.globalAlpha = sel ? 1 : 0.5 * fade; rr(g, -70, -36, 140, 72, 30); g.fillStyle = sel ? GOLD() : '#6a6a8a'; g.fill(); poly(g, [[-20, 30], [-40, 56], [0, 34]], sel ? GOLD() : '#6a6a8a'); for (let k = 0; k < 3; k++) circle(g, -30 + k * 30, 0, 7, sel ? '#2a1a00' : '#2a2a3a'); g.restore();
      }
    if (pick) { const k = ease.outBack(prog(t, 0.6, 1.2)), cx = E.W / 2, cy = E.H * 0.42; glow(g, cx, cy, 300, GOLD(), 0.3 * k); g.save(); g.translate(cx, cy); g.scale(2.2 * k, 2.2 * k); rr(g, -70, -36, 140, 72, 30); g.fillStyle = GOLD(); g.fill(); poly(g, [[-20, 30], [-40, 56], [0, 34]], GOLD()); for (let q = 0; q < 3; q++) circle(g, -30 + q * 30, 0, 7, '#2a1a00'); g.restore(); if (info.label) text(g, info.label, cx, cy - 150, { size: 64, color: GOLD(), weight: 900, alpha: ease.out(prog(t, 1.2, 1.6)) }); } },
  moth: (g, t) => { UI.blueprint(g); const cx = E.W / 2, cy = E.H * 0.5, f = Math.sin(t * 14) * 0.25; for (const sx of [-1, 1]) { g.save(); g.translate(cx, cy); g.scale(sx, 1); g.rotate(f); g.fillStyle = '#c8b080'; g.beginPath(); g.ellipse(170, -60, 190, 120, -0.3, 0, 7); g.fill(); g.fillStyle = '#a89060'; g.beginPath(); g.ellipse(130, 90, 120, 80, 0.4, 0, 7); g.fill(); g.restore(); }
    g.fillStyle = '#6a5a3a'; g.beginPath(); g.ellipse(cx, cy, 34, 150, 0, 0, 7); g.fill(); seg(g, [[cx - 10, cy - 140], [cx - 60, cy - 240]], 4, '#6a5a3a'); seg(g, [[cx + 10, cy - 140], [cx + 60, cy - 240]], 4, '#6a5a3a');
    text(g, '300,000 هرتز', cx, E.H * 0.2, { size: 76, color: GOLD(), weight: 900, font: FONTS.ui, glow: 16, glowColor: alpha(GOLD(), 0.6), alpha: ease.out(prog(t, 0.4, 0.8)) }); },
  clock24: (g, t, info) => { backdrop(g, ['#05070f', '#141a36']); const cx = E.W / 2, cy = E.H * 0.5, R = 330, k = ease.inOut(prog(t, 0.3, 2.0));
    g.fillStyle = '#1e2440'; g.beginPath(); g.arc(cx, cy, R, 0, 7); g.fill(); g.fillStyle = GOLD(); g.beginPath(); g.moveTo(cx, cy); g.arc(cx, cy, R - 20, -Math.PI / 2, -Math.PI / 2 + Math.PI * 2 * (23 / 24) * k); g.closePath(); g.fill();
    g.fillStyle = '#4a5aa0'; g.beginPath(); g.moveTo(cx, cy); g.arc(cx, cy, R - 20, -Math.PI / 2 - Math.PI * 2 / 24, -Math.PI / 2); g.closePath(); g.fill(); circle(g, cx, cy, R * 0.55, '#141a36');
    text(g, '23', cx, cy - 20, { size: 150, color: GOLD(), weight: 900, font: FONTS.ui }); text(g, 'ساعة يقظة', cx, cy + 90, { size: 48, color: CREAM(), weight: 900 }); text(g, '1 نوم', cx - 150, cy - R - 50, { size: 46, color: '#9fb0ff', weight: 900, alpha: ease.out(prog(t, 1.6, 2.0)) }); },
  mural: (g, t, info) => { const cx = E.W / 2, cy = E.H * 0.5, gray = info.gray; g.fillStyle = '#2a2026'; g.fillRect(-E.W, -E.H, E.W * 3, E.H * 3); rr(g, cx - 760, cy - 400, 1520, 760, 10); g.fillStyle = '#d8d0c0'; g.fill();
    const cols = gray ? ['#8a8a8a', '#6a6a6a', '#9a9a9a', '#7a7a7a'] : ['#e04a3a', '#f2c21a', '#2f7fd6', '#3fb950']; const k = gray ? 1 : ease.out(prog(t, 0.2, 2.0));
    for (let i = 0; i < 9; i++) { g.save(); g.globalAlpha = Math.min(1, k * 9 - i); g.fillStyle = cols[i % 4]; g.beginPath(); g.arc(cx - 600 + i * 150, cy + Math.sin(i * 1.7) * 160, 90 + (i % 3) * 30, 0, 7); g.fill(); g.restore(); }
    FX.sun(g, cx + 450, cy - 220, 80, gray ? '#cfcfcf' : '#fff3c0', gray ? '#9a9a9a' : '#ffc040', 3); if (gray) { g.fillStyle = 'rgba(40,40,50,.25)'; g.fillRect(cx - 760, cy - 400, 1520, 760); } },
  eeg: (g, t) => { UI.blueprint(g); const c = UI.bpStroke(); for (let r = 0; r < 4; r++) { const y0 = E.H * (0.25 + r * 0.15); g.strokeStyle = r === 0 ? GOLD() : alpha(c, 0.8); g.lineWidth = 4; g.beginPath();
      for (let x = 120; x < E.W - 120; x += 5) { const u = (x - 120) / (E.W - 240), deep = u < 0.72, amp = deep ? 60 : 18, f = deep ? 0.012 : 0.09; const y = y0 + Math.sin(x * f + r + t * 2) * amp * (u < (t / 3) ? 1 : 0); x === 120 ? g.moveTo(x, y) : g.lineTo(x, y); } g.stroke(); }
    const x = 120 + (E.W - 240) * 0.72; seg(g, [[x, E.H * 0.15], [x, E.H * 0.82]], 4, CORAL()); text(g, 'نوم عميق', x - 380, E.H * 0.2, { size: 50, color: GOLD(), weight: 900 }); text(g, 'استيقاظ!', x + 180, E.H * 0.2, { size: 50, color: CORAL(), weight: 900, alpha: ease.out(prog(t, 2.0, 2.4)) }); },
  chat: (g, t, info) => { const cx = E.W / 2, cy = E.H * 0.55; handArm(g, cx + 160, cy + 260, 1.3, '#c8692a'); rr(g, cx - 200, cy - 380, 400, 740, 44); g.fillStyle = '#101018'; g.fill(); rr(g, cx - 178, cy - 356, 356, 692, 30); g.fillStyle = '#0e1622'; g.fill();
    text(g, '3:07', cx, cy - 320, { size: 30, color: '#aab', weight: 900, font: FONTS.ui }); const msgs = info.msgs || ['صاحي؟', 'هههه شفت المباراة؟', 'يا جماعة؟', '…']; msgs.forEach((m, i) => { const a = ease.outBack(prog(t, 0.3 + i * 0.6, 0.6 + i * 0.6)); if (a <= 0) return; g.save(); g.translate(cx + 40, cy - 240 + i * 120); g.scale(a, a); rr(g, -120, -40, 260, 80, 22); g.fillStyle = '#1f6a4a'; g.fill(); text(g, m, 10, 0, { size: 34, color: '#fff', weight: 900 }); text(g, '✓', 110, 26, { size: 24, color: '#9aa', weight: 900, font: 'sans-serif' }); g.restore(); }); },
  breath: (g, t) => { backdrop(g, ['#0a0e1a', '#1a1030']); const cx = E.W / 2, cy = E.H * 0.5, s = 1 + 0.06 * Math.sin(t * 9); for (const sx of [-1, 1]) { g.save(); g.translate(cx + sx * 150, cy); g.scale(sx * s, s); g.fillStyle = alpha('#ff7a8a', 0.8); g.beginPath(); g.moveTo(0, -220); g.bezierCurveTo(160, -200, 190, 120, 120, 230); g.bezierCurveTo(40, 260, 10, 180, 0, 100); g.closePath(); g.fill(); g.restore(); }
    seg(g, [[cx, cy - 330], [cx, cy - 120]], 30, alpha('#ff7a8a', 0.8)); const n = Math.round(lerp(30, 40, clamp(t / 2.5))); text(g, `${n} نفسا / دقيقة`, cx, E.H * 0.17, { size: 70, color: CORAL(), weight: 900, glow: 18, glowColor: alpha(CORAL(), 0.5) }); for (let i = 0; i < 6; i++) { const u = (t * 1.5 + i / 6) % 1; text(g, '~', cx + 300 + u * 200, cy - 100 + i * 40, { size: 60, color: alpha(CREAM(), 1 - u), weight: 900, font: 'sans-serif' }); } },
  storybook: (g, t) => { const cx = E.W / 2, cy = E.H * 0.58; g.fillStyle = '#1e1622'; g.fillRect(-E.W, -E.H, E.W * 3, E.H * 3); glow(g, cx, cy - 100, 600, '#ffd47e', 0.2); g.save(); g.translate(cx, cy); rr(g, -620, -320, 600, 600, 12); g.fillStyle = '#f6efe0'; g.fill(); rr(g, 20, -320, 600, 600, 12); g.fill();
    g.fillStyle = '#5ab0e8'; g.fillRect(40, 60, 560, 200); for (let i = 0; i < 4; i++) { g.strokeStyle = '#3a90c8'; g.lineWidth = 6; g.beginPath(); g.moveTo(40, 100 + i * 45); for (let x = 40; x < 600; x += 40) g.quadraticCurveTo(x + 20, 85 + i * 45, x + 40, 100 + i * 45); g.stroke(); }
    const fy = -120 + Math.sin(t * 2) * 25; drawFigure(g, { x: 260, y: fy, s: 0.8, outfit: CAST.LINA, pose: POSES.wave, expr: 'joy', rot: -0.3 }); g.fillStyle = '#8a8a8a'; g.beginPath(); g.ellipse(430, fy - 40, 40, 26, 0, 0, 7); g.fill(); circle(g, 465, fy - 62, 22, '#8a8a8a');
    text(g, 'كان يا ما كان…', -320, -220, { size: 56, color: '#3a2a20', weight: 900 }); for (let i = 0; i < 8; i++) { g.fillStyle = 'rgba(60,40,30,.3)'; g.fillRect(-560, -120 + i * 44, 420 + (i % 3) * 40, 10); } g.restore(); },
  dreamsea: (g, t) => { backdrop(g, ['#0a0a2a', '#2a1a4a', '#4a2a5a']); const cx = E.W / 2; for (let i = 0; i < 60; i++) circle(g, (i * 173) % E.W, (i * 97) % (E.H * 0.5), 2 + (i % 3), alpha('#fff', 0.5 + 0.5 * Math.sin(t * 2 + i))); circle(g, cx + 500, E.H * 0.22, 70, '#fff3dc'); glow(g, cx + 500, E.H * 0.22, 300, '#fff3dc', 0.3);
    g.fillStyle = '#1a2a5a'; g.fillRect(-E.W, E.H * 0.68, E.W * 3, E.H); for (let i = 0; i < 12; i++) { g.fillStyle = `rgba(255,240,220,${0.4 - i * 0.03})`; g.fillRect(cx + 500 - 120 + Math.sin(t + i) * 20, E.H * 0.7 + i * i * 2, 240 - i * 15, 4); }
    const y = E.H * 0.45 + Math.sin(t * 1.5) * 20; drawFigure(g, { x: cx - 200 + t * 30, y, s: 1.2, outfit: CAST.LINA, pose: POSES.wave, expr: 'joy', rot: -0.5 }); drawFigure(g, { x: cx + 50 + t * 30, y: y + 30, s: 1.4, outfit: CAST.ZAID, pose: POSES.wave, expr: 'joy', rot: -0.5 }); },
  hypno: (g, t) => { UI.blueprint(g); const c = UI.bpStroke(), x0 = 380, x1 = E.W - 200, y0 = E.H * 0.3, step = E.H * 0.11; const lv = ['يقظة', 'حلم (REM)', 'خفيف', 'عميق'];
    lv.forEach((s, i) => text(g, s, x0 - 30, y0 + i * step, { size: 38, color: i === 1 ? GOLD() : CREAM(), weight: 900, align: 'right' }));
    const seq = [0, 2, 3, 3, 2, 1, 2, 3, 2, 1, 1, 2, 3, 2, 1, 1, 1, 2, 1, 1, 1, 0], k = ease.inOut(prog(t, 0.2, 2.6)), n = seq.length; g.strokeStyle = alpha(c, 0.9); g.lineWidth = 6; g.beginPath();
    for (let i = 0; i < n * k; i++) { const x = lerp(x0, x1, i / n), y = y0 + seq[i] * step; i ? g.lineTo(x, y) : g.moveTo(x, y); g.lineTo(lerp(x0, x1, (i + 1) / n), y); } g.stroke();
    for (let i = 0; i < n * k; i++) if (seq[i] === 1) { g.fillStyle = alpha(GOLD(), 0.5); g.fillRect(lerp(x0, x1, i / n), y0 + step - 14, (x1 - x0) / n, 28); }
    seg(g, [[lerp(x0, x1, 4 / n), y0 - 40], [lerp(x0, x1, 4 / n), y0 + 3.4 * step]], 5, CORAL()); text(g, 'ساعة زيد', lerp(x0, x1, 4 / n), y0 + 3.8 * step, { size: 44, color: CORAL(), weight: 900 }); text(g, '~90 دقيقة لكل دورة', E.W * 0.6, E.H * 0.19, { size: 48, color: GOLD(), weight: 900 }); },
  dolphin: (g, t) => { backdrop(g, ['#062a3a', '#0a4a5a']); const cx = E.W / 2, cy = E.H * 0.58, b = Math.sin(t * 1.2) * 15; g.save(); g.translate(cx, cy + b); g.rotate(-0.08);
    g.fillStyle = '#7aa0b8'; g.beginPath(); g.moveTo(-420, 10); g.quadraticCurveTo(-200, -150, 150, -110); g.quadraticCurveTo(330, -90, 360, -30); g.quadraticCurveTo(470, -20, 500, 0); g.quadraticCurveTo(470, 25, 360, 30); g.quadraticCurveTo(200, 120, -150, 90); g.quadraticCurveTo(-330, 70, -420, 10); g.fill();
    g.fillStyle = '#d8e8f0'; g.beginPath(); g.moveTo(-200, 70); g.quadraticCurveTo(100, 120, 360, 30); g.quadraticCurveTo(150, 60, -200, 70); g.fill();
    poly(g, [[-430, 10], [-560, -90], [-520, 10], [-560, 110]], '#7aa0b8'); g.fillStyle = '#7aa0b8'; g.beginPath(); g.moveTo(-60, -125); g.quadraticCurveTo(-20, -240, 60, -250); g.quadraticCurveTo(20, -170, 60, -115); g.fill();
    circle(g, 330, -45, 12, '#111'); g.strokeStyle = '#2a3a4a'; g.lineWidth = 4; g.beginPath(); g.moveTo(380, 8); g.quadraticCurveTo(430, 20, 480, 4); g.stroke(); g.restore();
    const bx = cx + 220, by = cy - 330; g.fillStyle = alpha('#3a4a6a', 0.9); g.beginPath(); g.arc(bx, by, 110, Math.PI / 2, Math.PI * 1.5); g.fill(); g.fillStyle = GOLD(); g.beginPath(); g.arc(bx, by, 110, -Math.PI / 2, Math.PI / 2); g.fill(); glow(g, bx + 40, by, 200, GOLD(), 0.3);
    text(g, 'نائم', bx - 220, by, { size: 50, color: '#9fb0ff', weight: 900 }); text(g, 'مستيقظ', bx + 250, by, { size: 50, color: GOLD(), weight: 900 }); for (let i = 0; i < 8; i++) { const u = (t * 0.5 + i / 8) % 1; circle(g, cx - 300 + i * 90, cy + 300 - u * 500, 8, alpha('#cfefff', 0.6 * (1 - u))); } },
};
export function insert(g, t, info) {
  const cam = camOf(t, { ...info, cam: info.cam || { z0: 1.0, z1: 1.08, x0: 0, x1: -20 } });
  backdrop(g, ['#1a1218', '#2a1e24', '#3a2a28']);
  g.save(); g.translate(E.W / 2, E.H / 2); g.scale(cam.z, cam.z); g.translate(-E.W / 2 + cam.x, -E.H / 2 + cam.y);
  INSERTS[info.kind]?.(g, t, info); g.restore();
  glow(g, E.W * 0.5, E.H * 0.2, 900, '#ffd59a', 0.06); FX.dust(g, t, { count: 30, a: 0.25 }); overlays(g, t, info);
}

// ---------- 4. DATA: a big animated number on a dark card ----------
function fmtNum(n, sep = ',') { return Math.round(n).toString().replace(/\B(?=(\d{3})+(?!\d))/g, sep); }
export function data(g, t, info) {
  UI.blueprint(g); const c = UI.bpStroke(), gold = GOLD(); const at = info.at ?? 0.3;
  const k = ease.out(prog(t, at, at + (info.count ?? 1.6)));
  const val = info.to != null ? fmtNum(lerp(info.from ?? 0, info.to, k)) + (info.suffix || '') : info.value;
  const pop = ease.outBack(prog(t, at - 0.2, at + 0.2));
  if (info.icon === 'brain') brainNet(g, t, E.W * 0.5, E.H * 0.42, 260, k);
  if (info.icon === 'life') { const w = 1300, x0 = E.W / 2 - w / 2, y = E.H * 0.33; rr(g, x0, y - 14, w, 28, 14); g.fillStyle = alpha(c, 0.15); g.fill(); rr(g, x0, y - 14, Math.max(28, w * k), 28, 14); g.fillStyle = gold; g.fill(); for (let i = 0; i <= 8; i++) { seg(g, [[x0 + i * w / 8, y + 24], [x0 + i * w / 8, y + 40]], 3, alpha(c, 0.7)); text(g, String(i * 10), x0 + i * w / 8, y + 64, { size: 26, color: alpha(c, 0.8), weight: 900, font: FONTS.ui }); } }
  g.save(); g.translate(E.W / 2, E.H * (info.icon ? 0.62 : 0.48)); g.scale(0.7 + 0.3 * pop, 0.7 + 0.3 * pop);
  text(g, val, 0, 0, { size: info.size || 150, color: info.color === 'coral' ? CORAL() : gold, weight: 900, font: FONTS.ui, glow: 30, glowColor: alpha(gold, 0.6), alpha: clamp(pop) });
  if (info.label) text(g, info.label, 0, (info.size || 150) * 0.62 + 50, { size: 60, color: CREAM(), weight: 900, alpha: ease.out(prog(t, at + 0.4, at + 0.8)) });
  g.restore();
  if (info.sub) text(g, info.sub, E.W / 2, E.H * 0.9, { size: 44, color: alpha(c, 0.9), weight: 700, alpha: ease.out(prog(t, at + 0.8, at + 1.2)) });
  overlays(g, t, info);
}
function brainNet(g, t, cx, cy, r, k) {
  const c = UI.bpStroke(); g.strokeStyle = alpha(c, 0.8); g.lineWidth = 5; g.beginPath(); g.ellipse(cx - r * 0.3, cy, r * 0.62, r * 0.75, 0, 0, 7); g.stroke(); g.beginPath(); g.ellipse(cx + r * 0.3, cy, r * 0.62, r * 0.75, 0, 0, 7); g.stroke();
  const pts = []; for (let i = 0; i < 46; i++) { const a = i * 2.39, d = Math.sqrt((i + 1) / 46) * r * 0.85; pts.push([cx + Math.cos(a) * d * 1.15, cy + Math.sin(a) * d * 0.85]); }
  for (let i = 0; i < pts.length; i++) for (let j = i + 1; j < pts.length; j++) { const dx = pts[i][0] - pts[j][0], dy = pts[i][1] - pts[j][1]; if (dx * dx + dy * dy < 9000 && (i + j) % 3 === 0) seg(g, [pts[i], pts[j]], 2, alpha(c, 0.35)); }
  pts.forEach(([x, y], i) => { const on = (i / pts.length) < k; circle(g, x, y, 6, on ? GOLD() : alpha(c, 0.5)); if (on) glow(g, x, y, 26, GOLD(), 0.3 + 0.3 * Math.sin(t * 4 + i)); });
}

// ---------- 5. CURVE: Ebbinghaus forgetting curve (blueprint) ----------
export function curve(g, t, info) {
  UI.blueprint(g); const c = UI.bpStroke(), gold = GOLD();
  const x0 = 380, x1 = E.W - 260, y0 = E.H * 0.22, y1 = E.H * 0.78;
  seg(g, [[x0, y0 - 30], [x0, y1], [x1 + 30, y1]], 4, alpha(c, 0.8));
  text(g, 'ما نتذكره', x0 - 20, y0 - 60, { size: 40, color: c, weight: 900, align: 'right' }); text(g, 'الأيام', x1, y1 + 60, { size: 40, color: c, weight: 900 });
  const k = ease.inOut(prog(t, 0.4, 2.6)); g.strokeStyle = CORAL(); g.lineWidth = 8; g.beginPath();
  for (let i = 0; i <= 100 * k; i++) { const u = i / 100, x = lerp(x0, x1, u), y = lerp(y0, y1, 1 - (0.25 + 0.75 * Math.exp(-u * 7))); i ? g.lineTo(x, y) : g.moveTo(x, y); } g.stroke();
  if (info.you) { const k2 = ease.inOut(prog(t, info.you, info.you + 1.2)); seg(g, [[x0, y0 + 4], [lerp(x0, x1, k2), y0 + 4]], 10, gold); glow(g, lerp(x0, x1, k2), y0 + 4, 60, gold, 0.6); if (k2 > 0.1) text(g, 'أنت', lerp(x0, x1, k2) - 60, y0 - 40, { size: 50, color: gold, weight: 900, glow: 16, glowColor: alpha(gold, 0.6) }); }
  UI.badge(g, { str: '1885', a: ease.out(prog(t, 0.2, 0.6)), size: 56 });
  if (info.label) text(g, info.label, E.W * 0.62, E.H * 0.42, { size: 52, color: CORAL(), weight: 900, alpha: ease.out(prog(t, 1.6, 2.1)) });
  overlays(g, t, info);
}

// ---------- 6. ARCHIVE: memory void (motif) ----------
export function archive(g, t, info) {
  const cam = camOf(t, info); P.archive(g, t, cam, { count: info.n || 36, speed: info.speed ?? 1, focus: info.focus });
  if (info.hero) layer(g, cam, 1, (g) => { const M = mood('void'); drawFigure(g, { x: E.W / 2, y: E.H * 0.78, s: info.hs || 1.5, facing: 1, outfit: CAST[info.heroC || 'YOU'], pose: breathe(POSES[info.pose || 'stand'], t), expr: seqVal(t, info.expr, 'awe'), rim: { color: '#ffd47e', dir: [0, -1] } }); FX.pool(g, E.W / 2, E.H * 0.79, 300, 50, '#ffd47e', 0.25); });
  if (info.cards) info.cards.forEach((s, i) => { const a = ease.outBack(prog(t, 0.3 + i * (info.gap ?? 0.5), 0.7 + i * (info.gap ?? 0.5))); if (a <= 0) return; const x = E.W * (info.cardsX?.[i] ?? (0.2 + 0.3 * i)), y = E.H * (info.cardsY?.[i] ?? 0.3);
    g.save(); g.translate(x, y); g.scale(a, a); rr(g, -190, -60, 380, 120, 16); g.fillStyle = 'rgba(18,28,48,.9)'; g.fill(); g.strokeStyle = alpha(GOLD(), 0.8); g.lineWidth = 3; g.stroke(); text(g, s, 0, 2, { size: 52, color: GOLD(), weight: 900 }); g.restore(); });
  overlays(g, t, info);
}

// ---------- 7. TITLE / BIGLINE / END ----------
export function title(g, t, info) {
  const M = mood('dusk'), cam = { z: 1.06 - 0.06 * ease.inOut(t / info.dur), y: -10 * t };
  layer(g, cam, 0.2, (g) => { backdrop(g, M.sky); FX.sun(g, E.W / 2, E.H * 0.64, 100, '#fff3dc', M.key, 5); FX.godRays(g, E.W / 2, E.H * 0.64, { count: 14, angle: -Math.PI / 2, spread: Math.PI * 1.6, len: 1800, a: 0.06, t }); });
  layer(g, cam, 0.5, (g) => FX.skyline(g, { x: -200, y: E.H * 0.76, w: E.W + 400, maxH: 320, color: '#2a1f36', windowColor: alpha(M.practical, 0.8), seed: 21 }));
  layer(g, cam, 0.8, (g) => { g.fillStyle = '#16111e'; g.fillRect(-E.W, E.H * 0.76, E.W * 3, E.H); });
  P.archive(g, t, { z: 1, x: 0 }, { count: 14, speed: 0.6 }); veil(g, '#120a14', 0.25);
  UI.titleCard(g, t, { lines: info.lines || ['ماذا لو', 'تذكرت كل ثانية من حياتك؟'], dur: info.dur, y: E.H * 0.4 });
}
export function bigline(g, t, info) {
  const cam = camOf(t, info); blurLayer(g, 10, (g) => drawSet(g, t, info, cam)); veil(g, '#0c0810', 0.5);
  UI.bigLine(g, t, { str: info.str, dur: info.dur, y: E.H * (info.y ?? 0.45), size: info.size || 84, color: info.coral ? CORAL() : GOLD() });
  if (info.str2) text(g, info.str2, E.W / 2, E.H * 0.6, { size: 54, color: CREAM(), weight: 700, alpha: ease.out(prog(t, info.at2 ?? 1, (info.at2 ?? 1) + 0.4)) });
  FX.dust(g, t, { count: 30, a: 0.3 });
}
export function endscreen(g, t, info) {
  UI.endScreen(g, t, { question: info.q || 'ما رأيك؟', cast: (info.cast || ['SALMA', 'MOM', 'YOU', 'LAYLA', 'ADAM', 'MAYA']).map(n => CAST[n]) });
}

// ---------- 8. MAP: the crisis — places flashing, countdown ----------
export function places(g, t, info) {
  UI.blueprint(g); const c = UI.bpStroke(), gold = GOLD(), cx = E.W / 2, cy = E.H * 0.52;
  g.strokeStyle = alpha(c, 0.25); g.lineWidth = 3; for (let i = -6; i <= 6; i++) { seg(g, [[cx + i * 150, 60], [cx + i * 150 + 80, E.H - 60]], 3, alpha(c, 0.18)); seg(g, [[100, cy + i * 90], [E.W - 100, cy + i * 90 - 40]], 3, alpha(c, 0.18)); }
  const pins = info.pins || [['البيت', 0.5, 0.55]];
  const N = info.many ? 120 : 0; for (let i = 0; i < N; i++) { const x = 140 + (i * 151) % (E.W - 280), y = 120 + (i * 97) % (E.H - 260), on = ((i * 7 + Math.floor(t * 6)) % 11) < 2 && t > (i / N) * (info.dur * 0.6); circle(g, x, y, 7, on ? gold : alpha(c, 0.35)); if (on) glow(g, x, y, 30, gold, 0.5); }
  pins.forEach(([s, px, py, at = 0], i) => { const a = ease.outBack(prog(t, at, at + 0.35)); if (a <= 0) return; const x = E.W * px, y = E.H * py; circle(g, x, y, 16 * a, info.home === i ? CREAM() : gold); glow(g, x, y, 70, gold, 0.4 * a); text(g, s, x, y - 50, { size: 44, color: CREAM(), weight: 900, alpha: a }); });
  if (info.timer) { const rem = info.timer[0] - (info.timer[1] ?? 1) * t / 60; text(g, `${Math.max(0, Math.ceil(rem))} دقيقة على الغروب`, E.W - 120, 110, { size: 50, color: CORAL(), weight: 900, align: 'right', glow: 16, glowColor: alpha(CORAL(), 0.6) }); }
  overlays(g, t, info);
}

// ---------- 9. CONTRAST split: grandma forgets vs you remember ----------
export function split(g, t, info) {
  const M = mood('interiorWarm'); backdrop(g, ['#1a1218', '#2a1e24']);
  g.save(); g.beginPath(); g.rect(0, 0, E.W / 2 - 4, E.H); g.clip(); blurLayer(g, 8, (g) => P.home(g, t, { z: 1.3, x: 300, y: -60 })); veil(g, '#0c0810', 0.45);
  bigFace(g, E.W * 0.25, E.H * 0.62, 230, { outfit: CAST.LAYLA, expr: 'confused', rimColor: M.rim, rimSide: 1, look: [0.3, -0.3] });
  for (let i = 0; i < 6; i++) { const a = prog(t, i * 0.4, i * 0.4 + 1.6); g.globalAlpha = 0.6 * (1 - a); rr(g, E.W * 0.12 + (i % 3) * 120, E.H * 0.18 - a * 120, 90, 60, 8); g.fillStyle = '#ffd47e'; g.fill(); g.globalAlpha = 1; } g.restore();
  g.save(); g.beginPath(); g.rect(E.W / 2 + 4, 0, E.W / 2, E.H); g.clip(); P.archive(g, t, { z: 1, x: 0 }, { count: 30, speed: 0.8 });
  bigFace(g, E.W * 0.75, E.H * 0.62, 230, { outfit: CAST.YOU, expr: 'sad', rimColor: '#ffd47e', rimSide: -1 }); g.restore();
  seg(g, [[E.W / 2, 0], [E.W / 2, E.H]], 6, '#0a070c'); overlays(g, t, info);
}

// ---------- 10. FREEZE: the memory replay moment (flash in) ----------
export function freeze(g, t, info) {
  const cam = { z: 1 + 0.03 * t, r: -0.02 + 0.01 * t };
  blurLayer(g, 10, (g) => drawSet(g, 0, info, { z: 1.4, x: -60, y: -100 })); veil(g, '#0c0810', 0.35);
  layer(g, cam, 1, (g) => { FX.drops(g, t, { count: 60, color: '#d8e4ff', rMax: 9, drift: 2 }); const M = mood('interiorWarm');
    bigFace(g, E.W / 2, E.H * 0.6, 300, { outfit: CAST[info.who || 'YOU'], expr: seqVal(t, info.expr, 'sad'), rimColor: M.rim, rimSide: -1 });
    FX.rings(g, E.W / 2, E.H * 0.55, t, { count: 3, r0: 340, r1: 700, speed: 0.35, color: '#e8f0ff', a: 0.35 }); });
  g.save(); g.globalCompositeOperation = 'soft-light'; g.fillStyle = 'rgba(80,120,255,.35)'; g.fillRect(0, 0, E.W, E.H); g.restore();
  overlays(g, t, info);
}

// ---------- overlays shared by every template: labels, readouts, badges ----------
function overlays(g, t, info) {
  for (const L of info.labels || []) { const at = L.at ?? 0.3, a = ease.out(prog(t, at, at + 0.35)) * (L.out ? 1 - prog(t, L.out, L.out + 0.3) : 1); if (a <= 0) continue;
    const x = E.W * (L.x ?? 0.5), y = E.H * (L.y ?? 0.2), sz = L.size || 64; g.save(); g.globalAlpha *= a; g.translate(x, y); const s = 0.8 + 0.2 * ease.outBack(prog(t, at, at + 0.35)); g.scale(s, s);
    if (L.box) { const w = measure(g, L.s, sz, FONTS.ui, 900) + 60; rr(g, -w / 2, -sz * 0.75, w, sz * 1.5, 18); g.fillStyle = 'rgba(14,18,34,.82)'; g.fill(); g.strokeStyle = alpha(L.coral ? CORAL() : GOLD(), 0.7); g.lineWidth = 3; g.stroke(); }
    text(g, L.s, 0, 0, { size: sz, color: L.coral ? CORAL() : L.cream ? CREAM() : GOLD(), weight: 900, glow: 18, glowColor: 'rgba(0,0,0,.6)' }); g.restore(); }
  if (info.badge) UI.badge(g, { str: info.badge, a: ease.out(prog(t, 0.2, 0.6)), size: 52 });
  if (info.clock) { const [h, m] = info.clock; const a = ease.out(prog(t, 0.2, 0.5)); g.save(); g.globalAlpha *= a; rr(g, 80, 70, 280, 100, 18); g.fillStyle = 'rgba(14,18,34,.8)'; g.fill(); text(g, `${h}:${String(m).padStart(2, '0')}`, 220, 122, { size: 64, color: GOLD(), weight: 900, font: FONTS.ui }); g.restore(); }
}

export const TPL = { stage, face, insert, data, curve, archive, title, bigline, endscreen, places, split, freeze };
