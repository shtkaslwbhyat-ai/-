# Synthesizes a music bed + sound effects for an ad, mixed to one stereo WAV.
import numpy as np, wave, sys, json
SR = 44100
rng = np.random.default_rng(7)

def env(n, a=0.005, r=0.2):
    t = np.arange(n) / SR
    e = np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / max(r, 1e-4))
    return e

def lowpass(x, cutoff):
    # one-pole lowpass, cutoff may be array
    y = np.zeros_like(x); a = np.exp(-2 * np.pi * np.broadcast_to(cutoff, x.shape) / SR); p = 0.0
    for i in range(len(x)):
        p = (1 - a[i]) * x[i] + a[i] * p; y[i] = p
    return y

def whoosh(d=0.6, up=True):
    n = int(d * SR); t = np.linspace(0, 1, n)
    noise = rng.standard_normal(n)
    cut = (300 + 6000 * (t if up else 1 - t) ** 2)
    shape = np.sin(np.pi * t) ** 2
    return lowpass(noise, cut) * shape * 0.9

def impact(d=0.9, f0=70):
    n = int(d * SR); t = np.arange(n) / SR
    f = f0 * (1 + 2.5 * np.exp(-t * 18))
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 5)
    click = rng.standard_normal(n) * np.exp(-t * 60) * 0.4
    return (body + lowpass(click, 2500)) * 0.9

def pop(f=900):
    n = int(0.18 * SR); t = np.arange(n) / SR
    fr = f * (1 + 1.5 * np.exp(-t * 40))
    return np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t * 28) * 0.5

def shimmer(d=1.4):
    n = int(d * SR); t = np.arange(n) / SR; out = np.zeros(n)
    for k, f in enumerate([2093, 2637, 3136, 3951, 4186, 5274]):
        st = int(k * 0.07 * SR)
        tt = t[: n - st]
        out[st:] += np.sin(2 * np.pi * f * tt) * np.exp(-tt * 4) * 0.12
    return out

def crackle(d=0.8):
    n = int(d * SR); out = np.zeros(n)
    for _ in range(26):
        p = rng.integers(0, n - 2000); L = rng.integers(200, 1500)
        out[p:p + L] += rng.standard_normal(L) * np.exp(-np.arange(L) / (L / 4)) * rng.uniform(.2, .7)
    return lowpass(out, 3500) * 1.2

def drop():
    n = int(0.35 * SR); t = np.arange(n) / SR
    f = 400 + 900 * np.exp(-t * 14)
    return np.sin(2 * np.pi * np.cumsum(f[::-1][::-1]) / SR) * np.exp(-t * 12) * 0.5

def riser(d=1.5):
    n = int(d * SR); t = np.linspace(0, 1, n)
    f = 200 + 1400 * t ** 2
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.25
    return (tone + lowpass(rng.standard_normal(n), 800 + 5000 * t) * 0.5) * t ** 1.5

def music(total, bpm=100, chords=None, mood="bright"):
    n = int(total * SR); t = np.arange(n) / SR; out = np.zeros(n)
    beat = 60 / bpm; bar = beat * 4
    chords = chords or [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]]  # Am F C G (midi)
    mtof = lambda m: 440 * 2 ** ((m - 69) / 12)
    # pad
    for i in range(int(total / bar) + 1):
        ch = chords[i % len(chords)]; s = int(i * bar * SR); e = min(n, int((i + 1) * bar * SR) + int(0.3 * SR))
        if s >= n: break
        tt = np.arange(e - s) / SR
        a = np.minimum(1, tt / 0.6) * np.minimum(1, (e - s) / SR - tt + 0.01)
        for m in ch:
            for det in (-0.08, 0.08):
                out[s:e] += np.sin(2 * np.pi * mtof(m) * (1 + det / 100) * tt) * a * 0.035
        # pluck arpeggio, 8th notes
        for j in range(8):
            ps = s + int(j * beat / 2 * SR)
            if ps >= n: break
            L = min(int(0.4 * SR), n - ps); tt2 = np.arange(L) / SR
            m = ch[j % 3] + 12 + (12 if j in (3, 7) else 0)
            out[ps:ps + L] += (np.sin(2 * np.pi * mtof(m) * tt2) + 0.3 * np.sin(4 * np.pi * mtof(m) * tt2)) * np.exp(-tt2 * 9) * 0.05
        # soft kick + hat
        for j in range(4):
            ks = s + int(j * beat * SR)
            if ks < n:
                L = min(int(0.25 * SR), n - ks); tt3 = np.arange(L) / SR
                out[ks:ks + L] += np.sin(2 * np.pi * (50 + 80 * np.exp(-tt3 * 30)) * tt3) * np.exp(-tt3 * 12) * 0.22
            hs = s + int((j + 0.5) * beat * SR)
            if hs < n:
                L = min(int(0.05 * SR), n - hs)
                out[hs:hs + L] += rng.standard_normal(L) * np.exp(-np.arange(L) / (0.01 * SR)) * 0.03
    return out

FX = dict(whoosh=whoosh, whoosh_down=lambda: whoosh(0.6, False), impact=impact, pop=pop, shimmer=shimmer,
          crackle=crackle, drop=drop, riser=riser, pop_hi=lambda: pop(1300))

def build(spec_path, out_path):
    spec = json.load(open(spec_path))
    total = spec["seconds"]; n = int(total * SR)
    mix = np.zeros(n)
    if spec.get("music", True):
        m = music(total, spec.get("bpm", 100))
        # duck music in the first beat (hook) and fade at end
        fade = np.ones(n); fo = int(1.2 * SR); fade[-fo:] = np.linspace(1, 0, fo)
        fi = int(spec.get("music_in", 0) * SR)
        fade[:fi] = 0
        if fi: fade[fi:fi + int(0.4 * SR)] *= np.linspace(0, 1, int(0.4 * SR))
        mix += m * fade * spec.get("music_gain", 1.0)
    for ev in spec["events"]:
        snd = FX[ev["fx"]]() * ev.get("gain", 1.0)
        s = int(ev["t"] * SR); e = min(n, s + len(snd))
        if s < n: mix[s:e] += snd[: e - s]
    mix = np.tanh(mix * 1.4) * 0.85
    st = np.stack([mix, np.roll(mix, 30)], axis=1)
    pcm = (st * 32767).astype(np.int16)
    with wave.open(out_path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())

if __name__ == "__main__":
    build(sys.argv[1], sys.argv[2])
