import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import { COLORS } from "../config";
import { Bg, Pop, StepBadge, monoFamily, useSpring } from "../theme";

export const Step4: React.FC = () => {
  const frame = useCurrentFrame();
  const p = interpolate(frame, [20, 110], [0, 100], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const done = useSpring(115, 9);
  return (
    <Bg>
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", gap: 80, padding: 90 }}>
        <StepBadge n={4} label="رندر ونشر" />
        <Pop delay={10} style={{ width: "100%" }}>
          <div style={{ fontFamily: monoFamily, direction: "ltr", fontSize: 42, color: COLORS.muted, marginBottom: 30 }}>
            $ npx remotion render
          </div>
          <div style={{ height: 60, borderRadius: 30, background: "#2f2823", overflow: "hidden" }}>
            <div style={{ height: "100%", width: `${p}%`, background: `linear-gradient(90deg, ${COLORS.orange}, #f0a27f)` }} />
          </div>
          <div style={{ fontFamily: monoFamily, fontSize: 56, marginTop: 24, textAlign: "center", direction: "ltr" }}>{Math.round(p)}%</div>
        </Pop>
        <div style={{ transform: `scale(${done})`, opacity: done, textAlign: "center" }}>
          <div style={{ fontSize: 220, lineHeight: 1 }}>🎬</div>
          <div style={{ fontSize: 84, fontWeight: 900, marginTop: 20 }}>
            <span style={{ color: COLORS.green }}>✓</span> video.mp4 جاهز
          </div>
          <div style={{ fontSize: 50, color: COLORS.muted, marginTop: 20 }}>للنشر على أي منصة</div>
        </div>
      </AbsoluteFill>
    </Bg>
  );
};
