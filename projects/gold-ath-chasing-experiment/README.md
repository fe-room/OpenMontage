# gold-ath-chasing-experiment — atelier (bespoke) composition

Hand-authored Remotion composition. Source of truth lives here under
`projects/gold-ath-chasing-experiment/`; at render time the atelier path auto-stages a junction at
`remotion-composer/projects/gold-ath-chasing-experiment/` so the bundler can resolve `node_modules`.

## Doctrine
- Read `skills/meta/bespoke-composition.md` first.
- Fill in `art-direction.md` BEFORE authoring scenes.
- No imports from `remotion-composer/src/*` (the tool will fail the render).
- Reuse engine knowledge only; hand-stitch every creative component.

## Render

```python
from tools.video.video_compose import VideoCompose
P = r"projects\\gold-ath-chasing-experiment"  # absolute path on your machine
VideoCompose().execute({
  "operation": "render",
  "output_path": P + r"\renders\final.mp4",
  "edit_decisions": {
    "render_runtime": "remotion",
    "composition_mode": "atelier",
    "bespoke": {
      "entry": P + r"\index.tsx",
      "composition_id": "GoldAthChasingExperiment",
      "props_path": P + r"\artifacts\props.json",
      "public_dir": P + r"\public",
      "art_direction": "<short note OR path to art-direction.md>",
      "scale": 1.0, "crf": 18, "concurrency": 8
    }
  }
})
```
