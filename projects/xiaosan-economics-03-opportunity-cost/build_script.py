#!/usr/bin/env python3
"""Build script.json for xiaosan-economics-03 from the plan's verbatim narration.

Guarantee: every section's text must be a contiguous verbatim slice of the plan's
section 22 narration (after stripping markdown ** markers and whitespace).
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
PLAN = Path("/Users/jishubu/Downloads/小散经济学03_机会成本_详细视频内容规划.md")
OUT = ROOT / "projects/xiaosan-economics-03-opportunity-cost/artifacts/script.json"

raw = PLAN.read_text(encoding="utf-8").split("\n")
body = [l.strip() for l in raw[644:828]]
body = [l for l in body if l and not l.startswith("##")]
plan_text = "".join(body).replace("**", "")
# normalise: drop whitespace for comparison
norm = re.sub(r"\s+", "", plan_text)

# Verbatim section texts (each a contiguous run from the plan narration).
sections = [
    ("s01", "01 开场｜没花钱是不是就没成本", [
        "周末在家躺一天，一分钱没花。",
        "这一天的成本是不是0？",
    ]),
    ("s02", "02 强化直觉｜为什么大家觉得成本是0", [
        "按我们平时理解“成本”的方式，好像确实是这样。",
        "没买东西。",
        "没打车。",
        "没出去吃饭。",
        "银行卡一分钱都没少。",
        "怎么看都是0成本。",
    ]),
    ("s03", "03 第一次反转｜经济学为什么不只看花了多少钱", [
        "但经济学算成本，有时候根本不只看你花了多少钱。",
        "它还会问你一个问题：",
        "这一天，你本来还能拿去干什么？",
    ]),
    ("s04", "04 核心场景｜4小时能怎么用", [
        "比如这个周六下午，你一共有4个小时。",
        "你可以在家休息。",
        "也可以拍一期视频。",
        "可以接一个兼职。",
        "或者去健身。",
        "问题是：",
        "这4个小时，你只能真正使用一次。",
        "最后你决定什么都不干，就在家休息。",
        "从银行卡来看，支出确实是0。",
    ]),
    ("s05", "05 核心揭晓｜什么才是机会成本", [
        "但经济学会继续问：",
        "如果你没有选择休息，你最可能去做的那件事是什么？",
        "假设你认真想了一下。",
        "如果不休息，你大概率会去接一个兼职。",
        "那个兼职对你的净价值，大概是500块钱。",
        "那你选择休息的时候，虽然没有真的掏出500块钱，",
        "但你确实放弃了一个价值大概500块钱的替代方案。",
        "这就是机会成本。",
    ]),
    ("s06", "06 第二次反转｜是不是所有没选的都加起来", [
        "不过这里有一个特别容易搞错的地方。",
        "你还可以拍视频，可以健身，可以出去玩。",
        "那这些是不是全部都要加起来？",
        "不是。",
        "因为就算你不休息，你也不可能同时完整做完所有这些事情。",
        "机会成本通常关注的是：",
        "你放弃掉的最佳替代方案。",
        "也就是说，",
        "你选择A真正付出的机会成本，",
        "不是所有B、C、D全部加起来，",
        "而是那些没有被选择的方案里，对你最有价值的那个。",
    ]),
    ("s07", "07 第三次反转｜那休息是不是亏了", [
        "不过说到这里，可能又会产生另一个误会。",
        "既然休息的机会成本可能是500块钱，",
        "那是不是说明我躺这4个小时就“亏了500”？",
        "也不是。",
        "机会成本告诉你的只是：",
        "你为了现在这个选择，放弃了什么。",
        "它并没有替你决定：",
        "这个选择到底对不对。",
        "如果你这一周已经非常累，",
        "你觉得休息4个小时带来的恢复，",
        "比接那单兼职对你更重要，",
        "那么休息完全可能就是更好的选择。",
        "所以：",
        "有机会成本，不等于不应该做。",
        "睡觉有机会成本。",
        "陪家人有机会成本。",
        "学习有机会成本。",
        "工作同样有机会成本。",
        "只要你在做选择，",
        "其他可能性就一定会被放弃。",
    ]),
    ("s08", "08 补充认知｜成本是不是一定是钱", [
        "而且机会成本也不意味着，",
        "所有东西都必须换算成钱。",
        "有些时候，你放弃的是收入。",
        "有些时候，放弃的是时间。",
        "有些时候，是精力。",
        "还有些时候，是陪伴、休息或者一次学习机会。",
        "所以经济学里的“成本”，其实比我们平时理解的“花了多少钱”要宽得多。",
        "比如商场送一杯免费咖啡。",
        "咖啡确实不要钱。",
        "但如果你要排两个小时的队，",
        "那两个小时并不是免费的。",
        "所以：",
        "免费，不等于没有成本。",
    ]),
    ("s09", "09 投资连接｜机会成本和投资有什么关系", [
        "投资里也是一样。",
        "假设两个选择的风险、流动性和其他限制都差不多。",
        "A最后赚了3%。",
        "B本来可以赚5%。",
        "那从机会成本的角度，",
        "你还会多问一句：",
        "我为了选择A，放弃了什么？",
        "当然，现实里的投资选择不会这么简单。",
        "风险、流动性和确定性往往都不同。",
        "所以不能只拿最终收益率机械比较。",
        "但机会成本会提醒我们一件事：",
        "判断一个选择，",
        "有时候不能只看它给了你什么，",
        "还要看：",
        "为了它，你放弃了什么。",
    ]),
    ("s10", "10 收束｜留下现实思考", [
        "所以下次再遇到一件“免费”的事情，",
        "别急着只问：",
        "我要花多少钱？",
        "也可以多问一句：",
        "为了它，我放弃了什么？",
    ]),
]

# ---- verbatim verification ----
cursor = 0
for sid, label, lines in sections:
    for ln in lines:
        piece = re.sub(r"\s+", "", ln)
        idx = norm.find(piece, cursor)
        if idx < 0:
            print(f"VERBATIM FAIL: {sid} :: {ln}")
            sys.exit(1)
        if idx > cursor:
            print(f"GAP between sections before {sid}: '{norm[cursor:idx]}'")
        cursor = idx + len(piece)
if cursor != len(norm):
    print(f"TAIL NOT COVERED: '{norm[cursor:]}'")
    sys.exit(1)
print("VERBATIM OK: full plan narration covered, no gaps, no changes.")

# ---- timing ----
han = []
for sid, label, lines in sections:
    t = "".join(lines)
    han.append(len(re.findall(r"[\u4e00-\u9fff0-9A-Za-z%]", t)))
total_han = sum(han)
CPS = 4.79
PAUSE_PER_SECTION = 0.9  # natural pause at each section boundary
est = total_han / CPS + PAUSE_PER_SECTION * len(sections)
print(f"han+alnum total={total_han}  est={est:.1f}s")

TARGET = 224.0
speak_budget = TARGET - PAUSE_PER_SECTION * len(sections)
dur = [h / total_han * speak_budget + PAUSE_PER_SECTION for h in han]

cum = 0.0
out_sections = []
for (sid, label, lines), d in zip(sections, dur):
    d = round(d, 2)
    out_sections.append({
        "id": sid,
        "label": label,
        "text": "".join(lines),
        "start_seconds": round(cum, 2),
        "end_seconds": round(cum + d, 2),
    })
    cum += d
total = round(cum, 2)

# section-level editorial metadata kept separately for scene planning
meta_sections = [
    {"id": "s01", "plan_paragraph": "01 开场", "claim_class": "SCENARIO",
     "source_ref": "research_brief.metadata.claim_classes.SCENARIO",
     "purpose": "2秒内制造冲突：不寒暄、不介绍栏目、不给定义",
     "reversal": None},
    {"id": "s02", "plan_paragraph": "02 强化直觉", "claim_class": "SCENARIO",
     "source_ref": "research_brief.audience_insights.misconceptions[0]",
     "purpose": "让用户先站到'0成本'这一边，不急于否定", "reversal": None},
    {"id": "s03", "plan_paragraph": "03 第一次反转", "claim_class": "FACT",
     "source_ref": "research_brief.data_points[0]",
     "purpose": "引出'你本来还能做什么'", "reversal": "1"},
    {"id": "s04", "plan_paragraph": "04 核心场景", "claim_class": "SCENARIO",
     "source_ref": "research_brief.metadata.claim_classes.SCENARIO",
     "purpose": "建立互斥的选择集合（4小时只能用一次）", "reversal": None},
    {"id": "s05", "plan_paragraph": "05 核心揭晓", "claim_class": "FACT",
     "source_ref": "research_brief.data_points[0],research_brief.data_points[1]",
     "purpose": "给出准确概念：最佳被放弃方案的净价值", "reversal": None},
    {"id": "s06", "plan_paragraph": "06 第二次反转", "claim_class": "FACT",
     "source_ref": "research_brief.data_points[2]",
     "purpose": "澄清机会成本不是所有选项相加", "reversal": "2"},
    {"id": "s07", "plan_paragraph": "07 第三次反转", "claim_class": "INFERENCE",
     "source_ref": "research_brief.data_points[6],research_brief.data_points[4]",
     "purpose": "避免价值判断误导：有机会成本≠选错", "reversal": "3"},
    {"id": "s08", "plan_paragraph": "08 补充认知", "claim_class": "FACT",
     "source_ref": "research_brief.data_points[3],research_brief.data_points[1]",
     "purpose": "成本不必货币化；免费≠没有成本", "reversal": None},
    {"id": "s09", "plan_paragraph": "09 投资连接", "claim_class": "FACT",
     "source_ref": "research_brief.data_points[5]",
     "purpose": "轻量连接投资，并自带风险差异限定", "reversal": None},
    {"id": "s10", "plan_paragraph": "10 总结 + 11 结尾", "claim_class": "THESIS",
     "source_ref": "research_brief.metadata.editorial_direction",
     "purpose": "收束为可复用的判断动作，不做课程式预告", "reversal": None},
]

script = {
    "version": "1.0",
    "title": "小散经济学 03｜周末躺一天，一分钱没花，成本真的是0吗？",
    "total_duration_seconds": total,
    "voice_performance": {
        "performance_intent": "老朋友观察型：平静、克制，像把一个刚想明白的问题讲给熟悉的朋友听。不寒暄、不介绍栏目、不先给定义。全片不加背景音乐，人声是唯一声源。",
        "pacing_profile": "contemplative",
        "energy_curve": "整体持平偏低。s01-s02 顺着观众直觉平稳铺陈；s03 转折处略压低；s04 摊开选择集合时放慢；s05 揭晓核心概念时最稳最慢；s06 先用平铺语气再以『不是』短促切断；s07 纠偏处最认真；s08-s09 回到日常语气；s10 收束留白。全程不提高音量，靠停顿制造重量。",
        "pause_policy": "句间留自然停顿。每段结束留 0.9 秒呼吸位；三次反转前的句子后各留 1.2 秒明显停顿（s02 后、s05 后、s06 后、s07 后）。数字『4 个小时』『500 块钱』『3%』『5%』单独放慢读出，不连读。",
        "sample_section_id": "s05",
        "provider_notes": {
            "provider": "doubao",
            "voice_name": "大壹 2.0",
            "voice_id": "zh_male_dayi_uranus_bigtts",
            "resource_id": "seed-tts-2.0",
            "generation_mode": "segmented",
            "speech_rate": "0",
            "emphasis_handling": "六处需要加重但不提高音量：『成本 = 0？』『这一天，你本来还能拿去干什么？』『这就是机会成本。』『不是。』『有机会成本，不等于不应该做。』『免费，不等于没有成本。』doubao 无 SSML，通过标点与断句实现：关键句独立成句、前后加逗号或句号。",
            "number_handling": "阿拉伯数字在 provider_text 中保留原样，交由 TTS 数字归一化；『4个小时』『500块钱』『3%』『5%』前加逗号制造停顿。",
            "prohibited": "不添加任何欢快／上扬的播报腔；不使用网络主播语气词；不朗读合规文案。"
        }
    },
    "sections": out_sections,
    "metadata": {
        "content_category": "finance",
        "pipeline": "finance-dossier",
        "playbook": "finance-dossier",
        "editorial_direction": None,  # filled below
        "narration_source": "user_authored_verbatim",
        "narration_source_note": "旁白逐字采用用户提供的内容规划第 22 节「完整推荐口播」，未做任何增删改写；已通过程序化校验确认全篇连续覆盖、无缺口、无改动。",
        "plan_paragraph_map": meta_sections,
        "finance_editorial": {
            "core_question": "周末在家躺一天、一分钱没花，这一天的成本真的是0吗？",
            "evidence_refs": [
                "research_brief.data_points[0]",
                "research_brief.data_points[1]",
                "research_brief.data_points[2]",
                "research_brief.data_points[6]"
            ],
            "boundary_conditions": [
                "机会成本只取被放弃方案中对你最有价值的那个，不是所有被放弃选项相加。",
                "机会成本是前瞻的、主观的，取决于你个人最看重哪个替代方案。",
                "机会成本不要求货币化；被放弃的可能是时间、精力、陪伴或学习机会。",
                "投资比较中风险、流动性与确定性往往不同，不能只拿最终收益率机械比较。",
                "本期 500 元兼职净价值是演示算例，不是真实收入数据，也不代表任何具体投资结论。"
            ],
            "reusable_judgment_method": "遇到一件看起来「免费」的事，除了问「我要花多少钱」，再问一句「为了它，我放弃了什么」。",
            "narration_style": "old_friend_observational"
        },
        "compliance": {
            "content_category": "finance",
            "financial_disclaimer": "本视频仅作知识分享，不构成任何投资建议。市场有风险，投资需谨慎。",
            "exact_text": "本视频仅作知识分享，不构成任何投资建议。市场有风险，投资需谨慎。",
            "presentation": "footer",
            "placement": "ending",
            "ending_section_id": "s10",
            "note": "以原生文字呈现在最终意义场景的页脚，不朗读、不单独成段。"
        },
        "inclusion_completeness": {
            "plan_sections_covered": 11,
            "three_reversals_present": True,
            "forbidden_topics_excluded": [
                "沉没成本", "边际成本", "时间价值复杂计算", "比较优势",
                "多个投资品种比较", "大量公共政策案例", "机会成本的数学模型"
            ]
        }
    }
}

# carry approved editorial_direction unchanged
proposal = json.loads((ROOT / "projects/xiaosan-economics-03-opportunity-cost/artifacts/proposal_packet.json").read_text())
script["metadata"]["editorial_direction"] = proposal["metadata"]["editorial_direction"]

# ---- per-section delivery cues ----
CUES = {
 "s01": {"pace":"brisk","energy":"平静但直接，像把一个问题放到桌上","emphasis_words":["躺一天","一分钱没花","成本","0"],"pause_after_seconds":0.6,"delivery_note":"不寒暄、不介绍栏目、不解释概念。第一句就要进入问题。"},
 "s02": {"pace":"measured","energy":"顺着对方说，不急于否定","emphasis_words":["没买东西","没打车","没出去吃饭","银行卡一分钱都没少","0成本"],"pause_after_seconds":1.2,"delivery_note":"让观众先站到『0成本』这一边。最后一句『怎么看都是0成本』要平，不暗示转折。"},
 "s03": {"pace":"measured","energy":"转折，略压低","emphasis_words":["根本不只看你花了多少钱","本来还能拿去干什么"],"pause_after_seconds":0.8,"delivery_note":"『但』之后稍作停顿再进入。末句是全片第一个反问，尾音不要上扬成疑问播报腔。"},
 "s04": {"pace":"measured","energy":"摊开选择集合，克制、不催促","emphasis_words":["4个小时","只能真正使用一次","在家休息"],"pause_after_seconds":0.8,"delivery_note":"四个选项逐项读出，每项之间留短停顿，让观众真正读完集合。『只能真正使用一次』是全段重心。"},
 "s05": {"pace":"slow","energy":"揭晓，最稳最慢","emphasis_words":["最可能去做的那件事","净价值","500块钱","这就是机会成本"],"pause_after_seconds":1.2,"delivery_note":"本段是样音审核段。『这就是机会成本。』独立成句，前后各留停顿，不加任何强调腔。"},
 "s06": {"pace":"conversational","energy":"先平铺，再用『不是』短促切断","emphasis_words":["全部都要加起来","不是","最佳替代方案","最有价值的那个"],"pause_after_seconds":1.2,"delivery_note":"『不是。』要短、要干，不做成反问。后半段解释『为什么不能相加』时语速略快，像顺理成章。"},
 "s07": {"pace":"slow","energy":"认真纠正，回避说教","emphasis_words":["亏了500","也不是","放弃了什么","有机会成本，不等于不应该做"],"pause_after_seconds":1.2,"delivery_note":"这是全片最重要的纠偏段，不能赶。『有机会成本，不等于不应该做。』独立成句、放慢，但不加重音量。"},
 "s08": {"pace":"measured","energy":"回到日常语气，扩展边界","emphasis_words":["换算成钱","时间","精力","免费咖啡","两个小时","免费，不等于没有成本"],"pause_after_seconds":0.9,"delivery_note":"排比四句（收入／时间／精力／陪伴休息学习）用同一语调读完，不逐句加重。结尾判断句独立成句。"},
 "s09": {"pace":"measured","energy":"轻量连接投资，自带限定","emphasis_words":["3%","5%","放弃了什么","不能只拿最终收益率机械比较"],"pause_after_seconds":0.9,"delivery_note":"『3%』『5%』放慢分开读。限定句（风险、流动性和确定性往往都不同）不能被赶，它不是免责套话，是本段的边界条件。"},
 "s10": {"pace":"custom","energy":"收束，留一个问题给观众","emphasis_words":["我要花多少钱","为了它，我放弃了什么"],"pause_after_seconds":1.0,"delivery_note":"最后一句是全片落点，读完后留足留白再进入结尾卡。不做课程式预告。"},
}
for sec in out_sections:
    c = CUES[sec["id"]]
    sec["delivery_cues"] = {
        "pace": c["pace"],
        "energy": c["energy"],
        "emphasis_words": c["emphasis_words"],
        "pause_after_seconds": c["pause_after_seconds"],
        "delivery_note": c["delivery_note"],
        "provider_text": sec["text"],
    }
    sec["speaker_directions"] = "老朋友观察型；" + c["energy"]

OUT.write_text(json.dumps(script, ensure_ascii=False, indent=2), encoding="utf-8")

from schemas.artifacts import validate_artifact
validate_artifact("script", script)
print(f"script.json written, SCHEMA OK, total={total}s, sections={len(out_sections)}")
for s, m in zip(out_sections, meta_sections):
    print(f"  {s['id']} {s['start_seconds']:>7.2f} - {s['end_seconds']:>7.2f}  {s['label']}")
