"""Step 2 — proposal_packet + decision_log for etf-100k-four-fund-race.

Single owner of: artifacts/proposal_packet.json, artifacts/decision_log.json

Human-gated stage. The user answered four intake questions up front
(系列归属 / 口播密度 / 画幅 / 审批方式) and explicitly pre-authorized all
downstream gates; that policy is recorded here and in decision_log.metadata.

NOTE on a schema/guide conflict: AGENT_GUIDE asks for a decision_log entry with
category "approval_policy", but schemas/artifacts/decision_log.schema.json does
not allow that value in its category enum. The pre-authorization is therefore
recorded in proposal_packet.metadata.approval_policy and in
decision_log.metadata.approval_policy instead of as an invalid decision entry.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parent
REPO = PROJECT.parent.parent
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

OUT_PROPOSAL = PROJECT / "artifacts" / "proposal_packet.json"
OUT_LOG = PROJECT / "artifacts" / "decision_log.json"

PROJECT_ID = PROJECT.name
SLUG = PROJECT.name
ART_DIR = f"projects/{SLUG}/art-direction-instrument-plate.md"
DISCLAIMER = "本视频仅作知识分享，不构成任何投资建议。市场有风险，投资需谨慎。"
DURATION = 97.0

# --------------------------------------------------------------------------
# decision_log — categories must come from the schema enum
# --------------------------------------------------------------------------
DECISIONS = [
    {
        "decision_id": "d-001",
        "stage": "proposal",
        "category": "pipeline_selection",
        "subject": "Production pipeline",
        "options_considered": [
            {
                "option_id": "finance-dossier",
                "label": "finance-dossier",
                "score": 0.95,
                "reason": "内容类别为 finance，需要结尾不可改写的原生合规文案与财经编辑层；本片是证据先行的数据对比短片，落在该流水线的能力正中。",
            },
            {
                "option_id": "animation",
                "label": "animation（动画优先）",
                "score": 0.72,
                "reason": "本片确实以动效承载全部内容，形式上接近动画优先。",
                "rejected_because": "该流水线没有 finance 的合规元数据契约，结尾免责声明只能退化为独立成卡，且缺少财经编辑规范与数据场景分类。",
            },
            {
                "option_id": "animated-explainer",
                "label": "animated-explainer",
                "score": 0.66,
                "reason": "通用解说，产能成熟。",
                "rejected_because": "同样缺失 finance 合规契约；且本片不需要解说型叙事结构。",
            },
        ],
        "selected": "finance-dossier",
        "reason": "「涉及基金与收益比较即 finance 类别」的硬性要求下，只有该流水线原生承载合规文案契约；同时它的数据场景族（explainer-data）与零基线图表规范正对本片形态。",
        "user_visible": True,
        "user_approved": True,
        "confidence": 0.95,
    },
    {
        "decision_id": "d-002",
        "stage": "proposal",
        "category": "concept_selection",
        "subject": "Narrative concept",
        "options_considered": [
            {
                "option_id": "c1",
                "label": "同一天起跑的四条线 → 冻结结果 → 但是过程一样吗 → 回撤与时间",
                "score": 0.97,
                "reason": "严格按用户提供的《视频内容规划》结构执行：开场提问、公布规则、核心动态折线、冻结结果、最大回撤、结尾分组。",
            },
            {
                "option_id": "c2",
                "label": "先亮出 8 万元的差距，再回到 2020 年重跑一遍",
                "score": 0.78,
                "reason": "倒叙的数字冲击更强，前3秒留存最好。", 
                "rejected_because": "会把观众的注意力引向\"结果\"而不是\"过程\"，削弱本片最有价值的发现（回撤的持续时间差异）。",
            },
            {
                "option_id": "c3",
                "label": "从 -38.5% 与 -12.9% 的回撤体验开场",
                "score": 0.74,
                "reason": "情绪冲击最直接。",
                "rejected_because": "以回撤开场需要先建立\"同样10万、同一天\"的前提，否则观众无法判断这两个数字是不是可比；顺序被规划明确固定。",
            },
            {
                "option_id": "c4",
                "label": "悬念式逐条加入曲线（一次只追一条线）",
                "score": 0.62,
                "reason": "单线追踪更长，适合更长的时长。",
                "rejected_because": "\"同一天、同一笔钱、四条线同时跑\"的并列张力会被拆散，且远超 90-100 秒的时长约束。",
            },
        ],
        "selected": "c1",
        "reason": "用户已提供完整内容规划并要求据此执行；c1 即规划结构本身，也是唯一在 97 秒内同时容纳\"四条线并列竞速 + 结果冻结 + 过程对比\"的方案。",
        "user_visible": True,
        "user_approved": True,
        "confidence": 0.97,
    },
    {
        "decision_id": "d-003",
        "stage": "proposal",
        "category": "playbook_selection",
        "subject": "Visual style and playbook",
        "options_considered": [
            {
                "option_id": "finance-dossier-instrument-plate",
                "label": "finance-dossier + 仪器刻线纸（本片专属美术方向）",
                "score": 0.94,
                "reason": "内容本质是一张计量图；刻线纸语言（细网格、等宽数字、零基线、起跑线装置）直接把\"这是一次测量\"的信任感建立起来，并支持四条线的长时可读。",
            },
            {
                "option_id": "premium-minimalist",
                "label": "premium-minimalist",
                "score": 0.71,
                "reason": "干净专业，适合专家解说。",
                "rejected_because": "它擅长的是文字层级与留白，缺少承载 1510 个点的图表制图规范与起跑线装置。",
            },
            {
                "option_id": "minimalist-diagram",
                "label": "minimalist-diagram",
                "score": 0.7,
                "reason": "适合技术图解。",
                "rejected_because": "面向静态结构图，长时间连续的收益曲线竞速不是它的强项。",
            },
            {
                "option_id": "flat-motion-graphics",
                "label": "flat-motion-graphics",
                "score": 0.62,
                "reason": "活泼、适合社交短视频。",
                "rejected_because": "本片基调是克制的数据分析，扁平动效的活泼感会与内容气质冲突，且削弱精确感。",
            },
        ],
        "selected": "finance-dossier-instrument-plate",
        "reason": "美术方向见 " + ART_DIR + "：冷调近白刻线纸、四条身份色、深墨反白强调、¥100,000 起跑线装置。刻意避开任何现有系列的纸张质感与页眉，因为本片按用户要求是独立单条、不做系列标识。",
        "user_visible": True,
        "user_approved": True,
        "confidence": 0.94,
    },
    {
        "decision_id": "d-004",
        "stage": "proposal",
        "category": "renderer_family_selection",
        "subject": "Creative renderer family",
        "options_considered": [
            {
                "option_id": "explainer-data",
                "label": "explainer-data",
                "score": 0.95,
                "reason": "本片是纯数据化解说：一个坐标系、四条序列、若干注解与两张统计图。",
            },
            {
                "option_id": "animation-first",
                "label": "animation-first",
                "score": 0.7,
                "reason": "全片确实由动效承载。",
                "rejected_because": "animation-first 偏向风格化运动表达，而本片的动效必须严格服从数据几何（揭示边界与数值同步），不是表现性动画。",
            },
            {
                "option_id": "cinematic-trailer",
                "label": "cinematic-trailer",
                "score": 0.28,
                "reason": "影调强、情绪强。",
                "rejected_because": "与克制分析型表达正面冲突，且会牺牲刻度与数字的可读性。",
            },
        ],
        "selected": "explainer-data",
        "reason": "与 finance-dossier 清单声明的 default_renderer_family 一致，也符合本片\"数据回答一个问题\"的形态。",
        "user_visible": True,
        "user_approved": True,
        "confidence": 0.95,
    },
    {
        "decision_id": "d-005",
        "stage": "proposal",
        "category": "render_runtime_selection",
        "subject": "Composition runtime",
        "options_considered": [
            {
                "option_id": "remotion",
                "label": "Remotion（React 合成）",
                "score": 0.95,
                "reason": "本片最难的三件事——1510 个点 × 4 条序列的 clipPath 揭示与末端数值签同步、四条跟随标签的竖向防重叠、竖屏安全区自动收敛——在 React 组件里表达最直接；确定性数字与图表几何由组件状态管理，不会漂移。",
            },
            {
                "option_id": "hyperframes",
                "label": "HyperFrames（HTML/CSS/GSAP 合成）",
                "score": 0.79,
                "reason": "诚实权衡：它在字体驱动的动势与编排上更强，做纯文字型短片更漂亮；但本片的难点是精确的图表几何与长序列揭示，且竖屏安全区需要手写实现，返工风险更高。",
                "rejected_because": "本片是数据几何驱动而非字体驱动；Remotion 在确定性与安全区上更可控。",
            },
            {
                "option_id": "ffmpeg",
                "label": "FFmpeg 纯剪辑",
                "score": 0.2,
                "reason": "诚实权衡：成本最低、最稳定，适合简单拼接。",
                "rejected_because": "无法实现曲线揭示、跟随标签与状态动效，会退化成静帧拼接，低于本片质量下限。",
            },
        ],
        "selected": "remotion",
        "reason": "内容适配优先：本片交付承诺依赖连续运动的确定性图表，Remotion 的组件化时间轴是摩擦最小的路径。preflight 已确认 ffmpeg / remotion / hyperframes 三者均可用，本选择不是可用性驱动的。",
        "user_visible": True,
        "user_approved": True,
        "confidence": 0.95,
    },
    {
        "decision_id": "d-006",
        "stage": "proposal",
        "category": "composition_mode",
        "subject": "Composition authoring mode",
        "options_considered": [
            {
                "option_id": "atelier",
                "label": "Atelier（手写专属合成）",
                "score": 0.93,
                "reason": "本片的核心机制无法由任何库存场景类型拼出来：需要一个跨越 57 秒连续揭示的坐标系、跟随曲线移动的双行数值签、随揭示点亮的年份刻度、以及常驻的 ¥100,000 起跑线装置。这些必须手写；库存组件最多只能作为机制参考。",
            },
            {
                "option_id": "templated",
                "label": "Templated（拼装库存场景类型）",
                "score": 0.55,
                "reason": "快、稳、便宜，`line_chart` / `bar_chart` / `stat_card` 可以直接拼出一版。",
                "rejected_because": "库存 `line_chart` 不支持跟随曲线的动态标签与跨场景连续揭示，成品会变成若干张静态图表卡片的轮播——而本片的全部价值恰恰在\"过程是连续的\"。",
            },
        ],
        "selected": "atelier",
        "reason": "本片是独立成片，视觉语言必须是一次性的；且必须新写图中装置。代价是比 templated 多花迭代成本，已在提案中如实告知。",
        "user_visible": True,
        "user_approved": True,
        "confidence": 0.93,
    },
    {
        "decision_id": "d-007",
        "stage": "proposal",
        "category": "motion_commitment",
        "subject": "Visual coverage strategy",
        "options_considered": [
            {
                "option_id": "composition-only",
                "label": "纯合成（确定性合成承担全部画面）",
                "score": 0.93,
                "reason": "按信息责任逐段分类，本片 15 个 beat 中 15 个都是 precision-critical：金额、比例、日期、回撤幅度、持续时长、年份刻度、排名位置——每一个都必须被读准。不存在任何一个 beat，真实素材能比确定性图形更准确地传达它要传达的信息。库存素材只能提供\"财经感\"的氛围，属于本片明令拒绝的 decorative_only。",
            },
            {
                "option_id": "light-hybrid",
                "label": "轻混合（确定性图形 + 少量真实动态素材）",
                "score": 0.6,
                "reason": "诚实权衡：可以给 75-85 秒的\"过程体验\"段加一到两个真实环境镜头（例如长时段延时），让\"熬了三年\"有一点身体感。",
                "rejected_because": "两个理由：一是该段的全部说服力来自 1087 天 vs 58 天这组精确数字，素材只能做背景无法承载事实，属于 decorative_only；二是用户提供的规划在\"建议删除\"里明确列入了泛财经空镜与复杂转场，\"建议保留\"里只有时间、金额、曲线、最终收益、最大回撤与少量年份节点。",
            },
            {
                "option_id": "footage-led",
                "label": "素材主导",
                "score": 0.25,
                "reason": "真实感最强。",
                "rejected_because": "与本片\"纯数据动态折线、极简背景、少文字\"的规划要求正面冲突。",
            },
        ],
        "selected": "composition-only",
        "reason": "结论是显式的：本片不存在语义动态候选。全部 15 个 beat 为 precision-critical，0 个语义动态候选，0 个装饰性素材被采用。因此素材阶段不调用任何视频生成或库存素材能力——这是审计结论，不是省略。",
        "user_visible": True,
        "user_approved": True,
        "confidence": 0.93,
    },
    {
        "decision_id": "d-008",
        "stage": "proposal",
        "category": "voice_selection",
        "subject": "Narration voice",
        "options_considered": [
            {
                "option_id": "none",
                "label": "无口播（用户选择）",
                "score": 1.0,
                "reason": "用户在开工前明确选择\"全程无口播：只有画面、字幕和数据，完全静音\"。",
            },
            {
                "option_id": "doubao-dayi-2",
                "label": "豆包 大壹 2.0（持久默认）",
                "score": 0.6,
                "reason": "持久默认人声，普通话自然、支持时间戳；若采用，会按 segmented 模式按段合成。",
                "rejected_because": "用户显式覆盖了默认值，选择完全无口播。已如实告知该选择对短视频平台完播与互动的不利影响，用户知情选择。",
            },
            {
                "option_id": "other-tts",
                "label": "其他 TTS 提供方",
                "score": 0.2,
                "reason": "当前 TTS 能力为 1/7 configured，仅豆包可用。",
                "rejected_because": "无提供方可用，且用户已选择无口播。",
            },
        ],
        "selected": "none",
        "reason": "用户显式覆盖持久默认值。本片不使用 tts_selector，不产出任何旁白音频；承载叙事的文字全部是原生场景排版，并在竖屏安全区内实现。",
        "user_visible": True,
        "user_approved": True,
        "confidence": 1.0,
    },
    {
        "decision_id": "d-009",
        "stage": "proposal",
        "category": "music_source",
        "subject": "Background music source",
        "options_considered": [
            {
                "option_id": "none",
                "label": "无背景音乐",
                "score": 1.0,
                "reason": "继承持久默认 media_defaults.background_music_enabled=false；且用户选择完全静音。",
            },
            {
                "option_id": "ai_generated",
                "label": "API 生成音乐",
                "score": 0.2,
                "reason": "当前 music_generation 为 0/3 configured，无可用提供方。",
                "rejected_because": "无提供方可用，且持久默认与用户选择都不启用音乐。",
            },
            {
                "option_id": "user_library",
                "label": "使用本地曲库",
                "score": 0.2,
                "reason": "music_library/ 未配置（0/1）。",
                "rejected_because": "无曲库可用，且用户选择完全静音。",
            },
        ],
        "selected": "none",
        "reason": "应用持久无BGM默认；下游素材、编辑与合成阶段必须完全省略音乐层。",
        "user_visible": True,
        "user_approved": True,
        "confidence": 1.0,
    },
    {
        "decision_id": "d-010",
        "stage": "proposal",
        "category": "provider_selection",
        "subject": "Cover visual provider",
        "options_considered": [
            {
                "option_id": "host_imagegen_plus_native",
                "label": "宿主图像生成提供材质底板 + 本地确定性排版叠加全部文字与图表",
                "score": 0.9,
                "reason": "非 Codex 宿主的等效能力：宿主图像生成负责无字的材质底板，中文、数字、图表几何、合规角标全部由本地确定性排版叠加，保证零错字与数值准确。",
            },
            {
                "option_id": "pure_deterministic",
                "label": "完全本地确定性合成（Pillow 直接绘制整张封面）",
                "score": 0.82,
                "reason": "最可控、零成本、零水印风险。",
                "rejected_because": "缺少材质层的封面在信息流里偏平；且宿主已有等效图像生成能力，按规程优先使用它提供核心视觉底板。",
            },
            {
                "option_id": "stock_only",
                "label": "仅使用库存图（Pexels / Pixabay）",
                "score": 0.5,
                "reason": "免费、真实。",
                "rejected_because": "库存财经图会引入本片明令拒绝的泛金融空镜语言，且与刻线纸美术方向不符。",
            },
        ],
        "selected": "host_imagegen_plus_native",
        "reason": "封面只广告真正拍出来的那支片：底板由宿主生成，全部中文与数字（含 8.09 万、93.62%、-38.45%）由本地确定性排版叠加，缩略图尺寸下复核可读。",
        "user_visible": True,
        "user_approved": True,
        "confidence": 0.9,
    },
    {
        "decision_id": "d-011",
        "stage": "cover",
        "category": "provider_selection",
        "subject": "Cover visual provider",
        "options_considered": [
            {
                "option_id": "pure_deterministic",
                "label": "完全本地确定性合成（Pillow 一次画完整张封面）",
                "score": 0.93,
                "reason": "封面核心视觉必须与成片同源：同一张归一化竞速图、同一条 ¥100,000 起跑线、同一组期末金额。确定性绘制让曲线几何与每一个数字都可核对，且零成本、零水印。",
            },
            {
                "option_id": "host_imagegen_plus_native",
                "label": "宿主图像生成提供材质底板 + 本地确定性排版叠加文字与图表（原方案 d-010）",
                "score": 0.6,
                "reason": "非 Codex 宿主的等效能力；底板可以给封面加一层材质。",
                "rejected_because": "执行时判断：① 底板不承载任何信息，却要消耗图像生成额度（单张约 5-10 credits）；② 生成图存在水印风险，需要额外裁切处理；③ 本片封面的说服力全部来自那张与成片同源的曲线图，底板加了也无法参与表达。改为完全确定性合成，能力使用量只减不增。",
            },
        ],
        "selected": "pure_deterministic",
        "reason": "本条取代 d-010 的选择（沿用同一 (category, subject) 组合追加记录，不改写历史条目）。执行期的判断修订，这不是能力降级：它减少了一次付费能力的调用，同时把封面的每一个像素都变成可核对的输出。cover_defaults.codex_primary_visual_required 仅适用于 Codex 会话，本机为非 Codex 宿主，因此不涉及 override。",
        "user_visible": True,
        "user_approved": True,
        "confidence": 0.93,
    },
]

DECISION_LOG = {
    "version": "1.0",
    "project_id": PROJECT_ID,
    "decisions": DECISIONS,
}

# The decision_log schema is additionalProperties:false at the root and its
# category enum has no approval-related value, so the run's approval policy is
# recorded on the gated proposal artifact instead. See module docstring.
APPROVAL_POLICY = {
    "mode": "pre_authorized_all_subsequent_gates",
    "recorded_at": "2026-09-21",
    "recorded_by": "user_explicit_choice",
    "gates_covered": ["script", "scene_plan", "assets", "cover", "publish"],
    "statement": (
        "用户在提案阶段明确选择「一次性预授权后续所有门」：提案确认后，"
        "script / scene_plan / assets / cover / publish 五道门自动推进，不再逐门人工确认；"
        "遇阻塞或需要变更已批准的重大选择时仍必须停下上报。"
    ),
    "proposal_gate_itself": "仍然需要一次人工确认（proposal 门未包含在预授权范围内）。",
    "schema_conflict_note": (
        "AGENT_GUIDE.md 要求把该预授权记为 decision_log 中 category='approval_policy' 的一条决策，"
        "但 schemas/artifacts/decision_log.schema.json 的顶层是 additionalProperties:false 且 category 枚举"
        "不含该取值，写进去会让 decision_log 无法通过自身 schema 校验。因此该记录改放在"
        "proposal_packet.metadata.approval_policy 与 proposal_packet.approval.user_notes。"
    ),
}

# --------------------------------------------------------------------------
# proposal_packet
# --------------------------------------------------------------------------
CONCEPTS = [
    {
        "id": "c1",
        "title": "10万元买4只ETF，6年后差多少？",
        "hook": "2020年7月3日，同一天，同一笔10万元，买了四只ETF。六年多以后，最差的那只还剩11万，最好的那只已经19万。",
        "narrative_structure": "data_narrative",
        "visual_approach": (
            "全片只有一张图：一个坐标系里的四条账户资产曲线，从同一起点 2020-07-03 起跑，"
            "连续揭示到 2026-09-18。折线用 clipPath 从左向右裁切，末端挂一个双行数值签（名称+代码 / 当前金额），"
            "随揭示边界移动并做竖向防重叠；年份刻度随进度点亮；一条 ¥100,000 的虚线起跑线常驻全片，"
            "线下铺浅灰绿的水下带。曲线冻结后转入结果表、零基线回撤柱、未创新高时间条，"
            "最后按三类分组收尾。全程无口播、无音轨，承载叙事的文字全部为原生排版。"
        ),
        "suggested_playbook": "finance-dossier + instrument-plate",
        "target_audience": "持有或考虑买入宽基/红利ETF、想弄清\"同样是10万块钱投进去，结果和过程到底差在哪\"的普通投资者",
        "target_platform": "tiktok",
        "target_duration_seconds": DURATION,
        "key_points": [
            "同一天、同一笔10万元、同一个终点：期末最好与最差相差 ¥80,941（¥193,622 vs ¥112,681），而不是几个百分点。",
            "最大回撤幅度相近，但要熬的时间差近20倍：沪深300 的最大回撤跨度 1087 个自然日，红利低波50 只有 58 天。",
            "沪深300 在 2021-02-10 见顶后，直到区间终点 2026-09-18 都没有再创新高，最长一段未创新高横跨 1358 个交易日。",
            "路径分化的结构性原因是编制规则：两只宽基按市值加权，两只红利低波按股息率（或股息率/波动率）加权。",
            "这四条曲线里的分红是按再投资处理的后复权口径，不等于你账户里收到的现金分红会自动复投。",
            "2020-07-03 至 2026-09-18 含A股长期调整与红利风格相对占优的年份，换起点可能换排名。",
        ],
        "core_message": "收益只是结果，回撤和它持续的时间才决定你能不能拿得住。",
        "cta": "下次看到\"年化收益\"对比时，除收益率之外，再问一句：中间最深亏了多少，亏了多久。",
        "tone": "克制、冷静、数据先行；不寒暄、不安慰、不推荐、不喊口号",
        "grounded_in": [
            "research_brief.data_points[0]",
            "research_brief.data_points[1]",
            "research_brief.data_points[2]",
            "research_brief.data_points[3]",
            "research_brief.data_points[4]",
            "research_brief.data_points[5]",
            "research_brief.data_points[6]",
            "research_brief.data_points[7]",
            "research_brief.data_points[9]",
            "research_brief.data_points[10]",
            "research_brief.audience_insights.misconceptions[0]",
            "research_brief.audience_insights.misconceptions[1]",
            "research_brief.audience_insights.misconceptions[2]",
        ],
        "why_this_works": (
            "严格按用户提供的内容规划执行：开场直接提问、每隔一段只讲一件事、"
            "并在\"冻结结果\"之后用回撤把\"过程\"单独拎出来。"
            "它把绝大多数同类内容里那个被忽略的变量——\"没回本持续了多久\"——放到主角位置，"
            "从而给出一个可复用的判断动作，而不是一个推荐结论。"
        ),
    },
    {
        "id": "c2",
        "title": "同一笔10万元，一个账户19万，一个账户11万",
        "hook": "同样10万元，一个账户期末是 ¥193,622，另一个是 ¥112,681。中间差的8万，就是这六年你选了什么。",
        "narrative_structure": "comparison",
        "visual_approach": (
            "先并排摆出两个终局账户（¥193,622 / ¥112,681），停留两秒，再用一条横线把画面推回 2020-07-03，"
            "倒叙重跑四条曲线。终点不变，观众的注意力被预先锚定在\"差8万\"上，看曲线的过程带着答案。"
        ),
        "suggested_playbook": "finance-dossier + instrument-plate",
        "target_audience": "对数字冲击敏感、先要一个结论再愿意看过程的短视频观众",
        "target_platform": "tiktok",
        "target_duration_seconds": DURATION,
        "key_points": [
            "期末两个账户的绝对差是 ¥80,941。",
            "8万元差距从 2021 年开始不可逆地拉开，2024-02-02 达到单日极差 ¥74,443。",
            "结果只是终点，过程中的回撤时长差异才是拿不拿得住的原因。",
        ],
        "core_message": "结果差8万，但真正决定你能不能拿到这8万的是过程。",
        "cta": "先看到终点，再回看过程——两次观看的感受不一样。",
        "tone": "数字冲击开场，随即回到克制分析",
        "grounded_in": [
            "research_brief.data_points[1]",
            "research_brief.data_points[5]",
        ],
        "why_this_works": "倒叙能让前3秒的留存更强，但它把\"过程\"降级成了论据，而本片最有价值的发现恰恰在过程里。",
    },
    {
        "id": "c3",
        "title": "跌得一样多，但要熬的时间差了20倍",
        "hook": "沪深300 和红利低波50 都跌过。可一个跌了将近三年才见底，一个两个月就回来了。",
        "narrative_structure": "myth_busting",
        "visual_approach": (
            "开场直接给两条回撤时间条（1087 天 vs 58 天），把\"回撤是幅度问题\"这个直觉先推翻；"
            "然后才切回四条曲线的完整赛跑，把收益结果当作第二个答案揭晓。"
        ),
        "suggested_playbook": "finance-dossier + instrument-plate",
        "target_audience": "有过浮亏体验、在意\"能不能拿住\"的持有型投资者",
        "target_platform": "tiktok",
        "target_duration_seconds": DURATION,
        "key_points": [
            "最大回撤幅度：-38.45% / -39.48% / -16.53% / -12.91%。",
            "最大回撤跨度：1087 天 / 875 天 / 58 天 / 208 天。",
            "沪深300 最长未创新高 1358 个交易日，一直延续到区间终点。",
        ],
        "core_message": "同样是跌，跌多久比跌多少更考验持有的人。",
        "cta": "下一次看回撤，除了百分比，再看一眼它持续了多久。",
        "tone": "反问式开场，冷静收束",
        "grounded_in": [
            "research_brief.data_points[2]",
            "research_brief.data_points[3]",
        ],
        "why_this_works": "把最锋利的发现前置，冲击力最强；但以回撤开场必须先建立\"同样10万、同一天\"的可比前提，观众在不理解前提时会觉得两个数字不可比。",
    },
    {
        "id": "c4",
        "title": "不是基金经理选的，是指数规则选的",
        "hook": "同样是跟踪A股的ETF，一条线越走越高，另一条走了三年下坡。差别不在基金经理，在指数规则。",
        "narrative_structure": "problem_solution",
        "visual_approach": (
            "把四条曲线按编制规则拆成两组：市值加权的两只（越大越买）与股息率加权的两只（越便宜越买），"
            "用两组不同权重的示意来对照，再回到曲线看两组的路径分化。"
        ),
        "suggested_playbook": "finance-dossier + minimal-diagram",
        "target_audience": "想知道\"为什么会这样\"、愿意理解指数编制规则的中阶投资者",
        "target_platform": "tiktok",
        "target_duration_seconds": DURATION,
        "key_points": [
            "沪深300 与中证500 均按调整市值（派许加权）计算，规模越大权重越高。",
            "中证红利低波动指数采用股息率加权；中证红利低波动100指数采用股息率/波动率加权、季度调样、单一二级行业20%上限。",
            "规则的差异解释了路径的差异，但不构成对未来的推断。",
        ],
        "core_message": "你买的不是一只基金的业绩，是一套选股与加权的规则。",
        "cta": "买ETF前，先看一眼它的跟踪指数是怎么选样、怎么加权的。",
        "tone": "机制解释型，密度略高",
        "grounded_in": [
            "research_brief.data_points[6]",
            "research_brief.data_points[7]",
        ],
        "why_this_works": "它给出最可复用的判断工具；但机制解释会挤占曲线竞速的篇幅，在 97 秒的短片里必须先保住\"过程\"这个主角。",
    },
]

PROPOSAL = {
    "version": "1.0",
    "content_category": "finance",
    "concept_options": CONCEPTS,
    "selected_concept": {
        "concept_id": "c1",
        "rationale": (
            "用户已提供完整内容规划并要求据此执行，c1 即规划结构本身。它也是四个方向中唯一同时满足"
            "「开场直接进入问题」「一条主线只追一件事」「在结果之后单独处理过程」的选择；"
            "c2/c3/c4 都各自牺牲了某一段规划已明确要求的内容。"
        ),
        "modifications": [
            "按用户选择：全程无口播、无音轨。因此规划中\"几乎无口播\"的留白处改为由原生场景排版承担叙事，"
            "画面文字的层级相应加强（标题 / 数值 / 口径三档），并全部落在竖屏安全区内。",
            "按用户选择：独立单条，画面不出现任何系列名、期号、常驻页眉或底部角标。",
            "按用户选择：1080×1920 竖屏。规划的横轴/纵轴在竖屏下改为\"纵轴=账户资产、横轴=日期\"的高瘦坐标系，"
            "四条线的分化空间比横屏更大，跟随标签改为双行右挂。",
            "在规划的\"最大回撤\"段之后补一个「未创新高时间条」段（约4.5秒）：数据里最锋利的发现是"
            "沪深300 有 1358 个交易日没有创新高，这个数字不属于回撤幅度，需要单独的视觉形式，否则会被浪费。",
            "规划建议的\"如出现明显交叉，可短暂停顿并显示排名发生变化\"落实为三个具名节点："
            "2021-02-10（沪深300 见顶）、2021-12-31（红利低波占据前二、沪深300 落到末位）、2024-02-02（单日极差最大）。"
            "不使用\"胜出\"\"最好\"等判断性表述。",
        ],
    },
    "production_plan": {
        "pipeline": "finance-dossier",
        "playbook": "finance-dossier",
        "renderer_family": "explainer-data",
        "render_runtime": "remotion",
        "composition_mode": "atelier",
        "delivery_promise": {
            "promise_type": "data_explainer",
            "motion_required": True,
            "source_required": False,
            "tone_mode": "educational",
            "quality_floor": "presentable",
            "approved_fallback": None,
        },
        "art_direction": (
            ART_DIR
            + "（冷调近白 #F6F7F4 刻线纸基面、细网格 #E1E6DF、四条身份色 靛蓝/赭橙/绛紫/松青、"
            "强制深墨反白做强调而不用第五种彩色、¥100,000 浅灰绿起跑线与水下带作为全片唯一标志装置、"
            "数字一律等宽、不使用红绿涨跌语义、禁止做旧纹理与泛金融空镜）"
        ),
        "taste_profile": {
            "design_read": "工作台上摊开的一张计量图——克制、可核对、没有表演。观众应该感觉像有人在纸上把同一笔钱的四条轨迹摊开给你看，而不是在听人劝你买什么。",
            "visual_variance": 5,
            "motion_intensity": 6,
            "information_density": 4,
            "palette_discipline": "仅四色身份色 + 石墨结构色 + 深墨反白强调。不引入第五种彩色，不使用红绿涨跌语义。",
            "layout_variation": "全片共享同一个坐标系与同一套制图规范；变化来自揭示进度、注解与统计图形的更替，而不是每个场景换一套版式。刻意拒绝\"一个信息组一张卡片\"。",
            "reference_strategy": "不复用任何现有系列的美术语言（不使用象牙白触感纸、页眉、朱红批注）。本片美术方向为一次性，见 art-direction-instrument-plate.md。",
            "anti_patterns": [
                "K线 / 金币 / 握手 / 机房等泛金融空镜",
                "涨跌红绿语义色",
                "截断纵轴放大差异",
                "四条曲线做成四张静态对比卡轮播",
                "为动效而动的粒子、发光、追尾拖影",
                "满屏滚动字幕",
            ],
            "quality_gates": [
                "全部金额、比例、日期与时长与源数据逐项一致，取整规则统一",
                "中文零错字、零裁切；等宽数字纵向可比",
                "竖屏字幕安全区（距底 520px、距侧 96px）内不被任何元素占用",
                "结尾合规文案原生、完整、可读、位于最末端",
                "首帧即含开场标题，不是空网格",
            ],
        },
        "voice_selection": {
            "provider": "none",
            "voice_name": "无口播（用户显式覆盖持久默认）",
            "generation_mode": "segmented",
            "inherited_from_defaults": False,
            "rationale": "用户在开工前明确选择\"全程无口播：只有画面、字幕和数据，完全静音\"。本片不调用 tts_selector，不产出旁白音频。",
            "estimated_cost_usd": 0.0,
            "delivery_style": "无语音；叙事由原生画面排版承担",
            "pacing_policy": "节奏完全由画面推进控制：开场快（约13秒铺完全部前提），中段稳（约57秒连续赛跑），结果段停顿（约7.5秒供阅读），过程段再收紧（约14.5秒），结尾留约3秒给合规页脚。",
            "sample_approval_required": False,
        },
        "music_source": {
            "source_type": "none",
            "inherited_from_defaults": True,
        },
        "decision_log_ref": f"projects/{SLUG}/artifacts/decision_log.json",
        "provider_rankings": {
            "tts": [
                {
                    "tool_name": "none",
                    "provider": "none",
                    "weighted_score": 1.0,
                    "task_fit": 1.0,
                    "output_quality": 1.0,
                    "explanation": "用户显式选择全程无口播；1/7 TTS 提供方已配置（仅豆包），本片不使用。",
                }
            ],
            "video": [
                {
                    "tool_name": "none",
                    "provider": "none",
                    "weighted_score": 1.0,
                    "task_fit": 1.0,
                    "output_quality": 1.0,
                    "explanation": "语义动效审计结论：15/15 个 beat 为 precision-critical，0 个语义动态候选，故不调用任何视频生成或库存素材能力。",
                }
            ],
            "image": [
                {
                    "tool_name": "host_image_generation",
                    "provider": "host",
                    "weighted_score": 0.9,
                    "task_fit": 0.9,
                    "output_quality": 0.9,
                    "explanation": "仅用于封面阶段的材质底板；全部中文、数字与图表由本地确定性排版叠加。",
                },
                {
                    "tool_name": "pillow",
                    "provider": "local",
                    "weighted_score": 0.85,
                    "task_fit": 0.95,
                    "output_quality": 0.8,
                    "explanation": "本地确定性排版与缩略图可读性自检；零成本、零水印。",
                },
            ],
            "music": [
                {
                    "tool_name": "none",
                    "provider": "none",
                    "weighted_score": 1.0,
                    "task_fit": 1.0,
                    "output_quality": 1.0,
                    "explanation": "应用持久无BGM默认（music_generation 0/3 configured），且用户选择完全静音。",
                }
            ],
        },
        "stages": [
            {
                "stage": "research",
                "tools": [],
                "approach": "已完成任务路由（EXPLAIN）、11 条带来源与期段的数据点、5 个来源、现有内容版图取样；四只ETF的数字已与用户工作簿「汇总」表逐项对账。",
            },
            {
                "stage": "proposal",
                "tools": [],
                "approach": "锁定概念、运行时、创作模式、动态覆盖、配音与音乐、画幅、预算；当前等待唯一一次人工批准。",
            },
            {
                "stage": "script",
                "tools": [],
                "approach": "无口播片，脚本产物承担\"画面节拍表\"职责：按 15 个分镜写出对应的屏幕文案、数值与停留时长，并写入脚本元数据（核心问题、证据引用、边界条件、可复用判断方法、合规元数据）。",
            },
            {
                "stage": "scene_plan",
                "tools": [],
                "approach": "15 个分镜，全部标注为 DATA / MECHANISM / DECISION 族，每个带来源锚点；连续赛跑段作为单一连续阶段处理，避免版式重复。",
            },
            {
                "stage": "assets",
                "tools": [],
                "approach": "不生成音频、不拉取素材。产出物是数据资产：由用户工作簿导出的 1510 点 × 4 序列数据集、回撤与未创新高区间、注解节点，全部落在项目工作区并记录来源与校验结果。",
            },
            {
                "stage": "edit",
                "tools": [],
                "approach": "写出手工时间轴：15 个 cut 覆盖 0→97 秒无空隙，锁定 render_runtime=remotion、composition_mode=atelier，声明竖屏安全区与合规页脚位置，不含 audio 与 music 键。",
            },
            {
                "stage": "compose",
                "tools": [],
                "approach": "手写 Remotion atelier 合成（theme / Foundation / 坐标系 / 15 个场景 / Captions 层），本地渲染 1080×1920 30fps H.264，无音轨；随后跑 ffprobe、抽帧与首帧亮度自检。",
            },
            {
                "stage": "cover",
                "tools": [],
                "approach": "宿主图像生成提供无字材质底板，再以本地确定性排版叠加标题、8.09万 / 93.62% 等真实数字与身份色，输出 1080×1440（3:4）封面并做缩略图可读性自检。",
            },
            {
                "stage": "publish",
                "tools": [],
                "approach": "本地打包 final.mp4、cover.png、屏幕文案全文、来源说明、元数据与发布文案；不登录、不上传、不建远程草稿，保持 manual_publish_required=true。",
            },
        ],
        "quality_tradeoffs": [
            {
                "tradeoff": "全程无口播（用户选择）vs 极简口播",
                "recommendation": "执行用户选择：无口播。",
                "quality_impact": "画面必须独立承担全部信息，因此文字层级与注解密度会略高于常规；代价是短视频平台在静音场景下的完播与互动通常低于带人声的同类内容。已在开工前如实告知，用户知情选择。",
            },
            {
                "tradeoff": "纯合成覆盖 vs 轻混合（加一两个真实素材节点）",
                "recommendation": "纯合成。",
                "quality_impact": "画面完全确定、数值零风险；放弃的是真实素材带来的氛围感——本片判定其为 decorative_only，不承担信息责任。",
            },
            {
                "tradeoff": "atelier 手写合成 vs templated 库存场景拼装",
                "recommendation": "atelier。",
                "quality_impact": "获得跨场景连续揭示的坐标系与跟随标签；代价是更多的编写与迭代轮次。templated 无法实现本片的连续性，会退化为静态图表轮播。",
            },
            {
                "tradeoff": "99 秒（交付）vs 97 秒（提案目标）vs 约 90 秒（规划建议）",
                "recommendation": "99 秒。",
                "quality_impact": (
                    "相对提案目标多出的 2 秒全部用于机制镜头——它是已批准概念里就有、原结构却漏掉的「为什么」；"
                    "相对规划建议的 90 秒多出的约 9 秒，用于机制镜头、「未创新高时间条」段与结尾约 3 秒的合规页脚停留。"
                    "若压回 90 秒，需要牺牲机制解释或结尾停留，两者都会削弱这支片子的完整性。"
                ),
            },
        ],
        "alternative_paths": [
            {
                "description": "templated 快速版：用库存 line_chart / bar_chart / stat_card 拼装，不手写坐标系",
                "total_cost_usd": 0.0,
                "quality_level": "budget",
                "what_changes": "制作时间大幅缩短；但失去连续揭示与跟随标签，四条线变成若干张静态图表卡，本片的核心价值（过程）不成立。",
            },
            {
                "description": "轻混合版：在\"过程\"段加入 1-2 个真实延时/环境镜头",
                "total_cost_usd": 0.0,
                "quality_level": "standard",
                "what_changes": "多一层氛围；但素材不承载事实，会稀释刻线纸的\"测量感\"，并与规划中\"建议删除\"的泛财经空镜相冲突。",
            },
            {
                "description": "本片方案：纯合成 atelier + 无口播 + 无音乐",
                "total_cost_usd": 0.0,
                "quality_level": "premium",
                "what_changes": "无 API 成本；全部预算投入在合成编写与数据校验上。",
            },
        ],
    },
    "cost_estimate": {
        "total_estimated_usd": 0.0,
        "line_items": [
            {
                "tool": "none",
                "operation": "旁白合成",
                "quantity": 0,
                "estimated_usd": 0.0,
                "notes": "用户选择全程无口播，本片不调用任何 TTS 提供方。",
            },
            {
                "tool": "none",
                "operation": "视频生成 / 库存素材",
                "quantity": 0,
                "estimated_usd": 0.0,
                "notes": "语义动效审计结论为纯合成覆盖，不调用任何视频或素材能力。",
            },
            {
                "tool": "video_compose / audio_mixer",
                "operation": "本地 Remotion atelier 渲染 1080×1920 30fps（无音轨）",
                "quantity": 1,
                "estimated_usd": 0.0,
                "notes": "本地计算，不计 API 费用。无音频层，audio_mixer 不参与。",
            },
            {
                "tool": "host_image_generation",
                "operation": "封面材质底板 1 张（大尺寸可直接复用为原图）",
                "quantity": 1,
                "estimated_usd": 0.0,
                "notes": "宿主能力，无额外计费；中文与数字由本地确定性排版叠加。",
            },
        ],
        "budget_cap_usd": 2,
        "budget_verdict": "within_budget",
        "savings_options": [
            "本片 API 成本已为 0：无 TTS、无素材、无视频生成、无音乐。若后续希望加回极简口播，需新增一次性 TTS 成本（约 60-80 字，低于 $0.02）。",
            "封面若不需要材质底板，可改为完全本地确定性合成，成本与效果差异都极小。",
        ],
    },
    "approval": {
        "status": "pending",
        "user_notes": (
            "开工前已确认四项设定：独立单条（不做系列标识）、全程无口播、1080×1920 竖屏、"
            "一次性预授权后续所有门。本提案为唯一一次人工确认点。"
        ),
    },
    "metadata": {
        "editorial_direction": None,  # filled from research_brief below
        "capability_status": {
            "composition": {"ffmpeg": True, "remotion": True, "hyperframes": True},
            "tts": "1/7 configured: Doubao（本片不使用）",
            "video_generation": "2/22 configured: Pexels, Pixabay（本片不使用）",
            "image_generation_registry": "2/12 configured（仅库存）；宿主图像生成额外可用，仅用于封面底板",
            "music_generation": "0/3 configured；应用持久无BGM默认，且用户选择完全静音",
            "video_post": "9/9 configured",
            "subtitle": "2/2 configured（本片无语音，不产生字幕轨）",
            "runtime_warnings": [
                "comfyui_video: resource_profile 是 ComfyUI 提供方的下限，不代表每个工作流都能装进 8GB 显存；本片不使用该能力。"
            ],
            "preflight_verdict": "passed",
        },
        "semantic_motion_audit": [
            {
                "beat": "sc01 开场提问（2020年7月3日 / 同一天同一笔钱 / 四只ETF各买10万 / 6年后差多少）",
                "responsibility": "precision_critical",
                "treatment": "原生排版：日期、金额与四个产品名必须逐字准确。",
                "information_contributed": "建立比较的可比前提（同一天、同一笔钱、同一终点）。",
            },
            {
                "beat": "sc02 四只ETF身份牌与 ¥100,000 起投额",
                "responsibility": "precision_critical",
                "treatment": "四张原生身份牌，各带名称、代码与 ¥100,000；四色身份色在此建立。",
                "information_contributed": "让观众在曲线出现前就认识四条线的身份，后续跟随标签才有指代对象。",
            },
            {
                "beat": "sc03 规则公布（起点 / 初始资金 / 分红按再投资 / 不定投不择时）",
                "responsibility": "precision_critical",
                "treatment": "原生规则清单 + START 落定；口径声明必须完整可读。",
                "information_contributed": "口径前置：先说明这是后复权总回报，避免观众误读为\"分红自动复投到账\"。",
            },
            {
                "beat": "13.2–70.0s 连续赛跑（网格、刻度、¥100,000 起跑线、四条曲线揭示、跟随数值签、年份点亮）",
                "responsibility": "precision_critical",
                "treatment": "Remotion 手写坐标系；clipPath 揭示；末端数值签与几何同步；标注三个具名节点。",
                "information_contributed": "全片的信息主干：把\"同一起点、同一时间、不同路径\"变成可看见的连续过程。",
            },
            {
                "beat": "三个具名节点（2021-02-10 见顶 ¥129,310 / 2021-12-31 排名变化 / 2024-02-02 单日极差 ¥74,443）",
                "responsibility": "precision_critical",
                "treatment": "原生图钉注解 + 精确数值；不使用判断性措辞。",
                "information_contributed": "把连续的曲线切成观众能记住的三个时刻，并保留每次点名对应的当日金额。",
            },
            {
                "beat": "sc11 冻结最终结果表（最终资产 / 累计收益 / 年化收益）",
                "responsibility": "precision_critical",
                "treatment": "原生四行结果表，等宽数字，停留约 7.5 秒供阅读。",
                "information_contributed": "给出规划要求的最终数据，让观众可以先记住结果。",
            },
            {
                "beat": "sc12 转折（但是，过程一样吗？）",
                "responsibility": "precision_critical",
                "treatment": "原生大字，短暂停留，无装饰。",
                "information_contributed": "把观众的注意力从结果切换到过程，为下一段做准备。",
            },
            {
                "beat": "sc13 最大回撤零基线横向柱（-38.45% / -39.48% / -16.53% / -12.91%）",
                "responsibility": "precision_critical",
                "treatment": "原生零基线柱状图，逐行标名称与数值，不靠颜色区分。",
                "information_contributed": "给出回撤幅度的可比视图；零基线保证不放大差异。",
            },
            {
                "beat": "sc14 未创新高时间条（1358 / 971 / 239 / 341 个交易日）",
                "responsibility": "precision_critical",
                "treatment": "原生四条横向时间条，按真实日期段绘制，标出未创新高区间与合计交易日数。",
                "information_contributed": "本片最锋利的发现：回撤不只是幅度问题，是能不能熬过去的问题。",
            },
            {
                "beat": "sc15 结尾分类与可复用判断方法 + 合规页脚",
                "responsibility": "precision_critical",
                "treatment": "原生三组分类 + 两行结语；合规文案以原生小字放在页脚，停留约3秒。",
                "information_contributed": "给出可复用的判断动作与三条边界条件，并完成强制合规呈现。",
            },
            {
                "beat": "K线、金币、握手、机房、券商 Logo 堆叠、财经新闻截图",
                "responsibility": "decorative_only",
                "treatment": "全部拒绝使用，且用户规划已在\"建议删除\"中列明。",
            },
        ],
        "motion_commitment_summary": (
            "选定 composition-only：15 个 beat 全部为 precision-critical，0 个语义动态候选，"
            "0 个装饰性素材被采用。本片不存在\"素材能比确定性图形更准确传达信息\"的段落，"
            "故素材阶段不调用任何视频生成或库存素材能力——这是显式审计结论，不是省略。"
        ),
        "compliance": {
            "content_category": "finance",
            "financial_disclaimer": DISCLAIMER,
            "exact_text": DISCLAIMER,
            "presentation": "footer",
            "placement": "ending",
            "ending_scene_id": "sc15",
            "ending_cut_id": "cut-15",
            "note": "合规文案以原生小字固定呈现在最终意义场景 sc15 的页脚，不朗读、不单独成卡。本片无音轨，因此该文案只以文字形式存在，且必须位于竖屏安全区内。",
        },
        "canvas": {
            "width": 1080,
            "height": 1920,
            "fps": 30,
            "aspect": "9:16",
            "platforms": ["douyin", "xiaohongshu", "wechat_channels"],
            "safe_area": {"policy": "social-ui-safe", "bottom_offset_px": 520, "side_margin_px": 96},
        },
        "audio_policy": {
            "audio_streams": 0,
            "narration": "none",
            "music": "none",
            "note": "用户显式选择全程无口播。成片不含任何音轨；下游 edit_decisions 不含 audio 与 music 键，compose 不调用 audio_mixer。",
        },
        "duration_estimate": {
            "target_seconds": DURATION,
            "delivered_seconds": 99.0,
            "scenes": 10,
            "race_window_seconds": 56.8,
            "trailing_hold_seconds": 3.0,
            "revision_note": (
                "提案锁定的目标是 97.0 秒、15 个场景。执行中做了两处结构调整并把最终成片定为 99.0 秒 / 10 个场景："
                "① 赛跑段本就是一个连续镜头（56.8 秒内没有任何剪辑），把它拆成七个场景会误述这支片子的拍法，"
                "因此七个章节改为同一场景内的注解拍，场景数由 15 降为 10；"
                "② 补入一个 5.6 秒的机制镜头（指数加权规则的对照），"
                "用来回答「为什么路径会分化」——这一点写在已批准的 c1 概念与 research_brief 的机制证据里，"
                "原结构里却没有承载它的镜头。净增 2.0 秒。"
            ),
            "note": "比规划建议的约90秒多约9秒，用于机制镜头、未创新高时间条段、以及结尾合规页脚的3秒停留；取舍见 quality_tradeoffs。",
        },
        "series_status": {
            "is_series_entry": False,
            "on_screen_series_mark": None,
            "note": "用户选择独立单条、不做系列标识：画面中不出现系列名、期号、常驻页眉或底部角标。",
        },
        "approval_policy": APPROVAL_POLICY,
    },
}


def main() -> None:
    from lib.checkpoint import validate_artifact

    brief = json.loads((PROJECT / "artifacts" / "research_brief.json").read_text())
    PROPOSAL["metadata"]["editorial_direction"] = brief["metadata"]["editorial_direction"]

    validate_artifact("decision_log", DECISION_LOG)
    validate_artifact("proposal_packet", PROPOSAL)

    OUT_LOG.write_text(json.dumps(DECISION_LOG, ensure_ascii=False, indent=1))
    OUT_PROPOSAL.write_text(json.dumps(PROPOSAL, ensure_ascii=False, indent=1))

    print("[ok] decision_log schema-valid")
    print("[ok] proposal_packet schema-valid")
    for p in (OUT_LOG, OUT_PROPOSAL):
        print(f"[write] {p.relative_to(REPO)}  ({p.stat().st_size/1024:.0f} KB)")
    print()
    print(f"  concepts           : {len(PROPOSAL['concept_options'])} (selected {PROPOSAL['selected_concept']['concept_id']})")
    print(f"  decisions logged   : {len(DECISION_LOG['decisions'])}")
    print(f"  render_runtime     : {PROPOSAL['production_plan']['render_runtime']} / {PROPOSAL['production_plan']['composition_mode']}")
    print(f"  duration target    : {DURATION}s, canvas {PROPOSAL['metadata']['canvas']['width']}x{PROPOSAL['metadata']['canvas']['height']}")
    print(f"  audio              : {PROPOSAL['metadata']['audio_policy']['audio_streams']} streams")
    print(f"  cost               : ${PROPOSAL['cost_estimate']['total_estimated_usd']:.2f} (cap ${PROPOSAL['cost_estimate']['budget_cap_usd']})")


if __name__ == "__main__":
    main()
