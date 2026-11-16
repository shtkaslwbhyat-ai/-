import {Composition} from 'remotion';
import {CinnamonVideo, TOTAL} from './Video';

export const Root = () => (
  <Composition
    id="Cinnamon"
    component={CinnamonVideo}
    durationInFrames={TOTAL}
    fps={30}
    width={1920}
    height={1080}
  />
);
