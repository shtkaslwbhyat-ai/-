import React from "react";
import { Composition } from "remotion";
import { FPS } from "./config";
import { ClaudeCodeVideo, calculateMetadata } from "./Video";

export const RemotionRoot: React.FC = () => (
  <Composition
    id="ClaudeCodeVideo"
    component={ClaudeCodeVideo}
    durationInFrames={1500}
    fps={FPS}
    width={1080}
    height={1920}
    defaultProps={{ scenes: [] }}
    calculateMetadata={calculateMetadata}
  />
);
