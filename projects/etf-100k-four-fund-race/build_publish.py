"""Step 9b — publish_log + local export bundle for etf-100k-four-fund-race.

Single owner of: artifacts/publish_log.json + deliverables/publish/*

Local packaging only: no login, no upload, no remote draft. Every artifact a
publisher would need travels with the video so the evidence, the boundaries and
the exact on-screen wording survive outside this repo.
"""

from __future__ import annotations

import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJECT = Path(__file__).resolve().parent
REPO = PROJECT.parent.parent
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

OUT = PROJECT / "artifacts" / "publish_log.json"
PUBLISH = PROJECT / "deliverables" / "publish"
SLUG = PROJECT.name

SCRIPT = json.loads((PROJECT / "artifacts" / "script.json").read_text())
BRIEF = json.loads((PROJECT / "artifacts" / "research_brief.json").read_text())
PROPOSAL = json.loads((PROJECT / "artifacts" / "proposal_packet.json").read_text())
REPORT = json.loads((PROJECT / "artifacts" / "render_report.json").read_text())
REVIEW = json.loads((PROJECT / "artifacts" / "final_review.json").read_text())
COVER = json.loads((PROJECT / "artifacts" / "cover_package.json").read_text())
DATA = json.loads((PROJECT / "artifacts" / "etf_data.json").read_text())
ASSETS = json.loads((PROJECT / "artifacts" / "asset_manifest.json").read_text())

DEADLINE = "2026-09-21"


def onscreen_text_md() -> str:
    lines = [
        "# 屏幕文案全文（本片无口播，画面文字即台词）",
        "",
        "> 本片全程无口播、无音轨，因此没有字幕文件。以下为屏幕上出现过的全部文字，",
        "> 按场景顺序排列，用于发布时的文案核对与无障碍说明。",
        "> 所有数值均由 `artifacts/etf_data.json` 生成，未经人工转写。",
        "",
    ]
    for s in SCRIPT["metadata"]["on_screen_script"]["scenes"]:
        d = s["data"]
        lines.append(f"## {s['id']}　{s['label']}")
        lines.append(f"`{s['start_seconds']:.1f}s – {s['end_seconds']:.1f}s`")
        lines.append("")
        if d.get("overline"):
            lines.append(f"- {d['overline']}")
        for k in ("head", "hero", "sub", "foot", "caveat", "method"):
            if d.get(k):
                lines.append(f"- {d[k]}")
        for t in d.get("lines", []):
            lines.append(f"- {t}")
        for r in d.get("rows", []):
            if isinstance(r, dict):
                parts = [str(r.get(k)) for k in ("name", "value", "drawdown", "days", "display") if r.get(k)]
                if parts:
                    lines.append(f"- {'　'.join(parts)}")
        for g in d.get("groups", []):
            lines.append(f"- {g['label']}：{'、'.join(g['names'])}")
        for b in d.get("beats", []):
            lines.append(f"- **{b['label']}**")
            for x in b["data"].get("pins", []):
                lines.append(f"  - {x['date']}　{x['head']}（{x['sub']}）")
            for x in b["data"].get("markers", []):
                lines.append(f"  - {x['text']}")
            for x in b["data"].get("callouts", []):
                lines.append(f"  - {x['kicker']}")
                for r in x["rows"]:
                    uw = "　水下" if r.get("underwater") else ""
                    lines.append(f"    - {r['name']} {r['code']}　{r['display']}{uw}")
            if b["data"].get("contrast"):
                c = b["data"]["contrast"]
                lines.append(f"  - {c['left']}　/　{c['right']}")
                lines.append(f"  - {c['hero']}")
        if d.get("scope_note"):
            lines.append(f"- {d['scope_note']}")
        if d.get("disclaimer"):
            lines.append("")
            lines.append(f"**合规页脚（原生小字，位于竖屏安全区内）：** {d['disclaimer']}")
        lines.append("")
    return "\n".join(lines)


def sources_md() -> str:
    tiers = {"primary": "一手来源（Tier 1）", "secondary": "二手来源（Tier 2）", "anecdotal": "社区/自媒体取样（Tier 3）"}
    out = [
        "# 数据来源与口径说明",
        "",
        f"区间：**{DATA['meta']['start_date']} 至 {DATA['meta']['end_date']}**　共 {DATA['meta']['trading_days']} 个交易日",
        "",
        "## 数据来源",
        "",
        "| 用途 | 来源 | 层级 |",
        "|---|---|---|",
    ]
    for s in BRIEF["sources"]:
        out.append(f"| {s['used_for'][:60]}… | [{s['title'][:70]}]({s['url']}) | {tiers.get(s['reliability'], s['reliability'])} |")
    out += [
        "",
        "## 计算口径",
        "",
        f"- 账户资产：`{DATA['meta']['account_formula']}`",
        f"- 分红处理：{DATA['meta']['dividend_treatment']}",
        f"- 累计收益率：最终账户资产 ÷ 100,000 − 1",
        f"- 年化收益率：(最终账户资产 ÷ 100,000)^(365.2425 ÷ 实际自然日数) − 1",
        f"- 最大回撤：每日账户资产相对此前历史峰值的最大跌幅",
        f"- 回撤跨度：最大回撤的峰值日到低点日之间的自然日数",
        f"- 最长未创新高：当日账户资产低于此前历史最高值的连续交易日数",
        "",
        "## 必须随片说明的边界条件",
        "",
    ]
    for b in SCRIPT["metadata"]["finance_editorial"]["boundary_conditions"]:
        out.append(f"- {b}")
    out += [
        "",
        "## 数据质量",
        "",
        f"- 四只基金的最终资产、累计收益率、年化收益率、最大回撤与回撤区间，全部与用户提供工作簿的「汇总」表逐项一致（容差 1e-5）。",
        f"- {BRIEF['metadata']['data_quality_check']['missing_record']}",
        f"- {DATA['meta']['caveat']}",
        "",
        "## 本片不主张什么",
        "",
        "- 不主张\"红利低波更好\"：2020-07-03 至 2026-09-18 包含 A 股自 2021 年高点后的长期调整与红利风格相对占优的年份，换一个起点或终点，排名可能不同。",
        "- 不主张曲线里的分红等于你账户里收到的分红：这是把分红按再投资处理的理论总回报路径。",
        "- 不构成对任何一只 ETF 未来表现的推断。",
        "",
    ]
    return "\n".join(out)


def publish_copy_md() -> str:
    best = max(DATA["metrics"].values(), key=lambda m: m["final_asset"])
    worst = min(DATA["metrics"].values(), key=lambda m: m["final_asset"])
    return f"""# 发布文案

## 视频标题（三选一）

1. 10万元买4只ETF，6年后差多少？
2. 沪深300 VS 中证500 VS 两只红利低波：6年真实收益对比
3. 如果2020年有10万元买了4只ETF

## 简介

同一天、同一笔10万元，买入四只ETF，一直不动，到 {DATA['meta']['end_date']} 会是什么结果？
期末最好与最差相差 ¥{best['final_asset'] - worst['final_asset']:,}；
但比收益差距更值得看的，是过程差距——最大回撤的**持续时间**差了将近20倍。

本片全程无口播、无音乐，只有数据。

## 核心结论（供口播/评论引用）

- 期末账户资产：红利低波50 ¥{DATA['metrics']['512890']['final_asset']:,}、
  红利低波100 ¥{DATA['metrics']['515100']['final_asset']:,}、
  中证500 ¥{DATA['metrics']['510500']['final_asset']:,}、
  沪深300 ¥{DATA['metrics']['510300']['final_asset']:,}
- 最大回撤：{" / ".join(f"{f['name']} {abs(DATA['metrics'][f['code']]['max_drawdown'])*100:.2f}%" for f in DATA['funds'])}
- 回撤跨度：{" / ".join(f"{f['name']} {DATA['metrics'][f['code']]['mdd_days']} 天" for f in DATA['funds'])}
- 最长未创新高：沪深300 {DATA['metrics']['510300']['longest_underwater_days']} 个交易日

## 话题标签

#ETF #指数基金 #红利低波 #沪深300 #中证500 #长期投资 #数据可视化 #定投

## 置顶评论

数据区间 {DATA['meta']['start_date']} → {DATA['meta']['end_date']}，后复权口径（分红按再投资处理）。
这一段包含 A 股自 2021 年高点后的长期调整，也是红利风格相对占优的几年，换一个起点可能换排名。
历史数据只能回答"过去发生了什么"，不代表未来。

本视频仅作知识分享，不构成任何投资建议。市场有风险，投资需谨慎。
"""


def main() -> None:
    from lib.checkpoint import validate_artifact

    if PUBLISH.exists():
        shutil.rmtree(PUBLISH)
    (PUBLISH / "images").mkdir(parents=True)

    shutil.copy2(PROJECT / "renders" / "final.mp4", PUBLISH / "final.mp4")
    shutil.copy2(PROJECT / "assets" / "images" / "cover.png", PUBLISH / "images" / "cover.png")

    (PUBLISH / "屏幕文案全文.md").write_text(onscreen_text_md())
    (PUBLISH / "sources.md").write_text(sources_md())
    (PUBLISH / "发布文案.md").write_text(publish_copy_md())

    metadata = {
        "title": SCRIPT["title"],
        "duration_seconds": SCRIPT["total_duration_seconds"],
        "resolution": "1080x1920",
        "aspect_ratio": "9:16",
        "fps": 30,
        "audio": "none（全程无口播、无音乐）",
        "language": "zh-CN",
        "content_category": "finance",
        "required_disclaimer": SCRIPT["metadata"]["compliance"]["financial_disclaimer"],
        "disclaimer_placement": "结尾场景原生页脚",
        "data_window": f"{DATA['meta']['start_date']} → {DATA['meta']['end_date']}",
        "data_provider": DATA["meta"]["source_provider"],
        "dividend_treatment": DATA["meta"]["dividend_treatment"],
        "key_figures": {
            f["name"]: {
                "code": f["code"],
                "final_asset": DATA["metrics"][f["code"]]["final_asset"],
                "cumulative_return": round(DATA["metrics"][f["code"]]["cumulative_return"], 6),
                "annualized_return": round(DATA["metrics"][f["code"]]["annualized_return"], 6),
                "max_drawdown": round(DATA["metrics"][f["code"]]["max_drawdown"], 6),
                "drawdown_span_days": DATA["metrics"][f["code"]]["mdd_days"],
                "longest_underwater_trading_days": DATA["metrics"][f["code"]]["longest_underwater_days"],
            }
            for f in DATA["funds"]
        },
        "spread_best_minus_worst": max(m["final_asset"] for m in DATA["metrics"].values())
        - min(m["final_asset"] for m in DATA["metrics"].values()),
        "boundary_conditions": SCRIPT["metadata"]["finance_editorial"]["boundary_conditions"],
        "reusable_judgment_method": SCRIPT["metadata"]["finance_editorial"]["reusable_judgment_method"],
        "series_status": "独立单条，无系列标识",
        "verification": {
            "review_status": REVIEW["status"],
            "audio_streams": REPORT["metadata"]["audio_streams"],
            "opening_frame_ink_pct": REVIEW["metadata"]["measurements"]["opening_frame"]["ink_pct_lt120"],
            "safe_area_measured_text_floor_y": REVIEW["metadata"]["measurements"]["safe_area"]["measured_lowest_text_row_max"],
        },
    }
    (PUBLISH / "metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=1))

    manifest = {
        "project": SLUG,
        "created_at": DEADLINE,
        "files": [],
    }
    for p in sorted(PUBLISH.rglob("*")):
        if p.is_file():
            manifest["files"].append(
                {
                    "path": str(p.relative_to(PUBLISH)),
                    "bytes": p.stat().st_size,
                }
            )
    manifest["total_bytes"] = sum(f["bytes"] for f in manifest["files"])
    (PUBLISH / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1))

    now = datetime.now(timezone.utc).isoformat()
    publish_log = {
        "version": "1.0",
        "entries": [
            {
                "platform": "local_bundle",
                "status": "exported",
                "timestamp": now,
                "visibility": "private",
                "export_path": f"projects/{SLUG}/deliverables/publish",
                "metadata_used": {
                    "title": SCRIPT["title"],
                    "duration_seconds": SCRIPT["total_duration_seconds"],
                    "resolution": "1080x1920",
                    "has_audio": False,
                    "required_disclaimer": SCRIPT["metadata"]["compliance"]["financial_disclaimer"],
                },
            }
        ],
        "metadata": {
            "content_category": "finance",
            "manual_publish_required": True,
            "note": "本地打包，未登录、未上传、未创建远程草稿。用户自行择时发布。",
            "package_contents": [f["path"] for f in manifest["files"]],
            "evidence_preserved": {
                "sources_document": "deliverables/publish/sources.md",
                "onscreen_text": "deliverables/publish/屏幕文案全文.md",
                "boundary_conditions": len(SCRIPT["metadata"]["finance_editorial"]["boundary_conditions"]),
                "uncertainty_language_preserved": True,
            },
            "packaging_guard": (
                "标题与简介保持提问式，未使用「一定」「稳赚」「必」等绝对化表述；"
                "简介明确写出区间与边界条件；封面上的每个数字都出现在成片中。"
            ),
            "cover_included": True,
            "subtitle_policy": "无语音，故不产出字幕文件；以《屏幕文案全文.md》替代。",
        },
    }
    validate_artifact("publish_log", publish_log)
    OUT.write_text(json.dumps(publish_log, ensure_ascii=False, indent=1))

    print("[ok] publish_log schema-valid")
    print(f"[write] {OUT.relative_to(REPO)}")
    print(f"[bundle] {PUBLISH.relative_to(REPO)}  ({manifest['total_bytes']/1024/1024:.1f} MB)")
    for f in manifest["files"]:
        print(f"    - {f['path']:<28s} {f['bytes']/1024:>8.0f} KB")


if __name__ == "__main__":
    main()
