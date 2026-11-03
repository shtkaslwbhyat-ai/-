import React from "react";
import {
  AbsoluteFill,
  Audio,
  Easing,
  Sequence,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { Avatar } from "./Avatar";
import { FontFaces } from "./fonts";
import { SCENES, SFX, SceneTiming } from "./timeline";

export const FPS = 30;
export const DURATION_SECONDS = 59.5;

export const C = {
  bg: "#07070c",
  lime: "#d6ff3f",
  mint: "#7cf7c9",
  muted: "#aeb3c7",
  soft: "#cfd3e6",
};

// Returns the entrance style of element `i` of the current scene.
type RevealFn = (i: number) => React.CSSProperties;

export const Background: React.FC = () => {
  const t = useCurrentFrame() / FPS;
  const blob = (x: number, y: number, color: string, i: number) => {
    const cx = 100 * (x + 0.12 * Math.sin(t * 0.35 + i * 2));
    const cy = 100 * (y + 0.08 * Math.cos(t * 0.3 + i));
    return `radial-gradient(800px circle at ${cx}% ${cy}%, ${color}, transparent 70%)`;
  };
  const off = (t * 20) % 80;
  return (
    <AbsoluteFill
      style={{
        backgroundColor: C.bg,
        backgroundImage: [
          "linear-gradient(rgba(255,255,255,0.035) 1px, transparent 1px)",
          "linear-gradient(90deg, rgba(255,255,255,0.035) 1px, transparent 1px)",
          blob(0.2, 0.25, "rgba(214,255,63,0.16)", 0),
          blob(0.8, 0.7, "rgba(124,247,201,0.14)", 1),
          blob(0.5, 0.5, "rgba(120,90,255,0.13)", 2),
        ].join(","),
        backgroundSize: "80px 80px, 80px 80px, 100% 100%, 100% 100%, 100% 100%",
        backgroundPosition: `${off}px ${off}px, ${off}px ${off}px, 0 0, 0 0, 0 0`,
      }}
    />
  );
};

const styles = {
  brand: {
    fontSize: 150,
    fontWeight: 900,
    letterSpacing: -2,
    direction: "ltr",
    background: `linear-gradient(90deg, ${C.lime}, ${C.mint})`,
    WebkitBackgroundClip: "text",
    color: "transparent",
  },
  h1: { fontSize: 92, fontWeight: 900, lineHeight: 1.3, textAlign: "center" },
  h2: { fontSize: 52, fontWeight: 700, color: C.soft, textAlign: "center", lineHeight: 1.5 },
  tag: {
    fontSize: 42,
    fontWeight: 700,
    padding: "8px 34px",
    borderRadius: 999,
    background: "rgba(214,255,63,.12)",
    color: C.lime,
    border: "2px solid rgba(214,255,63,.4)",
    marginBottom: 30,
  },
  chip: {
    fontSize: 44,
    fontWeight: 900,
    padding: "8px 30px",
    borderRadius: 20,
    background: "rgba(255,255,255,.08)",
    border: "2px solid rgba(255,255,255,.15)",
  },
  card: {
    background: "rgba(255,255,255,.06)",
    border: "2px solid rgba(255,255,255,.12)",
    borderRadius: 28,
    padding: "24px 20px",
    textAlign: "center",
  },
  row: {
    display: "flex",
    alignItems: "center",
    gap: 26,
    background: "rgba(255,255,255,.05)",
    borderRadius: 26,
    padding: "22px 28px",
    border: "2px solid rgba(255,255,255,.1)",
  },
  num: {
    flex: "none",
    width: 86,
    height: 86,
    borderRadius: "50%",
    background: C.lime,
    color: C.bg,
    fontSize: 50,
    fontWeight: 900,
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
  },
} satisfies Record<string, React.CSSProperties>;

const Accent: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <span style={{ color: C.lime }}>{children}</span>
);

const Intro: React.FC<{ r: RevealFn }> = ({ r }) => (
  <>
    <div style={{ ...styles.tag, ...r(0) }}>شرح مبسّط</div>
    <div style={{ ...styles.h1, ...r(1) }}>وش سالفة</div>
    <div style={{ ...styles.brand, ...r(2) }}>Higgsfield</div>
    <div style={{ ...styles.h2, ...r(3) }}>هكسفيلد… في أقل من دقيقة</div>
  </>
);

const What: React.FC<{ r: RevealFn }> = ({ r }) => (
  <>
    <div style={{ ...styles.tag, ...r(0) }}>الفكرة</div>
    <div style={{ ...styles.h1, fontSize: 80, ...r(1) }}>
      منصة <span style={{ color: C.lime, whiteSpace: "nowrap" }}>ذكاء اصطناعي</span>
      <br />
      للفيديو والصور
    </div>
    <div style={{ ...styles.h2, marginTop: 24, ...r(2) }}>تجمع أشهر النماذج في مكان واحد</div>
    <div
      style={{
        display: "flex",
        flexWrap: "wrap",
        justifyContent: "center",
        gap: 18,
        marginTop: 40,
        direction: "ltr",
        ...r(3),
      }}
    >
      {["Kling", "Veo", "Sora", "+ more"].map((m) => (
        <span key={m} style={styles.chip}>
          {m}
        </span>
      ))}
    </div>
  </>
);

const FEATURES: [string, string, string][] = [
  ["🎬", "نص ← فيديو", "اكتب المشهد واطلع بفيديو"],
  ["🖼️", "صورة ← فيديو", "حرّك صورك الثابتة"],
  ["🎥", "+60 حركة كاميرا", "زوم، دوران، درون"],
  ["✨", "مؤثرات جاهزة", "قوالب بضغطة وحدة"],
  ["🎨", "توليد صور", "واقعية أو فنية"],
  ["🗣️", "صوت ومزامنة", "تعليق صوتي وLipsync"],
];

const Features: React.FC<{ r: RevealFn }> = ({ r }) => (
  <>
    <div style={{ ...styles.h1, fontSize: 76, ...r(0) }}>وش تقدر تسوّي فيها؟</div>
    <div style={{ display: "grid", gridTemplateColumns: "repeat(2, 410px)", gap: 22, marginTop: 36 }}>
      {FEATURES.map(([ic, t, d], i) => (
        <div key={t} style={{ ...styles.card, ...r(i + 1) }}>
          <div style={{ fontSize: 70, lineHeight: 1 }}>{ic}</div>
          <div style={{ fontSize: 40, fontWeight: 900, marginTop: 10 }}>{t}</div>
          <div style={{ fontSize: 27, color: C.muted, lineHeight: 1.35 }}>{d}</div>
        </div>
      ))}
    </div>
  </>
);

const STEPS: [string, string?][] = [
  ["سجّل في الموقع", "higgsfield.ai"],
  ["اختر الأداة", "فيديو، صورة، أو مؤثر"],
  ["اكتب وصفك أو ارفع صورة"],
  ["اضغط Generate ونزّل"],
];

const How: React.FC<{ r: RevealFn }> = ({ r }) => (
  <>
    <div style={{ ...styles.h1, fontSize: 80, ...r(0) }}>طريقة الاستخدام</div>
    <div style={{ display: "flex", flexDirection: "column", gap: 24, marginTop: 40, width: 860 }}>
      {STEPS.map(([t, d], i) => (
        <div key={t} style={{ ...styles.row, ...r(i + 1) }}>
          <div style={styles.num}>{i + 1}</div>
          <div>
            <div style={{ fontSize: 44, fontWeight: 900, lineHeight: 1.3 }}>{t}</div>
            {d && <div style={{ fontSize: 30, color: C.muted }}>{d}</div>}
          </div>
        </div>
      ))}
    </div>
  </>
);

const Tips: React.FC<{ r: RevealFn }> = ({ r }) => {
  const tip: React.CSSProperties = {
    ...styles.row,
    fontSize: 44,
    fontWeight: 700,
    alignItems: "flex-start",
    lineHeight: 1.45,
  };
  return (
    <>
      <div style={{ ...styles.h1, fontSize: 80, ...r(0) }}>انتبه 💡</div>
      <div style={{ display: "flex", flexDirection: "column", gap: 24, marginTop: 40, width: 860 }}>
        <div style={{ ...tip, ...r(1) }}>
          💳 <span>كل توليد يستهلك <Accent>رصيد</Accent> ويختلف حسب النموذج</span>
        </div>
        <div style={{ ...tip, ...r(2) }}>
          🆓 <span>المجاني <Accent>محدود جداً</Accent> — جرّب قبل تشترك</span>
        </div>
        <div style={{ ...tip, ...r(3) }}>
          ✍️ <span>حدّد <Accent>المكان والإضاءة وحركة الكاميرا</Accent></span>
        </div>
      </div>
    </>
  );
};

const Cta: React.FC<{ r: RevealFn }> = ({ r }) => {
  const pulse = 1 + 0.03 * Math.sin((useCurrentFrame() / FPS) * 6);
  return (
    <>
      <div style={{ ...styles.h1, ...r(0) }}>تبي الرابط؟</div>
      <div
        style={{
          fontSize: 84,
          fontWeight: 900,
          textAlign: "center",
          lineHeight: 1.45,
          marginTop: 30,
          padding: "30px 50px",
          borderRadius: 36,
          background: "rgba(214,255,63,.10)",
          border: "3px solid rgba(214,255,63,.5)",
          ...r(1),
          scale: String(pulse),
        }}
      >
        اكتب{" "}
        <span style={{ color: C.bg, background: C.lime, padding: "0 26px", borderRadius: 18 }}>هكس</span>
        <br />
        في التعليقات 👇
      </div>
      <div style={{ ...styles.h2, marginTop: 36, fontSize: 60, ...r(2) }}>
        ويجيك الرابط <Accent>عالخاص</Accent> 📩
      </div>
    </>
  );
};

const SCENE_COMPONENTS: Record<string, React.FC<{ r: RevealFn }>> = {
  intro: Intro,
  what: What,
  features: Features,
  how: How,
  tips: Tips,
  cta: Cta,
};

const Scene: React.FC<{ timing: SceneTiming }> = ({ timing }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  const { start, end, reveals } = timing;
  if (t < start || t >= end) return null;

  const fadeIn = interpolate(t - start, [0, 0.35], [0, 1], { extrapolateRight: "clamp" });
  const fadeOut = interpolate(end - t, [0, 0.35], [0, 1], { extrapolateRight: "clamp" });
  const drift = interpolate(t, [start, end], [1, 1.02]);

  const r: RevealFn = (i) => {
    const p = spring({ frame: frame - Math.round(reveals[i] * fps), fps, config: { damping: 14, mass: 0.6 } });
    return {
      opacity: Math.min(1, p),
      transform: `translateY(${(1 - p) * 60}px) scale(${0.94 + 0.06 * p})`,
    };
  };

  const Body = SCENE_COMPONENTS[timing.id];
  // The explainer lives in the top half; the avatar fills the bottom.
  return (
    <div
      style={{
        position: "absolute",
        top: 60,
        height: 1100,
        left: -75,
        width: 1230,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        opacity: Math.min(fadeIn, fadeOut),
        transform: `scale(${0.8 * drift})`,
        transformOrigin: "50% 0",
      }}
    >
      <Body r={r} />
    </div>
  );
};

export const ProgressBar: React.FC = () => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const w = interpolate(frame, [0, durationInFrames], [0, 100], { easing: Easing.linear });
  return <div style={{ position: "absolute", top: 0, right: 0, height: 10, width: `${w}%`, background: C.lime }} />;
};

export const HiggsfieldTikTok: React.FC = () => {
  const { fps } = useVideoConfig();
  return (
    <AbsoluteFill style={{ fontFamily: "Cairo, sans-serif", color: "#fff", direction: "rtl" }}>
      <FontFaces />
      <Background />
      {SCENES.map((s) => (
        <Scene key={s.id} timing={s} />
      ))}
      <Avatar />
      <ProgressBar />

      <Audio src={staticFile("voiceover.mp3")} />
      {SFX.map((e, i) => (
        <Sequence key={i} from={Math.round(e.t * fps)} durationInFrames={Math.round(1.6 * fps)} layout="none">
          <Audio src={staticFile(`sfx/${e.type}.wav`)} volume={e.volume} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};
