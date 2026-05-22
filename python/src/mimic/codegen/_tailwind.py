"""Shared Tailwind-class derivation used by HTML and React generators.

Maps the framework-agnostic `Style` model to a list of Tailwind utility
classes. Centralized so improvements to mapping benefit both targets.
"""

from __future__ import annotations

from mimic.models import Style, WidgetKind


def style_classes(style: Style, kind: WidgetKind | None = None) -> list[str]:
    classes: list[str] = []

    if style.background_color:
        classes.append(_color_class("bg", style.background_color))
    if style.foreground_color:
        classes.append(_color_class("text", style.foreground_color))
    if style.border_color:
        classes.append(_color_class("border", style.border_color))
    if style.border_width is not None and style.border_width > 0:
        classes.append(f"border-{_size_step(style.border_width)}")
    if style.border_radius is not None:
        classes.append(_radius_class(style.border_radius))
    if style.opacity is not None:
        classes.append(f"opacity-{max(0, min(100, int(style.opacity * 100)))}")
    if style.shadow:
        classes.append("shadow-md")

    if style.padding:
        t, r, b, lf = style.padding
        if t == r == b == lf:
            classes.append(f"p-{_spacing_step(t)}")
        else:
            classes += [
                f"pt-{_spacing_step(t)}",
                f"pr-{_spacing_step(r)}",
                f"pb-{_spacing_step(b)}",
                f"pl-{_spacing_step(lf)}",
            ]

    if style.margin:
        t, r, b, lf = style.margin
        if t == r == b == lf:
            classes.append(f"m-{_spacing_step(t)}")
        else:
            classes += [
                f"mt-{_spacing_step(t)}",
                f"mr-{_spacing_step(r)}",
                f"mb-{_spacing_step(b)}",
                f"ml-{_spacing_step(lf)}",
            ]

    if style.font_size is not None:
        classes.append(_text_size_class(style.font_size))
    if style.font_weight in {"bold", "700", "800", "900"}:
        classes.append("font-bold")
    elif style.font_weight in {"500", "600", "medium", "semibold"}:
        classes.append("font-semibold")

    if style.text_align:
        classes.append(f"text-{style.text_align}")

    return classes


def layout_classes(kind: WidgetKind) -> list[str]:
    match kind:
        case "row":
            return ["flex", "flex-row", "items-center", "gap-2"]
        case "column":
            return ["flex", "flex-col", "gap-2"]
        case "stack":
            return ["relative"]
        case "list":
            return ["flex", "flex-col", "gap-1", "divide-y", "divide-slate-200"]
        case "card":
            return ["rounded-2xl", "bg-white", "shadow-sm", "p-4"]
        case "app_bar":
            return [
                "w-full",
                "px-4",
                "py-3",
                "flex",
                "items-center",
                "justify-between",
            ]
        case "fab":
            return [
                "fixed",
                "bottom-6",
                "right-6",
                "w-14",
                "h-14",
                "rounded-full",
                "shadow-lg",
                "flex",
                "items-center",
                "justify-center",
            ]
        case "scroll_view":
            return ["overflow-y-auto"]
        case "divider":
            return ["h-px", "w-full", "bg-slate-200"]
        case "spacer":
            return ["flex-1"]
        case _:
            return []


def _spacing_step(px: float) -> int:
    # Tailwind step ≈ 4px
    return max(0, min(96, round(px / 4)))


def _size_step(px: float) -> int:
    return max(0, min(8, round(px)))


def _radius_class(radius: float) -> str:
    if radius <= 0:
        return "rounded-none"
    if radius <= 4:
        return "rounded-sm"
    if radius <= 8:
        return "rounded"
    if radius <= 12:
        return "rounded-lg"
    if radius <= 20:
        return "rounded-xl"
    if radius <= 32:
        return "rounded-2xl"
    return "rounded-full"


def _text_size_class(px: float) -> str:
    table = [
        (12, "text-xs"),
        (14, "text-sm"),
        (16, "text-base"),
        (18, "text-lg"),
        (20, "text-xl"),
        (24, "text-2xl"),
        (30, "text-3xl"),
        (36, "text-4xl"),
        (48, "text-5xl"),
        (60, "text-6xl"),
    ]
    for limit, cls in table:
        if px <= limit:
            return cls
    return "text-6xl"


def _color_class(prefix: str, value: str) -> str:
    """Use Tailwind arbitrary-value syntax for unknown colors.

    Maps common color words to Tailwind palette where obvious; otherwise
    emits `bg-[#hex]` (arbitrary value). Reliable but not pretty.
    """
    v = value.strip()
    palette = {
        "white":       "white",
        "black":       "black",
        "transparent": "transparent",
    }
    lower = v.lower()
    if lower in palette:
        return f"{prefix}-{palette[lower]}"
    if v.startswith("#"):
        return f"{prefix}-[{v}]"
    if v.startswith("rgb"):
        compact = v.replace(" ", "")
        return f"{prefix}-[{compact}]"
    return f"{prefix}-[{v}]"
