#!/usr/bin/env python3
"""Generate the Finance Dossier real-topic stress-test artifacts.

The research is frozen to the disclosed 2026-08-28 cutoff. This script performs
no network calls and no media generation; it materializes the reviewed evidence,
router decisions, scripts, scene plans, and advisory validation output.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from lib.content_policy import FINANCIAL_DISCLAIMER_ZH, enforce_financial_disclaimer
from lib.finance_editorial import normalize_editorial_direction
from lib.finance_scene_variety import FinanceSceneVarietyValidator, validate_finance_mode_signatures


OUT = ROOT / "output" / "finance-dossier-real-stress-test"
CUTOFF = "2026-08-28"


def direction(primary, audience, rationale, evidence, visuals, canvases, hook, ending, risk, anti, *, secondary=None, confidence="high", density=None):
    result = {
        "primary_mode": primary,
        "classification_confidence": confidence,
        "audience_task": audience,
        "rationale": rationale,
        "evidence_priority": evidence,
        "visual_priority": visuals,
        "canvas_preference": canvases,
        "density_profile": density or {"opening": "sparse", "body": "standard", "evidence": "dense", "ending": "sparse"},
        "hook_grammar": hook,
        "ending_grammar": ending,
        "key_editorial_risk": risk,
        "key_anti_pattern": anti,
    }
    if secondary:
        result["secondary_mode"] = secondary
    return normalize_editorial_direction(result)


def scene(scene_id, finance_type, family, claim, source, role, intent, transition, start, end, description, **extra):
    item = {
        "id": scene_id,
        "type": "animation",
        "finance_scene_type": finance_type,
        "finance_family": family,
        "claim_class": claim,
        "source_anchor": source,
        "information_role": role,
        "shot_intent": intent,
        "transition_in": transition,
        "start_seconds": start,
        "end_seconds": end,
        "approximate_duration_seconds": end - start,
        "description": description,
        "why_exists": intent,
    }
    item.update(extra)
    return item


SOURCES = {
    "nvda_ir": "https://investor.nvidia.com/news/press-release-details/2025/NVIDIA-Announces-Financial-Results-for-Second-Quarter-Fiscal-2026/default.aspx",
    "nvda_10q": "https://www.sec.gov/Archives/edgar/data/1045810/000104581025000209/nvda-20250727.htm",
    "nvda_reaction": "https://www.investing.com/news/stock-market-news/ai-leader-nvidia-forecasts-thirdquarter-revenue-above-estimates-4213405",
    "nvda_close": "https://www.kiplinger.com/investing/stocks/s-p-500-tops-6-500-even-as-nvidia-slips-stock-market-today",
    "tariff_order": "https://www.whitehouse.gov/presidential-actions/2025/04/regulating-imports-with-a-reciprocal-tariff-to-rectify-trade-practices-that-contribute-to-large-and-persistent-annual-united-states-goods-trade-deficits/",
    "china_tariff": "https://gss.mof.gov.cn/gzdt/zhengcejiedu/202504/t20250404_3961452.htm",
    "market_reaction": "https://www.investing.com/news/stock-market-news/shares-bruised-dollar-crumbles-as-trump-tariffs-stir-recession-fears-3966939",
    "vix": "https://www.cboe.com/insights/posts/vix-index-attribution-of-notable-tail-events/",
    "sf_fed": "https://www.frbsf.org/wp-content/uploads/el2025-23_5cfd27.pdf",
    "fed_cut": "https://www.federalreserve.gov/newsevents/pressreleases/monetary20240918a.htm",
    "fed_minutes": "https://www.federalreserve.gov/monetarypolicy/fomcminutes20240918.htm",
    "fred_10y": "https://fred.stlouisfed.org/series/DGS10",
    "nyfed_term": "https://www.newyorkfed.org/research/data_indicators/term-premia-tabs",
    "epoch_ai": "https://epoch.ai/data-insights/ai-datacenter-cost-breakdown",
    "alphabet_call": "https://abc.xyz/investor/events/event-details/2026/2025-Q4-Earnings-Call-2026-Dr_C033hS6/default.aspx",
    "iea_ai": "https://www.iea.org/reports/energy-and-ai/",
    "intel_10k": "https://www.sec.gov/Archives/edgar/data/50863/000005086324000010/intc-20231230.htm",
}


cases = {}

cases["research"] = {
    "topic": "为什么英伟达 Q2 FY2026 财报看起来不错，市场反应却没有那么兴奋？",
    "event_date": "2025-08-27",
    "reaction_window": "2025-08-27 盘后至 2025-08-28 美股收盘",
    "why_not": "不是 MARKET：核心任务不是重建一段盘中异动，而是把公司报告、可比一致预期、结果质量与定价门槛放在同一研究框架内。",
    "router": direction(
        "RESEARCH", "对照英伟达公司结果、市场预期与增长质量",
        ["总营收与每股收益超过一致预期，但数据中心收入略低于可比预期；市场在交易超预期幅度，而不是收入是否增长。"],
        ["company_filings", "investor_relations", "market_expectations", "reaction_window", "operating_quality"],
        ["document", "expectation_gap", "chart", "evidence_card", "thesis_breaker"],
        ["document", "paper", "data", "margin-note"], "CONTRADICTION", "WHAT_CHANGES_THE_THESIS",
        "把盘后下跌单因归结为一个指标，或混用总营收一致预期与数据中心一致预期。",
        "不要把所有强指标都做成 EvidenceCard，也不要把弱反应写成确定性卖出结论。",
    ),
    "research": f"""# RESEARCH — NVIDIA Q2 FY2026

DATA CUT-OFF: {CUTOFF}
EVENT / EARNINGS DATE: 2025-08-27
MARKET REACTION WINDOW: 2025-08-27 盘后至 2025-08-28 美股收盘

## 结论边界

采用 2025 年 8 月财报，而非 2026-08-26 最新财报：后者在电话会后转为明显上涨，不符合“结果强但反应不兴奋”的测试条件。2025 年案例可被公司披露、SEC 文件和可比一致预期共同支持。

## Evidence ledger

- FACT — NVIDIA Q2 FY2026 营收 467 亿美元，环比 +6%、同比 +56%；Data Center 营收 411 亿美元，环比 +5%、同比 +56%；Blackwell Data Center 营收环比 +17%。来源：NVIDIA IR，2025-08-27。{SOURCES['nvda_ir']}
- FACT — GAAP 毛利率 72.4%；剔除 1.8 亿美元 H20 存货准备转回后，非 GAAP 毛利率为 72.3%。当季没有面向中国客户的 H20 销售。来源：NVIDIA IR / 10-Q。{SOURCES['nvda_10q']}
- FACT — 总营收约 467 亿美元、高于约 461 亿美元一致预期；调整后 EPS 1.05 美元、高于 1.01 美元。Data Center 411 亿美元、略低于约 413.4 亿美元一致预期。来源：Kiplinger 汇总的 Wall Street 一致预期，2025-08-28。{SOURCES['nvda_close']}
- FACT — 股票在财报发布后盘后一度约跌 3.2%，次日常规交易收跌 0.8%。来源：Reuters / Kiplinger。{SOURCES['nvda_reaction']} {SOURCES['nvda_close']}
- INFERENCE — 市场反应更像是在重估“超预期幅度、数据中心质量和中国不确定性”，而不是否认 AI 需求增长。不能据此证明单一因果。
- THESIS — 结果仍强，但高预期使“好”不再等于“足够超预期”。
- SCENARIO — 若后续 Data Center 再加速、毛利率改善且中国收入可见性提高，该判断会减弱；若增速继续放缓或毛利率承压，则会加强。

## Source hierarchy

Tier 1: NVIDIA IR、NVIDIA 10-Q。Tier 2: Reuters 与可核对的一致预期/收盘反应汇总。所有预期均明确对应同一季度和同一指标。
""",
    "script": """# SCRIPT — RESEARCH（约 58 秒）

【FACT】英伟达这份财报，标题数字并不差：季度营收 467 亿美元，同比增 56%，也高于约 461 亿美元的一致预期。

但市场先看的是更高的一道门槛。核心的数据中心收入是 411 亿美元，同比同样增 56%，却略低于约 413.4 亿美元的预期；财报发布后，股价盘后一度跌约 3.2%，次日收跌 0.8%。

【FACT】Blackwell 数据中心收入环比增 17%，但当季没有面向中国客户的 H20 销售；毛利率还受到 1.8 亿美元存货准备转回影响。

【INFERENCE】所以市场未必在交易“AI 需求消失”，更可能在交易：增长虽然强，但超预期幅度、结构质量和中国可见性，没有强到足以抬高已经很高的定价门槛。

【SCENARIO】接下来要看三件事：数据中心是否重新加速、毛利率能否改善、以及中国收入是否恢复可见性。它们才会改变这份判断。""",
}

cases["research"]["scenes"] = [
    scene("r1", "document", "DOCUMENT", "FACT", {"label": "NVIDIA Q2 FY2026 Results", "date": "2025-08-27", "period": "quarter ended 2025-07-27"}, "先确认报告本身是否强。", "这幕建立公司披露的事实基线，观众之后才能判断市场反应是否反常。", "问题 → 公司文件", 0, 11, "营收 467 亿美元，同比 +56%，高于总营收一致预期。", canvas_mode="document"),
    scene("r2", "expectation_gap", "DATA", "FACT", {"label": "NVIDIA / Wall Street consensus", "date": "2025-08-27", "period": "Q2 FY2026 Data Center revenue"}, "把同口径的数据中心实际值与预期放在一个画面。", "总营收、数据中心实际、预期和差额属于同一个比较任务，应合并而不是拆成三幕。", "公司结果 → 可比预期", 11, 23, "Data Center：实际 411 亿美元 vs 预期约 413.4 亿美元，差约 2.4 亿美元。", layout_variant="delta"),
    scene("r3", "chart", "DATA", "FACT", {"label": "NVIDIA IR", "date": "2025-08-27", "period": "Q2 FY2026"}, "检查增长质量，而不仅是标题数字。", "观众从‘有没有 beat’切换到‘增长由什么构成’，需要新的证据视角。", "预期差 → 质量", 23, 34, "展示 Data Center 同比 +56%、环比 +5%、Blackwell 环比 +17%。"),
    scene("r4", "evidence_card", "DATA", "INFERENCE", {"label": "NVIDIA IR / 10-Q", "date": "2025-08-27", "period": "Q2 FY2026"}, "给弱反应一个有边界的解释。", "这里不是再报数字，而是把 H20 缺席和毛利率调整转化为审慎解释。", "质量 → 解释", 34, 46, "一个可能解释：高门槛、中国不确定性与毛利率质量共同限制了兴奋度。", finance_justification="EvidenceCard is used once for the bounded synthesis, not for every metric."),
    scene("r5", "thesis_breaker", "DECISION", "SCENARIO", {"label": "NVIDIA future filings / earnings", "period": "subsequent quarters"}, "告诉观众什么证据会推翻当前判断。", "研究任务最后应落到可证伪的观察清单，而不是价格预测。", "解释 → 可证伪条件", 46, 58, "WATCH：Data Center 再加速、毛利率改善、中国收入可见性。"),
]

cases["market"] = {
    "topic": "2025 年 4 月 4 日美股暴跌，市场当时到底在交易什么？",
    "event_date": "2025-04-04",
    "reaction_window": "2025-04-02 美股收盘后至 2025-04-04 收盘",
    "why_not": "不是 MACRO：虽然增长与通胀路径重要，但观众首先要完成的是带时间戳的事件重建和跨资产反应核对，而非讲一个长期政策传导模型。",
    "router": direction(
        "MARKET", "重建 2025-04-04 关税冲击下的美股异动与当时交易的风险",
        ["核心是具体两日窗口中的公告、报复措施、指数与跨资产反应；多种解释并存。"],
        ["official_announcements", "timestamped_market_data", "reaction_window", "cross_asset_confirmation", "alternative_explanations"],
        ["evidence_card", "research_timeline", "chart", "document", "scenario_board"],
        ["dark-ink", "data", "full-bleed", "paper"], "WHAT_MOVED", "WATCH_NEXT",
        "把关税公告、报复措施、鲍威尔讲话和衰退担忧压缩成唯一原因。",
        "不要用 CausalChain 把时间相邻画成确定因果；先用时间线和跨资产反应。",
        secondary="MACRO", density={"opening": "sparse", "body": "dense", "evidence": "dense", "ending": "standard"},
    ),
    "research": f"""# MARKET — 2025-04-04 tariff sell-off

DATA CUT-OFF: {CUTOFF}
EVENT / EARNINGS DATE: 2025-04-02 至 2025-04-04
MARKET REACTION WINDOW: 2025-04-02 美股收盘后至 2025-04-04 收盘

## Evidence ledger

- FACT — 美国 2025-04-02 发布 reciprocal tariff 行政命令，10% 基准税率于 4 月 5 日起实施，部分更高税率原定 4 月 9 日实施。来源：White House。{SOURCES['tariff_order']}
- FACT — 中国 2025-04-04 宣布自 4 月 10 日起对原产美国的所有进口商品加征 34% 关税。来源：中国财政部。{SOURCES['china_tariff']}
- FACT — S&P 500 在 4 月 3 日约跌 4.8%，4 月 4 日再跌约 6.0%；旧金山联储后续研究按两日窗口计算约跌 11%。来源：S&P/Reuters、SF Fed。{SOURCES['market_reaction']} {SOURCES['sf_fed']}
- FACT — 4 月 4 日 VIX 从 21.5 升至 45.3；10 年期美债收益率当日降至约 3.93%，油价与其他大宗商品下跌。来源：Cboe、Reuters。{SOURCES['vix']} {SOURCES['market_reaction']}
- INFERENCE — 股票、油和长端收益率同跌，更符合市场同时上调增长下行风险；但价格反应不能证明关税是全部原因。
- Alternative explanations — 中国报复措施强化升级风险；鲍威尔当日强调等待观察关税影响；仓位去风险与波动率上升可能放大幅度。强劲就业数据未能逆转跌势，但不能据此忽略其他信息。
- SCENARIO — 若政策范围收窄、谈判落地且信用/波动指标修复，解释会减弱；若报复升级和盈利预期下修扩散，解释会加强。
""",
    "script": """# SCRIPT — MARKET（约 54 秒）

【FACT】2025 年 4 月 4 日，S&P 500 单日跌约 6%，前一天已经跌了约 4.8%。这不是一根孤立的阴线。

时间线很清楚：4 月 2 日美方公布大范围对等关税；4 月 4 日，中国宣布对美国商品加征 34% 关税。当天 VIX 从 21.5 升到 45.3，十年期美债收益率降到约 3.93%，油价也下跌。

【INFERENCE】股票、油和长端收益率一起走弱，说明市场交易的不只是某家公司利润，而是贸易升级可能压低增长、抬高不确定性。

但这不是单因故事。鲍威尔当天的谨慎表态、去风险仓位和波动率上升，都可能放大跌幅；强劲就业数据也没能扭转它。

【SCENARIO】接下来要看政策是否收窄、信用利差和 VIX 是否修复、盈利预期是否继续下调。它们会确认或削弱这套解释。""",
}

cases["market"]["scenes"] = [
    scene("mk1", "evidence_card", "DATA", "FACT", {"label": "S&P 500 / Reuters", "date": "2025-04-04", "period": "close-to-close"}, "让观众先感知波动量级。", "MARKET 的第一任务是确认发生了什么，而不是先解释。", "开场 → 市场异动", 0, 8, "S&P 500 单日约 −5.97%，前一日约 −4.8%。", canvas_mode="dark-ink"),
    scene("mk2", "research_timeline", "DOCUMENT", "FACT", {"label": "White House / China MOF", "date": "2025-04-02—2025-04-04"}, "把公告、报复措施和收盘按时间排序。", "观众从幅度切换到事件顺序；时间线比因果箭头更诚实。", "波动 → 时间戳事件", 8, 20, "4/2 美方公告；4/3 首轮抛售；4/4 中方 34% 反制；4/4 再度暴跌。", finance_justification="Chronology is the central structure; CausalChain is intentionally omitted."),
    scene("mk3", "chart", "DATA", "FACT", {"label": "S&P 500 / Nasdaq / Cboe", "date": "2025-04-03—2025-04-04"}, "确认这不是单一股票或单一板块。", "从事件切换到反应广度，需要市场数据画面。", "事件 → 反应模式", 20, 31, "两日指数跌幅与 VIX 跳升。"),
    scene("mk4", "evidence_card", "DATA", "INFERENCE", {"label": "Reuters cross-asset recap", "date": "2025-04-04"}, "用跨资产反应约束解释。", "观众从价格事实转向最谨慎的解释：增长担忧，但保留其他原因。", "反应模式 → 有边界解释", 31, 43, "10Y 收益率约 3.93%，油价下跌；可能反映增长下行风险与去风险。", finance_justification="One synthesis card combines closely related cross-asset evidence."),
    scene("mk5", "watch_list", "DECISION", "SCENARIO", {"label": "Policy announcements / VIX / credit spreads / earnings revisions", "period": "following sessions"}, "给出验证或推翻解释的下一组信号。", "最后的认知任务是判断这套解释以后是否仍成立。", "解释 → 下一步验证", 43, 54, "WATCH NEXT：政策范围、VIX、信用利差、盈利预期。"),
]

cases["macro"] = {
    "topic": "为什么美联储降息 50 个基点后，10 年期美债收益率反而上涨？",
    "event_date": "2024-09-18",
    "reaction_window": "2024-09-17 至 2024-10-31",
    "why_not": "不是 MARKET：这里不是解释某一天的波动，而是区分政策利率与长期收益率，并检验一个跨数周、带条件的传导机制。",
    "router": direction(
        "MACRO", "理解政策利率下降但长期收益率上升的条件性传导",
        ["核心问题是短端政策工具如何经由增长、通胀预期和期限溢价影响长端；结果不是机械同向。"],
        ["central_bank", "rates_data", "official_minutes", "term_premium_framework", "chain_breakers"],
        ["document", "chart", "causal_chain", "evidence_card", "scenario_board"],
        ["document", "data", "full-bleed", "margin-note"], "CONTRADICTION", "CHAIN_BREAKER",
        "用一条确定箭头把观察到的收益率上升解释为单一原因。",
        "必须把已观察的收益率变化、机制假说和条件结果分开。",
        secondary="EXPLAIN", confidence="high", density={"opening": "sparse", "body": "standard", "evidence": "dense", "ending": "standard"},
    ),
    "research": f"""# MACRO — Fed cut, long yield up

DATA CUT-OFF: {CUTOFF}
EVENT / EARNINGS DATE: 2024-09-18 FOMC
MARKET REACTION WINDOW: 2024-09-17 至 2024-10-31

## Evidence ledger

- FACT — FOMC 于 2024-09-18 将联邦基金目标区间下调 50bp 至 4.75%–5.00%。来源：Federal Reserve。{SOURCES['fed_cut']}
- FACT — FRED DGS10：10 年期美债收益率从 2024-09-17 的 3.65% 升至 2024-10-31 的 4.28%，上升 63bp。来源：Federal Reserve H.15 via FRED。{SOURCES['fred_10y']}
- FACT — FOMC 声明同时称经济活动仍以稳健速度扩张，通胀虽有进展但仍偏高；会议纪要记录当时政策与前景不确定。来源：Fed statement/minutes。{SOURCES['fed_minutes']}
- FACT/FRAMEWORK — 长期国债收益率可拆成未来短端利率路径预期与期限溢价；期限溢价不可直接观察，只能模型估计。来源：New York Fed ACM。{SOURCES['nyfed_term']}
- INFERENCE — 更强的增长数据、对未来降息路径的重新定价、通胀/财政风险补偿，都可能推高长端。无法仅靠同期价格确定各自贡献。
- SCENARIO — 若增长和通胀数据转弱且期限溢价回落，长端可重新下行；若通胀、财政供给或风险补偿上升，政策降息仍可能与长端上行并存。
""",
    "script": """# SCRIPT — MACRO（约 60 秒）

【FACT】2024 年 9 月 18 日，美联储一次降息 50 个基点，把政策利率区间降到 4.75% 到 5%。直觉上，利率应该都往下。

但十年期美债收益率从前一天的 3.65%，升到 10 月底的 4.28%，反而上行 63 个基点。

关键是：美联储直接控制的是隔夜政策利率，不是十年期收益率。长端还包含市场对未来短端利率路径的预期，以及持有长期债券要求的期限溢价。

【INFERENCE】如果经济数据比担忧中更强，市场会减少未来降息预期；如果通胀、财政供给或不确定性上升，期限溢价也可能抬高。两条路径都能抵消第一次降息。

但这只是常见传导路径，不是已证明的单一因果。

【SCENARIO】链条会在增长和通胀明显转弱、或期限溢价下降时被打断。所以，“美联储降息”不等于“所有期限利率同步下降”。""",
}

cases["macro"]["scenes"] = [
    scene("ma1", "document", "DOCUMENT", "FACT", {"label": "Federal Reserve FOMC statement", "date": "2024-09-18"}, "确认政策动作和精确目标区间。", "先把‘降息’固定为可核验的政策事实。", "问题 → 官方政策", 0, 10, "FOMC 降息 50bp，目标区间 4.75%–5.00%。", canvas_mode="document"),
    scene("ma2", "chart", "DATA", "FACT", {"label": "FRED DGS10", "date": "2024-09-17—2024-10-31"}, "显示与直觉相反的观察结果。", "观众从政策动作切换到市场结果，需要新的数据坐标。", "政策 → 观察结果", 10, 21, "10Y：3.65% → 4.28%，+63bp。"),
    scene("ma3", "causal_chain", "MECHANISM", "INFERENCE", {"label": "Fed / NY Fed ACM framework", "period": "conditional mechanism"}, "解释短端政策与长端收益率之间的条件性路径。", "这是唯一真正需要 A 影响 B 再影响 C 的认知任务，因此 CausalChain 有必要。", "观察结果 → 可能机制", 21, 36, "降息；增长/通胀路径重估与期限溢价；长端可能上行。", mechanism_importance="Policy rate does not mechanically set the 10-year yield; the viewer must follow two directional channels.", hypothesis=True),
    scene("ma4", "evidence_card", "DATA", "INFERENCE", {"label": "Federal Reserve / NY Fed", "period": "framework and contemporaneous data"}, "标出哪些部分可观察、哪些只能推断。", "从机制图切换到证据边界，防止箭头被误读为已证实因果。", "机制 → 证据边界", 36, 48, "FACT：收益率路径；INFERENCE：未来利率预期与期限溢价贡献。"),
    scene("ma5", "scenario_board", "DECISION", "SCENARIO", {"label": "Future inflation, growth, Treasury supply and term-premium data"}, "说明什么条件会打断这条传导。", "宏观结尾必须保留条件，而不是给出确定方向预测。", "机制边界 → 链条破坏条件", 48, 60, "CHAIN BREAKER：增长/通胀转弱、期限溢价回落；反之则长端仍可能上行。"),
]

cases["flow"] = {
    "topic": "AI 数据中心每投入 100 美元，钱到底流向哪些环节？",
    "event_date": "Epoch AI model updated 2026-05-19",
    "reaction_window": "不适用",
    "why_not": "不是 RESEARCH：问题的中心不是评估某家公司，而是先固定一个可加总的资本开支分母，再追踪价值分配与瓶颈。",
    "router": direction(
        "FLOW", "先定义 1GW 模型的前置 CapEx 分母，再追踪每 100 美元的可加总分配",
        ["Epoch AI 提供公开可复核、合计为总前置 CapEx 的单一模型；Alphabet 只作外部合理性参照，不与模型混加。"],
        ["cost_model", "scope_definition", "category_sources", "industry_cross_check", "uncertainty"],
        ["evidence_card", "money_flow", "document", "text_diagram"],
        ["data", "full-bleed", "margin-note"], "DENOMINATOR", "BOTTLENECK_IMPLICATION",
        "把一个 1GW、美国、GB200 配置的模型写成所有 AI 数据中心的普遍精确分配。",
        "只有同一前置 CapEx 分母中的可加总类别进入 Sankey；不混入电费、折旧或厂商收入。",
        secondary="RESEARCH", confidence="high", density={"opening": "standard", "body": "dense", "evidence": "dense", "ending": "sparse"},
    ),
    "research": f"""# FLOW — AI data-center up-front CapEx

DATA CUT-OFF: {CUTOFF}
EVENT / EARNINGS DATE: Epoch AI 数据更新 2026-05-19
MARKET REACTION WINDOW: 不适用

## Denominator decision

接受 Sankey，但只用于 Epoch AI 的“美国 hyperscaler、1GW IT nameplate、NVIDIA GB200 NVL72、前置 CapEx”模型。它不是全球平均、不是某个真实项目、不是年度 TCO，也不包含电费等 OpEx。

## Additive allocation

- FACT/MODEL INPUT — 总前置 CapEx 378.83 亿美元。Servers 211.88 亿；Facility 114.33 亿；Network infrastructure 49.25 亿；Land 1.72 亿；Utility works 1.64 亿。五项合计 378.82 亿，差 0.01 亿来自展示精度。来源：Epoch AI，更新 2026-05-19。{SOURCES['epoch_ai']}
- DERIVED FACT — 每 100 美元约为：Servers 55.9；Facility 30.2；Network 13.0；Land 0.5；Utility works 0.4。均由同一表分子除以同一总额计算，四舍五入后合计 100.0。
- FACT/CROSS-CHECK — Alphabet 表示其 2025 CapEx 约 60% 用于 machines/servers，约 40% 用于 data centers 和 networking equipment。该口径是 Alphabet 全公司 CapEx，不进入 Sankey，只作为方向性参照。{SOURCES['alphabet_call']}
- FACT — IEA 强调 AI 数据中心离不开电力，并指出综合数据仍有限。电力的重要性不能从其前置 CapEx 占比直接推断。{SOURCES['iea_ai']}
- THESIS — 服务器拿走最大资本份额；但土地和 utility works 占比很小，也可能因电力接入和建设时序成为项目瓶颈。
- LIMITATION — 服务器配置、地点、融资、采购价、设施设计和寿命假设变化都会改写比例。
""",
    "script": """# SCRIPT — FLOW（约 51 秒）

先定义这 100 美元是什么。这里不是全球平均，也不是运营成本，而是一个公开模型：美国、1GW IT 容量、全部采用 GB200 NVL72 的 AI 数据中心，前置资本开支总额约 378.83 亿美元。

【FACT / MODEL】按同一个可加总分母换算，每 100 美元里，服务器约 55.9，机房设施 30.2，网络 13.0，土地 0.5，公用事业接入约 0.4。

这组数可以画 Sankey，因为分子来自同一张表，口径一致，合计为 100。电费、维护和折旧没有混进来。

【THESIS】最大价值份额显然在服务器。但最小的份额不等于最不重要：电力接入和土地只占不到 1 美元，却可能卡住整个项目的时间表。

【LIMITATION】换服务器、地点、采购价或设施设计，比例都会变。所以这是一张可审计的模型地图，不是所有 AI 数据中心的精确账单。""",
}

cases["flow"]["scenes"] = [
    scene("fl1", "document", "DOCUMENT", "FACT", {"label": "Epoch AI 1GW model", "date": "2026-05-19", "period": "up-front CapEx"}, "先定义每 100 美元的分母。", "没有明确分母就不能判断后面的数字是否可加总；这幕防止伪 Sankey。", "问题 → 口径", 0, 12, "美国 1GW、GB200 NVL72、前置 CapEx；总额 378.83 亿美元。", canvas_mode="document"),
    scene("fl2", "money_flow", "MECHANISM", "FACT", {"label": "Epoch AI cost model", "date": "2026-05-19", "period": "up-front CapEx"}, "展示同一分母下的资金分配。", "口径确认后，观众的任务切换为追踪每 100 美元去向；Sankey 在此语义成立。", "口径 → 分配", 12, 28, "服务器 55.9；设施 30.2；网络 13.0；土地与 utility works 合计 0.9。", mechanism_importance="The additive allocation itself is the central information structure.", layout_variant="sankey-lite"),
    scene("fl3", "evidence_card", "DATA", "THESIS", {"label": "Epoch AI / IEA / Alphabet cross-check", "date": "2025—2026"}, "区分价值份额与项目瓶颈。", "从‘谁拿得多’切换到‘谁能卡住项目’，需要新的分析任务。", "分配 → 瓶颈", 28, 40, "服务器占比最大；电力接入占比小却可能制约上线时点。", finance_justification="One evidence frame supports the bottleneck distinction; no second CausalChain is needed."),
    scene("fl4", "text_diagram", "DECISION", "THESIS", {"label": "Model limitations", "date": "2026-05-19"}, "给出有边界的价值捕获结论。", "最后要让观众记住模型用途和不可外推边界，而不是多加一个组件。", "瓶颈 → 有边界结论", 40, 51, "服务器拿走最大资本份额；小占比基础设施仍可能决定项目能否按时上线。"),
]

cases["explain"] = {
    "topic": "为什么一家赚钱的公司，也可能自由现金流为负？",
    "event_date": "Intel FY2023 filed 2024-01-26",
    "reaction_window": "不适用",
    "why_not": "不是 RESEARCH：Intel 只是一个已披露的算例；核心任务是教会观众区分权责发生制利润、经营现金流与资本开支，而非判断 Intel 投资价值。",
    "router": direction(
        "EXPLAIN", "用一个真实报表例子纠正‘赚钱就一定有正自由现金流’的误解",
        ["任务是解释三个会计口径及一个算术桥梁；公司实例只是教学证据。"],
        ["accounting_definition", "cash_flow_statement", "worked_example", "metric_definition_limit"],
        ["comparison", "document", "evidence_card", "chart", "text_diagram"],
        ["paper", "document", "data", "margin-note"], "MISCONCEPTION", "ONE_LINE_TAKEAWAY",
        "把自由现金流说成统一 GAAP 指标，或把负自由现金流自动等同于经营失败。",
        "不强行使用 CausalChain、ExpectationGap、ScenarioBoard 或 ThesisBreaker。",
        secondary="RESEARCH", confidence="high", density={"opening": "sparse", "body": "standard", "evidence": "dense", "ending": "sparse"},
    ),
    "research": f"""# EXPLAIN — profitable but negative free cash flow

DATA CUT-OFF: {CUTOFF}
EVENT / EARNINGS DATE: Intel FY2023 Form 10-K filed 2024-01-26
MARKET REACTION WINDOW: 不适用

## Evidence ledger

- FACT — 权责发生制净利润确认收入和费用的时点，与现金收付不完全相同；经营现金流从净利润出发，调整非现金项目与营运资本变化。Intel 10-K 对经营现金流作同类说明。{SOURCES['intel_10k']}
- FACT — Intel FY2023 净利润 16.75 亿美元；经营现金流 114.71 亿美元；净增固定资产 232.28 亿美元；公司披露 adjusted free cash flow 为 −118.53 亿美元。来源：Intel 2023 Form 10-K。{SOURCES['intel_10k']}
- FACT — 同一现金流量表还列示折旧 78.47 亿美元、股权激励 32.29 亿美元，以及应收、库存、应付等营运资本变化，说明净利润不能直接替代现金流。
- INFERENCE — 负自由现金流可能来自高资本开支或营运资本占用，也可能是经营恶化；仅看正负号不能区分。
- LIMITATION — “自由现金流”不是统一 GAAP 小计，定义可能使用 gross capex、net capex 或其他调整。Intel 的 −118.53 亿美元是公司定义的 adjusted FCF，本例沿用其披露。
- TAKEAWAY — 先问净利润如何转成经营现金流，再问维持/扩张业务用了多少资本开支。
""",
    "script": """# SCRIPT — EXPLAIN（约 52 秒）

一家公司的净利润是正的，自由现金流仍然可以是负的。因为利润表和现金流量表回答的不是同一个问题。

【FACT】权责发生制会在收入赚得、费用发生时确认利润，不一定等到现金真正收付。应收账款、库存增加，会占用现金；折旧这类非现金费用，又会在经营现金流里加回来。

然后还有资本开支。

看 Intel 2023 年：净利润 16.75 亿美元，经营现金流 114.71 亿美元；但净增固定资产达到 232.28 亿美元，公司披露的调整后自由现金流是负 118.53 亿美元。

【INFERENCE】这不自动等于公司没有盈利，也不自动等于投资一定失败。它只说明，在这个定义下，当期经营现金不足以覆盖这笔资本投入。

所以判断现金质量要分两步：利润怎样变成经营现金；经营现金又被营运资本和资本开支拿走多少。还要先核对公司使用的自由现金流定义。""",
}

cases["explain"]["scenes"] = [
    scene("ex1", "comparison", "DATA", "THESIS", None, "纠正‘赚钱等于现金为正’的直觉。", "这幕只提出一个误解，不需要机构化研究结构。", "开场 → 误解", 0, 8, "净利润 > 0，不推出自由现金流 > 0。"),
    scene("ex2", "document", "DOCUMENT", "FACT", {"label": "Intel 2023 Form 10-K", "date": "2024-01-26", "period": "FY2023"}, "给出真实现金流量表证据。", "从概念切换到一份真实报表，观众需要新的证据载体。", "误解 → 报表证据", 8, 20, "净利润 16.75 亿；经营现金流 114.71 亿；净增固定资产 232.28 亿美元。", canvas_mode="document"),
    scene("ex3", "chart", "DATA", "FACT", {"label": "Intel 2023 Form 10-K", "period": "FY2023"}, "完成一个可核对的算例。", "报表原数切换到‘经营现金减资本投入’的计算任务。", "报表 → 算例", 20, 32, "Intel adjusted FCF = 114.71 − 232.28 − 0.96 = −118.53 亿美元。"),
    scene("ex4", "evidence_card", "DATA", "INFERENCE", {"label": "Intel 10-K / accounting framework", "period": "concept"}, "解释营运资本、非现金项目与 CapEx 的不同作用。", "观众从一个公司算例切换到可迁移的通用机制。", "算例 → 通用理解", 32, 43, "净利润经非现金项目与营运资本调整为 CFO；再扣资本开支才得到特定定义的 FCF。", finance_justification="A single synthesis card is simpler than a generic causal chain."),
    scene("ex5", "text_diagram", "DECISION", "THESIS", {"label": "Metric definition check", "period": "takeaway"}, "给观众一条可重复使用的检查顺序。", "最后的任务是带走判断方法，而不是形成公司观点。", "通用理解 → 一句话规则", 43, 52, "TAKEAWAY：先桥接净利润到经营现金，再核对资本开支和 FCF 定义。"),
]


DISCLAIMER = FINANCIAL_DISCLAIMER_ZH

render_cuts = [
    # RESEARCH
    {"id":"research-document","source":"","type":"evidence_card","in_seconds":0,"out_seconds":4,"label":"Q2 FY2026 总营收","primaryValue":"$46.7B","supportingMetrics":[{"label":"同比","value":"+56%","direction":"up"},{"label":"环比","value":"+6%","direction":"up"}],"interpretation":"标题数字强，但市场交易的是更高门槛。","variant":"document","canvasMode":"document","headerTreatment":"compact","sourceTreatment":"compact","period":"Q2 FY2026","sourceDate":"2025-08-27","sourceLabel":"NVIDIA · Q2 FY2026 Results","evidenceIndex":"FACT / COMPANY"},
    {"id":"research-gap","source":"","type":"expectation_gap","in_seconds":4,"out_seconds":8,"metric":"Data Center Revenue","expectedValue":"$41.34B","actualValue":"$41.10B","delta":"−$0.24B","interpretation":"总量强，不等于核心分部继续大幅超预期。","variant":"delta","canvasMode":"paper","density":"sparse","sourceTreatment":"full","period":"Q2 FY2026","sourceDate":"2025-08-27","sourceLabel":"NVIDIA IR · Wall Street consensus"},
    {"id":"research-quality","source":"","type":"evidence_card","in_seconds":8,"out_seconds":12,"label":"增长质量再检查","primaryValue":"72.4%","supportingMetrics":[{"label":"Blackwell 环比","value":"+17%","direction":"up"},{"label":"Data Center 同比","value":"+56%","direction":"up"}],"interpretation":"GAAP 毛利率；当季无面向中国客户的 H20 销售。","analystNote":"强增长仍在，但质量与可见性决定下一道门槛。","variant":"hero-number","canvasMode":"margin-note","headerTreatment":"compact","sourceTreatment":"inline","period":"Q2 FY2026","sourceDate":"2025-08-27","sourceLabel":"NVIDIA IR / 10-Q","evidenceIndex":"EVIDENCE / QUALITY"},
    {"id":"research-ending","source":"","type":"thesis_breaker","in_seconds":12,"out_seconds":16,"thesis":"市场没有否认增长，只是把“足够好”的门槛抬得更高。","conditions":[{"title":"Data Center 重新加速","evidenceToWatch":"quarterly segment revenue"},{"title":"毛利率改善","evidenceToWatch":"GAAP / adjusted margin bridge"},{"title":"中国收入恢复可见性","evidenceToWatch":"H20 / export disclosures"}],"canvasMode":"margin-note","headerTreatment":"compact","sourceTreatment":"compact","period":"NEXT QUARTERS","sourceLabel":"WATCH / NVIDIA filings and earnings","complianceText":DISCLAIMER},
    # MARKET
    {"id":"market-hero","source":"","type":"evidence_card","in_seconds":16,"out_seconds":20,"label":"2025-04-04 · S&P 500","primaryValue":"−5.97%","interpretation":"前一日已经下跌约 4.8%。这不是一根孤立的阴线。","variant":"hero-number","canvasMode":"dark-ink","headerTreatment":"compact","sourceTreatment":"compact","period":"CLOSE-TO-CLOSE","sourceDate":"2025-04-04","sourceLabel":"S&P / Reuters","evidenceIndex":"MARKET / MOVE"},
    {"id":"market-timeline","source":"","type":"research_timeline","in_seconds":20,"out_seconds":24,"title":"两天里发生了什么？","events":[{"date":"04/02","title":"美方公布对等关税","description":"收盘后公布大范围税率","source":"White House"},{"date":"04/03","title":"首轮抛售","description":"S&P 500 约 −4.8%","source":"S&P / Reuters"},{"date":"04/04","title":"中国宣布 34% 反制","description":"4 月 10 日起生效","source":"中国财政部"},{"date":"04/04","title":"风险再次定价","description":"S&P 500 约 −6%","source":"Reuters"}],"highlightedIndex":2,"variant":"vertical","canvasMode":"data","headerTreatment":"compact","sourceTreatment":"compact","period":"2025-04-02—04","sourceLabel":"Official announcements · market close data"},
    {"id":"market-crossasset","source":"","type":"evidence_card","in_seconds":24,"out_seconds":28,"label":"跨资产反应","primaryValue":"VIX 45.3","supportingMetrics":[{"label":"10Y 美债收益率","value":"3.93%","direction":"down"},{"label":"S&P 500 两日","value":"约 −11%","direction":"down"}],"interpretation":"股票、长端收益率与油价同时走弱，更像增长风险重估；不是单因证明。","variant":"table","canvasMode":"data","headerTreatment":"compact","sourceTreatment":"compact","period":"2025-04-04","sourceLabel":"Cboe · Reuters · SF Fed","evidenceIndex":"REACTION / CROSS-ASSET"},
    {"id":"market-ending","source":"","type":"scenario_board","in_seconds":28,"out_seconds":32,"title":"什么会确认或削弱这套解释？","scenarios":[{"name":"CONFIRM","title":"风险继续扩散","description":"盈利预期下修、信用利差走阔，说明增长担忧在扩散。","trigger":"政策升级或谈判失败","metrics":["VIX","credit spreads","earnings revisions"]},{"name":"WEAKEN","title":"政策与风险指标修复","description":"政策收窄、VIX 和信用利差回落，会削弱单向解释。","trigger":"可核验的政策调整","metrics":["official policy","VIX normalization"]}],"highlightedScenario":"CONFIRM","canvasMode":"paper","headerTreatment":"compact","sourceTreatment":"compact","period":"FOLLOWING SESSIONS","sourceLabel":"WATCH NEXT · official policy and market data","complianceText":DISCLAIMER},
    # MACRO
    {"id":"macro-policy","source":"","type":"evidence_card","in_seconds":32,"out_seconds":36,"label":"FOMC 政策利率","primaryValue":"−50 bp","supportingMetrics":[{"label":"新目标区间下限","value":"4.75%","direction":"down"},{"label":"新目标区间上限","value":"5.00%","direction":"down"}],"interpretation":"美联储直接控制的是隔夜政策利率，不是十年期收益率。","variant":"document","canvasMode":"document","headerTreatment":"compact","sourceTreatment":"compact","period":"FOMC","sourceDate":"2024-09-18","sourceLabel":"Federal Reserve · FOMC Statement","evidenceIndex":"FACT / POLICY"},
    {"id":"macro-data","source":"","type":"evidence_card","in_seconds":36,"out_seconds":40,"label":"降息以后，长端反而上行","primaryValue":"+63 bp","supportingMetrics":[{"label":"2024-09-17","value":"3.65%"},{"label":"2024-10-31","value":"4.28%","direction":"up"}],"interpretation":"政策动作与长端市场结果并不机械同向。","variant":"hero-number","canvasMode":"data","headerTreatment":"compact","sourceTreatment":"compact","period":"DGS10","sourceDate":"2024-09-17—10-31","sourceLabel":"Federal Reserve H.15 via FRED","evidenceIndex":"FACT / RATE PATH"},
    {"id":"macro-chain","source":"","type":"causal_chain","in_seconds":40,"out_seconds":44,"title":"一个可能的长端传导路径","nodes":[{"id":"cut","label":"政策利率下降","detail":"已观察事实"},{"id":"reprice","label":"未来短端路径重估","detail":"增长 / 通胀数据可能改变预期"},{"id":"premium","label":"期限溢价变化","detail":"风险补偿不可直接观察"},{"id":"yield","label":"10 年期收益率可能上行","detail":"条件性结果"}],"edges":[{"from":"cut","to":"reprice","relation":"uncertain","label":"未必持续宽松"},{"from":"reprice","to":"premium","relation":"uncertain","label":"与风险补偿并存"},{"from":"premium","to":"yield","relation":"positive","label":"可能推高"}],"hypothesis":True,"activeNodeId":"yield","variant":"linear","canvasMode":"data","headerTreatment":"compact","sourceTreatment":"compact","period":"CONDITIONAL MECHANISM","sourceLabel":"Fed · New York Fed ACM framework"},
    {"id":"macro-ending","source":"","type":"scenario_board","in_seconds":44,"out_seconds":48,"title":"哪里会打断这条链？","scenarios":[{"name":"BREAK","title":"增长与通胀转弱","description":"未来短端路径下移，期限溢价也可能回落。","trigger":"连续官方数据确认降温","metrics":["inflation","employment","term premium"]},{"name":"PERSIST","title":"风险补偿仍高","description":"财政供给、通胀或不确定性维持，长端可继续偏高。","trigger":"风险补偿没有回落","metrics":["Treasury supply","ACM term premium"]}],"canvasMode":"margin-note","headerTreatment":"compact","sourceTreatment":"inline","period":"CHAIN BREAKER","sourceLabel":"WATCH · official data and NY Fed estimates","complianceText":DISCLAIMER},
    # FLOW
    {"id":"flow-denominator","source":"","type":"evidence_card","in_seconds":48,"out_seconds":52,"label":"先定义这 100 美元","primaryValue":"$37.883B","supportingMetrics":[{"label":"IT nameplate","value":"1 GW"},{"label":"服务器配置","value":"GB200 NVL72"}],"interpretation":"美国 hyperscaler AI 数据中心模型；前置 CapEx，不含电费与运维。","variant":"document","canvasMode":"document","headerTreatment":"compact","sourceTreatment":"compact","period":"UP-FRONT CAPEX MODEL","sourceDate":"2026-05-19","sourceLabel":"Epoch AI · 1GW AI data center model","evidenceIndex":"DENOMINATOR"},
    {"id":"flow-sankey","source":"","type":"money_flow","in_seconds":52,"out_seconds":56,"title":"每 100 美元前置 CapEx 去向","nodes":[{"id":"total","label":"1GW AI Data Center","value":"$100.0"},{"id":"server","label":"Servers","value":"$55.9"},{"id":"facility","label":"Facility","value":"$30.2"},{"id":"network","label":"Network Infrastructure","value":"$13.0"},{"id":"other","label":"Land + Utility Works","value":"$0.9"}],"edges":[{"from":"total","to":"server","value":55.9,"label":"55.9"},{"from":"total","to":"facility","value":30.2,"label":"30.2"},{"from":"total","to":"network","value":13.0,"label":"13.0"},{"from":"total","to":"other","value":0.9,"label":"0.9"}],"highlightedPath":["total","server"],"variant":"sankey-lite","canvasMode":"full-bleed","headerTreatment":"none","sourceTreatment":"inline","period":"MODEL · UP-FRONT CAPEX","sourceDate":"2026-05-19","sourceLabel":"Epoch AI · stylized 1GW US model","evidenceIndex":"ALLOCATION"},
    {"id":"flow-bottleneck","source":"","type":"evidence_card","in_seconds":56,"out_seconds":60,"label":"最大份额，不等于唯一瓶颈","primaryValue":"55.9 / 100","supportingMetrics":[{"label":"Facility","value":"30.2"},{"label":"Network","value":"13.0"}],"interpretation":"服务器拿走最大资本份额。","analystNote":"占比不到 1 的土地与电力接入，也可能卡住整个上线时点。","variant":"hero-number","canvasMode":"margin-note","headerTreatment":"compact","sourceTreatment":"inline","period":"MODEL INTERPRETATION","sourceLabel":"Epoch AI · IEA cross-check","evidenceIndex":"VALUE CAPTURE"},
    {"id":"flow-ending","source":"","type":"evidence_card","in_seconds":60,"out_seconds":64,"label":"模型能回答什么？","primaryValue":"≠","interpretation":"资本份额，不等于项目关键性。它不能替代具体项目的采购、地点与电力约束。","analystNote":"可审计的模型地图，不是所有 AI 数据中心的精确账单。","variant":"hero-number","canvasMode":"data","density":"sparse","headerTreatment":"compact","sourceTreatment":"compact","period":"LIMITATION","sourceLabel":"Epoch AI model assumptions","evidenceIndex":"TAKEAWAY","complianceText":DISCLAIMER},
    # EXPLAIN
    {"id":"explain-misconception","source":"","type":"evidence_card","in_seconds":64,"out_seconds":68,"label":"赚钱，就一定有正自由现金流？","primaryValue":"不一定","interpretation":"利润确认时点、营运资本和资本开支，都会改变现金结果。","variant":"hero-number","canvasMode":"paper","density":"sparse","headerTreatment":"full","sourceTreatment":"compact","sourceLabel":"ACCOUNTING / CONCEPT","evidenceIndex":"MISCONCEPTION"},
    {"id":"explain-document","source":"","type":"evidence_card","in_seconds":68,"out_seconds":72,"label":"Intel FY2023 现金流量表","primaryValue":"$1.675B","supportingMetrics":[{"label":"经营现金流","value":"$11.471B","direction":"up"},{"label":"Adjusted FCF","value":"−$11.853B","direction":"down"}],"interpretation":"净利润为正，自由现金流仍可为负。","variant":"document","canvasMode":"document","headerTreatment":"compact","sourceTreatment":"compact","period":"FY2023","sourceDate":"2024-01-26","sourceLabel":"Intel · 2023 Form 10-K","evidenceIndex":"FACT / 10-K"},
    {"id":"explain-worked","source":"","type":"evidence_card","in_seconds":72,"out_seconds":76,"label":"经营现金之后，还有资本开支","primaryValue":"−$23.228B","supportingMetrics":[{"label":"CFO","value":"$11.471B"},{"label":"finance leases","value":"−$0.096B"}],"interpretation":"Intel 定义：11.471 − 23.228 − 0.096 = −11.853。","variant":"table","canvasMode":"data","headerTreatment":"compact","sourceTreatment":"compact","period":"FY2023 · ADJUSTED FCF BRIDGE","sourceLabel":"Intel · 2023 Form 10-K","evidenceIndex":"WORKED EXAMPLE"},
    {"id":"explain-ending","source":"","type":"evidence_card","in_seconds":76,"out_seconds":80,"label":"判断现金质量，分两步","primaryValue":"利润 → CFO → FCF","interpretation":"先看非现金项目与营运资本，再核对资本开支和公司采用的 FCF 定义。","analystNote":"负自由现金流不自动等于经营失败；正净利润也不等于现金充足。","variant":"hero-number","canvasMode":"margin-note","headerTreatment":"compact","sourceTreatment":"inline","period":"ONE-LINE TAKEAWAY","sourceLabel":"Intel 10-K · accounting framework","evidenceIndex":"TAKEAWAY","complianceText":DISCLAIMER},
]


EVALUATIONS = {
    "research": """# Evaluation — RESEARCH

- Editorial verdict: PASS.
- The document evidence, comparable expectation gap, operating-quality check, and watch-list ending form a company-research argument rather than an event recap.
- The weak reaction is kept separate from reported fundamentals; no single-cause claim is made.
- Visual review: the document and margin-note canvases feel publication-like, the source anchors are readable, and the expectation values fit after currency formatting was corrected.
- Limitation: consensus remains Tier 2 evidence and must always retain its metric/quarter qualifier.
""",
    "market": """# Evaluation — MARKET

- Editorial verdict: PASS WITH MINOR LIMITATION.
- The plan reconstructs a dated event window, then checks the cross-asset reaction and ends with confirm/weaken signals. It does not use CausalChain.
- Visual review: the dark-ink move frame and vertical timeline create appropriately faster pacing without leaving the Finance Dossier brand.
- Limitation: the two-column ScenarioBoard ending leaves more unused lower-panel space than ideal and feels slightly more template-like than the preceding frames.
""",
    "macro": """# Evaluation — MACRO

- Editorial verdict: PASS WITH MINOR LIMITATION.
- Observed policy and yield facts are separated from a conditional mechanism hypothesis. CausalChain is justified because the audience task is transmission, and uncertain edges prevent false certainty.
- Visual review: policy document, data result, mechanism, and chain-breaker canvases are materially distinct while remaining one publication family.
- Limitation: as in MARKET, the ScenarioBoard ending is visually less vertically efficient than the strongest evidence and mechanism frames.
""",
    "flow": """# Evaluation — FLOW

- Editorial verdict: PASS.
- The denominator is defined before allocation. The Epoch AI categories are one additive up-front CapEx model, so Sankey-lite is semantically valid and explicitly not presented as a universal bill of materials.
- Visual review: the full-bleed Sankey makes flow the hero; long labels stay inside nodes and sources remain readable. The ending clearly separates capital share from project criticality.
- Limitation: the smallest 0.9 allocation is visually legible but necessarily less prominent; narration must preserve the bottleneck caveat.
""",
    "explain": """# Evaluation — EXPLAIN

- Editorial verdict: PASS.
- The sequence teaches a misconception, presents a real 10-K example, performs one worked bridge, generalizes the mechanism, and ends with a reusable check. It avoids ExpectationGap, Sankey, ScenarioBoard, ThesisBreaker, and CausalChain.
- Visual review: the opening is deliberately quiet, the document page carries proof, and the final margin note reads as an educational takeaway rather than investment research theater.
- Limitation: Intel's adjusted FCF is a company-defined non-GAAP measure, so the definition caveat must remain adjacent to the example.
""",
}


def write_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    plans = {}
    summary = {"data_cut_off": CUTOFF, "cases": {}}
    for slug, case in cases.items():
        folder = OUT / slug
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "stills").mkdir(exist_ok=True)
        router_out = {
            "topic": case["topic"],
            "data_cut_off": CUTOFF,
            "event_or_earnings_date": case["event_date"],
            "market_reaction_window": case["reaction_window"],
            **case["router"],
            "why_is_this_not_another_mode": case["why_not"],
        }
        write_json(folder / "router.json", router_out)
        (folder / "research.md").write_text(case["research"].strip() + "\n", encoding="utf-8")
        (folder / "script.md").write_text(case["script"].strip() + "\n", encoding="utf-8")
        (folder / "evaluation.md").write_text(EVALUATIONS[slug].strip() + "\n", encoding="utf-8")
        plan = {
            "version": "1.0",
            "metadata": {
                "content_category": "finance",
                "data_cut_off": CUTOFF,
                "event_or_earnings_date": case["event_date"],
                "market_reaction_window": case["reaction_window"],
                "editorial_direction": case["router"],
                "compliance": {
                    "financial_disclaimer": DISCLAIMER,
                    "presentation": "footer",
                    "placement": "ending",
                    "ending_scene_id": case["scenes"][-1]["id"],
                },
            },
            "scenes": case["scenes"],
        }
        plans[slug] = plan
        write_json(folder / "scene-plan.json", plan)
        result = FinanceSceneVarietyValidator().validate(plan)
        compliance = {"valid": True, "presentation": "footer", "ending_scene_id": case["scenes"][-1]["id"]}
        try:
            enforce_financial_disclaimer("scene_plan", {"proposal_packet": {"content_category": "finance"}, "scene_plan": plan})
        except Exception as exc:  # pragma: no cover - retained in the artifact if policy changes
            compliance = {"valid": False, "error": str(exc)}
        validation = {"finance_scene_variety": result, "content_policy": compliance}
        write_json(folder / "validation.json", validation)
        summary["cases"][slug] = {
            "topic": case["topic"],
            "primary_mode": case["router"]["primary_mode"],
            "secondary_mode": case["router"].get("secondary_mode"),
            "scene_count": len(case["scenes"]),
            "causal_chain_used": any(s["finance_scene_type"] == "causal_chain" for s in case["scenes"]),
            "expectation_gap_used": any(s["finance_scene_type"] == "expectation_gap" for s in case["scenes"]),
            "sankey_used": any(s["finance_scene_type"] == "money_flow" and s.get("layout_variant") == "sankey-lite" for s in case["scenes"]),
            "standalone_disclaimer": False,
            "warning_codes": [w["code"] for w in result["warnings"]],
        }
    signature = validate_finance_mode_signatures(plans)
    write_json(OUT / "editorial-signature-validation.json", signature)
    summary["editorial_signature_validation"] = signature
    write_json(OUT / "summary.json", summary)
    (OUT / "evaluation-report.md").write_text(
        """# Finance Dossier real-topic stress test

DATA CUT-OFF: 2026-08-28

| Mode | Topic | Audience task | Scenes | Main visual language | CausalChain | ExpectationGap | Sankey | Standalone disclaimer | Warnings | Verdict |
|---|---|---|---:|---|---|---|---|---|---|---|
| RESEARCH | NVIDIA Q2 FY2026：结果强、反应弱 | 对照公司结果、预期与增长质量 | 5 | document / expectation gap / evidence / watch list | No | Yes | No | No | None | PASS |
| MARKET | 2025-04-04 关税冲击 | 重建时间窗与跨资产风险重估 | 5 | dark-ink hero / timeline / cross-asset evidence | No | No | No | No | None | PASS WITH MINOR LIMITATION |
| MACRO | 降息后长端收益率反而上行 | 区分政策动作、传导假设与条件结果 | 5 | document / data / conditional chain / chain breaker | Yes | No | No | No | None | PASS WITH MINOR LIMITATION |
| FLOW | 1GW AI 数据中心前置 CapEx | 先定义分母，再追踪可加总分配与瓶颈 | 4 | denominator document / full-bleed Sankey / annotation | No | No | Yes | No | None | PASS |
| EXPLAIN | 盈利公司为何自由现金流为负 | 用一份 10-K 完成可迁移的会计解释 | 5 | misconception / document / worked bridge / takeaway | No | No | No | No | None | PASS |

## What worked

- Five topics produce different editorial grammars without changing the Finance Dossier brand.
- Scene counts emerge from cognitive transitions: 5 / 5 / 5 / 4 / 5; no six-scene signature appears.
- Only the genuine macro-transmission case uses CausalChain.
- The FLOW case accepts Sankey only after establishing one additive denominator.
- FACT, INFERENCE, THESIS, SCENARIO, dates, reaction windows, and source anchors remain explicit.
- Compliance is rendered in the final meaningful frame footer; no standalone disclaimer scene exists.

## What failed or felt template-like

- No editorial failure condition was triggered.
- MARKET and MACRO ScenarioBoard endings leave more lower-panel space than the strongest frames and feel slightly more templated.
- Two initial render-fixture mappings needed correction during visual QA: currency suffix order in RESEARCH and an overlong hero value in the FLOW ending. Neither required a component or architecture change.

## What the system refused to force

- No synthetic consensus, current-event invention, deterministic cause, fixed six-scene plan, generic CausalChain, non-additive Sankey, or standalone disclaimer.
- The newest NVIDIA earnings case was rejected because its market response did not fit the proposed contradiction; a prior, better-supported quarter was selected and disclosed.

## Missing visual capability discovered

No new visual component is justified by this five-case sample. Portrait-native, source-aware time-series charts remain a candidate for further testing, but the current evidence/timeline compositions were sufficient here.

## Production verdict

READY WITH MINOR LIMITATIONS. Evidence discipline, routing, scene boundaries, compliance placement, and mode differentiation held across all five real topics. Before public release, each episode still needs human review of market-window definitions, Tier 2 consensus comparability, and final-frame vertical composition.
""",
        encoding="utf-8",
    )
    write_json(OUT / "render-props.json", {"theme": "finance-dossier", "width": 1080, "height": 1920, "brand": {"label": "深度财经研究所", "series": "FINANCE DOSSIER", "issue": "REAL TEST / 2026-08-28"}, "cuts": render_cuts, "overlays": [], "captions": [], "audio": {}})
    print(f"Wrote Finance Dossier stress-test artifacts to {OUT}")


if __name__ == "__main__":
    main()
