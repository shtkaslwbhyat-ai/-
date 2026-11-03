import React from "react";
import {
  AbsoluteFill,
  Audio,
  Img,
  Sequence,
  interpolate,
  random,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { FontFaces } from "../fonts";
import { Background, C, ProgressBar } from "../HiggsfieldTikTok";
import { SCENES, SFX, SceneTiming } from "./timeline";

export { DURATION_SECONDS } from "./timeline";

const AVATAR = staticFile("avatar.jpg");
const HANDLE = "@fahad.ai";

// ---------- helpers ----------

const useT = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return { frame, fps, t: frame / fps };
};

// Spring progress (0 → ~1) of a beat that starts at absolute time `at`.
const useBeat = () => {
  const { frame, fps } = useT();
  return (at: number, damping = 14) =>
    spring({ frame: frame - Math.round(at * fps), fps, config: { damping, mass: 0.6 } });
};

const enter = (p: number, dy = 60): React.CSSProperties => ({
  opacity: Math.min(1, p),
  transform: `translateY(${(1 - p) * dy}px) scale(${0.92 + 0.08 * p})`,
});

const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

// The avatar photo cropped into a w×h box, centred on (fx, fy) of the source image.
const Photo: React.FC<{
  w: number;
  h: number;
  zoom?: number;
  fx?: number;
  fy?: number;
  filter?: string;
  radius?: number | string;
  style?: React.CSSProperties;
  children?: React.ReactNode;
}> = ({ w, h, zoom = 1, fx = 0.5, fy = 0.45, filter, radius = 24, style, children }) => {
  const size = Math.max(w, h) * zoom;
  return (
    <div style={{ position: "relative", width: w, height: h, overflow: "hidden", borderRadius: radius, flex: "none", ...style }}>
      <Img
        src={AVATAR}
        style={{ position: "absolute", width: size, height: size, left: w / 2 - fx * size, top: h / 2 - fy * size, filter }}
      />
      {children}
    </div>
  );
};

// Post looks: a filter on the photo plus a tint, a sticker and a caption.
const LOOKS = [
  { filter: "saturate(1.25)", tint: "rgba(255,170,60,.18)", sticker: "☕", caption: "صباح الخير" },
  { filter: "hue-rotate(-20deg) saturate(1.3)", tint: "rgba(40,170,255,.22)", sticker: "🏝️", caption: "إجازة" },
  { filter: "contrast(1.15) brightness(.9)", tint: "rgba(255,40,90,.16)", sticker: "🏋️", caption: "تمرين" },
  { filter: "grayscale(1) contrast(1.1)", tint: "rgba(0,0,0,0)", sticker: "🎬", caption: "خلف الكواليس" },
  { filter: "sepia(.4) saturate(1.2)", tint: "rgba(214,255,63,.12)", sticker: "✈️", caption: "سفر" },
  { filter: "hue-rotate(25deg) saturate(1.4)", tint: "rgba(160,90,255,.2)", sticker: "🎮", caption: "قيمنق" },
];

const Post: React.FC<{ look: number; w: number; h: number; zoom?: number; fy?: number; radius?: number }> = ({
  look,
  w,
  h,
  zoom = 1.25,
  fy = 0.42,
  radius = 14,
}) => {
  const l = LOOKS[look % LOOKS.length];
  return (
    <Photo w={w} h={h} zoom={zoom} fy={fy} filter={l.filter} radius={radius}>
      <div style={{ position: "absolute", inset: 0, background: `linear-gradient(160deg, ${l.tint}, transparent 60%)` }} />
      <div style={{ position: "absolute", top: 8, left: 10, fontSize: w * 0.2 }}>{l.sticker}</div>
    </Photo>
  );
};

const Accent: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <span style={{ color: C.lime }}>{children}</span>
);

const H1: React.FC<{ style?: React.CSSProperties; children: React.ReactNode }> = ({ style, children }) => (
  <div style={{ fontSize: 84, fontWeight: 900, lineHeight: 1.25, textAlign: "center", ...style }}>{children}</div>
);

const Glass: React.CSSProperties = {
  background: "rgba(255,255,255,.06)",
  border: "2px solid rgba(255,255,255,.12)",
  borderRadius: 32,
};

const Check: React.FC<{ ok?: boolean; size?: number }> = ({ ok = true, size = 44 }) => (
  <span
    style={{
      display: "inline-flex",
      alignItems: "center",
      justifyContent: "center",
      width: size,
      height: size,
      borderRadius: "50%",
      background: ok ? C.lime : "#ffb020",
      color: C.bg,
      fontSize: size * 0.6,
      fontWeight: 900,
      flex: "none",
    }}
  >
    {ok ? "✓" : "!"}
  </span>
);

// ---------- scenes ----------

type SceneProps = { s: SceneTiming };

const formatFollowers = (n: number) => (n >= 1000 ? `${(n / 1000).toFixed(n >= 100000 ? 0 : 1)}K` : String(Math.round(n)));

const Hook: React.FC<SceneProps> = ({ s }) => {
  const { t, frame } = useT();
  const beat = useBeat();
  const [cProfile, cPosts, cCount, cGlitch] = s.cues;
  const followers = interpolate(t, [cCount, cCount + 2.6], [0, 248000], {
    ...clamp,
    easing: (x) => 1 - Math.pow(1 - x, 3),
  });
  const glitching = t >= cGlitch && t < cGlitch + 0.5;
  const after = t >= cGlitch;
  const stamp = beat(cGlitch + 0.15, 9);

  const phone = (
    <div
      style={{
        width: 700,
        height: 1180,
        borderRadius: 70,
        background: "#0d0d14",
        border: "10px solid #23232e",
        boxShadow: "0 40px 120px rgba(0,0,0,.6), 0 0 0 2px rgba(255,255,255,.05)",
        padding: "60px 36px",
        overflow: "hidden",
        filter: after ? "grayscale(.7) brightness(.75)" : undefined,
        ...enter(beat(cProfile)),
      }}
    >
      <div style={{ display: "flex", alignItems: "center", gap: 28 }}>
        <div style={{ padding: 6, borderRadius: "50%", background: `conic-gradient(${C.lime}, ${C.mint}, #a78bfa, ${C.lime})` }}>
          <Photo w={170} h={170} zoom={2.1} fy={0.33} radius="50%" style={{ border: "6px solid #0d0d14" }} />
        </div>
        <div style={{ flex: 1 }}>
          <div style={{ fontSize: 50, fontWeight: 900, display: "flex", alignItems: "center", gap: 12 }}>
            فهد <span style={{ fontSize: 30, background: "#3b82f6", borderRadius: "50%", width: 40, height: 40, display: "inline-flex", alignItems: "center", justifyContent: "center" }}>✓</span>
          </div>
          <div style={{ fontSize: 32, color: C.muted, direction: "ltr", textAlign: "right" }}>{HANDLE}</div>
        </div>
      </div>
      <div style={{ display: "flex", justifyContent: "space-around", margin: "40px 0 34px", textAlign: "center" }}>
        {[
          ["312", "منشور"],
          [formatFollowers(followers), "متابع"],
          ["180", "يتابع"],
        ].map(([n, l], i) => (
          <div key={l}>
            <div style={{ fontSize: 50, fontWeight: 900, color: i === 1 ? C.lime : "#fff", direction: "ltr" }}>{n}</div>
            <div style={{ fontSize: 28, color: C.muted }}>{l}</div>
          </div>
        ))}
      </div>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 8 }}>
        {LOOKS.map((_, i) => (
          <div key={i} style={enter(beat(cPosts + i * 0.12), 40)}>
            <Post look={i} w={204} h={260} />
          </div>
        ))}
      </div>
    </div>
  );

  // Horizontal slices of the phone shifted sideways for a digital glitch.
  const slices = glitching
    ? Array.from({ length: 7 }, (_, i) => {
        const top = (i / 7) * 100;
        const dx = (random(`g${i}-${frame}`) - 0.5) * 70;
        return (
          <div
            key={i}
            style={{
              position: "absolute",
              inset: 0,
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              clipPath: `inset(${top}% 0 ${100 - top - 100 / 7}% 0)`,
              transform: `translateX(${dx}px)`,
              mixBlendMode: i % 2 ? "screen" : "normal",
            }}
          >
            {phone}
          </div>
        );
      })
    : null;

  return (
    <AbsoluteFill style={{ alignItems: "center", justifyContent: "center" }}>
      <div style={{ position: "absolute", inset: 0, display: "flex", justifyContent: "center", alignItems: "center", paddingBottom: 120 }}>
        {glitching ? <div style={{ position: "relative", width: 1080, height: 1920 }}>{slices}</div> : phone}
      </div>
      {after && (
        <div
          style={{
            position: "absolute",
            top: 760,
            padding: "26px 56px",
            borderRadius: 30,
            background: C.lime,
            color: C.bg,
            fontSize: 96,
            fontWeight: 900,
            transform: `rotate(-7deg) scale(${2.2 - 1.2 * Math.min(stamp, 1)})`,
            opacity: Math.min(1, stamp * 1.5),
            boxShadow: "0 30px 80px rgba(0,0,0,.6)",
          }}
        >
          مو موجود! 🤖
        </div>
      )}
      {/* scanlines during the glitch */}
      {glitching && (
        <AbsoluteFill
          style={{ background: "repeating-linear-gradient(0deg, rgba(214,255,63,.10) 0 3px, transparent 3px 9px)" }}
        />
      )}
    </AbsoluteFill>
  );
};

const Title: React.FC<SceneProps> = ({ s }) => {
  const { t } = useT();
  const beat = useBeat();
  const [c0, c1] = s.cues;
  const p = beat(c0);
  return (
    <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", paddingBottom: 200 }}>
      <div style={{ position: "relative", width: 520, height: 520, ...enter(p) }}>
        <div
          style={{
            position: "absolute",
            inset: 0,
            borderRadius: "50%",
            background: `conic-gradient(from ${t * 90}deg, ${C.lime}, transparent 30%, ${C.mint} 50%, transparent 80%, ${C.lime})`,
          }}
        />
        <Photo w={480} h={480} zoom={1.9} fy={0.36} radius="50%" style={{ position: "absolute", top: 20, left: 20, border: `8px solid ${C.bg}` }} />
        {["✨", "📸", "🎬", "💬"].map((e, i) => {
          const a = t * 0.8 + (i * Math.PI) / 2;
          return (
            <div key={e} style={{ position: "absolute", left: 260 + Math.cos(a) * 320 - 40, top: 260 + Math.sin(a) * 320 - 40, fontSize: 70 }}>
              {e}
            </div>
          );
        })}
      </div>
      <div style={{ marginTop: 90, fontSize: 40, fontWeight: 700, color: C.lime, ...enter(beat(c0 + 0.3)) }}>خاصية في هكسفيلد</div>
      <div
        style={{
          fontSize: 130,
          fontWeight: 900,
          direction: "ltr",
          background: `linear-gradient(90deg, ${C.lime}, ${C.mint})`,
          WebkitBackgroundClip: "text",
          color: "transparent",
          ...enter(beat(c0 + 0.5)),
        }}
      >
        AI Influencer
      </div>
      <div style={{ fontSize: 52, fontWeight: 700, color: C.soft, ...enter(beat(c1)) }}>
        شخصية بالذكاء الاصطناعي… <Accent>من الصفر</Accent>
      </div>
    </AbsoluteFill>
  );
};

const ATTRS: [string, string][] = [
  ["الجنس", "رجل"],
  ["العمر", "28"],
  ["الأصل", "عربي"],
  ["البشرة", "حنطي"],
  ["العيون", "عسلي"],
];
const TABS = ["الوجه", "الجسم", "الستايل"];

const Builder: React.FC<SceneProps> = ({ s }) => {
  const { t } = useT();
  const beat = useBeat();
  const [cPanel, ...rest] = s.cues;
  const rowCues = rest.slice(0, 5);
  const tabCues = rest.slice(5, 8);
  const cStamp = rest[8];
  const done = rowCues.filter((c) => t >= c).length;
  const sharp = interpolate(t, [rowCues[0], rowCues[4] + 0.5], [0, 1], clamp);
  const activeTab = tabCues.filter((c) => t >= c).length - 1;
  const ROW_H = 92;

  // cursor glides from row to row, then along the tabs
  const targets = [...rowCues.map((c, i) => ({ c, x: 250, y: 600 + i * ROW_H })), ...tabCues.map((c, i) => ({ c, x: 700 - i * 270, y: 600 + 5 * ROW_H + 40 }))];
  const times = targets.map((p) => p.c - 0.35);
  const cx = interpolate(t, times, targets.map((p) => p.x), clamp);
  const cy = interpolate(t, times, targets.map((p) => p.y), clamp);
  const stamp = beat(cStamp, 10);

  return (
    <AbsoluteFill style={{ alignItems: "center", paddingTop: 210 }}>
      <div style={{ position: "relative", ...enter(beat(cPanel)) }}>
        <Photo
          w={330}
          h={330}
          zoom={1.6}
          fy={0.38}
          radius={40}
          filter={`blur(${(1 - sharp) * 26}px) grayscale(${1 - sharp})`}
          style={{ margin: "0 auto", border: `4px solid ${sharp >= 1 ? C.lime : "rgba(255,255,255,.15)"}` }}
        >
          {sharp < 1 && (
            <div
              style={{
                position: "absolute",
                left: 0,
                right: 0,
                top: `${(t * 120) % 100}%`,
                height: 6,
                background: C.lime,
                boxShadow: `0 0 30px ${C.lime}`,
              }}
            />
          )}
        </Photo>
        <div style={{ textAlign: "center", fontSize: 30, color: C.muted, marginTop: 10 }}>
          {done < 5 ? `جاري البناء… ${done * 20}%` : "جاهز ✓"}
        </div>
      </div>

      <div style={{ ...Glass, width: 860, marginTop: 26, padding: "18px 34px", ...enter(beat(cPanel + 0.2)) }}>
        <div style={{ fontSize: 34, fontWeight: 900, color: C.lime, direction: "ltr", textAlign: "left", marginBottom: 6 }}>Builder</div>
        {ATTRS.map(([k, v], i) => {
          const p = beat(rowCues[i], 12);
          return (
            <div
              key={k}
              style={{
                height: ROW_H,
                display: "flex",
                alignItems: "center",
                justifyContent: "space-between",
                borderBottom: "2px solid rgba(255,255,255,.07)",
              }}
            >
              <span style={{ fontSize: 42, fontWeight: 700 }}>{k}</span>
              <span
                style={{
                  fontSize: 38,
                  fontWeight: 900,
                  padding: "4px 28px",
                  borderRadius: 999,
                  background: t >= rowCues[i] ? C.lime : "rgba(255,255,255,.08)",
                  color: t >= rowCues[i] ? C.bg : C.muted,
                  transform: `scale(${t >= rowCues[i] ? 0.9 + 0.1 * p : 1})`,
                }}
              >
                {t >= rowCues[i] ? v : "اختر ▾"}
              </span>
            </div>
          );
        })}
        <div style={{ display: "flex", gap: 16, marginTop: 22 }}>
          {TABS.map((tab, i) => (
            <div
              key={tab}
              style={{
                flex: 1,
                textAlign: "center",
                fontSize: 38,
                fontWeight: 900,
                padding: "12px 0",
                borderRadius: 20,
                background: i === activeTab ? "rgba(214,255,63,.18)" : "rgba(255,255,255,.05)",
                border: `2px solid ${i <= activeTab ? C.lime : "rgba(255,255,255,.1)"}`,
                color: i <= activeTab ? "#fff" : C.muted,
              }}
            >
              {tab}
            </div>
          ))}
        </div>
      </div>

      {/* cursor */}
      {t < cStamp && (
        <div style={{ position: "absolute", left: cx, top: cy, fontSize: 70, filter: "drop-shadow(0 6px 10px rgba(0,0,0,.6))" }}>👆</div>
      )}

      {/* "no prompt" moment */}
      {t >= cStamp && (
        <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", background: `rgba(7,7,12,${0.75 * Math.min(1, stamp)})` }}>
          <div style={{ ...Glass, width: 820, padding: 36, direction: "ltr", ...enter(stamp) }}>
            <div style={{ fontSize: 28, color: C.muted, marginBottom: 10 }}>Prompt</div>
            <div style={{ position: "relative", fontSize: 36, color: C.soft, fontFamily: "monospace", lineHeight: 1.5 }}>
              a 28 year old arab man, short dark hair, trimmed beard, warm smile, studio light…
              <div
                style={{
                  position: "absolute",
                  left: 0,
                  top: "50%",
                  height: 10,
                  borderRadius: 5,
                  background: "#ff4d6d",
                  width: `${interpolate(t, [cStamp + 0.2, cStamp + 0.7], [0, 100], clamp)}%`,
                }}
              />
            </div>
          </div>
          <div
            style={{
              marginTop: 50,
              fontSize: 90,
              fontWeight: 900,
              color: C.bg,
              background: C.lime,
              padding: "16px 50px",
              borderRadius: 28,
              transform: `rotate(-4deg) scale(${interpolate(beat(cStamp + 0.6, 9), [0, 1], [1.8, 1])})`,
              opacity: Math.min(1, beat(cStamp + 0.6) * 1.5),
            }}
          >
            بدون برومبت ✓
          </div>
        </AbsoluteFill>
      )}
    </AbsoluteFill>
  );
};

const TRAITS = ["💇 الشعر", "👕 اللبس", "🎂 العمر", "💪 الجسم"];

const Face: React.FC<SceneProps> = ({ s }) => {
  const { t } = useT();
  const beat = useBeat();
  const [cZone, cDrop, cLock, cTraits] = s.cues;
  const drop = beat(cDrop, 11);
  const lock = beat(cLock, 9);
  return (
    <AbsoluteFill style={{ alignItems: "center", paddingTop: 230 }}>
      <H1 style={enter(beat(cZone))}>
        صورة <Accent>وحدة</Accent> لوجهك
      </H1>
      <div
        style={{
          position: "relative",
          width: 600,
          height: 700,
          marginTop: 50,
          borderRadius: 44,
          border: `5px dashed ${t >= cDrop + 0.4 ? C.lime : "rgba(255,255,255,.3)"}`,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          ...enter(beat(cZone + 0.2)),
        }}
      >
        <div style={{ textAlign: "center", color: C.muted, fontSize: 40, opacity: 1 - Math.min(1, drop) }}>
          <div style={{ fontSize: 110 }}>📤</div>ارفع صورة
        </div>
        <div
          style={{
            position: "absolute",
            transform: `translateY(${(1 - drop) * -900}px) rotate(${(1 - drop) * -14}deg)`,
          }}
        >
          <Photo w={500} h={600} zoom={1.25} fy={0.4} radius={30} style={{ boxShadow: "0 30px 80px rgba(0,0,0,.6)" }} />
        </div>
        {t >= cLock && (
          <div
            style={{
              position: "absolute",
              bottom: -40,
              padding: "14px 34px",
              borderRadius: 999,
              background: C.lime,
              color: C.bg,
              fontSize: 44,
              fontWeight: 900,
              transform: `scale(${interpolate(lock, [0, 1], [1.6, 1])})`,
              opacity: Math.min(1, lock * 1.5),
              whiteSpace: "nowrap",
            }}
          >
            🔒 ملامحك محفوظة
          </div>
        )}
      </div>
      <div style={{ display: "flex", flexWrap: "wrap", justifyContent: "center", gap: 18, marginTop: 80, width: 860 }}>
        {TRAITS.map((tr, i) => (
          <div
            key={tr}
            style={{
              ...Glass,
              borderRadius: 999,
              padding: "12px 30px",
              fontSize: 40,
              fontWeight: 700,
              display: "flex",
              gap: 14,
              alignItems: "center",
              ...enter(beat(cTraits + i * 0.15)),
            }}
          >
            {tr}
            <span style={{ display: "inline-block", transform: `rotate(${t * 200 + i * 40}deg)`, color: C.lime }}>⟳</span>
          </div>
        ))}
      </div>
      <div style={{ marginTop: 26, fontSize: 40, color: C.soft, fontWeight: 700, ...enter(beat(cTraits + 0.7)) }}>
        وأنت تغيّر الباقي
      </div>
    </AbsoluteFill>
  );
};

const OUTPUTS: [string, string][] = [
  ["📸", "صورة"],
  ["🎬", "فيديو"],
  ["🎞️", "@fahad"],
];

const Soul: React.FC<SceneProps> = ({ s }) => {
  const { t } = useT();
  const beat = useBeat();
  const [cGrid, cTrain, cDone, cOut] = s.cues;
  const pull = interpolate(t, [cTrain, cTrain + 1.2], [0, 1], { ...clamp, easing: (x) => x * x });
  const progress = interpolate(t, [cTrain + 0.6, cDone], [0, 100], clamp);
  const done = t >= cDone;
  const doneP = beat(cDone, 9);
  const CENTER_Y = 760;
  const R = 230;
  const circ = 2 * Math.PI * R;

  return (
    <AbsoluteFill style={{ alignItems: "center" }}>
      <div style={{ position: "absolute", top: 220, width: "100%", ...enter(beat(s.start + 0.5)) }}>
        <H1>
          السر: <span style={{ direction: "ltr", display: "inline-block", color: C.lime }}>Soul ID</span>
        </H1>
      </div>

      {/* intro: a locked face before the portraits arrive */}
      {t < cGrid + 0.4 && (
        <div
          style={{
            position: "absolute",
            top: 560,
            width: "100%",
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            opacity: interpolate(t, [cGrid, cGrid + 0.4], [1, 0], clamp),
            ...enter(beat(s.start + 0.9)),
          }}
        >
          <div style={{ position: "relative" }}>
            <Photo w={380} h={380} zoom={1.8} fy={0.36} radius="50%" style={{ border: `6px solid ${C.lime}` }} />
            <div
              style={{
                position: "absolute",
                bottom: -20,
                left: -20,
                fontSize: 120,
                transform: `rotate(${-12 + 6 * Math.sin(t * 3)}deg)`,
              }}
            >
              🔐
            </div>
          </div>
          <div style={{ fontSize: 52, fontWeight: 900, marginTop: 50 }}>
            <Accent>نفس الوجه</Accent> في كل مرة
          </div>
        </div>
      )}

      {/* portraits fly into the ring */}
      {Array.from({ length: 12 }, (_, i) => {
        const col = i % 4;
        const row = Math.floor(i / 4);
        const x0 = 540 + (col - 1.5) * 215;
        const y0 = 560 + row * 250;
        const x = interpolate(pull, [0, 1], [x0, 540]);
        const y = interpolate(pull, [0, 1], [y0, CENTER_Y]);
        const p = beat(cGrid + 0.3 + i * 0.07);
        if (pull >= 1) return null;
        return (
          <div
            key={i}
            style={{
              position: "absolute",
              left: x - 95,
              top: y - 115,
              opacity: Math.min(1, p) * (1 - pull),
              transform: `scale(${(0.9 + 0.1 * p) * (1 - 0.7 * pull)}) rotate(${pull * (i % 2 ? 90 : -90)}deg)`,
            }}
          >
            <Post look={i} w={190} h={230} zoom={1.1 + (i % 3) * 0.25} fy={0.38 + (i % 4) * 0.02} />
          </div>
        );
      })}

      {/* training ring */}
      {t >= cTrain + 0.4 && (
        <div style={{ position: "absolute", top: CENTER_Y - R - 20, left: 540 - R - 20, width: 2 * R + 40, height: 2 * R + 40 }}>
          <svg width={2 * R + 40} height={2 * R + 40} style={{ position: "absolute", transform: "rotate(-90deg)" }}>
            <circle cx={R + 20} cy={R + 20} r={R} fill="none" stroke="rgba(255,255,255,.1)" strokeWidth={18} />
            <circle
              cx={R + 20}
              cy={R + 20}
              r={R}
              fill="none"
              stroke={C.lime}
              strokeWidth={18}
              strokeLinecap="round"
              strokeDasharray={circ}
              strokeDashoffset={circ * (1 - progress / 100)}
            />
          </svg>
          <Photo
            w={2 * R - 40}
            h={2 * R - 40}
            zoom={1.8}
            fy={0.36}
            radius="50%"
            filter={done ? undefined : `grayscale(${1 - progress / 100}) blur(${(1 - progress / 100) * 8}px)`}
            style={{ position: "absolute", top: 60, left: 60 }}
          />
        </div>
      )}
      {t >= cTrain + 0.4 && (
        <div style={{ position: "absolute", top: CENTER_Y + R + 50, fontSize: 48, fontWeight: 900, textAlign: "center" }}>
          {done ? (
            <span style={{ color: C.lime, display: "inline-block", transform: `scale(${interpolate(doneP, [0, 1], [1.5, 1])})` }}>
              ✓ تم القفل على الوجه
            </span>
          ) : (
            <span>
              تدريب… <span style={{ color: C.lime }}>{Math.round(progress)}%</span>
            </span>
          )}
        </div>
      )}

      {/* same face everywhere */}
      <div style={{ position: "absolute", top: 1180, display: "flex", gap: 24 }}>
        {OUTPUTS.map(([ic, label], i) => (
          <div key={label} style={{ ...Glass, padding: 16, textAlign: "center", ...enter(beat(cOut + i * 0.2)) }}>
            <Post look={i * 2 + 1} w={240} h={260} />
            <div style={{ fontSize: 34, fontWeight: 900, marginTop: 10, direction: "ltr" }}>
              {ic} {label}
            </div>
            <div style={{ fontSize: 26, color: C.lime, fontWeight: 700 }}>✓ نفس الوجه</div>
          </div>
        ))}
      </div>
    </AbsoluteFill>
  );
};

const Limits: React.FC<SceneProps> = ({ s }) => {
  const beat = useBeat();
  const [cFront, cSide, cLight, cOutfit, cCredit] = s.cues;
  const card = (p: number): React.CSSProperties => ({ ...Glass, padding: 18, textAlign: "center", ...enter(p) });
  const label = (ok: boolean, text: string, sub: string) => (
    <div style={{ marginTop: 12 }}>
      <div style={{ display: "flex", gap: 12, justifyContent: "center", alignItems: "center", fontSize: 38, fontWeight: 900 }}>
        <Check ok={ok} size={42} /> {text}
      </div>
      <div style={{ fontSize: 28, color: ok ? C.lime : "#ffb020", fontWeight: 700 }}>{sub}</div>
    </div>
  );
  return (
    <AbsoluteFill style={{ alignItems: "center", paddingTop: 220 }}>
      <H1 style={enter(beat(s.start + 0.4))}>
        بس <span style={{ color: "#ffb020" }}>انتبه</span> ⚠️
      </H1>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(2, 400px)", gap: 24, marginTop: 40 }}>
        <div style={card(beat(cFront))}>
          <Photo w={364} h={330} zoom={1.5} fy={0.38} radius={20} />
          {label(true, "من قدّام", "ممتاز")}
        </div>
        <div style={card(beat(cSide))}>
          <div style={{ perspective: 900, width: 364, height: 330, overflow: "hidden", borderRadius: 20, background: "rgba(0,0,0,.3)" }}>
            <Photo w={364} h={330} zoom={1.5} fy={0.38} radius={20} style={{ transform: "rotateY(38deg) scale(.82)" }} />
          </div>
          {label(false, "زاوية جانبية", "الملامح ممكن تتغيّر")}
        </div>
        <div style={card(beat(cLight))}>
          <Photo w={364} h={330} zoom={1.5} fy={0.38} radius={20} filter="contrast(1.9) brightness(.75) saturate(1.4)">
            <div style={{ position: "absolute", inset: 0, background: "linear-gradient(100deg, rgba(255,60,60,.45), transparent 45%, rgba(40,80,255,.45))" }} />
          </Photo>
          {label(false, "إضاءة قوية", "تخرّب الملامح")}
        </div>
        <div style={card(beat(cOutfit))}>
          <div style={{ display: "flex", gap: 8 }}>
            <Post look={1} w={178} h={330} zoom={1.15} fy={0.5} radius={20} />
            <Post look={5} w={178} h={330} zoom={1.15} fy={0.5} radius={20} />
          </div>
          {label(false, "اللبس والخلفية", "ممكن يتغيّرون")}
        </div>
      </div>
      <div
        style={{
          marginTop: 34,
          fontSize: 46,
          fontWeight: 900,
          padding: "18px 40px",
          borderRadius: 26,
          border: `3px solid ${C.lime}`,
          background: "rgba(214,255,63,.1)",
          ...enter(beat(cCredit)),
        }}
      >
        💳 كل توليد <Accent>ياكل من رصيدك</Accent>
      </div>
    </AbsoluteFill>
  );
};

const Cta: React.FC<SceneProps> = ({ s }) => {
  const { t } = useT();
  const beat = useBeat();
  const [c0, c1, c2] = s.cues;
  const pulse = 1 + 0.03 * Math.sin(t * 6);
  return (
    <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", paddingBottom: 260 }}>
      <Photo w={300} h={300} zoom={1.9} fy={0.36} radius="50%" style={{ border: `6px solid ${C.lime}`, ...enter(beat(c0)) }} />
      <H1 style={{ marginTop: 30, ...enter(beat(c0 + 0.15)) }}>تبي الرابط؟</H1>
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
          ...enter(beat(c1)),
          scale: String(pulse),
        }}
      >
        اكتب <span style={{ color: C.bg, background: C.lime, padding: "0 26px", borderRadius: 18 }}>هكس</span>
        <br />
        في التعليقات 👇
      </div>
      <div style={{ fontSize: 60, fontWeight: 700, color: C.soft, marginTop: 36, ...enter(beat(c2)) }}>
        ويجيك الرابط <Accent>عالخاص</Accent> 📩
      </div>
    </AbsoluteFill>
  );
};

const SCENE_COMPONENTS: Record<SceneTiming["id"], React.FC<SceneProps>> = {
  hook: Hook,
  title: Title,
  builder: Builder,
  face: Face,
  soul: Soul,
  limits: Limits,
  cta: Cta,
};

const SceneSlot: React.FC<{ s: SceneTiming }> = ({ s }) => {
  const { t } = useT();
  if (t < s.start || t >= s.end) return null;
  const fadeIn = interpolate(t - s.start, [0, 0.3], [0, 1], clamp);
  const fadeOut = interpolate(s.end - t, [0, 0.3], [0, 1], clamp);
  // quick zoom-through transition between scenes
  const zoom = interpolate(t - s.start, [0, 0.3], [1.06, 1], clamp) * interpolate(s.end - t, [0, 0.3], [0.94, 1], clamp);
  const Body = SCENE_COMPONENTS[s.id];
  return (
    <AbsoluteFill style={{ opacity: Math.min(fadeIn, fadeOut), transform: `scale(${zoom})` }}>
      <Body s={s} />
    </AbsoluteFill>
  );
};

export const InfluencerTikTok: React.FC = () => {
  const { fps } = useVideoConfig();
  return (
    <AbsoluteFill style={{ fontFamily: "Cairo, sans-serif", color: "#fff", direction: "rtl" }}>
      <FontFaces />
      <Background />
      {SCENES.map((s) => (
        <SceneSlot key={s.id} s={s} />
      ))}
      <ProgressBar />

      <Audio src={staticFile("influencer/voiceover.mp3")} />
      {SFX.map((e, i) => (
        <Sequence key={i} from={Math.round(e.t * fps)} durationInFrames={Math.round(1.4 * fps)} layout="none">
          <Audio src={staticFile(`sfx/${e.type}.wav`)} volume={e.volume} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};
