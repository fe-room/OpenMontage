#!/usr/bin/env python3
"""Build the local publish bundle + publish_log for xiaosan-economics-03.

Local hand-off only. Nothing is uploaded, and no account is logged into.
Metadata deliberately avoids deterministic investment claims.
"""
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
PID = "xiaosan-economics-03-opportunity-cost"
PROJ = ROOT / "projects" / PID
ART = PROJ / "artifacts"
OUT = PROJ / "deliverables" / "publish"
(OUT / "images").mkdir(parents=True, exist_ok=True)

plan = json.loads((ART / "scene_plan.json").read_text())
script = json.loads((ART / "script.json").read_text())
report = json.loads((ART / "render_report.json").read_text())
cover = json.loads((ART / "cover_package.json").read_text())

DISC = "本视频仅作知识分享，不构成任何投资建议。市场有风险，投资需谨慎。"

# --- files ---
shutil.copy(PROJ / "renders/final-v3.mp4", OUT / "final.mp4")
shutil.copy(PROJ / "assets/images/cover.png", OUT / "images/cover.png")
shutil.copy(PROJ / "assets/subtitles.srt", OUT / "subtitles.srt")

# --- chapters: one per script section (editorial unit), from the scene plan ---
sec_first_scene = {}
for sc in plan["scenes"]:
    sec_first_scene.setdefault(sc["script_section_id"], sc)

chapters = []
for s in script["sections"]:
    sc = sec_first_scene.get(s["id"])
    if not sc:
        continue
    t = sc["start_seconds"]
    chapters.append({
        "section_id": s["id"],
        "title": s["label"],
        "start_seconds": round(t, 3),
        "timestamp": f"{int(t // 60):02d}:{int(t % 60):02d}",
    })

# --- publishing metadata (no deterministic investment claim) ---
meta = {
    "title": "周末躺一天，一分钱没花，成本真的是0吗？｜小散经济学 03",
    "series": "小散经济学",
    "issue": "03",
    "topic": "机会成本",
    "duration_seconds": report["outputs"][0]["duration_seconds"],
    "resolution": "1080x1920",
    "summary": (
        "周末在家躺一天，一分钱没花——这一天的成本是不是0？"
        "本期不先给定义，而是从这个问题出发，用「周六下午4小时」一个场景完成三次认知修正："
        "没花钱不等于没成本；机会成本看的是被放弃的那个最佳替代方案，不是所有没做的事情相加；"
        "而且有机会成本，不等于这个选择是错的。"
    ),
    "description": (
        "周末在家躺一天，一分钱没花。这一天的成本是不是0？\n\n"
        "按我们平时理解「成本」的方式，好像确实是这样：没买东西、没打车、没出去吃饭，"
        "银行卡一分钱都没少。但经济学算成本，有时候根本不只看你花了多少钱——"
        "它还会问一句：这一天，你本来还能拿去干什么？\n\n"
        "本期只追一个场景：周六下午的 4 小时。你可以休息、拍视频、接兼职、去健身，"
        "但这 4 个小时你只能真正使用一次。我们一路追问下去，完成三次修正——\n"
        "1. 没花钱，不等于没成本。\n"
        "2. 机会成本不是所有没选的都加起来，而是被放弃的最佳替代方案。\n"
        "3. 有机会成本，不等于这个选择是错的。\n\n"
        "本期不展开：沉没成本、边际成本、时间价值的复杂计算、比较优势、多个投资品种的比较、"
        "机会成本的数学模型。\n\n"
        f"{DISC}"
    ),
    "tags": ["机会成本", "经济学思维", "小散经济学", "周末躺一天", "成本",
             "投资思维", "决策", "免费不等于没有成本"],
    "chapters": chapters,
    "chapters_text": "\n".join(f"{c['timestamp']} {c['title']}" for c in chapters),
    "cover": "images/cover.png",
    "subtitles": "subtitles.srt",
    "compliance": {
        "content_category": "finance",
        "financial_disclaimer": DISC,
        "publishing_rule": "标题与简介保持提问式，不把机会成本说成确定的投资结论，也不做绝对化承诺。",
    },
    "manual_publish_required": True,
    "published_by_agent": False,
}

(OUT / "metadata.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

(OUT / "发布文案.md").write_text(
    f"""# 发布文案｜小散经济学 03

## 标题
{meta['title']}

## 简介
{meta['description']}

## 标签
{' / '.join(meta['tags'])}

## 章节
{meta['chapters_text']}

## 素材
- 成片：`final.mp4`（1080×1920，{meta['duration_seconds']}s）
- 封面：`images/cover.png`（1080×1440，3:4）
- 字幕：`subtitles.srt`

> 本地交付包，未上传任何平台、未登录任何账号。发布需人工完成。
""",
    encoding="utf-8",
)

(OUT / "sources.md").write_text(
    """# 来源与事实锚点

本期为 EXPLAIN（概念解释）模式，所有定义与限定均来自下列资料；片内数字除演示算例外均无实时数值。

| 用途 | 来源 |
|---|---|
| 机会成本定义：所放弃的次优替代方案的价值；互斥备选前提 | Opportunity cost — 微观经济学基础条目 |
| 机会成本定义、显性/隐性成本区分、「免费」时间与时间价值 | Federal Reserve Bank of St. Louis, *Real-Life Examples of Opportunity Cost*, 2020-01 |
| 「为了得到某样东西而必须放弃的东西」经典表述 | N. Gregory Mankiw, *Principles of Microeconomics*, Ch.1（经 CSUN 教学讲义引述） |
| 只取次优方案、不是全部相加（120/90/40 教学算例） | EconLearn, *Opportunity Cost Explained* |
| 不可通约价值；机会成本是分析工具而非货币化公式 | UC Santa Barbara, *Opportunity Costs: The Hidden Price of Every Decision* |
| 投资比较算例（5% vs 8%，机会成本 3 个百分点）及风险差异限定 | Fiveable, *1.1 Scarcity, choice, and opportunity cost* |

## 片内数字的性质

| 数字 | 性质 |
|---|---|
| 0 元支出 | 演示情景 |
| 4 小时 | 演示情景 |
| 兼职净价值约 500 元 | 演示算例（非真实收入数据） |
| 3% / 5% | 演示算例，且画面已标注「风险、流动性与其他限制相当」 |
""",
    encoding="utf-8",
)

files = sorted(str(p.relative_to(OUT)) for p in OUT.rglob("*") if p.is_file())
(OUT / "manifest.json").write_text(json.dumps({
    "project_id": PID,
    "deliverable_type": "video",
    "files": files,
    "total_bytes": sum((OUT / f).stat().st_size for f in files),
}, ensure_ascii=False, indent=2), encoding="utf-8")

# --- publish_log ---
log = {
    "version": "1.0",
    "entries": [
        {
            "platform": "douyin",
            "status": "exported",
            "export_path": str((OUT).relative_to(ROOT)),
            "visibility": "private",
            "timestamp": "2026-09-21T10:55:00+08:00",
            "metadata_used": {
                "title": meta["title"],
                "tags": meta["tags"],
                "cover": "images/cover.png",
                "chapters": chapters,
                "subtitles": "subtitles.srt",
            },
        }
    ],
    "metadata": {
        "content_category": "finance",
        "manual_publish_required": True,
        "published_by_agent": False,
        "note": "仅生成本地交付包；未登录、未上传、未在平台创建草稿。发布由人工完成。",
        "cover_handoff": {
            "path": "images/cover.png",
            "ratio": "3:4",
            "source": cover["primary_cover"]["path"],
        },
        "compliance": meta["compliance"],
        "bundle_files": files,
    },
}
(ART / "publish_log.json").write_text(json.dumps(log, ensure_ascii=False, indent=2), encoding="utf-8")

from schemas.artifacts import validate_artifact
validate_artifact("publish_log", log)
print(f"publish bundle -> {OUT.relative_to(ROOT)}")
for f in files:
    print(f"   {f}  ({(OUT / f).stat().st_size/1e6:.2f} MB)" if (OUT / f).stat().st_size > 1e5 else f"   {f}")
print(f"chapters: {len(chapters)} | publish_log SCHEMA OK | manual_publish_required=True")
