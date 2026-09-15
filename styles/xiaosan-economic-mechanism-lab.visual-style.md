---
name: "小散·经济机制实验室"
version: "1.0"
tags: ["finance education", "editorial", "native typography", "restrained motion"]
author: "OpenMontage"
created: "2026-09-15"
style_prompt_short: >
  冷灰实验台、玻璃与哑光金属装置，辅以深青结构色与少量橙色控制点；文字依附解释关系，不用大块背景遮挡装置。
style_prompt_full: >
  Create a restrained economic mechanism laboratory visual system for Chinese economics videos. Use a continuous cool grey environment #EDF2F2, navy graphite #192A38, petrol teal #275956 and scarce orange #DF6B3F for meaningful control points. The central hero is one coherent physical explanatory apparatus: glass reservoirs, transparent conduits, matte aluminium supports or simple balance systems selected for the actual concept. Keep contact shadows, realistic glass edges and topology legible. Generate text-free heroes with planned empty zones; add all Chinese labels, numbers and connectors natively using PingFang SC or Noto Sans SC. Title size is 60–72px at 1080x1920, body 28–34px, captions 22–26px. Let the apparatus dominate the image; native labels sit outside its silhouette and use thin non-crossing leaders only when the mapping is meaningful. For reused illustrations, blend only empty background edge zones into the common canvas through soft alpha masks; never fade the apparatus, paste opaque label blocks over it, or hide mistakes with colored cards. Distinguish metaphors from causal or quantitative evidence. Motion is a deterministic control adjustment followed by relevant flow or state changes when the explanatory mapping supports it; never imply a scientific simulation with unvalidated generated footage. Reuse material and label grammar, not a fixed device or completed layout.
colors:
  primary:
    - name: "Common Canvas"
      hex: "#EDF2F2"
      role: "one continuous ground; no patchwork text backgrounds"
    - name: "Navy Graphite"
      hex: "#192A38"
      role: "native headlines and primary explanation"
  accent:
    - name: "Structural Accent"
      hex: "#275956"
      role: "series identity, sparse rules and explanatory structure"
    - name: "Analytical Orange"
      hex: "#DF6B3F"
      role: "scarce emphasis; meaningful changes and control points only"
  neutral:
    - name: "Secondary Ink"
      hex: "#667681"
      role: "secondary explanation and source metadata"
    - name: "Quiet Rule"
      hex: "#9FBAB7"
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
  grid: "Apparatus-first asymmetric layout; 96px portrait text margins, silhouette exclusion zones and 32px base spacing"
  alignment: "shared left anchors, deliberate negative space, ragged right"
  aspect_ratio: "9:16"
  notes:
    - "Labels require a planned empty zone and at least 32px clearance from the apparatus silhouette."
    - "A hero background may blend via alpha masks only in empty edge zones; preserve apparatus and contact shadows."
    - "Leader lines are native, sparse and non-crossing; omit them when no valid conceptual mapping exists."
    - "Each episode chooses a mechanism suited to its topic; the glass-pipe specimen is not a universal template."
motion:
  transitions: ["hard editorial cut", "restrained opacity reveal", "meaningful mask reveal"]
  animation_style: >
    Reveal control, transmission and response in meaningful order. Quantitative diagrams and labels are deterministic; generated stills are not claimed to be validated simulations.
  pacing: "Readable holds; one meaningful motion event per reasoning beat."
  audio_cues: ["Optional explanatory contact sounds only; no automatic BGM or generic whooshes."]
mood:
  keywords: ["analytical", "restrained", "contemporary", "trustworthy"]
  era: "contemporary"
  cultural_reference: "educational exhibits and precision product photography"
  avoid:
    - "opaque text cards over apparatus"
    - "hard seams between near-matching studio backgrounds"
    - "crossing leader lines or labels inside silhouettes"
    - "random lab equipment without explanatory mapping"
    - "metaphors presented as quantitative evidence"
assets:
  reference_images: []
  gsep_elements: []
  html_snippets: []
x_openmontage:
  reference_style: "styles/xiaosan-tactile-research-paper.visual-style.md"
  candidate_preview: "styles/references/xiaosan-economic-mechanism-lab/candidate-preview.png"
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

冷灰实验台、玻璃与哑光金属装置，辅以深青结构色与少量橙色控制点；文字依附解释关系，不用大块背景遮挡装置。

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

