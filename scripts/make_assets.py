#!/usr/bin/env python3
"""Generate the Ghost Protocol Labs profile art: hero banner, section headers, divider and footer.

Only needs re-running when you change the text or the theme:

    python scripts/make_assets.py

Edit TAGLINE, TITLES (the rotating typed line) or HEADERS below, then re-run.
All SVGs are self-contained: system fonts only, SMIL animation only, no scripts, no external references.
"""
from __future__ import annotations

import random
import sys

from theme import ASSETS, BG, BLOOD, FOG, GHOST, GREEN, MONO, MUTED, PURPLE, SERIF, esc, glow_filter, tombstone_path, write_text

NAME = "GHOST PROTOCOL LABS"
TAGLINE = "Unseen.  Unheard.  Unrelenting."
TITLES = [  # the rotating, typed line in the hero
    "> Red Team Engagements",
    "> Web & Application Pentesting",
    "> Network & Infrastructure",
    "> OSINT & Recon Assessment",
    "> Custom Red Team Tooling",
    "> Free Writeups & Activities",
]
HEADERS = [  # (file key, title, epitaph)
    ("about", "UNSEEN. UNHEARD. UNRELENTING.", "No theater. No noise."),
    ("services", "WHAT WE DO", "Authorized. Scoped. Accountable."),
    ("lab", "IN THE LAB", "Tools on the roadmap. All of them planned."),
    ("free", "FREE FOR EVERYONE", "No scope call required."),
    ("rules", "CODE OF THE CRYPT", "Authorized targets only. Always."),
    ("connect", "MAKE CONTACT", "Start with the contact page on our website."),
]

# --- shared building blocks ---------------------------------------------------------
GHOST_PATH = (
    "M28 2 C13 2 4 14 4 30 L4 64 C4 68 8 69 10.5 66 L15 61 L20 68 L25 62 L28 67 "
    "L31 62 L36 68 L41 61 L45.5 66 C48 69 52 68 52 64 L52 30 C52 14 43 2 28 2 Z"
)


def common_defs() -> str:
    return (
        "<defs>"
        + glow_filter("glow", 2.4)
        + glow_filter("glowBig", 6)
        + '<filter id="ghostGlow" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="3.2" result="b"/>'
        '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
        + '<filter id="fogBlur" x="-30%" y="-80%" width="160%" height="260%"><feGaussianBlur stdDeviation="13"/></filter>'
        + '<linearGradient id="ghostFill" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f4fffb" stop-opacity="0.96"/><stop offset="1" stop-color="#bfe9dc" stop-opacity="0.5"/></linearGradient>'
        + f'<linearGradient id="panel" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#12171d"/><stop offset="1" stop-color="{BG}"/></linearGradient>'
        + f'<g id="ghost"><path d="{GHOST_PATH}" fill="url(#ghostFill)"/>'
        f'<ellipse cx="20" cy="31" rx="4" ry="6" fill="{BG}"/><ellipse cx="36" cy="31" rx="4" ry="6" fill="{BG}"/>'
        f'<circle cx="21" cy="29" r="1.3" fill="{GREEN}"/><circle cx="37" cy="29" r="1.3" fill="{GREEN}"/>'
        f'<ellipse cx="28" cy="46" rx="3.6" ry="5" fill="{BG}" opacity="0.85"/></g>'
        + "</defs>"
    )


def float_anim(amp: float, dur: float, begin: float = 0.0, sway: float = 0.0) -> str:
    xs = f"0 0;{sway} {-amp};0 0" if sway else f"0 0;0 {-amp};0 0"
    return (
        f'<animateTransform attributeName="transform" type="translate" values="{xs}" keyTimes="0;0.5;1" '
        f'calcMode="spline" keySplines="0.45 0 0.55 1;0.45 0 0.55 1" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/>'
    )


def ghost(x: float, y: float, s: float = 1.0, op: float = 1.0, amp: float = 8, dur: float = 4.2, begin: float = 0.0, sway: float = 0.0) -> str:
    return (
        f'<g transform="translate({x:g},{y:g})" opacity="{op}"><g>{float_anim(amp, dur, begin, sway)}'
        f'<g transform="scale({s})"><use xlink:href="#ghost" filter="url(#ghostGlow)"/></g></g></g>'
    )


def tomb_shape(kind: str, x: float, base: float, w: float, h: float) -> str:
    if kind == "round":
        return tombstone_path(x, base - h, w, h)
    if kind == "cross":
        a, cx, arm = w * 0.3, x + w / 2, base - h * 0.62
        return (f"M{cx - a / 2:.1f},{base} V{arm:.1f} H{x:.1f} V{arm - a:.1f} H{cx - a / 2:.1f} V{base - h:.1f} "
                f"H{cx + a / 2:.1f} V{arm - a:.1f} H{x + w:.1f} V{arm:.1f} H{cx + a / 2:.1f} V{base:.1f} Z")
    if kind == "obelisk":
        return (f"M{x + w * .15:.1f},{base} L{x + w * .3:.1f},{base - h * .85:.1f} L{x + w / 2:.1f},{base - h:.1f} "
                f"L{x + w * .7:.1f},{base - h * .85:.1f} L{x + w * .85:.1f},{base} Z")
    return (f"M{x:.1f},{base} V{base - h * .8:.1f} L{x + w * .15:.1f},{base - h:.1f} H{x + w * .85:.1f} "
            f"L{x + w:.1f},{base - h * .8:.1f} V{base} Z")  # slab


def tombs(items, fill: str, stroke: str | None = None, rip: bool = False) -> str:
    out = []
    for i, (kind, x, base, w, h) in enumerate(items):
        st = f' stroke="{stroke}" stroke-width="1"' if stroke else ""
        out.append(f'<path d="{tomb_shape(kind, x, base, w, h)}" fill="{fill}"{st}/>')
        if rip and kind in ("round", "slab") and i % 2 == 0:
            out.append(f'<text x="{x + w / 2:.1f}" y="{base - h * 0.45:.1f}" font-family="{MONO}" font-size="{max(w * 0.22, 5):.1f}" fill="#3b4854" text-anchor="middle">RIP</text>')
    return "".join(out)


def dead_tree(x: float, base: float, s: float = 1.0, flip: bool = False) -> str:
    sx = -s if flip else s
    return (
        f'<g transform="translate({x},{base}) scale({sx},{s})" stroke="#06080a" stroke-linecap="round" fill="none">'
        '<path d="M0 0 C-3 -45 4 -85 0 -135" stroke-width="9"/>'
        '<path d="M1 -88 C-14 -102 -26 -106 -40 -124" stroke-width="4"/>'
        '<path d="M1 -108 C16 -122 28 -126 40 -146" stroke-width="3.5"/>'
        '<path d="M-1 -58 C-16 -66 -24 -68 -36 -82" stroke-width="3"/>'
        '<path d="M-40 -124 C-44 -134 -48 -138 -52 -146 M-40 -124 C-34 -134 -34 -140 -30 -148" stroke-width="2"/>'
        '<path d="M40 -146 C42 -156 46 -160 50 -168 M40 -146 C34 -154 32 -160 30 -168" stroke-width="2"/>'
        '<path d="M0 -135 C-4 -148 -2 -156 -6 -166 M0 -135 C5 -146 8 -152 12 -160" stroke-width="2.4"/></g>'
    )


def fog(cx: float, cy: float, rx: float, ry: float, op: float, dist: float, dur: float, color: str = "#cfe8e0") -> str:
    return (
        f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{color}" opacity="{op}" filter="url(#fogBlur)">'
        f'<animateTransform attributeName="transform" type="translate" values="{-dist} 0;{dist} 0;{-dist} 0" keyTimes="0;0.5;1" '
        f'calcMode="spline" keySplines="0.45 0 0.55 1;0.45 0 0.55 1" dur="{dur}s" repeatCount="indefinite"/></ellipse>'
    )


def stars(w: int, h: int, n: int, seed: int = 7) -> str:
    rng = random.Random(seed)
    out = []
    for _ in range(n):
        x, y, r = rng.uniform(8, w - 8), rng.uniform(6, h * 0.55), rng.choice([0.6, 0.8, 1.0, 1.3])
        lo, hi = rng.uniform(0.15, 0.35), rng.uniform(0.6, 0.95)
        out.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="#dff7ef" opacity="{hi:.2f}">'
            f'<animate attributeName="opacity" values="{hi:.2f};{lo:.2f};{hi:.2f}" dur="{rng.uniform(2.4, 6):.1f}s" begin="{rng.uniform(0, 4):.1f}s" repeatCount="indefinite"/></circle>'
        )
    return "".join(out)


def typing_block(titles: list[str], cx: float, y: float, fs: float = 18) -> str:
    """Typewriter effect with SMIL: each title is clipped by an animated-width rect, then erased."""
    cw = fs * 0.6
    slot, typ, hold, erase = 3.4, 1.2, 1.4, 0.6
    total = slot * len(titles)
    out = []
    for i, t in enumerate(titles):
        length = len(t) * cw
        x0 = cx - length / 2
        t0 = i * slot
        kt = ";".join(f"{k / total:.4f}" for k in (0, t0, t0 + typ, t0 + typ + hold, t0 + typ + hold + erase, total))
        out.append(
            f'<clipPath id="tc{i}"><rect x="{x0:.1f}" y="{y - fs:.1f}" height="{fs * 1.5:.1f}" width="0">'
            f'<animate attributeName="width" values="0;0;{length:.1f};{length:.1f};0;0" keyTimes="{kt}" dur="{total}s" repeatCount="indefinite"/></rect></clipPath>'
            f'<text x="{x0:.1f}" y="{y}" font-family="{MONO}" font-size="{fs}" fill="{GREEN}" textLength="{length:.1f}" lengthAdjust="spacing" clip-path="url(#tc{i})" filter="url(#glow)">{esc(t)}</text>'
        )
        vis = ";".join(f"{k / total:.4f}" for k in (0, t0, t0 + typ + hold + erase, total))
        out.append(
            f'<g opacity="0"><animate attributeName="opacity" values="0;1;0;0" keyTimes="{vis}" calcMode="discrete" dur="{total}s" repeatCount="indefinite"/>'
            f'<g><animate attributeName="opacity" values="1;0" keyTimes="0;0.5" calcMode="discrete" dur="0.9s" repeatCount="indefinite"/>'
            f'<rect x="{x0:.1f}" y="{y - fs + 2:.1f}" width="9" height="{fs * 1.1:.1f}" fill="{GREEN}">'
            f'<animate attributeName="x" values="{x0:.1f};{x0:.1f};{x0 + length:.1f};{x0 + length:.1f};{x0:.1f};{x0:.1f}" keyTimes="{kt}" dur="{total}s" repeatCount="indefinite"/></rect></g></g>'
        )
    return "".join(out)


# --- hero -----------------------------------------------------------------------------
def hero_body(w: int = 900, h: int = 340) -> str:
    back = [("round", 40, 292, 30, 42), ("cross", 100, 290, 28, 50), ("slab", 150, 296, 34, 40), ("obelisk", 214, 294, 26, 52),
            ("round", 262, 298, 26, 30), ("round", 640, 298, 28, 32), ("slab", 690, 296, 34, 44), ("cross", 748, 292, 30, 54),
            ("round", 800, 294, 32, 46), ("obelisk", 852, 296, 24, 42)]
    front = [("round", -6, 346, 46, 64), ("cross", 70, 346, 40, 66), ("slab", 190, 346, 48, 40), ("round", 740, 346, 50, 56),
             ("cross", 820, 346, 42, 70), ("slab", 868, 346, 44, 50)]
    return (
        f'<rect width="{w}" height="{h}" fill="url(#heroSky)"/>'
        + stars(w, h, 46)
        # moon
        + '<g><circle cx="742" cy="92" r="78" fill="url(#moonHalo)"><animate attributeName="opacity" values="0.8;1;0.8" dur="7s" repeatCount="indefinite"/></circle>'
        '<circle cx="742" cy="92" r="38" fill="url(#moonFill)"/>'
        '<circle cx="730" cy="82" r="7" fill="#a9cdc2" opacity="0.45"/><circle cx="752" cy="104" r="9" fill="#a9cdc2" opacity="0.38"/>'
        '<circle cx="756" cy="78" r="4" fill="#a9cdc2" opacity="0.4"/><circle cx="728" cy="106" r="3.5" fill="#a9cdc2" opacity="0.35"/></g>'
        + '<path d="M0 256 C120 226 220 266 340 246 C470 220 560 262 690 242 C790 226 850 250 900 240 V340 H0 Z" fill="#0b0f14"/>'
        + dead_tree(58, 306, 1.0) + dead_tree(846, 306, 0.9, flip=True)
        + fog(300, 262, 300, 26, 0.07, 70, 19) + fog(640, 270, 280, 24, 0.06, 80, 23)
        + tombs(back, "#121820", "#202a35", rip=True)
        + ghost(46, 92, 1.15, 0.95, 10, 4.6, 0.0, 4) + ghost(792, 168, 0.8, 0.7, 8, 5.4, 1.3, -3) + ghost(640, 78, 0.5, 0.38, 6, 6.2, 2.1, 3) + ghost(262, 60, 0.42, 0.3, 5, 5.0, 0.7, -2)
        # name, tagline, typed line
        + f'<g font-family="{MONO}" text-anchor="middle" font-weight="bold" font-size="44" letter-spacing="3">'
        f'<text x="446" y="150" fill="{PURPLE}" opacity="0.55">{NAME}<animate attributeName="x" values="446;446;442;451;446;446" keyTimes="0;0.9;0.93;0.96;0.98;1" dur="5.5s" repeatCount="indefinite"/></text>'
        f'<text x="454" y="150" fill="{GREEN}" opacity="0.5">{NAME}<animate attributeName="x" values="454;454;458;449;454;454" keyTimes="0;0.9;0.93;0.96;0.98;1" dur="5.5s" repeatCount="indefinite"/></text>'
        f'<text x="450" y="150" fill="{GHOST}" filter="url(#glowBig)">{NAME}'
        '<animate attributeName="opacity" values="1;1;0.82;1;0.9;1;1" keyTimes="0;0.55;0.57;0.6;0.62;0.65;1" dur="7s" repeatCount="indefinite"/></text></g>'
        + f'<text x="450" y="190" font-family="{MONO}" font-size="17" letter-spacing="2.5" fill="{GHOST}" fill-opacity="0.88" text-anchor="middle" xml:space="preserve">{esc(TAGLINE)}</text>'
        + f'<line x1="330" y1="206" x2="570" y2="206" stroke="{GREEN}" stroke-opacity="0.35"/>'
        + typing_block(TITLES, 450, 236)
        # ground, foreground tombstones, front fog
        + '<path d="M0 304 C150 294 300 310 450 302 C600 294 750 310 900 300 V340 H0 Z" fill="#06080a"/>'
        + tombs(front, "#05070a")
        + fog(200, 318, 330, 22, 0.1, 90, 21) + fog(700, 322, 320, 20, 0.09, 80, 26)
        + f'<rect width="{w}" height="{h}" fill="url(#vignette)"/>'
        + f'<rect x="0" y="{h - 2}" width="{w}" height="2" fill="url(#edge)"/>'
    )


def hero_defs() -> str:
    return (
        "<defs>"
        '<linearGradient id="heroSky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#05070a"/><stop offset="0.55" stop-color="#0b1016"/><stop offset="1" stop-color="#1b2c34"/></linearGradient>'
        '<radialGradient id="moonHalo"><stop offset="0" stop-color="#39ff9c" stop-opacity="0.28"/><stop offset="0.6" stop-color="#39ff9c" stop-opacity="0.07"/><stop offset="1" stop-color="#39ff9c" stop-opacity="0"/></radialGradient>'
        '<radialGradient id="moonFill" cx="0.4" cy="0.38"><stop offset="0" stop-color="#f7fffc"/><stop offset="1" stop-color="#c3e2d8"/></radialGradient>'
        '<radialGradient id="vignette" cx="0.5" cy="0.5" r="0.75"><stop offset="0.6" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity="0.55"/></radialGradient>'
        f'<linearGradient id="edge" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{PURPLE}" stop-opacity="0"/><stop offset="0.5" stop-color="{GREEN}"/><stop offset="1" stop-color="{PURPLE}" stop-opacity="0"/></linearGradient>'
        "</defs>"
    )


def hero_svg() -> str:
    w, h = 900, 340
    head = (
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="t d">'
        f'<title id="t">{NAME} - {esc(TAGLINE)}</title>'
        f'<desc id="d">A moonlit graveyard with drifting fog and floating ghosts. {NAME}: {esc(TAGLINE)} Authorized security engagements.</desc>'
    )
    return head + common_defs() + hero_defs() + hero_body(w, h) + "</svg>\n"



# --- headers, divider, footer ----------------------------------------------------------------
def header_svg(title: str, epitaph: str) -> str:
    w, h = 830, 76
    cross = lambda x, y, o: f'<path d="M{x},{y} v14 M{x - 4.5},{y + 5} h9" stroke="{GREEN}" stroke-width="1.4" stroke-linecap="round" opacity="{o}"/>'  # noqa: E731
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="t">'
        f'<title id="t">{esc(title)}</title>' + common_defs()
        + f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="14" fill="url(#panel)" stroke="{FOG}"/>'
        + f'<path d="{tombstone_path(24, 9, 38, 58)}" fill="#141a20" stroke="{GREEN}" stroke-width="1.5" filter="url(#glow)"/>'
        + f'<path d="M43,20 v14 M38,25 h10" stroke="{GREEN}" stroke-width="1.6" stroke-linecap="round"/>'
        + f'<text x="43" y="52" font-family="{MONO}" font-size="8.5" fill="{MUTED}" text-anchor="middle" letter-spacing="1.5">RIP</text>'
        + f'<text x="84" y="37" font-family="{MONO}" font-size="22" font-weight="bold" letter-spacing="3.5" fill="{GREEN}" filter="url(#glow)">{esc(title)}</text>'
        + f'<text x="85" y="58" font-family="{MONO}" font-size="12.5" font-style="italic" fill="{MUTED}">{esc(epitaph)}</text>'
        + cross(700, 30, 0.25) + cross(724, 40, 0.18) + cross(668, 42, 0.14)
        + ghost(770, 14, 0.5, 0.85, 5, 3.8, 0.4, 2)
        + "</svg>\n"
    )


def divider_svg() -> str:
    w, h = 830, 44
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="divider">'
        f'<defs><linearGradient id="l" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{GREEN}" stop-opacity="0"/><stop offset="1" stop-color="{GREEN}" stop-opacity="0.6"/></linearGradient>'
        f'<linearGradient id="r" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{GREEN}" stop-opacity="0.6"/><stop offset="1" stop-color="{GREEN}" stop-opacity="0"/></linearGradient>'
        + glow_filter("g", 2.2) + "</defs>"
        f'<rect x="40" y="21.5" width="340" height="1" fill="url(#l)"/><rect x="450" y="21.5" width="340" height="1" fill="url(#r)"/>'
        f'<path d="{tombstone_path(404, 6, 22, 30)}" fill="#141a20" stroke="{GREEN}" stroke-width="1.4" filter="url(#g)"/>'
        f'<path d="M415,13 v10 M411,17 h8" stroke="{GREEN}" stroke-width="1.4" stroke-linecap="round"/>'
        f'<path d="M392,30 v8 M389.5,33 h5 M438,30 v8 M435.5,33 h5" stroke="{GREEN}" stroke-width="1.2" stroke-linecap="round" opacity="0.5"/>'
        "</svg>\n"
    )


def footer_svg() -> str:
    w, h = 830, 200
    back = [("round", 30, 176, 30, 44), ("cross", 84, 172, 28, 56), ("slab", 128, 178, 34, 40), ("obelisk", 176, 176, 26, 58),
            ("round", 600, 178, 30, 40), ("slab", 650, 174, 34, 50), ("cross", 704, 172, 30, 60), ("round", 760, 176, 34, 46)]
    front = [("round", -4, 206, 50, 70), ("cross", 70, 206, 40, 62), ("slab", 720, 206, 54, 56), ("round", 790, 206, 50, 74)]
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="t">'
        '<title id="t">Authorized engagements only.</title>' + common_defs()
        + '<defs><linearGradient id="fsky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#090c10"/><stop offset="1" stop-color="#16222a"/></linearGradient>'
        f'<linearGradient id="edge" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{PURPLE}" stop-opacity="0"/><stop offset="0.5" stop-color="{GREEN}"/><stop offset="1" stop-color="{PURPLE}" stop-opacity="0"/></linearGradient></defs>'
        + f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="14" fill="url(#fsky)" stroke="{FOG}"/>'
        + stars(w, h, 26, seed=21)
        + '<path d="M0 150 C140 132 260 160 400 146 C540 130 680 160 830 142 V200 H0 Z" fill="#0b0f14"/>'
        + tombs(back, "#121820", "#202a35", rip=True)
        + ghost(64, 40, 0.8, 0.8, 8, 4.8, 0.3, 3) + ghost(722, 34, 0.62, 0.55, 7, 5.6, 1.4, -3)
        + f'<text x="415" y="88" font-family="{MONO}" font-size="21" font-weight="bold" letter-spacing="4" fill="{GREEN}" text-anchor="middle" filter="url(#glow)">AUTHORIZED ENGAGEMENTS ONLY.</text>'
        + f'<text x="415" y="112" font-family="{MONO}" font-size="12.5" letter-spacing="2" fill="{MUTED}" text-anchor="middle">Ghost Protocol Labs  ·  GHPL  ·  No theater. No noise.</text>'
        + '<path d="M0 176 C140 168 300 182 450 174 C600 166 720 182 830 172 V200 H0 Z" fill="#06080a"/>'
        + tombs(front, "#05070a")
        + fog(220, 186, 280, 18, 0.1, 80, 22) + fog(620, 190, 260, 16, 0.09, 70, 27)
        + f'<rect x="14" y="{h - 3}" width="{w - 28}" height="2" fill="url(#edge)"/>'
        + "</svg>\n"
    )



def main() -> int:
    write_text(ASSETS / "hero.svg", hero_svg())
    for key, title, epitaph in HEADERS:
        write_text(ASSETS / f"header-{key}.svg", header_svg(title, epitaph))
    write_text(ASSETS / "divider.svg", divider_svg())
    write_text(ASSETS / "footer.svg", footer_svg())
    return 0


if __name__ == "__main__":
    sys.exit(main())
