import React from "react";
import { C, display } from "./theme";

export const Bean: React.FC<{ size?: number; color?: string; style?: React.CSSProperties }> = ({
  size = 60,
  color = C.coffee,
  style,
}) => (
  <svg width={size} height={size * 1.35} viewBox="0 0 40 54" style={style}>
    <ellipse cx="20" cy="27" rx="18" ry="25" fill={color} />
    <path d="M20 3 C10 18 30 34 20 51" stroke={C.espresso} strokeWidth="3.2" fill="none" strokeLinecap="round" />
  </svg>
);

/** Takeaway hot cup with branded sleeve */
export const HotCup: React.FC<{ width?: number; style?: React.CSSProperties }> = ({ width = 360, style }) => (
  <svg width={width} height={width * 1.45} viewBox="0 0 200 290" style={style}>
    <defs>
      <linearGradient id="cupBody" x1="0" x2="1">
        <stop offset="0" stopColor="#EADBC6" />
        <stop offset="0.45" stopColor={C.milk} />
        <stop offset="1" stopColor="#D9C6AC" />
      </linearGradient>
    </defs>
    <path d="M30 60 L170 60 L152 280 Q100 290 48 280 Z" fill="url(#cupBody)" />
    <rect x="14" y="36" width="172" height="28" rx="10" fill={C.roast} />
    <path d="M40 24 Q100 4 160 24 L168 38 L32 38 Z" fill={C.coffee} />
    <path d="M38 130 L162 130 L154 220 L46 220 Z" fill={C.coffee} />
    <path d="M38 130 L162 130 L161 140 L39 140 Z" fill={C.gold} />
    <path d="M46 210 L154 210 L154 220 L46 220 Z" fill={C.gold} />
    <text x="100" y="192" textAnchor="middle" fontFamily={display} fontSize="36" fill={C.cream}>
      الجمهور
    </text>
  </svg>
);

/** Iced cup with ice cubes and straw */
export const IcedCup: React.FC<{ width?: number; style?: React.CSSProperties; f?: number }> = ({
  width = 360,
  style,
  f = 0,
}) => (
  <svg width={width} height={width * 1.55} viewBox="0 0 200 310" style={style}>
    <rect x="118" y="0" width="14" height="150" rx="6" fill={C.ember} transform="rotate(12 125 75)" />
    <path d="M28 50 L172 50 L154 300 Q100 310 46 300 Z" fill="rgba(255,255,255,0.18)" stroke="rgba(255,255,255,0.6)" strokeWidth="3" />
    <path d="M38 120 L162 120 L154 296 Q100 305 46 296 Z" fill={C.caramel} />
    <path d="M36 96 L164 96 L162 124 L38 124 Z" fill={C.milk} opacity="0.9" />
    {[0, 1, 2, 3].map((i) => (
      <rect
        key={i}
        x={50 + i * 26}
        y={110 + (i % 2) * 34 + Math.sin(f / 9 + i) * 4}
        width="34"
        height="34"
        rx="7"
        fill="rgba(220,245,255,0.55)"
        stroke="rgba(255,255,255,0.85)"
        strokeWidth="2"
        transform={`rotate(${(i * 23) % 40 - 20} ${67 + i * 26} ${127 + (i % 2) * 34})`}
      />
    ))}
    <rect x="20" y="40" width="160" height="16" rx="8" fill="rgba(255,255,255,0.75)" />
  </svg>
);

export const Steam: React.FC<{ f: number; width?: number; style?: React.CSSProperties }> = ({ f, width = 220, style }) => (
  <svg width={width} height={width} viewBox="0 0 100 100" style={style}>
    {[0, 1, 2].map((i) => {
      const t = ((f + i * 14) % 45) / 45;
      return (
        <path
          key={i}
          d={`M${30 + i * 20} 95 C${20 + i * 20} 75 ${42 + i * 20} 60 ${30 + i * 20} 40 C${20 + i * 20} 25 ${38 + i * 20} 15 ${30 + i * 20} 5`}
          stroke={C.cream}
          strokeWidth="5"
          strokeLinecap="round"
          fill="none"
          opacity={Math.sin(t * Math.PI) * 0.8}
          transform={`translate(0 ${-t * 18})`}
        />
      );
    })}
  </svg>
);

/** Round brand seal */
export const Seal: React.FC<{ size?: number; spin?: number }> = ({ size = 520, spin = 0 }) => {
  return (
    <svg width={size} height={size} viewBox="0 0 300 300">
      <circle cx="150" cy="150" r="146" fill={C.gold} />
      <circle cx="150" cy="150" r="138" fill={C.espresso} />
      <g transform={`rotate(${spin} 150 150)`}>
        {Array.from({ length: 16 }).map((_, i) => (
          <g key={i} transform={`rotate(${i * 22.5} 150 150)`}>
            <ellipse cx="150" cy="31" rx="6" ry="9" fill={i % 2 ? C.gold : C.caramel} />
            <path d="M150 23 C147 28 153 34 150 39" stroke={C.espresso} strokeWidth="1.6" fill="none" />
          </g>
        ))}
      </g>
      <circle cx="150" cy="150" r="96" fill={C.cream} />
      <ellipse cx="150" cy="112" rx="17" ry="24" fill={C.coffee} />
      <path d="M150 89 C141 104 159 120 150 135" stroke={C.cream} strokeWidth="3.5" fill="none" />
      <text x="150" y="182" textAnchor="middle" fontFamily={display} fontSize="40" fill={C.espresso}>
        الجمهور
      </text>
      <text x="150" y="212" textAnchor="middle" fontFamily={display} fontSize="20" fill={C.coffee}>
        قهوة مختصة
      </text>
    </svg>
  );
};
