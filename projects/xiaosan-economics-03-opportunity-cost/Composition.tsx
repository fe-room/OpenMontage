import React from "react";
import { AbsoluteFill, Audio, Sequence, staticFile, useCurrentFrame } from "remotion";
import {
  COMPLIANCE_TEXT,
  DURATION_IN_FRAMES,
  NARRATION,
  SCENES,
  type SceneKey,
} from "./timeline";
import { Captions } from "./Captions";
import { SeriesHeader } from "./Foundation";
import { CostZeroHero, QuestionFork, RealLieIn, StrikeTheSpend, ZeroLedger } from "./ScenesOpening";
import {
  AskTheOneThing,
  DefinitionCard,
  FourHoursTitle,
  MutualExclusion,
  NameTheOpportunityCost,
  OptionCardsIn,
} from "./ScenesMechanism";
import {
  CostIsNotError,
  ExtinguishSum,
  MisreadCard,
  NoVerdictBalance,
  NotANegation,
  StrikeTheEquals,
} from "./ScenesReversal";
import {
  BoundaryTerms,
  ClosingQuestion,
  CompleteTheJudgment,
  FreeCoffeeQueue,
  ThreeVsFive,
} from "./ScenesClosing";

// ---------------------------------------------------------------------------
// 手工编排的时间轴。每一场各自构图，没有共享的场景模板。
// ---------------------------------------------------------------------------

const Visual: React.FC<{ kind: SceneKey; durationInFrames: number }> = ({
  kind,
  durationInFrames,
}) => {
  const d = durationInFrames;
  switch (kind) {
    case "RealLieIn":
      return <RealLieIn durationInFrames={d} />;
    case "CostZeroHero":
      return <CostZeroHero durationInFrames={d} />;
    case "ZeroLedger":
      return <ZeroLedger durationInFrames={d} />;
    case "StrikeTheSpend":
      return <StrikeTheSpend durationInFrames={d} />;
    case "QuestionFork":
      return <QuestionFork durationInFrames={d} />;
    case "FourHoursTitle":
      return <FourHoursTitle durationInFrames={d} />;
    case "OptionCardsIn":
      return <OptionCardsIn durationInFrames={d} />;
    case "MutualExclusion":
      return <MutualExclusion durationInFrames={d} />;
    case "AskTheOneThing":
      return <AskTheOneThing durationInFrames={d} />;
    case "NameTheOpportunityCost":
      return <NameTheOpportunityCost durationInFrames={d} />;
    case "DefinitionCard":
      return <DefinitionCard durationInFrames={d} />;
    case "NotANegation":
      return <NotANegation durationInFrames={d} />;
    case "ExtinguishSum":
      return <ExtinguishSum durationInFrames={d} />;
    case "MisreadCard":
      return <MisreadCard durationInFrames={d} />;
    case "NoVerdictBalance":
      return <NoVerdictBalance durationInFrames={d} />;
    case "CostIsNotError":
      return <CostIsNotError durationInFrames={d} />;
    case "StrikeTheEquals":
      return <StrikeTheEquals durationInFrames={d} />;
    case "FreeCoffeeQueue":
      return <FreeCoffeeQueue durationInFrames={d} />;
    case "ThreeVsFive":
      return <ThreeVsFive durationInFrames={d} />;
    case "BoundaryTerms":
      return <BoundaryTerms durationInFrames={d} />;
    case "CompleteTheJudgment":
      return <CompleteTheJudgment durationInFrames={d} />;
    case "ClosingQuestion":
      return <ClosingQuestion durationInFrames={d} complianceText={COMPLIANCE_TEXT} />;
    default:
      return <AbsoluteFill style={{ background: "#000" }} />;
  }
};

// 常驻页眉：系列感交给画面，而不是口播。
// 除结尾卡外全片可见；实拍场景切浅色变体；开场 0.4 秒淡入，不做弹跳。
const HeaderLayer: React.FC = () => {
  const frame = useCurrentFrame();
  const scene = SCENES.find(
    (sc) => frame >= sc.from && frame < sc.from + sc.durationInFrames
  );
  const tone: "ink" | "light" =
    scene?.type === "broll" || scene?.key === "FreeCoffeeQueue" ? "light" : "ink";
  // 首帧即完整可见：平台会取第 0 帧做质量判定，不能让页眉还在淡入
  return <SeriesHeader tone={tone} opacity={1} />;
};

export const Film: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: "#F4F1E8" }}>
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
    {/* 页眉：结尾卡让位给底部系列小字，不重复出现 */}
    <Sequence
      from={0}
      durationInFrames={SCENES[SCENES.length - 1].from}
      name="series-header"
    >
      <HeaderLayer />
    </Sequence>
    {/* 字幕层独立于场景，跨场不中断 */}
    <Captions />
    {/* 人声是唯一声源：全片不含音乐层 */}
    <Audio src={staticFile(NARRATION)} />
  </AbsoluteFill>
);

export const DURATION = DURATION_IN_FRAMES;
