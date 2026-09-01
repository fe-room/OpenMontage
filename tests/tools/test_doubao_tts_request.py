from tools.audio.doubao_tts import DoubaoTTS


def test_submit_body_passes_speech_2_context_controls_in_additions():
    body = DoubaoTTS()._submit_body(
        {
            "text": "测试文本。",
            "context_texts": ["保持沉稳男声，咬字清晰，不要叹气。"],
            "section_id": "gold-narration-v2",
            "disable_markdown_filter": False,
        },
        voice_id="zh_male_dayi_saturn_bigtts",
        request_id="request-id",
    )

    import json

    additions = json.loads(body["req_params"]["additions"])
    assert additions == {
        "disable_markdown_filter": False,
        "context_texts": ["保持沉稳男声，咬字清晰，不要叹气。"],
        "section_id": "gold-narration-v2",
    }


def test_official_unidirectional_body_matches_documented_fields():
    body = DoubaoTTS()._unidirectional_body(
        {
            "text": "官方请求测试。",
            "disable_markdown_filter": False,
            "disable_emoji_filter": False,
            "enable_latex_tn": True,
        },
        voice_id="zh_male_dayi_uranus_bigtts",
    )

    import json

    assert body["req_params"]["speaker"] == "zh_male_dayi_uranus_bigtts"
    assert body["req_params"]["audio_params"] == {
        "format": "mp3",
        "sample_rate": 24000,
        "speech_rate": 0,
        "enable_subtitle": True,
    }
    assert json.loads(body["req_params"]["additions"]) == {
        "disable_markdown_filter": False,
        "disable_emoji_filter": False,
        "enable_latex_tn": True,
    }


def test_usage_header_uses_official_wildcard():
    headers = DoubaoTTS()._headers(
        api_key="secret",
        resource_id="seed-tts-2.0",
        request_id="request-id",
        return_usage=True,
    )
    assert headers["X-Control-Require-Usage-Tokens-Return"] == "*"


def test_semantic_splitter_keeps_chunks_under_quality_limit():
    text = "第一句话。\n\n" + ("第二句话比较长。" * 80) + "\n\n最后一句话。"
    chunks = DoubaoTTS.split_text_semantically(text, max_chars=120)

    assert len(chunks) > 2
    assert all(len(chunk) <= 120 for chunk in chunks)
    assert "".join(chunk.replace("\n", "") for chunk in chunks) == text.replace("\n", "")
