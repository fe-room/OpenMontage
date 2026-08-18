"""Local packaging for a manually published WeChat Official Account article."""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

from tools.base_tool import (
    BaseTool,
    Determinism,
    ExecutionMode,
    ResourceProfile,
    ToolResult,
    ToolRuntime,
    ToolStability,
    ToolStatus,
    ToolTier,
)


class WechatArticleBundle(BaseTool):
    name = "wechat_article_bundle"
    version = "0.1.0"
    tier = ToolTier.PUBLISH
    capability = "publish"
    provider = "local"
    stability = ToolStability.BETA
    execution_mode = ExecutionMode.SYNC
    determinism = Determinism.DETERMINISTIC
    runtime = ToolRuntime.LOCAL

    dependencies: list[str] = []
    install_instructions = "No setup required — uses the Python standard library."
    agent_skills: list[str] = []
    capabilities = ["package_wechat_article", "write_article_manifest"]
    supports = {"local_offline": True, "uploads": False, "manual_publish": True}
    best_for = ["assembling an article, cover, figures, sources, and checklist for manual WeChat publishing"]
    not_good_for = ["logging into or uploading to WeChat Official Accounts"]

    input_schema = {
        "type": "object",
        "required": [
            "title", "article_markdown_path", "cover_path", "image_paths",
            "source_notes", "checklist", "disclaimer", "output_dir",
        ],
        "properties": {
            "title": {"type": "string"},
            "digest": {"type": "string"},
            "article_markdown_path": {"type": "string"},
            "cover_path": {"type": "string"},
            "image_paths": {"type": "array", "items": {"type": "string"}, "minItems": 1},
            "source_notes": {"type": "string"},
            "checklist": {"type": "object"},
            "disclaimer": {"type": "string"},
            "output_dir": {"type": "string"},
        },
    }
    output_schema = {"type": "object", "properties": {"wechat_article_package": {"type": "object"}}}
    resource_profile = ResourceProfile(cpu_cores=1, ram_mb=128, vram_mb=0, disk_mb=20)
    side_effects = ["writes a local WeChat hand-off bundle"]
    user_visible_verification = [
        "Open article.md and confirm headings, figures, data notes, and disclaimer",
        "Check cover.png and every numbered image at phone width",
        "Manually paste the approved content into WeChat Official Accounts",
    ]

    def get_status(self) -> ToolStatus:
        return ToolStatus.AVAILABLE

    def execute(self, inputs: dict[str, Any]) -> ToolResult:
        from lib.wechat_editorial import WECHAT_FINANCE_DISCLAIMER

        if inputs.get("disclaimer") != WECHAT_FINANCE_DISCLAIMER:
            return ToolResult(success=False, error="The finance article disclaimer is missing or not exact")

        article_in = Path(inputs["article_markdown_path"])
        cover_in = Path(inputs["cover_path"])
        image_inputs = [Path(path) for path in inputs["image_paths"]]
        for label, path in [("article_markdown_path", article_in), ("cover_path", cover_in)]:
            if not path.is_file():
                return ToolResult(success=False, error=f"{label} not found: {path}")
        for path in image_inputs:
            if not path.is_file():
                return ToolResult(success=False, error=f"image_path not found: {path}")

        output_dir = Path(inputs["output_dir"])
        images_dir = output_dir / "images"
        images_dir.mkdir(parents=True, exist_ok=True)

        article_out = output_dir / "article.md"
        sources_out = output_dir / "sources.md"
        cover_out = images_dir / f"cover{cover_in.suffix.lower() or '.png'}"
        shutil.copy2(article_in, article_out)
        shutil.copy2(cover_in, cover_out)

        ordered_images: list[str] = []
        for index, path in enumerate(image_inputs, start=1):
            target = images_dir / f"{index:02d}-{path.stem}{path.suffix.lower() or '.png'}"
            shutil.copy2(path, target)
            ordered_images.append(str(target))

        sources_out.write_text(inputs["source_notes"].rstrip() + "\n", encoding="utf-8")
        manifest_out = output_dir / "manifest.json"
        package = {
            "version": "1.0",
            "status": "ready" if all(bool(v) for v in inputs["checklist"].values()) else "needs_revision",
            "platform": "wechat_official_account",
            "manual_publish_required": True,
            "title": inputs["title"],
            "digest": inputs.get("digest", ""),
            "article_markdown_path": str(article_out),
            "article_html_path": None,
            "assets_dir": str(images_dir),
            "cover_path": str(cover_out),
            "ordered_images": ordered_images,
            "source_notes_path": str(sources_out),
            "manifest_path": str(manifest_out),
            "checklist": inputs["checklist"],
            "disclaimer": inputs["disclaimer"],
            "delivery_notes": [
                "This package does not upload or publish anything.",
                "Re-check WeChat preview on a phone before manual publication.",
            ],
        }

        try:
            from schemas.artifacts import validate_artifact

            validate_artifact("wechat_article_package", package)
        except Exception as exc:
            return ToolResult(success=False, error=f"wechat_article_package failed validation: {exc}")

        manifest_out.write_text(json.dumps(package, ensure_ascii=False, indent=2), encoding="utf-8")
        return ToolResult(
            success=True,
            data={"wechat_article_package": package},
            artifacts=[str(article_out), str(cover_out), *ordered_images, str(sources_out), str(manifest_out)],
        )
