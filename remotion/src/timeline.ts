// Scene timing (seconds), synced to public/voiceover.mp3.
// `reveals` are the absolute times each element of the scene animates in, in DOM order.
export type SceneTiming = { id: string; start: number; end: number; reveals: number[] };

export const SCENES: SceneTiming[] = [
  { id: "intro", start: 0, end: 4.4, reveals: [0.05, 0.9, 1.5, 2.7] },
  { id: "what", start: 4.4, end: 14.2, reveals: [4.5, 4.8, 12.8, 13.3] },
  { id: "features", start: 14.2, end: 29.3, reveals: [14.3, 14.5, 17.0, 18.3, 23.7, 25.6, 26.8] },
  { id: "how", start: 29.3, end: 38.8, reveals: [29.4, 31.0, 32.3, 33.5, 35.7] },
  { id: "tips", start: 38.8, end: 53.2, reveals: [38.9, 40.1, 44.3, 48.2] },
  { id: "cta", start: 53.2, end: 59.5, reveals: [53.4, 54.6, 56.2] },
];

export type SfxEvent = { type: "whoosh" | "pop" | "ding"; t: number; volume: number };

// Whoosh on every scene change, pop on every element after a scene's first, ding on the CTA keyword.
export const SFX: SfxEvent[] = SCENES.flatMap((s) => [
  { type: "whoosh" as const, t: Math.max(0, s.start - 0.25), volume: 0.5 },
  ...s.reveals.slice(1).map((t) =>
    s.id === "cta" && t === 54.6
      ? { type: "ding" as const, t, volume: 0.4 }
      : { type: "pop" as const, t, volume: 0.3 }
  ),
]);
