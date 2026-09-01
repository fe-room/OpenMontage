"""Persistent narration defaults must survive selector routing."""

from __future__ import annotations

from tools.audio.tts_selector import TTSSelector
from tools.base_tool import ToolResult, ToolStatus


class _FakeDoubao:
    name = "doubao_tts"
    provider = "doubao"

    def __init__(self):
        self.received = None

    def execute(self, inputs):
        self.received = inputs
        return ToolResult(success=True, data={"output_path": "narration.mp3"})

    def get_status(self):
        return ToolStatus.AVAILABLE

    def get_info(self):
        return {"agent_skills": [], "usage_location": "test", "best_for": []}


def test_selector_inherits_dayi_and_doubao_defaults(monkeypatch):
    selector = TTSSelector()
    provider = _FakeDoubao()
    monkeypatch.setattr(selector, "_providers", lambda: [provider])
    monkeypatch.setattr(
        selector,
        "_select_best_tool",
        lambda inputs, candidates, context: (provider, None),
    )

    result = selector.execute({"text": "默认配音测试"})

    assert result.success
    assert provider.received["preferred_provider"] == "doubao"
    assert provider.received["voice_id"] == "zh_male_dayi_uranus_bigtts"
    assert provider.received["resource_id"] == "seed-tts-2.0"
    assert provider.received["speech_rate"] == 0
    assert provider.received["api_mode"] == "unidirectional"
    assert provider.received["max_chars_per_request"] == 400


def test_explicit_project_voice_override_wins(monkeypatch):
    selector = TTSSelector()
    provider = _FakeDoubao()
    monkeypatch.setattr(selector, "_providers", lambda: [provider])
    monkeypatch.setattr(
        selector,
        "_select_best_tool",
        lambda inputs, candidates, context: (provider, None),
    )

    selector.execute(
        {
            "text": "单项目覆盖测试",
            "preferred_provider": "doubao",
            "voice_id": "custom_voice",
            "resource_id": "custom_resource",
            "speech_rate": 12,
        }
    )

    assert provider.received["voice_id"] == "custom_voice"
    assert provider.received["resource_id"] == "custom_resource"
    assert provider.received["speech_rate"] == 12


def test_dayi_voice_does_not_leak_to_another_provider():
    selector = TTSSelector()
    resolved = selector._apply_selected_provider_defaults(
        {"text": "fallback", "preferred_provider": "piper"},
        "piper",
    )

    assert "voice_id" not in resolved
    assert "resource_id" not in resolved
    assert "speech_rate" not in resolved
