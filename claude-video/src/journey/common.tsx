import React from "react";
import { COLORS } from "../config";
import { Pop } from "../theme";

export type SceneProps = { dur: number };

// "المحاولة X" chip with 3 progress dots — ties the journey together.
export const AttemptTag: React.FC<{ n: 1 | 2 | 3; ok?: boolean }> = ({ n, ok }) => (
  <Pop style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 24 }}>
    <div
      style={{
        fontSize: 56, fontWeight: 900, padding: "18px 48px", borderRadius: 999,
        background: ok ? COLORS.green : "#2f2823", color: ok ? COLORS.bg : COLORS.cream,
      }}
    >
      المحاولة {["الأولى", "الثانية", "الثالثة"][n - 1]}
    </div>
    <div style={{ display: "flex", gap: 18 }}>
      {[1, 2, 3].map((i) => (
        <div key={i} style={{ width: i === n ? 70 : 24, height: 24, borderRadius: 12, background: i <= n ? COLORS.orange : "#3a322b" }} />
      ))}
    </div>
  </Pop>
);

export const Stamp: React.FC<{ s: number; color: string; children: React.ReactNode }> = ({ s, color, children }) => (
  <div
    style={{
      transform: `rotate(-8deg) scale(${2.4 - 1.4 * s})`, opacity: s, border: `10px solid ${color}`, color,
      fontSize: 66, fontWeight: 900, whiteSpace: "nowrap", padding: "20px 50px", borderRadius: 30, background: "rgba(20,18,16,.85)",
    }}
  >
    {children}
  </div>
);
