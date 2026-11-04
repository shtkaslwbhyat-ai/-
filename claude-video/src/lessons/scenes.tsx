import React from "react";
import { AbsoluteFill, OffthreadVideo, interpolate, staticFile, useCurrentFrame } from "remotion";
import { COLORS } from "../config";
import { Bg, Pop, Spark, useSpring } from "../theme";

export type SceneProps = { dur: number };
const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const RED = "#E5484D";

/* Shared: quality meter that climbs lesson by lesson */
const Meter: React.FC<{ from: number; to: number; delay: number; dur: number }> = ({ from, to, delay, dur }) => {
  const frame = useCurrentFrame();
  const v = interpolate(frame, [delay, delay + dur], [from, to], clamp);
  const color = v < 40 ? RED : v < 80 ? "#E8B04B" : COLORS.green;
  return (
    <div style={{ width: "100%" }}>
      <div style={{ display: "flex", justifyContent: "space-between", fontSize: 44, fontWeight: 700, marginBottom: 16 }}>
        <span style={{ color: COLORS.muted }}>جودة الفيديو</span>
        <span style={{ color, direction: "ltr" }}>{Math.round(v)}%</span>
      </div>
      <div style={{ height: 44, borderRadius: 22, background: "#2f2823", overflow: "hidden" }}>
        <div style={{ height: "100%", width: `${v}%`, background: color, borderRadius: 22, marginRight: 0 }} />
      </div>
    </div>
  );
};

const LessonHead: React.FC<{ n: string; title: string }> = ({ n, title }) => {
  const s = useSpring(0, 12);
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 40, alignSelf: "stretch" }}>
      <div style={{ fontSize: 230, fontWeight: 900, lineHeight: 0.9, color: "transparent", WebkitTextStroke: `5px ${COLORS.orange}`, transform: `translateX(${(1 - s) * 200}px)`, opacity: s, direction: "ltr" }}>{n}</div>
      <div style={{ opacity: s }}>
        <div style={{ fontSize: 48, color: COLORS.muted, fontWeight: 700 }}>الدرس</div>
        <div style={{ fontSize: 84, fontWeight: 900, lineHeight: 1.15 }}>{title}</div>
      </div>
    </div>
  );
};

/* Piece that snaps onto the Claude block */
const Block: React.FC<{ label: string; color: string; textColor?: string; s?: number; from?: number }> = ({ label, color, textColor = COLORS.bg, s = 1, from = 0 }) => (
  <div style={{ width: 760, padding: "38px 0", borderRadius: 30, background: color, color: textColor, textAlign: "center", fontSize: 70, fontWeight: 900, direction: "ltr", transform: `translateY(${(1 - s) * from}px)`, opacity: Math.min(1, s * 1.5) }}>
    {label}
  </div>
);

/* 1 — HOOK: first vs third */
export const LHook: React.FC<SceneProps> = ({ dur }) => {
  const frame = useCurrentFrame();
  const zoom = interpolate(frame, [0, 10], [2.2, 1], clamp);
  const glitch = frame % 7 < 2 ? 12 : 0;
  const second = useSpring(Math.round(dur * 0.5), 12);
  const blur = interpolate(frame, [dur * 0.5, dur * 0.9], [30, 12], clamp);
  return (
    <Bg>
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", gap: 50, padding: 90 }}>
        <div style={{ transform: `scale(${zoom})`, textAlign: "center" }}>
          <div style={{ fontSize: 66, color: COLORS.muted, fontWeight: 700 }}>أول فيديو سويته بالـ AI</div>
          <div style={{ fontSize: 150, fontWeight: 900, color: RED, transform: `translateX(${glitch}px)`, textShadow: glitch ? `-8px 0 #36c, 8px 0 ${COLORS.orange}` : "none" }}>كارثة 💀</div>
        </div>
        <div style={{ display: "flex", gap: 40 }}>
          <Pop delay={12}>
            <div style={{ width: 400, height: 640, borderRadius: 40, background: "#bdbdbd", filter: "grayscale(1)", display: "flex", alignItems: "center", justifyContent: "center", fontFamily: "serif", fontSize: 46, color: "#555", direction: "ltr", border: `6px solid ${RED}`, transform: `translateX(${glitch / 2}px)` }}>
              My Video
            </div>
            <div style={{ textAlign: "center", fontSize: 50, fontWeight: 900, marginTop: 20 }}>الأول</div>
          </Pop>
          <div style={{ opacity: second, transform: `scale(${0.7 + second * 0.3})` }}>
            <div style={{ width: 400, height: 640, borderRadius: 40, overflow: "hidden", border: `6px solid ${COLORS.green}`, position: "relative" }}>
              <OffthreadVideo src={staticFile("v1-clip.mp4")} muted style={{ width: "100%", height: "100%", objectFit: "cover", filter: `blur(${blur}px)` }} />
              <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", fontSize: 120 }}>👀</AbsoluteFill>
            </div>
            <div style={{ textAlign: "center", fontSize: 50, fontWeight: 900, marginTop: 20, color: COLORS.green }}>الثالث؟ شوفه بنفسك</div>
          </div>
        </div>
      </AbsoluteFill>
    </Bg>
  );
};

/* 2 — LESSON 1: Claude alone → primitive */
export const L1: React.FC<SceneProps> = ({ dur }) => {
  const frame = useCurrentFrame();
  const out = useSpring(Math.round(dur * 0.45), 12);
  return (
    <Bg>
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", gap: 70, padding: 90 }}>
        <LessonHead n="01" title="الذكاء وحده ما يكفي" />
        <Pop delay={10}><Block label="Claude Code" color={COLORS.orange} /></Pop>
        <Pop delay={20}><div style={{ fontSize: 50, color: COLORS.muted }}>بدون أدوات 🧰 = فاضي</div></Pop>
        <div style={{ opacity: out, transform: `scale(${out})`, display: "flex", alignItems: "center", gap: 30 }}>
          <div style={{ fontSize: 80 }}>⬅️</div>
          <div style={{ width: 360, height: 220, background: "#bdbdbd", filter: "grayscale(1)", display: "flex", alignItems: "center", justifyContent: "center", fontFamily: "serif", fontSize: 40, color: "#555", direction: "ltr", transform: `rotate(${Math.sin(frame / 3) * 1.5}deg)` }}>Hello World</div>
          <div style={{ fontSize: 64, fontWeight: 900, color: RED }}>بدائي</div>
        </div>
        <Meter from={0} to={20} delay={Math.round(dur * 0.45)} dur={25} />
      </AbsoluteFill>
    </Bg>
  );
};

/* 3 — LESSON 2: + Remotion snaps in */
export const L2: React.FC<SceneProps> = ({ dur }) => {
  const frame = useCurrentFrame();
  const snap = useSpring(18, 11);
  const chipsAt = Math.round(dur * 0.4);
  const chips = ["الحركة", "التوقيت", "التصميم"];
  return (
    <Bg>
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", gap: 50, padding: 90 }}>
        <LessonHead n="02" title="أضف السكل الصح" />
        <div style={{ display: "flex", flexDirection: "column", gap: 14, alignItems: "center" }}>
          <Block label="Claude Code" color={COLORS.orange} />
          <Block label="+ Remotion ✨" color={COLORS.cream} s={snap} from={-500} />
        </div>
        <div style={{ display: "flex", gap: 24 }}>
          {chips.map((c, i) => (
            <Pop key={c} delay={chipsAt + i * 14}>
              <div style={{ fontSize: 54, fontWeight: 900, padding: "22px 40px", borderRadius: 999, border: `4px solid ${COLORS.orange}`, color: COLORS.orange }}>{c}</div>
            </Pop>
          ))}
        </div>
        {/* mini animated timeline */}
        <Pop delay={chipsAt} style={{ width: "100%" }}>
          <div style={{ display: "flex", flexDirection: "column", gap: 14, direction: "ltr" }}>
            {[0, 1, 2].map((r) => (
              <div key={r} style={{ height: 34, background: "#211c18", borderRadius: 10, position: "relative", overflow: "hidden" }}>
                <div style={{ position: "absolute", left: `${(r * 22 + frame * 0.6) % 70}%`, width: `${30 - r * 6}%`, height: "100%", borderRadius: 10, background: [COLORS.orange, COLORS.cream, "#E8B04B"][r] }} />
              </div>
            ))}
          </div>
        </Pop>
        <Meter from={20} to={65} delay={chipsAt} dur={30} />
      </AbsoluteFill>
    </Bg>
  );
};

/* 4 — LESSON 3: + ElevenLabs gives it a voice */
export const L3: React.FC<SceneProps> = ({ dur }) => {
  const frame = useCurrentFrame();
  const snapAt = Math.round(dur * 0.3);
  const snap = useSpring(snapAt, 11);
  const live = frame > snapAt + 10;
  return (
    <Bg>
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", gap: 50, padding: 90 }}>
        <LessonHead n="03" title="أعطه صوت وروح" />
        <Pop delay={8}><div style={{ fontSize: 58, color: COLORS.muted }}>الصورة = <span style={{ color: COLORS.cream, fontWeight: 900 }}>نص القصة</span></div></Pop>
        <div style={{ display: "flex", flexDirection: "column", gap: 14, alignItems: "center" }}>
          <Block label="Claude Code" color={COLORS.orange} />
          <Block label="+ Remotion ✨" color={COLORS.cream} />
          <Block label="+ ElevenLabs 🎙️" color="#2f2823" textColor={COLORS.cream} s={snap} from={-600} />
        </div>
        <div style={{ display: "flex", gap: 12, alignItems: "center", height: 170 }}>
          {Array.from({ length: 30 }).map((_, i) => (
            <div key={i} style={{ width: 16, borderRadius: 8, background: i % 3 ? COLORS.orange : COLORS.cream, height: live ? 24 + Math.abs(Math.sin(frame / 3 + i * 0.7) * Math.cos(frame / 7 + i)) * 150 : 16 }} />
          ))}
        </div>
        <Meter from={65} to={100} delay={snapAt + 10} dur={30} />
      </AbsoluteFill>
    </Bg>
  );
};

/* 5 — RESULT: idea → published, zero editing apps */
export const LResult: React.FC<SceneProps> = ({ dur }) => {
  const frame = useCurrentFrame();
  const steps = ["💡 فكرة", "✍️ سكربت", "🎙️ صوت", "🎞️ مشاهد", "🎬 جاهز للنشر"];
  const lit = interpolate(frame, [5, dur * 0.55], [0, steps.length], clamp);
  const zero = useSpring(Math.round(dur * 0.6), 9);
  return (
    <Bg>
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", gap: 60, padding: 90 }}>
        <div style={{ display: "flex", gap: 50, alignItems: "center" }}>
          <div style={{ display: "flex", flexDirection: "column", gap: 22 }}>
            {steps.map((s, i) => {
              const on = lit > i;
              return (
                <div key={s} style={{ fontSize: 50, fontWeight: 900, padding: "24px 36px", borderRadius: 26, width: 430, background: on ? (i === steps.length - 1 ? COLORS.orange : "#2f2823") : "#1b1714", color: on ? (i === steps.length - 1 ? COLORS.bg : COLORS.cream) : "#4a423b", transform: `scale(${on ? 1 : 0.94})` }}>
                  {s}
                </div>
              );
            })}
          </div>
          <Pop delay={4}>
            <div style={{ width: 380, height: 676, borderRadius: 50, background: "#000", padding: 12, boxShadow: `0 0 0 5px #3a322b, 0 30px 100px ${COLORS.orange}44` }}>
              <div style={{ width: "100%", height: "100%", borderRadius: 40, overflow: "hidden" }}>
                <OffthreadVideo src={staticFile("v1-clip.mp4")} muted style={{ width: "100%", height: "100%", objectFit: "cover" }} />
              </div>
            </div>
          </Pop>
        </div>
        <div style={{ textAlign: "center", opacity: zero, transform: `scale(${zero})` }}>
          <div style={{ fontSize: 90, fontWeight: 900 }}>
            <span style={{ color: COLORS.orange }}>0</span> برامج مونتاج
          </div>
          <div style={{ display: "flex", gap: 20, justifyContent: "center", marginTop: 16, direction: "ltr" }}>
            {["Premiere", "CapCut", "After Effects"].map((t) => (
              <div key={t} style={{ fontSize: 34, color: COLORS.muted, textDecoration: "line-through", textDecorationColor: RED, textDecorationThickness: 5 }}>{t}</div>
            ))}
          </div>
        </div>
      </AbsoluteFill>
    </Bg>
  );
};

/* 6 — OUTRO */
export const LOutro: React.FC<SceneProps> = ({ dur }) => {
  const frame = useCurrentFrame();
  const t = (p: number) => Math.round(dur * p);
  const strike = useSpring(t(0.18), 20);
  const need = useSpring(t(0.3), 12);
  const cta = useSpring(t(0.66), 10);
  const pulse = 1 + Math.sin(frame / 6) * 0.04;
  return (
    <Bg>
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", gap: 70, padding: 90, textAlign: "center" }}>
        <Spark size={150} rotate={frame * 1.5} />
        <Pop>
          <div style={{ fontSize: 60, color: COLORS.muted, fontWeight: 700 }}>الخلاصة؟</div>
          <div style={{ fontSize: 88, fontWeight: 900, marginTop: 10, whiteSpace: "nowrap" }}>
            ما تحتاج تكون{" "}
            <span style={{ position: "relative", display: "inline-block" }}>
              مونتير
              <span style={{ position: "absolute", right: -10, top: "52%", height: 12, borderRadius: 6, background: RED, width: `calc(${strike * 100}% + 20px)` }} />
            </span>
          </div>
        </Pop>
        <div style={{ opacity: need, transform: `translateY(${(1 - need) * 40}px)`, display: "flex", flexDirection: "column", gap: 24 }}>
          <div style={{ fontSize: 64, fontWeight: 900 }}>تحتاج تعرف:</div>
          <div style={{ fontSize: 60, fontWeight: 900, background: "#211c18", padding: "26px 50px", borderRadius: 28, borderRight: `12px solid ${COLORS.orange}` }}>🗣️ وش تطلب</div>
          <div style={{ fontSize: 60, fontWeight: 900, background: "#211c18", padding: "26px 50px", borderRadius: 28, borderRight: `12px solid ${COLORS.orange}` }}>🧰 ومن وين تجيب الأدوات</div>
        </div>
        <div style={{ opacity: cta, transform: `scale(${cta * pulse})`, display: "flex", flexDirection: "column", gap: 20, alignItems: "center" }}>
          <div style={{ fontSize: 62, fontWeight: 900, background: COLORS.orange, color: COLORS.bg, padding: "34px 70px", borderRadius: 999 }}>🔖 احفظ الفيديو</div>
          <div style={{ fontSize: 52, fontWeight: 700 }}>وسوّ أول فيديو لك <span style={{ color: COLORS.orange }}>اليوم</span></div>
        </div>
      </AbsoluteFill>
    </Bg>
  );
};
