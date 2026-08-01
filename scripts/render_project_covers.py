#!/usr/bin/env python3
"""Render the unified OpenMontage finance cover series."""

from pathlib import Path
from shutil import copy2

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
FONT_PATH = "/System/Library/Fonts/STHeiti Medium.ttc"
SIZE = (1080, 1440)

CREAM = "#F1E7D3"
GOLD = "#D6A541"
RED = "#E4473F"
MINT = "#49CDB0"
INK = "#07131F"


COVERS = [
    {
        "source": "covers/cola-bubbles-tech-selloff-background.png",
        "output": "covers/cola-bubbles-tech-selloff-cover-3x4.png",
        "eyebrow": "财经拆解  ·  06",
        "issue": "06",
        "title": [
            ("最有“泡沫”", CREAM, 108),
            ("反而涨了", RED, 116),
        ],
        "subtitle": "科技股暴跌，可口可乐为何逆势？",
        "footer": "DEFENSIVE  /  ROTATION",
        "accent": GOLD,
    },
    {
        "source": "covers/optical-module-valuation-background.png",
        "output": "covers/optical-module-valuation-cover-3x4.png",
        "eyebrow": "财经拆解  ·  05",
        "issue": "05",
        "title": [
            ("光模块会赢", CREAM, 108),
            ("你买贵了吗？", RED, 112),
        ],
        "subtitle": "科技暴跌 · 上市破发 · 好赛道≠好价格",
        "footer": "TECH  /  VALUATION",
        "accent": MINT,
    },
    {
        "source": "covers/dividend-series-episode-1-background.png",
        "output": "covers/dividend-series-episode-1-cover-3x4.png",
        "eyebrow": "分红系列  ·  01",
        "issue": "01",
        "title": [
            ("分红到账", CREAM, 108),
            ("5000元", GOLD, 124),
            ("养老真容易？", RED, 104),
        ],
        "title_positions": (122, 222, 326),
        "separator_y": 438,
        "subtitle_y": 458,
        "footer_y": 508,
        "subtitle": "到账不等于凭空多赚五千元",
        "footer": "DIVIDEND  /  EX-DATE",
        "accent": GOLD,
    },
    {
        "project": "a-share-ancestral-rules",
        "issue": "01",
        "title": [("A股祖训", CREAM, 132), ("冲高就跑？", RED, 132)],
        "subtitle": "大涨之后，真正该防的是情绪",
        "footer": "MARKET  /  BEHAVIOR",
        "accent": GOLD,
    },
    {
        "project": "dividend-series-episode-2",
        "issue": "02",
        "title": [("分红不是", CREAM, 132), ("白送钱", GOLD, 150)],
        "subtitle": "为什么长期投资者仍然看重它？",
        "footer": "DIVIDEND  /  VALUE",
        "accent": GOLD,
    },
    {
        "project": "microsoft-meta-ai-earnings-20260730",
        "issue": "03",
        "title": [("AI 的钱", CREAM, 140), ("谁烧得值？", RED, 132)],
        "subtitle": "微软 VS META · 华尔街开始给 AI 算账",
        "footer": "CAPEX  /  RETURNS",
        "accent": MINT,
    },
    {
        "project": "shenme-shi-laodenggu",
        "issue": "04",
        "title": [("什么是", CREAM, 132), ("老登股？", RED, 150)],
        "subtitle": "科技回调时，它为什么又香了？",
        "footer": "STYLE  /  ROTATION",
        "accent": GOLD,
    },
]


def font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_PATH, size=size)


def fit_font(draw: ImageDraw.ImageDraw, text: str, max_size: int, max_width: int) -> ImageFont.FreeTypeFont:
    size = max_size
    while size > 24:
        candidate = font(size)
        if draw.textbbox((0, 0), text, font=candidate)[2] <= max_width:
            return candidate
        size -= 2
    return font(size)


def add_top_shade(image: Image.Image) -> Image.Image:
    shade = Image.new("RGBA", SIZE, (7, 19, 31, 0))
    pixels = shade.load()
    for y in range(560):
        alpha = max(0, round(115 * (1 - y / 560)))
        for x in range(SIZE[0]):
            pixels[x, y] = (7, 19, 31, alpha)
    return Image.alpha_composite(image.convert("RGBA"), shade)


def render_cover(spec: dict) -> Path:
    if "project" in spec:
        project_dir = ROOT / "projects" / spec["project"]
        source = project_dir / "assets" / "images" / "video-cover-background-v1.png"
        output = project_dir / "assets" / "images" / "video-cover-3x4-v2.png"
        export = project_dir / "exports" / "thumbnails" / "video-cover-3x4-v2.png"
    else:
        source = ROOT / spec["source"]
        output = ROOT / spec["output"]
        export = None

    source_image = Image.open(source).convert("RGB")
    image = ImageOps.fit(
        source_image,
        SIZE,
        method=Image.Resampling.LANCZOS,
        centering=(0.5, 0.28),
    )
    image = add_top_shade(image)
    draw = ImageDraw.Draw(image)

    x = 76
    accent = spec["accent"]
    draw.rectangle((x, 54, x + 10, 100), fill=accent)
    eyebrow = spec.get("eyebrow", f"财经拆解  ·  {spec['issue']}")
    draw.text((105, 54), eyebrow, font=font(36), fill=accent)

    y_positions = spec.get("title_positions", (135, 255))
    for (text, color, max_size), y in zip(spec["title"], y_positions):
        title_font = fit_font(draw, text, min(max_size, 116), 920)
        draw.text(
            (x, y),
            text,
            font=title_font,
            fill=color,
            stroke_width=2,
            stroke_fill=INK,
        )

    separator_y = spec.get("separator_y", 405)
    subtitle_y = spec.get("subtitle_y", 426)
    footer_y = spec.get("footer_y", 478)
    draw.rectangle((x, separator_y, 736, separator_y + 2), fill=accent)
    subtitle_font = fit_font(draw, spec["subtitle"], 38, 920)
    draw.text((x, subtitle_y), spec["subtitle"], font=subtitle_font, fill="#E9DECA")
    draw.text((x, footer_y), spec["footer"], font=font(22), fill=accent)

    output.parent.mkdir(parents=True, exist_ok=True)
    image.convert("RGB").save(output, format="PNG", optimize=True)
    if export is not None:
        export.parent.mkdir(parents=True, exist_ok=True)
        copy2(output, export)
    return output


def main() -> None:
    for cover in COVERS:
        print(render_cover(cover))


if __name__ == "__main__":
    main()
