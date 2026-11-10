#!/usr/bin/env python3
"""Generate animated SVG cards for the GitHub profile README."""

import os
import xml.sax.saxutils as sax
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CARDS = ROOT / "cards"

BG = "#F8FAFC"
PANEL = "#FFFFFF"
TEXT = "#172033"
MUTED = "#64748B"
BLUE = "#2563EB"
BLUE_DARK = "#1D4ED8"
BLUE_LIGHT = "#DBEAFE"
BORDER = "#E2E8F0"
STATIC = os.getenv("STATIC", "0") == "1"


def esc(value):
    return sax.escape(str(value))


def svg_start(width, height, title):
    return f"""<svg xmlns="http://www.w3.org/2000/svg"
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
        @media (prefers-reduced-motion: reduce) {{
          animate, animateTransform {{ display: none; }}
        }}
      </style>
      <linearGradient id="blueGlow" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%" stop-color="#60A5FA"/>
        <stop offset="100%" stop-color="{BLUE_DARK}"/>
      </linearGradient>
    </defs>
    """


def save_svg(filename, content):
    CARDS.mkdir(parents=True, exist_ok=True)
    (CARDS / filename).write_text(content + "</svg>", encoding="utf-8")
    print(f"Generated: cards/{filename}")


def rounded_background(width, height, radius=24):
    return f'<rect width="{width}" height="{height}" rx="{radius}" fill="{BG}"/>'


def animation(duration="3s"):
    if STATIC:
        return ""
    return (
        f'<animate attributeName="opacity" values="0.75;1;0.75" '
        f'dur="{duration}" repeatCount="indefinite"/>'
    )


def create_hero():
    width, height = 1500, 390
    s = svg_start(width, height, "Veer Harischandrakar — Developer Profile")
    s += rounded_background(width, height)
    s += '<circle cx="1320" cy="70" r="180" fill="#DBEAFE" opacity=".65"/>'
    s += '<circle cx="1400" cy="330" r="150" fill="#BFDBFE" opacity=".45"/>'
    s += f"""
    <text x="90" y="105" font-size="20" fill="{BLUE_DARK}"
          letter-spacing="4" font-weight="700">HELLO, I'M VEER</text>
    <text x="90" y="190" class="heading" font-size="68">
      Veer Harischandrakar
    </text>
    <text x="92" y="245" font-size="25" fill="{MUTED}">
      Computer Science &amp; Engineering · Developer · Builder
    </text>
    <text x="92" y="305" font-size="19" fill="{BLUE_DARK}">
      Generative AI  /  Agentic AI  /  Cloud Computing  /  Full-Stack
    </text>
    <rect x="90" y="335" width="110" height="5" rx="2.5" fill="{BLUE}"/>
    <circle cx="1290" cy="195" r="85" fill="none"
            stroke="{BLUE}" stroke-width="2" opacity=".25"/>
    <circle cx="1290" cy="195" r="65" fill="none"
            stroke="{BLUE}" stroke-width="2" opacity=".45"/>
    <circle cx="1290" cy="195" r="45" fill="url(#blueGlow)">
      {animation("4s")}
    </circle>
    <text x="1290" y="205" text-anchor="middle"
          font-size="30" fill="white" font-weight="700">V</text>
    """
    save_svg("hero.svg", s)


def create_focus_card(filename, title, subtitle, number, description):
    width, height = 500, 250
    s = svg_start(width, height, title)
    s += rounded_background(width, height, 22)
    s += f"""
    <rect x="1" y="1" width="498" height="248" rx="22"
          fill="none" stroke="{BORDER}"/>
    <text x="32" y="48" font-size="14" fill="{BLUE_DARK}"
          font-weight="700" letter-spacing="2">{number}</text>
    <text x="32" y="105" class="heading" font-size="38">{esc(title)}</text>
    <text x="32" y="145" font-size="18" fill="{MUTED}">{esc(subtitle)}</text>
    <text x="32" y="195" font-size="14" fill="{BLUE_DARK}">
      {esc(description)}
    </text>
    <circle cx="435" cy="45" r="9" fill="{BLUE}">
      {animation("2.5s")}
    </circle>
    """
    save_svg(filename, s)


def create_activity():
    width, height = 1500, 260
    s = svg_start(width, height, "GitHub Activity Summary")
    s += rounded_background(width, height)
    values = [
        ("CARD STATUS", "READY"),
        ("DATA SOURCE", "LOCAL"),
        ("TOKEN REQUIRED", "NO"),
    ]
    s += (
        f'<text x="65" y="60" font-size="16" fill="{MUTED}" '
        'letter-spacing="3">GITHUB ACTIVITY</text>'
    )
    for i, (label, value) in enumerate(values):
        x = 65 + i * 470
        s += f"""
        <rect x="{x}" y="90" width="420" height="125" rx="18"
              fill="{PANEL}" stroke="{BORDER}"/>
        <text x="{x + 28}" y="130" font-size="14" fill="{MUTED}"
              letter-spacing="1.5">{label}</text>
        <text x="{x + 28}" y="185" font-size="35"
              font-weight="700" fill="{BLUE_DARK}">{value}</text>
        """
    save_svg("activity.svg", s)


def create_project(filename, name, tagline, description, stack, index):
    width, height = 1500, 260
    s = svg_start(width, height, f"{name} — {tagline}")
    s += rounded_background(width, height)
    s += f"""
    <rect x="1" y="1" width="1498" height="258" rx="24"
          fill="none" stroke="{BORDER}"/>
    <text x="65" y="55" font-size="15" fill="{BLUE_DARK}"
          letter-spacing="3">FEATURED PROJECT  /  0{index}</text>
    <text x="65" y="120" font-size="43" font-weight="700"
          fill="{TEXT}">{esc(name)}</text>
    <text x="65" y="160" font-size="20" fill="{BLUE_DARK}">
      {esc(tagline)}
    </text>
    <text x="65" y="205" font-size="17" fill="{MUTED}">
      {esc(description)}
    </text>
    <rect x="1120" y="75" width="300" height="100" rx="18"
          fill="{BLUE_LIGHT}"/>
    <text x="1270" y="135" text-anchor="middle" font-size="19"
          font-weight="700" fill="{BLUE_DARK}">{esc(stack)}</text>
    """
    save_svg(filename, s)


def main():
    create_hero()
    create_focus_card(
        "build.svg", "BUILD", "Ideas into products", "01",
        "Full-stack apps · Developer tools"
    )
    create_focus_card(
        "explore.svg", "EXPLORE", "Intelligence through AI", "02",
        "Generative AI · Agentic systems"
    )
    create_focus_card(
        "connect.svg", "CONNECT", "Technology and community", "03",
        "Cloud · AWS · Collaboration"
    )
    create_activity()
    create_project(
        "repo-schema-view.svg", "Schema View",
        "Interactive Database Visualizer",
        "Explore database structures and visualize relationships.",
        "NEXT.JS / POSTGRESQL", 1
    )
    create_project(
        "repo-stockshift.svg", "StockShift AI",
        "Autonomous Inventory Intelligence",
        "AI-powered inventory and supply-chain management.",
        "NEXT.JS / AI", 2
    )
    create_project(
        "repo-codelens.svg", "CodeLens",
        "Real-time Code Complexity Visualization",
        "Understand code complexity through visual insights.",
        "CHROME / JAVASCRIPT", 3
    )
    create_project(
        "repo-vaultfs.svg", "VaultFS Core",
        "Secure File System Simulator",
        "A Java-based file system simulator and CLI project.",
        "JAVA", 4
    )
    print("\nAll 9 SVG cards generated successfully.")


if __name__ == "__main__":
    main()
