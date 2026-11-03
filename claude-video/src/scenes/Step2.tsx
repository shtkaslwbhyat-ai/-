import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { COLORS } from "../config";
import { Bg, Pop, StepBadge } from "../theme";

const ITEMS = ["✍️  يكتب السكربت", "🎙️  يختار الصوت المناسب", "🔊  يولّد التعليق الصوتي"];

export const Step2: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Bg>
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", gap: 70, padding: 90 }}>
        <StepBadge n={2} label="السكربت والصوت" />
        <div style={{ display: "flex", flexDirection: "column", gap: 36, width: "100%" }}>
          {ITEMS.map((t, i) => (
            <Pop key={t} delay={25 + i * 45}>
              <div style={{ fontSize: 62, fontWeight: 700, background: "#211c18", borderRadius: 32, padding: "40px 50px", borderRight: `12px solid ${COLORS.orange}` }}>
                {t}
              </div>
            </Pop>
          ))}
        </div>
        <Pop delay={150}>
          <div style={{ display: "flex", gap: 14, alignItems: "center", height: 220 }}>
            {Array.from({ length: 28 }).map((_, i) => {
              const h = 30 + Math.abs(Math.sin(frame / 4 + i * 0.7) * Math.cos(frame / 9 + i)) * 180;
              return <div key={i} style={{ width: 18, height: h, borderRadius: 9, background: i % 3 ? COLORS.orange : COLORS.cream }} />;
            })}
          </div>
        </Pop>
        <Pop delay={160}>
          <div style={{ fontSize: 48, color: COLORS.muted, direction: "ltr" }}>ElevenLabs ✓</div>
        </Pop>
      </AbsoluteFill>
    </Bg>
  );
};
