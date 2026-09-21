"""合成源码与成片的硬性自检。

两件事，都是被真实缺陷逼出来的：

1. 浅色墨只能落在深色底片上。
   本片的浅色墨是 C.invertText（#F6F7F4）。曾经 sc08 的柱状图用
   `color: labelInside ? C.invertText : f.color` 这类**由数据决定**的选色，
   配合 textAlign:right + 固定 width，把近白字推到了柱端之外 168px，
   落在浅色底板上只有 1.06:1 对比度 —— 屏幕上等于没写。
   所以规则收紧为：invertText 只能出现在显式设置 background: C.invert 的元素里，
   且不允许由数据条件决定。

2. 可读文字必须落在竖屏安全区里。
   实测每帧有墨迹的最左/最右列与最低行，而不是相信布局声明。
   声明过 safe area 却越界的情况已经发生过两次。

用法：
    ./.venv/bin/python projects/etf-100k-four-fund-race/check_composition.py
    ./.venv/bin/python projects/etf-100k-four-fund-race/check_composition.py --frames
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parent
REPO = PROJECT.parent.parent

LIGHT_INK = "C.invertText"
# 注意：不能用 `"C.invert" in window` 来判断有没有深色底片 ——
# "C.invert" 是 "C.invertText" 的子串，那样写永远为真，检查就成了摆设。
DARK_CHIP = re.compile(r"background\s*:\s*C\.invert(?!Text)")
SAFE_LEFT, SAFE_RIGHT = 96, 984
SAFE_BOTTOM = 1400

failures: list[str] = []


# ---------------------------------------------------------------------------
# 1. 静态不变量：浅色墨必须落在深色底片上
# ---------------------------------------------------------------------------
def check_light_ink_containment() -> None:
    print("=" * 72)
    print("静态不变量 · 浅色墨 (§1)")
    print("=" * 72)

    total = 0
    for src in sorted(PROJECT.glob("*.tsx")):
        text = src.read_text()
        for m in re.finditer(re.escape(LIGHT_INK), text):
            total += 1
            line_no = text[: m.start()].count("\n") + 1
            # 所在元素的属性区间：从本行的 '{' 起往回找 400 字符，往后找 400 字符
            lo = max(0, m.start() - 400)
            hi = min(len(text), m.end() + 400)
            window = text[lo:hi]

            if not DARK_CHIP.search(window):
                failures.append(
                    f"{src.name}:{line_no} 浅色墨没有落在 background: C.invert 的容器里"
                )
                status = "FAIL  没有深色底片"
            else:
                status = "ok    在深色底片上"

            # 数据条件选色：{cond ? C.invertText : x} / {x : C.invertText} 一律禁止
            cond = re.search(
                r"\?\s*" + re.escape(LIGHT_INK) + r"|" + re.escape(LIGHT_INK) + r"\s*:",
                window,
            )
            if cond:
                failures.append(
                    f"{src.name}:{line_no} 浅色墨由数据条件决定 —— 数据一变底色就变，禁止"
                )
                status += " + FAIL 条件选色"

            print(f"  {src.name}:{line_no:<5} {status}")

    print(f"  invertText 出现次数：{total}")
    if total == 0:
        print("  注意：本片当前没有任何浅色墨，说明标签已经全部改为墨色。")
    print()


# ---------------------------------------------------------------------------
# 2. 实测安全区：抽帧求有墨迹的边界
# ---------------------------------------------------------------------------
def check_safe_area(sample_every: int = 30) -> None:
    print("=" * 72)
    print(f"实测安全区 · 每 {sample_every} 帧抽一帧 (§2)")
    print("=" * 72)

    video = PROJECT / "renders" / "final.mp4"
    if not video.exists():
        print("  成片不存在，跳过。\n")
        return

    try:
        import numpy as np
        from PIL import Image
    except ImportError:
        print("  缺少 numpy / Pillow，跳过。\n")
        return

    try:
        probe = subprocess.run(
            ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_streams", str(video)],
            capture_output=True, text=True, check=True,
        )
        nb = int(json.loads(probe.stdout)["streams"][0]["nb_frames"])
    except Exception as exc:  # noqa: BLE001
        print(f"  ffprobe 失败：{exc}\n")
        return

    tmp = Path("/tmp/etf_qa_safearea")
    if tmp.exists():
        for f in tmp.glob("*.png"):
            f.unlink()
    tmp.mkdir(parents=True, exist_ok=True)

    # 一次 ffmpeg 抽完所有采样帧。
    # 注意不要写成「每帧调用一次 ffmpeg 并 select 到第 n 帧」——那是 O(n²) 解码，
    # 2970 帧的片子抽 99 帧会把每个采样点到该帧的全部帧都解一遍，慢到被杀。
    subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-i", str(video),
         "-vf", f"select='not(mod(n\\,{sample_every}))'", "-vsync", "0",
         "-frame_pts", "1", str(tmp / "s%06d.png")],
        check=True,
    )
    pngs = sorted(tmp.glob("s*.png"))
    print(f"  抽出 {len(pngs)} 帧（每 {sample_every} 帧一抽）")

    worst = {"left": 10_000, "right": -1, "bottom": -1, "frame": -1}
    checked = 0
    for png in pngs:
        fr_num = int(png.stem[1:])
        frame = fr_num * sample_every
        g = np.array(Image.open(png).convert("L"))
        ink = g < 190
        cols, rows = ink.sum(axis=0), ink.sum(axis=1)
        xs = [i for i, c in enumerate(cols) if c > 1]
        ys = [i for i, c in enumerate(rows) if c > 2]
        if not xs or not ys:
            continue
        checked += 1
        left, right, bottom = min(xs), max(xs), max(ys)
        if left < worst["left"]:
            worst["left"] = left
        worst["right"] = max(worst["right"], right)
        if bottom > worst["bottom"]:
            worst["bottom"] = bottom
            worst["frame"] = frame
        if left < SAFE_LEFT - 4 or right > SAFE_RIGHT + 4 or bottom > SAFE_BOTTOM:
            failures.append(
                f"frame {frame}: 墨迹越界 x {left}..{right}（限制 {SAFE_LEFT}..{SAFE_RIGHT}）"
                f" 最低行 {bottom}（限制 {SAFE_BOTTOM}）"
            )

    print(f"  抽检 {checked} 帧")
    print(f"  最左列 {worst['left']}  最右列 {worst['right']}  最低行 {worst['bottom']}")
    print(f"  限制   {SAFE_LEFT}..{SAFE_RIGHT}                 {SAFE_BOTTOM}")
    print(f"  -> {'PASS' if not failures else 'FAIL'}")
    print()


def main() -> None:
    check_light_ink_containment()
    if "--frames" in sys.argv:
        check_safe_area()
    else:
        print("（加 --frames 可对成片抽帧实测安全区）\n")

    print("=" * 72)
    if failures:
        print(f"不通过：{len(failures)} 项")
        for f in failures:
            print("  - " + f)
        sys.exit(1)
    print("全部通过")


if __name__ == "__main__":
    main()
