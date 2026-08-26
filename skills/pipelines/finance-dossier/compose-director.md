# Finance Dossier — Compose Director

Produce `render_report` and `final_review` by routing strictly from the approved `render_runtime`. Read `skills/core/remotion.md` plus the `video_compose` Layer 3 skills before invoking tools. If `render_runtime: hyperframes`, follow the HyperFrames path; if it is unavailable, stop and surface the blocker rather than silently selecting Remotion.

## Templated path

Use the existing `Explainer` composition and finance cut dispatch. Run `composition_validator` before render, then TypeScript/bundle validation as appropriate. Do not create another engine or composition router.

## Atelier path

Follow `skills/meta/bespoke-composition.md`. Retain the finance-dossier palette, typography, evidence/source treatment, and analytical restraint, but do not import or reconstruct reusable finance scene components. Produce per-scene stills for the assets gate before the full render.

## Post-render gate

1. Run ffprobe: verify video/audio streams, resolution, fps, size, and duration.
2. Extract representative frames for every scene family and inspect layout, clipping, mobile readability, one-claim-per-frame, direction labels, and source strips.
3. Transcribe narration and compare coverage to the approved script.
4. Inspect the ending frame and record that `本视频仅作知识分享，不构成任何投资建议。市场有风险，投资需谨慎。` is exact, readable, native text, and at the end.
5. Verify no runtime/provider substitution occurred and no music layer exists when source is none.

Any unreadable source, fabricated value, deterministic scenario language, or missing disclaimer is critical and requires re-render.
