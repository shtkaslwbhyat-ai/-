import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import { COLORS } from "../config";
import { Bg, Pop, Spark, StepBadge, monoFamily } from "../theme";

const CODE = [
  ["<Sequence", COLORS.orange],
  ["  from={0}", COLORS.cream],
  ["  durationInFrames={90}>", COLORS.cream],
  ["  <Title text=\"هوك قوي\" />", COLORS.green],
  ["  <Audio src={voice} />", COLORS.green],
  ["</Sequence>", COLORS.orange],
] as const;

export const Step3: React.FC = () => {
  const frame = useCurrentFrame();
  const lines = Math.floor(interpolate(frame, [25, 120], [0, CODE.length], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }));
  return (
    <Bg>
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", gap: 70, padding: 90 }}>
        <StepBadge n={3} label="يبني المشاهد" />
        <Pop delay={10} style={{ width: "100%" }}>
          <div style={{ background: "#0d0b0a", borderRadius: 36, padding: 50, direction: "ltr", fontFamily: monoFamily, fontSize: 44, lineHeight: 1.6, border: "3px solid #3a322b", minHeight: 480 }}>
            {CODE.slice(0, lines).map(([l, c]) => (
              <div key={l} style={{ color: c, whiteSpace: "pre" }}>{l}</div>
            ))}
          </div>
        </Pop>
        <div style={{ display: "flex", gap: 40, justifyContent: "center" }}>
          {[
            { t: "حركات", delay: 130 },
            { t: "ألوان", delay: 160 },
            { t: "نصوص متزامنة", delay: 190 },
          ].map(({ t, delay }) => (
            <Pop key={t} delay={delay}>
              <div style={{ fontSize: 52, fontWeight: 900, padding: "24px 40px", borderRadius: 999, background: COLORS.orange, color: COLORS.bg }}>{t}</div>
            </Pop>
          ))}
        </div>
        <Pop delay={30}>
          <div style={{ fontSize: 50, color: COLORS.muted, direction: "ltr", display: "flex", alignItems: "center", gap: 20 }}>
            <Spark size={60} rotate={frame * 3} /> Remotion
          </div>
        </Pop>
      </AbsoluteFill>
    </Bg>
  );
};
