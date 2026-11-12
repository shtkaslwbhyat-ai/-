import React from "react";

// Flat-illustration characters for the TV ad. Local box 300×600; scale via `size`.
export type Hair = "long" | "short" | "hijab" | "old" | "pony" | "curly";
export type CharProps = {
  x: number; y: number; size?: number; skin: string; hair: Hair; hairColor?: string; shirt: string; pants?: string;
  beard?: boolean; armL?: number; armR?: number; blink?: boolean; smile?: number; flip?: boolean; glowHands?: number; sweat?: boolean;
};

const Arm: React.FC<{ sx: number; sy: number; angle: number; color: string; skin: string; glow?: number; mirror?: boolean }> = ({ sx, sy, angle, color, skin, glow = 0, mirror }) => (
  <g transform={`rotate(${mirror ? angle : -angle} ${sx} ${sy})`}>
    <rect x={sx - 18} y={sy - 4} width={36} height={130} rx={18} fill={color} />
    <rect x={sx - 14} y={sy + 96} width={28} height={50} rx={14} fill={skin} />
    <circle cx={sx} cy={sy + 152} r={20} fill={skin} />
    {glow > 0 ? <circle cx={sx} cy={sy + 152} r={30 + glow * 14} fill="#ffffff" opacity={0.55 * glow} /> : null}
  </g>
);

export const Person: React.FC<CharProps> = ({ x, y, size = 1, skin, hair, hairColor = "#2b1d14", shirt, pants = "#34495e", beard, armL = 8, armR = 8, blink, smile = 1, flip, glowHands = 0, sweat }) => {
  const w = 300 * size, h = 600 * size;
  const hairBack = hair === "long" || hair === "pony";
  return (
    <svg width={w} height={h} viewBox="0 0 300 600" style={{ position: "absolute", left: x - w / 2, top: y - h, overflow: "visible", transform: flip ? "scaleX(-1)" : undefined }}>
      <ellipse cx={150} cy={590} rx={110} ry={14} fill="rgba(0,0,0,.12)" />
      {/* hair behind */}
      {hairBack ? <path d="M78 110 Q70 260 95 300 L205 300 Q230 260 222 110 Z" fill={hairColor} /> : null}
      {hair === "hijab" ? <path d="M62 120 Q60 30 150 28 Q240 30 238 120 Q245 230 215 260 L85 260 Q55 230 62 120 Z" fill={hairColor} /> : null}
      {/* legs */}
      <rect x={102} y={410} width={40} height={175} rx={18} fill={pants} />
      <rect x={158} y={410} width={40} height={175} rx={18} fill={pants} />
      <ellipse cx={118} cy={585} rx={30} ry={13} fill="#2c2c2c" />
      <ellipse cx={182} cy={585} rx={30} ry={13} fill="#2c2c2c" />
      {/* body */}
      <rect x={82} y={190} width={136} height={240} rx={56} fill={shirt} />
      {/* neck + head */}
      {hair !== "hijab" ? <rect x={135} y={160} width={30} height={40} rx={10} fill={skin} /> : null}
      <circle cx={150} cy={112} r={66} fill={skin} />
      {/* hair front */}
      {hair === "long" || hair === "pony" ? <path d="M84 110 Q86 44 150 42 Q214 44 216 110 Q190 70 150 72 Q110 72 84 110 Z" fill={hairColor} /> : null}
      {hair === "pony" ? <circle cx={222} cy={78} r={26} fill={hairColor} /> : null}
      {hair === "short" ? <path d="M86 104 Q86 40 150 40 Q214 40 214 104 Q206 66 150 64 Q96 66 86 104 Z" fill={hairColor} /> : null}
      {hair === "curly" ? <g fill={hairColor}>{[[100, 70], [125, 52], [155, 46], [185, 54], [205, 76], [90, 98], [212, 100]].map(([cx, cy], i) => <circle key={i} cx={cx} cy={cy} r={24} />)}</g> : null}
      {hair === "old" ? <path d="M86 112 Q84 70 104 62 Q100 92 96 118 Z M214 112 Q216 70 196 62 Q200 92 204 118 Z" fill="#e8e8e8" /> : null}
      {hair === "hijab" ? <path d="M84 120 Q86 52 150 50 Q214 52 216 120 Q205 76 150 76 Q95 76 84 120 Z" fill={hairColor} /> : null}
      {beard ? <path d={`M96 120 Q100 190 150 192 Q200 190 204 120 Q190 160 150 162 Q110 160 96 120 Z`} fill={hair === "old" ? "#e8e8e8" : hairColor} /> : null}
      {/* face */}
      <ellipse cx={126} cy={110} rx={7} ry={blink ? 1 : 8} fill="#222" />
      <ellipse cx={174} cy={110} rx={7} ry={blink ? 1 : 8} fill="#222" />
      <circle cx={112} cy={134} r={10} fill="#ff8a80" opacity={0.35} />
      <circle cx={188} cy={134} r={10} fill="#ff8a80" opacity={0.35} />
      <path d={`M130 ${140} Q150 ${140 + 16 * smile} 170 ${140}`} stroke="#5a2e1d" strokeWidth={5} fill="none" strokeLinecap="round" />
      {sweat ? <path d="M222 80 q8 14 0 22 q-8 -8 0 -22z" fill="#7fc8ff" /> : null}
      {/* arms */}
      <Arm sx={92} sy={214} angle={armL} color={shirt} skin={skin} glow={glowHands} mirror />
      <Arm sx={208} sy={214} angle={armR} color={shirt} skin={skin} glow={glowHands} />
    </svg>
  );
};

export const Sparkles: React.FC<{ x: number; y: number; t: number; color?: string }> = ({ x, y, t, color = "#ffffff" }) => (
  <svg width={240} height={240} viewBox="-120 -120 240 240" style={{ position: "absolute", left: x - 120, top: y - 120, overflow: "visible", opacity: Math.max(0, 1 - Math.abs(t - 0.5) * 2) }}>
    {Array.from({ length: 6 }).map((_, i) => {
      const a = (i / 6) * Math.PI * 2 + t * 2; const r = 30 + t * 70;
      return <path key={i} transform={`translate(${Math.cos(a) * r} ${Math.sin(a) * r}) scale(${1 - t * 0.5})`} d="M0 -14 L4 -4 L14 0 L4 4 L0 14 L-4 4 L-14 0 L-4 -4 Z" fill={color} />;
    })}
  </svg>
);
