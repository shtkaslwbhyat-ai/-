import { Composition } from "remotion";
import { HiggsfieldTikTok, DURATION_SECONDS, FPS } from "./HiggsfieldTikTok";

export const RemotionRoot: React.FC = () => (
  <Composition
    id="HiggsfieldTikTok"
    component={HiggsfieldTikTok}
    durationInFrames={Math.round(DURATION_SECONDS * FPS)}
    fps={FPS}
    width={1080}
    height={1920}
  />
);
