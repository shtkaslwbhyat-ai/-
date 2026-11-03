import React from "react";
import { AbsoluteFill, random, useCurrentFrame, useVideoConfig } from "remotion";

// A stylised "generated" film shot built entirely in SVG/CSS: a rider crossing dunes at sunset.
export type Camera = {
  zoom?: number; // 1 = wide
  panX?: number; // px, positive moves the view right
  rise?: number; // px, positive lifts the camera (drone)
  tilt?: number; // deg
};
export type FilmLook = "clean" | "35mm" | "8mm";

const LOOK_FILTER: Record<FilmLook, string> = {
  clean: "none",
  "35mm": "saturate(1.15) contrast(1.05) sepia(.12)",
  "8mm": "sepia(.55) saturate(.9) contrast(1.15) brightness(.95)",
};

const dune = (w: number, h: number, base: number, amp: number, phase: number) => {
  const pts: string[] = [`M0 ${h}`, `L0 ${base}`];
  for (let x = 0; x <= w; x += 40) {
    const y = base - amp * Math.sin((x / w) * Math.PI * 2 + phase) - amp * 0.4 * Math.sin((x / w) * Math.PI * 5 + phase * 2);
    pts.push(`L${x} ${y.toFixed(1)}`);
  }
  pts.push(`L${w} ${h}`, "Z");
  return pts.join(" ");
};

export const DesertScene: React.FC<{
  w: number;
  h: number;
  camera?: Camera;
  look?: FilmLook;
  letterbox?: boolean;
  style?: React.CSSProperties;
}> = ({ w, h, camera = {}, look = "35mm", letterbox = true, style }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  const { zoom = 1, panX = 0, rise = 0, tilt = 0 } = camera;
  const W = 1400;
  const H = 2000;
  const riderX = ((t * 70) % (W + 300)) - 150;
  const jitter = look === "8mm" ? (random(`j${frame}`) - 0.5) * 6 : 0;

  const layer = (depth: number, children: React.ReactNode) => (
    <g transform={`translate(${-panX * depth} ${rise * depth})`}>{children}</g>
  );

  return (
    <div style={{ position: "relative", width: w, height: h, overflow: "hidden", background: "#1a0f2e", ...style }}>
      <div
        style={{
          position: "absolute",
          inset: 0,
          transform: `translateY(${jitter}px) scale(${zoom}) rotate(${tilt}deg)`,
          transformOrigin: "55% 68%",
          filter: LOOK_FILTER[look],
        }}
      >
        <svg viewBox={`0 0 ${W} ${H}`} preserveAspectRatio="xMidYMid slice" width="100%" height="100%">
          <defs>
            <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0" stopColor="#2b1055" />
              <stop offset="0.45" stopColor="#d1416b" />
              <stop offset="0.7" stopColor="#ff9a3c" />
              <stop offset="1" stopColor="#ffd28a" />
            </linearGradient>
            <radialGradient id="sun">
              <stop offset="0" stopColor="#fff4c2" />
              <stop offset="0.35" stopColor="#ffd36b" />
              <stop offset="1" stopColor="rgba(255,160,60,0)" />
            </radialGradient>
          </defs>
          <rect width={W} height={H} fill="url(#sky)" />
          {layer(0.1, <circle cx={W * 0.62} cy={H * 0.56} r={420} fill="url(#sun)" />)}
          {layer(0.1, <circle cx={W * 0.62} cy={H * 0.56} r={130} fill="#fff1c9" />)}
          {layer(0.3, <path d={dune(W + 400, H, H * 0.64, 60, 0.6)} fill="#b4502f" transform="translate(-200 0)" />)}
          {layer(0.6, <path d={dune(W + 600, H, H * 0.72, 80, 2.1)} fill="#7a2f22" transform="translate(-300 0)" />)}
          {layer(
            0.8,
            <text x={riderX} y={H * 0.715} fontSize={150} style={{ filter: "brightness(0)" }}>
              🏇
            </text>
          )}
          {layer(1, <path d={dune(W + 800, H, H * 0.82, 70, 4)} fill="#3d1414" transform="translate(-400 0)" />)}
          {/* drifting dust */}
          {Array.from({ length: 24 }, (_, i) => {
            const x = (random(`dx${i}`) * W + t * (20 + random(`ds${i}`) * 40)) % W;
            const y = H * (0.55 + random(`dy${i}`) * 0.35);
            return <circle key={i} cx={x} cy={y} r={2 + random(`dr${i}`) * 4} fill="rgba(255,220,170,.35)" />;
          })}
        </svg>
      </div>
      {/* grain + vignette */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          opacity: look === "clean" ? 0.04 : look === "8mm" ? 0.16 : 0.08,
          backgroundImage: "repeating-radial-gradient(circle at 17% 32%, #fff 0 1px, transparent 1px 3px)",
          backgroundPosition: `${(frame * 37) % 100}px ${(frame * 53) % 100}px`,
          mixBlendMode: "overlay",
        }}
      />
      <div style={{ position: "absolute", inset: 0, boxShadow: `inset 0 0 ${look === "8mm" ? 260 : 160}px rgba(0,0,0,.75)` }} />
      {letterbox && (
        <>
          <div style={{ position: "absolute", left: 0, right: 0, top: 0, height: h * 0.1, background: "#000" }} />
          <div style={{ position: "absolute", left: 0, right: 0, bottom: 0, height: h * 0.1, background: "#000" }} />
        </>
      )}
    </div>
  );
};

// Camera viewfinder overlay: corner brackets, REC, timecode.
export const Viewfinder: React.FC<{ w: number; h: number; label?: string }> = ({ w, h, label = "4K · 24fps" }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const secs = Math.floor(frame / fps);
  const tc = `00:00:${String(secs).padStart(2, "0")}:${String(frame % fps).padStart(2, "0")}`;
  const b = (pos: React.CSSProperties, r: string) => (
    <div style={{ position: "absolute", width: 90, height: 90, ...pos, border: "6px solid rgba(255,255,255,.85)", borderRadius: r }} />
  );
  return (
    <div style={{ position: "absolute", inset: 0, width: w, height: h, pointerEvents: "none", direction: "ltr" }}>
      {b({ top: 40, left: 40, borderRight: "none", borderBottom: "none" }, "12px 0 0 0")}
      {b({ top: 40, right: 40, borderLeft: "none", borderBottom: "none" }, "0 12px 0 0")}
      {b({ bottom: 40, left: 40, borderRight: "none", borderTop: "none" }, "0 0 0 12px")}
      {b({ bottom: 40, right: 40, borderLeft: "none", borderTop: "none" }, "0 0 12px 0")}
      <div style={{ position: "absolute", top: 70, left: 150, display: "flex", alignItems: "center", gap: 14, fontSize: 36, fontWeight: 900, color: "#fff" }}>
        <span style={{ width: 26, height: 26, borderRadius: "50%", background: "#ff3b3b", opacity: frame % 30 < 18 ? 1 : 0.2 }} />
        REC
      </div>
      <div style={{ position: "absolute", top: 72, right: 150, fontSize: 32, fontWeight: 700, color: "#fff", fontFamily: "monospace" }}>{tc}</div>
      <div style={{ position: "absolute", bottom: 72, right: 150, fontSize: 30, fontWeight: 700, color: "rgba(255,255,255,.85)" }}>{label}</div>
    </div>
  );
};
