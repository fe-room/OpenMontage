"""WaveSpeedAI video generation for the model selected in ``.env``.

The provider supports both text-to-video and image-to-video WaveSpeed models.
Its advertised contract is resolved from ``WAVESPEED_VIDEO_MODEL`` so preflight
describes the model that will actually receive a paid prediction.
"""

from __future__ import annotations

import os
import re
import time
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


_API_BASE = "https://api.wavespeed.ai/api/v3"
_UPLOAD_URL = f"{_API_BASE}/media/upload/binary"
_DEFAULT_MODEL = "wavespeed-ai/wan-2.2/i2v-480p-ultra-fast"
_WAN_22_T2V_5B_720P = "wavespeed-ai/wan-2.2/t2v-5b-720p"
_MODEL_ID_RE = re.compile(r"^[A-Za-z0-9._-]+(?:/[A-Za-z0-9._-]+)+$")
_TERMINAL_FAILURES = {"failed", "cancelled", "timeout"}
_ACTIVE_STATUSES = {"created", "processing", "queued", "submitted"}


def _configured_value(name: str) -> str | None:
    value = os.environ.get(name, "").strip()
    if not value or value.lower() in {"your-key", "your_api_key", "changeme"} or value == "你的Key":
        return None
    return value


def _is_t2v_model(model: str) -> bool:
    return "/t2v" in model.lower()


class WaveSpeedVideo(BaseTool):
    name = "wavespeed_video"
    version = "0.1.0"
    tier = ToolTier.GENERATE
    capability = "video_generation"
    provider = "wavespeed"
    stability = ToolStability.BETA
    execution_mode = ExecutionMode.ASYNC
    determinism = Determinism.SEEDED
    runtime = ToolRuntime.API

    dependencies = ["env:WAVESPEED_API_KEY"]
    install_instructions = (
        "Set WAVESPEED_API_KEY to your WaveSpeedAI API key and optionally set\n"
        f"WAVESPEED_VIDEO_MODEL to the desired endpoint (legacy fallback: {_DEFAULT_MODEL}).\n"
        "Get a key at https://wavespeed.ai/accesskey"
    )
    agent_skills = ["ai-video-gen"]

    capabilities = ["text_to_video", "image_to_video", "first_last_frame_to_video", "model_selection"]
    supports = {
        "text_to_video": True,
        "image_to_video": True,
        "reference_image": True,
        "first_last_frame_to_video": True,
        "negative_prompt": True,
        "seed": True,
        "native_audio": False,
    }
    best_for = [
        "low-cost WaveSpeedAI text-to-video or image-to-video generation",
        "model-selected previews using the endpoint configured in .env",
    ]
    not_good_for = [
        "synchronized native audio",
        "using an operation unsupported by the configured model endpoint",
    ]
    fallback_tools = ["wan_video", "comfyui_video", "seedance_video", "kling_video"]
    quality_score = 0.72

    input_schema = {
        "type": "object",
        "required": ["prompt"],
        "properties": {
            "prompt": {"type": "string"},
            "operation": {
                "type": "string",
                "enum": ["text_to_video", "image_to_video"],
                "description": "Defaults to the operation implied by WAVESPEED_VIDEO_MODEL.",
            },
            "model": {
                "type": "string",
                "default": _DEFAULT_MODEL,
                "description": "WaveSpeedAI model ID; WAVESPEED_VIDEO_MODEL is used when omitted.",
            },
            "reference_image_url": {
                "type": "string",
                "description": "Public first-frame image URL.",
            },
            "reference_image_path": {
                "type": "string",
                "description": "Local first-frame image; uploaded to WaveSpeedAI automatically.",
            },
            "last_image_url": {
                "type": "string",
                "description": "Optional public final-frame image URL.",
            },
            "last_image_path": {
                "type": "string",
                "description": "Optional local final frame; uploaded automatically.",
            },
            "negative_prompt": {"type": "string"},
            "size": {
                "type": "string",
                "enum": ["1280*720", "720*1280"],
                "default": "1280*720",
                "description": (
                    "Wan 2.2 T2V 5B accepts only these two native sizes: "
                    "1280*720 for 16:9 landscape or 720*1280 for 9:16 portrait. "
                    "The WaveSpeed endpoint reads size, not aspect_ratio; selectors must map "
                    "the requested ratio to this field explicitly."
                ),
            },
            "duration": {
                "type": "integer",
                "enum": [5, 8],
                "default": 5,
            },
            "seed": {
                "type": "integer",
                "minimum": -1,
                "default": -1,
            },
            "output_path": {"type": "string"},
            "poll_interval_seconds": {
                "type": "number",
                "minimum": 2,
                "default": 2.0,
            },
            "timeout_seconds": {
                "type": "integer",
                "minimum": 30,
                "default": 600,
            },
        },
    }

    resource_profile = ResourceProfile(
        cpu_cores=1, ram_mb=512, vram_mb=0, disk_mb=500, network_required=True
    )
    retry_policy = RetryPolicy(
        max_retries=4,
        backoff_seconds=1.0,
        retryable_errors=["rate_limit", "timeout", "server_error"],
    )
    idempotency_key_fields = [
        "prompt",
        "model",
        "reference_image_url",
        "reference_image_path",
        "last_image_url",
        "last_image_path",
        "negative_prompt",
        "duration",
        "seed",
    ]
    side_effects = [
        "uploads local reference images to WaveSpeedAI temporary storage",
        "submits a paid WaveSpeedAI prediction",
        "writes the generated video to output_path",
    ]
    user_visible_verification = [
        "Watch the generated clip for motion coherence, reference fidelity, and 480p artifacts"
    ]

    def get_status(self) -> ToolStatus:
        return ToolStatus.AVAILABLE if _configured_value("WAVESPEED_API_KEY") else ToolStatus.UNAVAILABLE

    def is_operation_available(self, operation: str) -> bool:
        """Only advertise the operation implemented by the configured endpoint."""
        if self.get_status() != ToolStatus.AVAILABLE:
            return False
        model = self._model({})
        expected = "text_to_video" if _is_t2v_model(model) else "image_to_video"
        return operation == expected

    def get_info(self) -> dict[str, Any]:
        """Expose effective model capability and pricing, not stale class defaults."""
        info = super().get_info()
        model = self._model({})
        is_t2v = _is_t2v_model(model)
        operation = "text_to_video" if is_t2v else "image_to_video"
        info["configured_model"] = model
        info["capabilities"] = [operation, "model_selection"]
        if not is_t2v:
            info["capabilities"].append("first_last_frame_to_video")
        info["supports"] = {
            **info["supports"],
            "text_to_video": is_t2v,
            "image_to_video": not is_t2v,
            "reference_image": not is_t2v,
            "first_last_frame_to_video": not is_t2v,
            "negative_prompt": not is_t2v,
        }
        info["input_schema"] = {
            **info["input_schema"],
            "properties": {
                **info["input_schema"]["properties"],
                "model": {
                    **info["input_schema"]["properties"]["model"],
                    "default": model,
                },
                "operation": {
                    **info["input_schema"]["properties"]["operation"],
                    "default": operation,
                },
                "duration": {
                    **info["input_schema"]["properties"]["duration"],
                    "enum": [5] if is_t2v else [5, 8],
                    "default": 5,
                },
            },
        }
        if model == _WAN_22_T2V_5B_720P:
            info["best_for"] = [
                "5-second 720p text-to-video clips from a prompt",
                "low-cost social and explainer B-roll generation",
            ]
            info["not_good_for"] = [
                "image-to-video or reference-conditioned generation",
                "native synchronized audio",
            ]
            info["pricing"] = {
                "unit": "per_video",
                "duration_seconds": 5,
                "estimated_cost_usd": 0.05,
            }
            info["output_profile"] = {
                "duration_seconds": 5,
                "sizes": ["1280*720", "720*1280"],
                "aspect_ratio_to_size": {
                    "16:9": "1280*720",
                    "9:16": "720*1280",
                },
                "size_constraint": "Only the two listed native sizes are supported.",
                "verification_note": (
                    "The size value is the API request profile. Probe the downloaded MP4 because "
                    "provider-side H.264 encoding can report a slightly different coded short edge."
                ),
                "resolution": "720p",
            }
        return info

    @staticmethod
    def _model(inputs: dict[str, Any]) -> str:
        model = str(
            inputs.get("model")
            or _configured_value("WAVESPEED_VIDEO_MODEL")
            or _DEFAULT_MODEL
        ).strip()
        if not _MODEL_ID_RE.fullmatch(model):
            raise ValueError("WaveSpeedAI model must be a slash-delimited model ID")
        return model

    @staticmethod
    def _duration(inputs: dict[str, Any]) -> int:
        duration = int(inputs.get("duration", 5))
        if duration not in {5, 8}:
            raise ValueError("WaveSpeedAI Wan 2.2 ultra-fast duration must be 5 or 8 seconds")
        return duration

    @classmethod
    def _operation(cls, inputs: dict[str, Any], model: str) -> str:
        operation = str(
            inputs.get("operation")
            or ("text_to_video" if _is_t2v_model(model) else "image_to_video")
        )
        expected = "text_to_video" if _is_t2v_model(model) else "image_to_video"
        if operation != expected:
            raise ValueError(f"Configured WaveSpeedAI model {model} supports {expected}, not {operation}")
        return operation

    def estimate_cost(self, inputs: dict[str, Any]) -> float:
        if self._model(inputs) == _WAN_22_T2V_5B_720P:
            return 0.05
        return round(self._duration(inputs) * 0.01, 2)

    def estimate_runtime(self, inputs: dict[str, Any]) -> float:
        if self._model(inputs) == _WAN_22_T2V_5B_720P:
            return 90.0
        return 42.0 if self._duration(inputs) == 5 else 55.0

    def execute(self, inputs: dict[str, Any]) -> ToolResult:
        api_key = _configured_value("WAVESPEED_API_KEY")
        if not api_key:
            return ToolResult(success=False, error="WAVESPEED_API_KEY not set. " + self.install_instructions)
        started = time.time()
        try:
            result = self._generate(inputs, api_key=api_key)
        except Exception as exc:
            return ToolResult(success=False, error=f"WaveSpeedAI video generation failed: {exc}")

        result.duration_seconds = round(time.time() - started, 2)
        return result

    def _generate(self, inputs: dict[str, Any], *, api_key: str) -> ToolResult:
        import requests
        from requests.adapters import HTTPAdapter
        from urllib3.util.retry import Retry

        from tools.video._shared import probe_output

        headers = {"Authorization": f"Bearer {api_key}"}
        model = self._model(inputs)
        operation = self._operation(inputs, model)
        payload: dict[str, Any] = {
            "prompt": str(inputs["prompt"]).strip(),
            "seed": int(inputs.get("seed", -1)),
        }
        image_url = None
        last_image_url = None
        if operation == "text_to_video":
            size = str(inputs.get("size", "1280*720"))
            if size not in {"1280*720", "720*1280"}:
                raise ValueError("WaveSpeedAI Wan 2.2 T2V 5B size must be 1280*720 or 720*1280")
            payload["size"] = size
            duration = 5
        else:
            image_url = inputs.get("reference_image_url")
            if not image_url and inputs.get("reference_image_path"):
                image_url = self._upload_media(str(inputs["reference_image_path"]), headers=headers)
            if not image_url:
                raise ValueError("image_to_video requires reference_image_url or reference_image_path")
            last_image_url = inputs.get("last_image_url")
            if not last_image_url and inputs.get("last_image_path"):
                last_image_url = self._upload_media(str(inputs["last_image_path"]), headers=headers)
            duration = self._duration(inputs)
            payload["image"] = image_url
            payload["duration"] = duration
            if inputs.get("negative_prompt"):
                payload["negative_prompt"] = inputs["negative_prompt"]
            if last_image_url:
                payload["last_image"] = last_image_url

        # WaveSpeedAI explicitly warns against automatically retrying the paid
        # submission POST because an accepted request can be billed even when
        # the client loses the response.
        submit = requests.post(
            f"{_API_BASE}/{model}",
            headers={**headers, "Content-Type": "application/json"},
            json=payload,
            timeout=(10, 60),
        )
        submit.raise_for_status()
        task = self._response_data(submit.json(), action="Task submission")
        prediction_id = str(task.get("id") or "").strip()
        if not prediction_id:
            raise RuntimeError("Task submission response did not contain a prediction id")
        result_url = (task.get("urls") or {}).get("get") or f"{_API_BASE}/predictions/{prediction_id}/result"

        session = requests.Session()
        session.mount(
            "https://",
            HTTPAdapter(
                max_retries=Retry(
                    total=4,
                    backoff_factor=0.5,
                    status_forcelist=(429, 500, 502, 503, 504),
                    allowed_methods={"GET"},
                    respect_retry_after_header=True,
                )
            ),
        )
        completed = self._poll_result(
            session,
            str(result_url),
            headers=headers,
            poll_interval=float(inputs.get("poll_interval_seconds", 2.0)),
            timeout_seconds=int(inputs.get("timeout_seconds", 600)),
        )
        video_url = self._first_output_url(completed.get("outputs"))

        download = session.get(video_url, timeout=(10, 180))
        download.raise_for_status()
        output_path = Path(inputs.get("output_path", "wavespeed_video.mp4"))
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(download.content)

        probed = probe_output(output_path)
        return ToolResult(
            success=True,
            data={
                "provider": "wavespeed",
                "model": model,
                "prediction_id": prediction_id,
                "prompt": payload["prompt"],
                "operation": operation,
                "duration": duration,
                "resolution": "720p" if operation == "text_to_video" else "480p",
                "size": payload.get("size"),
                "seed": completed.get("seed", payload["seed"]),
                "source_image_url": image_url,
                "last_image_url": last_image_url,
                "video_url": video_url,
                "output": str(output_path),
                "output_path": str(output_path),
                "format": "mp4",
                **probed,
            },
            artifacts=[str(output_path)],
            cost_usd=self.estimate_cost(inputs),
            seed=completed.get("seed") if isinstance(completed.get("seed"), int) else None,
            model=model,
        )

    @staticmethod
    def _response_data(body: Any, *, action: str) -> dict[str, Any]:
        if not isinstance(body, dict):
            raise RuntimeError(f"{action} returned a non-object response")
        if body.get("code") not in (None, 200):
            raise RuntimeError(str(body.get("message") or f"{action} failed"))
        data = body.get("data", body)
        if not isinstance(data, dict):
            raise RuntimeError(f"{action} response did not contain an object data field")
        return data

    @classmethod
    def _upload_media(cls, path_value: str, *, headers: dict[str, str]) -> str:
        import requests

        path = Path(path_value)
        if not path.is_file():
            raise FileNotFoundError(f"Reference image not found: {path}")
        with path.open("rb") as handle:
            response = requests.post(
                _UPLOAD_URL,
                headers=headers,
                files={"file": (path.name, handle)},
                timeout=(10, 300),
            )
        response.raise_for_status()
        data = cls._response_data(response.json(), action="Media upload")
        url = data.get("download_url") or data.get("url")
        if not isinstance(url, str) or not url:
            raise RuntimeError("Media upload response did not contain a download URL")
        return url

    @classmethod
    def _poll_result(
        cls,
        session: Any,
        result_url: str,
        *,
        headers: dict[str, str],
        poll_interval: float,
        timeout_seconds: int,
    ) -> dict[str, Any]:
        deadline = time.monotonic() + timeout_seconds
        delay = max(2.0, poll_interval)
        while time.monotonic() < deadline:
            response = session.get(result_url, headers=headers, timeout=(10, 30))
            response.raise_for_status()
            data = cls._response_data(response.json(), action="Result query")
            status = str(data.get("status") or "").lower()
            if status == "completed":
                return data
            if status in _TERMINAL_FAILURES:
                raise RuntimeError(str(data.get("error") or f"Prediction ended with status {status}"))
            if status not in _ACTIVE_STATUSES:
                raise RuntimeError(f"Unexpected prediction status: {status or 'missing'}")
            time.sleep(delay)
            delay = min(10.0, delay + 1.0)
        raise TimeoutError("Timed out waiting for WaveSpeedAI prediction")

    @staticmethod
    def _first_output_url(outputs: Any) -> str:
        if not isinstance(outputs, list) or not outputs:
            raise RuntimeError("Completed prediction did not contain outputs")
        first = outputs[0]
        if isinstance(first, str) and first.startswith(("https://", "http://")):
            return first
        if isinstance(first, dict):
            for key in ("url", "video_url", "download_url"):
                value = first.get(key)
                if isinstance(value, str) and value.startswith(("https://", "http://")):
                    return value
        raise RuntimeError("Completed prediction output did not contain a video URL")
