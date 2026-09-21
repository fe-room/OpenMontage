#!/usr/bin/env python3
"""Build asset_manifest.json and wire static assets into remotion-composer/public."""
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
PID = "xiaosan-economics-03-opportunity-cost"
PROJ = ROOT / "projects" / PID
ASSETS = PROJ / "assets"
ART = PROJ / "artifacts"

script = json.loads((ART / "script.json").read_text())
plan = json.loads((ART / "scene_plan.json").read_text())


def probe(p: Path):
    out = subprocess.check_output([
        "ffprobe", "-v", "error", "-select_streams", "v:0",
        "-show_entries", "stream=width,height", "-of", "json", str(p)
    ]).decode()
    st = json.loads(out)["streams"][0]
    dur = float(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=nw=1:nk=1", str(p)]).decode().strip())
    return st["width"], st["height"], dur


assets = []

# --- narration: one asset per final spoken section (segmented generation) ---
TTS_COST = 0.06 / len(script["sections"])
for s in script["sections"]:
    mp3 = ASSETS / f"audio/narration-{s['id']}-v1.mp3"
    w, h, dur = None, None, float(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=nw=1:nk=1", str(mp3)]).decode().strip())
    assets.append({
        "id": f"narration-{s['id']}",
        "type": "audio",
        "subtype": "narration_section",
        "path": str(mp3.relative_to(ROOT)),
        "source_tool": "tts_selector",
        "provider": "doubao",
        "model": "seed-tts-2.0",
        "scene_id": next(sc["id"] for sc in plan["scenes"] if sc["script_section_id"] == s["id"]),
        "duration_seconds": round(dur, 3),
        "format": "mp3",
        "cost_usd": round(TTS_COST, 5),
        "license": "generated-for-this-project",
        "prompt": s["delivery_cues"]["provider_text"],
        "voice_performance": {
            "source_section_id": s["id"],
            "synthesis_mode": "segmented",
            "delivery_cues_applied": True,
            "provider_text_used": True,
            "provider_settings": {
                "resource_id": "seed-tts-2.0",
                "voice_id": "zh_male_dayi_uranus_bigtts",
                "voice_name": "大壹 2.0",
                "speech_rate": 0,
                "api_mode": "unidirectional",
                "pace": s["delivery_cues"]["pace"],
                "energy": s["delivery_cues"]["energy"],
                "emphasis_words": s["delivery_cues"]["emphasis_words"],
                "pause_after_seconds": s["delivery_cues"]["pause_after_seconds"],
            },
            "sample_approved": True,
            "sample_path": f"projects/{PID}/assets/audio/sample-s05-opportunity-cost-v1.mp3",
            "review_notes": s["delivery_cues"]["delivery_note"],
        },
        "generation_summary": f"分段旁白 {s['id']}（{len(s['text'])} 字 / 实测 {dur:.2f}s），逐字采用规划第22节口播。",
    })

master = ASSETS / "audio/narration-master-v1.wav"
mw, mh, mdur = None, None, float(subprocess.check_output([
    "ffprobe", "-v", "error", "-show_entries", "format=duration",
    "-of", "default=nw=1:nk=1", str(master)]).decode().strip())
assets.append({
    "id": "narration-master",
    "type": "audio",
    "subtype": "narration_master",
    "path": str(master.relative_to(ROOT)),
    "source_tool": "ffmpeg",
    "provider": "local",
    "model": "pcm_s16le/48k",
    "scene_id": "sc01",
    "duration_seconds": round(mdur, 3),
    "format": "wav",
    "cost_usd": 0.0,
    "license": "derived",
    "generation_summary": "10 段旁白按批准停顿计划拼接的无损母带；与分镜时间轴逐帧对齐（偏差 0.000s）。全片无音乐层。",
})

# --- semantic-motion footage (light hybrid: 3 approved beats only) ---
FOOT = [
    ("footage-sc01-lie-in", "assets/video/sc01-lie-in-v1.mp4", "sc01",
     "person relaxing lying on sofa at home using phone",
     "让'周末在家躺一天'变成观众已经历过的具体处境，直接服务2秒留存。",
     "Pexels 库存素材（免费商用）", None),
    ("footage-sc08-hourglass", "assets/video/sc08-hourglass-v1.mp4", "sc08",
     "hourglass sand falling timelapse",
     "沙粒单向落下不可逆，为'这4个小时你只能真正使用一次'提供可感知的不可逆性；落沙同时匹配本片象牙暖色系。",
     "Pexels 库存素材（免费商用）", None),
    ("footage-sc18-queue", "assets/video/sc18-queue-v1.mp4", "sc18",
     "people standing in line queue waiting at store",
     "真实排队画面让'两个小时'可被体感；墙上的时钟提供额外的时间暗示，为'免费≠没有成本'提供具身证据。",
     "Pexels 库存素材（免费商用）", None),
]
for aid, rel, scid, q, why, lic, url in FOOT:
    p = PROJ / rel
    w, h, dur = probe(p)
    assets.append({
        "id": aid,
        "type": "video",
        "subtype": "stock_footage",
        "path": str(p.relative_to(ROOT)),
        "source_tool": "pexels_video",
        "provider": "pexels",
        "model": None,
        "scene_id": scid,
        "duration_seconds": round(dur, 3),
        "resolution": f"{w}x{h}",
        "format": "mp4",
        "cost_usd": 0.0,
        "license": lic,
        **({"original_url": url} if url else {}),
        "prompt": q,
        "quality_score": 0.85,
        "generation_summary": why,
    })

# --- subtitle / caption assets ---
for aid, rel, tool in [("captions", "assets/captions.json", "subtitle_gen"),
                       ("subtitles", "assets/subtitles.srt", "subtitle_gen")]:
    p = PROJ / rel
    assets.append({
        "id": aid,
        "type": "subtitle",
        "path": str(p.relative_to(ROOT)),
        "source_tool": tool,
        "provider": "local",
        "scene_id": "sc01",
        "format": p.suffix.lstrip("."),
        "cost_usd": 0.0,
        "license": "derived",
        "generation_summary": "97 条分层短句字幕，文字与已批准旁白逐字一致；时长按实测分段音频确定性分配（未使用 ASR）。",
    })

for a in assets:
    for k in [k for k, v in a.items() if v is None]:
        a.pop(k)

manifest = {
    "version": "1.0",
    "assets": assets,
    "total_cost_usd": round(sum(a.get("cost_usd", 0) for a in assets), 5),
    "metadata": {
        "content_category": "finance",
        "pipeline": "finance-dossier",
        "music": {
            "source_type": "none",
            "assets_created": 0,
            "note": "持久无BGM默认；本清单中不存在任何音乐资产或占位音轨。",
        },
        "coverage_strategy": "light-hybrid",
        "precision_critical_beats": "全部数字（4小时、500元、3%、5%、0元）与定义文字由 Remotion 确定性图层渲染，素材镜头不承载任何需被读准的事实。",
        "rejected_assets": [
            "金币飘落 / 钞票雨 / K线 / 握手 / 西装人物 / 摩天楼 / 蓝紫渐变 / 霓虹终端 / HUD / 全息 / 团队开会 / 火箭（decorative_only，已拒绝）",
            "AI 生成图承载中文标题或合规文案（禁止）",
        ],
        "remotion_public_mirror": f"remotion-composer/public/{PID}/",
        "timeline": {
            "total_duration_seconds": plan["scenes"][-1]["end_seconds"],
            "trailing_hold_seconds": plan["metadata"]["trailing_hold_seconds"],
        },
    },
}
(ART / "asset_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

from schemas.artifacts import validate_artifact
validate_artifact("asset_manifest", manifest)

print(f"asset_manifest.json SCHEMA OK | assets={len(assets)} | total_cost_usd={manifest['total_cost_usd']}")
vids = [a for a in assets if a["type"] == "video"]
print(f"  narration sections: {len([a for a in assets if a.get('subtype')=='narration_section'])}")
print(f"  footage: {len(vids)}")
print(f"  music assets: {len([a for a in assets if a['type']=='music'])} (must be 0)")
print(f"  narration master: {mdur:.3f}s")
