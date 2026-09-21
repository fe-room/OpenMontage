#!/usr/bin/env python3
"""Build captions.json / subtitles.srt for xiaosan-economics-03.

Doubao does not persist word-level timestamps locally (its metadata JSON keeps
only redacted audio-chunk events), so caption timing is deterministic:
each section's REAL audio duration is distributed across its semantic
phrase groups by punctuation-aware character weight. No ASR is used, so
captions stay byte-identical to the approved narration.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
ART = ROOT / "projects/xiaosan-economics-03-opportunity-cost/artifacts"
ASSETS = ROOT / "projects/xiaosan-economics-03-opportunity-cost/assets"

CAPTION_MAP = {
 "s01": ["周末在家躺一天", "一分钱没花", "这一天的成本是不是0"],
 "s02": ["按我们平时理解成本的方式", "好像确实是这样", "没买东西", "没打车", "没出去吃饭",
         "银行卡一分钱都没少", "怎么看都是0成本"],
 "s03": ["但经济学算成本", "有时候根本不只看你花了多少钱", "它还会问你一个问题",
         "这一天你本来还能拿去干什么"],
 "s04": ["比如这个周六下午你一共有4个小时", "你可以在家休息", "也可以拍一期视频", "可以接一个兼职",
         "或者去健身", "问题是这4个小时你只能真正使用一次", "最后你决定什么都不干就在家休息",
         "从银行卡来看支出确实是0"],
 "s05": ["但经济学会继续问", "如果你没有选择休息", "你最可能去做的那件事是什么",
         "假设你认真想了一下", "如果不休息你大概率会去接一个兼职", "那个兼职对你的净价值",
         "大概是500块钱", "那你选择休息的时候", "虽然没有真的掏出500块钱",
         "但你确实放弃了一个价值大概500块钱的替代方案", "这就是机会成本"],
 "s06": ["不过这里有一个特别容易搞错的地方", "你还可以拍视频可以健身可以出去玩",
         "那这些是不是全部都要加起来", "不是", "因为就算你不休息",
         "你也不可能同时完整做完所有这些事情", "机会成本通常关注的是", "你放弃掉的最佳替代方案", "也就是说你选择A真正付出的机会成本",
         "不是所有BCD全部加起来", "而是那些没有被选择的方案里", "对你最有价值的那个"],
 "s07": ["不过说到这里可能又会产生另一个误会", "既然休息的机会成本可能是500块钱",
         "那是不是说明我躺这4个小时就亏了500", "也不是", "机会成本告诉你的只是",
         "你为了现在这个选择放弃了什么", "它并没有替你决定", "这个选择到底对不对",
         "如果你这一周已经非常累", "你觉得休息4个小时带来的恢复", "比接那单兼职对你更重要",
         "那么休息完全可能就是更好的选择", "所以有机会成本不等于不应该做", "睡觉有机会成本",
         "陪家人有机会成本", "学习有机会成本", "工作同样有机会成本", "只要你在做选择",
         "其他可能性就一定会被放弃"],
 "s08": ["而且机会成本也不意味着", "所有东西都必须换算成钱", "有些时候你放弃的是收入",
         "有些时候放弃的是时间", "有些时候是精力", "还有些时候是陪伴休息或者一次学习机会",
         "所以经济学里的成本", "其实比我们平时理解的花了多少钱要宽得多", "比如商场送一杯免费咖啡",
         "咖啡确实不要钱", "但如果你要排两个小时的队", "那两个小时并不是免费的",
         "所以免费不等于没有成本"],
 "s09": ["投资里也是一样", "假设两个选择的风险流动性和其他限制都差不多", "A最后赚了3%",
         "B本来可以赚5%", "那从机会成本的角度", "你还会多问一句", "我为了选择A放弃了什么",
         "当然现实里的投资选择不会这么简单", "风险流动性和确定性往往都不同",
         "所以不能只拿最终收益率机械比较", "但机会成本会提醒我们一件事", "判断一个选择",
         "有时候不能只看它给了你什么", "还要看", "为了它你放弃了什么"],
 "s10": ["所以下次再遇到一件免费的事情", "别急着只问", "我要花多少钱", "也可以多问一句",
         "为了它我放弃了什么"],
}

PUNCT = "，。！？、；："
norm = lambda t: re.sub(r"[\s，。！？、；：“”‘’（）()\-—…《》\"']", "", t)


def weight(text: str) -> float:
    """Punctuation-aware weight: TTS pauses slightly at punctuation."""
    punct = sum(1 for ch in text if ch in PUNCT)
    return len(norm(text)) + 1.6 * punct


script = json.loads((ART / "script.json").read_text())
captions = []
for s in script["sections"]:
    sid = s["id"]
    groups = CAPTION_MAP[sid]
    # 1) caption text must reconstruct the section narration exactly
    joined = norm("".join(groups))
    target = norm(s["text"])
    assert joined == target, f"caption/section mismatch in {sid}\n  cap={joined}\n  sec={target}"

    start = s["start_seconds"]
    dur = s["end_seconds"] - s["start_seconds"]
    wts = [weight(g) for g in groups]
    total_w = sum(wts)
    t = start
    for g, w in zip(groups, wts):
        seg = dur * w / total_w
        captions.append({
            "id": f"cap-{sid}-{len(captions)+1:02d}",
            "section_id": sid,
            "text": g,
            "start_seconds": round(t, 3),
            "end_seconds": round(t + seg, 3),
        })
        t += seg

# 2) monotonic + last caption must not exceed the timeline
for a, b in zip(captions, captions[1:]):
    assert b["start_seconds"] >= a["end_seconds"] - 1e-6, f"caption overlap {a['id']}->{b['id']}"
assert captions[-1]["end_seconds"] <= script["total_duration_seconds"] + 1e-6

# 3) every section fully covered, no gaps inside sections
from collections import defaultdict
by_sec = defaultdict(list)
for c in captions:
    by_sec[c["section_id"]].append(c)
for s in script["sections"]:
    cs = by_sec[s["id"]]
    assert cs, f"no captions for {s['id']}"
    assert abs(cs[0]["start_seconds"] - s["start_seconds"]) < 1e-6
    assert abs(cs[-1]["end_seconds"] - s["end_seconds"]) < 1e-6

ASSETS.mkdir(parents=True, exist_ok=True)
(ASSETS / "captions.json").write_text(json.dumps({
    "version": "1.0",
    "timing_method": "deterministic punctuation-aware distribution over real per-section TTS durations",
    "timing_method_note": "豆包未在本地持久化词级时间戳，故不使用 ASR；字幕文字与已批准旁白逐字一致。",
    "total_duration_seconds": script["total_duration_seconds"],
    "captions": captions,
}, ensure_ascii=False, indent=2), encoding="utf-8")


def ts(x):
    h = int(x // 3600); m = int(x % 3600 // 60); sec = x % 60
    return f"{h:02d}:{m:02d}:{sec:06.3f}".replace(".", ",")


srt = []
for n, c in enumerate(captions, 1):
    srt.append(f"{n}\n{ts(c['start_seconds'])} --> {ts(c['end_seconds'])}\n{c['text']}\n")
(ASSETS / "subtitles.srt").write_text("\n".join(srt), encoding="utf-8")

print(f"captions={len(captions)}  sections={len(script['sections'])}  "
      f"timeline={script['total_duration_seconds']}s")
print(f"last caption ends {captions[-1]['end_seconds']}s")
for s in script["sections"]:
    n = len(by_sec[s["id"]])
    print(f"  {s['id']}  {n:>2} captions  {s['start_seconds']:>8.3f}-{s['end_seconds']:>8.3f}")
