import React from "react";
import { AbsoluteFill, Audio, OffthreadVideo, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { COLORS } from "../config";
import { fontFamily } from "../theme";

// Commentary video: user's AI clip (muted) + ElevenLabs voiceover + synced captions + comment CTA.
const YELLOW = "#FFD84D";

type Caption = { at: number; text: string; hl?: string };

// v1 — first voice (Nasser). Timings measured from pauses in the voiceover.
const CAPTIONS: Caption[] = [
  { at: 0.0, text: "تقدر تسوّي فيديو زي ذا 👆" },
  { at: 1.6, text: "بكل سهولة" },
  { at: 2.7, text: "بنفسك 🤯" },
  { at: 3.6, text: "عن طريق موقع Vidu", hl: "Vidu" },
  { at: 5.25, text: "ارسل كلمة Vidu", hl: "Vidu" },
  { at: 6.4, text: "في التعليقات 💬" },
  { at: 7.1, text: "ويجيك الرابط عالخاص 📩" },
];
const CTA_AT = 7.1;

// v2 — 40s marketing voice (Mansour) with a scroll-stopping hook.
const CAPTIONS_V2: Caption[] = [
  { at: 0.0, text: "وقّف ثانية! ✋" },
  { at: 1.1, text: "هذي القطة..." },
  { at: 1.7, text: "ما لها وجود 😳" },
  { at: 3.3, text: "ولا كاميرا، ولا مصوّر 🎥" },
  { at: 5.0, text: "ولا ميزانية إنتاج 💸" },
  { at: 6.7, text: "فيديو كامل بالذكاء الاصطناعي 🤖" },
  { at: 8.85, text: "تسوّيه بنفسك في دقايق ⏱️" },
  { at: 10.5, text: "عن طريق موقع Vidu", hl: "Vidu" },
  { at: 12.2, text: "تبي الرابط؟ 👀" },
  { at: 13.1, text: "اكتب Vidu في التعليقات 💬", hl: "Vidu" },
  { at: 14.7, text: "ويوصلك عالخاص 📩" },
];

// v3 — opens with "اليوم تقدر تسوي مثل هالمقاطع"; shows a prompt being typed → clip.
const CAPTIONS_V3: Caption[] = [
  { at: 0.0, text: "اليوم... 📅" },
  { at: 0.65, text: "تقدر تسوّي مثل هالمقاطع 👆" },
  { at: 2.45, text: "بدون أي خبرة ❌" },
  { at: 3.78, text: "وبدون أدوات ❌" },
  { at: 5.06, text: "تكتب وصف بسيط ✍️" },
  { at: 7.06, text: "والذكاء الاصطناعي يحوّله 🤖" },
  { at: 8.27, text: "لمشهد سينمائي 🎬" },
  { at: 10.02, text: "خلال دقايق ⏱️" },
  { at: 11.41, text: "كل هذا عن طريق Vidu", hl: "Vidu" },
  { at: 13.59, text: "تبي تجرب؟ 👀" },
  { at: 14.46, text: "اكتب Vidu في التعليقات 💬", hl: "Vidu" },
  { at: 15.94, text: "وأرسل لك الرابط عالخاص 📩" },
];
const PROMPT_TEXT = "قطة عملاقة تمشي في شوارع نيويورك، تصوير سينمائي 🐈";
const PROMPT_FROM = 5.06;
const PROMPT_TO = 7.06;

type Variant = "v1" | "v2" | "v3";
const VARIANTS: Record<Variant, { captions: Caption[]; ctaAt: number; audio: string; loop: boolean; title: string; badge: string }> = {
  v1: { captions: CAPTIONS, ctaAt: CTA_AT, audio: "vidu/vo.mp3", loop: false, title: "قطة عملاقة في نيويورك 😱", badge: "مصنوعة بالذكاء الاصطناعي 🤖" },
  v2: { captions: CAPTIONS_V2, ctaAt: 13.1, audio: "vidu/vo2.mp3", loop: true, title: "هذي القطة ما لها وجود 😳", badge: "مصنوعة بالذكاء الاصطناعي 🤖" },
  v3: { captions: CAPTIONS_V3, ctaAt: 14.46, audio: "vidu/vo3.mp3", loop: true, title: "بدون خبرة ❌ بدون أدوات ❌", badge: "اكتب وصف ✍️ والباقي على الـ AI" },
};

export type ViduProps = { variant?: Variant };
const CLIP_FRAMES = 301; // 10.04s clip at 30fps

const Highlight: React.FC<{ text: string; hl?: string }> = ({ text, hl }) => {
  if (!hl) return <>{text}</>;
  const [a, b] = text.split(hl);
  return (
    <>
      {a}
      <span style={{ color: COLORS.bg, background: YELLOW, padding: "0 18px", borderRadius: 16, direction: "ltr", display: "inline-block" }}>{hl}</span>
      {b}
    </>
  );
};

const Clip: React.FC<{ style: React.CSSProperties; loop: boolean; total: number }> = ({ style, loop, total }) => {
  if (!loop) return <OffthreadVideo src={staticFile("vidu/cat.mp4")} muted style={style} />;
  // play the clip, then replay it from the start until the voice ends
  return (
    <>
      <Sequence durationInFrames={CLIP_FRAMES} layout="none">
        <OffthreadVideo src={staticFile("vidu/cat.mp4")} muted style={style} />
      </Sequence>
      <Sequence from={CLIP_FRAMES} durationInFrames={total - CLIP_FRAMES} layout="none">
        <OffthreadVideo src={staticFile("vidu/cat.mp4")} muted style={style} />
      </Sequence>
    </>
  );
};

const PromptBox: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  if (t < PROMPT_FROM - 0.2 || t > PROMPT_TO + 0.4) return null;
  const inS = spring({ frame: frame - Math.round((PROMPT_FROM - 0.2) * fps), fps, config: { damping: 13 } });
  const out = interpolate(t, [PROMPT_TO - 0.15, PROMPT_TO + 0.35], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const chars = Math.floor(interpolate(t, [PROMPT_FROM, PROMPT_TO - 0.5], [0, Array.from(PROMPT_TEXT).length], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }));
  const typed = Array.from(PROMPT_TEXT).slice(0, chars).join("");
  const pressed = t > PROMPT_TO - 0.45;
  return (
    <AbsoluteFill style={{ background: `rgba(10,8,6,${0.82 * out})`, alignItems: "center", justifyContent: "center", opacity: out }}>
      <div style={{ width: 960, background: "white", color: "#111", borderRadius: 34, padding: "30px 36px", transform: `scale(${(0.8 + inS * 0.2) * (1 + (1 - out) * 0.3)})`, boxShadow: "0 30px 80px rgba(0,0,0,.6)" }}>
        <div style={{ fontSize: 30, color: "#888", fontWeight: 700, marginBottom: 12 }}>✍️ اكتب وصف الفيديو</div>
        <div style={{ fontSize: 42, fontWeight: 700, minHeight: 112, lineHeight: 1.35 }}>
          {typed}
          <span style={{ color: COLORS.orange, opacity: Math.floor(frame / 8) % 2 ? 0 : 1 }}>|</span>
        </div>
        <div style={{ display: "flex", justifyContent: "flex-end", marginTop: 10 }}>
          <div style={{ fontSize: 36, fontWeight: 900, background: pressed ? "#111" : YELLOW, color: pressed ? YELLOW : "#111", padding: "12px 34px", borderRadius: 999, transform: `scale(${pressed ? 0.94 : 1})`, direction: "ltr" }}>
            Generate ✨
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

export const ViduPromo: React.FC<ViduProps> = ({ variant = "v1" }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const V = VARIANTS[variant];
  const v2 = V.loop;
  const CAPTIONS_USED = V.captions;
  const ctaAt = V.ctaAt;
  const flash = v2 ? interpolate(frame, [CLIP_FRAMES - 2, CLIP_FRAMES, CLIP_FRAMES + 8], [0, 0.85, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }) : 0;
  const t = frame / fps;
  const idx = CAPTIONS_USED.reduce((acc, c, i) => (t >= c.at ? i : acc), 0);
  const cap = CAPTIONS_USED[idx];
  const capIn = spring({ frame: frame - Math.round(cap.at * fps), fps, config: { damping: 12 } });
  const hook = spring({ frame, fps, config: { damping: 11 } });
  const cta = spring({ frame: frame - Math.round(ctaAt * fps), fps, config: { damping: 10 } });
  const pulse = 1 + Math.sin(frame / 5) * 0.05;
  const zoom = interpolate(frame % CLIP_FRAMES, [0, CLIP_FRAMES], [1.0, 1.08]);
  // v3: flash when the prompt "generates" the clip
  const genFlash = variant === "v3" ? interpolate(t, [PROMPT_TO - 0.05, PROMPT_TO + 0.05, PROMPT_TO + 0.4], [0, 0.9, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }) : 0;

  return (
    <AbsoluteFill style={{ background: COLORS.bg, fontFamily, direction: "rtl", color: "white", overflow: "hidden" }}>
      {/* blurred fill background from the same clip */}
      <AbsoluteFill style={{ transform: "scale(1.9)", filter: "blur(40px) brightness(.45)" }}>
        <Clip loop={v2} total={durationInFrames} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
      </AbsoluteFill>

      {/* hook */}
      <div style={{ position: "absolute", top: 150, left: 70, right: 70, textAlign: "center", transform: `scale(${0.6 + hook * 0.4})`, opacity: hook }}>
        <div style={{ fontSize: 72, fontWeight: 900, lineHeight: 1.2, whiteSpace: "nowrap", textShadow: "0 6px 30px rgba(0,0,0,.6)" }}>
          {V.title}
        </div>
        <div style={{ marginTop: 22, display: "inline-block", fontSize: 46, whiteSpace: "nowrap", fontWeight: 900, background: COLORS.orange, color: COLORS.bg, padding: "12px 36px", borderRadius: 999 }}>
          {V.badge}
        </div>
      </div>

      {/* main clip, muted */}
      <div style={{ position: "absolute", top: 600, left: 0, width: 1080, height: 608, overflow: "hidden", boxShadow: "0 30px 90px rgba(0,0,0,.6)" }}>
        <Clip loop={v2} total={durationInFrames} style={{ width: "100%", height: "100%", objectFit: "cover", transform: `scale(${zoom})` }} />
        {variant === "v3" ? <PromptBox /> : null}
        <AbsoluteFill style={{ background: "white", opacity: Math.max(flash, genFlash) }} />
      </div>

      {/* synced captions */}
      <div style={{ position: "absolute", top: 1290, left: 50, right: 50, textAlign: "center" }}>
        <div key={idx} style={{ display: "inline-block", fontSize: 62, fontWeight: 900, lineHeight: 1.3, whiteSpace: "nowrap", padding: "18px 36px", borderRadius: 30, background: "rgba(0,0,0,.55)", transform: `scale(${0.7 + capIn * 0.3}) translateY(${(1 - capIn) * 30}px)`, opacity: capIn, textShadow: "0 4px 20px rgba(0,0,0,.5)" }}>
          <Highlight text={cap.text} hl={cap.hl} />
        </div>
      </div>

      {/* comment CTA */}
      <div style={{ position: "absolute", bottom: 130, left: 0, right: 0, display: "flex", justifyContent: "center", opacity: cta, transform: `translateY(${(1 - cta) * 120}px) scale(${pulse})` }}>
        <div style={{ display: "flex", alignItems: "center", gap: 24, background: "white", color: "#111", borderRadius: 999, padding: "22px 50px", fontSize: 58, fontWeight: 900, boxShadow: "0 20px 60px rgba(0,0,0,.5)" }}>
          <span>💬 اكتب</span>
          <span style={{ background: YELLOW, padding: "0 20px", borderRadius: 14, direction: "ltr" }}>Vidu</span>
          <span>👇</span>
        </div>
      </div>

      <Audio src={staticFile(V.audio)} />
    </AbsoluteFill>
  );
};
