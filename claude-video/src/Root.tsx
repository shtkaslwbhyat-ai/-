import React from "react";
import { Composition } from "remotion";
import { FPS } from "./config";
import { ClaudeCodeVideo, calculateMetadata } from "./Video";
import { JourneyVideo, calculateJourneyMetadata } from "./journey/Journey";
import { LessonsVideo, calculateLessonsMetadata } from "./lessons/Lessons";

export const RemotionRoot: React.FC = () => (
  <>
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
    <Composition
      id="JourneyVideo"
      component={JourneyVideo}
      durationInFrames={1500}
      fps={FPS}
      width={1080}
      height={1920}
      defaultProps={{ scenes: [] }}
      calculateMetadata={calculateJourneyMetadata}
    />
    <Composition
      id="LessonsVideo"
      component={LessonsVideo}
      durationInFrames={1500}
      fps={FPS}
      width={1080}
      height={1920}
      defaultProps={{ scenes: [] }}
      calculateMetadata={calculateLessonsMetadata}
    />
  </>
);
