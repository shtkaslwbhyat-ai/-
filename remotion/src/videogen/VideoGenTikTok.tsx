import React from "react";
import {
  AbsoluteFill,
  Audio,
  CalculateMetadataFunction,
  Sequence,
  interpolate,
  random,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { getAudioDurationInSeconds } from "@remotion/media-utils";
import { FontFaces } from "../fonts";
import { Background, C, ProgressBar } from "../HiggsfieldTikTok";
import { Camera, DesertScene, FilmLook, Viewfinder } from "./DesertScene";

// One voice clip per scene, in public/videogen/. Scenes are laid back to back, so each
// scene lasts exactly as long as its clip (plus TAIL) and there are no dead gaps.
const SCENE_IDS = ["hook", "models", "studio", "how", "tip", "close"] as const;
type SceneId = (typeof SCENE_IDS)[number];
const clip = (i: number) => `videogen/s${i + 1}.mp3`;
const TAIL = 0.12;
// Used when a clip is missing, so the video still previews.
const FALLBACK = [6, 7, 11, 4.5, 6, 9];

export type VideoGenProps = { durations: number[]; hasAudio: boolean[] };

export const calculateVideoGenMetadata: CalculateMetadataFunction<VideoGenProps> = async () => {
  const results = await Promise.all(
    SCENE_IDS.map((_, i) => getAudioDurationInSeconds(staticFile(clip(i))).then((d) => ({ d, ok: true }), () => ({ d: FALLBACK[i], ok: false })))
  );
  const durations = results.map((r) => r.d + TAIL);
  const total = durations.reduce((a, b) => a + b, 0) + 0.5;
  return { durationInFrames: Math.ceil(total * 30), props: { durations, hasAudio: results.map((r) => r.ok) } };
};

type Timing = { id: SceneId; start: number; dur: number };
const layout = (durations: number[]): Timing[] => {
  let at = 0;
  return SCENE_IDS.map((id, i) => {
    const s = { id, start: at, dur: durations[i] };
    at += durations[i];
    return s;
  });
};

// ---------- helpers ----------

const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const easeOut = (x: number) => 1 - Math.pow(1 - x, 3);

// Beat helpers for a scene: `at(f)` is the absolute time at fraction f of the scene,
// `beat(f)` the spring progress of a beat that starts there.
const useScene = (s: Timing) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  const at = (f: number) => s.start + f * s.dur;
  const beat = (f: number, damping = 14) => spring({ frame: frame - Math.round(at(f) * fps), fps, config: { damping, mass: 0.6 } });
  const after = (f: number) => t >= at(f);
  return { frame, fps, t, at, beat, after, u: (t - s.start) / s.dur };
};

const enter = (p: number, dy = 60): React.CSSProperties => ({
  opacity: Math.min(1, p),
  transform: `translateY(${(1 - p) * dy}px) scale(${0.92 + 0.08 * p})`,
});

const slam = (p: number, from = 2.4): React.CSSProperties => ({
  opacity: Math.min(1, p * 1.5),
  transform: `scale(${interpolate(p, [0, 1], [from, 1])})`,
});

const Accent: React.FC<{ children: React.ReactNode }> = ({ children }) => <span style={{ color: C.lime }}>{children}</span>;

const Glass: React.CSSProperties = {
  background: "rgba(255,255,255,.06)",
  border: "2px solid rgba(255,255,255,.12)",
  borderRadius: 30,
};

const H1: React.FC<{ style?: React.CSSProperties; children: React.ReactNode }> = ({ style, children }) => (
  <div style={{ fontSize: 88, fontWeight: 900, lineHeight: 1.25, textAlign: "center", textShadow: "0 8px 40px rgba(0,0,0,.6)", ...style }}>{children}</div>
);

const Chip: React.FC<{ on?: boolean; style?: React.CSSProperties; children: React.ReactNode }> = ({ on, style, children }) => (
  <div
    style={{
      fontSize: 34,
      fontWeight: 900,
      padding: "10px 24px",
      borderRadius: 18,
      textAlign: "center",
      background: on ? C.lime : "rgba(255,255,255,.07)",
      color: on ? C.bg : C.soft,
      border: `2px solid ${on ? C.lime : "rgba(255,255,255,.12)"}`,
      direction: "ltr",
      ...style,
    }}
  >
    {children}
  </div>
);

// ---------- scenes ----------

const PROMPT = "فارس يعبر الصحراء وقت الغروب، لقطة درون سينمائية…";

const Hook: React.FC<{ s: Timing }> = ({ s }) => {
  const { t, at, beat, after, frame } = useScene(s);
  const NOS: [string, string, number][] = [
    ["🎥", "بدون كاميرا", 0.27],
    ["🎭", "ولا ممثلين", 0.37],
    ["💰", "ولا ميزانية", 0.47],
  ];
  const typed = Math.floor(interpolate(t, [at(0.6), at(0.84)], [0, PROMPT.length], clamp));
  const reveal = interpolate(t, [at(0.86), at(0.95)], [0, 1], clamp);
  const shake = Math.max(0, 1 - (t - s.start) / 0.4) * 22;
  return (
    <AbsoluteFill style={{ transform: `translate(${(random(`a${frame}`) - 0.5) * shake}px, ${(random(`b${frame}`) - 0.5) * shake}px)` }}>
      <AbsoluteFill style={{ filter: `blur(${(1 - reveal) * 14}px) brightness(${0.45 + 0.55 * reveal})`, transform: `scale(${1.15 - 0.15 * reveal})` }}>
        <DesertScene w={1080} h={1920} camera={{ zoom: 1.1 + 0.1 * Math.sin(t * 0.5), panX: t * 15 }} />
      </AbsoluteFill>
      {reveal > 0.5 && <Viewfinder w={1080} h={1920} />}
      <AbsoluteFill style={{ background: "#fff", opacity: interpolate(t - s.start, [0, 0.12], [0.85, 0], clamp) }} />

      {t < at(0.86) && (
        <AbsoluteFill style={{ alignItems: "center", paddingTop: 260 }}>
          <H1 style={{ fontSize: 104, ...slam(beat(0, 9)) }}>
            مشهد <Accent>سينمائي</Accent> 🎬
          </H1>
          <div style={{ display: "flex", flexDirection: "column", gap: 22, marginTop: 50 }}>
            {NOS.map(([ic, txt, f]) => (
              <div key={txt} style={{ ...Glass, background: "rgba(7,7,12,.7)", display: "flex", alignItems: "center", gap: 24, padding: "16px 40px", fontSize: 60, fontWeight: 900, ...enter(beat(f)) }}>
                <span style={{ position: "relative" }}>
                  {ic}
                  {after(f + 0.03) && (
                    <span style={{ position: "absolute", inset: -8, display: "flex", alignItems: "center", justifyContent: "center", color: "#ff3b5c", fontSize: 96, ...slam(beat(f + 0.03, 8), 2) }}>
                      ✕
                    </span>
                  )}
                </span>
                {txt}
              </div>
            ))}
          </div>
          {after(0.58) && (
            <div style={{ ...Glass, background: "rgba(7,7,12,.85)", width: 900, marginTop: 60, padding: "26px 34px", ...enter(beat(0.58)) }}>
              <div style={{ fontSize: 28, color: C.muted, marginBottom: 8 }}>✍️ جملة وحدة</div>
              <div style={{ fontSize: 42, fontWeight: 700, minHeight: 120, lineHeight: 1.45 }}>
                {PROMPT.slice(0, typed)}
                <span style={{ opacity: frame % 16 < 8 ? 1 : 0, color: C.lime }}>|</span>
              </div>
              <div style={{ display: "flex", justifyContent: "flex-start" }}>
                <div
                  style={{
                    fontSize: 40,
                    fontWeight: 900,
                    padding: "10px 36px",
                    borderRadius: 18,
                    background: C.lime,
                    color: C.bg,
                    direction: "ltr",
                    transform: `scale(${after(0.84) && !after(0.87) ? 0.9 : 1})`,
                  }}
                >
                  Generate ⚡
                </div>
              </div>
            </div>
          )}
        </AbsoluteFill>
      )}
      {after(0.9) && (
        <AbsoluteFill style={{ alignItems: "center", justifyContent: "flex-end", paddingBottom: 520 }}>
          <H1 style={{ fontSize: 80, ...enter(beat(0.9)) }}>
            وخلّ <Accent>هكسفيلد</Accent> يسوّي الباقي
          </H1>
        </AbsoluteFill>
      )}
    </AbsoluteFill>
  );
};

const MODELS = ["Kling", "Veo", "Seedance", "Sora", "WAN", "MiniMax"];

const Models: React.FC<{ s: Timing }> = ({ s }) => {
  const { t, at, beat, after } = useScene(s);
  const highlight = [0.42, 0.52, 0.62].filter((f) => after(f)).length - 1;
  const converge = interpolate(t, [at(0.8), at(0.92)], [0, 1], { ...clamp, easing: easeOut });
  return (
    <AbsoluteFill style={{ alignItems: "center", paddingTop: 230 }}>
      <div style={{ display: "flex", gap: 24 }}>
        {[
          ["📝", "نص", 0.03],
          ["🖼️", "صورة", 0.16],
        ].map(([ic, label, f]) => (
          <div key={label as string} style={{ ...Glass, padding: "22px 30px", display: "flex", alignItems: "center", gap: 16, fontSize: 50, fontWeight: 900, ...enter(beat(f as number)) }}>
            {ic} {label} <span style={{ color: C.lime }}>←</span> 🎬 فيديو
          </div>
        ))}
      </div>

      <div style={{ fontSize: 46, fontWeight: 900, color: C.soft, marginTop: 70, ...enter(beat(0.3)) }}>اختر النموذج 👇</div>

      <div style={{ position: "relative", width: 1000, height: 760, marginTop: 20 }}>
        {MODELS.map((m, i) => {
          const a = (i / MODELS.length) * Math.PI * 2 + t * 0.6;
          const r = 300 * (1 - converge);
          const on = i === highlight && converge < 0.5;
          return (
            <div
              key={m}
              style={{
                position: "absolute",
                left: 500 + Math.cos(a) * r - 140,
                top: 360 + Math.sin(a) * r * 0.8 - 50,
                width: 280,
                opacity: (1 - converge) * Math.min(1, beat(0.32 + i * 0.03)),
                transform: `scale(${on ? 1.2 : 1})`,
              }}
            >
              <Chip on={on} style={{ fontSize: 46, padding: "16px 0" }}>
                {m}
              </Chip>
            </div>
          );
        })}
        {after(0.72) && converge < 0.6 && (
          <div style={{ position: "absolute", left: 0, right: 0, top: 330, textAlign: "center", fontSize: 44, fontWeight: 900, color: C.lime, ...enter(beat(0.72)) }}>
            + غيرها
          </div>
        )}
        {converge > 0 && (
          <div
            style={{
              position: "absolute",
              left: 500 - 220,
              top: 360 - 220,
              width: 440,
              height: 440,
              borderRadius: "50%",
              background: `radial-gradient(circle, rgba(214,255,63,.25), rgba(214,255,63,.05) 60%, transparent 70%)`,
              border: `5px solid ${C.lime}`,
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              justifyContent: "center",
              transform: `scale(${converge})`,
            }}
          >
            <div style={{ fontSize: 64, fontWeight: 900, direction: "ltr" }}>Higgsfield</div>
            <div style={{ fontSize: 36, fontWeight: 700, color: C.lime }}>كلها في مكان واحد</div>
          </div>
        )}
      </div>
    </AbsoluteFill>
  );
};

const MOVES: [string, string][] = [
  ["Dolly In", "↗"],
  ["Drone", "🚁"],
  ["Robot Arm", "🦾"],
  ["POV", "👁️"],
  ["Pan Left", "⬅"],
  ["Crane", "🏗️"],
];

const Studio: React.FC<{ s: Timing }> = ({ s }) => {
  const { t, at, beat, after } = useScene(s);
  const move = after(0.4) ? 2 : after(0.3) ? 1 : -1; // Drone, then Robot Arm
  const body: FilmLook = after(0.63) ? "8mm" : after(0.55) ? "35mm" : "clean";
  const lens = after(0.72) ? 85 : 35;
  // the preview's camera follows the selected move
  const local = t - at(move === 2 ? 0.4 : 0.3);
  const camera: Camera =
    move === 1
      ? { rise: interpolate(local, [0, 1.2], [0, 260], clamp), zoom: interpolate(local, [0, 1.2], [1.25, 1], clamp) }
      : move === 2
        ? { panX: Math.sin(local * 1.6) * 160, zoom: 1.15, tilt: Math.sin(local * 1.6) * 2 }
        : { zoom: 1.05 + 0.02 * Math.sin(t) };
  if (lens === 85) camera.zoom = (camera.zoom ?? 1) * interpolate(t, [at(0.72), at(0.78)], [1, 1.45], clamp);

  const section = (title: string, f: number, children: React.ReactNode) => (
    <div style={{ marginTop: 22, ...enter(beat(f)) }}>
      <div style={{ fontSize: 30, fontWeight: 900, color: C.muted, marginBottom: 10 }}>{title}</div>
      {children}
    </div>
  );

  return (
    <AbsoluteFill style={{ alignItems: "center", paddingTop: 200 }}>
      <div style={{ display: "flex", alignItems: "center", gap: 20, ...enter(beat(0.02)) }}>
        <div style={{ fontSize: 70, fontWeight: 900, direction: "ltr" }}>Cinema Studio</div>
      </div>
      <div style={{ fontSize: 56, fontWeight: 900, color: C.bg, background: C.lime, padding: "4px 34px", borderRadius: 20, marginTop: 10, ...slam(beat(0.1, 9)) }}>
        أنت المخرج 🎬
      </div>

      <div style={{ position: "relative", marginTop: 30, borderRadius: 28, overflow: "hidden", border: "3px solid rgba(255,255,255,.15)", ...enter(beat(0.14)) }}>
        <DesertScene w={900} h={500} camera={camera} look={body} letterbox={false} />
        <div style={{ position: "absolute", top: 16, left: 20, fontSize: 26, fontWeight: 900, color: "#fff", direction: "ltr", textShadow: "0 2px 8px #000" }}>
          ● PREVIEW · {lens}mm · {body === "clean" ? "Digital" : body === "35mm" ? "35mm Film" : "8mm Film"}
        </div>
      </div>

      <div style={{ ...Glass, width: 900, padding: "10px 30px 28px", marginTop: 20 }}>
        {section(
          "حركة الكاميرا · +30",
          0.22,
          <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 12 }}>
            {MOVES.map(([m, ic], i) => (
              <Chip key={m} on={i === move}>
                {ic} {m}
              </Chip>
            ))}
          </div>
        )}
        {section(
          "نوع الكاميرا",
          0.5,
          <div style={{ display: "flex", gap: 12 }}>
            {(["35mm", "8mm"] as FilmLook[]).map((b) => (
              <Chip key={b} on={body === b} style={{ flex: 1 }}>
                🎞️ {b} Film
              </Chip>
            ))}
          </div>
        )}
        {section(
          "العدسة · النوع · الحقبة",
          0.7,
          <div style={{ display: "flex", gap: 12 }}>
            <Chip on={after(0.72)} style={{ flex: 1 }}>
              🔭 85mm
            </Chip>
            <Chip on={after(0.8)} style={{ flex: 1 }}>
              🤠 Western
            </Chip>
            <Chip on={after(0.88)} style={{ flex: 1 }}>
              📅 1970s
            </Chip>
          </div>
        )}
      </div>
    </AbsoluteFill>
  );
};

const How: React.FC<{ s: Timing }> = ({ s }) => {
  const { t, at, beat, after } = useScene(s);
  const steps: [string, string, number][] = [
    ["✍️", "اكتب الوصف أو ارفع صورة", 0.1],
    ["🎥", "اضبط الكاميرا", 0.42],
    ["⚡", "اضغط Generate", 0.62],
  ];
  const progress = interpolate(t, [at(0.66), at(0.86)], [0, 100], clamp);
  return (
    <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", paddingBottom: 200 }}>
      <H1 style={enter(beat(0))}>الطريقة؟</H1>
      <div style={{ display: "flex", flexDirection: "column", gap: 26, marginTop: 50, width: 900 }}>
        {steps.map(([ic, txt, f], i) => (
          <div key={txt} style={{ ...Glass, display: "flex", alignItems: "center", gap: 26, padding: "24px 34px", ...enter(beat(f), 0), transform: `translateX(${(1 - Math.min(1, beat(f))) * -300}px)` }}>
            <div style={{ width: 90, height: 90, borderRadius: "50%", background: C.lime, color: C.bg, fontSize: 52, fontWeight: 900, display: "flex", alignItems: "center", justifyContent: "center", flex: "none" }}>
              {i + 1}
            </div>
            <div style={{ fontSize: 50, fontWeight: 900 }}>
              {ic} {txt}
            </div>
          </div>
        ))}
        {after(0.66) && (
          <div style={{ height: 22, borderRadius: 11, background: "rgba(255,255,255,.1)", overflow: "hidden" }}>
            <div style={{ height: "100%", width: `${progress}%`, background: C.lime, boxShadow: `0 0 30px ${C.lime}` }} />
          </div>
        )}
      </div>
      {after(0.86) && (
        <div style={{ marginTop: 50, fontSize: 130, fontWeight: 900, color: C.bg, background: C.lime, padding: "0 60px", borderRadius: 40, transform: `rotate(-6deg)`, ...slam(beat(0.86, 8)) }}>
          بس! ✅
        </div>
      )}
    </AbsoluteFill>
  );
};

const Tip: React.FC<{ s: Timing }> = ({ s }) => {
  const { t, at, beat } = useScene(s);
  const meters: [string, number][] = [
    ["⏱️ الطول", 0.55],
    ["🖥️ الدقة", 0.68],
    ["🧠 النموذج", 0.8],
  ];
  return (
    <AbsoluteFill style={{ alignItems: "center", paddingTop: 260 }}>
      <H1 style={slam(beat(0, 9))}>💡 نصيحة</H1>
      <div style={{ display: "flex", gap: 20, marginTop: 50 }}>
        <div style={{ ...Glass, padding: "20px 34px", fontSize: 46, fontWeight: 900, ...enter(beat(0.15)) }}>
          <Accent>✓</Accent> مقاطع قصيرة
        </div>
        <div style={{ ...Glass, padding: "20px 34px", fontSize: 46, fontWeight: 900, ...enter(beat(0.3)) }}>
          <Accent>✓</Accent> دقة أقل
        </div>
      </div>
      <div style={{ ...Glass, width: 900, marginTop: 50, padding: "30px 40px", ...enter(beat(0.45)) }}>
        <div style={{ fontSize: 40, fontWeight: 900, marginBottom: 20 }}>
          💳 الرصيد <span style={{ color: "#ffb020" }}>يزيد</span> مع:
        </div>
        {meters.map(([label, f]) => {
          const fill = interpolate(t, [at(f), at(f) + 0.7], [10, 92], { ...clamp, easing: easeOut });
          return (
            <div key={label} style={{ display: "flex", alignItems: "center", gap: 20, marginTop: 18 }}>
              <div style={{ width: 230, fontSize: 38, fontWeight: 700 }}>{label}</div>
              <div style={{ flex: 1, height: 34, borderRadius: 17, background: "rgba(255,255,255,.08)", overflow: "hidden" }}>
                <div style={{ height: "100%", width: `${fill}%`, borderRadius: 17, background: `linear-gradient(90deg, ${C.lime}, #ffb020 70%, #ff3b5c)` }} />
              </div>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

const Close: React.FC<{ s: Timing }> = ({ s }) => {
  const { t, at, beat, after } = useScene(s);
  const cta = interpolate(t, [at(0.58), at(0.66)], [0, 1], { ...clamp, easing: easeOut });
  const lines: [React.ReactNode, number][] = [
    [<>القصة اللي في بالك؟</>, 0.02],
    [<>صوّرها <Accent>الليلة</Accent> 🌙</>, 0.17],
    [<>لا تنتظر الميزانية</>, 0.3],
    [<>ابدأ <Accent>بجملة</Accent> ✍️</>, 0.43],
  ];
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{ filter: `brightness(${1 - 0.55 * cta}) blur(${cta * 8}px)` }}>
        <DesertScene w={1080} h={1920} camera={{ zoom: 1 + (t - s.start) * 0.03, panX: (t - s.start) * 25 }} />
      </AbsoluteFill>
      {cta < 1 && (
        <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", gap: 30, opacity: 1 - cta, paddingBottom: 200 }}>
          {lines.map(([node, f], i) => (
            <H1 key={i} style={{ fontSize: i % 2 ? 100 : 76, ...enter(beat(f)) }}>
              {node}
            </H1>
          ))}
        </AbsoluteFill>
      )}
      {cta > 0 && (
        <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", paddingBottom: 240, transform: `translateY(${(1 - cta) * 400}px)`, opacity: cta }}>
          <H1>تبي الرابط؟</H1>
          <div
            style={{
              fontSize: 92,
              fontWeight: 900,
              textAlign: "center",
              lineHeight: 1.45,
              marginTop: 30,
              padding: "30px 56px",
              borderRadius: 40,
              background: "rgba(7,7,12,.75)",
              border: `4px solid ${C.lime}`,
              scale: String(1 + 0.03 * Math.sin(t * 6)),
              ...enter(beat(0.68)),
            }}
          >
            اكتب <span style={{ color: C.bg, background: C.lime, padding: "0 26px", borderRadius: 18 }}>هكس</span>
            <br />
            في التعليقات 👇
          </div>
          {after(0.85) && <div style={{ fontSize: 62, fontWeight: 900, marginTop: 36, ...enter(beat(0.85)) }}>ويجيك الرابط <Accent>عالخاص</Accent> 📩</div>}
        </AbsoluteFill>
      )}
    </AbsoluteFill>
  );
};

const SCENES: Record<SceneId, React.FC<{ s: Timing }>> = { hook: Hook, models: Models, studio: Studio, how: How, tip: Tip, close: Close };

const Slot: React.FC<{ s: Timing }> = ({ s }) => {
  const { fps } = useVideoConfig();
  const t = useCurrentFrame() / fps;
  if (t < s.start || t >= s.start + s.dur) return null;
  // quick punch-in between scenes; the hook starts hard with no fade
  const local = t - s.start;
  const fade = s.id === "hook" ? 1 : interpolate(local, [0, 0.18], [0, 1], clamp);
  const Body = SCENES[s.id];
  return (
    <AbsoluteFill style={{ opacity: fade, transform: `scale(${interpolate(local, [0, 0.2], [s.id === "hook" ? 1 : 1.08, 1], clamp)})` }}>
      <Body s={s} />
    </AbsoluteFill>
  );
};

type Sfx = { type: string; t: number; volume: number };

const sfxFor = (scenes: Timing[]): Sfx[] => {
  const S = Object.fromEntries(scenes.map((s) => [s.id, s])) as Record<SceneId, Timing>;
  const at = (id: SceneId, f: number) => S[id].start + f * S[id].dur;
  return [
    { type: "impact", t: 0, volume: 0.7 },
    ...[0.3, 0.4, 0.5].map((f) => ({ type: "pop", t: at("hook", f), volume: 0.35 })),
    ...Array.from({ length: 10 }, (_, i) => ({ type: "tick", t: at("hook", 0.6) + i * 0.12, volume: 0.12 })),
    { type: "impact", t: at("hook", 0.86), volume: 0.5 },
    ...scenes.slice(1).map((s) => ({ type: "whoosh", t: Math.max(0, s.start - 0.2), volume: 0.4 })),
    ...[0.03, 0.16, 0.42, 0.52, 0.62].map((f) => ({ type: "pop", t: at("models", f), volume: 0.3 })),
    { type: "success", t: at("models", 0.82), volume: 0.4 },
    { type: "drop", t: at("studio", 0.1), volume: 0.45 },
    ...[0.3, 0.4, 0.55, 0.63, 0.72, 0.8, 0.88].map((f) => ({ type: "tick", t: at("studio", f), volume: 0.3 })),
    ...[0.1, 0.42, 0.62].map((f) => ({ type: "pop", t: at("how", f), volume: 0.35 })),
    { type: "ding", t: at("how", 0.86), volume: 0.4 },
    { type: "drop", t: at("tip", 0), volume: 0.4 },
    ...[0.15, 0.3].map((f) => ({ type: "pop", t: at("tip", f), volume: 0.3 })),
    { type: "whoosh", t: at("close", 0.58), volume: 0.45 },
    { type: "ding", t: at("close", 0.68), volume: 0.4 },
  ];
};

export const VideoGenTikTok: React.FC<VideoGenProps> = ({ durations, hasAudio }) => {
  const { fps } = useVideoConfig();
  const scenes = layout(durations);
  return (
    <AbsoluteFill style={{ fontFamily: "Cairo, sans-serif", color: "#fff", direction: "rtl" }}>
      <FontFaces />
      <Background />
      {scenes.map((s) => (
        <Slot key={s.id} s={s} />
      ))}
      <ProgressBar />
      {scenes.map((s, i) =>
        hasAudio[i] ? (
          <Sequence key={s.id} from={Math.round(s.start * fps)} layout="none">
            <Audio src={staticFile(clip(i))} />
          </Sequence>
        ) : null
      )}
      {sfxFor(scenes).map((e, i) => (
        <Sequence key={i} from={Math.round(e.t * fps)} durationInFrames={Math.round(1.4 * fps)} layout="none">
          <Audio src={staticFile(`sfx/${e.type}.wav`)} volume={e.volume} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};
