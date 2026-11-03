import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { COLORS } from "../config";
import { Bg, Pop, StepBadge, monoFamily } from "../theme";

const PROMPT = "سوّ لي فيديو يشرح كذا، وابدأ بهوك قوي 🔥";

export const Step1: React.FC = () => {
  const frame = useCurrentFrame();
  const chars = Math.max(0, Math.floor((frame - 70) / 1.6));
  const typed = Array.from(PROMPT).slice(0, chars).join("");
  const cursor = Math.floor(frame / 15) % 2 === 0;
  return (
    <Bg>
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", gap: 80, padding: 90 }}>
        <StepBadge n={1} label="اكتب فكرتك" />
        <Pop delay={15} style={{ width: "100%" }}>
          <div style={{ background: "#0d0b0a", borderRadius: 36, overflow: "hidden", border: "3px solid #3a322b", boxShadow: "0 40px 120px rgba(0,0,0,.5)" }}>
            <div style={{ display: "flex", gap: 16, padding: "26px 32px", background: "#221d19", direction: "ltr" }}>
              {["#ff5f57", "#febc2e", "#28c840"].map((c) => (
                <div key={c} style={{ width: 26, height: 26, borderRadius: 13, background: c }} />
              ))}
              <div style={{ fontFamily: monoFamily, fontSize: 30, color: COLORS.muted, marginLeft: 20 }}>claude</div>
            </div>
            <div style={{ padding: "50px 50px 70px", minHeight: 420 }}>
              <div style={{ fontFamily: monoFamily, fontSize: 40, color: COLORS.orange, direction: "ltr" }}>✻ Welcome to Claude Code</div>
              <div style={{ marginTop: 50, fontSize: 60, fontWeight: 700, lineHeight: 1.5 }}>
                <span style={{ color: COLORS.orange, fontFamily: monoFamily }}>{"< "}</span>
                {typed}
                <span style={{ opacity: cursor ? 1 : 0, color: COLORS.orange }}>▍</span>
              </div>
            </div>
          </div>
        </Pop>
        <Pop delay={40}>
          <div style={{ fontSize: 52, color: COLORS.muted, textAlign: "center" }}>بكلام بسيط… بدون أي خبرة برمجة</div>
        </Pop>
      </AbsoluteFill>
    </Bg>
  );
};
