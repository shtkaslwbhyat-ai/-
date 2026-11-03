import { Composition } from "remotion";
import { HiggsfieldTikTok, DURATION_SECONDS, FPS } from "./HiggsfieldTikTok";
import {
  InfluencerTikTok,
  InfluencerTikTokV2,
  DURATION_SECONDS as INFLUENCER_SECONDS,
  DURATION_SECONDS_V2 as INFLUENCER_V2_SECONDS,
} from "./influencer/InfluencerTikTok";

export const RemotionRoot: React.FC = () => (
  <>
  <Composition
    id="HiggsfieldTikTok"
    component={HiggsfieldTikTok}
    durationInFrames={Math.round(DURATION_SECONDS * FPS)}
    fps={FPS}
    width={1080}
    height={1920}
  />
  <Composition
    id="InfluencerTikTok"
    component={InfluencerTikTok}
    durationInFrames={Math.round(INFLUENCER_SECONDS * FPS)}
    fps={FPS}
    width={1080}
    height={1920}
  />
  <Composition
    id="InfluencerTikTokV2"
    component={InfluencerTikTokV2}
    durationInFrames={Math.round(INFLUENCER_V2_SECONDS * FPS)}
    fps={FPS}
    width={1080}
    height={1920}
  />
  </>
);
