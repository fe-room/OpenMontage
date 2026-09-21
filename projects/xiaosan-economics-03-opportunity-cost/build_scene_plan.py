#!/usr/bin/env python3
"""Build scene_plan.json for xiaosan-economics-03-opportunity-cost."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
ART = ROOT / "projects/xiaosan-economics-03-opportunity-cost/artifacts"

script = json.loads((ART / "script.json").read_text())
proposal = json.loads((ART / "proposal_packet.json").read_text())
sec = {s["id"]: (s["start_seconds"], s["end_seconds"]) for s in script["sections"]}
S = lambda k: sec[k]
TOTAL = script["total_duration_seconds"]

# The RAW table below is authored against the original 224.01s design timeline.
# Scenes are stored as FRACTIONS of their script section so that rebuilding the
# timeline from real TTS durations never misplaces a scene boundary.
ORIG = {
 "s01": (0.00, 5.50), "s02": (5.50, 16.43), "s03": (16.43, 26.31),
 "s04": (26.31, 45.39), "s05": (45.39, 72.41), "s06": (72.41, 103.40),
 "s07": (103.40, 148.60), "s08": (148.60, 180.42), "s09": (180.42, 214.54),
 "s10": (214.54, 224.01),
}

TAIL_HOLD = 3.0  # seconds of hold after the last spoken word for the ending card
ANCHORS = {
 "fed": {"label":"Federal Reserve Bank of St. Louis — Real-Life Examples of Opportunity Cost","url":"https://www.stlouisfed.org/open-vault/2020/january/real-life-examples-opportunity-cost","date":"2020-01","tier":1},
 "fed2": {"label":"Federal Reserve Bank of St. Louis — 显性成本与隐性成本区分（Money and Missed Opportunities 延伸）","url":"https://www.stlouisfed.org/open-vault/2020/january/real-life-examples-opportunity-cost","date":"2020-01","tier":1},
 "wiki": {"label":"Opportunity cost — 微观经济学基础条目（互斥备选前提；机会成本不限于货币成本）","url":"https://simple.wikipedia.com/wiki/Opportunity_cost","tier":2},
 "mankiw": {"label":"N. Gregory Mankiw《Principles of Microeconomics》Ch.1（经 CSUN 教学讲义引述）","url":"https://www.csun.edu/sites/default/files/micro1.pdf","tier":1},
 "econlearn": {"label":"EconLearn — Opportunity Cost Explained（教学算例：机会成本只取次优方案，非全部相加）","url":"https://www.econlearn.org/blog/opportunity-cost-explained","tier":3},
 "ucsb": {"label":"UC Santa Barbara — Opportunity Costs: The Hidden Price of Every Decision（分析工具而非货币化公式）","url":"https://efp.ucsb.edu/think-economist/opportunity-costs-hidden-price-every-decision","tier":2},
 "fiveable": {"label":"Fiveable — 1.1 Scarcity, choice, and opportunity cost（投资比较算例及风险差异限定）","url":"https://frontend.prod.fiveable.me/key-terms/intermediate-microeconomic-theory/allocation-of-resources","tier":3},
 "econlearn_gloss": {"label":"EconLearn 术语表 — 机会成本不总是以金钱衡量","url":"https://www.econlearn.org/glossary/opportunity-cost","tier":3},
 "takeaway": {"label":"本期可复用判断动作（收束自 research_brief.data_points[0] 的机会成本定义）","tier":2},
}

DISC = "本视频仅作知识分享，不构成任何投资建议。市场有风险，投资需谨慎。"

# (id, script_section, type, start, end, role, family, ftype, claim, anchor, importance, layout, desc, intent, transition_in, assets)
RAW = [
 ("sc01","s01","broll",0.00,3.20,"开场：把提问落到观众自己的周六","",None,"SCENARIO",None,"medium","full-bleed-real",
  "真实生活素材：周末在家躺卧／沙发／手机，画面右上角压一行叠字「周末在家躺一天」（原生排版，不是素材里的字）。",
  "在2秒内让观众认出这是自己刚刚度过的周末，把抽象提问变成已经历过的处境。","冷开场，无转场铺垫",
  [("broll","周末在家躺卧的真实生活素材（沙发/床/手机/周末氛围）","source")]),
 ("sc02","s01","text_card",3.20,5.50,"开场：把冲突压成一行","",None,"SCENARIO",None,"high","hero",
  "两屏极速切换：先出「一分钱没花」，紧接着放大到全屏大字「成本 = 0？」。第二屏的字重明显大于第一屏。",
  "35 秒内不解释任何概念，只把冲突摆上桌。","硬切",
  [("overlay","两屏原生大字叠字：一分钱没花 / 成本 = 0？","generate")]),
 ("sc03","s02","animation",5.50,16.43,"强化直觉：让观众先站到0成本这一边","DATA",None,"SCENARIO",None,"medium","paper-ledger",
  "纸张质感的极简支出清单，四行逐行落下：「没买东西」「没打车」「没出去吃饭」「银行卡一分钱都没少」，每行右侧都是 0 元。四行齐了之后，整张清单下方压出结论「怎么看都是0成本」。",
  "顺着观众的直觉走，不给任何转折提示，为第一次反转蓄势。","清单从空开始，逐行补全",
  [("animation","原生排版的0支出清单与逐行落字动效","generate")]),
 ("sc04","s03","text_card",16.43,21.40,"第一次反转：经济学为什么不只看花了多少钱","",None,"FACT",
  "fed2","high","headline-annotation",
  "「但经济学算成本，根本不只看你花了多少钱」——「花了多少钱」四字被一道朱红横线划掉，划掉的动作跟随朗读节奏完成。",
  "第一次认知反转的落点。用划掉这个动作代替任何解释性文字。","朱红横线从左侧进入",
  [("animation","朱红批注划删动效","generate")]),
 ("sc05","s03","diagram",21.40,26.31,"第一次反转：把追问摆出来","MECHANISM",None,"FACT",
  "wiki","high","question-diagram",
  "一个问题占满画面：「这一天，你本来还能拿去干什么？」问号下方伸出四条极细的深青短线，指向画面下方四个尚未填写的空白纸位——预告下一场的选择集合。",
  "把'机会成本'的第一层含义压缩成一个观众必须自己回答的问题。","承上，四条线引出下一场",
  [("diagram","原生问句排版 + 深青引导线","generate")]),
 ("sc06","s04","text_card",26.31,31.50,"核心场景：建立约束","",None,"SCENARIO",None,"high","hero",
  "画面中央一行：「周六下午：4 小时」。上方留大量空白，下方什么都没有——先把约束立住，再给选项。",
  "让'4 小时'这个有限资源成为整期的度量单位。","从上一场的引导线收拢到这一行",
  [("overlay","原生大字：周六下午：4 小时","generate")]),
 ("sc07","s04","animation",31.50,38.60,"核心场景：建立选择集合","MECHANISM",None,"SCENARIO",None,"high","option-cards",
  "四张等权纸卡依次落到画面：A 在家休息 / B 拍一期视频 / C 接一个兼职 / D 去健身。每张卡落下时有轻微旋转与投影，形成纸张厚度。四个选项读完后不停留。",
  "把'你本来还能拿去干什么'具体化为四个互斥选项。","第一张卡从上方落下，其余依次跟随",
  [("animation","四张选项纸卡的原生让位与落纸动效","generate")]),
 ("sc08","s04","animation",38.60,45.39,"核心场景：互斥约束与选中","MECHANISM",None,"SCENARIO",None,"high","option-cards-constraint",
  "一条朱红横线划过四张卡：「这 4 个小时，你只能真正使用一次」。随后 A 卡被抬起加厚，B/C/D 转为暗态但轮廓仍可读。画面右下角压出「支出：0 元」。",
  "先把互斥性钉死（这是后面'不能相加'的伏笔），再完成选择。","朱红线一次性划过四张卡",
  [("broll","短促的真实时间流逝素材，用于让'4小时正在过去'可被体感","source"),
   ("animation","朱红约束线 + A卡抬起 + B/C/D 暗态","generate")]),
 ("sc09","s05","text_card",45.39,53.20,"核心揭晓：把追问再推进一层","",None,"FACT",
  "wiki","high","question-headline",
  "「如果你没有选择休息，你最可能去做的那件事是什么？」逐字打出，打出速度比朗读略慢，制造'认真想一想'的感觉。",
  "让观众自己产出答案，再由画面命名它——这比直接给定义更不容易被划走。","黑场极短，然后逐字打出",
  [("overlay","原生逐字打出排版","generate")]),
 ("sc10","s05","animation",53.20,65.00,"核心揭晓：命名机会成本","MECHANISM","causal_chain","FACT",
  "fed","high","highlight-reveal",
  "B/C/D 全部暗下，只有 C（接一个兼职）重新点亮并放大，卡面浮出「最佳被放弃方案」，下方接一行「净价值约 500 元」。最后一屏放大到「机会成本」。",
  "精确呈现定义：不是所有选项，而是被你放弃的那个最佳替代方案。","暗场一次，再逐个点亮，只留一张",
  [("animation","选项卡变暗/重新高亮的确定性状态动效","generate")]),
 ("sc11","s05","text_card",65.00,72.41,"核心概念：定义卡单独停留一屏","DOCUMENT","document","FACT",
  "fed","high","definition-card",
  "整屏定义卡：「机会成本 ≠ 你花出去的钱」「机会成本 = 为了当前选择而放弃的最佳替代方案的价值」。卡片下方以小字给出引用来源。整屏静止 1.2 秒后离开。",
  "定义需要被读到，而不是被听到。这是全片唯一一次让画面完全静止。","从上一场的放大态推入，静止",
  [("overlay","原生定义卡排版 + 来源小字","generate")]),
 ("sc12","s06","text_card",72.41,84.37,"第二次反转：先立问题再否定","",None,"FACT",
  "econlearn","high","hero-negation",
  "先打出「那这些是不是全部都要加起来？」，停半拍，整屏翻成一个大字「不是。」「不是」二字用干燥的字重，不带任何装饰。",
  "先让观众自己产生'求和'的直觉，再用一个最短的否定切断它。","从上一屏静止直接翻页",
  [("overlay","原生大字翻页：不是。","generate")]),
 ("sc13","s06","animation",84.37,103.40,"第二次反转：拆解为什么不能相加","MECHANISM","causal_chain","FACT",
  "econlearn","high","extinguish-arithmetic",
  "朱红算式「B + C + D = 机会成本」被逐字划掉。同时 B/C/D 三张卡逐个熄灭（不是消失，是失去对比度并下沉）。最后重新浮现一句话：「你放弃掉的最佳替代方案」。",
  "用'熄灭'和'划掉的加号'两个动作完成一次纯视觉的否定，不依赖口播。","算式先出现，再被划掉",
  [("animation","逐个熄灭 + 算式朱红划删动效","generate")]),
 ("sc14","s07","text_card",103.40,117.34,"第三次反转：提出误会再否定","",None,"INFERENCE",
  "ucsb","high","misread-card",
  "先浮现观众的误会：「躺这 4 个小时就'亏了500'？」（整句套在虚线框里，表示这是待纠正的说法）。随后翻出「也不是。」",
  "第三次反转必须先立起误会，否则纠偏没有对象。虚线框承担'这是误读'的信号。","从上一场的熄灭态起",
  [("overlay","原生虚线框误会卡 + 翻页","generate")]),
 ("sc15","s07","diagram",117.34,134.00,"第三次反转：机会成本不替你判断","MECHANISM",None,"INFERENCE",
  "ucsb","high","balance-diagram",
  "一条水平基准线，左端压「休息4小时的恢复」，右端压「兼职净价值约500元」，两端之间不给出胜负——线上方标注「机会成本只回答：你放弃了什么」。线下方另起一行「它不替你决定：这个选择对不对」。",
  "把'机会成本是分析工具，不是价值判断'做成一个可见的结构，而不是一句口号。","静态基准线先出现，两端再压上纸片",
  [("diagram","原生基准线与纸片比较（不给胜负结论）","generate")]),
 ("sc16","s07","text_card",134.00,148.60,"第三次反转：纠偏落点","DECISION","thesis_breaker","INFERENCE",
  "ucsb","critical","annotation-card",
  "朱红批注式大字：「有机会成本，不等于不应该做。」停留一拍。随后四行小字快速并列落下：睡觉 / 陪家人 / 学习 / 工作——每行后面都跟着同一个词「有机会成本」。",
  "全片最重要的一次纠偏，防止观众把机会成本读成'休息就是浪费'。","从上一场的基准线收拢",
  [("overlay","原生朱红批注卡 + 四行并列小字","generate")]),
 ("sc17","s08","animation",148.60,165.00,"补充认知：成本不必货币化","DATA",None,"FACT",
  "wiki","high","strike-the-equals",
  "画面中一个朱红等号被划掉。随后四类被放弃项以纸片形式依次落下：收入 / 时间 / 精力 / 陪伴·休息·一次学习机会。每类纸片的形状不同，但都没有价格标签。",
  "明确否掉'所有东西都必须换算成钱'，这是机会成本最容易被误用的地方。","等号先被划掉，再落下四类纸片",
  [("animation","等号划删 + 四类无价签纸片落纸","generate")]),
 ("sc18","s08","broll",165.00,180.42,"补充认知：免费不等于没有成本","DATA",None,"FACT",
  "fed2","high","full-bleed-real",
  "真实排队素材：一条缓慢移动的队伍。画面上半部压「咖啡 0 元」，下半部压「那两个小时，不是免费的」。最后一行结论「免费，不等于没有成本」。",
  "用一个具体、极短的案例把'免费'和'没有成本'分开，避免抽象说教。","从纸面切到真实画面，形成一次材质对照",
  [("broll","商场/门店前缓慢排队两小时的真实素材","source"),
   ("overlay","原生对比文字：咖啡 0 元 / 那两个小时不是免费的","generate")]),
 ("sc19","s09","diagram",180.42,192.00,"投资连接：确定性收益率比较","DATA","chart","FACT",
  "fiveable","high","comparison-chart",
  "两个并排的确定性柱形：A 3% / B 5%。柱形上方明确标注前提「风险、流动性与其他限制相当」。两柱之间用一个问号括号连起来，标注「为了选 A，你放弃了什么？」。",
  "把机会成本接到投资上，但把前提写在图上而不是藏在口播里。","从真实画面回到纸面",
  [("diagram","原生确定性柱形比较图 + 前提标注","generate")]),
 ("sc20","s09","text_card",192.00,205.00,"投资连接：边界条件不能被赶","",None,"FACT",
  "fiveable","high","boundary-card",
  "三条边界条件逐行落下：「风险不同」「流动性不同」「确定性不同」，随后一行结论「所以不能只拿最终收益率机械比较」。这一屏刻意不放慢，但字距略宽以便读完。",
  "限定条件必须与结论同屏，不能被快节奏带过——否则这句比较就变成了投资建议。","柱形图淡出，转入条款式排版",
  [("overlay","原生边界条件条款排版","generate")]),
 ("sc21","s09","animation",205.00,214.54,"投资连接：把判断动作补全","DECISION",None,"THESIS",
  "fiveable","high","completion-reveal",
  "「判断一个选择，不能只看它给了你什么」——这一行先出现，其下方留空。紧接着「为了它，你放弃了什么」从右侧补进空白处，两行合成一个完整的判断动作。",
  "把'关注收益'补全为'同时关注放弃'，为结尾的追问做铺垫。","从边界条件收进一个完整句",
  [("animation","原生两行补全动效","generate")]),
 ("sc22","s10","text_card",214.54,224.01,"收束：留下一个现实思考","DECISION","watch_list","THESIS",
  "takeaway","critical","closing-card",
  "先出「我要花多少钱？」（灰），其下方补出「为了它，我放弃了什么？」（石墨重字）。画面底部小字角标「小散经济学 03｜机会成本」。最底部以原生小字固定呈现合规文案：「本视频仅作知识分享，不构成任何投资建议。市场有风险，投资需谨慎。」",
  "只留一个可复用的判断动作，不做课程式预告。合规文案必须原生、完整、可读，并留在成片最末端。","从补全句直接收到这一屏，不放任何转场花活",
  [("overlay","原生结尾追问卡 + 系列角标 + 合规 footer","generate")]),
]

scenes = []
FRACS = {}
for (sid, ssec, stype, st, en, role, fam, ftype, claim, anchor, imp, layout, desc, intent, tin, assets) in RAW:
    o0, o1 = ORIG[ssec]
    n0, n1 = sec[ssec]
    f0 = (st - o0) / (o1 - o0)
    f1 = (en - o0) / (o1 - o0)
    st = round(n0 + f0 * (n1 - n0), 3)
    en = round(n0 + f1 * (n1 - n0), 3)
    s = {
        "id": sid,
        "type": stype,
        "description": desc,
        "start_seconds": st,
        "end_seconds": en,
        "script_section_id": ssec,
        "information_role": role,
        "shot_intent": intent,
        "transition_in": tin,
        "framing": "1080x1920 竖屏；关键文字与数字全部落在社交安全区内（距底 520px、距侧 96px）",
        "movement": "见 description 中的动效说明；纹理固定 seed，不逐帧随机",
        "overlay_notes": "不铺设整段口播字幕；只保留分层短句大字与关键词强调",
        "required_assets": [{"type": a[0], "description": a[1], "source": a[2]} for a in assets],
    }
    FRACS[sid] = [round(f0, 4), round(f1, 4)]
    if fam:
        s["finance_family"] = fam
    if ftype:
        s["finance_scene_type"] = ftype
    if claim:
        s["claim_class"] = claim
    if anchor:
        s["source_anchor"] = ANCHORS[anchor]
        s["mechanism_importance"] = (fam == "MECHANISM")
        s["layout_variant"] = layout
        s["finance_justification"] = intent
    if sid in ("sc10", "sc16"):
        s["hero_moment"] = True
    scenes.append(s)

# Frame 0 is already the opening visual (lead-in silence belongs to sc01), and a
# section-boundary pause is a deliberate hold: the previous scene keeps its final
# state on screen through the breath. Absorbing the pause into the preceding scene
# is what makes the timeline continuous with no gaps.
scenes[0]["start_seconds"] = 0.0
for a, b in zip(scenes, scenes[1:]):
    if b["start_seconds"] > a["end_seconds"] + 1e-9:
        a["end_seconds"] = b["start_seconds"]

# continuity check
prev_end = 0.0
for s in scenes:
    assert abs(s["start_seconds"] - prev_end) < 1e-6, f"gap/overlap at {s['id']}: {s['start_seconds']} vs {prev_end}"
    prev_end = s["end_seconds"]
# sc22 absorbs the trailing hold so the closing card + compliance footer can be read
scenes[-1]["end_seconds"] = round(TOTAL + TAIL_HOLD, 3)
prev_end = scenes[-1]["end_seconds"]
assert prev_end >= TOTAL, f"timeline ends at {prev_end}, script ends at {TOTAL}"
assert scenes[-1]["id"] == "sc22"

fams = sorted({s["finance_family"] for s in scenes if s.get("finance_family")})
types = sorted({s["type"] for s in scenes})
runs, cur = 1, 1
for a, b in zip(scenes, scenes[1:]):
    cur = cur + 1 if a["type"] == b["type"] else 1
    runs = max(runs, cur)
assert runs < 3, f"3+ consecutive same scene type (run={runs})"

plan = {
    "version": "1.0",
    "style_playbook": "finance-dossier",
    "scenes": scenes,
    "metadata": {
        "content_category": "finance",
        "editorial_direction": proposal["metadata"]["editorial_direction"],
        "art_direction": proposal["production_plan"]["art_direction"],
        "composition_mode": "atelier",
        "render_runtime": "remotion",
        "canvas": {"width": 1080, "height": 1920, "fps": 30},
        "subtitle_safe_area": {"bottom_px": 520, "side_px": 96, "policy": "social-ui-safe"},
        "rhythm": ["快(sc01-sc02)", "慢(sc03)", "快(sc04)", "停(sc05)", "慢(sc06-sc08)",
                   "停(sc09-sc11)", "快(sc12-sc13)", "慢(sc14-sc16)", "慢(sc17-sc18)",
                   "慢(sc19-sc21)", "收(sc22)"],
        "scene_count_rationale": "22 个场景，每个边界对应一次认知任务的实质变化（提问→直觉→反转→选择集合→定义→否定求和→纠偏→边界→投资→收束）。EXPLAIN 模式不强制组件清单，也未为凑数量而拆场。",
        "finance_family_mix": fams,
        "scene_type_mix": types,
        "max_consecutive_same_type": runs,
        "semantic_motion_usage": [
            {"scene": "sc01", "why": "开场躺卧：让抽象提问变成观众已经历过的具体处境，直接服务2秒留存"},
            {"scene": "sc08", "why": "4小时流逝：把'只能使用一次'从一句话变成可感知的紧迫性，支撑互斥前提"},
            {"scene": "sc18", "why": "排队两小时：为'免费≠没有成本'提供具身证据，比纯卡片更有说服力"}
        ],
        "source_verification": "所有数字（4小时、500元、3%、5%、0元）均为演示算例或原生图表数值，逐帧由确定性图层渲染；素材镜头不承载任何需要被读准的事实。",
        "trailing_hold_seconds": TAIL_HOLD,
        "scene_section_fractions": FRACS,
        "scene_timing_basis": "每个场景以所属脚本段落内的比例定位，再映射到实测配音时长；重建时间轴不会移动场景边界。",
        "compliance": {
            "content_category": "finance",
            "financial_disclaimer": DISC,
            "exact_text": DISC,
            "presentation": "footer",
            "placement": "ending",
            "ending_scene_id": "sc22",
            "note": "合规文案以原生小字固定呈现在最终意义场景 sc22 的页脚，不朗读、不单独成场。"
        }
    }
}

(ART / "scene_plan.json").write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")

from schemas.artifacts import validate_artifact
validate_artifact("scene_plan", plan)
print(f"scene_plan.json SCHEMA OK | scenes={len(scenes)} | families={fams} | types={types} | max_run={runs} | total={prev_end}")
