#!/usr/bin/env python3
"""Rebuild script + scene_plan timelines from real TTS durations, then
concatenate the narration master and build captions from doubao timestamps."""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
ART = ROOT / "projects/xiaosan-economics-03-opportunity-cost/artifacts"
AUD = ROOT / "projects/xiaosan-economics-03-opportunity-cost/assets/audio"

LEAD_IN = 0.12
TAIL = 3.00
PAUSE_AFTER = {
    "s01": 0.35, "s02": 1.20, "s03": 0.50, "s04": 0.60, "s05": 1.20,
    "s06": 1.20, "s07": 1.20, "s08": 0.80, "s09": 0.90, "s10": TAIL,
}

script = json.loads((ART / "script.json").read_text())
old = {s["id"]: (s["start_seconds"], s["end_seconds"]) for s in script["sections"]}

# --- real durations ---
durs = {}
for s in script["sections"]:
    f = AUD / f"narration-{s['id']}-v1.mp3"
    durs[s["id"]] = float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(f)]).decode().strip())

# --- rebuild section timeline ---
t = LEAD_IN
sec_new = {}
for s in script["sections"]:
    sid = s["id"]
    start = t
    end = start + durs[sid]
    sec_new[sid] = (round(start, 3), round(end, 3))
    s["start_seconds"] = round(start, 3)
    s["end_seconds"] = round(end, 3)
    t = end + PAUSE_AFTER[sid]

TOTAL = round(t, 3)
script["total_duration_seconds"] = TOTAL
script["metadata"]["timeline_basis"] = {
    "source": "real doubao seed-tts-2.0 segment durations",
    "lead_in_seconds": LEAD_IN,
    "tail_seconds": TAIL,
    "pause_after_seconds": PAUSE_AFTER,
    "note": "时间轴以实测配音时长为权威依据，不迁就提案阶段的字数估算。",
}
script["metadata"]["section_audio_durations"] = {k: round(v, 3) for k, v in durs.items()}
script["metadata"]["pacing_actual"] = {
    "chars_per_second_measured": round(sum(len(s["text"]) for s in script["sections"]) /
                                       sum(durs.values()), 2),
    "total_speech_seconds": round(sum(durs.values()), 2),
    "note": "实测豆包 seed-tts-2.0 / 大壹 2.0、speech_rate=0 的合成语速。",
}
(ART / "script.json").write_text(json.dumps(script, ensure_ascii=False, indent=2), encoding="utf-8")

# NOTE: scene_plan is NOT rescaled here. It is derived from script timings by
# build_scene_plan.py (scenes are stored as fractions of their script section),
# which keeps the two artifacts consistent without double-scaling.

# --- concat narration master (16-bit 48k wav, lossless splice) ---
parts = []
for i, s in enumerate(script["sections"]):
    src = AUD / f"narration-{s['id']}-v1.mp3"
    if i:
        parts.append("|" + str(PAUSE_AFTER[script["sections"][i - 1]["id"]]))
    parts.append(str(src))

tmp = AUD / "concat-list.txt"
lines = []
for s in script["sections"]:
    lines.append(f"file '{AUD / ('narration-%s-v1.mp3' % s['id'])}'")
tmp.write_text("\n".join(lines) + "\n", encoding="utf-8")

# single pass: resample each, insert exact silence, concat with ffmpeg filter_complex
inputs, filters = [], []
idx = 0
labels = []
if LEAD_IN > 0:
    inputs += ["-f", "lavfi", "-t", str(LEAD_IN), "-i", "anullsrc=r=48000:cl=mono"]
    filters.append(f"[{idx}:a]aresample=48000,aformat=sample_fmts=s16:channel_layouts=mono[a{idx}]")
    labels.append(f"[a{idx}]")
    idx += 1
for s in script["sections"]:
    inputs += ["-i", str(AUD / f"narration-{s['id']}-v1.mp3")]
    filters.append(f"[{idx}:a]aresample=48000,aformat=sample_fmts=s16:channel_layouts=mono[a{idx}]")
    labels.append(f"[a{idx}]")
    idx += 1
    p = PAUSE_AFTER[s["id"]]
    if p > 0:
        inputs += ["-f", "lavfi", "-t", str(p), "-i", "anullsrc=r=48000:cl=mono"]
        filters.append(f"[{idx}:a]aresample=48000,aformat=sample_fmts=s16:channel_layouts=mono[a{idx}]")
        labels.append(f"[a{idx}]")
        idx += 1

master = AUD / "narration-master-v1.wav"
fc = ";".join(filters) + ";" + "".join(labels) + f"concat=n={len(labels)}:v=0:a=1[out]"
subprocess.run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", fc,
                "-map", "[out]", "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "1", str(master)], check=True)
mdur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries",
                                      "format=duration", "-of", "default=nw=1:nk=1",
                                      str(master)]).decode().strip())
print(f"narration master: {master.name}  {mdur:.3f}s  (timeline {TOTAL}s, delta {mdur-TOTAL:+.3f}s)")

# --- captions from doubao timestamps (grouped by semantic phrase) ---
def load_words(sid):
    meta = json.loads((AUD / f"narration-{sid}-v1.mp3.json").read_text())
    words = []
    for sent in meta.get("sentences", []):
        for w in sent.get("words", []):
            if w.get("word"):
                words.append((w["word"], float(w["startTime"]), float(w["endTime"])))
    return words

CAPTION_MAP = {
 "s01": [["周末在家躺一天"], ["一分钱没花"], ["这一天的成本是不是0"]],
 "s02": [["按我们平时理解成本的方式"], ["好像确实是这样"], ["没买东西", "没打车"], ["没出去吃饭"], ["银行卡一分钱都没少"], ["怎么看都是0成本"]],
 "s03": [["但经济学算成本"], ["有时候根本不只看你花了多少钱"], ["这一天你本来还能拿去干什么"]],
 "s04": [["比如这个周六下午你一共有4个小时"], ["你可以在家休息"], ["也可以拍一期视频"], ["可以接一个兼职"], ["或者去健身"], ["这4个小时你只能真正使用一次"], ["最后你决定什么都不干就在家休息"], ["从银行卡来看支出确实是0"]],
 "s05": [["但经济学会继续问"], ["如果你没有选择休息"], ["你最可能去做的那件事是什么"], ["如果不休息你大概率会去接一个兼职"], ["那个兼职对你的净价值"], ["大概是500块钱"], ["你确实放弃了一个价值大概500块钱的替代方案"], ["这就是机会成本"]],
 "s06": [["不过这里有一个特别容易搞错的地方"], ["你还可以拍视频可以健身可以出去玩"], ["那这些是不是全部都要加起来"], ["不是"], ["因为就算你不休息"], ["你也不可能同时完整做完所有这些事情"], ["机会成本通常关注的是"], ["你放弃掉的最佳替代方案"], ["不是所有BCD全部加起来"], ["而是那些没有被选择的方案里"], ["对你最有价值的那个"]],
 "s07": [["不过说到这里可能又会产生另一个误会"], ["既然休息的机会成本可能是500块钱"], ["那是不是说明我躺这4个小时就亏了500"], ["也不是"], ["机会成本告诉你的只是"], ["你为了现在这个选择放弃了什么"], ["它并没有替你决定"], ["这个选择到底对不对"], ["如果你这一周已经非常累"], ["你觉得休息4个小时带来的恢复"], ["比接那单兼职对你更重要"], ["那么休息完全可能就是更好的选择"], ["有机会成本不等于不应该做"], ["睡觉有机会成本"], ["陪家人有机会成本"], ["学习有机会成本"], ["工作同样有机会成本"], ["只要你在做选择"], ["其他可能性就一定会被放弃"]],
 "s08": [["而且机会成本也不意味着"], ["所有东西都必须换算成钱"], ["有些时候你放弃的是收入"], ["有些时候放弃的是时间"], ["有些时候是精力"], ["还有些时候是陪伴休息或者一次学习机会"], ["所以经济学里的成本"], ["其实比我们平时理解的花了多少钱要宽得多"], ["比如商场送一杯免费咖啡"], ["咖啡确实不要钱"], ["但如果你要排两个小时的队"], ["那两个小时并不是免费的"], ["免费不等于没有成本"]],
 "s09": [["投资里也是一样"], ["假设两个选择的风险流动性和其他限制都差不多"], ["A最后赚了3%"], ["B本来可以赚5%"], ["那从机会成本的角度"], ["你还会多问一句"], ["我为了选择A放弃了什么"], ["当然现实里的投资选择不会这么简单"], ["风险流动性和确定性往往都不同"], ["所以不能只拿最终收益率机械比较"], ["但机会成本会提醒我们一件事"], ["判断一个选择"], ["有时候不能只看它给了你什么"], ["还要看"], ["为了它你放弃了什么"]],
 "s10": [["所以下次再遇到一件免费的事情"], ["别急着只问"], ["我要花多少钱"], ["也可以多问一句"], ["为了它我放弃了什么"]],
}

captions = []
for s in script["sections"]:
    sid = s["id"]
    words = load_words(sid)
    base = s["start_seconds"]
    i = 0
    for group in CAPTION_MAP[sid]:
        need = sum(len(g) for g in group)
        take = words[i:i + need]
        if not take:
            i += need
            continue
        st = base + take[0][1]
        en = base + take[-1][2]
        captions.append({"id": f"cap-{sid}-{len(captions)+1:02d}", "section_id": sid,
                         "text": "".join(group), "start_seconds": round(st, 3),
                         "end_seconds": round(en, 3)})
        i += need
    if i < len(words):
        print(f"  note: {sid} {len(words)-i} words unused by caption map")

# enforce monotonicity
for a, b in zip(captions, captions[1:]):
    if b["start_seconds"] < a["end_seconds"] - 0.001:
        b["start_seconds"] = a["end_seconds"]
    if b["end_seconds"] <= b["start_seconds"]:
        b["end_seconds"] = b["start_seconds"] + 0.4

(AUD.parent / "captions.json").write_text(json.dumps(captions, ensure_ascii=False, indent=2), encoding="utf-8")

def ts(x):
    h = int(x // 3600); m = int(x % 3600 // 60); s = x % 60
    return f"{h:02d}:{m:02d}:{s:06.3f}".replace(".", ",")

srt = []
for n, c in enumerate(captions, 1):
    srt.append(f"{n}\n{ts(c['start_seconds'])} --> {ts(c['end_seconds'])}\n{c['text']}\n")
(AUD.parent / "subtitles.srt").write_text("\n".join(srt), encoding="utf-8")

print(f"captions: {len(captions)} | subtitles.srt written")
print(f"TIMELINE TOTAL = {TOTAL}s")
for s in script["sections"]:
    print(f"  {s['id']} {s['start_seconds']:>8.3f} - {s['end_seconds']:>8.3f}  ({s['end_seconds']-s['start_seconds']:>6.2f}s)")
