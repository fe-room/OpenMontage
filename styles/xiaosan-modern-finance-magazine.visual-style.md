---
name: "小散·现代财经杂志"
version: "1.0"
tags: ["finance education", "editorial", "native typography", "restrained motion"]
author: "OpenMontage"
created: "2026-09-15"
style_prompt_short: >
  冷白底色、石墨蓝文字与克制钴蓝强调；用明确照片边界、统一图文网格和自然留白，构成当代财经杂志的编辑感。
style_prompt_full: >
  Create a contemporary financial editorial magazine visual system for Chinese economics videos. Use a single cool off-white canvas #F7F8F6, navy ink #192A38, cobalt #315DE5 for structural emphasis and scarce burnt orange #DF6B3F for analytical highlights. Use PingFang SC or Noto Sans SC for native Chinese typography, one readable claim per frame. Place deliberately cropped city, industry or behavioral photography inside explicit rectangular image apertures aligned to an asymmetric eight-column grid. Plan native text zones before image generation. Main titles are 64–78px at 1080x1920; body text 28–34px, captions 22–26px. Never use opaque patches over photography to create fake whitespace, near-matching color slabs, or floating information cards obscuring image subjects. Keep main text on the common canvas, outside photo apertures; captions align with photo edges. Use hard editorial cuts and short mask reveals to advance reasoning, not constant drift. No vintage yellow paper, neon terminals, candlestick wallpaper or generic corporate slide layout. Reuse typography, palette and alignment discipline, not completed scene compositions.
colors:
  primary:
    - name: "Common Canvas"
      hex: "#F7F8F6"
      role: "one continuous ground; no patchwork text backgrounds"
    - name: "Navy Graphite"
      hex: "#192A38"
      role: "native headlines and primary explanation"
  accent:
    - name: "Structural Accent"
      hex: "#315DE5"
      role: "series identity, sparse rules and explanatory structure"
    - name: "Analytical Orange"
      hex: "#DF6B3F"
      role: "scarce emphasis; meaningful changes and control points only"
  neutral:
    - name: "Secondary Ink"
      hex: "#667681"
      role: "secondary explanation and source metadata"
    - name: "Quiet Rule"
      hex: "#C9D2D6"
      role: "hairline editorial separators"
typography:
  display:
    family: "PingFang SC, Noto Sans SC, Source Han Sans SC"
    weight: "700"
    style: "left aligned, tight but readable tracking, at most two short title lines"
  body:
    family: "PingFang SC, Noto Sans SC, Source Han Sans SC"
    weight: "400–600"
    style: "28–34px at 1080x1920; line-height 1.45–1.65"
  caption:
    family: "PingFang SC, Noto Sans SC, Source Han Sans SC"
    weight: "400–500"
    style: "22–26px at 1080x1920; quiet and readable"
  rules:
    - "Exact Chinese, data, labels and compliance are native text, never baked into AI images."
    - "One main claim per frame; do not repeat narration in multiple competing text tiers."
    - "Use actual installed fonts; package or load licensed fallback fonts for portable renders."
layout:
  grid: "Asymmetric eight-column editorial grid; 96px portrait side margins, 32px base spacing"
  alignment: "shared left anchors, deliberate negative space, ragged right"
  aspect_ratio: "9:16"
  notes:
    - "Main text uses the one canvas color; no local background rectangle to rescue unreadable overlays."
    - "Photos have deliberate boundaries and share alignment with title, caption and analytical notes."
    - "Leave at least 32px between image aperture and captions; do not crop key semantic subjects."
    - "Sample is a style specimen, not a fixed episode layout."
motion:
  transitions: ["hard editorial cut", "restrained opacity reveal", "meaningful mask reveal"]
  animation_style: >
    Photo aperture reveals and selective underline reveals advance the argument. Hold text still while it is read; no bouncing cards, ornamental zooms or perpetual drifting.
  pacing: "Readable holds; one meaningful motion event per reasoning beat."
  audio_cues: ["Optional explanatory contact sounds only; no automatic BGM or generic whooshes."]
mood:
  keywords: ["analytical", "restrained", "contemporary", "trustworthy"]
  era: "contemporary"
  cultural_reference: "financial visual journalism and contemporary editorial grids"
  avoid:
    - "opaque color patches over photos"
    - "near-matching stacked background slabs"
    - "information cards covering image subjects"
    - "identical title-photo-footer layout in every scene"
    - "neon market terminals"
assets:
  reference_images: []
  gsep_elements: []
  html_snippets: []
x_openmontage:
  reference_style: "styles/xiaosan-tactile-research-paper.visual-style.md"
  candidate_preview: "styles/references/xiaosan-modern-finance-magazine/candidate-preview.png"
  approval_status: "awaiting_user_review"
  reuse_scope: "palette, typography, material and layout rules only; never completed compositions"
  sample_dimensions: [1080, 1920]
  preview_kind: "static style specimen; motion guidance is not yet verified"
  portrait_subtitle_safe_area:
    policy: "social-ui-safe"
    left_px: 96
    right_px: 96
    bottom_px: 520
---

## Design Principles

冷白底色、石墨蓝文字与克制钴蓝强调；用明确照片边界、统一图文网格和自然留白，构成当代财经杂志的编辑感。

继承触感研究纸文件的组织方式、克制的信息层级和“复用语言，不复用成品版式”原则，
不继承纸张材质。先规划文字与主体的空间，再生成或裁切视觉资产。

这份文件覆盖宽泛财经与经济学题材，不限于利率。按题材调整信息结构；
封面、正文机制画面与结尾不应共用一套固定布局。

## OpenMontage / Remotion Mapping

- Base canvas uses one shared color token; native text remains outside semantic image subjects.
- Use Img/staticFile for local assets. Crop through explicit apertures, not background-color patches.
- Review actual rendered frames for seam visibility, subject cropping, text contrast and collision.
- Portrait burned-in subtitles preserve 96px side margins and 520px bottom clearance at 1080x1920.
- The exact finance disclaimer belongs on the final meaningful scene, not every scene.
- Reference preview is committed under styles/references rather than ignored projects/.
- This preview is pending review; do not populate approved_preview or approved_on before user confirmation.

