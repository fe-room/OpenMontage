# Subtitle Sync Skill

## When to Use

Use the `subtitle_gen` tool to convert transcript data (from `transcriber`)
into properly timed subtitle files. This skill covers timing strategy,
formatting, and readability for both vertical and horizontal video.

## Tool

| Tool | Capability |
|------|-----------|
| `subtitle_gen` | Generate SRT, VTT, or caption JSON from word-level timestamps |

## Output Formats

| Format | Extension | Use Case |
|--------|-----------|----------|
| SRT | `.srt` | Universal — works with FFmpeg, players, YouTube upload |
| VTT | `.vtt` | Web-native — HTML5 video, browser playback |
| Caption JSON | `.caption.json` | Programmatic — word-level data for custom renderers |

## Cue Length by Format

### Vertical Short-form (TikTok, Reels, Shorts)

- **Max 3-4 words per cue** — screen is narrow, text must be large enough to read
- **Max 20 characters per line** — prevents wrapping on narrow screens
- Subtitles are **mandatory** (most viewers watch muted)

### Horizontal Standard (YouTube, web)

- **Max 6-8 words per cue** — wider screen accommodates more text
- **Max 42 characters per line** — standard broadcast limit

### General Rules

- Average viewer reads ~15 characters/second
- Minimum display time: 0.5 seconds per cue
- Maximum display time: 5 seconds per cue

## Styling for Burn-in (ASS force_style)

When burning subtitles via `video_compose`, these parameters are passed as ASS
`force_style`. Use the correct ASS color format: `&HAABBGGRR` (not hex RGB).

### Vertical Video (1080x1920)

```
font: Arial
font_size: 18
bold: true
primary_color: &H00FFFFFF      # white (ASS format: alpha=00, BGR=FFFFFF)
outline_color: &H00000000      # black
outline_width: 3               # thick outline for readability on varied backgrounds
shadow: 2
margin_v: 520                  # shared social UI safe area; renderer enforces this minimum
margin_l: 96                   # keep clear of edge controls/crops
margin_r: 96
alignment: 2                   # bottom center
```

### Horizontal Video (1920x1080)

```
font: Arial
font_size: 22
bold: true
primary_color: &H00FFFFFF
outline_color: &H00000000
outline_width: 2
shadow: 1
margin_v: 40
alignment: 2
```

### Common Mistakes

- **Wrong color format:** `&HFFFFFF` breaks positioning. Always use full 8-char `&H00FFFFFF`.
- **Font too large on vertical:** `font_size: 28` fills the center of a 9:16 frame. Use 18 max.
- **Too many words per cue on vertical:** 5+ words creates multi-line blocks that cover the face.
- **Using the old 40-100px bottom margin on portrait video:** this puts captions behind the platform title, account/avatar, and interaction chrome. The shared 1080x1920 minimum is 520px.
- **Per-platform guesswork:** use the single conservative `social-ui-safe` lane for a master that may be posted to TikTok, Reels, or Shorts. Do not lower it for one platform unless the user explicitly requests a platform-only variant.

## Portrait Social Safe Area (Mandatory)

For every output where `height > width`, caption placement uses the shared
`social-ui-safe` policy. At 1080x1920 this means:

- bottom clearance: at least `520px`;
- left/right clearance: at least `96px`;
- caption copy stays centered in the resulting lane;
- a larger project-specific clearance is allowed, but a smaller value is
  clamped by Remotion and FFmpeg.

Record the decision in `edit_decisions.subtitles.safe_area`:

```json
{
  "policy": "social-ui-safe",
  "bottom_offset_px": 520,
  "side_margin_px": 96
}
```

Remotion's shared `CaptionOverlay`, `video_compose`'s FFmpeg subtitle burn, and
`remotion_caption_burn` all apply the same rule automatically. HyperFrames or
atelier compositions must implement these clearances explicitly and declare
them in `edit_decisions`; post-render review fails the safe-area check otherwise.

## Timing Best Practices

### Alignment with Speech

- Cue start must match word onset (not before the speaker starts)
- Cue end should extend ~200ms past the last word for comfortable reading
- Never let a cue linger into the next speaker's turn

### Word Boundary Grouping

The `subtitle_gen` tool groups words respecting `max_words_per_cue` and
`max_chars_per_line`. When word timestamps are unavailable, it falls back
to segment-level timing with even distribution.

## Quality Checklist

- [ ] Every spoken word appears in a subtitle cue
- [ ] No cue exceeds the character limit for the target format
- [ ] Portrait subtitles sit above the bottom social UI exclusion zone (520px at 1080x1920), not at the physical bottom edge
- [ ] Portrait subtitles keep at least 96px side clearance at 1080x1920
- [ ] Text is readable on mobile at native resolution
- [ ] Timing matches speech — no early or late cues
- [ ] Cues don't overlap each other
- [ ] Outline/shadow provides sufficient contrast against all backgrounds
