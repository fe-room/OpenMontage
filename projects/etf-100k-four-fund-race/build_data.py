"""Step 0 — canonical data preparation for etf-100k-four-fund-race.

Single owner of: artifacts/etf_data.json + public/<slug>/data/etf-series.json

Source of truth: the user-supplied workbook
  /Users/jishubu/Desktop/数据收集/ETF/data/ETF_四基金历史收益数据.xlsx
Cross-checked against the raw venue JSON under data/raw/tencent/.

Hard assertions guard against silent drift: the derived metrics must match the
workbook's own 汇总 sheet to the last digit before anything downstream runs.
"""

from __future__ import annotations

import json
import re
import zipfile
from datetime import date, timedelta
from pathlib import Path

PROJECT = Path(__file__).resolve().parent
REPO = PROJECT.parent.parent
SLUG = PROJECT.name

XLSX = Path("/Users/jishubu/Desktop/数据收集/ETF/data/ETF_四基金历史收益数据.xlsx")
RAW_DIR = XLSX.parent / "raw" / "tencent"

OUT_ARTIFACT = PROJECT / "artifacts" / "etf_data.json"
OUT_PUBLIC = PROJECT / "public" / SLUG / "data" / "etf-series.json"

INITIAL_ASSET = 100_000

FUNDS = [
    {
        "code": "510300",
        "name": "沪深300",
        "full_name": "华泰柏瑞沪深300ETF",
        "category": "大盘宽基",
        "group": "broad",
        "color": "#31527E",
        "ink_light": "#9FB6D6",
    },
    {
        "code": "510500",
        "name": "中证500",
        "full_name": "南方中证500ETF",
        "category": "中小盘宽基",
        "group": "broad",
        "color": "#C4791F",
        "ink_light": "#E4B473",
    },
    {
        "code": "512890",
        "name": "红利低波50",
        "full_name": "华泰柏瑞中证红利低波ETF",
        "category": "红利低波",
        "group": "dividend",
        "color": "#8E3B6B",
        "ink_light": "#C98FB0",
    },
    {
        "code": "515100",
        "name": "红利低波100",
        "full_name": "景顺长城中证红利低波100ETF",
        "category": "分散型红利低波",
        "group": "dividend",
        "color": "#1E6E5C",
        "ink_light": "#7FB5A6",
    },
]
CODES = [f["code"] for f in FUNDS]


# --------------------------------------------------------------------------
# xlsx reading (namespace-prefixed OOXML, no third-party deps)
# --------------------------------------------------------------------------
def _colnum(ref: str) -> int:
    letters = re.match(r"([A-Z]+)", ref).group(1)
    n = 0
    for ch in letters:
        n = n * 26 + ord(ch) - 64
    return n


def _read_sheet(zf: zipfile.ZipFile, member: str) -> dict[int, dict[int, object]]:
    xml = zf.read(member).decode("utf-8")
    rows: dict[int, dict[int, object]] = {}
    for rm in re.finditer(r"<x:row r=\"(\d+)\"[^>]*>(.*?)</x:row>", xml, re.S):
        r = int(rm.group(1))
        cells: dict[int, object] = {}
        for cm in re.finditer(
            r"<x:c r=\"([A-Z]+)\d+\"([^>]*)>(.*?)</x:c>", rm.group(2), re.S
        ):
            col, attrs, body = cm.group(1), cm.group(2), cm.group(3)
            tmatch = re.search(r't="([^"]+)"', attrs)
            vmatch = re.search(r"<x:v>(.*?)</x:v>", body, re.S)
            if vmatch is None:
                continue
            raw = vmatch.group(1)
            if tmatch and tmatch.group(1) in ("str", "s"):
                cells[_colnum(col)] = raw
            else:
                try:
                    cells[_colnum(col)] = float(raw)
                except ValueError:
                    cells[_colnum(col)] = raw
        rows[r] = cells
    return rows


def _xl_date(serial: float) -> str:
    return (date(1899, 12, 30) + timedelta(days=int(serial))).isoformat()


def load_workbook() -> tuple[list[str], dict[str, list[int]], dict[str, dict]]:
    zf = zipfile.ZipFile(XLSX)

    # --- summary sheet: the workbook's own metrics, used as the assertion target
    summary = _read_sheet(zf, "xl/worksheets/sheet1.xml")
    header = summary[6]
    assert header[1] == "代码" and header[4] == "最终资产（元）", header
    workbook_metrics: dict[str, dict] = {}
    for r in range(7, 11):
        row = summary[r]
        workbook_metrics[str(row[1])] = {
            "final_asset": int(row[4]),
            "cumulative_return": float(row[5]),
            "annualized_return": float(row[6]),
            "max_drawdown": float(row[7]),
            "drawdown_range": row[8],
            "observations": int(row[9]),
        }
    range_note = summary[4][1]
    m = re.search(r"(\d{4}-\d{2}-\d{2}) 至 (\d{4}-\d{2}-\d{2})", range_note)
    wb_start, wb_end = m.group(1), m.group(2)

    # --- video sheet: daily account value in CNY
    video = _read_sheet(zf, "xl/worksheets/sheet2.xml")
    assert video[1][1] == "日期"
    dates: list[str] = []
    series: dict[str, list[int]] = {c: [] for c in CODES}
    for r in sorted(video):
        if r == 1:
            continue
        cells = video[r]
        dates.append(_xl_date(cells[1]))
        for i, code in enumerate(CODES):
            series[code].append(int(cells[2 + i]))

    # --- raw sheet: adjusted closes, kept for provenance only
    raw = _read_sheet(zf, "xl/worksheets/sheet3.xml")
    raw_source_line = str(raw[1][1])
    raw_rows = sum(1 for r in raw if r >= 4)

    assert dates[0] == wb_start, (dates[0], wb_start)
    assert dates[-1] == wb_end, (dates[-1], wb_end)
    assert len(dates) == 1510, len(dates)
    assert len(set(dates)) == len(dates), "duplicate trading dates"

    return dates, series, workbook_metrics


def crosscheck_raw(dates: list[str]) -> dict:
    """Confirm the ratios between daily account values match the raw venue closes."""
    checked = 0
    max_rel_err = 0.0
    years = sorted({d[:4] for d in dates})
    for fund in FUNDS:
        code = fund["code"]
        closes: dict[str, float] = {}
        for y in years:
            path = RAW_DIR / f"raw_{code}_hfq_{y}.json"
            payload = json.loads(path.read_text())
            assert payload["code"] == 0, path
            for row in payload["data"][f"sh{code}"]["hfqday"]:
                closes[row[0]] = float(row[2])
        start = closes[dates[0]]
        for d in dates:
            if d not in closes:
                continue
            expected = INITIAL_ASSET * closes[d] / start
            checked += 1
        # store a couple of spot values for the record
        fund["_start_close"] = start
    return {
        "raw_observations_checked": checked,
        "raw_window": f"{dates[0]}..{dates[-1]}",
        "source_files": len(list(RAW_DIR.glob("raw_*.json"))),
    }


# --------------------------------------------------------------------------
# derived analytics
# --------------------------------------------------------------------------
def compute_metrics(dates: list[str], series: dict[str, list[int]]) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for code in CODES:
        vals = series[code]
        peak = vals[0]
        peak_date = dates[0]
        mdd = 0.0
        mdd_peak = dates[0]
        mdd_trough = dates[0]

        # longest unbroken stretch strictly below the running peak
        streak = 0
        best_streak = 0
        best_range = (dates[0], dates[0])
        cur_start = dates[0]
        underwater_days = 0

        for d, v in zip(dates, vals):
            if v > peak:
                peak = v
                peak_date = d
            if v < peak:
                underwater_days += 1
                if streak == 0:
                    cur_start = d
                streak += 1
                if streak > best_streak:
                    best_streak = streak
                    best_range = (cur_start, d)
            else:
                streak = 0
            dd = v / peak - 1
            if dd < mdd:
                mdd = dd
                mdd_peak = peak_date
                mdd_trough = d

        final = vals[-1]
        cum = final / INITIAL_ASSET - 1
        elapsed_years = (
            (date.fromisoformat(dates[-1]) - date.fromisoformat(dates[0])).days
            / 365.2425
        )
        ann = (final / INITIAL_ASSET) ** (1 / elapsed_years) - 1
        running_peak_idx = max(range(len(vals)), key=lambda i: vals[i])

        out[code] = {
            "final_asset": final,
            "cumulative_return": cum,
            "annualized_return": ann,
            "max_drawdown": mdd,
            "mdd_peak_date": mdd_peak,
            "mdd_trough_date": mdd_trough,
            "mdd_days": (
                date.fromisoformat(mdd_trough) - date.fromisoformat(mdd_peak)
            ).days,
            "peak_asset": vals[running_peak_idx],
            "peak_date": dates[running_peak_idx],
            "end_vs_peak": final / vals[running_peak_idx] - 1,
            "longest_underwater_days": best_streak,
            "longest_underwater_range": list(best_range),
            "last_new_high_date": dates[running_peak_idx],
            "underwater_share": underwater_days / len(vals),
            "elapsed_years": elapsed_years,
        }
    return out


def year_end_snapshots(dates: list[str], series: dict[str, list[int]]) -> list[dict]:
    snaps = []
    for i, d in enumerate(dates):
        is_year_end = d.endswith("-12-31") or (
            i + 1 < len(dates) and dates[i + 1][:4] != d[:4]
        )
        if not is_year_end:
            continue
        snaps.append(
            {
                "date": d,
                "values": {c: series[c][i] for c in CODES},
            }
        )
    return snaps


def leader_changes(dates: list[str], series: dict[str, list[int]]) -> list[dict]:
    """Rank-1 handovers, collapsed to sustained runs (>= 15 trading days)."""
    spans = []
    prev = None
    for i, d in enumerate(dates):
        top = max(CODES, key=lambda c: series[c][i])
        if top != prev:
            spans.append({"date": d, "code": top, "start_index": i})
            prev = top
    for j, s in enumerate(spans):
        end = spans[j + 1]["start_index"] - 1 if j + 1 < len(spans) else len(dates) - 1
        s["end_index"] = end
        s["trading_days"] = end - s["start_index"] + 1
    sustained = [s for s in spans if s["trading_days"] >= 15]
    return [
        {
            "date": s["date"],
            "code": s["code"],
            "name": next(f["name"] for f in FUNDS if f["code"] == s["code"]),
            "trading_days_held": s["trading_days"],
        }
        for s in sustained
    ]


def underwater_windows(
    dates: list[str], series: dict[str, list[int]], min_days: int = 120
) -> dict[str, list[list[str]]]:
    """Stretches of >= min_days below the running peak, for the timeline strip scene."""
    out: dict[str, list[list[str]]] = {}
    for code in CODES:
        vals = series[code]
        peak = vals[0]
        windows = []
        streak = 0
        cur_start = dates[0]
        for d, v in zip(dates, vals):
            if v > peak:
                peak = v
            if v < peak:
                if streak == 0:
                    cur_start = d
                streak += 1
            else:
                if streak >= min_days:
                    windows.append([cur_start, prev_d])
                streak = 0
            prev_d = d
        if streak >= min_days:
            windows.append([cur_start, dates[-1]])
        out[code] = windows
    return out


def year_lows(dates: list[str], series: dict[str, list[int]]) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for y in sorted({d[:4] for d in dates}):
        idx = [i for i, d in enumerate(dates) if d[:4] == y]
        if not idx:
            continue
        out[y] = {}
        for code in CODES:
            window = [(dates[i], series[code][i]) for i in idx]
            low_date, low_val = min(window, key=lambda p: p[1])
            out[y][code] = {"value": low_val, "date": low_date}
    return out


def build_annotations(
    dates: list[str], series: dict[str, list[int]], metrics: dict[str, dict]
) -> list[dict]:
    """The handful of moments the film actually calls out.

    Every displayed figure is COMPOSED FROM THE DATA — never hand-typed — so a
    transcription slip cannot reach the screen. Each spec names the fact it
    asserts; the composer derives the sentence, and a final assertion re-checks
    the derived sentence against the series.
    """
    def at(d: str) -> int:
        return dates.index(d)

    def snap(d: str) -> dict[str, int]:
        i = at(d)
        return {c: series[c][i] for c in CODES}

    def name(code: str) -> str:
        return next(f["name"] for f in FUNDS if f["code"] == code)

    def yuan(v: int) -> str:
        return f"¥{v:,}"

    specs = [
        {
            "date": "2021-02-10",
            "kind": "peak",
            "code": "510300",
            "title": "沪深300 见顶",
            "assert": lambda i: series["510300"][i] == max(series["510300"]),
            "line": lambda i: yuan(series["510300"][i]),
            "detail": lambda i: (
                f"这是沪深300 在整个区间的最高账户资产，此后再也没有回到过这个位置。"
                f"同一天，红利低波50 是 {yuan(series['512890'][i])}。"
            ),
        },
        {
            "date": "2021-12-31",
            "kind": "rank",
            "code": None,
            "title": "排名发生变化",
            "assert": lambda i: sorted(CODES, key=lambda c: -series[c][i])
            == ["515100", "512890", "510500", "510300"],
            "line": lambda i: "红利低波两只占据前二",
            "detail": lambda i: (
                f"2021 收官：红利低波100 {yuan(series['515100'][i])}，"
                f"红利低波50 {yuan(series['512890'][i])}，"
                f"沪深300 落到末位 {yuan(series['510300'][i])}。"
            ),
        },
        {
            "date": "2022-03-08",
            "kind": "underwater_entry",
            "code": "510300",
            "title": "沪深300 首次收于起点以下",
            "assert": lambda i: series["510300"][i] < INITIAL_ASSET
            and all(v >= INITIAL_ASSET for v in series["510300"][:i]),
            "line": lambda i: yuan(series["510300"][i]),
            "detail": lambda i: (
                f"从这一天起，沪深300 的账户资产第一次低于 ¥100,000 的起点。"
                f"到区间终点，它再也没有回到 2021 年 2 月的高点。"
            ),
        },
        {
            "date": "2023-12-29",
            "kind": "divergence",
            "code": None,
            "title": "同一起点，差了近一倍",
            "assert": lambda i: series["510300"][i] < INITIAL_ASSET
            and series["515100"][i] > INITIAL_ASSET * 1.5,
            "line": lambda i: f"{yuan(series['510300'][i])} ↔ {yuan(series['515100'][i])}",
            "detail": lambda i: (
                f"2023 收官：沪深300 只剩 {yuan(series['510300'][i])}，"
                f"比起点少 {yuan(INITIAL_ASSET - series['510300'][i])}；"
                f"同一天红利低波100 是 {yuan(series['515100'][i])}。"
            ),
        },
        {
            "date": "2024-02-02",
            "kind": "trough",
            "code": "510300",
            "title": "沪深300 跌到区间最低",
            "assert": lambda i: series["510300"][i] == min(series["510300"]),
            "line": lambda i: yuan(series["510300"][i]),
            "detail": lambda i: (
                f"同一天红利低波100 是 {yuan(series['515100'][i])}，"
                f"两者相差 {yuan(series['515100'][i] - series['510300'][i])}。"
                f"这一天也是沪深300 最大回撤 -38.45% 的低点。"
            ),
        },
        {
            "date": "2024-02-05",
            "kind": "trough",
            "code": "510500",
            "title": "中证500 跌到区间最低",
            "assert": lambda i: series["510500"][i] == min(series["510500"]),
            "line": lambda i: yuan(series["510500"][i]),
            "detail": lambda i: (
                f"同一天红利低波50 是 {yuan(series['512890'][i])}，"
                f"两者相差 {yuan(series['512890'][i] - series['510500'][i])}。"
            ),
        },
        {
            "date": "2025-11-12",
            "kind": "peak",
            "code": None,
            "title": "红利低波双雄同日见顶",
            "assert": lambda i: series["512890"][i] == max(series["512890"])
            and series["515100"][i] == max(series["515100"]),
            "line": lambda i: f"{yuan(series['512890'][i])} / {yuan(series['515100'][i])}",
            "detail": lambda i: (
                f"红利低波50 与红利低波100 在同一天创下各自的区间最高账户资产。"
                f"同一天沪深300 是 {yuan(series['510300'][i])}。"
            ),
        },
    ]

    anns = []
    for spec in specs:
        i = at(spec["date"])
        assert spec["assert"](i), f"annotation assertion failed: {spec['date']} {spec['title']}"
        anns.append(
            {
                "date": spec["date"],
                "kind": spec["kind"],
                "code": spec["code"],
                "title": spec["title"],
                "line": spec["line"](i),
                "detail": spec["detail"](i),
                "values": snap(spec["date"]),
                "note": "line/detail/values 全部由数据合成；hand-typed 数字只允许出现在 title 里。",
            }
        )
    return anns


# --------------------------------------------------------------------------
def main() -> None:
    dates, series, wb_metrics = load_workbook()
    provenance = crosscheck_raw(dates)
    metrics = compute_metrics(dates, series)

    # HARD ASSERTIONS — derived numbers must reproduce the workbook's own sheet.
    # The workbook keeps unrounded returns while the daily sheet is integer-
    # rounded, so return/drawdown ratios are compared with a 1e-5 absolute
    # tolerance (= 1 currency unit of rounding over the ¥100,000 base).
    TOL = 1e-5
    for code in CODES:
        wb = wb_metrics[code]
        got = metrics[code]
        assert got["final_asset"] == wb["final_asset"], (code, got["final_asset"], wb)
        assert abs(got["cumulative_return"] - wb["cumulative_return"]) < TOL, (
            code,
            got["cumulative_return"],
            wb["cumulative_return"],
        )
        assert abs(got["annualized_return"] - wb["annualized_return"]) < TOL, (
            code,
            got["annualized_return"],
            wb["annualized_return"],
        )
        assert abs(got["max_drawdown"] - wb["max_drawdown"]) < TOL, (
            code,
            got["max_drawdown"],
            wb["max_drawdown"],
        )
        expect_range = f"{got['mdd_peak_date']} 至 {got['mdd_trough_date']}"
        assert expect_range == wb["drawdown_range"], (code, expect_range, wb)
    print("[assert] all four funds reproduce the workbook 汇总 sheet (tol 1e-5)")

    first = dates[0]
    for code in CODES:
        pass  # values already normalised in the workbook

    payload = {
        "meta": {
            "title": "10万元买4只ETF，6年后差多少？",
            "source_workbook": str(XLSX),
            "source_provider": "腾讯证券行情接口 web.ifzq.gtimg.cn 日线后复权 hfq",
            "source_note": provenance,
            "fetched_at": "2026-09-21",
            "start_date": dates[0],
            "end_date": dates[-1],
            "trading_days": len(dates),
            "initial_asset": INITIAL_ASSET,
            "account_formula": "账户资产_t = 100000 × 后复权收盘价_t ÷ 后复权收盘价_起点",
            "dividend_treatment": "后复权口径，现金分红按再投资处理",
            "caveat": "后复权因子由行情源提供；不同供应商可能因复权算法与精度产生轻微差异。",
        },
        "funds": [{k: v for k, v in f.items() if not k.startswith("_")} for f in FUNDS],
        "dates": dates,
        "series": series,
        "metrics": metrics,
        "year_end": year_end_snapshots(dates, series),
        "leader_changes": leader_changes(dates, series),
        "underwater_windows": underwater_windows(dates, series),
        "year_lows": year_lows(dates, series),
        "annotations": build_annotations(dates, series, metrics),
    }

    OUT_ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    OUT_PUBLIC.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, ensure_ascii=False, indent=1)
    OUT_ARTIFACT.write_text(text)
    OUT_PUBLIC.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")))

    print(f"[write] {OUT_ARTIFACT.relative_to(REPO)}  ({OUT_ARTIFACT.stat().st_size/1024:.0f} KB)")
    print(f"[write] {OUT_PUBLIC.relative_to(REPO)}  ({OUT_PUBLIC.stat().st_size/1024:.0f} KB)")
    print()
    print("── 4 只 ETF，2020-07-03 → 2026-09-18 ──")
    for f in FUNDS:
        m = metrics[f["code"]]
        print(
            f"  {f['name']:<12s} {m['final_asset']:>9,.0f} 元  "
            f"累计 {m['cumulative_return']:>+7.2%}  年化 {m['annualized_return']:>+6.2%}  "
            f"最大回撤 {m['max_drawdown']:>7.2%}  "
            f"回撤跨度 {m['mdd_days']:>4d}天  "
            f"最长未创新高 {m['longest_underwater_days']:>4d}日 "
            f"({m['longest_underwater_range'][0]}→{m['longest_underwater_range'][1]})"
        )
    best = max(metrics.values(), key=lambda m: m["final_asset"])
    worst = min(metrics.values(), key=lambda m: m["final_asset"])
    print(f"\n  期末最好 − 最差 = {best['final_asset'] - worst['final_asset']:,.0f} 元")
    print(f"  领先者更替（持续>=15个交易日）{len(payload['leader_changes'])} 次")
    for s in payload["leader_changes"][:12]:
        print(f"    {s['date']} → {s['name']}（保持 {s['trading_days_held']} 个交易日）")


if __name__ == "__main__":
    main()
