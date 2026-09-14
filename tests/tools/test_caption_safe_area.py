"""Cross-runtime contract for portrait social caption placement."""

from lib.media_profiles import (
    INSTAGRAM_REELS,
    TIKTOK,
    YOUTUBE_SHORTS,
    resolve_caption_safe_area,
)
from tools.video.video_compose import VideoCompose


def test_all_portrait_social_profiles_share_one_caption_lane():
    for profile in (TIKTOK, INSTAGRAM_REELS, YOUTUBE_SHORTS):
        assert profile.caption_safe_area is not None
        assert profile.caption_safe_area.policy == "social-ui-safe"
        assert profile.caption_safe_area.bottom_px == 520
        assert profile.caption_safe_area.side_px == 96


def test_custom_portrait_canvas_scales_the_safe_area():
    safe = resolve_caption_safe_area(720, 1280)
    assert safe is not None
    assert safe.bottom_px == 347
    assert safe.side_px == 64


def test_landscape_canvas_does_not_force_portrait_clearance():
    assert resolve_caption_safe_area(1920, 1080) is None


def test_ffmpeg_caption_style_is_clamped_for_portrait():
    style = VideoCompose._apply_caption_safe_area(
        {"margin_v": 40, "margin_l": 10, "margin_r": 10},
        width=1080,
        height=1920,
    )
    assert style["margin_v"] == 520
    assert style["margin_l"] == 96
    assert style["margin_r"] == 96


def test_larger_project_specific_clearance_is_preserved():
    style = VideoCompose._apply_caption_safe_area(
        {"margin_v": 600, "margin_l": 120, "margin_r": 140},
        width=1080,
        height=1920,
    )
    assert style["margin_v"] == 600
    assert style["margin_l"] == 120
    assert style["margin_r"] == 140


def test_ass_style_serializes_vertical_and_side_margins():
    ass = VideoCompose._build_subtitle_style(
        {"margin_v": 520, "margin_l": 96, "margin_r": 96}
    )
    assert "MarginV=520" in ass
    assert "MarginL=96" in ass
    assert "MarginR=96" in ass
