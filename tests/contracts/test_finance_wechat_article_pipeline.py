"""Contracts for the finance-video → WeChat article derivative branch."""

from __future__ import annotations

from pathlib import Path

import pytest

from backlot.state import load_board_state
from lib.checkpoint import CheckpointValidationError, get_next_stage, init_project, write_checkpoint
from lib.pipeline_loader import get_stage_order, load_pipeline
from lib.wechat_editorial import WECHAT_FINANCE_DISCLAIMER
from schemas.artifacts import ARTIFACT_NAMES, validate_artifact
from tools.graphics.finance_chart import FinanceChart
from tools.publishers.wechat_article_bundle import WechatArticleBundle


ROOT = Path(__file__).resolve().parents[2]


def source_analysis() -> dict:
    return {
        "version": "1.0",
        "content_category": "finance",
        "source": {
            "kind": "openmontage_project",
            "project_id": "source-finance-video",
            "artifacts_used": ["script", "research_brief"],
        },
        "core_question": "高股息是否必然带来更高收益？",
        "video_summary": "视频用一个历史分组结果说明高股息与未来收益并不存在简单线性关系。",
        "video_coverage": {
            "conclusions": ["高股息不等于高收益"],
            "evidence_shown": ["展示了一张五分组收益图"],
            "omitted_depth": ["样本筛选", "收益计算口径", "局限性"],
            "time_sensitivity": "evergreen",
            "mandatory_disclaimer_present": True,
        },
        "expansion_opportunities": [
            {"kind": "method", "description": "补全分组方法", "article_value": "可复核"},
            {"kind": "boundary", "description": "解释幸存者偏差", "article_value": "避免误读"},
        ],
    }


def content_screen(action: str = "write") -> dict:
    return {
        "version": "1.0",
        "source_ref": "wechat_source_analysis",
        "factors": {
            "evergreen_value": {"answer": True, "score": 1, "evidence": "长期投资问题"},
            "unfinished_depth": {"answer": True, "score": 1, "evidence": "方法未展开"},
            "evidence_value": {"answer": True, "score": 1, "evidence": "图表与计算可保存"},
            "series_fit": {"answer": True, "score": 1, "evidence": "可进入财经数据实验室"},
        },
        "total_score": 4,
        "selection_band": "strongly_recommended",
        "content_priority": "data_validation",
        "article_tier": "A_core_research",
        "series_name": "财经数据实验室",
        "approved_action": action,
        "rationale": "问题具备长期价值，且短视频未完整保留方法、数据口径和研究局限。",
        "upgrade_path": {"can_upgrade": False, "upgraded_question": None, "upgrade_notes": []},
        "extended_checklist": {
            "searchable": True,
            "adds_information": True,
            "supports_positioning": True,
            "upgrades_hotspot_to_evergreen": False,
        },
    }


def skip_screen() -> dict:
    data = content_screen("skip")
    for name in data["factors"]:
        data["factors"][name] = {"answer": False, "score": 0, "evidence": "仅当日情绪表达"}
    data.update({
        "total_score": 0,
        "selection_band": "not_recommended",
        "content_priority": "emotion_only",
        "article_tier": None,
        "series_name": None,
        "rationale": "内容只针对当日行情进行情绪表达，没有可继续验证的数据、方法或长期问题。",
    })
    return data


def full_checklist() -> dict:
    return {
        "clear_question": True,
        "evergreen_value": True,
        "adds_beyond_video": True,
        "conclusion_early": True,
        "sources_noted": True,
        "as_of_date_noted": True,
        "method_explained": True,
        "limitations_explained": True,
        "charts_mobile_readable": True,
        "terms_explained": True,
        "no_text_wall": True,
        "series_linked": True,
        "exact_disclaimer": True,
    }


def test_manifest_and_skills_are_complete():
    manifest = load_pipeline("finance-wechat-article")
    assert manifest["deliverable_type"] == "article"
    assert get_stage_order(manifest) == [
        "source_analysis", "screening", "evidence", "drafting", "visuals", "packaging"
    ]
    assert manifest["stages"][1]["halt_when"]["equals_any"] == ["skip"]
    for stage in manifest["stages"]:
        assert stage["primary_artifact"] in ARTIFACT_NAMES
        assert (ROOT / "skills" / f"{stage['skill']}.md").is_file()


def test_screening_score_is_semantically_enforced():
    validate_artifact("wechat_content_screen", content_screen())
    invalid = content_screen()
    invalid["total_score"] = 3
    with pytest.raises(ValueError, match="factor sum"):
        validate_artifact("wechat_content_screen", invalid)


def test_low_score_cannot_write_without_upgrade():
    invalid = skip_screen()
    invalid["approved_action"] = "write"
    with pytest.raises(ValueError, match="cannot go straight"):
        validate_artifact("wechat_content_screen", invalid)


def test_skip_is_a_resumable_terminal_outcome(tmp_path):
    project_id = "skip-finance-article"
    init_project(project_id, title="Skip", pipeline_type="finance-wechat-article", pipeline_dir=tmp_path)
    write_checkpoint(
        tmp_path, project_id, "source_analysis", "completed",
        {"wechat_source_analysis": source_analysis()}, pipeline_type="finance-wechat-article",
    )
    write_checkpoint(
        tmp_path, project_id, "screening", "completed",
        {"wechat_content_screen": skip_screen()}, pipeline_type="finance-wechat-article",
        human_approved=True,
    )
    assert get_next_stage(tmp_path, project_id, "finance-wechat-article") is None
    board = load_board_state(tmp_path / project_id)
    statuses = {stage["name"]: stage["status"] for stage in board["stages"]}
    assert statuses["screening"] == "completed"
    assert statuses["evidence"] == "not_applicable"
    assert statuses["packaging"] == "not_applicable"


def test_primary_artifact_is_required_for_custom_stage(tmp_path):
    project_id = "missing-artifact"
    init_project(project_id, title="Missing", pipeline_type="finance-wechat-article", pipeline_dir=tmp_path)
    with pytest.raises(CheckpointValidationError, match="wechat_source_analysis"):
        write_checkpoint(
            tmp_path, project_id, "source_analysis", "completed", {},
            pipeline_type="finance-wechat-article",
        )


def test_finance_chart_writes_phone_readable_png(tmp_path):
    output = tmp_path / "chart.png"
    result = FinanceChart().execute({
        "chart_type": "bar",
        "title": "高股息组并没有持续获得最高收益",
        "series": [{
            "name": "未来一年收益",
            "values": [
                {"label": "低股息", "value": 5.2},
                {"label": "中股息", "value": 7.1},
                {"label": "高股息", "value": 6.0},
            ],
        }],
        "unit": "%",
        "source_note": "数据来源：测试数据；区间：2016—2026",
        "output_path": str(output),
    })
    assert result.success, result.error
    assert output.is_file()
    assert result.data["width"] >= 640


def test_local_bundle_never_publishes_and_keeps_exact_disclaimer(tmp_path):
    article = tmp_path / "draft.md"
    cover = tmp_path / "cover.png"
    figure = tmp_path / "figure.png"
    article.write_text("# 标题\n\n正文\n\n" + WECHAT_FINANCE_DISCLAIMER, encoding="utf-8")
    cover.write_bytes(b"cover")
    figure.write_bytes(b"figure")

    result = WechatArticleBundle().execute({
        "title": "高股息是否必然带来更高收益？",
        "article_markdown_path": str(article),
        "cover_path": str(cover),
        "image_paths": [str(figure)],
        "source_notes": "数据来源：测试",
        "checklist": full_checklist(),
        "disclaimer": WECHAT_FINANCE_DISCLAIMER,
        "output_dir": str(tmp_path / "deliverables" / "wechat"),
    })
    assert result.success, result.error
    package = result.data["wechat_article_package"]
    assert package["manual_publish_required"] is True
    assert package["platform"] == "wechat_official_account"
    assert package["status"] == "ready"
    assert Path(package["manifest_path"]).is_file()
