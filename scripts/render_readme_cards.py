
#!/usr/bin/env python3
"""
Veer Harischandrakar — GitHub Profile SVG Generator

Generates:
  hero.svg
  build.svg
  explore.svg
  connect.svg
  activity.svg
  heatmap.svg
  repo-schema-view.svg
  repo-stockshift.svg
  repo-codelens.svg
  repo-vaultfs.svg

Run:
  python scripts/render_readme_cards.py

Optional:
  GITHUB_TOKEN=your_token python scripts/render_readme_cards.py
  STATIC=1 python scripts/render_readme_cards.py
"""

import json
import os
import urllib.request
import xml.sax.saxutils as sax
from pathlib import Path
from datetime import date, timedelta
from collections import Counter

ROOT = Path(__file__).resolve().parent.parent
CARDS = ROOT / "cards"
DATA = ROOT / "data" / "contributions.json"

USERNAME = "Veer2401"

# Green theme
BG = "#F5F7F2"
PANEL = "#FFFFFF"
TEXT = "#17251B"
MUTED = "#718075"
GREEN = "#16A34A"
GREEN_DARK = "#087A35"
GREEN_LIGHT = "#DCFCE7"
BORDER = "#E2E9E1"

STATIC = os.getenv("STATIC", "0") == "1"


def esc(value):
    return sax.escape(str(value))


def svg_start(width, height, title):
    return f'''<svg xmlns="http://www.w3.org/2000/svg"
        xmlns:xlink="http://www.w3.org/1999/xlink"
        width="{width}" height="{height}"
        viewBox="0 0 {width} {height}" role="img"
        aria-label="{esc(title)}">
    <title>{esc(title)}</title>
    <defs>
      <style>
        text {{
          font-family: Inter, ui-sans-serif, system-ui, -apple-system,
                       BlinkMacSystemFont, "Segoe UI", sans-serif;
        }}
        .muted {{ fill: {MUTED}; }}
        .heading {{ fill: {TEXT}; font-weight: 700; }}
        .green {{ fill: {GREEN}; }}
        .fade {{ opacity: .65; }}
        @media (prefers-reduced-motion: reduce) {{
          animate, animateTransform {{ display: none; }}
        }}
      </style>
      <linearGradient id="greenGlow" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%" stop-color="#22C55E"/>
        <stop offset="100%" stop-color="#087A35"/>
      </linearGradient>
    </defs>
    '''


def svg_end():
    return "</svg>"


def save_svg(filename, content):
    CARDS.mkdir(parents=True, exist_ok=True)
    path = CARDS / filename
    path.write_text(content + svg_end(), encoding="utf-8")
    print(f"Generated: cards/{filename}")


def rounded_background(width, height, radius=24):
    return f'<rect width="{width}" height="{height}" rx="{radius}" fill="{BG}"/>'


def animation(element, duration="3s"):
    if STATIC:
        return ""
    return f'<animate attributeName="opacity" values="0.75;1;0.75" dur="{duration}" repeatCount="indefinite"/>'


# ---------------------------------------------------------
# Contribution data
# ---------------------------------------------------------

def fetch_github_contributions():
    """Fetch contribution data from GitHub GraphQL when a token is available."""
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        return None

    query = """
    query($user: String!) {
      user(login: $user) {
        contributionsCollection {
          contributionCalendar {
            totalContributions
            weeks {
              contributionDays {
                contributionCount
                date
              }
            }
          }
        }
      }
    }
    """

    payload = json.dumps({
        "query": query,
        "variables": {"user": USERNAME}
    }).encode("utf-8")

    request = urllib.request.Request(
        "https://api.github.com/graphql",
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "Veer2401-Profile-Generator"
        }
    )

    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            result = json.loads(response.read().decode("utf-8"))

        calendar = result["data"]["user"]["contributionsCollection"]["contributionCalendar"]

        data = {
            "total": calendar["totalContributions"],
            "weeks": [
                [
                    {
                        "date": day["date"],
                        "count": day["contributionCount"]
                    }
                    for day in week["contributionDays"]
                ]
                for week in calendar["weeks"]
            ]
        }

        DATA.parent.mkdir(parents=True, exist_ok=True)
        DATA.write_text(json.dumps(data, indent=2), encoding="utf-8")
        print("Fetched latest GitHub contribution data.")
        return data

    except Exception as error:
        print(f"GitHub API unavailable: {error}")
        return None


def load_contributions():
    fresh = fetch_github_contributions()
    if fresh:
        return fresh

    if DATA.exists():
        try:
            return json.loads(DATA.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass

    print("No contribution data found. Using an empty contribution calendar.")
    return {"total": 0, "weeks": []}


CONTRIBUTIONS = load_contributions()


def flatten_days():
    result = []
    for week in CONTRIBUTIONS.get("weeks", []):
        for day in week:
            if isinstance(day, dict):
                result.append({
                    "date": day.get("date", ""),
                    "count": int(day.get("count", day.get("contributionCount", 0)))
                })
            else:
                result.append({"date": "", "count": int(day)})
    return result


DAYS = flatten_days()
TOTAL = sum(day["count"] for day in DAYS)
ACTIVE_DAYS = sum(1 for day in DAYS if day["count"] > 0)


# ---------------------------------------------------------
# Hero card
# ---------------------------------------------------------

def create_hero():
    width, height = 1500, 390
    s = svg_start(width, height, "Veer Harischandrakar — Developer Profile")
    s += rounded_background(width, height)

    s += '<circle cx="1320" cy="70" r="180" fill="#DCFCE7" opacity=".65"/>'
    s += '<circle cx="1400" cy="330" r="150" fill="#BBF7D0" opacity=".45"/>'

    s += f'''
    <text x="90" y="105" font-size="20" fill="{GREEN_DARK}"
          letter-spacing="4" font-weight="700">HELLO, I'M VEER</text>
    <text x="90" y="190" class="heading" font-size="68">
      Veer Harischandrakar
    </text>
    <text x="92" y="245" font-size="25" fill="{MUTED}">
      Computer Science &amp; Engineering · Developer · Builder
    </text>
    <text x="92" y="305" font-size="19" fill="{GREEN_DARK}">
      Generative AI  /  Agentic AI  /  Cloud Computing  /  Full-Stack
    </text>
    <rect x="90" y="335" width="110" height="5" rx="2.5" fill="{GREEN}"/>
    <circle cx="1290" cy="195" r="85" fill="none"
            stroke="{GREEN}" stroke-width="2" opacity=".25"/>
    <circle cx="1290" cy="195" r="65" fill="none"
            stroke="{GREEN}" stroke-width="2" opacity=".45"/>
    <circle cx="1290" cy="195" r="45" fill="url(#greenGlow)">
      {animation('<circle/>', '4s')}
    </circle>
    <text x="1290" y="205" text-anchor="middle"
          font-size="30" fill="white" font-weight="700">V</text>
    '''
    save_svg("hero.svg", s)


# ---------------------------------------------------------
# Build / Explore / Connect cards
# ---------------------------------------------------------

def create_focus_card(filename, title, subtitle, number, description):
    width, height = 500, 250
    s = svg_start(width, height, title)
    s += rounded_background(width, height, 22)
    s += f'''
    <rect x="1" y="1" width="498" height="248" rx="22"
          fill="none" stroke="{BORDER}"/>
    <text x="32" y="48" font-size="14" fill="{GREEN_DARK}"
          font-weight="700" letter-spacing="2">{number}</text>
    <text x="32" y="105" class="heading" font-size="38">{esc(title)}</text>
    <text x="32" y="145" font-size="18" fill="{MUTED}">{esc(subtitle)}</text>
    <text x="32" y="195" font-size="14" fill="{GREEN_DARK}">
      {esc(description)}
    </text>
    <circle cx="435" cy="45" r="9" fill="{GREEN}">
      {animation('<circle/>', '2.5s')}
    </circle>
    '''
    save_svg(filename, s)


# ---------------------------------------------------------
# Activity summary
# ---------------------------------------------------------

def create_activity():
    width, height = 1500, 260
    s = svg_start(width, height, "GitHub Activity Summary")
    s += rounded_background(width, height)

    values = [
        ("TOTAL CONTRIBUTIONS", f"{TOTAL:,}"),
        ("ACTIVE DAYS", f"{ACTIVE_DAYS:,}"),
        ("DAILY AVERAGE", f"{TOTAL / max(len(DAYS), 1):.1f}"),
    ]

    s += f'<text x="65" y="60" font-size="16" fill="{MUTED}" letter-spacing="3">GITHUB ACTIVITY</text>'

    for i, (label, value) in enumerate(values):
        x = 65 + i * 470
        s += f'''
        <rect x="{x}" y="90" width="420" height="125" rx="18"
              fill="{PANEL}" stroke="{BORDER}"/>
        <text x="{x + 28}" y="130" font-size="14" fill="{MUTED}"
              letter-spacing="1.5">{label}</text>
        <text x="{x + 28}" y="185" font-size="43"
              font-weight="700" fill="{GREEN_DARK}">{value}</text>
        '''
    save_svg("activity.svg", s)


# ---------------------------------------------------------
# GitHub contribution heatmap
# ---------------------------------------------------------

def intensity(count):
    if count <= 0:
        return "#E5E7E4"
    if count <= 2:
        return "#BBF7D0"
    if count <= 5:
        return "#86EFAC"
    if count <= 9:
        return "#4ADE80"
    return "#15803D"


def create_heatmap():
    width, height = 1500, 410
    s = svg_start(width, height, "Every Day — GitHub Contributions")
    s += rounded_background(width, height, 24)

    # Exact requested title
    s += f'''
    <text x="72" y="100" font-size="54" fill="{TEXT}"
          font-family="Georgia, serif">Every Day</text>
    '''

    cell = 20
    gap = 6
    start_x = 72
    start_y = 160

    # GitHub contribution graph: 7 rows, up to 53 weeks.
    weeks = CONTRIBUTIONS.get("weeks", [])

    if weeks:
        normalized = []
        for week in weeks[-53:]:
            normalized.append([
                int(day.get("count", day.get("contributionCount", 0)))
                if isinstance(day, dict) else int(day)
                for day in week
            ])
    else:
        normalized = [[0] * 7 for _ in range(53)]

    while len(normalized) < 53:
        normalized.insert(0, [0] * 7)

    for col, week in enumerate(normalized[-53:]):
        for row in range(7):
            count = week[row] if row < len(week) else 0
            x = start_x + col * (cell + gap)
            y = start_y + row * (cell + gap)
            s += (
                f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" '
                f'rx="6" fill="{intensity(count)}">'
            )
            if not STATIC and count > 0:
                s += '<animate attributeName="opacity" values="0.85;1;0.85" dur="4s" repeatCount="indefinite"/>'
            s += '</rect>'

    # Month labels
    if DAYS:
        dates = [d["date"] for d in DAYS if d["date"]]
        if dates:
            first = date.fromisoformat(dates[0])
            labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                      "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            for col in range(53):
                current = first + timedelta(weeks=col)
                if current.day <= 7:
                    x = start_x + col * (cell + gap)
                    s += f'<text x="{x}" y="365" font-size="15" fill="{MUTED}">{labels[current.month - 1]}</text>'

    # Legend
    legend_x = 1080
    s += f'<text x="{legend_x - 48}" y="365" font-size="15" fill="{MUTED}">less</text>'

    for i, color in enumerate([
        "#E5E7E4", "#BBF7D0", "#86EFAC",
        "#4ADE80", "#22C55E", "#15803D"
    ]):
        x = legend_x + i * 27
        s += f'<rect x="{x}" y="346" width="19" height="19" rx="5" fill="{color}"/>'

    s += f'<text x="{legend_x + 170}" y="365" font-size="15" fill="{MUTED}">more</text>'

    save_svg("heatmap.svg", s)


# ---------------------------------------------------------
# Project cards
# ---------------------------------------------------------

def create_project(filename, name, tagline, description, stack, index):
    width, height = 1500, 260
    s = svg_start(width, height, f"{name} — {tagline}")
    s += rounded_background(width, height)

    s += f'''
    <rect x="1" y="1" width="1498" height="258" rx="24"
          fill="none" stroke="{BORDER}"/>
    <text x="65" y="55" font-size="15" fill="{GREEN_DARK}"
          letter-spacing="3">FEATURED PROJECT  /  0{index}</text>
    <text x="65" y="120" font-size="43" font-weight="700"
          fill="{TEXT}">{esc(name)}</text>
    <text x="65" y="160" font-size="20" fill="{GREEN_DARK}">
      {esc(tagline)}
    </text>
    <text x="65" y="205" font-size="17" fill="{MUTED}">
      {esc(description)}
    </text>
    <rect x="1120" y="75" width="300" height="100" rx="18"
          fill="{GREEN_LIGHT}"/>
    <text x="1270" y="135" text-anchor="middle" font-size="19"
          font-weight="700" fill="{GREEN_DARK}">{esc(stack)}</text>
    '''
    save_svg(filename, s)


# ---------------------------------------------------------
# Generate all cards
# ---------------------------------------------------------

def main():
    create_hero()

    create_focus_card(
        "build.svg",
        "BUILD",
        "Ideas into products",
        "01",
        "Full-stack apps · Developer tools"
    )

    create_focus_card(
        "explore.svg",
        "EXPLORE",
        "Intelligence through AI",
        "02",
        "Generative AI · Agentic systems"
    )

    create_focus_card(
        "connect.svg",
        "CONNECT",
        "Technology and community",
        "03",
        "Cloud · AWS · Collaboration"
    )

    create_activity()
    create_heatmap()

    create_project(
        "repo-schema-view.svg",
        "Schema View",
        "Interactive Database Visualizer",
        "Explore database structures and visualize relationships.",
        "NEXT.JS / POSTGRESQL",
        1
    )

    create_project(
        "repo-stockshift.svg",
        "StockShift AI",
        "Autonomous Inventory Intelligence",
        "AI-powered inventory and supply-chain management.",
        "NEXT.JS / AI",
        2
    )

    create_project(
        "repo-codelens.svg",
        "CodeLens",
        "Real-time Code Complexity Visualization",
        "Understand code complexity through visual insights.",
        "CHROME / JAVASCRIPT",
        3
    )

    create_project(
        "repo-vaultfs.svg",
        "VaultFS Core",
        "Secure File System Simulator",
        "A Java-based file system simulator and CLI project.",
        "JAVA",
        4
    )

    print("\nAll 10 SVG cards generated successfully.")


if __name__ == "__main__":
    main()
