import React from "react";
import { AbsoluteFill, Audio, Img, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { fontFamily } from "../theme";
import { Person, Sparkles } from "./People";
import { C } from "./Ad15";

// 30s 16:9 TV spot — flat-illustration family, real jar on the packshot. SFX only, no music.
const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const S = (f: number, fps: number, d = 12) => spring({ frame: f, fps, config: { damping: d } });
const FLOOR = 960;
const SKIN = { a: "#f1c7a3", b: "#d9a27a", c: "#c68863", d: "#e7b98f" };
const blinkAt = (f: number, off = 0) => (f + off) % 90 < 4;

const Super: React.FC<{ text: string; delay?: number }> = ({ text, delay = 8 }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = S(f - delay, fps, 14);
  return (
    <div style={{ position: "absolute", bottom: 70, right: 110, opacity: s, transform: `translateX(${(1 - s) * -60}px)` }}>
      <div style={{ fontSize: 64, fontWeight: 900, color: "white", background: C.deep, padding: "14px 44px", borderRadius: 22, boxShadow: "0 12px 30px rgba(0,0,0,.2)" }}>{text}</div>
    </div>
  );
};

/* backgrounds */
const Bedroom: React.FC = () => (
  <AbsoluteFill style={{ background: "#fdf3e7" }}>
    <div style={{ position: "absolute", left: 1280, top: 150, width: 420, height: 480, background: "#bfe3f7", border: "18px solid #fff", borderRadius: 16 }} />
    <div style={{ position: "absolute", left: 1250, top: 130, width: 120, height: 560, background: "#e8f3e4", borderRadius: 10 }} />
    <div style={{ position: "absolute", left: 1620, top: 130, width: 120, height: 560, background: "#e8f3e4", borderRadius: 10 }} />
    <div style={{ position: "absolute", left: 140, top: 640, width: 520, height: 320, background: "#9ccf8f", borderRadius: "40px 40px 0 0" }} />
    <div style={{ position: "absolute", left: 160, top: 600, width: 200, height: 90, background: "white", borderRadius: 40 }} />
    <div style={{ position: "absolute", left: 0, top: FLOOR, width: 1920, height: 120, background: "#e9d6bf" }} />
  </AbsoluteFill>
);
const Park: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{ background: "linear-gradient(#ffe6b8, #fff6e2 60%)" }}>
      <div style={{ position: "absolute", left: 1500, top: 110, width: 200, height: 200, borderRadius: 100, background: "#ffc547", boxShadow: `0 0 ${80 + Math.sin(f / 8) * 20}px #ffd166` }} />
      {[180, 420, 1500, 1720].map((x, i) => (
        <div key={x}>
          <div style={{ position: "absolute", left: x + 40, top: 560, width: 40, height: 400, background: "#8a5a3b", borderRadius: 10 }} />
          <div style={{ position: "absolute", left: x - 70, top: 380 + (i % 2) * 40, width: 260, height: 260, borderRadius: 130, background: i % 2 ? "#6cbf5a" : "#4fa64a" }} />
        </div>
      ))}
      <div style={{ position: "absolute", left: 0, top: FLOOR - 20, width: 1920, height: 140, background: "#8fcf73" }} />
      <div style={{ position: "absolute", left: 600, top: FLOOR - 10, width: 720, height: 130, background: "#e9cf9e", clipPath: "polygon(20% 0, 80% 0, 100% 100%, 0 100%)" }} />
    </AbsoluteFill>
  );
};
const Living: React.FC = () => (
  <AbsoluteFill style={{ background: "#f3efe6" }}>
    <div style={{ position: "absolute", left: 160, top: 180, width: 300, height: 220, background: "#d8ead3", border: "14px solid #b88b5e", borderRadius: 8 }} />
    <div style={{ position: "absolute", left: 1500, top: 300, width: 16, height: 660, background: "#555" }} />
    <div style={{ position: "absolute", left: 1430, top: 230, width: 160, height: 110, background: "#ffd98a", borderRadius: "80px 80px 10px 10px" }} />
    <div style={{ position: "absolute", left: 300, top: 700, width: 1300, height: 260, background: "#5d8fa8", borderRadius: "50px 50px 20px 20px" }} />
    <div style={{ position: "absolute", left: 0, top: FLOOR, width: 1920, height: 120, background: "#c9b08f" }} />
  </AbsoluteFill>
);
const Office: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{ background: "#eef3f6" }}>
      <div style={{ position: "absolute", left: 1250, top: 110, width: 460, height: 130, background: "white", borderRadius: 20, boxShadow: "0 8px 20px rgba(0,0,0,.08)" }}>
        <div style={{ position: "absolute", left: 30, bottom: 22, width: 400, height: 10, background: "#cfd8dc", borderRadius: 5 }} />
      </div>
      {[0, 1, 2].map((i) => (
        <div key={i} style={{ position: "absolute", left: 1320 + i * 120, top: 270 + ((f * 3 + i * 40) % 160), width: 70, height: 8, borderRadius: 4, background: "#9fd3f5", opacity: 1 - ((f * 3 + i * 40) % 160) / 160 }} />
      ))}
      <div style={{ position: "absolute", left: 1420, top: 150, fontSize: 70 }}>❄️</div>
      <div style={{ position: "absolute", left: 0, top: FLOOR, width: 1920, height: 120, background: "#cfd8dc" }} />
    </AbsoluteFill>
  );
};
const Desk: React.FC = () => (
  <>
    <div style={{ position: "absolute", left: 560, top: 780, width: 800, height: 36, background: "#b07a4f", borderRadius: 10 }} />
    <div style={{ position: "absolute", left: 600, top: 816, width: 720, height: 154, background: "#9a6a44" }} />
    <div style={{ position: "absolute", left: 1090, top: 650, width: 210, height: 130, background: "#37474f", borderRadius: 10 }} />
    <div style={{ position: "absolute", left: 1070, top: 770, width: 250, height: 14, background: "#263238", borderRadius: 6 }} />
  </>
);

/* 1 — OPENING: daily dryness */
const Open: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const icons = ["☀️", "❄️", "🚿"];
  const t = S(f - 40, fps, 13);
  const crack = interpolate(f, [55, 95], [0, 1], clamp);
  return (
    <AbsoluteFill style={{ background: "radial-gradient(circle at 50% 45%, #fff6ec, #f0dcc8)", alignItems: "center", justifyContent: "center" }}>
      <svg width="1920" height="1080" style={{ position: "absolute", opacity: 0.4 }}>
        {["960,540 880,420 930,300 850,160", "960,540 1060,430 1030,290 1120,140", "960,540 840,660 880,800 790,960", "960,540 1080,670 1040,820 1130,980"].map((p, i) => (
          <polyline key={i} points={p} fill="none" stroke="#b08968" strokeWidth={6} strokeDasharray={900} strokeDashoffset={900 * (1 - crack)} />
        ))}
      </svg>
      <div style={{ display: "flex", gap: 120, marginBottom: 60 }}>
        {icons.map((e, i) => {
          const s = S(f - i * 9, fps, 10);
          return <div key={e} style={{ fontSize: 150, transform: `scale(${s}) translateY(${Math.sin((f + i * 20) / 12) * 10}px)` }}>{e}</div>;
        })}
      </div>
      <div style={{ fontSize: 96, fontWeight: 900, color: "#4a3426", opacity: t, transform: `translateY(${(1 - t) * 40}px)` }}>
        كل يوم... بشرتنا تواجه <span style={{ color: "#b5651d" }}>الجفاف</span>
      </div>
    </AbsoluteFill>
  );
};

/* 2 — MOM + DAUGHTER */
const MomKid: React.FC<{ dur: number }> = ({ dur }) => {
  const f = useCurrentFrame();
  const reach = interpolate(f, [20, 45, dur - 30, dur - 10], [8, 29, 29, 10], clamp) + (f > 45 && f < dur - 30 ? Math.sin(f / 3) * 2 : 0);
  const touch = interpolate(f, [45, 90], [0, 1], clamp);
  return (
    <AbsoluteFill>
      <Bedroom />
      <Person x={820} y={FLOOR} size={1.15} skin={SKIN.b} hair="hijab" hairColor="#2e7d5b" shirt="#f7f7f2" pants="#6d8b74" armR={reach} armL={14} blink={blinkAt(f)} />
      <Person x={1000} y={FLOOR} size={0.62} skin={SKIN.a} hair="pony" hairColor="#3b2416" shirt="#ff9eb5" pants="#7986cb" armL={10} armR={14} blink={blinkAt(f, 30)} smile={1 + touch * 0.6} />
      <Sparkles x={975} y={672} t={touch} />
      <Super text="من أصغر فرد في العائلة..." />
    </AbsoluteFill>
  );
};

/* 3 — YOUNG MAN AFTER A RUN */
const Runner: React.FC<{ dur: number }> = ({ dur }) => {
  const f = useCurrentFrame();
  const rub = interpolate(f, [15, 35], [8, 22], clamp) + (f > 35 ? Math.sin(f / 2.2) * 4 : 0);
  const glow = interpolate(f, [50, 100], [0, 1], clamp);
  return (
    <AbsoluteFill>
      <Park />
      <Person x={960} y={FLOOR} size={1.2} skin={SKIN.c} hair="short" hairColor="#1d1d1d" beard shirt="#2196f3" pants="#263238" armL={-rub} armR={-rub} blink={blinkAt(f, 10)} sweat={f < 60} smile={0.6 + glow * 0.8} glowHands={glow * 0.8} />
      <Sparkles x={960} y={FLOOR - 720 + 354 * 1.2} t={interpolate(f, [60, 110], [0, 1], clamp)} />
      <Super text="لكل يوم مليان حركة..." />
    </AbsoluteFill>
  );
};

/* 4 — GRANDDAUGHTER + GRANDFATHER */
const Grandpa: React.FC<{ dur: number }> = ({ dur }) => {
  const f = useCurrentFrame();
  const g = interpolate(f, [10, 30], [8, 75], clamp);
  const girl = interpolate(f, [30, 55], [8, 82], clamp) + (f > 55 ? Math.sin(f / 3) * 3 : 0);
  const glow = interpolate(f, [60, 110], [0, 1], clamp);
  return (
    <AbsoluteFill>
      <Living />
      <Person x={800} y={FLOOR} size={1.1} skin={SKIN.d} hair="old" beard shirt="#8d6e63" pants="#4e342e" armR={g} armL={10} blink={blinkAt(f, 50)} smile={0.8 + glow * 0.7} />
      <Person x={1250} y={FLOOR} size={1.0} skin={SKIN.a} hair="long" hairColor="#4a2c1a" shirt="#7cc576" pants="#3f51b5" armL={girl} armR={12} blink={blinkAt(f, 20)} />
      <Sparkles x={1030} y={588} t={glow} color="#fff6c7" />
      <Super text="لين أكبر فرد فيها ❤️" />
    </AbsoluteFill>
  );
};

/* 5 — OFFICE, AC all day */
const OfficeWoman: React.FC<{ dur: number }> = () => {
  const f = useCurrentFrame();
  const rub = interpolate(f, [25, 42], [8, 22], clamp) + (f > 42 ? Math.sin(f / 2.2) * 4 : 0);
  const glow = interpolate(f, [55, 95], [0, 1], clamp);
  return (
    <AbsoluteFill>
      <Office />
      <Person x={840} y={FLOOR} size={1.1} skin={SKIN.b} hair="curly" hairColor="#2a1a12" shirt="#5c6bc0" pants="#37474f" armL={-rub} armR={-rub} blink={blinkAt(f, 5)} smile={0.4 + glow} glowHands={glow * 0.8} />
      <Desk />
      <Sparkles x={840} y={FLOOR - 660 + 354 * 1.1} t={interpolate(f, [60, 105], [0, 1], clamp)} />
      <Super text="حتى مع المكيّف طول اليوم" />
    </AbsoluteFill>
  );
};

/* 6 — WHOLE FAMILY + real jar */
const Family: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const jar = S(f - 10, fps, 10);
  const people = [
    { x: 330, size: 1.05, skin: SKIN.d, hair: "old" as const, beard: true, shirt: "#8d6e63", pants: "#4e342e" },
    { x: 610, size: 1.15, skin: SKIN.b, hair: "hijab" as const, hairColor: "#2e7d5b", shirt: "#f7f7f2", pants: "#6d8b74" },
    { x: 1310, size: 1.2, skin: SKIN.c, hair: "short" as const, hairColor: "#1d1d1d", beard: true, shirt: "#2196f3", pants: "#263238" },
    { x: 1560, size: 0.95, skin: SKIN.a, hair: "long" as const, hairColor: "#4a2c1a", shirt: "#7cc576", pants: "#3f51b5" },
    { x: 1760, size: 0.62, skin: SKIN.a, hair: "pony" as const, hairColor: "#3b2416", shirt: "#ff9eb5", pants: "#7986cb" },
  ];
  return (
    <AbsoluteFill>
      <Living />
      {people.map((p, i) => {
        const s = S(f - i * 4, fps, 12);
        return (
          <div key={i} style={{ position: "absolute", inset: 0, transform: `translateY(${(1 - s) * 200}px)`, opacity: s }}>
            <Person y={FLOOR} {...p} armL={10 + Math.sin(f / 6 + i) * 4} armR={i % 2 ? 150 + Math.sin(f / 4 + i) * 15 : 10} blink={blinkAt(f, i * 17)} smile={1.6} />
          </div>
        );
      })}
      <div style={{ position: "absolute", left: 960 - 190, top: 430, width: 380, transform: `scale(${jar}) translateY(${Math.sin(f / 10) * 8}px)` }}>
        <Img src={staticFile("cetaphil/jar.png")} style={{ width: "100%", filter: "drop-shadow(0 30px 30px rgba(0,0,0,.25))" }} />
      </div>
      <Sparkles x={960} y={600} t={interpolate(f, [15, 60], [0, 1], clamp)} color="#fff6c7" />
      <Super text="ترطيب واحد... للعائلة كلها" />
    </AbsoluteFill>
  );
};

/* 7 — PACKSHOT */
const Pack: React.FC<{ dur: number }> = ({ dur }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const jar = S(f, fps, 10);
  const sweep = interpolate(f, [8, 40], [-40, 140], clamp);
  const items = ["💧 ترطيب يدوم 48 ساعة", "🌿 لطيف على البشرة الحساسة", "🛡️ يرمّم حاجز البشرة"];
  const tag = S(f - Math.round(dur * 0.6), fps, 12);
  return (
    <AbsoluteFill style={{ background: `radial-gradient(circle at 30% 50%, #ffffff, ${C.mint} 55%, #cfe8c8)` }}>
      <div style={{ position: "absolute", left: 230, top: 150, width: 640, transform: `scale(${0.5 + jar * 0.5}) rotate(${(1 - jar) * -10}deg)` }}>
        <Img src={staticFile("cetaphil/jar.png")} style={{ width: "100%", filter: "drop-shadow(0 40px 40px rgba(15,42,26,.28))" }} />
        <div style={{ position: "absolute", inset: 0, WebkitMaskImage: `url(${staticFile("cetaphil/jar.png")})`, WebkitMaskSize: "100% 100%", background: `linear-gradient(100deg, transparent ${sweep - 18}%, rgba(255,255,255,.8) ${sweep}%, transparent ${sweep + 18}%)` }} />
      </div>
      <div style={{ position: "absolute", right: 150, top: 230, display: "flex", flexDirection: "column", gap: 28, alignItems: "flex-start" }}>
        {items.map((t, i) => {
          const s = S(f - 12 - i * 10, fps, 13);
          return <div key={t} style={{ fontSize: 58, fontWeight: 900, color: C.ink, background: "white", padding: "18px 40px", borderRadius: 999, borderRight: `14px solid ${C.green}`, opacity: s, transform: `translateX(${(1 - s) * -120}px)`, boxShadow: "0 10px 30px rgba(0,0,0,.08)" }}>{t}</div>;
        })}
      </div>
      <div style={{ position: "absolute", right: 150, bottom: 160, opacity: tag, transform: `translateY(${(1 - tag) * 30}px)`, textAlign: "right" }}>
        <div style={{ fontSize: 96, fontWeight: 900, color: C.deep }}>ترطيب لكل العائلة</div>
      </div>
    </AbsoluteFill>
  );
};

/* green circle wipe on every cut */
const Wipe: React.FC<{ at: number[] }> = ({ at }) => {
  const f = useCurrentFrame();
  return (
    <>
      {at.map((c) => {
        const r = interpolate(f, [c - 9, c, c + 9], [0, 1, 0], clamp);
        if (r <= 0) return null;
        const growing = f < c;
        return <AbsoluteFill key={c} style={{ background: C.green, clipPath: `circle(${r * 120}% at ${growing ? "100% 100%" : "0% 0%"})` }} />;
      })}
    </>
  );
};

export const AD30 = { open: 120, mom: 150, run: 150, grandpa: 150, office: 120, family: 90, pack: 120 };
export const AD30_TOTAL = Object.values(AD30).reduce((a, b) => a + b, 0);

export const Ad30: React.FC<{ audio?: string | null }> = ({ audio = "cetaphil/sfx30.wav" }) => {
  const d = AD30;
  const starts: number[] = [];
  Object.values(d).reduce((acc, v) => { starts.push(acc); return acc + v; }, 0);
  const [o, m, r, g, of, fa, p] = starts;
  return (
    <AbsoluteFill style={{ fontFamily, direction: "rtl", background: "#fff" }}>
      <Sequence from={o} durationInFrames={d.open}><Open /></Sequence>
      <Sequence from={m} durationInFrames={d.mom}><MomKid dur={d.mom} /></Sequence>
      <Sequence from={r} durationInFrames={d.run}><Runner dur={d.run} /></Sequence>
      <Sequence from={g} durationInFrames={d.grandpa}><Grandpa dur={d.grandpa} /></Sequence>
      <Sequence from={of} durationInFrames={d.office}><OfficeWoman dur={d.office} /></Sequence>
      <Sequence from={fa} durationInFrames={d.family}><Family /></Sequence>
      <Sequence from={p} durationInFrames={d.pack}><Pack dur={d.pack} /></Sequence>
      <Wipe at={starts.slice(1)} />
      {audio ? <Audio src={staticFile(audio)} /> : null}
    </AbsoluteFill>
  );
};
