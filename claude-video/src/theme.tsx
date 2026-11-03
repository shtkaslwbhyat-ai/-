import React from "react";
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import "@fontsource/cairo/400.css";
import "@fontsource/cairo/700.css";
import "@fontsource/cairo/900.css";
import "@fontsource/jetbrains-mono/400.css";
import "@fontsource/jetbrains-mono/700.css";
import { COLORS } from "./config";

export const fontFamily = "'Cairo', 'Noto Color Emoji', sans-serif";
export const monoFamily = "'JetBrains Mono', monospace";

export const useSpring = (delay = 0, damping = 14) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return spring({ frame: frame - delay, fps, config: { damping } });
};

export const Bg: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const frame = useCurrentFrame();
  const angle = interpolate(frame, [0, 300], [0, 40]);
  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(circle at 50% ${35 + Math.sin(frame / 40) * 6}%, ${COLORS.bg2} 0%, ${COLORS.bg} 70%)`,
        fontFamily,
        direction: "rtl",
        color: COLORS.cream,
        overflow: "hidden",
      }}
    >
      <AbsoluteFill
        style={{
          opacity: 0.08,
          backgroundImage: `repeating-linear-gradient(${angle}deg, ${COLORS.orange} 0 2px, transparent 2px 80px)`,
        }}
      />
      {children}
    </AbsoluteFill>
  );
};

export const Pop: React.FC<{ delay?: number; children: React.ReactNode; style?: React.CSSProperties }> = ({
  delay = 0,
  children,
  style,
}) => {
  const s = useSpring(delay);
  return (
    <div style={{ transform: `translateY(${(1 - s) * 60}px) scale(${0.85 + s * 0.15})`, opacity: s, ...style }}>
      {children}
    </div>
  );
};

export const StepBadge: React.FC<{ n: number; label: string }> = ({ n, label }) => (
  <Pop style={{ display: "flex", alignItems: "center", gap: 28, justifyContent: "center" }}>
    <div
      style={{
        width: 120, height: 120, borderRadius: 60, background: COLORS.orange, color: COLORS.bg,
        fontSize: 72, fontWeight: 900, display: "flex", alignItems: "center", justifyContent: "center",
      }}
    >
      {n}
    </div>
    <div style={{ fontSize: 84, fontWeight: 900 }}>{label}</div>
  </Pop>
);

export const Spark: React.FC<{ size: number; color?: string; rotate?: number }> = ({ size, color = COLORS.orange, rotate = 0 }) => (
  <svg width={size} height={size} viewBox="0 0 100 100" style={{ transform: `rotate(${rotate}deg)` }}>
    {Array.from({ length: 8 }).map((_, i) => (
      <rect key={i} x="46" y="4" width="8" height="46" rx="4" fill={color} transform={`rotate(${i * 45} 50 50)`} />
    ))}
  </svg>
);
