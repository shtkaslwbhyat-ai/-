import React from "react";
import { Audio, CalculateMetadataFunction, Series, staticFile } from "remotion";
import { getAudioDurationInSeconds } from "@remotion/media-utils";
import { FPS, PAD_SECONDS } from "../config";
import { JOURNEY_SCENES, JourneySceneId } from "./config";
import { SceneProps } from "./common";
import { JConnect, JHook, JOutro, JResult, JSearch, JTry1, JTry2 } from "./scenes";

const COMPONENTS: Record<JourneySceneId, React.FC<SceneProps>> = {
  hook: JHook, try1: JTry1, search: JSearch, try2: JTry2, connect: JConnect, result: JResult, outro: JOutro,
};

export type JourneyProps = {
  scenes: { id: JourneySceneId; durationInFrames: number; audio: string | null }[];
};

export const calculateJourneyMetadata: CalculateMetadataFunction<JourneyProps> = async () => {
  const scenes = await Promise.all(
    JOURNEY_SCENES.map(async (s) => {
      try {
        const secs = await getAudioDurationInSeconds(staticFile(s.audio));
        return { id: s.id, audio: s.audio, durationInFrames: Math.ceil((secs + PAD_SECONDS) * FPS) };
      } catch {
        return { id: s.id, audio: null, durationInFrames: Math.ceil((s.fallbackSeconds + PAD_SECONDS) * FPS) };
      }
    }),
  );
  // Hold the final frame a little longer so the ending lands.
  scenes[scenes.length - 1].durationInFrames += FPS;
  return { durationInFrames: scenes.reduce((a, s) => a + s.durationInFrames, 0), props: { scenes } };
};

export const JourneyVideo: React.FC<JourneyProps> = ({ scenes }) => (
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
