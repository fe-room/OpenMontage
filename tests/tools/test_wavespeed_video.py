"""Contract and mocked API coverage for the WaveSpeedAI video provider."""

from __future__ import annotations

from pathlib import Path

from tools.base_tool import ToolStatus
from tools.video.wavespeed_video import WaveSpeedVideo


class _Response:
    def __init__(self, body=None, content=b""):
        self._body = body
        self.content = content

    def raise_for_status(self):
        return None

    def json(self):
        return self._body


def test_wavespeed_video_contract(monkeypatch):
    monkeypatch.delenv("WAVESPEED_API_KEY", raising=False)
    monkeypatch.setenv("WAVESPEED_VIDEO_MODEL", "wavespeed-ai/wan-2.2/i2v-480p-ultra-fast")
    tool = WaveSpeedVideo()

    assert tool.provider == "wavespeed"
    assert tool.capability == "video_generation"
    assert tool.supports["image_to_video"] is True
    assert tool.supports["text_to_video"] is True
    assert tool.get_status() == ToolStatus.UNAVAILABLE
    assert tool.estimate_cost({"duration": 5}) == 0.05
    assert tool.estimate_cost({"duration": 8}) == 0.08


def test_wavespeed_model_comes_from_environment(monkeypatch):
    monkeypatch.setenv("WAVESPEED_VIDEO_MODEL", "wavespeed-ai/wan-2.2/i2v-480p-ultra-fast")
    assert WaveSpeedVideo._model({}) == "wavespeed-ai/wan-2.2/i2v-480p-ultra-fast"


def test_wavespeed_t2v_contract_comes_from_environment(monkeypatch):
    monkeypatch.setenv("WAVESPEED_API_KEY", "test-key")
    monkeypatch.setenv("WAVESPEED_VIDEO_MODEL", "wavespeed-ai/wan-2.2/t2v-5b-720p")
    tool = WaveSpeedVideo()

    info = tool.get_info()
    assert info["configured_model"] == "wavespeed-ai/wan-2.2/t2v-5b-720p"
    assert info["supports"]["text_to_video"] is True
    assert info["supports"]["image_to_video"] is False
    assert info["pricing"]["estimated_cost_usd"] == 0.05
    assert info["output_profile"]["duration_seconds"] == 5
    assert tool.is_operation_available("text_to_video") is True
    assert tool.is_operation_available("image_to_video") is False
    assert tool.estimate_cost({}) == 0.05


def test_wavespeed_t2v_submit_poll_and_download(monkeypatch, tmp_path):
    import requests

    calls = {"posts": [], "gets": []}
    output_path = tmp_path / "clip.mp4"

    def post(url, **kwargs):
        calls["posts"].append((url, kwargs))
        return _Response(
            {
                "code": 200,
                "data": {
                    "id": "prediction-t2v",
                    "status": "created",
                    "urls": {"get": "https://api.test/result"},
                },
            }
        )

    class Session:
        def mount(self, *args, **kwargs):
            return None

        def get(self, url, **kwargs):
            calls["gets"].append((url, kwargs))
            if url == "https://api.test/result":
                return _Response(
                    {
                        "code": 200,
                        "data": {
                            "id": "prediction-t2v",
                            "status": "completed",
                            "outputs": ["https://cdn.test/video.mp4"],
                        },
                    }
                )
            return _Response(content=b"fake mp4")

    monkeypatch.setattr(requests, "post", post)
    monkeypatch.setattr(requests, "Session", Session)
    monkeypatch.setenv("WAVESPEED_API_KEY", "test-key")
    monkeypatch.setenv("WAVESPEED_VIDEO_MODEL", "wavespeed-ai/wan-2.2/t2v-5b-720p")
    monkeypatch.setattr("tools.video._shared.probe_output", lambda path: {"probed": True})

    result = WaveSpeedVideo().execute(
        {
            "prompt": "A red dividend yield certificate fractures in mid-air",
            "operation": "text_to_video",
            "size": "720*1280",
            "output_path": str(output_path),
        }
    )

    assert result.success, result.error
    assert result.model == "wavespeed-ai/wan-2.2/t2v-5b-720p"
    assert result.cost_usd == 0.05
    assert calls["posts"][0][1]["json"] == {
        "prompt": "A red dividend yield certificate fractures in mid-air",
        "seed": -1,
        "size": "720*1280",
    }


def test_wavespeed_upload_submit_poll_and_download(monkeypatch, tmp_path):
    import requests

    calls = {"posts": [], "gets": []}
    image_path = tmp_path / "first.png"
    image_path.write_bytes(b"png")
    output_path = tmp_path / "clip.mp4"

    def post(url, **kwargs):
        calls["posts"].append((url, kwargs))
        if url.endswith("/media/upload/binary"):
            return _Response({"code": 200, "data": {"download_url": "https://cdn.test/input.png"}})
        return _Response(
            {
                "code": 200,
                "data": {
                    "id": "prediction-1",
                    "status": "created",
                    "urls": {"get": "https://api.test/result"},
                },
            }
        )

    class Session:
        def mount(self, *args, **kwargs):
            return None

        def get(self, url, **kwargs):
            calls["gets"].append((url, kwargs))
            if url == "https://api.test/result":
                return _Response(
                    {
                        "code": 200,
                        "data": {
                            "id": "prediction-1",
                            "status": "completed",
                            "outputs": ["https://cdn.test/video.mp4"],
                        },
                    }
                )
            return _Response(content=b"fake mp4")

    monkeypatch.setattr(requests, "post", post)
    monkeypatch.setattr(requests, "Session", Session)
    monkeypatch.setenv("WAVESPEED_API_KEY", "test-key")
    monkeypatch.setenv("WAVESPEED_VIDEO_MODEL", "wavespeed-ai/wan-2.2/i2v-480p-ultra-fast")
    monkeypatch.setattr("tools.video._shared.probe_output", lambda path: {"probed": True})

    result = WaveSpeedVideo().execute(
        {
            "prompt": "The subject turns toward camera",
            "operation": "image_to_video",
            "reference_image_path": str(image_path),
            "duration": 5,
            "output_path": str(output_path),
        }
    )

    assert result.success, result.error
    assert output_path.read_bytes() == b"fake mp4"
    assert result.model == "wavespeed-ai/wan-2.2/i2v-480p-ultra-fast"
    assert result.cost_usd == 0.05
    assert calls["posts"][1][1]["json"]["image"] == "https://cdn.test/input.png"
    assert calls["posts"][1][1]["json"]["duration"] == 5


def test_video_selector_discovers_wavespeed(monkeypatch):
    from tools.tool_registry import ToolRegistry

    monkeypatch.setenv("WAVESPEED_API_KEY", "test-key")
    monkeypatch.setenv("WAVESPEED_VIDEO_MODEL", "wavespeed-ai/wan-2.2/i2v-480p-ultra-fast")
    registry = ToolRegistry()
    registry.discover()

    tool = registry.get("wavespeed_video")
    assert tool is not None
    assert tool.get_status() == ToolStatus.AVAILABLE
    assert tool in registry.get_by_capability("video_generation")

    selector = registry.get("video_selector")
    providers = [
        candidate
        for candidate in registry.get_by_capability("video_generation")
        if candidate.name != "video_selector"
    ]
    eligible = selector._filter_candidates(
        {"operation": "image_to_video"},
        providers,
    )
    assert "wavespeed_video" in {candidate.name for candidate in eligible}

    text_to_video = selector._filter_candidates(
        {"operation": "text_to_video"},
        providers,
    )
    assert "wavespeed_video" not in {candidate.name for candidate in text_to_video}


def test_video_selector_discovers_wavespeed_t2v(monkeypatch):
    from tools.tool_registry import ToolRegistry

    monkeypatch.setenv("WAVESPEED_API_KEY", "test-key")
    monkeypatch.setenv("WAVESPEED_VIDEO_MODEL", "wavespeed-ai/wan-2.2/t2v-5b-720p")
    registry = ToolRegistry()
    registry.discover()

    tool = registry.get("wavespeed_video")
    selector = registry.get("video_selector")
    assert tool is not None
    providers = [
        candidate
        for candidate in registry.get_by_capability("video_generation")
        if candidate.name != "video_selector"
    ]
    text_to_video = selector._filter_candidates(
        {"operation": "text_to_video"},
        providers,
    )
    assert "wavespeed_video" in {candidate.name for candidate in text_to_video}

    image_to_video = selector._filter_candidates(
        {"operation": "image_to_video"},
        providers,
    )
    assert "wavespeed_video" not in {candidate.name for candidate in image_to_video}


def test_video_selector_maps_portrait_aspect_ratio_to_wavespeed_size(monkeypatch, tmp_path):
    monkeypatch.setenv("WAVESPEED_API_KEY", "test-key")
    monkeypatch.setenv("WAVESPEED_VIDEO_MODEL", "wavespeed-ai/wan-2.2/t2v-5b-720p")

    from tools.video.video_selector import VideoSelector

    selector = VideoSelector()
    wavespeed = next(tool for tool in selector._providers() if tool.name == "wavespeed_video")
    captured = {}

    def fake_execute(inputs):
        captured.update(inputs)
        from tools.base_tool import ToolResult
        return ToolResult(success=True, data={"output_path": str(tmp_path / "clip.mp4")})

    monkeypatch.setattr(wavespeed, "execute", fake_execute)
    monkeypatch.setattr(selector, "_providers", lambda: [wavespeed])

    result = selector.execute({
        "prompt": "portrait financial metaphor",
        "preferred_provider": "wavespeed",
        "allowed_providers": ["wavespeed"],
        "operation": "text_to_video",
        "aspect_ratio": "9:16",
        "duration": "5",
        "output_path": str(tmp_path / "clip.mp4"),
    })

    assert result.success
    assert captured["size"] == "720*1280"


def test_wavespeed_t2v_documents_native_size_mapping(monkeypatch):
    monkeypatch.setenv("WAVESPEED_VIDEO_MODEL", "wavespeed-ai/wan-2.2/t2v-5b-720p")

    tool = WaveSpeedVideo()
    info = tool.get_info()

    assert info["output_profile"]["sizes"] == ["1280*720", "720*1280"]
    assert info["output_profile"]["aspect_ratio_to_size"] == {
        "16:9": "1280*720",
        "9:16": "720*1280",
    }
