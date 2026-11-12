import React from "react";
import { Composition } from "remotion";
import { FPS } from "./config";
import { ClaudeCodeVideo, calculateMetadata } from "./Video";
import { JourneyVideo, calculateJourneyMetadata } from "./journey/Journey";
import { LessonsVideo, calculateLessonsMetadata } from "./lessons/Lessons";
import { ViduPromo } from "./vidu/ViduPromo";
import { Ad15, AD15_TOTAL } from "./cetaphil/Ad15";

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
    <Composition id="ViduPromo" component={ViduPromo} durationInFrames={300} fps={FPS} width={1080} height={1920} defaultProps={{ variant: "v1" as const }} />
    <Composition id="ViduPromoV2" component={ViduPromo} durationInFrames={506} fps={FPS} width={1080} height={1920} defaultProps={{ variant: "v2" as const }} />
    <Composition id="ViduPromoV3" component={ViduPromo} durationInFrames={554} fps={FPS} width={1080} height={1920} defaultProps={{ variant: "v3" as const }} />
    <Composition id="CetaphilAd15" component={Ad15} durationInFrames={AD15_TOTAL} fps={FPS} width={1080} height={1920} defaultProps={{ audio: "cetaphil/sfx15.wav" as string | null }} />
  </>
);
