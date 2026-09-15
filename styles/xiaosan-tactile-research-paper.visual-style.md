---
name: "小散·触感研究纸"
version: "1.0"
tags:
  - editorial research
  - tactile paper
  - finance education
  - restrained motion
author: "OpenMontage + user-approved"
created: "2026-09-15"

style_prompt_short: >
  中性象牙白的真实研究纸，而不是纯黄色背景；用静态细颗粒、稀疏纤维、纸边厚度、石墨文字与克制朱红批注，形成可触摸但不做旧的研究桌质感。

style_prompt_full: >
  Create a restrained tactile editorial research-paper visual system for vertical video.
  Use neutral ivory paper #F4F1E8 rather than a yellow vintage wash, graphite ink #171715,
  deep teal #345C5B for structure, vermillion #B44736 for analytical annotations,
  muted graphite #6C6860 for secondary text, and desaturated paper-strip colors only when
  they encode categories. Build paper material from four subtle deterministic layers:
  low-frequency tonal mottling, fine static grain at 2–3% perceived intensity, sparse hairline
  fibers visible mainly in close views, and restrained edge darkening. Paper pieces have a
  1px compressed edge, shallow realistic shadow, and occasional sub-degree rotation to show
  thickness and stacking. Use pencil underlines, editorial crop marks, slight ink-density
  variation, and minimal registration offset; never use coffee stains, strong sepia, heavy
  distress, crawling frame-by-frame noise, neon finance graphics, or a bordered card around
  every content group. Texture must use a fixed seed and remain temporally static in video.
  Reuse this material language across the series, but design new scene compositions and one
  episode-specific signature device each time.

colors:
  primary:
    - name: "Neutral Ivory Paper"
      hex: "#F4F1E8"
      role: "dominant paper substrate; neutral, never visibly yellow"
    - name: "Graphite Ink"
      hex: "#171715"
      role: "headlines, main claims, rules and structural ink"
  accent:
    - name: "Analyst Teal"
      hex: "#345C5B"
      role: "systems, explanatory connectors and series identity"
    - name: "Vermillion Pencil"
      hex: "#B44736"
      role: "scarce annotations, underlines and thesis emphasis"
  neutral:
    - name: "Muted Graphite"
      hex: "#6C6860"
      role: "secondary text and source metadata"
    - name: "Paper Edge"
      hex: "#BDB5A7"
      role: "compressed edge, hairline border and fiber shadow"
    - name: "Desk Ground"
      hex: "#D9D3C7"
      role: "quiet surrounding surface behind layered paper"

typography:
  display:
    family: "Noto Sans SC, Source Han Sans SC, PingFang SC"
    weight: "700"
    style: "dense editorial headline, tight tracking, left aligned"
  body:
    family: "Noto Sans SC, Source Han Sans SC, PingFang SC"
    weight: "400–600"
    style: "short spoken-language lines, generous leading, ragged right"
  caption:
    family: "IBM Plex Mono, SFMono-Regular, PingFang SC"
    weight: "500"
    style: "small source metadata, restrained tracking"
  rules:
    - "Chinese carries narrative meaning; English is limited to taxonomy and metadata."
    - "Use one primary claim per frame and avoid stranded single Chinese characters."
    - "Do not duplicate narration as both a large headline and accessibility caption in the same window."

layout:
  grid: "Asymmetric 8-column editorial grid with 96px portrait safe margins"
  alignment: "Hard left alignment, variable paper layers, generous negative space"
  aspect_ratio: "9:16"
  notes:
    - "Do not wrap every information group in a bordered card."
    - "Use paper thickness and overlap only where hierarchy or allocation needs explanation."
    - "Each episode receives a new signature device; material language stays consistent."

motion:
  transitions:
    - "hard editorial cut"
    - "paper mask reveal"
    - "restrained opacity fade"
    - "short physical paper slide"
  animation_style: >
    Motion reveals reasoning: paper strips compress, make room, slide under one another, or expose
    annotations. Shadows respond subtly to displacement. No constant floating, bouncing cards, or
    decorative camera drift. Texture is fixed-seed and static across frames.
  pacing: "Calm and deliberate; preserve readable holds, with one tactile motion event per reasoning beat."
  audio_cues:
    - "Optional quiet pencil or paper contact only when it clarifies an action."
    - "No generic whooshes or impact hits."

mood:
  keywords:
    - "tactile"
    - "analytical"
    - "restrained"
    - "trustworthy"
    - "hand-reviewed"
  era: "contemporary editorial with analog material cues"
  cultural_reference: "research notebook, annotated proof sheet, analyst desk"
  avoid:
    - "flat yellow backgrounds"
    - "strong sepia or coffee-stain aging"
    - "heavy global noise"
    - "frame-randomized crawling grain"
    - "generic finance dashboards and candlestick wallpaper"
    - "identical paper-card layouts in every scene"

assets:
  reference_images: []
  gsep_elements: []
  html_snippets: []

x_openmontage:
  approved_preview: "styles/references/xiaosan-tactile-research-paper/approved-preview.png"
  approved_on: "2026-09-15"
  reuse_scope: "material tokens and texture recipe only; never reuse completed scene compositions"
  texture_recipe:
    base: "#F4F1E8"
    broad_mottle_opacity: 0.08
    static_grain_opacity: 0.025
    fiber_opacity: 0.10
    edge_darkening_opacity: 0.04
    grain_seed: 27
    max_paper_rotation_degrees: 1.3
---

## Design Principles

The paper should be felt before it is noticed. Material cues stay below the level of a filter and
become visible through stacking, close crops, and controlled light. The system is contemporary,
not nostalgic: no yellow wash, dirt, or theatrical aging.

Series consistency comes from substrate, ink, annotation behavior, and typography. Episode
distinctness comes from the information structure and one new signature device. Never turn this
style into a fixed scene template.

## OpenMontage / Remotion Mapping

- Render the base, mottle, grain, and fibers as separate deterministic layers.
- Use a fixed seed; never call `Math.random()` per frame.
- Keep texture static while paper geometry moves.
- Apply edge/shadow layers to paper objects, not to the whole canvas.
- For portrait delivery, maintain the shared social UI safe area for captions.
