"""Deterministic, mobile-first finance charts for WeChat articles."""

from __future__ import annotations

import math
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


class FinanceChart(BaseTool):
    name = "finance_chart"
    version = "0.1.0"
    tier = ToolTier.CORE
    capability = "graphics"
    provider = "pillow"
    stability = ToolStability.BETA
    execution_mode = ExecutionMode.SYNC
    determinism = Determinism.DETERMINISTIC
    runtime = ToolRuntime.LOCAL

    dependencies = ["python:PIL"]
    install_instructions = "Install Pillow: pip install Pillow"
    agent_skills = ["d3-viz"]
    capabilities = [
        "finance_bar_chart",
        "finance_line_chart",
        "finance_comparison_chart",
        "wechat_cover_card",
    ]
    supports = {
        "local_offline": True,
        "mobile_first": True,
        "exact_text": True,
        "source_annotation": True,
    }
    best_for = [
        "one-question finance charts with conclusion-led titles",
        "phone-readable WeChat article visuals",
        "native rendering of exact numbers and labels",
    ]
    not_good_for = [
        "dense dashboards or more than three series",
        "decorative imagery",
        "interactive charts",
    ]

    input_schema = {
        "type": "object",
        "required": ["chart_type", "title", "output_path"],
        "properties": {
            "chart_type": {
                "type": "string",
                "enum": ["bar", "line", "comparison", "card"],
            },
            "title": {"type": "string"},
            "subtitle": {"type": "string"},
            "highlight": {"type": "string"},
            "series": {
                "type": "array",
                "maxItems": 3,
                "items": {
                    "type": "object",
                    "required": ["name", "values"],
                    "properties": {
                        "name": {"type": "string"},
                        "values": {
                            "type": "array",
                            "maxItems": 12,
                            "items": {
                                "type": "object",
                                "required": ["label", "value"],
                                "properties": {
                                    "label": {"type": "string"},
                                    "value": {"type": "number"},
                                },
                            },
                        },
                    },
                },
            },
            "unit": {"type": "string"},
            "source_note": {"type": "string"},
            "as_of_note": {"type": "string"},
            "colors": {"type": "array", "items": {"type": "string"}},
            "width": {"type": "integer", "minimum": 640, "default": 1080},
            "height": {"type": "integer", "minimum": 480, "default": 720},
            "allow_nonzero_baseline": {"type": "boolean", "default": False},
            "baseline_note": {"type": "string"},
            "output_path": {"type": "string"},
        },
    }
    output_schema = {
        "type": "object",
        "properties": {
            "output_path": {"type": "string"},
            "width": {"type": "integer"},
            "height": {"type": "integer"},
            "chart_type": {"type": "string"},
            "baseline": {"type": "number"},
        },
    }
    resource_profile = ResourceProfile(cpu_cores=1, ram_mb=256, vram_mb=0, disk_mb=20)
    side_effects = ["writes a PNG image to output_path"]
    user_visible_verification = [
        "Verify every number against its cited source",
        "Verify the chart title states the one conclusion the chart supports",
        "Verify labels and source notes remain readable at phone width",
    ]

    _BG = "#F7F5F0"
    _INK = "#17202A"
    _MUTED = "#687078"
    _GRID = "#D9D5CC"
    _DEFAULT_COLORS = ["#C43D32", "#246B72", "#D89B2B"]

    def get_status(self) -> ToolStatus:
        try:
            from PIL import Image  # noqa: F401

            return ToolStatus.AVAILABLE
        except ImportError:
            return ToolStatus.UNAVAILABLE

    @staticmethod
    def _font(size: int, *, bold: bool = False):
        from PIL import ImageFont

        candidates = [
            "/System/Library/Fonts/PingFang.ttc",
            "/System/Library/Fonts/STHeiti Medium.ttc" if bold else "/System/Library/Fonts/STHeiti Light.ttc",
            "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc" if bold else "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ]
        for candidate in candidates:
            if Path(candidate).is_file():
                try:
                    return ImageFont.truetype(candidate, size=size)
                except OSError:
                    pass
        return ImageFont.load_default()

    @staticmethod
    def _format_number(value: float, unit: str) -> str:
        absolute = abs(value)
        if absolute >= 100_000_000:
            text = f"{value / 100_000_000:.1f}亿"
        elif absolute >= 10_000:
            text = f"{value / 10_000:.1f}万"
        elif math.isclose(value, round(value), abs_tol=1e-9):
            text = str(int(round(value)))
        else:
            text = f"{value:.2f}".rstrip("0").rstrip(".")
        return f"{text}{unit}"

    @staticmethod
    def _nice_step(span: float, target_intervals: int = 5) -> float:
        """Return a publication-friendly tick step (1/2/2.5/5 × 10^n)."""
        if span <= 0:
            return 1.0
        rough = span / max(target_intervals, 1)
        magnitude = 10 ** math.floor(math.log10(rough))
        normalized = rough / magnitude
        for candidate in (1.0, 2.0, 2.5, 5.0, 10.0):
            if normalized <= candidate:
                return candidate * magnitude
        return 10.0 * magnitude

    @staticmethod
    def _text_lines(draw, text: str, font, max_width: int, max_lines: int = 2) -> list[str]:
        if not text:
            return []
        lines: list[str] = []
        current = ""
        for char in text:
            candidate = current + char
            if current and draw.textlength(candidate, font=font) > max_width:
                lines.append(current)
                current = char
                if len(lines) == max_lines - 1:
                    break
            else:
                current = candidate
        consumed = sum(len(line) for line in lines)
        remaining = text[consumed:]
        if len(lines) < max_lines and remaining:
            final = remaining
            while draw.textlength(final, font=font) > max_width and len(final) > 1:
                final = final[:-1]
            if len(final) < len(remaining):
                final = final[:-1] + "…"
            lines.append(final)
        return lines

    def execute(self, inputs: dict[str, Any]) -> ToolResult:
        try:
            from PIL import Image, ImageDraw
        except ImportError:
            return ToolResult(success=False, error="Pillow is required for finance_chart")

        chart_type = inputs["chart_type"]
        series = inputs.get("series") or []
        if chart_type != "card":
            if not series or any(not item.get("values") for item in series):
                return ToolResult(success=False, error="Charts require at least one non-empty series")
            labels = [point["label"] for point in series[0]["values"]]
            if any([point["label"] for point in item["values"]] != labels for item in series):
                return ToolResult(success=False, error="Every series must use the same ordered labels")
            if not str(inputs.get("source_note", "")).strip():
                return ToolResult(success=False, error="Finance charts require source_note")
        else:
            labels = []

        width = int(inputs.get("width", 1080))
        height = int(inputs.get("height", 720))
        output_path = Path(inputs["output_path"])
        output_path.parent.mkdir(parents=True, exist_ok=True)

        image = Image.new("RGB", (width, height), self._BG)
        draw = ImageDraw.Draw(image)
        title_font = self._font(max(32, width // 24), bold=True)
        subtitle_font = self._font(max(19, width // 48))
        label_font = self._font(max(16, width // 58))
        value_font = self._font(max(16, width // 58), bold=True)
        source_font = self._font(max(14, width // 68))

        # Editorial accent and conclusion-led title.
        draw.rounded_rectangle((48, 46, 64, 148), radius=8, fill="#C43D32")
        title_lines = self._text_lines(draw, inputs["title"], title_font, width - 150, 2)
        y = 48
        for line in title_lines:
            draw.text((88, y), line, font=title_font, fill=self._INK)
            y += int(title_font.size * 1.25) if hasattr(title_font, "size") else 42
        if inputs.get("subtitle"):
            draw.text((88, y + 4), inputs["subtitle"], font=subtitle_font, fill=self._MUTED)

        if chart_type == "card":
            highlight = str(inputs.get("highlight") or "核心问题")
            big_font = self._font(max(54, width // 12), bold=True)
            box = (72, 250, width - 72, height - 110)
            draw.rounded_rectangle(box, radius=28, fill="#FFFFFF", outline=self._GRID, width=2)
            bbox = draw.textbbox((0, 0), highlight, font=big_font)
            tw = bbox[2] - bbox[0]
            draw.text(((width - tw) / 2, 330), highlight, font=big_font, fill="#C43D32")
            footer = inputs.get("as_of_note") or "财经研究档案"
            draw.text((88, height - 72), footer, font=source_font, fill=self._MUTED)
            image.save(output_path, format="PNG", optimize=True)
            return ToolResult(
                success=True,
                data={"output_path": str(output_path), "width": width, "height": height, "chart_type": chart_type, "baseline": 0},
                artifacts=[str(output_path)],
            )

        values = [float(point["value"]) for item in series for point in item["values"]]
        allow_nonzero = bool(inputs.get("allow_nonzero_baseline", False))
        if allow_nonzero and not str(inputs.get("baseline_note", "")).strip():
            return ToolResult(success=False, error="A non-zero baseline requires baseline_note")
        data_min, data_max = min(values), max(values)
        baseline = data_min if allow_nonzero else min(0.0, data_min)
        top = data_max if allow_nonzero else max(0.0, data_max)
        if math.isclose(top, baseline):
            top = baseline + 1.0
        span = top - baseline
        step = self._nice_step(span)
        y_min = math.floor(baseline / step) * step if allow_nonzero else baseline
        y_max = math.ceil(top / step) * step
        if math.isclose(y_max, y_min):
            y_max = y_min + step
        tick_intervals = max(1, int(round((y_max - y_min) / step)))

        left, right = 108, width - 54
        top_px, bottom = 215, height - 132
        chart_h, chart_w = bottom - top_px, right - left

        def y_pos(value: float) -> float:
            return bottom - (value - y_min) / (y_max - y_min) * chart_h

        for tick in range(tick_intervals + 1):
            value = y_min + step * tick
            py = y_pos(value)
            draw.line((left, py, right, py), fill=self._GRID, width=1)
            tick_text = self._format_number(value, inputs.get("unit", ""))
            bbox = draw.textbbox((0, 0), tick_text, font=label_font)
            draw.text((left - 12 - (bbox[2] - bbox[0]), py - 10), tick_text, font=label_font, fill=self._MUTED)

        colors = (inputs.get("colors") or self._DEFAULT_COLORS)[: len(series)]
        while len(colors) < len(series):
            colors.append(self._DEFAULT_COLORS[len(colors) % len(self._DEFAULT_COLORS)])

        count = len(labels)
        x_step = chart_w / max(count, 1)
        if chart_type in {"bar", "comparison"}:
            group_width = x_step * 0.72
            bar_width = max(8, group_width / len(series))
            zero_y = y_pos(0 if y_min <= 0 <= y_max else y_min)
            for s_idx, item in enumerate(series):
                for idx, point in enumerate(item["values"]):
                    cx = left + x_step * (idx + 0.5)
                    x0 = cx - group_width / 2 + s_idx * bar_width
                    x1 = x0 + bar_width * 0.82
                    py = y_pos(float(point["value"]))
                    draw.rounded_rectangle((x0, min(py, zero_y), x1, max(py, zero_y)), radius=4, fill=colors[s_idx])
                    if count <= 8:
                        value_text = self._format_number(float(point["value"]), inputs.get("unit", ""))
                        bbox = draw.textbbox((0, 0), value_text, font=value_font)
                        draw.text(((x0 + x1 - (bbox[2] - bbox[0])) / 2, min(py, zero_y) - 26), value_text, font=value_font, fill=self._INK)
        else:
            for s_idx, item in enumerate(series):
                points = []
                for idx, point in enumerate(item["values"]):
                    px = left + x_step * (idx + 0.5)
                    py = y_pos(float(point["value"]))
                    points.append((px, py))
                if len(points) > 1:
                    draw.line(points, fill=colors[s_idx], width=5, joint="curve")
                for px, py in points:
                    draw.ellipse((px - 6, py - 6, px + 6, py + 6), fill=self._BG, outline=colors[s_idx], width=4)

        for idx, label in enumerate(labels):
            px = left + x_step * (idx + 0.5)
            short = label if len(label) <= 8 else label[:7] + "…"
            bbox = draw.textbbox((0, 0), short, font=label_font)
            draw.text((px - (bbox[2] - bbox[0]) / 2, bottom + 14), short, font=label_font, fill=self._INK)

        # Legend only adds value when there is more than one series.
        if len(series) > 1:
            legend_x = right - sum(110 for _ in series)
            for idx, item in enumerate(series):
                draw.rounded_rectangle((legend_x, 178, legend_x + 20, 198), radius=5, fill=colors[idx])
                draw.text((legend_x + 28, 176), item["name"], font=label_font, fill=self._INK)
                legend_x += 110

        footer_parts = [inputs.get("source_note", ""), inputs.get("as_of_note", "")]
        if allow_nonzero:
            footer_parts.append(inputs["baseline_note"])
        footer = "  ·  ".join(part for part in footer_parts if part)
        draw.text((54, height - 48), footer, font=source_font, fill=self._MUTED)

        image.save(output_path, format="PNG", optimize=True)
        return ToolResult(
            success=True,
            data={"output_path": str(output_path), "width": width, "height": height, "chart_type": chart_type, "baseline": baseline},
            artifacts=[str(output_path)],
        )
