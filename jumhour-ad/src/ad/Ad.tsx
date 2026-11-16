import React from "react";
import { AbsoluteFill, Easing, interpolate, Sequence, staticFile, useCurrentFrame } from "remotion";
import { Audio } from "@remotion/media";
import { Bean, HotCup, IcedCup, Seal, Steam } from "./shapes";
import { body, C, display, ease, pop } from "./theme";

// Scene timing (frames @30fps) — tuned to the voiceover
export const T = {
  hook: [0, 105],
  kaif: [105, 195],
  brand: [195, 345],
  choice: [345, 435],
  crowd: [435, 520],
  end: [520, 640],
} as const;
export const TOTAL = T.end[1];

const rtl: React.CSSProperties = { direction: "rtl", textAlign: "center" };

const Bg: React.FC<{ tint?: string }> = ({ tint = C.roast }) => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{ background: `radial-gradient(circle at 50% 40%, ${tint} 0%, ${C.espresso} 75%)` }}>
      {Array.from({ length: 14 }).map((_, i) => {
        const x = (i * 137) % 1080;
        const y = ((i * 263 + f * (1.2 + (i % 4) * 0.5)) % 2200) - 200;
        return (
          <Bean
            key={i}
            size={30 + (i % 5) * 12}
            color={i % 3 === 0 ? C.caramel : C.coffee}
            style={{ position: "absolute", left: x, top: 1920 - y, opacity: 0.18, rotate: `${f * (i % 2 ? 1 : -1) + i * 40}deg` }}
          />
        );
      })}
    </AbsoluteFill>
  );
};

/** Scene wrapper: zoom-in entrance, fade-out exit */
const Scene: React.FC<{ dur: number; children: React.ReactNode; tint?: string }> = ({ dur, children, tint }) => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill
      style={{
        opacity: interpolate(f, [0, 6, dur - 6, dur], [0, 1, 1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
        scale: ease(f, [0, 14], [1.12, 1]),
      }}
    >
      <Bg tint={tint} />
      {children}
    </AbsoluteFill>
  );
};

const Word: React.FC<{ children: React.ReactNode; at: number; size?: number; color?: string; style?: React.CSSProperties }> = ({
  children,
  at,
  size = 150,
  color = C.cream,
  style,
}) => {
  const f = useCurrentFrame();
  const p = pop(f, at);
  return (
    <span
      style={{
        display: "inline-block",
        fontFamily: display,
        fontSize: size,
        color,
        lineHeight: 1.15,
        scale: String(p),
        opacity: Math.min(1, p * 2),
        ...style,
      }}
    >
      {children}
    </span>
  );
};

const Chip: React.FC<{ label: string; at: number; tilt: number; bg: string; fg?: string }> = ({ label, at, tilt, bg, fg = C.espresso }) => {
  const f = useCurrentFrame();
  return (
    <div
      style={{
        fontFamily: display,
        fontSize: 92,
        background: bg,
        color: fg,
        padding: "8px 56px 18px",
        borderRadius: 999,
        rotate: `${tilt}deg`,
        translate: `${ease(f, [at, at + 16], [tilt > 0 ? 900 : -900, 0])}px 0px`,
        boxShadow: "0 18px 40px rgba(0,0,0,.35)",
      }}
    >
      {label}
    </div>
  );
};

const Hook: React.FC = () => (
  <Scene dur={T.hook[1] - T.hook[0]}>
    <AbsoluteFill style={{ ...rtl, justifyContent: "center", alignItems: "center", gap: 50, paddingBottom: 120 }}>
      <div style={{ display: "flex", gap: 36, direction: "rtl" }}>
        <Word at={2}>وش</Word>
        <Word at={8}>عندك</Word>
        <Word at={14} color={C.gold}>اليوم؟</Word>
      </div>
      <Chip label="دوام؟" at={30} tilt={-5} bg={C.cream} />
      <Chip label="جامعة؟" at={46} tilt={4} bg={C.gold} />
      <Chip label="ولا طلعة مع الربع؟" at={62} tilt={-3} bg={C.ember} fg={C.milk} />
    </AbsoluteFill>
  </Scene>
);

const Kaif: React.FC = () => {
  const f = useCurrentFrame();
  const level = interpolate(f, [0, 40, 55, 80], [0.06, 0.06, 1, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.bezier(0.65, 0, 0.35, 1),
  });
  const shake = f > 22 && f < 36 ? Math.sin(f * 2.2) * 10 : 0;
  return (
    <Scene dur={T.kaif[1] - T.kaif[0]}>
      <AbsoluteFill style={{ ...rtl, alignItems: "center", paddingTop: 300, gap: 30 }}>
        <Word at={0} size={110}>ترى يومك ما يمشي</Word>
        <Word at={20} size={260} color={C.gold} style={{ translate: `${shake}px 0px` }}>
          بلا كيف!
        </Word>
        {/* mood battery */}
        <div style={{ marginTop: 80, display: "flex", alignItems: "center", gap: 14, direction: "ltr" }}>
          <div style={{ width: 560, height: 200, border: `10px solid ${C.cream}`, borderRadius: 40, padding: 14, boxSizing: "border-box" }}>
            <div
              style={{
                width: `${level * 100}%`,
                height: "100%",
                borderRadius: 22,
                background: level < 0.3 ? C.ember : `linear-gradient(90deg, ${C.caramel}, ${C.gold})`,
              }}
            />
          </div>
          <div style={{ width: 26, height: 80, background: C.cream, borderRadius: 8 }} />
        </div>
        <div style={{ fontFamily: body, fontWeight: 800, fontSize: 64, color: C.cream }}>
          المزاج: {Math.round(level * 100)}٪
        </div>
      </AbsoluteFill>
    </Scene>
  );
};

const Feature: React.FC<{ label: string; at: number }> = ({ label, at }) => {
  const f = useCurrentFrame();
  return (
    <div
      style={{
        display: "flex",
        alignItems: "center",
        gap: 28,
        background: "rgba(246,235,221,0.08)",
        border: `3px solid ${C.gold}`,
        borderRadius: 34,
        padding: "18px 44px 26px",
        width: 820,
        boxSizing: "border-box",
        opacity: ease(f, [at, at + 10], [0, 1]),
        translate: `0px ${ease(f, [at, at + 16], [80, 0])}px`,
      }}
    >
      <Bean size={46} color={C.gold} />
      <span style={{ fontFamily: display, fontSize: 76, color: C.cream }}>{label}</span>
    </div>
  );
};

const Brand: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <Scene dur={T.brand[1] - T.brand[0]} tint={C.coffee}>
      {/* bean burst */}
      {Array.from({ length: 16 }).map((_, i) => {
        const a = (i / 16) * Math.PI * 2;
        const r = ease(f, [0, 30], [0, 520 + (i % 3) * 90]);
        return (
          <Bean
            key={i}
            size={54}
            color={i % 2 ? C.caramel : C.coffee}
            style={{
              position: "absolute",
              left: 540 + Math.cos(a) * r - 27,
              top: 600 + Math.sin(a) * r - 36,
              rotate: `${i * 50 + f * 3}deg`,
              opacity: ease(f, [20, 60], [1, 0.35]),
            }}
          />
        );
      })}
      <AbsoluteFill style={{ ...rtl, alignItems: "center", paddingTop: 220 }}>
        <div style={{ scale: String(pop(f, 4, 24)), rotate: `${ease(f, [4, 30], [-90, 0])}deg` }}>
          <Seal size={600} spin={f * 0.8} />
        </div>
        <div style={{ marginTop: 40 }}>
          <Word at={22} size={150} color={C.gold}>قهوة الجمهور</Word>
        </div>
        <div style={{ display: "flex", flexDirection: "column", gap: 26, marginTop: 40, alignItems: "center" }}>
          <Feature label="حبوب مختارة" at={50} />
          <Feature label="محمّصة على أصولها" at={74} />
          <Feature label="طعم يعدّل الراس" at={98} />
        </div>
      </AbsoluteFill>
    </Scene>
  );
};

const Choice: React.FC = () => {
  const f = useCurrentFrame();
  const split = ease(f, [0, 20], [0, 1]);
  return (
    <Scene dur={T.choice[1] - T.choice[0]}>
      <AbsoluteFill style={{ flexDirection: "row-reverse" }}>
        {/* hot (right) */}
        <div style={{ flex: 1, background: `linear-gradient(180deg, ${C.ember}, ${C.roast})`, translate: `${(1 - split) * 540}px 0px`, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 20 }}>
          <Steam f={f} width={200} style={{ marginBottom: -60 }} />
          <HotCup width={300} style={{ rotate: `${Math.sin(f / 12) * 3}deg` }} />
          <Word at={18} size={130}>حارّة</Word>
        </div>
        {/* cold (left) */}
        <div style={{ flex: 1, background: `linear-gradient(180deg, #2E6F86, ${C.espresso})`, translate: `${(split - 1) * 540}px 0px`, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 20 }}>
          <IcedCup width={290} f={f} style={{ rotate: `${Math.sin(f / 12 + 1) * 3}deg` }} />
          <Word at={26} size={130} color={C.ice}>باردة</Word>
        </div>
      </AbsoluteFill>
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", paddingBottom: 150 }}>
        <div style={{ fontFamily: display, fontSize: 120, color: C.espresso, background: C.gold, borderRadius: "50%", width: 190, height: 190, display: "flex", alignItems: "center", justifyContent: "center", scale: String(pop(f, 14)), boxShadow: "0 0 0 14px rgba(30,17,10,.4)" }}>
          ولا
        </div>
      </AbsoluteFill>
      <AbsoluteFill style={{ ...rtl, justifyContent: "flex-end", alignItems: "center", paddingBottom: 170 }}>
        <div style={{ background: C.cream, color: C.espresso, fontFamily: display, fontSize: 84, padding: "10px 50px 22px", borderRadius: 28, opacity: ease(f, [40, 52], [0, 1]), translate: `0px ${ease(f, [40, 56], [60, 0])}px` }}>
          اطلب اللي على كيفك
        </div>
      </AbsoluteFill>
    </Scene>
  );
};

const Crowd: React.FC = () => {
  const f = useCurrentFrame();
  const cols = 6;
  return (
    <Scene dur={T.crowd[1] - T.crowd[0]} tint={C.coffee}>
      <AbsoluteFill style={{ ...rtl, alignItems: "center", paddingTop: 280, gap: 10 }}>
        <Word at={0} size={140} color={C.cream}>حيّاك الله..</Word>
        <Word at={22} size={130} color={C.gold}>وتراك من الجمهور!</Word>
      </AbsoluteFill>
      {/* stadium wave of cups */}
      {[0, 1, 2].map((row) =>
        Array.from({ length: cols }).map((_, i) => {
          const wave = Math.max(0, Math.sin((f - i * 4 - row * 3) / 7)) * 70;
          const rise = ease(f, [6 + row * 6, 26 + row * 6], [500, 0]);
          return (
            <div key={`${row}-${i}`} style={{ position: "absolute", left: i * 180 + (row % 2) * 90 - 40, top: 1180 + row * 200 + rise - wave }}>
              {(i + row) % 3 === 1 ? <IcedCup width={170} f={f} /> : <HotCup width={170} />}
            </div>
          );
        }),
      )}
    </Scene>
  );
};

const End: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <Scene dur={T.end[1] - T.end[0]}>
      <AbsoluteFill style={{ background: `radial-gradient(circle at 50% 38%, ${C.caramel}55, transparent 60%)` }} />
      <AbsoluteFill style={{ ...rtl, alignItems: "center", paddingTop: 260 }}>
        <div style={{ scale: String(pop(f, 0, 22)) }}>
          <Seal size={520} spin={f * 0.6} />
        </div>
        <div style={{ marginTop: 50 }}>
          <Word at={14} size={170} color={C.cream}>قهوة الجمهور</Word>
        </div>
        <div style={{ position: "relative", marginTop: 10 }}>
          <Word at={30} size={120} color={C.gold}>الكيف كيفنا</Word>
          <div style={{ height: 10, background: C.gold, borderRadius: 5, width: `${ease(f, [40, 60], [0, 100])}%`, margin: "0 auto" }} />
        </div>
        <div
          style={{
            marginTop: 110,
            fontFamily: display,
            fontSize: 72,
            color: C.espresso,
            background: C.cream,
            padding: "14px 70px 26px",
            borderRadius: 999,
            opacity: ease(f, [55, 68], [0, 1]),
            scale: String(1 + Math.max(0, Math.sin((f - 70) / 6)) * 0.04 * (f > 70 ? 1 : 0)),
          }}
        >
          حيّاك في أقرب فرع ☕
        </div>
      </AbsoluteFill>
    </Scene>
  );
};

export const Ad: React.FC<{ voice: boolean; music: boolean }> = ({ voice, music }) => {
  const seq = (k: keyof typeof T, el: React.ReactNode) => (
    <Sequence from={T[k][0]} durationInFrames={T[k][1] - T[k][0]} name={k}>
      {el}
    </Sequence>
  );
  return (
    <AbsoluteFill style={{ backgroundColor: C.espresso }}>
      {seq("hook", <Hook />)}
      {seq("kaif", <Kaif />)}
      {seq("brand", <Brand />)}
      {seq("choice", <Choice />)}
      {seq("crowd", <Crowd />)}
      {seq("end", <End />)}
      {music ? <Audio src={staticFile("music.mp3")} volume={0.25} /> : null}
      {voice ? (
        <Sequence from={6}>
          <Audio src={staticFile("voiceover.mp3")} />
        </Sequence>
      ) : null}
    </AbsoluteFill>
  );
};
