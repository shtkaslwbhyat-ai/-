import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { COLORS } from "../config";
import { Bg, Pop, Spark } from "../theme";

const Brand: React.FC<{ name: string; sub: string; color: string; delay: number }> = ({ name, sub, color, delay }) => (
  <Pop delay={delay}>
    <div style={{ background: "#211c18", border: `4px solid ${color}`, borderRadius: 48, padding: "50px 70px", textAlign: "center", width: 760 }}>
      <div style={{ fontSize: 96, fontWeight: 900, color, direction: "ltr" }}>{name}</div>
      <div style={{ fontSize: 48, color: COLORS.muted, marginTop: 10 }}>{sub}</div>
    </div>
  </Pop>
);

export const Reveal: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Bg>
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", gap: 60 }}>
        <Pop>
          <div style={{ fontSize: 96, fontWeight: 900, textAlign: "center" }}>هذا الفيديو؟</div>
        </Pop>
        <Pop delay={20}>
          <div style={{ fontSize: 56, color: COLORS.muted }}>انصنع بالكامل عن طريق</div>
        </Pop>
        <Brand name="Claude Code" sub="الكود والمونتاج" color={COLORS.orange} delay={35} />
        <Pop delay={95}>
          <div style={{ fontSize: 90, fontWeight: 900, color: COLORS.muted }}>+</div>
        </Pop>
        <Brand name="ElevenLabs" sub="الصوت" color={COLORS.cream} delay={110} />
      </AbsoluteFill>
      <div style={{ position: "absolute", bottom: 160, right: 120 }}>
        <Spark size={90} rotate={-frame * 2} />
      </div>
    </Bg>
  );
};
