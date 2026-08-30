#!/usr/bin/env python3
"""Build a tiny pixel garden from GitHub contribution counts.

The workflow passes a JSON contribution calendar produced by GitHub's GraphQL
API. Keeping the renderer dependency-free makes it easy to run in Actions.
"""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "pixel-garden.svg"

LEVEL_COLORS = ["#17212b", "#173b34", "#176b4d", "#27a66f", "#57e389"]
PLANT_COLORS = ["#69e6a1", "#f6c453", "#ff7b72", "#8ab4ff"]


def esc(value: str) -> str:
    return (value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;"))


def main() -> None:
    raw = os.environ.get("CONTRIBUTIONS", "[]")
    try:
        days = json.loads(raw)
    except json.JSONDecodeError:
        days = []
    days = days[-364:]
    total = sum(int(day.get("contributionCount", 0)) for day in days)
    max_count = max([int(day.get("contributionCount", 0)) for day in days] or [1])
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    # 52 columns x 7 rows, with one plant for every high-activity cell.
    cells = []
    plants = []
    for index, day in enumerate(days):
        col, row = index // 7, index % 7
        count = int(day.get("contributionCount", 0))
        level = min(4, round((count / max_count) * 4)) if count else 0
        x, y = 34 + col * 13, 68 + row * 13
        cells.append(f'<rect x="{x}" y="{y}" width="10" height="10" rx="2" fill="{LEVEL_COLORS[level]}"/>')
        if count >= max(3, max_count * 0.55):
            color = PLANT_COLORS[(col + row) % len(PLANT_COLORS)]
            plants.append(f'<g transform="translate({x + 5},{y})" class="plant" style="--delay:{(col + row) % 9 * 0.17:.2f}s"><rect x="-1" y="-12" width="2" height="12" fill="{color}"/><rect x="-7" y="-11" width="6" height="4" fill="{color}"/><rect x="1" y="-7" width="6" height="4" fill="{color}"/></g>')

    title = f"{total} contributions mapped into a tiny pixel garden"
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="760" height="230" viewBox="0 0 760 230" role="img" aria-labelledby="title desc">
<title id="title">{esc(title)}</title><desc id="desc">Higher contribution activity grows plants above the pixel garden.</desc>
<style>text{{font-family:ui-monospace,SFMono-Regular,Menlo,monospace}}.plant{{transform-box:fill-box;transform-origin:bottom;animation:g 2.8s ease-in-out var(--delay) infinite alternate}}@keyframes g{{to{{transform:translateY(-2px) scaleY(1.08)}}}}</style>
<rect width="760" height="230" rx="18" fill="#0b1118" stroke="#263645"/><text x="28" y="32" fill="#8ab4ff" font-size="14">GITHUB // COMMIT GARDEN</text><text x="28" y="52" fill="#dbe7f3" font-size="12">{esc(title)}</text>
<path d="M28 166H732" stroke="#31513f" stroke-width="3"/><path d="M28 169Q190 184 370 168T732 171" fill="none" stroke="#183828" stroke-width="13"/>{''.join(cells)}{''.join(plants)}
<text x="28" y="205" fill="#6f8498" font-size="10">updated {now} · plants bloom when activity spikes</text><text x="600" y="205" fill="#57e389" font-size="10">■ growing</text>
</svg>'''
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    main()
