#!/usr/bin/env python3
"""ORIGIN EMPIRE — sample video (typographic brand draft, no AI imagery).
Renders frames with PIL, synthesizes SFX with numpy, muxes with ffmpeg."""
import math, subprocess, sys, wave, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
VOICE = sys.argv[1]
OUT = sys.argv[2]
W, H, FPS = 1920, 1080, 25
O = 1.0                      # voice offset (s)
VO_DUR = 31.87
TOTAL = O + VO_DUR + 3.0

NAVY = (16, 26, 42); GOLD = (196, 154, 72); IVORY = (232, 229, 221)
STEEL = (82, 101, 121); CHAR = (23, 27, 34)

F = lambda n, s: ImageFont.truetype(os.path.join(HERE, "fonts", n), s, layout_engine=ImageFont.Layout.RAQM)
def playfair(s, w=700):
    f = ImageFont.truetype(os.path.join(HERE, "fonts", "Playfair.ttf"), s)
    try: f.set_variation_by_axes([w])
    except Exception: pass
    return f
INTER = "/usr/share/fonts/opentype/inter/Inter-Medium.otf"
inter = lambda s: ImageFont.truetype(INTER, s)

ar_bold = {s: F("PlexAr-Bold.ttf", s) for s in (100, 130, 150)}
ar_semi = {s: F("PlexAr-SemiBold.ttf", s) for s in (56, 60, 64, 70)}
ar_med = {s: F("PlexAr-Medium.ttf", s) for s in (26, 48, 54, 56)}

# ---------- background (precomputed) ----------
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
r = np.sqrt(((xx - W * 0.5) / (W * 0.62)) ** 2 + ((yy - H * 0.46) / (H * 0.70)) ** 2)
t = np.clip(r, 0, 1) ** 1.4
bg = (np.array(NAVY, np.float32) * (1 - t)[..., None] + np.array(CHAR, np.float32) * t[..., None])
bg *= (1 - 0.35 * np.clip(r - 0.75, 0, 1))[..., None]          # vignette
rng = np.random.default_rng(7)
grains = [rng.normal(0, 4.0, (H, W, 1)).astype(np.float32) for _ in range(6)]
glow_cache = {}

def background(fi, cold=0.0):
    a = bg + grains[fi % 6]
    if cold > 0:
        a = a * (1 - 0.16 * cold) + np.array(STEEL, np.float32) * 0.16 * cold
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGB").convert("RGBA")

def ease(x):  x = min(max(x, 0), 1); return x * x * (3 - 2 * x)
def fade(t, a, b, fi=0.5, fo=0.4):
    if t < a or t > b: return 0.0
    return ease((t - a) / fi) * ease((b - t) / fo)

def text(img, s, font, color, cx, cy, alpha, rtl=True, anchor="mm"):
    if alpha <= 0.003: return
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    kw = {"direction": "rtl", "language": "ar"} if rtl else {}
    d.text((cx, cy), s, font=font, fill=color + (int(255 * alpha),), anchor=anchor, **kw)
    img.alpha_composite(layer)

def spaced(img, s, font, color, cx, cy, alpha, track):
    if alpha <= 0.003: return
    widths = [font.getlength(c) for c in s]
    total = sum(widths) + track * (len(s) - 1)
    x = cx - total / 2
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    for c, w in zip(s, widths):
        d.text((x, cy), c, font=font, fill=color + (int(255 * alpha),), anchor="lm"); x += w + track
    img.alpha_composite(layer)

def line(img, x0, y0, x1, y1, color, alpha, width=3):
    if alpha <= 0.003: return
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(layer).line([(x0, y0), (x1, y1)], fill=color + (int(255 * alpha),), width=width)
    img.alpha_composite(layer)

def dot(img, x, y, rad, color, alpha):
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(layer).ellipse([x - rad, y - rad, x + rad, y + rad], fill=color + (int(255 * alpha),))
    img.alpha_composite(layer)

CX, CY = W // 2, H // 2
# scene windows (absolute seconds)
A = (1.0, 3.95); B = (4.0, 7.85); C = (7.9, 12.25); D = (12.3, 16.25)
E = (16.3, 19.25); Fs = (19.3, 28.65); G = (28.7, TOTAL + 1)
TICKS = [4.25 + i * 0.21 for i in range(10)]          # 1976 -> 1985 counter
WORDS = [(22.8, "قرارات"), (24.0, "أخطاء"), (25.2, "عودة")]

def frame(fi):
    t = fi / FPS
    cold = ease((t - E[0]) / 0.6) * (1 - ease((t - (E[1] - 0.3)) / 0.6))
    img = background(fi, cold)
    drift = lambda a: (t - a) * 6       # slow upward drift (px)

    # A — tagline
    a = fade(t, *A)
    text(img, "كلُّ ثروةٍ لها بداية", ar_bold[100], IVORY, CX, CY - 20 - drift(A[0]), a)
    half = 260 * ease((t - 1.6) / 1.2)
    line(img, CX - half, CY + 70, CX + half, CY + 70, GOLD, a * 0.9, 2)

    # B — year counter
    a = fade(t, *B)
    n = sum(1 for k in TICKS[1:] if t >= k)
    text(img, str(1976 + n), playfair(250), GOLD, CX, CY - 40, a, rtl=False)
    text(img, "تأسيس الشركة" if n == 0 else ("عام الخروج" if n == 9 else ""), ar_med[54], IVORY,
         CX, CY + 165, a * (0.85 if n in (0, 9) else 0))

    # C — Steve Jobs leaves
    a = fade(t, *C)
    spaced(img, "STEVE JOBS", inter(34), STEEL, CX, CY - 150, a, 14)
    text(img, "ستيف جوبز", ar_bold[130], IVORY, CX, CY - 40, a)
    text(img, "يغادر الشركة التي شارك في تأسيسها", ar_med[56], IVORY, CX, CY + 110, a * 0.85 * ease((t - 9.0) / 0.6))

    # D — timeline 1985 -> 1997 (right to left)
    a = fade(t, *D)
    if a > 0:
        xr, xl, ly = CX + 560, CX - 560, CY + 40
        line(img, xl, ly, xr, ly, STEEL, a * 0.8, 3)
        p = ease((t - 12.8) / 1.6)
        line(img, xr - (xr - xl) * p, ly, xr, ly, GOLD, a, 4)
        dot(img, xr, ly, 10, GOLD, a); dot(img, xl, ly, 10, GOLD if p >= 1 else STEEL, a)
        text(img, "1985", playfair(80), IVORY, xr, ly + 85, a, rtl=False)
        text(img, "1997", playfair(80), GOLD if p >= 1 else STEEL, xl, ly + 85, a, rtl=False)
        text(img, "نحو 12 عامًا", ar_semi[64], IVORY, CX, ly - 110, a * ease((t - 12.9) / 0.6))
        text(img, "العودة", ar_med[48], GOLD, xl, ly - 70, a * ease((t - 14.5) / 0.5))

    # E — crisis
    a = fade(t, *E)
    text(img, "أزمة حادّة", ar_bold[150], IVORY, CX, CY - 10, a)
    text(img, "1997", playfair(60, 500), STEEL, CX, CY - 170, a * 0.9, rtl=False)

    # F — not an infallible genius
    a = fade(t, *Fs)
    text(img, "ليست قصة عبقريٍّ لا يُخطئ", ar_semi[64], IVORY, CX, CY - 170, a * 0.9)
    xs = [CX + 380, CX, CX - 380]                       # RTL order
    for (ts, w), x in zip(WORDS, xs):
        wa = a * ease((t - ts) / 0.45)
        text(img, w, ar_bold[100], IVORY, x, CY + 10 + 18 * (1 - ease((t - ts) / 0.45)), wa)
    for x in (CX + 190, CX - 190):
        dot(img, x, CY + 20, 6, GOLD, a * ease((t - 24.0) / 0.4))
    text(img, "غيّرت صناعةً كاملة", ar_semi[60], GOLD, CX, CY + 180, a * ease((t - 26.4) / 0.6))

    # G — end card (placeholder wordmark; owner's logo replaces it)
    a = fade(t, *G, fi=0.9)
    if a > 0:
        spaced(img, "ORIGIN EMPIRE", playfair(118), GOLD, CX, CY - 60, a, 18)
        half = 380 * ease((t - 29.2) / 1.0)
        line(img, CX - half, CY + 30, CX + half, CY + 30, GOLD, a * 0.7, 2)
        spaced(img, "Every Fortune Has a Beginning.", inter(38), IVORY, CX, CY + 95, a * ease((t - 30.0) / 0.7), 2)
        text(img, "نروي القصة من بدايتها", ar_med[48], STEEL, CX, CY + 175, a * ease((t - 30.6) / 0.7))

    # persistent draft label
    text(img, "نسخة تجريبية للإيقاع والهوية — المشاهد ثلاثية الأبعاد تُضاف لاحقًا", ar_med[26], IVORY,
         W - 60, 55, 0.5 * ease(t / 0.8) * (1 - ease((t - TOTAL + 0.8) / 0.8)), anchor="rm")
    # fade from/to black
    k = ease(t / 0.6) * (1 - ease((t - TOTAL + 0.9) / 0.9))
    if k < 1:
        img = Image.blend(Image.new("RGBA", img.size, (0, 0, 0, 255)), img, k)
    return img.convert("RGB")

if os.environ.get("TEST"):
    for ts in map(float, os.environ["TEST"].split(",")):
        frame(int(ts * FPS)).save(os.path.join(HERE, f"test_{ts:05.1f}.png"))
    sys.exit(0)

# ---------- SFX (procedural, no music) ----------
SR = 44100
N = int(TOTAL * SR)
mix = np.zeros(N, np.float32)
tt = np.arange(N) / SR
def add(sig, at, gain):
    i = int(at * SR); j = min(N, i + len(sig)); mix[i:j] += gain * sig[: j - i]
def env_exp(d, tau): x = np.arange(int(d * SR)) / SR; return np.exp(-x / tau)
def lp(x, k): return np.convolve(x, np.ones(k) / k, mode="same")
def boom(freq, d, tau):
    x = np.arange(int(d * SR)) / SR
    f = freq * (1 + 0.6 * np.exp(-x / 0.08))
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-x / tau)
def noise(d): return rng.normal(0, 1, int(d * SR)).astype(np.float32)

# room tone
room = lp(lp(noise(TOTAL), 400), 200); room /= np.abs(room).max() + 1e-9
fadeenv = np.clip(tt / 1.5, 0, 1) * np.clip((TOTAL - tt) / 1.5, 0, 1)
mix += 0.035 * room[:N] * fadeenv
# opening low impact + air swell
sw = lp(noise(0.9), 30) * np.linspace(0, 1, int(0.9 * SR)) ** 2
add(sw / (np.abs(sw).max() + 1e-9), 0.0, 0.06)
add(boom(46, 2.5, 0.7), 0.85, 0.55)
# counter ticks (clock-like)
for k in TICKS:
    c = np.sin(2 * np.pi * 2300 * np.arange(int(0.03 * SR)) / SR) * env_exp(0.03, 0.006)
    c += 0.5 * noise(0.03) * env_exp(0.03, 0.002)
    add(c, k, 0.10)
add(boom(55, 1.5, 0.45), TICKS[-1], 0.30)          # land on 1985
# timeline whoosh
d = 1.6; ws = lp(noise(d), 18); e = np.sin(np.pi * np.linspace(0, 1, len(ws))) ** 2
add(ws * e / (np.abs(ws).max() + 1e-9), 12.6, 0.12)
# crisis dull hit
add(boom(58, 1.8, 0.5), E[0], 0.40)
add(lp(noise(1.2), 60) * env_exp(1.2, 0.3), E[0], 0.12)
# word beats
for ts, _ in WORDS: add(boom(90, 0.5, 0.09), ts, 0.16)
# end card: deep impact + metallic vault shimmer
add(boom(40, 3.0, 0.9), G[0], 0.60)
x = np.arange(int(3.0 * SR)) / SR
shim = sum(np.sin(2 * np.pi * f * x) * np.exp(-x / tau) for f, tau in ((1210, .9), (1873, .7), (2911, .5), (4130, .35)))
add(shim / 4 * np.clip(x / 0.01, 0, 1), G[0], 0.10)
mix = np.clip(mix, -1, 1)
sfx_path = os.path.join(HERE, "sfx.wav")
with wave.open(sfx_path, "wb") as wf:
    wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(SR)
    wf.writeframes((mix * 32767).astype(np.int16).tobytes())

# ---------- render video ----------
nframes = int(TOTAL * FPS)
silent = os.path.join(HERE, "video_silent.mp4")
p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                      "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium",
                      "-crf", "18", "-pix_fmt", "yuv420p", silent], stdin=subprocess.PIPE)
for fi in range(nframes):
    p.stdin.write(frame(fi).tobytes())
    if fi % 100 == 0: print("frame", fi, "/", nframes, flush=True)
p.stdin.close(); p.wait()

# ---------- mix & mux ----------
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", silent, "-i", VOICE, "-i", sfx_path,
    "-filter_complex",
    f"[1:a]adelay={int(O*1000)},aresample=48000,volume=1.0[v];"
    "[2:a]aresample=48000,volume=0.9[s];"
    "[v][s]amix=inputs=2:duration=longest:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=11[a]",
    "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", OUT], check=True)
print("done", OUT)
