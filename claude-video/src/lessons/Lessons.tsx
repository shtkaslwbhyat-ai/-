import React from "react";
import { Audio, CalculateMetadataFunction, Series, staticFile } from "remotion";
import { getAudioDurationInSeconds } from "@remotion/media-utils";
import { FPS, PAD_SECONDS } from "../config";
import { LESSON_SCENES, LessonSceneId } from "./config";
import { L1, L2, L3, LHook, LOutro, LResult, SceneProps } from "./scenes";

const COMPONENTS: Record<LessonSceneId, React.FC<SceneProps>> = { hook: LHook, l1: L1, l2: L2, l3: L3, result: LResult, outro: LOutro };

export type LessonsProps = { scenes: { id: LessonSceneId; durationInFrames: number; audio: string | null }[] };

export const calculateLessonsMetadata: CalculateMetadataFunction<LessonsProps> = async () => {
  const scenes = await Promise.all(
    LESSON_SCENES.map(async (s) => {
      try {
        const secs = await getAudioDurationInSeconds(staticFile(s.audio));
        return { id: s.id, audio: s.audio, durationInFrames: Math.ceil((secs + PAD_SECONDS) * FPS) };
      } catch {
        return { id: s.id, audio: null, durationInFrames: Math.ceil((s.fallbackSeconds + PAD_SECONDS) * FPS) };
      }
    }),
  );
  scenes[scenes.length - 1].durationInFrames += FPS;
  return { durationInFrames: scenes.reduce((a, s) => a + s.durationInFrames, 0), props: { scenes } };
};

export const LessonsVideo: React.FC<LessonsProps> = ({ scenes }) => (
  <Series>
    {scenes.map((s) => {
      const C = COMPONENTS[s.id];
      return (
        <Series.Sequence key={s.id} name={s.id} durationInFrames={s.durationInFrames}>
          <C dur={s.durationInFrames} />
          {s.audio ? <Audio src={staticFile(s.audio)} /> : null}
        </Series.Sequence>
      );
    })}
  </Series>
);
