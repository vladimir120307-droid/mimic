"""Structured representation of a captured UI.

A `WidgetTree` is the contract between vision adapters (which produce it) and
code generators (which consume it). Every vision backend must return this
shape; every codegen target accepts this shape. The vision layer never emits
target-framework strings directly — that is codegen's job.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

WidgetKind = Literal[
    "container",
    "row",
    "column",
    "stack",
    "text",
    "image",
    "icon",
    "button",
    "text_field",
    "checkbox",
    "switch",
    "slider",
    "list",
    "list_item",
    "card",
    "app_bar",
    "tab_bar",
    "bottom_nav",
    "fab",
    "scroll_view",
    "spacer",
    "divider",
    "unknown",
]

InteractionKind = Literal[
    "tap",
    "long_press",
    "double_tap",
    "scroll",
    "drag",
    "text_input",
    "focus",
    "navigate",
]


class BoundingBox(BaseModel):
    x: float
    y: float
    width: float
    height: float


class Style(BaseModel):
    background_color: str | None = None
    foreground_color: str | None = None
    border_color: str | None = None
    border_width: float | None = None
    border_radius: float | None = None
    padding: tuple[float, float, float, float] | None = None
    margin: tuple[float, float, float, float] | None = None
    font_size: float | None = None
    font_weight: str | None = None
    text_align: Literal["left", "center", "right", "justify"] | None = None
    opacity: float | None = None
    shadow: bool = False


class WidgetNode(BaseModel):
    id: str
    kind: WidgetKind
    bounds: BoundingBox
    text: str | None = None
    placeholder: str | None = None
    icon_name: str | None = None
    image_url: str | None = None
    style: Style = Field(default_factory=Style)
    children: list[WidgetNode] = Field(default_factory=list)
    role: str | None = None
    semantic_label: str | None = None


class Interaction(BaseModel):
    kind: InteractionKind
    source_widget_id: str
    target_screen_id: str | None = None
    text_value: str | None = None
    metadata: dict[str, str] = Field(default_factory=dict)


class Screen(BaseModel):
    id: str
    name: str
    root: WidgetNode
    background_color: str | None = None
    safe_area: BoundingBox | None = None


class WidgetTree(BaseModel):
    """Top-level capture result: one or more screens plus transitions between them."""

    screens: list[Screen]
    interactions: list[Interaction] = Field(default_factory=list)
    target_platform: Literal["mobile", "desktop", "web", "unknown"] = "unknown"
    aspect_ratio: float | None = None

    @property
    def initial_screen(self) -> Screen:
        return self.screens[0]
