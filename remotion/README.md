# Higgsfield explainer (Remotion)

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
