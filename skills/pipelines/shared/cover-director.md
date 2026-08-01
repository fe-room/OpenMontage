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
- `skills/meta/reviewer.md` and `skills/meta/checkpoint-protocol.md`

If the host is Codex and generated imagery is needed, read the host `imagegen`
skill and use the built-in `image_gen` path by default. This host capability is
outside the Python registry. On other hosts, discover image-generation
providers through the registry and route with `image_selector`. Never silently
switch provider or model.

## Output contract

Produce:

- `projects/<project-id>/assets/images/cover.png` as the primary working asset
- optional versioned variants beside it
- `projects/<project-id>/artifacts/cover_package.json`
- `checkpoint_cover.json`

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

### 3. Choose one cover approach

Choose and communicate one of these before consequential generation:

1. **Frame-led** — use a strong final-video frame, then grade and typeset it.
2. **Generated editorial** — create a new text-free hero visual grounded in the
   video's subject and art direction.
3. **Composited** — combine inspected video frames/assets into a new layout.

Prefer frame-led when the video contains a distinctive face, product, or hero
shot. Prefer generated editorial for abstract explainers whose frames do not
read clearly as a static cover.

### 4. Design for feed readability

- One dominant subject and one visual tension.
- Headline: normally two lines; at most three short lines.
- Keep exact Chinese or other non-Latin text out of generated pixels when a
  deterministic local text compositor is available.
- Use the active art direction's palette, materials, and type personality.
- Maintain platform safe zones and high contrast at phone-thumbnail size.
- No watermarks, accidental logos, invented data, or unrelated clickbait.

### 5. Generate sample, then finish

For generated or composited covers, make one sample first. Inspect it for
subject clarity, style match, unwanted text/logos, and crop viability. Only
then create the final or additional variants. Before every paid generation
call, announce tool, provider, model/variant, reason, and whether it is a sample
or batch.

Save generated backgrounds and final composites inside the project. Preserve
previous approved covers with versioned filenames on re-runs unless the user
explicitly requested replacement.

### 6. Verify the actual file

The stage is not complete until all are true:

- the primary file exists inside the project,
- pixel dimensions and aspect ratio match the resolved spec,
- headline text is exact and contains no missing glyphs,
- the cover is readable at mobile thumbnail size,
- the subject and promise match the final video,
- no watermark, accidental logo, broken crop, or unsupported claim is visible.

Set `status: "needs_revision"` if any check fails. Do not mark the checkpoint
completed until the issues are fixed.

### 7. Persist and gate

Validate `cover_package` against its schema, write the artifact and checkpoint,
then run the normal reviewer. This stage is human-gated by default: write
`awaiting_human`, present the cover and verification summary, and end the turn.
After approval, complete the checkpoint so `publish` can package the real cover.

## Common pitfalls

- Reusing the first video frame without checking whether it works as a cover.
- Generating in-image Chinese text and shipping misspellings.
- Creating an attractive image that promises a different video.
- Treating the cover as a publish-stage note instead of a real file.
- Saving the image outside `projects/<project-id>/`.
- Generating several paid variants before inspecting one sample.
