import React from "react";
import { AbsoluteFill, Sequence } from "remotion";
import { C } from "./theme";
import { DURATION_IN_FRAMES, SCENES, type SceneKey } from "./timeline";
import { Cast, Opening, Rules } from "./ScenesOpening";
import { Result, Turn } from "./ScenesResult";
import { Drawdown, Mechanism, Underwater } from "./ScenesEvidence";
import { Closing } from "./ScenesClosing";
import { RaceStage } from "./RaceStage";

// ---------------------------------------------------------------------------
// 手工编排的时间轴。每一场各自构图，没有共享的场景模板，也没有剪辑转场。
// 全片无音轨：不存在 Audio 元素，也没有音乐层。
// ---------------------------------------------------------------------------

const Visual: React.FC<{ kind: SceneKey; durationInFrames: number }> = ({
  kind,
  durationInFrames,
}) => {
  switch (kind) {
    case "Opening":
      return <Opening />;
    case "Cast":
      return <Cast />;
    case "Rules":
      return <Rules />;
    case "Race":
      return <RaceStage durationInFrames={durationInFrames} />;
    case "Result":
      return <Result />;
    case "Turn":
      return <Turn />;
    case "Mechanism":
      return <Mechanism />;
    case "Drawdown":
      return <Drawdown />;
    case "Underwater":
      return <Underwater />;
    case "Closing":
      return <Closing />;
    default:
      return <AbsoluteFill style={{ background: C.base }} />;
  }
};

export const Film: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: C.base }}>
    {SCENES.map((s) => (
      <Sequence
        key={s.id}
        name={s.id}
        from={s.from}
        durationInFrames={s.durationInFrames}
        premountFor={30}
      >
        <Visual kind={s.key} durationInFrames={s.durationInFrames} />
      </Sequence>
    ))}
  </AbsoluteFill>
);

export const DURATION = DURATION_IN_FRAMES;
