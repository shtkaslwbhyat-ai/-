import React from "react";
import { Audio, CalculateMetadataFunction, Series, staticFile } from "remotion";
import { getAudioDurationInSeconds } from "@remotion/media-utils";
import { FPS, PAD_SECONDS, SCENES, SceneId } from "./config";
import { Hook } from "./scenes/Hook";
import { Reveal } from "./scenes/Reveal";
import { Step1 } from "./scenes/Step1";
import { Step2 } from "./scenes/Step2";
import { Step3 } from "./scenes/Step3";
import { Step4 } from "./scenes/Step4";
import { Cta } from "./scenes/Cta";

const COMPONENTS: Record<SceneId, React.FC> = {
  hook: Hook, reveal: Reveal, step1: Step1, step2: Step2, step3: Step3, step4: Step4, cta: Cta,
};

export type VideoProps = {
  scenes: { id: SceneId; durationInFrames: number; audio: string | null }[];
};

export const calculateMetadata: CalculateMetadataFunction<VideoProps> = async () => {
  const scenes = await Promise.all(
    SCENES.map(async (s) => {
      try {
        const secs = await getAudioDurationInSeconds(staticFile(s.audio));
        return { id: s.id, audio: s.audio, durationInFrames: Math.ceil((secs + PAD_SECONDS) * FPS) };
      } catch {
        // Clip not present yet — keep the scene, silent, at its estimated length.
        return { id: s.id, audio: null, durationInFrames: Math.ceil((s.fallbackSeconds + PAD_SECONDS) * FPS) };
      }
    }),
  );
  return {
    durationInFrames: scenes.reduce((a, s) => a + s.durationInFrames, 0),
    props: { scenes },
  };
};

export const ClaudeCodeVideo: React.FC<VideoProps> = ({ scenes }) => (
  <Series>
    {scenes.map((s) => {
      const C = COMPONENTS[s.id];
      return (
        <Series.Sequence key={s.id} name={s.id} durationInFrames={s.durationInFrames}>
          <C />
          {s.audio ? <Audio src={staticFile(s.audio)} /> : null}
        </Series.Sequence>
      );
    })}
  </Series>
);
