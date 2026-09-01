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
