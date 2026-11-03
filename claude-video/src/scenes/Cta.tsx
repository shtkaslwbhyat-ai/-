import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { COLORS } from "../config";
import { Bg, Pop, Spark } from "../theme";

export const Cta: React.FC = () => {
  const frame = useCurrentFrame();
  const pulse = 1 + Math.sin(frame / 6) * 0.04;
  return (
    <Bg>
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", gap: 70, padding: 90, textAlign: "center" }}>
        <Spark size={200} rotate={frame * 1.5} />
        <Pop delay={5}>
          <div style={{ fontSize: 100, fontWeight: 900, lineHeight: 1.3 }}>
            أنت عليك <span style={{ color: COLORS.orange }}>الفكرة</span>
          </div>
        </Pop>
        <Pop delay={45}>
          <div style={{ fontSize: 100, fontWeight: 900, lineHeight: 1.3 }}>والباقي على كلود</div>
        </Pop>
        <Pop delay={90}>
          <div style={{ transform: `scale(${pulse})`, fontSize: 64, fontWeight: 900, background: COLORS.orange, color: COLORS.bg, padding: "36px 80px", borderRadius: 999 }}>
            جرّبها اليوم 🚀
          </div>
        </Pop>
        <Pop delay={120}>
          <div style={{ fontSize: 52, color: COLORS.muted }}>تابعني لأفكار أكثر</div>
        </Pop>
      </AbsoluteFill>
    </Bg>
  );
};
