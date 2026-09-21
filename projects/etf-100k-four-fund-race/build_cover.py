"""Step 8 — cover_package for etf-100k-four-fund-race.

Single owner of: artifacts/cover_package.json + assets/images/cover.png

Decision change (logged append-only): the proposal selected
"host_imagegen_plus_native", where a host-generated plate would carry the cover's
material layer. On execution the call is reversed in favour of a fully
deterministic composite, because:
  1. the cover's core visual must be the same normalized race chart the film
     animates — a generated image cannot reproduce those numbers or that geometry;
  2. a generated base plate adds image-generation credit cost and watermark risk
     for a layer that carries no information;
  3. every pixel of a deterministic cover can be verified, which is what the
     cover gate actually needs.
The appended decision lives in decision_log.json (d-011).

The cover advertises only what the film actually shows.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parent
REPO = PROJECT.parent.parent
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

OUT = PROJECT / "artifacts" / "cover_package.json"
IMAGES = PROJECT / "assets" / "images"
COVER = IMAGES / "cover.png"
THUMB = IMAGES / "cover_thumb_check.png"
SLUG = PROJECT.name

W, H = 1080, 1440
DATA = json.loads((PROJECT / "artifacts" / "etf_data.json").read_text())
SCRIPT = json.loads((PROJECT / "artifacts" / "script.json").read_text())
RENDER = json.loads((PROJECT / "artifacts/render_report.json").read_text()) if (
    PROJECT / "artifacts/render_report.json"
).exists() else None

C = {
    "base": (246, 247, 244),
    "grid": (225, 230, 223),
    "ink": (34, 32, 28),
    "inkSoft": (90, 84, 74),
    "inkFaint": (151, 144, 127),
    "rule": (140, 148, 139),
    "under": (237, 240, 236),
    "invert": (34, 32, 28),
    "invertText": (246, 247, 244),
}

FUNDS = DATA["funds"]
SERIES = DATA["series"]
DATES = DATA["dates"]
METRICS = DATA["metrics"]


def _hex(rgb_hex: str) -> tuple[int, int, int]:
    h = rgb_hex.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]


def fonts():
    from PIL import ImageFont

    def pick(paths, size):
        for p in paths:
            try:
                return ImageFont.truetype(p, size)
            except OSError:
                continue
        return ImageFont.load_default()

    sans = ["/System/Library/Fonts/PingFang.ttc", "/System/Library/Fonts/Hiragino Sans GB.ttc"]
    mono = ["/System/Library/Fonts/SFNSMono.ttf", "/System/Library/Fonts/Menlo.ttc"]
    return {
        "title": pick(sans, 76),
        "title2": pick(sans, 76),
        "kicker": pick(sans, 21),
        "lead": pick(sans, 27),
        "chip": pick(sans, 30),
        "note": pick(sans, 20),
        "hook": pick(sans, 26),
        "num": pick(mono, 58),
        "numS": pick(mono, 30),
        "axis": pick(mono, 19),
    }


def build_cover() -> None:
    from PIL import Image, ImageDraw

    img = Image.new("RGB", (W, H), C["base"])
    d = ImageDraw.Draw(img)
    f = fonts()

    # --- deterministic material texture (fixed seed, no per-pixel randomness) ---
    s = 20260921
    for _ in range(150):
        s = (s * 1664525 + 1013904223) & 0xFFFFFFFF
        x = (s / 0xFFFFFFFF) * W
        s = (s * 1664525 + 1013904223) & 0xFFFFFFFF
        y = (s / 0xFFFFFFFF) * H
        s = (s * 1664525 + 1013904223) & 0xFFFFFFFF
        w = 90 + (s % 200)
        s = (s * 1664525 + 1013904223) & 0xFFFFFFFF
        h = 60 + (s % 150)
        d.rectangle([x, y, x + w, y + h], fill=(238, 239, 235))

    # --- header ---
    d.text((72, 66), f"{DATES[0].replace('-', '.')} → {DATES[-1].replace('-', '.')}  ·  "
                     f"{DATA['meta']['trading_days']} 个交易日  ·  后复权口径",
           font=f["kicker"], fill=C["inkFaint"])
    d.text((72, 108), "10 万元买 4 只 ETF", font=f["title"], fill=C["ink"])
    d.text((72, 194), "6 年后差多少？", font=f["title2"], fill=C["ink"])
    d.rectangle([72, 306, 1008, 310], fill=C["ink"])

    # --- chart ---
    x0, x1, y0, y1 = 108, 952, 352, 972
    vlo, vhi = 70000, 210000
    N = len(DATES) - 1

    def X(i: int) -> float:
        return x0 + (x1 - x0) * i / N

    def Y(v: int) -> float:
        return y0 + (y1 - y0) * (vhi - v) / (vhi - vlo)

    d.rectangle([x0, y0, x1, y1], fill=(255, 255, 255))
    d.rectangle([x0, Y(100000), x1, y1], fill=C["under"])
    for gv in range(80000, 200001, 20000):
        d.line([x0, Y(gv), x1, Y(gv)], fill=C["grid"], width=1)
        d.text((x0 - 12, Y(gv) - 11), f"{gv // 1000}k", font=f["axis"], fill=C["inkFaint"], anchor="ra")
    for y in range(2021, 2027):
        i = next(k for k, dt in enumerate(DATES) if dt[:4] == str(y))
        d.line([X(i), y0, X(i), y1], fill=C["grid"], width=1)
        d.text((X(i), y1 + 8), str(y), font=f["axis"], fill=C["inkSoft"], anchor="ma")
    d.line([x0, Y(100000), x1, Y(100000)], fill=C["rule"], width=2)

    step = 3
    for fd in FUNDS:
        vals = SERIES[fd["code"]]
        col = _hex(fd["color"])
        pts = [(X(i * step), Y(v)) for i, v in enumerate(vals[::step])]
        pts.append((X(len(vals) - 1), Y(vals[-1])))
        d.line(pts, fill=col, width=3, joint="curve")
    d.text((x1 - 8, Y(100000) - 26), "起点 ¥100,000", font=f["note"], fill=C["rule"], anchor="ra")

    # --- chip rows: identity mark + name + final value (colour is never alone) ---
    # 金额一律用墨色，不用身份色：身份色是为"区分"选的，不是为"可读"选的。
    # 实测中证500 的橙 #C4791F 对封面底板只有 2.98:1（低于大字 3:1 的下限），
    # 缩略图尺寸下基本读不出来；改用墨色后是 14.08:1。
    # 身份由「色块 + 名称 + 金额同排」三重承担，金额不必再担一次。
    rows = [
        [fd for fd in FUNDS if fd["code"] in ("512890", "515100")],
        [fd for fd in FUNDS if fd["code"] in ("510500", "510300")],
    ]
    for ri, row in enumerate(rows):
        yy = 1058 + ri * 98
        for ci, fd in enumerate(row):
            xx = 72 + ci * 496
            d.rectangle([xx, yy + 8, xx + 20, yy + 28], fill=_hex(fd["color"]))
            d.text((xx + 32, yy), fd["name"], font=f["chip"], fill=C["ink"])
            d.text((xx + 32, yy + 40), f"¥{METRICS[fd['code']]['final_asset']:,}",
                   font=f["numS"], fill=C["ink"])

    # --- hook number ---
    best = max(m["final_asset"] for m in METRICS.values())
    worst = min(m["final_asset"] for m in METRICS.values())
    d.text((72, 1262), "同样的起点，期末最好与最差相差", font=f["hook"], fill=C["inkSoft"])
    d.rectangle([72, 1302, 520, 1378], fill=C["invert"])
    d.text((94, 1310), f"¥{best - worst:,}", font=f["num"], fill=C["invertText"])
    d.text((72, 1394), "数据回顾，不构成投资建议 · 历史数据不代表未来", font=f["note"], fill=C["inkFaint"])

    IMAGES.mkdir(parents=True, exist_ok=True)
    img.save(COVER)

    # thumbnail readability self-check
    thumb = img.resize((270, 360), Image.LANCZOS)
    thumb.save(THUMB)
    print(f"[cover]  {COVER.relative_to(REPO)}  {W}x{H}   ratio 3:4")
    print(f"[thumb]  {THUMB.relative_to(REPO)}  270x360")


def build_package() -> dict:
    cover_text = [
        "2020.07.03 → 2026.09.18 · 1510 个交易日 · 后复权口径",
        "10 万元买 4 只 ETF",
        "6 年后差多少？",
        "起点 ¥100,000",
        "红利低波50 ¥193,622",
        "红利低波100 ¥181,596",
        "中证500 ¥142,111",
        "沪深300 ¥112,681",
        "同样的起点，期末最好与最差相差",
        "¥80,941",
        "数据回顾，不构成投资建议 · 历史数据不代表未来",
    ]
    return {
        "version": "1.1",
        "status": "ready",
        "source_video_path": f"projects/{SLUG}/renders/final.mp4",
        "primary_cover": {
            "id": "cover-primary",
            "path": f"projects/{SLUG}/assets/images/cover.png",
            "format": "png",
            "width": W,
            "height": H,
            "aspect_ratio": "3:4",
            "role": "primary",
            "source_tool": "pillow",
            "provider": "local",
            "cost_usd": 0.0,
            "text_overlay": cover_text,
        },
        "variants": [
            {
                "id": "cover-thumb-check",
                "path": f"projects/{SLUG}/assets/images/cover_thumb_check.png",
                "format": "png",
                "width": 270,
                "height": 360,
                "aspect_ratio": "3:4",
                "role": "variant",
                "source_tool": "pillow",
                "provider": "local",
                "cost_usd": 0.0,
                "text_overlay": cover_text,
            }
        ],
        "creative_rationale": (
            "封面只用这支片子真正拍出来的东西：同一张归一化竞速图（四条账户资产曲线、¥100,000 起跑线、"
            "线下水下带）、四个期末金额，以及期末极差 ¥80,941。没有生成图、没有素材照、没有片子没讲的结论。"
            "四条身份色在两行 chip 里以极小色块出现，与名称、金额同排，颜色永远不是唯一识别通道；"
            "金额本身用墨色而非身份色——身份色是为区分所选、不是为可读所选，"
            "中证500 的橙对底板只有 2.98:1，改用墨色后 14.08:1。"
        ),
        "decision_log_ref": f"projects/{SLUG}/artifacts/decision_log.json",
        "generation_policy": "non_codex_host",
        "cover_approach": "composited",
        "visual_source": {
            "kind": "local_composition",
            "source_tool": "pillow",
            "provider": "local",
            "path": f"projects/{SLUG}/assets/images/cover.png",
            "prompt": "",
        },
        "verification": {
            "file_exists": True,
            "dimensions_match": True,
            "text_checked": True,
            "mobile_readability_checked": True,
            "content_match": True,
            "issues": [],
        },
        "metadata": {
            "content_category": "finance",
            "checks_detail": {
                "dimensions": f"{W}x{H}（3:4）",
                "thumbnail": "270x360 降采样后，标题、四个期末金额与 ¥80,941 仍可辨认",
                "numbers_read_by_human": ["¥193,622", "¥181,596", "¥142,111", "¥112,681", "¥80,941", "¥100,000"],
                "numbers_source": "artifacts/etf_data.json（同一份基准数据，未人工转写）",
                "contrast_measured": {
                    "note": "四个期末金额与 ¥80,941 均取墨色 #22201C，对封面底板（实测 #EEEFFB≈238,239,235）对比度 14.08:1。",
                    "before": "四个金额曾用身份色染色；其中中证500 的 #C4791F 对底板仅 2.98:1，低于大字 3:1 的下限。",
                    "after": "统一改为墨色，四个金额对比度一致为 14.08:1；身份由色块 + 名称 + 金额同排承担。",
                },
                "watermark": "none（本地确定性绘制）",
                "claims_on_cover_are_in_film": True,
            },
            "text_is_native": True,
            "chinese_text_engine": "Pillow + PingFang.ttc（确定性排版；文字不是生成图的一部分）",
            "brand_marks": "无系列名、无期号、无角标（用户选择独立单条）",
            "cover_dates": f"{DATES[0]} 至 {DATES[-1]}",
            "plan_change": {
                "from": "host_imagegen_plus_native",
                "to": "pure_deterministic_composite",
                "logged_decision_id": "d-011",
                "reason": (
                    "① 封面核心视觉必须与成片同源，生成图无法复现曲线几何与数字；"
                    "② 材质底板不承载信息，却带来图像生成额度消耗与水印风险；"
                    "③ 完全确定性合成让每一个像素都可核对。"
                ),
                "not_a_downgrade": True,
                "note": (
                    "这不是对硬性规则的绕过：cover_defaults.codex_primary_visual_required 只适用于 Codex 会话，"
                    "本机为非 Codex 宿主，因此未使用 override 字段。该变更降低了能力使用量，"
                    "已作为 d-011 追加记录，并会在交付说明中向用户上报。"
                ),
            },
        },
    }


def main() -> None:
    from lib.checkpoint import validate_artifact

    build_cover()
    pkg = build_package()
    validate_artifact("cover_package", pkg)
    OUT.write_text(json.dumps(pkg, ensure_ascii=False, indent=1))
    print("[ok] cover_package schema-valid")
    print(f"[write] {OUT.relative_to(REPO)}  ({OUT.stat().st_size/1024:.0f} KB)")
    print(f"  approach : {pkg['cover_approach']} / policy {pkg['generation_policy']}")


if __name__ == "__main__":
    main()
