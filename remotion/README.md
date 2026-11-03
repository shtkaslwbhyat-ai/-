# Higgsfield explainers (Remotion)

Two compositions: `HiggsfieldTikTok` (the platform overview) and `InfluencerTikTok` (the AI Influencer feature).

## HiggsfieldTikTok

Vertical 1080×1920 TikTok explainer: the explanation sits in the top half and an animated, talking avatar fills the bottom half. Saudi-dialect voiceover plus sound effects, no music.

## Run

```bash
npm install
npm run studio   # live preview and editing in the browser
npm run render   # writes out/higgsfield-tiktok-avatar.mp4
```

In a cloud container without a downloaded Chrome, add `--browser-executable=/opt/pw-browsers/chromium` to the commands.

## Where to edit

- `src/timeline.ts`: scene start/end times and when each element appears, all synced to the voiceover. The sound effects are derived from these times.
- `src/HiggsfieldTikTok.tsx`: the text and layout of every scene.
- `src/Avatar.tsx`: the mouth movement (driven by `public/mouth-envelope.json`), blinking and head motion.
- `public/`: the avatar image, the voiceover, the sound effects and the Cairo font.

If you change the voiceover, regenerate `public/mouth-envelope.json` (per-frame voice loudness, 0 to 1, at 30fps) and update the times in `src/timeline.ts`.

## InfluencerTikTok

A 68-second vertical explainer for Higgsfield's AI Influencer feature, made entirely in Remotion with no generated footage. The "influencer" is `public/avatar.jpg`.

```bash
npm run render:influencer   # writes out/higgsfield-ai-influencer.mp4
```

- `src/influencer/timeline.ts`: scene times and beats, synced to `public/influencer/voiceover.mp3`. The sound effects are listed here too.
- `src/influencer/InfluencerTikTok.tsx`: the seven scenes (fake profile with glitch reveal, title, Builder panel, face upload, Soul ID training, limits, call to action).

### InfluencerTikTokV2

The same video with a stronger opening: an extreme close-up with "وقّف", a follower counter, a glitch "مو إنسان" reveal and the promise "تقدر تسوّي واحد مثله". The hook has its own voice line (`public/influencer/hook-v2.mp3`), then the original narration continues from the title scene. The hook scene is `StrongHook` in `src/influencer/InfluencerTikTok.tsx`.

```bash
npm run render:influencer-v2   # writes out/higgsfield-ai-influencer-v2.mp4
```
