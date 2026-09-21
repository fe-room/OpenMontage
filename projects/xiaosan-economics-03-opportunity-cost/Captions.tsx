import React from "react";
import { Sequence } from "remotion";
import { CAPTIONS, SUBTITLE_SAFE_BOTTOM_PX, SUBTITLE_SAFE_SIDE_PX, SCENES } from "./timeline";
import { C, FONT_SERIF } from "./theme";

// ---------------------------------------------------------------------------
// 字幕层。
// 设计原则（skills/meta/bespoke-composition.md → "Captions vs on-screen text"）：
// 画面大字永远是「提炼后的词」，字幕承担口语整句。二者含义相同但文字不同。
// 唯一例外是那些「字形本身就是这一拍」的场景（typeCarriesLine），
// 那里不重复出字幕，否则同一句话出现两遍。
// 竖屏安全区：距底 520px、距侧 96px。
// ---------------------------------------------------------------------------

const sceneTypeAt = (frame: number) => {
  for (const s of SCENES) {
    if (frame >= s.from && frame < s.from + s.durationInFrames) return s.type;
  }
  return "text_card";
};

export const Captions: React.FC = () => {
  return (
    <>
      {CAPTIONS.filter((c) => !c.typeCarriesLine).map((c) => {
        const onFootage = sceneTypeAt(c.from) === "broll";
        return (
          <Sequence
            key={c.id}
            from={c.from}
            durationInFrames={c.durationInFrames}
            name={`cap-${c.id}`}
          >
            <div
              style={{
                position: "absolute",
                left: SUBTITLE_SAFE_SIDE_PX,
                right: SUBTITLE_SAFE_SIDE_PX,
                bottom: SUBTITLE_SAFE_BOTTOM_PX,
                textAlign: "center",
                fontFamily: FONT_SERIF,
                fontSize: 46,
                lineHeight: 1.45,
                letterSpacing: 2,
                color: onFootage ? "#F6F3EA" : C.ink,
                textShadow: onFootage ? "0 3px 14px rgba(0,0,0,0.72)" : "none",
              }}
            >
              {c.text}
            </div>
          </Sequence>
        );
      })}
    </>
  );
};
