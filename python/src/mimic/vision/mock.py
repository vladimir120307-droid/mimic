"""Deterministic mock vision provider for tests and demos.

Returns hand-crafted WidgetTrees without calling any external API. Used by:

- `pytest` so tests can exercise the codegen pipeline end-to-end
- `mimic gen --provider mock` so users can try the tool without an API key
- example fixtures in `examples/`
"""

from __future__ import annotations

from mimic.models import (
    BoundingBox,
    Interaction,
    Screen,
    Style,
    WidgetNode,
    WidgetTree,
)
from mimic.vision.base import VisionInput, VisionProvider

_FIXTURES: dict[str, WidgetTree] = {}


def _bb(x: float, y: float, w: float, h: float) -> BoundingBox:
    return BoundingBox(x=x, y=y, width=w, height=h)


def _login_screen() -> WidgetTree:
    root = WidgetNode(
        id="login_root",
        kind="column",
        bounds=_bb(0, 0, 1, 1),
        style=Style(background_color="#F8FAFC", padding=(24, 24, 24, 24)),
        children=[
            WidgetNode(
                id="logo",
                kind="icon",
                icon_name="bolt",
                bounds=_bb(0.45, 0.15, 0.1, 0.08),
                style=Style(foreground_color="#6E56CF", font_size=48),
            ),
            WidgetNode(
                id="title",
                kind="text",
                text="Welcome back",
                bounds=_bb(0.1, 0.28, 0.8, 0.07),
                style=Style(font_size=28, font_weight="bold", text_align="center"),
            ),
            WidgetNode(
                id="subtitle",
                kind="text",
                text="Sign in to continue to your dashboard",
                bounds=_bb(0.1, 0.36, 0.8, 0.05),
                style=Style(
                    font_size=14, foreground_color="#64748B", text_align="center"
                ),
            ),
            WidgetNode(
                id="email_field",
                kind="text_field",
                placeholder="Email address",
                bounds=_bb(0.1, 0.45, 0.8, 0.06),
            ),
            WidgetNode(
                id="password_field",
                kind="text_field",
                placeholder="Password",
                bounds=_bb(0.1, 0.53, 0.8, 0.06),
            ),
            WidgetNode(
                id="sign_in_button",
                kind="button",
                text="Sign in",
                bounds=_bb(0.1, 0.63, 0.8, 0.07),
                style=Style(background_color="#6E56CF", foreground_color="#FFFFFF"),
            ),
            WidgetNode(
                id="signup_hint",
                kind="text",
                text="Don't have an account? Create one",
                bounds=_bb(0.1, 0.74, 0.8, 0.04),
                style=Style(font_size=13, foreground_color="#6E56CF", text_align="center"),
            ),
        ],
    )
    return WidgetTree(
        screens=[Screen(id="login", name="Login", root=root, background_color="#F8FAFC")],
        target_platform="mobile",
        aspect_ratio=9 / 19.5,
    )


def _dashboard_flow() -> WidgetTree:
    home_root = WidgetNode(
        id="home_root",
        kind="column",
        bounds=_bb(0, 0, 1, 1),
        style=Style(background_color="#FFFFFF"),
        children=[
            WidgetNode(
                id="app_bar",
                kind="app_bar",
                bounds=_bb(0, 0, 1, 0.08),
                style=Style(background_color="#6E56CF", foreground_color="#FFFFFF"),
                children=[
                    WidgetNode(
                        id="app_title",
                        kind="text",
                        text="mimic",
                        bounds=_bb(0.05, 0.02, 0.4, 0.04),
                        style=Style(font_size=20, font_weight="bold",
                                    foreground_color="#FFFFFF"),
                    ),
                ],
            ),
            WidgetNode(
                id="hero_card",
                kind="card",
                bounds=_bb(0.05, 0.12, 0.9, 0.18),
                style=Style(background_color="#EEF2FF", border_radius=16,
                            padding=(16, 16, 16, 16)),
                children=[
                    WidgetNode(
                        id="hero_text",
                        kind="text",
                        text="Good morning, Vladimir",
                        bounds=_bb(0, 0, 1, 0.4),
                        style=Style(font_size=22, font_weight="bold"),
                    ),
                ],
            ),
            WidgetNode(
                id="list",
                kind="list",
                bounds=_bb(0.05, 0.34, 0.9, 0.58),
                children=[
                    WidgetNode(
                        id="li1",
                        kind="list_item",
                        bounds=_bb(0, 0, 1, 0.12),
                        text="Recent activity",
                    ),
                    WidgetNode(
                        id="li2",
                        kind="list_item",
                        bounds=_bb(0, 0.13, 1, 0.12),
                        text="Saved projects",
                    ),
                    WidgetNode(
                        id="li3",
                        kind="list_item",
                        bounds=_bb(0, 0.26, 1, 0.12),
                        text="Settings",
                    ),
                ],
            ),
            WidgetNode(
                id="fab",
                kind="fab",
                bounds=_bb(0.82, 0.85, 0.12, 0.06),
                icon_name="add",
                style=Style(background_color="#6E56CF", foreground_color="#FFFFFF"),
            ),
        ],
    )

    details_root = WidgetNode(
        id="details_root",
        kind="column",
        bounds=_bb(0, 0, 1, 1),
        style=Style(background_color="#FFFFFF"),
        children=[
            WidgetNode(
                id="details_app_bar",
                kind="app_bar",
                bounds=_bb(0, 0, 1, 0.08),
                text="Recent activity",
                style=Style(background_color="#6E56CF", foreground_color="#FFFFFF"),
            ),
            WidgetNode(
                id="empty_state",
                kind="text",
                text="No activity yet — start recording to see something here",
                bounds=_bb(0.1, 0.45, 0.8, 0.1),
                style=Style(font_size=15, foreground_color="#94A3B8",
                            text_align="center"),
            ),
        ],
    )

    return WidgetTree(
        screens=[
            Screen(id="home", name="Home", root=home_root),
            Screen(id="details", name="Activity", root=details_root),
        ],
        interactions=[
            Interaction(kind="tap", source_widget_id="li1", target_screen_id="details"),
            Interaction(kind="tap", source_widget_id="fab", target_screen_id="details"),
        ],
        target_platform="mobile",
    )


_FIXTURES = {
    "login":     _login_screen(),
    "dashboard": _dashboard_flow(),
}


class MockVision(VisionProvider):
    """Returns hand-crafted fixtures keyed by `mock_name`.

    Convention: encode the desired fixture in `mock_name` (constructor arg).
    Default is "dashboard" — a two-screen flow that exercises navigation.
    """

    name = "mock"

    def __init__(self, fixture: str = "dashboard") -> None:
        if fixture not in _FIXTURES:
            raise ValueError(
                f"Unknown mock fixture {fixture!r}. Available: {sorted(_FIXTURES)}"
            )
        self._fixture = fixture

    async def analyze(self, source: VisionInput) -> WidgetTree:
        return _FIXTURES[self._fixture].model_copy(deep=True)


def list_fixtures() -> list[str]:
    return sorted(_FIXTURES)


def get_fixture(name: str) -> WidgetTree:
    return _FIXTURES[name].model_copy(deep=True)
