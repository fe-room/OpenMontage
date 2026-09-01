"""Doubao Speech text-to-speech provider tool."""

from __future__ import annotations

import base64
import json
import os
import re
import time
import uuid
import warnings
from pathlib import Path
from typing import Any

from tools.base_tool import (
    BaseTool,
    Determinism,
    ExecutionMode,
    ResourceProfile,
    RetryPolicy,
    ToolResult,
    ToolRuntime,
    ToolStability,
    ToolStatus,
    ToolTier,
)


class DoubaoTTS(BaseTool):
    name = "doubao_tts"
    version = "0.1.0"
    tier = ToolTier.VOICE
    capability = "tts"
    provider = "doubao"
    stability = ToolStability.EXPERIMENTAL
    execution_mode = ExecutionMode.ASYNC
    determinism = Determinism.STOCHASTIC
    runtime = ToolRuntime.API

    dependencies = []
    install_instructions = (
        "Set DOUBAO_SPEECH_API_KEY to a Volcengine Doubao Speech API Key.\n"
        "Optional: set DOUBAO_SPEECH_VOICE_TYPE to the default speaker voice.\n"
        "Use the new console API key flow; do not pass app id/access token as the API key."
    )
    fallback = "google_tts"
    fallback_tools = ["google_tts", "elevenlabs_tts", "openai_tts", "piper_tts"]
    agent_skills = ["doubao-tts", "text-to-speech"]

    capabilities = [
        "text_to_speech",
        "voice_selection",
        "multilingual",
        "timestamp_alignment",
    ]
    supports = {
        "voice_cloning": False,
        "multilingual": True,
        "offline": False,
        "native_audio": True,
        "timestamps": True,
        "long_text_async": False,
        "official_unidirectional_streaming": True,
        "semantic_chunk_limit": 400,
    }
    best_for = [
        "natural Mandarin narration",
        "Chinese explainer voiceovers with character-level timestamps",
        "long-form narration that needs subtitle alignment",
    ]
    not_good_for = [
        "fully offline production",
        "voice clone matching",
        "real-time interactive speech playback",
    ]

    input_schema = {
        "type": "object",
        "required": ["text"],
        "properties": {
            "text": {"type": "string", "description": "Text to convert to speech"},
            "voice_id": {
                "type": "string",
                "description": (
                    "Doubao speaker/voice_type. Defaults to DOUBAO_SPEECH_VOICE_TYPE, "
                    "then config.yaml narration_defaults.voice_id."
                ),
            },
            "resource_id": {
                "type": "string",
                "default": "seed-tts-2.0",
                "description": "Volcengine resource id. Use seed-tts-2.0 for Doubao Speech 2.0 voices.",
            },
            "format": {
                "type": "string",
                "default": "mp3",
                "enum": ["mp3", "ogg_opus", "pcm"],
            },
            "sample_rate": {
                "type": "integer",
                "default": 24000,
                "enum": [8000, 16000, 22050, 24000, 32000, 44100, 48000],
            },
            "speech_rate": {
                "type": "integer",
                "default": 0,
                "minimum": -50,
                "maximum": 100,
                "description": "Doubao speech rate. 0=normal, 100=2x, -50=0.5x.",
            },
            "api_mode": {
                "type": "string",
                "default": "unidirectional",
                "enum": ["unidirectional", "async_legacy"],
                "description": "Official V3 unidirectional streaming API, or the deprecated async submit/query path.",
            },
            "max_chars_per_request": {
                "type": "integer",
                "default": 400,
                "minimum": 50,
                "description": "Fail closed above this size so callers split long narration semantically.",
            },
            "enable_timestamp": {
                "type": "boolean",
                "default": True,
                "description": "Return sentence/word timing metadata when supported by the selected endpoint.",
            },
            "disable_markdown_filter": {
                "type": "boolean",
                "default": False,
                "description": "Pass through Doubao markdown filtering behavior. Defaults to API-safe false.",
            },
            "disable_emoji_filter": {
                "type": "boolean",
                "default": False,
            },
            "enable_latex_tn": {
                "type": "boolean",
                "default": True,
            },
            "context_texts": {
                "type": "array",
                "items": {"type": "string"},
                "description": (
                    "Doubao Speech 2.0 voice-performance instructions. Sent in "
                    "req_params.additions.context_texts."
                ),
            },
            "section_id": {
                "type": "string",
                "description": (
                    "Stable context id shared by serial Speech 2.0 requests to preserve "
                    "speaker and delivery continuity."
                ),
            },
            "return_usage": {
                "type": "boolean",
                "default": True,
                "description": "Request usage token data from Volcengine when available.",
            },
            "output_path": {"type": "string"},
            "metadata_path": {
                "type": "string",
                "description": "Where to save request/response metadata. Defaults next to output_path.",
            },
            "poll_interval_seconds": {
                "type": "number",
                "default": 2.0,
                "minimum": 0.5,
            },
            "timeout_seconds": {
                "type": "integer",
                "default": 300,
                "minimum": 30,
            },
        },
    }

    output_schema = {
        "type": "object",
        "properties": {
            "output": {"type": "string"},
            "metadata_path": {"type": "string"},
            "task_id": {"type": "string"},
            "audio_duration_seconds": {"type": ["number", "null"]},
            "sentences": {"type": "array"},
            "usage": {"type": ["object", "null"]},
        },
    }
    artifact_schema = {
        "type": "array",
        "items": {"type": "string"},
    }

    resource_profile = ResourceProfile(
        cpu_cores=1, ram_mb=256, vram_mb=0, disk_mb=50, network_required=True
    )
    retry_policy = RetryPolicy(
        max_retries=2,
        backoff_seconds=2.0,
        retryable_errors=["timeout", "rate_limit", "quota exceeded for types: concurrency"],
    )
    idempotency_key_fields = ["text", "voice_id", "resource_id", "speech_rate", "sample_rate"]
    side_effects = [
        "writes audio file to output_path",
        "writes redacted Doubao request/response metadata JSON next to output_path",
        "calls Volcengine Doubao Speech API",
    ]
    user_visible_verification = [
        "Listen to generated audio for Mandarin naturalness and pacing",
        "Check timestamp JSON before building subtitles",
    ]
    quality_score = 0.88
    latency_p50_seconds = 8.0

    UNIDIRECTIONAL_URL = "https://openspeech.bytedance.com/api/v3/tts/unidirectional"
    LEGACY_SUBMIT_URL = "https://openspeech.bytedance.com/api/v3/tts/submit"
    LEGACY_QUERY_URL = "https://openspeech.bytedance.com/api/v3/tts/query"
    DEFAULT_RESOURCE_ID = "seed-tts-2.0"
    DEFAULT_VOICE_ENV = "DOUBAO_SPEECH_VOICE_TYPE"

    @staticmethod
    def _configured_default_voice() -> str | None:
        try:
            from lib.config_model import OpenMontageConfig

            defaults = OpenMontageConfig.load().narration_defaults
            if defaults.provider == "doubao":
                return defaults.voice_id
        except Exception:
            return None
        return None

    def get_status(self) -> ToolStatus:
        if os.environ.get("DOUBAO_SPEECH_API_KEY"):
            return ToolStatus.AVAILABLE
        return ToolStatus.UNAVAILABLE

    def estimate_cost(self, inputs: dict[str, Any]) -> float:
        # Volcengine bills Doubao Speech 2.0 by characters. Keep this conservative
        # and prefer provider-returned usage when available.
        return round(len(inputs.get("text", "")) * 0.000015, 4)

    @staticmethod
    def split_text_semantically(text: str, max_chars: int = 400) -> list[str]:
        """Split long Mandarin narration at paragraph/sentence boundaries."""
        if max_chars < 50:
            raise ValueError("max_chars must be at least 50")
        paragraphs = [part.strip() for part in re.split(r"\n{2,}", text) if part.strip()]
        units: list[str] = []
        for paragraph in paragraphs:
            if len(paragraph) <= max_chars:
                units.append(paragraph)
                continue
            sentences = [
                part.strip()
                for part in re.findall(r".*?(?:[。！？!?]+[”’']?|$)", paragraph)
                if part.strip()
            ]
            for sentence in sentences:
                if len(sentence) <= max_chars:
                    units.append(sentence)
                else:
                    units.extend(
                        sentence[index:index + max_chars]
                        for index in range(0, len(sentence), max_chars)
                    )

        chunks: list[str] = []
        current = ""
        for unit in units:
            candidate = unit if not current else f"{current}\n\n{unit}"
            if len(candidate) <= max_chars:
                current = candidate
            else:
                if current:
                    chunks.append(current)
                current = unit
        if current:
            chunks.append(current)
        return chunks

    def execute(self, inputs: dict[str, Any]) -> ToolResult:
        api_key = os.environ.get("DOUBAO_SPEECH_API_KEY")
        if not api_key:
            return ToolResult(success=False, error="No Doubao Speech API key. " + self.install_instructions)

        voice_id = (
            inputs.get("voice_id")
            or os.environ.get(self.DEFAULT_VOICE_ENV)
            or self._configured_default_voice()
        )
        if not voice_id:
            return ToolResult(
                success=False,
                error=(
                    "No Doubao voice_id provided. Pass voice_id or set "
                    f"{self.DEFAULT_VOICE_ENV} in the environment."
                ),
            )

        api_mode = inputs.get("api_mode", "unidirectional")
        if api_mode == "async_legacy":
            warnings.warn(
                "Doubao async submit/query mode is deprecated; use the official "
                "V3 unidirectional streaming mode.",
                DeprecationWarning,
                stacklevel=2,
            )
        max_chars = int(inputs.get("max_chars_per_request", 400))
        if api_mode == "unidirectional" and len(inputs["text"]) > max_chars:
            return ToolResult(
                success=False,
                error=(
                    f"Doubao official unidirectional request has {len(inputs['text'])} characters, "
                    f"above the configured {max_chars}-character quality limit. Split the text "
                    "at semantic sentence boundaries and synthesize the chunks separately."
                ),
            )

        start = time.time()
        try:
            result = self._generate(inputs, api_key=api_key, voice_id=voice_id)
        except Exception as exc:
            return ToolResult(success=False, error=f"Doubao TTS failed: {self._safe_error(exc)}")

        result.duration_seconds = round(time.time() - start, 2)
        if not result.cost_usd:
            result.cost_usd = self.estimate_cost(inputs)
        return result

    def _generate(self, inputs: dict[str, Any], *, api_key: str, voice_id: str) -> ToolResult:
        if inputs.get("api_mode", "unidirectional") == "async_legacy":
            return self._generate_async_legacy(inputs, api_key=api_key, voice_id=voice_id)
        return self._generate_unidirectional(inputs, api_key=api_key, voice_id=voice_id)

    def _generate_unidirectional(
        self,
        inputs: dict[str, Any],
        *,
        api_key: str,
        voice_id: str,
    ) -> ToolResult:
        import requests

        text = inputs["text"]
        fmt = inputs.get("format", "mp3")
        resource_id = inputs.get("resource_id", self.DEFAULT_RESOURCE_ID)
        output_path = Path(inputs.get("output_path", f"doubao_tts.{self._extension_for_format(fmt)}"))
        metadata_path = Path(
            inputs.get("metadata_path") or output_path.with_suffix(output_path.suffix + ".json")
        )
        output_path.parent.mkdir(parents=True, exist_ok=True)
        metadata_path.parent.mkdir(parents=True, exist_ok=True)

        request_id = str(uuid.uuid4())
        headers = self._headers(
            api_key=api_key,
            resource_id=resource_id,
            request_id=request_id,
            return_usage=bool(inputs.get("return_usage", True)),
        )
        headers["Connection"] = "keep-alive"
        body = self._unidirectional_body(inputs, voice_id=voice_id)

        audio_data = bytearray()
        response_events: list[dict[str, Any]] = []
        sentences: list[dict[str, Any]] = []
        usage: dict[str, Any] | None = None
        completed = False

        with requests.Session() as session:
            with session.post(
                self.UNIDIRECTIONAL_URL,
                headers=headers,
                json=body,
                stream=True,
                timeout=(10, int(inputs.get("timeout_seconds", 300))),
            ) as response:
                response.raise_for_status()
                log_id = response.headers.get("X-Tt-Logid") or response.headers.get("X-Tt-LogId")
                for line in response.iter_lines(decode_unicode=True):
                    if not line:
                        continue
                    event = json.loads(line)
                    code = event.get("code", 0)
                    encoded_audio = event.get("data")
                    if code == 0 and encoded_audio:
                        audio_data.extend(base64.b64decode(encoded_audio))
                    sentence = event.get("sentence")
                    # The final stream event may repeat the full input as a summary
                    # sentence without word timing. Keep only timing-bearing entries
                    # in the public subtitle list; raw events remain in metadata.
                    if isinstance(sentence, dict) and sentence.get("words"):
                        sentences.append(sentence)
                    if isinstance(event.get("usage"), dict):
                        usage = event["usage"]
                    response_events.append(
                        {
                            key: value
                            for key, value in event.items()
                            if key != "data"
                        }
                        | ({"audio_base64_chars": len(encoded_audio)} if encoded_audio else {})
                    )
                    if code == 20000000:
                        completed = True
                        break
                    if isinstance(code, int) and code > 0:
                        raise RuntimeError(
                            f"Doubao unidirectional synthesis failed: code {code}: "
                            f"{event.get('message', 'unknown error')}"
                        )

        if not completed:
            raise RuntimeError("Doubao unidirectional stream ended without completion code 20000000")
        if not audio_data:
            raise RuntimeError("Doubao unidirectional stream completed without audio data")

        partial_path = output_path.with_suffix(output_path.suffix + ".part")
        partial_path.write_bytes(audio_data)
        partial_path.replace(output_path)

        request_record = {
            "endpoint": self.UNIDIRECTIONAL_URL,
            "api_mode": "unidirectional",
            "request_id": request_id,
            "log_id": log_id,
            "request": {
                "headers": {
                    key: value
                    for key, value in headers.items()
                    if key.lower() != "x-api-key"
                },
                "body": body,
            },
            "response_events": response_events,
            "usage": usage,
        }
        metadata_path.write_text(
            json.dumps(request_record, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

        audio_duration = self._audio_duration(output_path)
        cost = self._cost_from_usage(usage) or self.estimate_cost(inputs)
        return ToolResult(
            success=True,
            data={
                "provider": self.provider,
                "model": resource_id,
                "resource_id": resource_id,
                "voice_id": voice_id,
                "api_mode": "unidirectional",
                "format": fmt,
                "sample_rate": inputs.get("sample_rate", 24000),
                "speech_rate": inputs.get("speech_rate", 0),
                "text_length": len(text),
                "request_id": request_id,
                "log_id": log_id,
                "audio_duration_seconds": round(audio_duration, 2) if audio_duration else None,
                "output": str(output_path),
                "metadata_path": str(metadata_path),
                "sentences": sentences,
                "usage": usage,
            },
            artifacts=[str(output_path), str(metadata_path)],
            cost_usd=cost,
            model=resource_id,
        )

    def _generate_async_legacy(
        self,
        inputs: dict[str, Any],
        *,
        api_key: str,
        voice_id: str,
    ) -> ToolResult:
        import requests

        text = inputs["text"]
        fmt = inputs.get("format", "mp3")
        resource_id = inputs.get("resource_id", self.DEFAULT_RESOURCE_ID)
        output_path = Path(inputs.get("output_path", f"doubao_tts.{self._extension_for_format(fmt)}"))
        metadata_path = Path(
            inputs.get("metadata_path") or output_path.with_suffix(output_path.suffix + ".json")
        )
        output_path.parent.mkdir(parents=True, exist_ok=True)
        metadata_path.parent.mkdir(parents=True, exist_ok=True)

        req_id = str(uuid.uuid4())
        headers = self._headers(
            api_key=api_key,
            resource_id=resource_id,
            request_id=req_id,
            return_usage=bool(inputs.get("return_usage", True)),
        )
        body = self._submit_body(inputs, voice_id=voice_id, request_id=req_id)

        submit_response = requests.post(self.LEGACY_SUBMIT_URL, headers=headers, json=body, timeout=(10, 60))
        submit_data = self._json_or_raise(submit_response)
        self._raise_for_doubao_error(submit_response.status_code, submit_data)

        task_id = submit_data.get("data", {}).get("task_id")
        if not task_id:
            raise RuntimeError("Doubao submit succeeded but did not return data.task_id")

        query_data = self._poll_query(
            requests_module=requests,
            api_key=api_key,
            resource_id=resource_id,
            task_id=task_id,
            return_usage=bool(inputs.get("return_usage", True)),
            poll_interval=float(inputs.get("poll_interval_seconds", 2.0)),
            timeout_seconds=int(inputs.get("timeout_seconds", 300)),
        )
        data = query_data.get("data", {})
        audio_url = data.get("audio_url")
        if not audio_url:
            raise RuntimeError("Doubao task completed but did not return data.audio_url")

        # Persist the completed task response before downloading the potentially
        # large narration file. If the CDN connection drops, the task id and
        # signed URL remain available for diagnosis or manual recovery.
        metadata_path.write_text(json.dumps(query_data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        # Long-form narration can be tens of megabytes. Stream it to a partial
        # file and retry transient/incomplete CDN reads without resubmitting the
        # paid synthesis task. Replace the final path only after a full download.
        partial_path = output_path.with_suffix(output_path.suffix + ".part")
        download_error: Exception | None = None
        for attempt in range(3):
            try:
                with requests.get(audio_url, timeout=(10, 300), stream=True) as audio_response:
                    audio_response.raise_for_status()
                    with open(partial_path, "wb") as audio_file:
                        for chunk in audio_response.iter_content(chunk_size=1024 * 1024):
                            if chunk:
                                audio_file.write(chunk)
                partial_path.replace(output_path)
                download_error = None
                break
            except Exception as exc:
                download_error = exc
                partial_path.unlink(missing_ok=True)
                if attempt < 2:
                    time.sleep(2 ** attempt)
        if download_error is not None:
            raise download_error

        audio_duration = self._audio_duration(output_path)
        usage = data.get("usage")
        cost = self._cost_from_usage(usage) or self.estimate_cost(inputs)

        return ToolResult(
            success=True,
            data={
                "provider": self.provider,
                "model": resource_id,
                "resource_id": resource_id,
                "voice_id": voice_id,
                "format": fmt,
                "sample_rate": inputs.get("sample_rate", 24000),
                "speech_rate": inputs.get("speech_rate", 0),
                "text_length": len(text),
                "task_id": task_id,
                "task_status": data.get("task_status"),
                "req_text_length": data.get("req_text_length"),
                "synthesize_text_length": data.get("synthesize_text_length"),
                "audio_duration_seconds": round(audio_duration, 2) if audio_duration else None,
                "output": str(output_path),
                "metadata_path": str(metadata_path),
                "sentences": data.get("sentences", []),
                "usage": usage,
                "url_expire_time": data.get("url_expire_time"),
            },
            artifacts=[str(output_path), str(metadata_path)],
            cost_usd=cost,
            model=resource_id,
        )

    def _headers(
        self,
        *,
        api_key: str,
        resource_id: str,
        request_id: str,
        return_usage: bool,
    ) -> dict[str, str]:
        headers = {
            "X-Api-Key": api_key,
            "X-Api-Resource-Id": resource_id,
            "X-Api-Request-Id": request_id,
            "Content-Type": "application/json",
        }
        if return_usage:
            headers["X-Control-Require-Usage-Tokens-Return"] = "*"
        return headers

    def _unidirectional_body(self, inputs: dict[str, Any], *, voice_id: str) -> dict[str, Any]:
        additions = {
            "disable_markdown_filter": bool(inputs.get("disable_markdown_filter", False)),
            "disable_emoji_filter": bool(inputs.get("disable_emoji_filter", False)),
            "enable_latex_tn": bool(inputs.get("enable_latex_tn", True)),
        }
        context_texts = inputs.get("context_texts")
        if context_texts:
            additions["context_texts"] = list(context_texts)
        section_id = inputs.get("section_id")
        if section_id:
            additions["section_id"] = section_id
        return {
            "req_params": {
                "text": inputs["text"],
                "speaker": voice_id,
                "additions": json.dumps(additions, ensure_ascii=False),
                "audio_params": {
                    "format": inputs.get("format", "mp3"),
                    "sample_rate": inputs.get("sample_rate", 24000),
                    "speech_rate": inputs.get("speech_rate", 0),
                    "enable_subtitle": bool(inputs.get("enable_timestamp", True)),
                },
            }
        }

    def _submit_body(self, inputs: dict[str, Any], *, voice_id: str, request_id: str) -> dict[str, Any]:
        audio_params = {
            "format": inputs.get("format", "mp3"),
            "sample_rate": inputs.get("sample_rate", 24000),
            "speech_rate": inputs.get("speech_rate", 0),
            "enable_timestamp": bool(inputs.get("enable_timestamp", True)),
        }
        additions = {
            "disable_markdown_filter": bool(inputs.get("disable_markdown_filter", False)),
        }
        context_texts = inputs.get("context_texts")
        if context_texts:
            additions["context_texts"] = list(context_texts)
        section_id = inputs.get("section_id")
        if section_id:
            additions["section_id"] = section_id
        return {
            "user": {"uid": inputs.get("user_id", "openmontage")},
            "unique_id": request_id,
            "req_params": {
                "text": inputs["text"],
                "speaker": voice_id,
                "audio_params": audio_params,
                "additions": json.dumps(additions, ensure_ascii=False),
            },
        }

    def _poll_query(
        self,
        *,
        requests_module: Any,
        api_key: str,
        resource_id: str,
        task_id: str,
        return_usage: bool,
        poll_interval: float,
        timeout_seconds: int,
    ) -> dict[str, Any]:
        deadline = time.time() + timeout_seconds
        while time.time() < deadline:
            time.sleep(poll_interval)
            headers = self._headers(
                api_key=api_key,
                resource_id=resource_id,
                request_id=str(uuid.uuid4()),
                return_usage=return_usage,
            )
            response = requests_module.post(self.LEGACY_QUERY_URL, headers=headers, json={"task_id": task_id}, timeout=(10, 60))
            query_data = self._json_or_raise(response)
            self._raise_for_doubao_error(response.status_code, query_data)
            status = query_data.get("data", {}).get("task_status")
            if status == 2:
                return query_data
            if status == 3:
                raise RuntimeError(f"Doubao task failed: {query_data.get('message', 'unknown error')}")
        raise TimeoutError(f"Doubao task did not finish within {timeout_seconds} seconds")

    @staticmethod
    def _json_or_raise(response: Any) -> dict[str, Any]:
        try:
            return response.json()
        except ValueError as exc:
            raise RuntimeError(f"Non-JSON response from Doubao API: HTTP {response.status_code}") from exc

    def _raise_for_doubao_error(self, http_status: int, payload: dict[str, Any]) -> None:
        code = payload.get("code")
        if http_status < 400 and code == 20000000:
            return
        message = payload.get("message", "unknown error")
        hint = self._diagnostic_hint(message)
        raise RuntimeError(f"HTTP {http_status}, code {code}: {message}{hint}")

    @staticmethod
    def _diagnostic_hint(message: str) -> str:
        lowered = message.lower()
        if "load grant" in lowered or "requested grant not found" in lowered:
            return " (check DOUBAO_SPEECH_API_KEY and use the new-console X-Api-Key flow)"
        if "speaker permission denied" in lowered or "access denied" in lowered:
            return " (check voice_id/DOUBAO_SPEECH_VOICE_TYPE and voice authorization)"
        if "quota exceeded" in lowered:
            return " (check quota, concurrency, or remaining character package)"
        if "unsupported additions explicit language" in lowered:
            return " (do not pass additions.explicit_language for this endpoint)"
        return ""

    @staticmethod
    def _safe_error(exc: Exception) -> str:
        # Avoid ever echoing request headers or secrets in user-visible errors.
        return str(exc).replace(os.environ.get("DOUBAO_SPEECH_API_KEY", ""), "[redacted]")

    @staticmethod
    def _extension_for_format(fmt: str) -> str:
        if fmt == "ogg_opus":
            return "ogg"
        if fmt == "pcm":
            return "pcm"
        return "mp3"

    @staticmethod
    def _audio_duration(path: Path) -> float | None:
        try:
            from tools.analysis.audio_probe import probe_duration

            return probe_duration(path)
        except Exception:
            return None

    @staticmethod
    def _cost_from_usage(usage: Any) -> float | None:
        if not isinstance(usage, dict):
            return None
        text_words = usage.get("text_words")
        if not isinstance(text_words, (int, float)):
            return None
        return round(float(text_words) * 0.000015, 4)
