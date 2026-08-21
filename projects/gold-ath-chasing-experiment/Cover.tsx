import React from "react";
import {AbsoluteFill} from "remotion";

const C = {
  bg: "#090A0C",
  paper: "#F2EBDD",
  muted: "#8F8B82",
  gold: "#B58A3A",
  goldBright: "#E0B85D",
  red: "#A9473F",
  line: "#2A2926",
};

const fineDots = Array.from({length: 199}, (_, i) => i);
const groups = [18, 25, 32, 21, 29, 19, 31, 24];

export const Cover: React.FC = () => {
  return (
    <AbsoluteFill
      style={{
        overflow: "hidden",
        color: C.paper,
        background: C.bg,
        fontFamily: '"PingFang SC","Hiragino Sans GB",sans-serif',
      }}
    >
      <div
        style={{
          position: "absolute",
          inset: 0,
          background:
            "radial-gradient(circle at 86% 16%, rgba(181,138,58,.18), transparent 30%), radial-gradient(circle at 12% 84%, rgba(169,71,63,.10), transparent 32%), linear-gradient(145deg, #0D0E11 0%, #08090B 65%, #11100D 100%)",
        }}
      />
      <div
        style={{
          position: "absolute",
          inset: 0,
          opacity: 0.34,
          backgroundImage:
            "linear-gradient(rgba(255,255,255,.035) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,.035) 1px, transparent 1px)",
          backgroundSize: "54px 54px",
        }}
      />

      <main style={{position: "absolute", inset: "68px 72px 72px"}}>
        <header style={{display: "flex", alignItems: "center", gap: 18}}>
          <div style={{width: 48, height: 4, background: C.goldBright}} />
          <div
            style={{
              color: C.goldBright,
              fontSize: 25,
              fontWeight: 750,
              letterSpacing: 5,
            }}
          >
            GOLD · HISTORICAL TEST
          </div>
          <div style={{marginLeft: "auto", color: C.muted, fontSize: 22}}>
            2001—2026
          </div>
        </header>

        <section style={{marginTop: 82}}>
          <div
            style={{
              fontFamily: '"Songti SC","STSong",serif',
              fontSize: 96,
              fontWeight: 700,
              lineHeight: 1.17,
              letterSpacing: -3,
            }}
          >
            黄金创新高后，
            <br />
            <span style={{color: C.goldBright}}>还能不能买？</span>
          </div>
          <div
            style={{
              marginTop: 30,
              width: 640,
              height: 5,
              background: `linear-gradient(90deg, ${C.goldBright}, ${C.red} 76%, transparent)`,
            }}
          />
        </section>

        <section
          style={{
            marginTop: 86,
            height: 570,
            border: `1px solid ${C.line}`,
            background: "rgba(15,16,18,.84)",
            padding: "48px 48px 42px",
            position: "relative",
          }}
        >
          <div style={{display: "flex", alignItems: "baseline", gap: 18}}>
            <span style={{fontSize: 118, fontWeight: 850, color: C.goldBright, letterSpacing: -7}}>
              199
            </span>
            <span style={{fontSize: 33, fontWeight: 650}}>个新高日</span>
            <span style={{marginLeft: "auto", color: C.muted, fontSize: 23}}>表面样本</span>
          </div>

          <div
            style={{
              marginTop: 22,
              display: "grid",
              gridTemplateColumns: "repeat(40, 1fr)",
              gap: "7px 8px",
              width: "100%",
            }}
          >
            {fineDots.map((i) => (
              <i
                key={i}
                style={{
                  display: "block",
                  width: 7,
                  height: 7,
                  borderRadius: 7,
                  background: i % 13 === 0 ? C.goldBright : C.gold,
                  opacity: i % 9 === 0 ? 1 : 0.62,
                }}
              />
            ))}
          </div>

          <div style={{height: 1, background: C.line, marginTop: 38}} />

          <div style={{display: "flex", alignItems: "center", marginTop: 28}}>
            <div style={{color: C.muted, fontSize: 22, lineHeight: 1.5}}>
              按 60 个交易日
              <br />
              去重以后
            </div>
            <div style={{width: 98, height: 2, background: C.gold, margin: "0 30px", position: "relative"}}>
              <div
                style={{
                  position: "absolute",
                  right: -2,
                  top: -5,
                  width: 10,
                  height: 10,
                  borderTop: `2px solid ${C.gold}`,
                  borderRight: `2px solid ${C.gold}`,
                  transform: "rotate(45deg)",
                }}
              />
            </div>
            <div style={{display: "flex", gap: 13, alignItems: "center"}}>
              {groups.map((n) => (
                <div
                  key={n}
                  style={{
                    width: 24,
                    height: 24,
                    borderRadius: 24,
                    border: `3px solid ${C.goldBright}`,
                    boxShadow: "0 0 18px rgba(224,184,93,.22)",
                  }}
                />
              ))}
            </div>
            <div style={{marginLeft: "auto", display: "flex", alignItems: "baseline", gap: 10}}>
              <span style={{fontSize: 88, fontWeight: 850, color: C.paper, letterSpacing: -5}}>8</span>
              <span style={{fontSize: 27, fontWeight: 650}}>次</span>
            </div>
          </div>
        </section>

        <footer
          style={{
            position: "absolute",
            left: 0,
            right: 0,
            bottom: 0,
            display: "flex",
            alignItems: "center",
            color: C.muted,
            fontSize: 23,
          }}
        >
          <span style={{color: C.paper}}>新高不是结论，历史数据也不是预言。</span>
          <span style={{marginLeft: "auto", color: C.red}}>历史回测 · 非买入建议</span>
        </footer>
      </main>
    </AbsoluteFill>
  );
};
