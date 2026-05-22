"""Extract a theme (palette + typography) from a WidgetTree.

A `Theme` is a derived view of the input — repeated colors and font sizes
are consolidated into a small named palette so generators can emit
`Theme.of(context).colorScheme.primary` (Flutter), CSS custom properties
(HTML), or a Tailwind config `theme.extend.colors` block (React).

The extraction is intentionally heuristic — we want generated code to read
like a human wrote it, not like a 1:1 dump of input pixel colors.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field

from mimic.models import Style, WidgetNode, WidgetTree


@dataclass
class Theme:
    primary: str | None    = None
    secondary: str | None  = None
    surface: str | None    = None
    on_surface: str | None = None
    error: str | None      = None
    background: str | None = None
    extra: dict[str, str]  = field(default_factory=dict)
    body_font_size: float | None  = None
    title_font_size: float | None = None

    def named_colors(self) -> dict[str, str]:
        out: dict[str, str] = {}
        for name in ("primary", "secondary", "surface", "on_surface", "error", "background"):
            v = getattr(self, name)
            if v:
                out[name] = v
        out.update(self.extra)
        return out

    def color_to_name(self) -> dict[str, str]:
        return {v: k for k, v in self.named_colors().items()}


def extract(tree: WidgetTree) -> Theme:
    """Scan the tree and pick a small named palette."""
    counts: Counter[str] = Counter()
    for screen in tree.screens:
        if screen.background_color:
            counts[_norm(screen.background_color)] += 3  # weight bg highly
        _walk(screen.root, counts)

    palette_pairs = counts.most_common(8)
    palette = [c for c, _ in palette_pairs if c]

    theme = Theme()
    if palette:
        theme.background = palette[0]
    if len(palette) >= 2:
        theme.surface = palette[1] if _is_light(palette[1]) else palette[0]
    if len(palette) >= 3:
        # Pick the most-saturated non-neutral color as primary.
        accents = [c for c in palette if _saturation(c) > 0.2]
        if accents:
            theme.primary = accents[0]
        if len(accents) >= 2:
            theme.secondary = accents[1]
    error = next(
        (c for c in palette if _is_redish(c) and c != theme.primary),
        None,
    )
    if error:
        theme.error = error

    if theme.background and _is_dark(theme.background):
        theme.on_surface = "#F8FAFC"
    else:
        theme.on_surface = "#0F172A"

    font_sizes = Counter[float]()
    for screen in tree.screens:
        _collect_font_sizes(screen.root, font_sizes)
    if font_sizes:
        common = font_sizes.most_common(2)
        theme.body_font_size = common[0][0]
        if len(common) > 1:
            theme.title_font_size = max(s for s, _ in common)

    return theme


def _walk(node: WidgetNode, counts: Counter[str]) -> None:
    for color in (
        node.style.background_color,
        node.style.foreground_color,
        node.style.border_color,
    ):
        if color:
            counts[_norm(color)] += 1
    for child in node.children:
        _walk(child, counts)


def _collect_font_sizes(node: WidgetNode, sizes: Counter[float]) -> None:
    if node.style.font_size is not None:
        sizes[float(node.style.font_size)] += 1
    for child in node.children:
        _collect_font_sizes(child, sizes)


def _norm(c: str) -> str:
    c = c.strip()
    if c.startswith("#"):
        return c.upper()
    return c


def _rgb(c: str) -> tuple[int, int, int] | None:
    if not c.startswith("#"):
        return None
    h = c.lstrip("#")
    if len(h) == 3:
        h = "".join(ch * 2 for ch in h)
    if len(h) not in {6, 8}:
        return None
    try:
        r = int(h[0:2], 16)
        g = int(h[2:4], 16)
        b = int(h[4:6], 16)
    except ValueError:
        return None
    return r, g, b


def _is_light(c: str) -> bool:
    rgb = _rgb(c)
    if not rgb:
        return True
    r, g, b = rgb
    luma = (r * 299 + g * 587 + b * 114) / 1000
    return luma > 180


def _is_dark(c: str) -> bool:
    rgb = _rgb(c)
    if not rgb:
        return False
    r, g, b = rgb
    luma = (r * 299 + g * 587 + b * 114) / 1000
    return luma < 60


def _saturation(c: str) -> float:
    rgb = _rgb(c)
    if not rgb:
        return 0.0
    r, g, b = rgb
    mx, mn = max(r, g, b), min(r, g, b)
    return (mx - mn) / 255.0 if mx else 0.0


def _is_redish(c: str) -> bool:
    rgb = _rgb(c)
    if not rgb:
        return False
    r, g, b = rgb
    return r > 150 and r > g + 40 and r > b + 40
