import React from "react";
import { AbsoluteFill, Audio, Img, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { fontFamily } from "../theme";

// 15s vertical social ad — trendy, kinetic. Real jar photo for exact branding; AI macro for texture.
export const C = { green: "#5DB247", deep: "#1F6E3A", mint: "#E7F3E4", cream: "#FFFFFF", ink: "#0F2A1A", blue: "#1B5FAA" };
const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const S = (f: number, fps: number, d = 12) => spring({ frame: f, fps, config: { damping: d } });

/* 1 — HOOK: dry, tight skin. Text cracks open. */
const Hook: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const zoom = interpolate(f, [0, 8], [1.8, 1], clamp);
  const shake = f < 10 ? Math.sin(f * 4) * (10 - f) * 2 : 0;
  const crack = interpolate(f, [18, 40], [0, 1], clamp);
  const sub = S(f - 30, fps);
  return (
    <AbsoluteFill style={{ background: "radial-gradient(circle at 50% 40%, #3b2f27, #120d0a 75%)", alignItems: "center", justifyContent: "center" }}>
      <svg width="1080" height="1920" style={{ position: "absolute", opacity: 0.55 }}>
        {[["540,900 470,760 520,640 430,470", 0], ["540,900 640,780 610,620 700,430", 0.1], ["540,900 420,1010 460,1180 360,1380", 0.2], ["540,900 660,1040 620,1220 720,1450", 0.3]].map(([pts, d], i) => (
          <polyline key={i} points={pts as string} fill="none" stroke="#c9b6a3" strokeWidth={5} strokeDasharray={1200} strokeDashoffset={1200 * (1 - Math.max(0, Math.min(1, (crack - (d as number)) / 0.7)))} />
        ))}
      </svg>
      <div style={{ transform: `scale(${zoom}) translateX(${shake}px)`, textAlign: "center", color: "white" }}>
        <div style={{ fontSize: 120, fontWeight: 900, lineHeight: 1.15 }}>بشرتك<br />تشد وتجف؟</div>
      </div>
      <div style={{ position: "absolute", bottom: 420, fontSize: 52, color: "#d8c9bb", fontWeight: 700, opacity: sub, transform: `translateY(${(1 - sub) * 30}px)` }}>
        المكيّف، الشمس، والماء الحار... 🥵
      </div>
    </AbsoluteFill>
  );
};

/* 2 — TEXTURE + 48h counter */
const Texture: React.FC<{ dur: number }> = ({ dur }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const reveal = interpolate(f, [0, 14], [0, 1], clamp);
  const zoom = interpolate(f, [0, dur], [1.15, 1.35]);
  const n = Math.round(interpolate(f, [12, dur * 0.7], [0, 48], clamp));
  const t = S(f - 10, fps, 11);
  return (
    <AbsoluteFill style={{ background: C.mint }}>
      <AbsoluteFill style={{ clipPath: `circle(${reveal * 120}% at 50% 55%)` }}>
        <Img src={staticFile("cetaphil/cream.png")} style={{ position: "absolute", height: "100%", left: "50%", transform: `translateX(-50%) scale(${zoom})`, transformOrigin: "50% 60%" }} />
        <AbsoluteFill style={{ background: "linear-gradient(180deg, rgba(231,243,228,.92) 0%, rgba(231,243,228,0) 38%, rgba(231,243,228,0) 70%, rgba(231,243,228,.85) 100%)" }} />
      </AbsoluteFill>
      <div style={{ position: "absolute", top: 210, left: 0, right: 0, textAlign: "center", color: C.ink, transform: `scale(${0.7 + t * 0.3})`, opacity: t }}>
        <div style={{ fontSize: 60, fontWeight: 700 }}>ترطيب يدوم</div>
        <div style={{ fontSize: 300, fontWeight: 900, lineHeight: 1, color: C.deep, direction: "ltr" }}>{n}</div>
        <div style={{ fontSize: 80, fontWeight: 900 }}>ساعة 💧</div>
      </div>
    </AbsoluteFill>
  );
};

/* 3 — HERO: real jar drops in, light sweep, benefit chips */
const Hero: React.FC<{ dur: number }> = ({ dur }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const drop = S(f, fps, 9);
  const sweep = interpolate(f, [10, 40], [-60, 160], clamp);
  const chips = ["للبشرة الجافة جداً", "لطيف على البشرة الحساسة", "يرمّم حاجز البشرة"];
  const float = Math.sin(f / 14) * 10;
  return (
    <AbsoluteFill style={{ background: `radial-gradient(circle at 50% 45%, #ffffff 0%, ${C.mint} 45%, #cfe8c8 100%)`, alignItems: "center" }}>
      <div style={{ position: "absolute", top: 560, width: 700, height: 120, borderRadius: "50%", background: "rgba(31,110,58,.18)", filter: "blur(30px)", transform: `translateY(${560}px) scale(${drop})` }} />
      <div style={{ position: "absolute", top: 420, transform: `translateY(${(1 - drop) * -1200 + float}px) rotate(${(1 - drop) * -12}deg)`, width: 720 }}>
        <Img src={staticFile("cetaphil/jar.png")} style={{ width: "100%", filter: "drop-shadow(0 40px 50px rgba(15,42,26,.28))" }} />
        <div style={{ position: "absolute", inset: 0, WebkitMaskImage: `url(${staticFile("cetaphil/jar.png")})`, WebkitMaskSize: "100% 100%", background: `linear-gradient(100deg, transparent ${sweep - 20}%, rgba(255,255,255,.75) ${sweep}%, transparent ${sweep + 20}%)` }} />
      </div>
      <div style={{ position: "absolute", top: 1420, display: "flex", flexDirection: "column", gap: 22, alignItems: "center" }}>
        {chips.map((c, i) => {
          const s = S(f - Math.round(dur * 0.22) - i * 12, fps, 12);
          return (
            <div key={c} style={{ fontSize: 50, fontWeight: 900, color: "white", background: i === 1 ? C.blue : C.deep, padding: "16px 44px", borderRadius: 999, opacity: s, transform: `translateX(${(1 - s) * (i % 2 ? -300 : 300)}px)` }}>
              ✓ {c}
            </div>
          );
        })}
      </div>
      <div style={{ position: "absolute", top: 200, fontSize: 70, fontWeight: 900, color: C.ink, opacity: S(f - 6, fps) }}>كريم مرطّب يومي</div>
    </AbsoluteFill>
  );
};

/* 4 — END CARD */
const End: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = S(f, fps, 11);
  const t = S(f - 12, fps, 12);
  return (
    <AbsoluteFill style={{ background: `linear-gradient(170deg, ${C.green}, ${C.deep})`, alignItems: "center", justifyContent: "center", gap: 50 }}>
      <Img src={staticFile("cetaphil/jar.png")} style={{ width: 520, transform: `scale(${0.6 + s * 0.4}) rotate(${(1 - s) * 8}deg)`, filter: "drop-shadow(0 30px 40px rgba(0,0,0,.35))" }} />
      <div style={{ textAlign: "center", color: "white", opacity: t, transform: `translateY(${(1 - t) * 40}px)` }}>
        <div style={{ fontSize: 92, fontWeight: 900, lineHeight: 1.2 }}>بشرتك تستاهل<br />ترطيب يدوم</div>
        <div style={{ marginTop: 30, display: "inline-block", fontSize: 46, fontWeight: 900, background: "white", color: C.deep, padding: "14px 46px", borderRadius: 999 }}>متوفر الآن 🛒</div>
      </div>
    </AbsoluteFill>
  );
};

// Scene lengths in frames (30fps) — tuned to the voiceover.
export const AD15_SCENES = { hook: 75, texture: 105, hero: 150, end: 120 };
export const AD15_TOTAL = AD15_SCENES.hook + AD15_SCENES.texture + AD15_SCENES.hero + AD15_SCENES.end;

// Cut transition: punch-zoom out of the old scene + white flash + zoom into the new one.
const Cuts: React.FC<{ at: number[] }> = ({ at }) => {
  const f = useCurrentFrame();
  const o = Math.max(0, ...at.map((c) => interpolate(f, [c - 3, c, c + 7], [0, 0.9, 0], clamp)));
  return <AbsoluteFill style={{ background: "white", opacity: o, pointerEvents: "none" }} />;
};
const Punch: React.FC<{ len: number; children: React.ReactNode }> = ({ len, children }) => {
  const f = useCurrentFrame();
  const zin = interpolate(f, [0, 10], [1.12, 1], clamp);
  const zout = interpolate(f, [len - 6, len], [1, 1.18], clamp);
  const blur = interpolate(f, [len - 6, len], [0, 14], clamp) + interpolate(f, [0, 6], [10, 0], clamp);
  return <AbsoluteFill style={{ transform: `scale(${zin * zout})`, filter: `blur(${blur}px)` }}>{children}</AbsoluteFill>;
};

export const Ad15: React.FC<{ audio?: string | null }> = ({ audio = "cetaphil/sfx15.wav" }) => {
  const s = AD15_SCENES;
  const c1 = s.hook, c2 = s.hook + s.texture, c3 = s.hook + s.texture + s.hero;
  return (
    <AbsoluteFill style={{ fontFamily, direction: "rtl", background: "#000" }}>
      <Sequence durationInFrames={s.hook}><Punch len={s.hook}><Hook /></Punch></Sequence>
      <Sequence from={c1} durationInFrames={s.texture}><Punch len={s.texture}><Texture dur={s.texture} /></Punch></Sequence>
      <Sequence from={c2} durationInFrames={s.hero}><Punch len={s.hero}><Hero dur={s.hero} /></Punch></Sequence>
      <Sequence from={c3} durationInFrames={s.end}><Punch len={s.end + 10}><End /></Punch></Sequence>
      <Cuts at={[c1, c2, c3]} />
      {audio ? <Audio src={staticFile(audio)} /> : null}
    </AbsoluteFill>
  );
};
