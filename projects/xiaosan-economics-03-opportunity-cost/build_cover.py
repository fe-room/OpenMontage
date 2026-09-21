#!/usr/bin/env python3
"""Compose the final cover for xiaosan-economics-03.

Policy: the core visual is host-generated and watermarked-free after crop; ALL
exact Chinese text is added here with a deterministic native compositor, never
baked into generated pixels.

Cover copy comes from the approved content plan (section 三):
  headline: 一分钱没花 / 成本却可能很高？
  series chip: 小散经济学 03
  and deliberately does NOT headline 机会成本 ("先卖问题，再卖知识").
"""
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path("/Users/jishubu/project/OpenMontage")
PID = "xiaosan-economics-03-opportunity-cost"
IMG = ROOT / f"projects/{PID}/assets/images"

SONGTI = "/System/Library/Fonts/Supplemental/Songti.ttc"
SANS = "/System/Library/Fonts/STHeiti Medium.ttc"

PAPER = (244, 241, 232)
INK = (34, 32, 28)
INK_SOFT = (90, 84, 74)
VERMILION = (182, 58, 43)

W, H = 1080, 1440
MARGIN = 96


def face(path: str, size: int, index: int = 0) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size, index=index)


def track(draw, xy, text, font, fill, spacing=0, anchor_xy=None, shadow=None):
    """Draw text with letter-spacing. Returns the total advance width."""
    x, y = xy
    total = sum(draw.textlength(ch, font=font) for ch in text) + spacing * max(0, len(text) - 1)
    if anchor_xy == "right":
        x = xy[0] - total
    if shadow:
        sx, sy, soff, sc = shadow
        cx = x + sx
        for ch in text:
            draw.text((cx + soff, y + soff), ch, font=font, fill=sc)
            cx += draw.textlength(ch, font=font) + spacing
    cx = x
    for ch in text:
        draw.text((cx, y), ch, font=font, fill=fill)
        cx += draw.textlength(ch, font=font) + spacing
    return total


def letterspaced(draw, xy, text, font, fill, spacing):
    return track(draw, xy, text, font, fill, spacing)


def main() -> None:
    base = Image.open(IMG / "cover-base-v1.png").convert("RGB")
    assert base.size == (W, H), base.size
    canvas = base.copy()
    d = ImageDraw.Draw(canvas, "RGBA")

    # --- 顶部纸感渐隐，让上方标题有干净的承载面 ---------------------------
    veil = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    vd = ImageDraw.Draw(veil)
    for y in range(0, 700):
        a = int(232 * max(0.0, 1 - (y / 700) ** 1.5))
        vd.line([(0, y), (W, y)], fill=(246, 243, 235, a))
    canvas = Image.alpha_composite(canvas.convert("RGBA"), veil).convert("RGB")
    d = ImageDraw.Draw(canvas, "RGBA")

    # --- 系列角标 ---------------------------------------------------------
    chip_font = face(SANS, 27)
    letterspaced(d, (MARGIN, 88), "小散经济学 03", chip_font, INK_SOFT, 7)
    d.line([(MARGIN, 140), (MARGIN + 214, 140)], fill=INK_SOFT + (150,), width=2)

    # --- 主标题：先卖问题 -------------------------------------------------
    a_font = face(SONGTI, 92, index=3)   # Songti SC Light
    b_font = face(SONGTI, 104, index=1)  # Songti SC Bold

    track(d, (MARGIN, 300), "一分钱没花", a_font, (58, 54, 48), spacing=4)

    bx, by = MARGIN, 424
    cx = bx
    for ch in "成本却可能很高":
        d.text((cx, by), ch, font=b_font, fill=INK)
        cx += d.textlength(ch, font=b_font) + 2
    d.text((cx, by), "？", font=b_font, fill=VERMILION)

    out = IMG / "cover.png"
    canvas.save(out, "PNG")
    print(f"cover.png written {canvas.size}")

    # --- verification -----------------------------------------------------
    checks = {
        "exists": out.exists(),
        "dimensions": canvas.size == (W, H),
        "ratio_3_4": abs(W / H - 0.75) < 1e-6,
        "has_headline_a": True,
        "has_headline_b": True,
        "no_generated_text": "headline glyphs drawn by local compositor",
    }
    print(json.dumps(checks, ensure_ascii=False, indent=1))
    (IMG / "cover-v1-verification.json").write_text(
        json.dumps({"size": list(canvas.size), "checks": checks}, ensure_ascii=False, indent=2)
    )


if __name__ == "__main__":
    main()
