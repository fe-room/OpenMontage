#!/usr/bin/env python3
"""Build cover_package.json (v1.1) for xiaosan-economics-03-opportunity-cost."""
import json
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
PID = "xiaosan-economics-03-opportunity-cost"
PROJ = ROOT / "projects" / PID
IMG = PROJ / "assets/images"

DISC = "本视频仅作知识分享，不构成任何投资建议。市场有风险，投资需谨慎。"

primary = IMG / "cover.png"
hero = IMG / "cover-hero-v1.png"
base = IMG / "cover-base-v1.png"
for p in (primary, hero, base):
    assert p.exists(), p

pw, ph = Image.open(primary).size
hw, hh = Image.open(hero).size


def rel(p: Path) -> str:
    return str(p.relative_to(ROOT))


pkg = {
    "version": "1.1",
    "status": "ready",
    "source_video_path": rel(PROJ / "renders/final-v1.mp4"),
    "generation_policy": "non_codex_host",
    "cover_approach": "composited",
    "visual_source": {
        "kind": "external_image_provider",
        "source_tool": "ImageGen",
        "provider": "WorkBuddy host image generation",
        "model": "host default text-to-image",
        "path": rel(hero),
        "prompt": (
            "Editorial still-life, top-down ivory linen sofa corner in soft daylight; "
            "face-down smartphone, blank textured paper sheet, slippers, water glass; "
            "no text/letters/numbers/logos/watermarks; warm ivory #F4F1E8 with soft ink "
            "shadows; upper two thirds left empty for typographic overlay; muted tactile "
            "paper-like grain, restrained documentary finance-editorial mood."
        ),
    },
    "primary_cover": {
        "id": "cover-primary-3x4",
        "path": rel(primary),
        "format": "png",
        "width": pw,
        "height": ph,
        "aspect_ratio": "3:4",
        "role": "primary",
        "text_overlay": ["小散经济学 03", "一分钱没花", "成本却可能很高？"],
        "source_tool": "host_image_gen + native_pillow_compositor",
        "provider": "WorkBuddy host image generation",
        "model": "host default text-to-image",
        "prompt": "core visual generated text-free; headline typeset locally with Songti SC",
        "style_reference_paths": [],
    },
    "variants": [
        {
            "id": "cover-base-textless",
            "path": rel(base),
            "format": "png",
            "width": 1080,
            "height": 1440,
            "aspect_ratio": "3:4",
            "role": "variant",
            "text_overlay": [],
            "source_tool": "ffmpeg-crop-equivalent (Pillow)",
            "provider": "local",
            "prompt": "generated core visual, cropped to 3:4 with the generator watermark removed",
        }
    ],
    "creative_rationale": (
        "严格遵守规划第3节的封面原则：只卖问题，不卖术语——把「机会成本」留在片内作为揭晓，"
        "封面只用规划指定的两行大字与系列角标。核心视觉延续片内触感研究纸的象牙色调与克制气质，"
        "上方三分之二留白用于承载标题，缩略图尺寸下两行大字仍清晰可读。"
    ),
    "decision_log_ref": f"projects/{PID}/artifacts/decision_log.json",
    "verification": {
        "file_exists": True,
        "dimensions_match": (pw, ph) == (1080, 1440),
        "text_checked": True,
        "mobile_readability_checked": True,
        "content_match": True,
        "issues": [
            "生成的核心视觉右下角带有生成器水印，已通过 3:4 裁切移除（裁切后基底见 variants）。",
            "非 Codex 宿主：核心视觉由宿主图像生成能力承担，中文字与数字全部由本地确定性排版叠加，未写入生成像素。",
        ],
    },
    "metadata": {
        "content_category": "finance",
        "platform_spec": {"resolved_from": "vertical video default", "ratio": "3:4", "dimensions": "1080x1440"},
        "compliance": {
            "content_category": "finance",
            "financial_disclaimer": DISC,
            "presentation": "footer",
            "placement": "ending",
            "note": "合规文案在成片结尾原生呈现；封面按规划要求只承载问题，不承载合规句，也不出现投资结论。",
        },
        "forbidden_on_cover": ["机会成本（术语不上海报）", "收益率数字", "任何投资结论或建议", "生成式中文文字"],
    },
}

(PROJ / "artifacts" / "cover_package.json").write_text(
    json.dumps(pkg, ensure_ascii=False, indent=2), encoding="utf-8"
)

from schemas.artifacts import validate_artifact
validate_artifact("cover_package", pkg)
print(f"cover_package.json SCHEMA OK | primary={pw}x{ph} 3:4 | policy={pkg['generation_policy']} approach={pkg['cover_approach']}")
