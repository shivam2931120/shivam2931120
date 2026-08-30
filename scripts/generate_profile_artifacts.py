#!/usr/bin/env python3
"""Render the small animated dashboard panels used by the profile README."""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets"
QUOTES = [
    ("The best interface is the one that gets out of the way.", "— Golden rule of shipping"),
    ("Make it work. Make it clear. Then make it delightful.", "— The builder's loop"),
    ("A small deployed feature beats a perfect unfinished idea.", "— Production wisdom"),
    ("Good systems make hard things feel ordinary.", "— Backend philosophy"),
]


def esc(value: str) -> str:
    return (str(value).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def latest_commit() -> tuple[str, str]:
    try:
        data = json.loads(os.environ.get("LATEST_COMMIT", "{}"))
        message = data.get("message", "latest changes")
        sha = data.get("sha", "------")[:7]
    except json.JSONDecodeError:
        message, sha = "latest changes", "------"
    return " ".join(message.split())[:62], sha


def render() -> None:
    month = int(os.environ.get("MONTHLY_COUNT", "0") or 0)
    try:
        days = json.loads(os.environ.get("CONTRIBUTIONS", "[]"))
    except json.JSONDecodeError:
        days = []
    total = sum(int(day.get("contributionCount", 0)) for day in days)
    recent = days[-42:]
    active_days = sum(1 for day in recent if int(day.get("contributionCount", 0)) > 0)
    message, sha = latest_commit()
    quote_index = int(os.environ.get("QUOTE_INDEX", "0") or 0) % len(QUOTES)
    month_label = datetime.now(timezone.utc).strftime("%B %Y").upper()

    if month >= 40:
        weather, icon, color, forecast = "SUNNY", "☀", "#f6c453", "high shipping pressure"
    elif month >= 15:
        weather, icon, color, forecast = "PARTLY CLOUDY", "◒", "#8ab4ff", "steady commits incoming"
    elif month:
        weather, icon, color, forecast = "LIGHT DRIZZLE", "☂", "#69e6a1", "small steps still count"
    else:
        weather, icon, color, forecast = "CALM", "○", "#6f8498", "the next idea is loading"

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "latest-commit.svg").write_text(f'''<svg xmlns="http://www.w3.org/2000/svg" width="760" height="118" viewBox="0 0 760 118" role="img" aria-label="Latest GitHub commit terminal log">
<style>text{{font-family:ui-monospace,SFMono-Regular,Menlo,monospace}}.cursor{{animation:b 1s steps(2) infinite}}@keyframes b{{50%{{opacity:0}}}}</style><rect width="760" height="118" rx="16" fill="#0b1118" stroke="#263645"/><circle cx="28" cy="27" r="6" fill="#ff7b72"/><circle cx="48" cy="27" r="6" fill="#f6c453"/><circle cx="68" cy="27" r="6" fill="#57e389"/><text x="28" y="57" fill="#69e6a1" font-size="12">shivam@github:~$ git log -1 --oneline</text><text x="28" y="82" fill="#dbe7f3" font-size="13">{esc(sha)}  {esc(message)}</text><text x="28" y="102" fill="#8ab4ff" font-size="11">&gt; stream: live profile telemetry<span class="cursor">_</span></text></svg>''', encoding="utf-8")

    (OUT / "coding-weather.svg").write_text(f'''<svg xmlns="http://www.w3.org/2000/svg" width="370" height="150" viewBox="0 0 370 150" role="img" aria-label="Monthly coding weather: {esc(weather)}">
<style>text{{font-family:ui-monospace,SFMono-Regular,Menlo,monospace}}.cloud{{animation:d 4s ease-in-out infinite alternate}}@keyframes d{{to{{transform:translateX(8px)}}}}</style><rect width="370" height="150" rx="16" fill="#0b1118" stroke="#263645"/><text x="22" y="29" fill="#8ab4ff" font-size="12">CODING WEATHER // {month_label}</text><text x="26" y="78" fill="{color}" font-size="38" class="cloud">{icon}</text><text x="82" y="72" fill="{color}" font-size="17">{weather}</text><text x="22" y="106" fill="#dbe7f3" font-size="12">{month} contributions this month</text><text x="22" y="128" fill="#6f8498" font-size="10">forecast: {forecast}</text></svg>''', encoding="utf-8")

    quote_text, author = QUOTES[quote_index]
    next_text, next_author = QUOTES[(quote_index + 1) % len(QUOTES)]
    (OUT / "developer-quotes.svg").write_text(f'''<svg xmlns="http://www.w3.org/2000/svg" width="760" height="112" viewBox="0 0 760 112" role="img" aria-label="Rotating developer quote">
<style>text{{font-family:ui-monospace,SFMono-Regular,Menlo,monospace}}.q1{{animation:q 12s infinite}}.q2{{animation:q 12s 6s infinite;opacity:0}}@keyframes q{{0%,45%{{opacity:1}}50%,95%,100%{{opacity:0}}}}</style><rect width="760" height="112" rx="16" fill="#0b1118" stroke="#263645"/><text x="28" y="29" fill="#ff7b72" font-size="12">// RANDOM TRANSMISSION</text><g class="q1"><text x="28" y="63" fill="#dbe7f3" font-size="15">“{esc(quote_text)}”</text><text x="28" y="88" fill="#8ab4ff" font-size="11">{esc(author)}</text></g><g class="q2"><text x="28" y="63" fill="#dbe7f3" font-size="15">“{esc(next_text)}”</text><text x="28" y="88" fill="#8ab4ff" font-size="11">{esc(next_author)}</text></g></svg>''', encoding="utf-8")

    meteors = []
    for index, day in enumerate(recent):
        count = int(day.get("contributionCount", 0))
        if count:
            x, y = 40 + (index * 17) % 680, 58 + (index * 31) % 74
            meteors.append(f'<g class="m" style="--delay:{index * .19:.2f}s"><path d="M{x} {y}l-18 18" stroke="#8ab4ff" stroke-width="2"/><circle cx="{x}" cy="{y}" r="{2 + min(count, 4)}" fill="#f6c453"/></g>')
    (OUT / "commit-meteor-shower.svg").write_text(f'''<svg xmlns="http://www.w3.org/2000/svg" width="760" height="170" viewBox="0 0 760 170" role="img" aria-label="Commit meteor shower from recent GitHub activity">
<style>text{{font-family:ui-monospace,SFMono-Regular,Menlo,monospace}}.m{{animation:fall 3.8s linear var(--delay) infinite;opacity:0}}@keyframes fall{{0%{{transform:translate(-24px,-24px);opacity:0}}15%{{opacity:1}}70%,100%{{transform:translate(35px,35px);opacity:0}}}}</style><rect width="760" height="170" rx="16" fill="#0b1118" stroke="#263645"/><text x="28" y="31" fill="#f6c453" font-size="13">COMMIT METEOR SHOWER</text><text x="28" y="51" fill="#6f8498" font-size="11">{active_days} active days detected in the last 6 weeks · every spark is a commit day</text>{''.join(meteors)}<path d="M40 140h680" stroke="#173b34" stroke-width="2"/><text x="28" y="157" fill="#69e6a1" font-size="10">activity enters orbit → ideas become releases</text></svg>''', encoding="utf-8")

    if total >= 1000:
        stage, title, accessory = "MAX LEVEL", "SHIPMASTER", '<path d="M333 77h94l-12 18h-70Z" fill="#f6c453"/><circle cx="380" cy="72" r="8" fill="#ff7b72"/>'
    elif total >= 500:
        stage, title, accessory = "LEVEL 3", "SYSTEM ARCHITECT", '<path d="M338 78h84v17h-84Z" fill="#8ab4ff"/><path d="M380 61v17" stroke="#8ab4ff" stroke-width="5"/>'
    elif total >= 100:
        stage, title, accessory = "LEVEL 2", "PRODUCT BUILDER", '<path d="M342 83h76v12h-76Z" fill="#69e6a1"/>'
    else:
        stage, title, accessory = "LEVEL 1", "CODE EXPLORER", '<circle cx="380" cy="85" r="9" fill="#f6c453"/>'
    (OUT / "pixel-avatar-evolution.svg").write_text(f'''<svg xmlns="http://www.w3.org/2000/svg" width="760" height="180" viewBox="0 0 760 180" role="img" aria-label="Pixel avatar evolution: {esc(title)}">
<style>text{{font-family:ui-monospace,SFMono-Regular,Menlo,monospace}}.a{{animation:bob 2s ease-in-out infinite alternate}}@keyframes bob{{to{{transform:translateY(-5px)}}}}</style><rect width="760" height="180" rx="16" fill="#0b1118" stroke="#263645"/><text x="28" y="31" fill="#ff7b72" font-size="13">PIXEL AVATAR EVOLUTION // {stage}</text><text x="28" y="53" fill="#dbe7f3" font-size="12">{esc(title)} · {total} total contributions mapped to XP</text><g class="a"><rect x="344" y="63" width="72" height="50" fill="#8ab4ff"/><rect x="354" y="51" width="52" height="14" fill="#69e6a1"/><rect x="356" y="75" width="12" height="10" fill="#0b1118"/><rect x="392" y="75" width="12" height="10" fill="#0b1118"/><rect x="368" y="96" width="24" height="7" fill="#ff7b72"/>{accessory}</g><path d="M250 131h260" stroke="#263645"/><text x="28" y="157" fill="#6f8498" font-size="10">next evolution unlocks at the next contribution milestone</text></svg>''', encoding="utf-8")

    fish = []
    for index in range(min(9, 2 + active_days // 4)):
        x, y = 72 + (index * 79) % 610, 79 + (index * 37) % 45
        color = ["#8ab4ff", "#f6c453", "#ff7b72", "#69e6a1"][index % 4]
        fish.append(f'<g class="fish" style="--delay:{index * .5:.1f}s"><path d="M{x} {y}q18 -13 36 0q-18 13 -36 0Z" fill="{color}"/><path d="M{x} {y}l-10 -9v18Z" fill="{color}"/><circle cx="{x + 27}" cy="{y - 2}" r="2" fill="#0b1118"/></g>')
    (OUT / "contribution-aquarium.svg").write_text(f'''<svg xmlns="http://www.w3.org/2000/svg" width="760" height="190" viewBox="0 0 760 190" role="img" aria-label="Contribution aquarium with fish grown from coding activity">
<style>text{{font-family:ui-monospace,SFMono-Regular,Menlo,monospace}}.fish{{animation:swim 5s ease-in-out var(--delay) infinite alternate}}.bubble{{animation:rise 3s linear infinite}}@keyframes swim{{to{{transform:translateX(28px)}}}}@keyframes rise{{to{{transform:translateY(-45px);opacity:0}}}}</style><rect width="760" height="190" rx="16" fill="#071923" stroke="#263645"/><text x="28" y="31" fill="#69e6a1" font-size="13">CONTRIBUTION AQUARIUM</text><text x="28" y="51" fill="#6f8498" font-size="11">{active_days} active days → {len(fish)} new fish in the tank</text><path d="M28 155h704" stroke="#176b4d" stroke-width="12"/><path d="M75 145v-45l10-12 10 12v45m550 0V88l9-11 10 11v57" stroke="#173b34" stroke-width="9" fill="none"/>{''.join(fish)}<circle class="bubble" cx="155" cy="135" r="3" fill="#8ab4ff"/><circle class="bubble" cx="590" cy="135" r="3" fill="#8ab4ff"/><text x="28" y="178" fill="#8ab4ff" font-size="10">feed the aquarium with commits · keep shipping to unlock rare species</text></svg>''', encoding="utf-8")

    prophecies = [
        "today's bug is tomorrow's architecture lesson",
        "the next commit contains a plot twist",
        "ship the small version before the idea grows teeth",
        "your terminal knows the way; follow the green build",
        "a clean API is hiding behind one more refactor",
    ]
    prophecy = prophecies[(datetime.now(timezone.utc).timetuple().tm_yday + total) % len(prophecies)]
    (OUT / "daily-terminal-prophecy.svg").write_text(f'''<svg xmlns="http://www.w3.org/2000/svg" width="760" height="116" viewBox="0 0 760 116" role="img" aria-label="Daily terminal prophecy">
<style>text{{font-family:ui-monospace,SFMono-Regular,Menlo,monospace}}.cursor{{animation:b 1s steps(2) infinite}}@keyframes b{{50%{{opacity:0}}}}</style><rect width="760" height="116" rx="16" fill="#0b1118" stroke="#263645"/><text x="28" y="31" fill="#8ab4ff" font-size="12">DAILY TERMINAL PROPHECY // {datetime.now(timezone.utc).strftime('%Y-%m-%d')}</text><text x="28" y="63" fill="#69e6a1" font-size="13">&gt; oracle --today</text><text x="28" y="88" fill="#dbe7f3" font-size="14">{esc(prophecy)}<span class="cursor">_</span></text></svg>''', encoding="utf-8")

    windows = []
    for x in range(22, 740, 28):
        for y in range(91, 150, 18):
            if (x * 3 + y) % 7 in (0, 2):
                windows.append(f'<rect x="{x}" y="{y}" width="7" height="6" fill="#f6c453" opacity=".8"><animate attributeName="opacity" values=".25;.9;.25" dur="{2 + (x + y) % 4}s" repeatCount="indefinite"/></rect>')
    (OUT / "bengaluru-skyline.svg").write_text(f'''<svg xmlns="http://www.w3.org/2000/svg" width="760" height="190" viewBox="0 0 760 190" role="img" aria-label="Animated pixel-art Bengaluru skyline">
<rect width="760" height="190" rx="16" fill="#0b1118" stroke="#263645"/><text x="28" y="31" fill="#8ab4ff" font-family="monospace" font-size="13">BENGALURU // NIGHT BUILD</text><circle cx="675" cy="46" r="19" fill="#f6c453" opacity=".85"/><path d="M0 162H760" stroke="#31513f" stroke-width="4"/><g fill="#173b34"><path d="M20 162V91h72v71Z"/><path d="M106 162V61h90v101Z"/><path d="M210 162V103h62v59Z"/><path d="M286 162V76h108v86Z"/><path d="M410 162V47h56v115Z"/><path d="M480 162V88h82v74Z"/><path d="M578 162V68h126v94Z"/><path d="M720 162V105h40v57Z"/></g>{''.join(windows)}<path d="M0 166h760v24H0Z" fill="#10251f"/><text x="28" y="181" fill="#69e6a1" font-family="monospace" font-size="10">signals: online · city: awake · next deploy: pending</text></svg>''', encoding="utf-8")


if __name__ == "__main__":
    render()
