import React from "react";
import {Composition, Still} from "remotion";
import {Scene, calculateMetadata, SceneProps} from "./Composition";
import {Cover} from "./Cover";

export const Root:React.FC=()=> <>
  <Composition id="GoldAthChasingExperiment" component={Scene} durationInFrames={5895} fps={30} width={1080} height={1920} defaultProps={{totalSeconds:196.48} satisfies SceneProps} calculateMetadata={calculateMetadata}/>
  <Still id="GoldAthCover" component={Cover} width={1080} height={1440}/>
</>;
