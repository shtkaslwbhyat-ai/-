import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import { COLORS } from "../config";
import { Bg, Pop, Spark, useSpring } from "../theme";

// Strong hook: punchy zoom-in on "فيديو احترافي", then a timeline of editing tools gets crossed out → "0 ثانية مونتاج".
export const Hook: React.FC = () => {
  const frame = useCurrentFrame();
  const zoom = interpolate(frame, [0, 12], [2.2, 1], { extrapolateRight: "clamp" });
  const shake = frame < 14 ? Math.sin(frame * 3) * (14 - frame) : 0;
  const strike = useSpring(75, 20);
  const zero = useSpring(110, 10);
  return (
    <Bg>
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", gap: 70, padding: 100 }}>
        <div style={{ transform: `scale(${zoom}) translateX(${shake}px)`, textAlign: "center" }}>
          <div style={{ fontSize: 76, color: COLORS.muted, fontWeight: 700 }}>تخيّل...</div>
          <div style={{ fontSize: 150, fontWeight: 900, lineHeight: 1.15 }}>
            فيديو <span style={{ color: COLORS.orange }}>احترافي</span>
          </div>
        </div>
        <Pop delay={40}>
          <div style={{ position: "relative", display: "flex", gap: 30, direction: "ltr" }}>
            {["Premiere", "CapCut", "After Effects"].map((t) => (
              <div key={t} style={{ fontSize: 40, padding: "22px 34px", borderRadius: 24, background: "#2f2823", color: COLORS.muted }}>
                {t}
              </div>
            ))}
            <div
              style={{
                position: "absolute", top: "50%", left: -20, height: 14, borderRadius: 7, background: COLORS.orange,
                width: `calc(${strike * 100}% + 40px)`, transform: "rotate(-4deg)",
              }}
            />
          </div>
        </Pop>
        <div style={{ transform: `scale(${zero})`, opacity: zero, textAlign: "center" }}>
          <div style={{ fontSize: 260, fontWeight: 900, color: COLORS.orange, lineHeight: 1 }}>0</div>
          <div style={{ fontSize: 80, fontWeight: 900 }}>ثانية مونتاج!</div>
        </div>
      </AbsoluteFill>
      <div style={{ position: "absolute", top: 140, left: 110, opacity: zero }}>
        <Spark size={110} rotate={frame * 2} />
      </div>
    </Bg>
  );
};
