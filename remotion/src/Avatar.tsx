import { useEffect, useLayoutEffect, useRef, useState } from "react";
import { continueRender, delayRender, staticFile, useCurrentFrame, useVideoConfig } from "remotion";

// Per-frame voice loudness (0..1) at 30fps, precomputed from voiceover.mp3.
type Envelope = number[];

// Jaw region of avatar.jpg (1024x1024 source pixels) that is warped to open the mouth.
const RX0 = 430;
const RX1 = 590;
const YS = 416; // just under the upper teeth
const YE = 520; // chin
const TOP = 380;
const EYES: [number, number][] = [
  [455, 289],
  [571, 289],
];

// 1 across the middle of the mouth, easing to 0 at the corners.
const mouthWidth = (x: number) => {
  const c = 511;
  const half = 22;
  const fall = 44;
  const dx = Math.abs(x - c);
  if (dx <= half) return 1;
  if (dx >= half + fall) return 0;
  return 0.5 + 0.5 * Math.cos((Math.PI * (dx - half)) / fall);
};

const blinkAmount = (t: number) => {
  const period = 3.7;
  const ph = (t + 0.9 * Math.sin(t * 0.37)) % period;
  const d = ph - (period - 0.18);
  return d > 0 ? Math.sin((Math.PI * d) / 0.18) : 0;
};

type Prepared = { work: HTMLCanvasElement; base: HTMLCanvasElement; jaw: ImageData; env: Envelope };

export const Avatar: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const canvas = useRef<HTMLCanvasElement>(null);
  const [prepared, setPrepared] = useState<Prepared | null>(null);
  const [handle] = useState(() => delayRender("Loading avatar"));

  useEffect(() => {
    const img = new Image();
    img.src = staticFile("avatar.jpg");
    Promise.all([
      img.decode(),
      fetch(staticFile("mouth-envelope.json")).then((r) => r.json() as Promise<Envelope>),
    ]).then(([, env]) => {
      const base = document.createElement("canvas");
      base.width = base.height = 1024;
      const bctx = base.getContext("2d")!;
      bctx.drawImage(img, 0, 0);
      const work = document.createElement("canvas");
      work.width = work.height = 1024;
      setPrepared({ base, work, env, jaw: bctx.getImageData(RX0, TOP, RX1 - RX0, YE - TOP) });
      continueRender(handle);
    });
  }, [handle]);

  useLayoutEffect(() => {
    if (!prepared || !canvas.current) return;
    const { base, work, jaw, env } = prepared;
    const t = frame / fps;
    const open = env[Math.min(env.length - 1, frame)] ?? 0;
    const D = open > 0.12 ? 12 * open : 0; // jaw drop in source px

    const wctx = work.getContext("2d")!;
    wctx.drawImage(base, 0, 0);

    if (D > 0) {
      const W = RX1 - RX0;
      const H = YE - TOP;
      const out = wctx.createImageData(W, H);
      const sd = jaw.data;
      const od = out.data;
      od.set(sd);
      for (let x = 0; x < W; x++) {
        const d = D * mouthWidth(RX0 + x);
        if (d < 0.2) continue;
        for (let y = YS - TOP; y < H; y++) {
          const yy = y + TOP;
          const sy = yy - (d * (YE - yy)) / (YE - YS);
          const i = (y * W + x) * 4;
          if (sy < YS) {
            // inside of the open mouth
            const k = (YS - sy) / Math.max(d, 1);
            od[i] = 22 + 30 * k;
            od[i + 1] = 8 + 6 * k;
            od[i + 2] = 9 + 6 * k;
          } else {
            const y0 = Math.floor(sy) - TOP;
            const f = sy - Math.floor(sy);
            const a = (y0 * W + x) * 4;
            const b = ((y0 + 1) * W + x) * 4;
            for (let c = 0; c < 3; c++) od[i + c] = sd[a + c] * (1 - f) + sd[b + c] * f;
          }
          od[i + 3] = 255;
        }
      }
      wctx.putImageData(out, RX0, TOP);
    }

    const bl = blinkAmount(t);
    if (bl > 0.01) {
      for (const [ex, ey] of EYES) {
        wctx.save();
        wctx.beginPath();
        wctx.ellipse(ex, ey, 30, 14, 0, 0, Math.PI * 2);
        wctx.clip();
        const lid = ey - 14 + 28 * bl;
        const g = wctx.createLinearGradient(0, ey - 14, 0, lid);
        g.addColorStop(0, "rgb(150,92,72)");
        g.addColorStop(1, "rgb(172,106,84)");
        wctx.fillStyle = g;
        wctx.fillRect(ex - 32, ey - 16, 64, lid - (ey - 16));
        wctx.fillStyle = "rgba(40,20,15,0.85)";
        wctx.fillRect(ex - 32, lid - 2, 64, 3);
        wctx.restore();
      }
    }

    // idle head sway, a little livelier while speaking
    const rot = 0.008 * Math.sin(t * 0.9) + 0.006 * open * Math.sin(t * 5.3);
    const bob = 5 * Math.sin(t * 1.3) + 4 * open;
    const ctx = canvas.current.getContext("2d")!;
    ctx.fillStyle = "#07070c";
    ctx.fillRect(0, 0, 1080, 1080);
    ctx.save();
    ctx.translate(540, 700 + bob);
    ctx.rotate(rot);
    ctx.scale(1.12, 1.12);
    ctx.drawImage(work, -512, -660);
    ctx.restore();
  }, [prepared, frame, fps]);

  return (
    <div
      style={{
        position: "absolute",
        left: 0,
        top: 890,
        width: 1080,
        height: 1030,
        overflow: "hidden",
        WebkitMaskImage: "linear-gradient(to bottom, transparent 0, #000 110px)",
      }}
    >
      <canvas ref={canvas} width={1080} height={1080} />
    </div>
  );
};
