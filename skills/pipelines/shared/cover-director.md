# Cover Director — Shared Post-Render Stage

## When to use

Run this stage immediately after `compose` succeeds and before `publish`. The
video is already rendered; your job is to produce a real, platform-ready cover,
not a thumbnail concept or a text-only suggestion.

## Prerequisites

Read these before doing work:

- `schemas/artifacts/cover_package.schema.json`
- the active pipeline manifest and style playbook/art direction
- `render_report`, `final_review`, and the final video itself
- the final script plus `brief` or `proposal_packet` when available
- `config.yaml` loaded through `OpenMontageConfig`; apply `cover_defaults` as a
  binding persistent user preference
- `skills/meta/reviewer.md` and `skills/meta/checkpoint-protocol.md`

When the host is Codex and `cover_defaults.codex_primary_visual_required` is
true, read the host `imagegen` skill and use the built-in `image_gen` path for
the primary cover's core visual. This is mandatory, not a weak provider
preference, and it applies even though the host capability is outside the
Python registry. Add exact text afterward with a deterministic native
compositor when `cover_defaults.exact_text_compositor` is `native`.

Do not replace the Codex-generated core visual with a final-video frame,
existing asset, pure Remotion/HTML/SVG composition, `image_selector`, or
FFmpeg-only composition unless the user explicitly approves that override for
this project. A good frame, lower cost, provider availability, or convenience
does not count as approval. If the built-in call is blocked or fails, stop and
surface the blocker; do not silently fall back. On non-Codex hosts, discover
image-generation providers through the registry and route with
`image_selector`. Never silently switch provider or model.

## Output contract

Produce:

- `projects/<project-id>/assets/images/cover.png` as the primary working asset
- optional versioned variants beside it
- `projects/<project-id>/artifacts/cover_package.json`
- `checkpoint_cover.json`

New cover runs MUST emit `cover_package` version `1.1` with
`generation_policy`, `cover_approach`, and `visual_source`. Existing version
`1.0` artifacts remain readable only for backward compatibility.

Do not leave a referenced cover only in the host image-generation directory or
in a temporary folder. `publish` is responsible for copying the approved cover
into the export bundle.

## Process

### 1. Ground the cover in the finished video

Inspect the final render, not only the proposal. Extract or inspect representative
frames from the opening, midpoint, climax, and ending. Identify:

- the video's single strongest promise or tension,
- the most recognizable visual subject,
- the actual final visual language,
- any sensitive claims, brand restrictions, or compliance boundaries.

The cover must advertise the video that was actually rendered. If the final
render drifted from the proposal, the render wins.

### 2. Resolve the platform specification

Use an explicit cover specification from `brief.metadata.cover_spec` or
`proposal_packet.production_plan.cover_spec` when present. Otherwise:

- vertical video → `3:4`, `1080x1440`
- landscape video → `16:9`, `1280x720`
- square video → `1:1`, `1080x1080`

Record the resolved ratio and dimensions in `cover_package`. Do not stretch an
existing frame to fit. Crop, recompose, or generate for the target canvas.

### 3. Resolve and announce the visual-source policy

In a Codex session, default to
`generation_policy: "codex_generated_visual_native_text"`. Announce that the
sample core visual will use Codex built-in `image_gen`, and that exact text will
be added locally. This persistent preference does not need reconfirmation.

If the user explicitly chooses another source, record
`generation_policy: "user_approved_alternative"` and include
`override.user_approved: true` plus the user's reason. On non-Codex hosts,
record `generation_policy: "non_codex_host"`.

### 4. Choose one cover approach

Choose and communicate one of these before consequential generation:

1. **Generated editorial** — create a new text-free hero visual grounded in the
   video's subject and art direction.
2. **Composited** — use the Codex-generated core visual in a layout with native
   typography and, when useful, inspected video details or approved assets.
3. **Frame-led override** — use a strong final-video frame, then grade and
   typeset it. In Codex this requires explicit user approval.

In Codex, prefer generated editorial or Codex-led composited. A distinctive
face, product, or hero shot may inform the prompt or serve as an edit reference,
but it does not waive the generated-visual requirement.

### 5. Design for feed readability

- One dominant subject and one visual tension.
- Headline: normally two lines; at most three short lines.
- Keep exact Chinese or other non-Latin text out of generated pixels when a
  deterministic local text compositor is available.
- Use the active art direction's palette, materials, and type personality.
- Maintain platform safe zones and high contrast at phone-thumbnail size.
- No watermarks, accidental logos, invented data, or unrelated clickbait.

### 6. Generate sample, then finish

For generated or composited covers, make one sample first. Inspect it for
subject clarity, style match, unwanted text/logos, and crop viability. Only
then create the final or additional variants. Before every paid generation
call, announce tool, provider, model/variant, reason, and whether it is a sample
or batch.

Save generated backgrounds and final composites inside the project. Preserve
previous approved covers with versioned filenames on re-runs unless the user
explicitly requested replacement.

### 7. Verify the actual file

The stage is not complete until all are true:

- the primary file exists inside the project,
- pixel dimensions and aspect ratio match the resolved spec,
- headline text is exact and contains no missing glyphs,
- the cover is readable at mobile thumbnail size,
- the subject and promise match the final video,
- no watermark, accidental logo, broken crop, or unsupported claim is visible.
- for the Codex default, `visual_source.kind` is
  `codex_builtin_image_gen` and its generated source file exists inside the
  project; a local compositor alone is not valid provenance,
- for an alternative, the artifact contains the explicit user-approved
  override.

Set `status: "needs_revision"` if any check fails. Do not mark the checkpoint
completed until the issues are fixed.

### 8. Persist and gate

Validate `cover_package` against its schema, write the artifact and checkpoint,
then run the normal reviewer. This stage is human-gated by default: write
`awaiting_human`, present the cover and verification summary, and end the turn.
After approval, complete the checkpoint so `publish` can package the real cover.

## Common pitfalls

- Reusing the first video frame without checking whether it works as a cover.
- Treating a strong video frame or a local Remotion composition as permission
  to bypass the Codex-generated primary visual default.
- Writing Codex provenance for a cover whose actual core visual came only from
  a local compositor.
- Generating in-image Chinese text and shipping misspellings.
- Creating an attractive image that promises a different video.
- Treating the cover as a publish-stage note instead of a real file.
- Saving the image outside `projects/<project-id>/`.
- Generating several paid variants before inspecting one sample.
