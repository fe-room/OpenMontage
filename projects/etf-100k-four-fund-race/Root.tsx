import React from "react";
import { Composition } from "remotion";
import { Film, DURATION } from "./Composition";
import { HEIGHT, WIDTH, FPS } from "./timeline";

export const Root: React.FC = () => (
  <Composition
    id="EtfFourFundRace"
    component={Film}
    durationInFrames={DURATION}
    fps={FPS}
    width={WIDTH}
    height={HEIGHT}
  />
);
