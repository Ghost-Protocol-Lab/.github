"""Palette and SVG helpers for the Ghost Protocol Labs profile art (standard library only)."""
from __future__ import annotations

from pathlib import Path
from xml.sax.saxutils import escape as esc

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "profile" / "assets"

BG = "#0b0d10"       # near-black
FOG = "#1a1f26"      # fog gray
GHOST = "#e6f1ef"    # ghost white
GREEN = "#39ff9c"    # spectral green
PURPLE = "#8b5cf6"   # ghost purple
BLOOD = "#b0212d"    # blood red (sparingly)
MUTED = "#8b9a96"    # secondary text

# System fonts only: SVGs shown through <img> on GitHub cannot load web fonts.
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'DejaVu Sans Mono', monospace"
SERIF = "Georgia, 'Times New Roman', serif"


def glow_filter(fid: str = "glow", std: float = 2.5) -> str:
    return (
        f'<filter id="{fid}" x="-60%" y="-60%" width="220%" height="220%">'
        f'<feGaussianBlur stdDeviation="{std}" result="b"/>'
        f'<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
    )


def tombstone_path(x: float, y: float, w: float, h: float) -> str:
    """Rounded-top tombstone with its bottom-left corner at (x, y+h)."""
    r = w / 2
    return f"M{x:.2f},{y + h:.2f} V{y + r:.2f} A{r:.2f},{r:.2f} 0 0 1 {x + w:.2f},{y + r:.2f} V{y + h:.2f} Z"


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    try:
        shown = path.resolve().relative_to(ROOT)
    except ValueError:
        shown = path
    print(f"wrote {shown}")
