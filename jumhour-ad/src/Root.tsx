import { Composition } from "remotion";
import { Ad, TOTAL } from "./ad/Ad";

export const RemotionRoot: React.FC = () => (
  <Composition
    id="JumhourAd"
    component={Ad}
    durationInFrames={TOTAL}
    fps={30}
    width={1080}
    height={1920}
    defaultProps={{ voice: false, music: false }}
  />
);
