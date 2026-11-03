// Scene timing (seconds), synced to public/influencer/voiceover.mp3.
// `cues` are absolute times of the beats inside a scene, in the order the scene uses them.
export type SceneTiming = { id: SceneId; start: number; end: number; cues: number[] };
export type SceneId = "hook" | "title" | "builder" | "face" | "soul" | "limits" | "cta";

export const SCENES: SceneTiming[] = [
  // cues: profile in, posts in, counter start, glitch reveal
  { id: "hook", start: 0, end: 7.9, cues: [0.1, 0.9, 1.0, 6.22] },
  // cues: title, subtitle
  { id: "title", start: 7.9, end: 14.8, cues: [8.3, 11.8] },
  // cues: panel, 5 attribute rows, 3 tabs, no-prompt stamp
  { id: "builder", start: 14.8, end: 27.0, cues: [15.1, 17.74, 18.5, 19.2, 20.04, 20.9, 22.0, 22.8, 23.6, 24.93] },
  // cues: dropzone, photo drops, lock, trait chips
  { id: "face", start: 27.0, end: 33.3, cues: [27.1, 28.27, 30.1, 31.4] },
  // cues: portraits, training ring start, Soul ID done, outputs
  { id: "soul", start: 33.3, end: 46.5, cues: [37.3, 39.6, 41.6, 42.4] },
  // cues: front ok, side, lighting, outfit/background, credits
  { id: "limits", start: 46.5, end: 61.6, cues: [48.2, 50.4, 51.8, 55.5, 58.6] },
  // cues: question, keyword box, DM line
  { id: "cta", start: 61.6, end: 68, cues: [62.0, 63.3, 65.1] },
];

export const DURATION_SECONDS = SCENES[SCENES.length - 1].end;

export type SfxType = "whoosh" | "pop" | "ding" | "glitch" | "tick" | "success" | "drop";
export type SfxEvent = { type: SfxType; t: number; volume: number };

const cue = (id: SceneId, i: number) => SCENES.find((s) => s.id === id)!.cues[i];

export const SFX: SfxEvent[] = [
  ...SCENES.slice(1).map((s) => ({ type: "whoosh" as const, t: Math.max(0, s.start - 0.25), volume: 0.45 })),
  { type: "pop", t: cue("hook", 0), volume: 0.3 },
  { type: "pop", t: cue("hook", 1), volume: 0.3 },
  // follower counter ticks
  ...Array.from({ length: 12 }, (_, i) => ({ type: "tick" as const, t: cue("hook", 2) + i * 0.22, volume: 0.18 })),
  { type: "glitch", t: cue("hook", 3), volume: 0.5 },
  { type: "pop", t: cue("title", 1), volume: 0.3 },
  ...SCENES.find((s) => s.id === "builder")!.cues.slice(1, 9).map((t) => ({ type: "pop" as const, t, volume: 0.3 })),
  { type: "drop", t: cue("builder", 9), volume: 0.5 },
  { type: "drop", t: cue("face", 1) + 0.25, volume: 0.5 },
  { type: "ding", t: cue("face", 2), volume: 0.35 },
  { type: "pop", t: cue("face", 3), volume: 0.3 },
  ...Array.from({ length: 10 }, (_, i) => ({ type: "tick" as const, t: cue("soul", 1) + i * 0.24, volume: 0.15 })),
  { type: "success", t: cue("soul", 2), volume: 0.45 },
  { type: "pop", t: cue("soul", 3), volume: 0.3 },
  ...SCENES.find((s) => s.id === "limits")!.cues.map((t) => ({ type: "pop" as const, t, volume: 0.3 })),
  { type: "ding", t: cue("cta", 1), volume: 0.4 },
];
