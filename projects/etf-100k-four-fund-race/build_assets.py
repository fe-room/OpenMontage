"""Step 5 — asset_manifest for etf-100k-four-fund-race.

Single owner of: artifacts/asset_manifest.json + assets/qa/data_proof.png

This is a composition-only, silent film. Per the recorded motion commitment
(decision d-007) and the user's explicit no-narration choice (d-008), this stage
intentionally generates NO narration, NO music, NO stock footage and NO
generated imagery. The assets this film actually consumes are data:
  1. the canonical 1510-day × 4-series account-value dataset,
  2. the on-screen copy/number deck every scene renders from.

The stage's filmstrip substitute is assets/qa/data_proof.png — a rendered proof
sheet of all four series plus the full metric set, so the numbers can be eyeballed
against the source workbook before anything is authored.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parent
REPO = PROJECT.parent.parent
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

OUT = PROJECT / "artifacts" / "asset_manifest.json"
QA_DIR = PROJECT / "assets" / "qa"
PROOF = QA_DIR / "data_proof.png"
SLUG = PROJECT.name

DATA = json.loads((PROJECT / "artifacts" / "etf_data.json").read_text())
DECK = json.loads((PROJECT / "artifacts" / "onscreen.json").read_text())
SCENE_PLAN = json.loads((PROJECT / "artifacts" / "scene_plan.json").read_text())

DATASET_REL = f"projects/{SLUG}/public/{SLUG}/data/etf-series.json"
DECK_REL = f"projects/{SLUG}/artifacts/onscreen.json"


def render_proof() -> None:
    from PIL import Image, ImageDraw, ImageFont

    W, H = 1700, 1330
    img = Image.new("RGB", (W, H), "#F6F7F4")
    d = ImageDraw.Draw(img)

    def font(size: int, mono: bool = False):
        for cand in (
            ["/System/Library/Fonts/SFNSMono.ttf", "/System/Library/Fonts/Menlo.ttc"]
            if mono
            else ["/System/Library/Fonts/Supplemental/Songti.ttc", "/System/Library/Fonts/PingFang.ttc"]
        ):
            try:
                return ImageFont.truetype(cand, size)
            except OSError:
                continue
        return ImageFont.load_default()

    f_title, f_lab, f_num, f_small = font(32), font(20), font(19, mono=True), font(16)

    d.text((60, 40), "数据核对表 · 四只ETF · 10万元起始", font=f_title, fill="#22201C")
    d.text(
        (60, 86),
        f"{DATA['meta']['start_date']} → {DATA['meta']['end_date']}　"
        f"{DATA['meta']['trading_days']} 个交易日　"
        f"口径：{DATA['meta']['dividend_treatment']}　标的一：后复权总回报",
        font=f_small, fill="#5A544A",
    )

    dates, series, funds = DATA["dates"], DATA["series"], DATA["funds"]
    x0, x1, y0, y1 = 110, 1400, 690, 175
    vlo, vhi = 70000, 210000

    def X(i: int) -> float:
        return x0 + (x1 - x0) * i / (len(dates) - 1)

    def Y(v: int) -> float:
        return y1 + (y0 - y1) * (vhi - v) / (vhi - vlo)

    d.rectangle([x0, y1, x1, y0], fill="#FFFFFF")
    d.rectangle([x0, Y(100000), x1, y0], fill="#EDF0EC")
    for gv in range(80000, 200001, 20000):
        d.line([x0, Y(gv), x1, Y(gv)], fill="#E1E6DF", width=1)
        d.text((x0 - 12, Y(gv) - 10), f"{gv // 1000}k", font=f_num, fill="#97907F", anchor="ra")
    for y in range(2021, 2027):
        i = next(k for k, dt in enumerate(dates) if dt[:4] == str(y))
        d.line([X(i), y1, X(i), y0], fill="#E1E6DF", width=1)
        d.text((X(i), y0 + 8), str(y), font=f_num, fill="#5A544A", anchor="ma")
    d.line([x0, Y(100000), x1, Y(100000)], fill="#8C948B", width=2)

    step = 3
    for f in funds:
        vals = series[f["code"]]
        pts = [(X(i * step), Y(v)) for i, v in enumerate(vals[::step])]
        pts.append((X(len(vals) - 1), Y(vals[-1])))
        d.line(pts, fill=f["color"], width=3, joint="curve")
    # end labels, de-collided
    ends = sorted(
        ((Y(series[f["code"]][-1]), f) for f in funds), key=lambda p: p[0]
    )
    last_y = -1e9
    for yv, f in ends:
        yl = max(yv, last_y + 46)
        last_y = yl
        d.line([x1 + 4, yv, x1 + 16, yl - 12], fill=f["color"], width=2)
        d.text((x1 + 22, yl - 26), f["name"], font=f_lab, fill=f["color"])
        d.text((x1 + 22, yl - 2), f"{series[f['code']][-1]:,}", font=f_num, fill=f["color"])
    d.text((x0, y0 + 46), "账户资产（元）　起点 ￥100,000　线下浅色为「水下」", font=f_small, fill="#5A544A")

    # ---- metrics table ----
    tx, ty = 60, 856
    cols = [("名称 / 代码", 230), ("最终资产", 170), ("累计收益", 150), ("年化收益", 150),
            ("最大回撤", 160), ("回撤跨度", 180), ("最长未创新高", 220)]
    d.rectangle([tx, ty - 48, tx + sum(w for _, w in cols), ty], fill="#22201C")
    cx = tx
    for name, w in cols:
        d.text((cx + 12, ty - 34), name, font=f_small, fill="#F6F7F4")
        cx += w
    for r, f in enumerate(sorted(funds, key=lambda x: -DATA["metrics"][x["code"]]["final_asset"])):
        m = DATA["metrics"][f["code"]]
        yy = ty + r * 74
        d.rectangle([tx, yy, tx + sum(w for _, w in cols), yy + 68],
                    fill="#FFFFFF" if r % 2 == 0 else "#EFEFEA")
        d.rectangle([tx, yy + 8, tx + 5, yy + 60], fill=f["color"])
        cx = tx
        vals = [
            f"{f['name']}　{f['code']}",
            f"{m['final_asset']:,}",
            f"{m['cumulative_return'] * 100:+.2f}%",
            f"{m['annualized_return'] * 100:+.2f}%",
            f"{m['max_drawdown'] * 100:.2f}%",
            f"{m['mdd_days']} 天",
            f"{m['longest_underwater_days']} 日",
        ]
        for i, (v, (_, w)) in enumerate(zip(vals, cols)):
            d.text((cx + 12, yy + 22), v, font=(f_lab if i == 0 else f_num),
                   fill="#22201C" if i == 0 else "#3A3833")
            cx += w

    best = max(m["final_asset"] for m in DATA["metrics"].values())
    worst = min(m["final_asset"] for m in DATA["metrics"].values())
    d.text((tx, ty + 4 * 74 + 22), f"期末最好 - 最差 = ￥{best - worst:,}",
           font=f_lab, fill="#8E3B6B")

    d.text((60, H - 96), "本表由 build_assets.py 从 artifacts/etf_data.json 直接生成，未经人工转写；"
                          "数值与用户工作簿「汇总」表逐项一致（容差 1e-5）。", font=f_small, fill="#5A544A")
    d.text((60, H - 66), "「回撤跨度」= 最大回撤的峰值日到低点日之间的自然日数。", font=f_small, fill="#5A544A")
    d.text((60, H - 36), "本片全程无口播、无音轨、无素材镜头、无生成图像；素材阶段只产出数据资产。",
           font=f_small, fill="#5A544A")
    QA_DIR.mkdir(parents=True, exist_ok=True)
    img.save(PROOF)
    print(f"[render] {PROOF.relative_to(REPO)}  {img.size[0]}x{img.size[1]}")


def build() -> dict:
    race_scene = next(s for s in SCENE_PLAN["scenes"] if s["id"] == "sc04")
    assets = [
        {
            "id": "etf-series",
            "type": "diagram",
            "path": DATASET_REL,
            "source_tool": "build_data.py",
            "scene_id": "sc04",
            "subtype": "canonical_account_value_series",
            "format": "json",
            "provider": "local",
            "license": "derived_from_user_supplied_workbook",
            "cost_usd": 0.0,
            "generation_summary": (
                "四只ETF 1510 个交易日的账户资产序列（归一化到 ￥100,000 起点），"
                "附最大回撤、回撤跨度、最长未创新高区间、年末截面与七个注解节点。"
                "由用户工作簿导出并与工作簿「汇总」表逐项对账后才允许下游运行。"
            ),
        },
        {
            "id": "onscreen-deck",
            "type": "diagram",
            "path": DECK_REL,
            "source_tool": "build_script.py",
            "scene_id": "sc01",
            "subtype": "on_screen_copy_and_number_deck",
            "format": "json",
            "provider": "local",
            "license": "project_internal",
            "cost_usd": 0.0,
            "generation_summary": (
                "本片十场画面的文案与数值台本。所有数值由 build_script.py 的数据辅助函数生成，"
                "verify() 会在写入前把 51 处屏幕数字逐一回查序列；手写文案里不含任何需被读准的数字。"
            ),
        },
    ]
    return {
        "version": "1.0",
        "assets": assets,
        "total_cost_usd": 0.0,
        "metadata": {
            "content_category": "finance",
            "composition_only": True,
            "narration_omitted": True,
            "narration_omitted_reason": "用户显式选择全程无口播（decision d-008）。本阶段不调用 tts_selector。",
            "music_omitted": True,
            "music_omitted_reason": "持久无BGM默认 + 用户选择完全静音（decision d-009）。本文件不含 music 资产。",
            "footage_omitted": True,
            "footage_omitted_reason": "语义动效审计结论：15/15 个 beat 为 precision-critical，0 个语义动态候选（decision d-007）。不调用 video_selector / image_selector。",
            "audio_assets": 0,
            "required_tools_note": (
                "finance-dossier 清单把 tts_selector 列为 assets 阶段的 required_tool。"
                "本片因用户显式选择无口播而不使用它——这是已批准的 deviation，"
                "依据是 decision d-008 与用户开工前的四项设定，不是遗漏。"
            ),
            "requirement_type_map": {
                "data": "diagram",
                "copy_deck": "diagram",
                "note": (
                    "scene_plan.required_assets[].type 用 data / copy_deck 描述需求；"
                    "asset_manifest 的 type 枚举没有对应取值，故两者都落在 diagram（图表数据类）。"
                ),
            },
            "scene_coverage": {
                "scenes_requiring_etf-dataset": [s["id"] for s in SCENE_PLAN["scenes"] if any(a["type"] == "data" for a in s["required_assets"])],
                "scenes_requiring_onscreen-deck": [s["id"] for s in SCENE_PLAN["scenes"] if any(a["type"] == "copy_deck" for a in s["required_assets"])],
            },
            "filmstrip_substitute": {
                "path": f"projects/{SLUG}/assets/qa/data_proof.png",
                "why": "本片没有图像素材可做剧照条。资产复核对象是数字本身，因此用数据核对表代替剧照条：四条曲线 + 全量指标 + 对账说明，供逐项核对后再进入编写。",
            },
            "review_evidence": {
                "workbook_reconciliation": DATA["meta"]["source_note"],
                "account_formula": DATA["meta"]["account_formula"],
                "dividend_treatment": DATA["meta"]["dividend_treatment"],
                "missing_record": "512890 在 2021-10-22 缺 1 条成交记录，按用户工作簿口径沿用前一交易日账户资产。",
                "caveat": DATA["meta"]["caveat"],
            },
            "race_scene_note": race_scene["overlay_notes"],
        },
    }


def main() -> None:
    from lib.checkpoint import validate_artifact

    render_proof()
    manifest = build()
    validate_artifact("asset_manifest", manifest)

    OUT.write_text(json.dumps(manifest, ensure_ascii=False, indent=1))
    print("[ok] asset_manifest schema-valid")
    print(f"[write] {OUT.relative_to(REPO)}  ({OUT.stat().st_size/1024:.0f} KB)")
    print(f"  assets        : {len(manifest['assets'])}")
    for a in manifest["assets"]:
        print(f"    - {a['id']:<16s} {a['type']:<9s} {a['path']}")
    print(f"  audio assets  : {manifest['metadata']['audio_assets']}")
    print(f"  total cost    : ${manifest['total_cost_usd']:.2f}")


if __name__ == "__main__":
    main()
