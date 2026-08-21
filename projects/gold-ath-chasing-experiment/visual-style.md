---
name: "Gold High-Water Marks"
version: "1.0"
created: "2026-08-21"
tags:
  - finance
  - data experiment
  - editorial motion

style_prompt_short: >
  把黄金历史价格做成一把不断抬升的“高水位刻度尺”：黑曜石底、旧金数据、风险红水下区，冷静而不煽动。

style_prompt_full: >
  A bespoke vertical financial-data film built around a rising high-water-mark ruler.
  Use Obsidian #0A0B0D as the dominant ground, Aged Gold #D6A94A for verified data
  and new-high marks, Bone #F2EBDD for readable typography, Risk Red #D85852 only
  for underwater losses, and Muted Steel #77808A for methodology notes. Typography
  is editorial Chinese sans serif: Source Han Sans SC / Noto Sans CJK SC, heavy but
  not condensed for display, regular for narration captions, tabular numerals for
  every statistic. Compose on a 6-column vertical grid with large breathing room.
  Motion should feel like evidence being uncovered: dates slide along a calibrated
  ruler, new highs click into place, clustered marks compress from 199 into 8, and
  drawdown curves sink below a zero line with physical weight. Use deliberate holds,
  precise spring settling, and one signature 'high-water compression' transformation
  at the statistical reveal. No gold bars, coins, bullion glamour, candlestick clichés,
  fake trading terminals, neon fintech gradients, or decorative AI imagery.

colors:
  primary:
    - name: "Obsidian"
      hex: "#0A0B0D"
      role: "dominant background and negative space"
    - name: "Bone"
      hex: "#F2EBDD"
      role: "primary text and chart labels"
  accent:
    - name: "Aged Gold"
      hex: "#D6A94A"
      role: "verified values, new-high signals, selected path"
    - name: "Risk Red"
      hex: "#D85852"
      role: "losses and underwater periods only"
  neutral:
    - name: "Muted Steel"
      hex: "#77808A"
      role: "sources, methodology, secondary axes"

typography:
  display:
    family: "Source Han Sans SC"
    weight: "800"
    style: "compact editorial statements, restrained line length"
  body:
    family: "Source Han Sans SC"
    weight: "400"
    style: "mobile-readable, generous line height"
  caption:
    family: "Source Han Sans SC"
    weight: "500"
    style: "small labels with tabular numerals"
  rules:
    - "All financial numbers use tabular figures"
    - "Never show more than one headline and one supporting annotation per focal region"
    - "Source and scope labels remain visible long enough to read"

layout:
  grid: "6-column vertical editorial grid with 72px safe margins"
  alignment: "mostly flush left; centered only for the 199-to-8 signature reveal"
  aspect_ratio: "9:16"
  notes:
    - "Alternate wide chart fields, intimate number close-ups, and split evidence frames"
    - "Every chart preserves units, horizon, denominator, and baseline"

motion:
  transitions:
    - "calibrated ruler travel"
    - "data-point compression"
    - "zero-line wipe"
    - "hard editorial cuts"
  animation_style: >
    Evidence-first motion with restrained springs. Objects have weight; risk falls,
    records lock upward, and grouped samples physically cluster before compression.
  pacing: "measured hook, accelerating evidence build, deliberate boundary-condition close"
  audio_cues:
    - "No background music"
    - "Optional dry ticks for new highs and one low thump for drawdown, subject to later approval"

mood:
  keywords:
    - "credible"
    - "counterintuitive"
    - "forensic"
    - "restrained"
  era: "contemporary editorial data journalism"
  cultural_reference: "financial research notebook meets precision instrument"
  avoid:
    - "gold-bar glamour imagery"
    - "green-red candlestick wallpaper"
    - "AI-generated numbers or charts"
    - "generic purple fintech gradients"
    - "continuous ticker clutter"
---

## Design Principles

1. 数据是主角，所有关键数字和图表都由构图引擎原生渲染。
2. “旧金色”只代表可追溯证据，“风险红”只代表真实下行，不做装饰。
3. 每一幕的主体不同；高水位压缩仅在“199 → 8”高潮处出现一次。
4. 结论必须和样本量、持有期、最大浮亏及数据口径同屏出现。

## Remotion Mapping

Hand-author all scenes in a project-local atelier composition. Build charts directly
with SVG/React primitives and deterministic frame interpolation. Do not import stock
scene components from the shared Remotion registry.
