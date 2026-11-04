import React from "react";
import { AbsoluteFill, OffthreadVideo, interpolate, staticFile, useCurrentFrame } from "remotion";
import { COLORS } from "../config";
import { Bg, Pop, Spark, useSpring } from "../theme";
import { AttemptTag, SceneProps, Stamp } from "./common";

const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

/* 1 — HOOK */
export const JHook: React.FC<SceneProps> = ({ dur }) => {
  const frame = useCurrentFrame();
  const zoom = interpolate(frame, [0, 10], [2.4, 1], clamp);
  const shake = frame < 12 ? Math.sin(frame * 3) * (12 - frame) * 1.5 : 0;
  const reveal = useSpring(Math.round(dur * 0.45), 11);
  return (
    <Bg>
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", gap: 80, padding: 90, textAlign: "center" }}>
        <div style={{ transform: `scale(${zoom}) translateX(${shake}px)` }}>
          <div style={{ fontSize: 80, fontWeight: 700, color: COLORS.muted }}>جرّبت أسوّي فيديو</div>
          <div style={{ fontSize: 120, fontWeight: 900, lineHeight: 1.2 }}>
            بـ <span style={{ color: COLORS.orange, direction: "ltr", display: "inline-block" }}>Claude Code</span>
          </div>
        </div>
        <div style={{ display: "flex", gap: 30, opacity: reveal, transform: `translateY(${(1 - reveal) * 80}px)` }}>
          {["❌", "❌", "✅"].map((e, i) => (
            <div key={i} style={{ width: 220, height: 300, borderRadius: 30, background: "#211c18", border: `4px solid ${i === 2 ? COLORS.green : "#3a322b"}`, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 110 }}>
              {e}
            </div>
          ))}
        </div>
        <div style={{ fontSize: 96, fontWeight: 900, opacity: reveal, transform: `scale(${0.6 + reveal * 0.4})` }}>
          وهذا اللي <span style={{ color: COLORS.orange }}>صار</span> 👇
        </div>
      </AbsoluteFill>
    </Bg>
  );
};

/* 2 — ATTEMPT 1: no skill → disappointing result */
export const JTry1: React.FC<SceneProps> = ({ dur }) => {
  const frame = useCurrentFrame();
  const stamp = useSpring(Math.round(dur * 0.62), 12);
  const flicker = 0.85 + Math.sin(frame * 1.7) * 0.05;
  return (
    <Bg>
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", gap: 70, padding: 90 }}>
        <AttemptTag n={1} />
        <Pop delay={15}>
          <div style={{ fontSize: 56, color: COLORS.muted, textAlign: "center" }}>
            بدون أي <span style={{ color: COLORS.cream, fontWeight: 900 }}>سكل</span> أو إضافة
          </div>
        </Pop>
        <Pop delay={30} style={{ position: "relative", display: "flex", alignItems: "center", justifyContent: "center" }}>
          {/* deliberately bland "first result" */}
          <div style={{ width: 760, height: 760, background: "#d9d9d9", opacity: flicker, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 30, direction: "ltr", filter: "grayscale(1)" }}>
            <div style={{ fontFamily: "serif", fontSize: 70, color: "#333" }}>My Video</div>
            <div style={{ fontFamily: "serif", fontSize: 36, color: "#666" }}>Lorem ipsum text here</div>
            <div style={{ width: 300, height: 30, background: "#999" }} />
          </div>
          <div style={{ position: "absolute" }}>
            <Stamp s={stamp} color="#E5484D">مو النتيجة اللي أبيها</Stamp>
          </div>
        </Pop>
      </AbsoluteFill>
    </Bg>
  );
};

/* 3 — SEARCH → enable Remotion */
const QUERY = "كيف أسوي فيديو احترافي بكلود كود؟";
export const JSearch: React.FC<SceneProps> = ({ dur }) => {
  const frame = useCurrentFrame();
  const typed = Array.from(QUERY).slice(0, Math.max(0, Math.floor((frame - 8) / 1.2))).join("");
  const resultAt = Math.round(dur * 0.45);
  const toggleAt = Math.round(dur * 0.68);
  const toggle = useSpring(toggleAt, 12);
  return (
    <Bg>
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", gap: 70, padding: 90 }}>
        <Pop>
          <div style={{ fontSize: 90, fontWeight: 900 }}>بعدها بحثت... 🔍</div>
        </Pop>
        <Pop delay={5} style={{ width: "100%" }}>
          <div style={{ background: COLORS.cream, color: COLORS.bg, borderRadius: 999, padding: "34px 50px", fontSize: 48, fontWeight: 700, minHeight: 64, display: "flex", alignItems: "center", gap: 24 }}>
            <span>🔍</span>
            <span>{typed}</span>
            <span style={{ opacity: Math.floor(frame / 12) % 2 ? 0 : 1, color: COLORS.orange }}>|</span>
          </div>
        </Pop>
        <Pop delay={resultAt} style={{ width: "100%" }}>
          <div style={{ background: "#211c18", borderRadius: 40, padding: 50, border: `4px solid ${toggle > 0.5 ? COLORS.orange : "#3a322b"}`, display: "flex", alignItems: "center", gap: 40 }}>
            <Spark size={130} rotate={frame * 2} />
            <div style={{ flex: 1 }}>
              <div style={{ fontSize: 80, fontWeight: 900, direction: "ltr", textAlign: "right" }}>Remotion</div>
              <div style={{ fontSize: 44, color: COLORS.muted }}>إضافة (Skill) لصناعة الفيديو بالكود</div>
            </div>
            {/* toggle switch */}
            <div style={{ width: 170, height: 94, borderRadius: 47, background: toggle > 0.5 ? COLORS.orange : "#3a322b", position: "relative", direction: "ltr" }}>
              <div style={{ position: "absolute", top: 9, left: 9 + toggle * 76, width: 76, height: 76, borderRadius: 38, background: COLORS.cream }} />
            </div>
          </div>
        </Pop>
        <div style={{ fontSize: 64, fontWeight: 900, color: COLORS.green, opacity: toggle, transform: `scale(${toggle})` }}>تم التفعيل ✓</div>
      </AbsoluteFill>
    </Bg>
  );
};

/* 4 — ATTEMPT 2: pretty but silent */
export const JTry2: React.FC<SceneProps> = ({ dur }) => {
  const frame = useCurrentFrame();
  const muteAt = Math.round(dur * 0.55);
  const mute = useSpring(muteAt, 10);
  const desat = interpolate(frame, [muteAt, muteAt + 15], [0, 0.6], clamp);
  return (
    <Bg>
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", gap: 70, padding: 90 }}>
        <AttemptTag n={2} />
        <Pop delay={10} style={{ position: "relative" }}>
          <div style={{ width: 760, height: 760, borderRadius: 50, overflow: "hidden", position: "relative", filter: `saturate(${1 - desat}) brightness(${1 - desat * 0.4})`, background: `linear-gradient(135deg, ${COLORS.orange}, #7b3fa0)` }}>
            {Array.from({ length: 6 }).map((_, i) => (
              <div key={i} style={{ position: "absolute", width: 160 + i * 30, height: 160 + i * 30, borderRadius: "50%", border: "6px solid rgba(255,255,255,.35)", left: 380 + Math.cos(frame / 20 + i) * 220 - 80 - i * 15, top: 380 + Math.sin(frame / 25 + i * 1.3) * 220 - 80 - i * 15 }} />
            ))}
            <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", fontSize: 130, fontWeight: 900, color: "white", textShadow: "0 10px 40px rgba(0,0,0,.4)" }}>
              ✨ حلو!
            </AbsoluteFill>
          </div>
          <div style={{ position: "absolute", right: -30, bottom: -30, transform: `scale(${mute})`, opacity: mute, width: 200, height: 200, borderRadius: 100, background: "#E5484D", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 110, boxShadow: "0 20px 60px rgba(0,0,0,.5)" }}>
            🔇
          </div>
        </Pop>
        <div style={{ fontSize: 84, fontWeight: 900, opacity: mute, transform: `translateY(${(1 - mute) * 40}px)` }}>
          بس... <span style={{ color: "#E5484D" }}>بدون صوت</span>
        </div>
      </AbsoluteFill>
    </Bg>
  );
};

/* 5 — CONNECT ElevenLabs */
export const JConnect: React.FC<SceneProps> = ({ dur }) => {
  const frame = useCurrentFrame();
  const link = interpolate(frame, [10, dur * 0.7], [0, 1], clamp);
  const done = link >= 1;
  const Node: React.FC<{ label: string; color: string }> = ({ label, color }) => (
    <div style={{ width: 760, padding: "50px 0", borderRadius: 40, background: "#211c18", border: `5px solid ${color}`, textAlign: "center", fontSize: 84, fontWeight: 900, color, direction: "ltr", boxShadow: done ? `0 0 80px ${color}55` : "none" }}>
      {label}
    </div>
  );
  return (
    <Bg>
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", gap: 0, padding: 90 }}>
        <Pop><div style={{ fontSize: 76, fontWeight: 900, marginBottom: 70 }}>رجعت وربطت 🔌</div></Pop>
        <Pop delay={3}><Node label="Claude Code" color={COLORS.orange} /></Pop>
        <div style={{ height: 300, width: 16, position: "relative", background: "#2f2823", borderRadius: 8 }}>
          <div style={{ position: "absolute", top: 0, width: "100%", height: `${link * 100}%`, borderRadius: 8, background: `linear-gradient(${COLORS.orange}, ${COLORS.cream})` }} />
          <div style={{ position: "absolute", left: -22, top: `calc(${link * 100}% - 30px)`, width: 60, height: 60, borderRadius: 30, background: COLORS.cream, boxShadow: `0 0 40px ${COLORS.orange}` }} />
        </div>
        <Pop delay={8}><Node label="ElevenLabs" color={COLORS.cream} /></Pop>
        <div style={{ display: "flex", gap: 12, alignItems: "center", height: 160, marginTop: 60, opacity: done ? 1 : 0.15 }}>
          {Array.from({ length: 24 }).map((_, i) => (
            <div key={i} style={{ width: 16, borderRadius: 8, background: i % 3 ? COLORS.orange : COLORS.cream, height: done ? 30 + Math.abs(Math.sin(frame / 3 + i * 0.8)) * 130 : 20 }} />
          ))}
        </div>
      </AbsoluteFill>
    </Bg>
  );
};

/* 6 — RESULT: the first video, playing in a phone */
export const JResult: React.FC<SceneProps> = () => {
  const frame = useCurrentFrame();
  const phone = useSpring(4, 13);
  const title = useSpring(30, 9);
  return (
    <Bg>
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", gap: 60, padding: 90 }}>
        <AttemptTag n={3} ok />
        <div style={{ transform: `translateY(${(1 - phone) * 300}px) rotate(${(1 - phone) * 8}deg)`, opacity: phone, position: "relative" }}>
          <div style={{ width: 560, height: 996, borderRadius: 70, background: "#000", padding: 18, boxShadow: `0 0 0 6px #3a322b, 0 40px 140px ${COLORS.orange}55` }}>
            <div style={{ width: "100%", height: "100%", borderRadius: 54, overflow: "hidden" }}>
              <OffthreadVideo src={staticFile("v1-clip.mp4")} muted style={{ width: "100%", height: "100%", objectFit: "cover" }} />
            </div>
          </div>
          {[[-90, 80], [600, 200], [-60, 820], [610, 900]].map(([x, y], i) => (
            <div key={i} style={{ position: "absolute", left: x, top: y, opacity: title }}>
              <Spark size={90} rotate={frame * (i % 2 ? 3 : -3)} color={i % 2 ? COLORS.cream : COLORS.orange} />
            </div>
          ))}
        </div>
        <div style={{ fontSize: 100, fontWeight: 900, transform: `scale(${title})`, opacity: title }}>
          فيديو <span style={{ color: COLORS.orange }}>رائع!</span> 🔥
        </div>
      </AbsoluteFill>
    </Bg>
  );
};

/* 7 — OUTRO: the lesson + CTA */
export const JOutro: React.FC<SceneProps> = ({ dur }) => {
  const frame = useCurrentFrame();
  const t = (p: number) => Math.round(dur * p);
  const steps = [
    { e: "❌", l: "بدون سكل" },
    { e: "✨", l: "+ Remotion" },
    { e: "🔊", l: "+ ElevenLabs" },
    { e: "🎬", l: "النتيجة" },
  ];
  const lesson = useSpring(t(0.08), 12);
  const cta = useSpring(t(0.7), 10);
  const pulse = 1 + Math.sin(frame / 6) * 0.04;
  return (
    <Bg>
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", gap: 70, padding: 90, textAlign: "center" }}>
        <div style={{ opacity: lesson, transform: `translateY(${(1 - lesson) * 50}px)` }}>
          <div style={{ fontSize: 60, color: COLORS.muted, fontWeight: 700 }}>الدرس اللي تعلمته</div>
          <div style={{ fontSize: 80, fontWeight: 900, lineHeight: 1.35, marginTop: 20, whiteSpace: "nowrap" }}>
            الأداة لحالها ما تكفي...
            <br />
            السر في <span style={{ color: COLORS.orange }}>الإضافات الصح</span>
          </div>
        </div>
        <div style={{ display: "flex", gap: 20, justifyContent: "center" }}>
          {steps.map((s, i) => (
            <Pop key={s.l} delay={t(0.3) + i * 10}>
              <div style={{ width: 205, padding: "28px 0", borderRadius: 30, background: i === 3 ? COLORS.orange : "#211c18", color: i === 3 ? COLORS.bg : COLORS.cream }}>
                <div style={{ fontSize: 80 }}>{s.e}</div>
                <div style={{ fontSize: 34, fontWeight: 900, direction: i === 1 || i === 2 ? "ltr" : "rtl" }}>{s.l}</div>
              </div>
            </Pop>
          ))}
        </div>
        <Pop delay={t(0.45)}>
          <div style={{ fontSize: 56, color: COLORS.muted, lineHeight: 1.5 }}>كل محاولة فاشلة... كانت خطوة للنتيجة</div>
        </Pop>
        <div style={{ opacity: cta, transform: `scale(${cta * pulse})`, fontSize: 64, fontWeight: 900, background: COLORS.orange, color: COLORS.bg, padding: "36px 70px", borderRadius: 999 }}>
          جرّبها بنفسك وقلّي وش بتسوّي 👇
        </div>
      </AbsoluteFill>
    </Bg>
  );
};

