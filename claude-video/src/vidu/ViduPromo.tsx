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

export type ViduProps = { v2?: boolean };
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

export const ViduPromo: React.FC<ViduProps> = ({ v2 = false }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const CAPTIONS_USED = v2 ? CAPTIONS_V2 : CAPTIONS;
  const ctaAt = v2 ? 13.1 : CTA_AT;
  const flash = v2 ? interpolate(frame, [CLIP_FRAMES - 2, CLIP_FRAMES, CLIP_FRAMES + 8], [0, 0.85, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }) : 0;
  const t = frame / fps;
  const idx = CAPTIONS_USED.reduce((acc, c, i) => (t >= c.at ? i : acc), 0);
  const cap = CAPTIONS_USED[idx];
  const capIn = spring({ frame: frame - Math.round(cap.at * fps), fps, config: { damping: 12 } });
  const hook = spring({ frame, fps, config: { damping: 11 } });
  const cta = spring({ frame: frame - Math.round(ctaAt * fps), fps, config: { damping: 10 } });
  const pulse = 1 + Math.sin(frame / 5) * 0.05;
  const zoom = interpolate(frame % CLIP_FRAMES, [0, CLIP_FRAMES], [1.0, 1.08]);

  return (
    <AbsoluteFill style={{ background: COLORS.bg, fontFamily, direction: "rtl", color: "white", overflow: "hidden" }}>
      {/* blurred fill background from the same clip */}
      <AbsoluteFill style={{ transform: "scale(1.9)", filter: "blur(40px) brightness(.45)" }}>
        <Clip loop={v2} total={durationInFrames} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
      </AbsoluteFill>

      {/* hook */}
      <div style={{ position: "absolute", top: 150, left: 70, right: 70, textAlign: "center", transform: `scale(${0.6 + hook * 0.4})`, opacity: hook }}>
        <div style={{ fontSize: 72, fontWeight: 900, lineHeight: 1.2, whiteSpace: "nowrap", textShadow: "0 6px 30px rgba(0,0,0,.6)" }}>
          {v2 ? "هذي القطة ما لها وجود 😳" : "قطة عملاقة في نيويورك 😱"}
        </div>
        <div style={{ marginTop: 22, display: "inline-block", fontSize: 50, fontWeight: 900, background: COLORS.orange, color: COLORS.bg, padding: "12px 36px", borderRadius: 999 }}>
          مصنوعة بالذكاء الاصطناعي 🤖
        </div>
      </div>

      {/* main clip, muted */}
      <div style={{ position: "absolute", top: 600, left: 0, width: 1080, height: 608, overflow: "hidden", boxShadow: "0 30px 90px rgba(0,0,0,.6)" }}>
        <Clip loop={v2} total={durationInFrames} style={{ width: "100%", height: "100%", objectFit: "cover", transform: `scale(${zoom})` }} />
        <AbsoluteFill style={{ background: "white", opacity: flash }} />
      </div>

      {/* synced captions */}
      <div style={{ position: "absolute", top: 1290, left: 50, right: 50, textAlign: "center" }}>
        <div key={idx} style={{ display: "inline-block", fontSize: 72, fontWeight: 900, lineHeight: 1.3, whiteSpace: "nowrap", padding: "18px 40px", borderRadius: 30, background: "rgba(0,0,0,.55)", transform: `scale(${0.7 + capIn * 0.3}) translateY(${(1 - capIn) * 30}px)`, opacity: capIn, textShadow: "0 4px 20px rgba(0,0,0,.5)" }}>
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

      <Audio src={staticFile(v2 ? "vidu/vo2.mp3" : "vidu/vo.mp3")} />
    </AbsoluteFill>
  );
};
