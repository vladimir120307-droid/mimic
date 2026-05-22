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
                style=Style(font_size=14, foreground_color="#64748B", text_align="center"),
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
                        style=Style(font_size=20, font_weight="bold", foreground_color="#FFFFFF"),
                    ),
                ],
            ),
            WidgetNode(
                id="hero_card",
                kind="card",
                bounds=_bb(0.05, 0.12, 0.9, 0.18),
                style=Style(background_color="#EEF2FF", border_radius=16, padding=(16, 16, 16, 16)),
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
                style=Style(font_size=15, foreground_color="#94A3B8", text_align="center"),
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


def _chat_flow() -> WidgetTree:
    inbox_root = WidgetNode(
        id="inbox_root",
        kind="column",
        bounds=_bb(0, 0, 1, 1),
        style=Style(background_color="#FFFFFF"),
        children=[
            WidgetNode(
                id="inbox_app_bar",
                kind="app_bar",
                bounds=_bb(0, 0, 1, 0.08),
                text="Messages",
                style=Style(background_color="#0EA5E9", foreground_color="#FFFFFF"),
            ),
            WidgetNode(
                id="search_field",
                kind="text_field",
                placeholder="Search conversations",
                bounds=_bb(0.04, 0.1, 0.92, 0.06),
            ),
            WidgetNode(
                id="threads",
                kind="list",
                bounds=_bb(0.04, 0.18, 0.92, 0.75),
                children=[
                    WidgetNode(
                        id=f"thread_{i}",
                        kind="list_item",
                        bounds=_bb(0, i * 0.18, 1, 0.16),
                        text=name,
                        style=Style(font_size=15, font_weight="500"),
                    )
                    for i, name in enumerate(["Anna", "Boris", "Team", "Mike", "Family"])
                ],
            ),
        ],
    )
    chat_root = WidgetNode(
        id="chat_root",
        kind="column",
        bounds=_bb(0, 0, 1, 1),
        style=Style(background_color="#F1F5F9"),
        children=[
            WidgetNode(
                id="chat_app_bar",
                kind="app_bar",
                bounds=_bb(0, 0, 1, 0.08),
                text="Anna",
                style=Style(background_color="#0EA5E9", foreground_color="#FFFFFF"),
            ),
            WidgetNode(
                id="msg_in_1",
                kind="card",
                bounds=_bb(0.04, 0.15, 0.6, 0.08),
                text="Hey, free for lunch?",
                style=Style(background_color="#FFFFFF", border_radius=16, padding=(12, 12, 12, 12)),
            ),
            WidgetNode(
                id="msg_out_1",
                kind="card",
                bounds=_bb(0.36, 0.25, 0.6, 0.08),
                text="Yes! 12:30 at the usual?",
                style=Style(
                    background_color="#0EA5E9",
                    foreground_color="#FFFFFF",
                    border_radius=16,
                    padding=(12, 12, 12, 12),
                ),
            ),
            WidgetNode(
                id="msg_in_2",
                kind="card",
                bounds=_bb(0.04, 0.35, 0.6, 0.08),
                text="Perfect, see you there",
                style=Style(background_color="#FFFFFF", border_radius=16, padding=(12, 12, 12, 12)),
            ),
            WidgetNode(
                id="composer",
                kind="text_field",
                placeholder="Type a message",
                bounds=_bb(0.04, 0.9, 0.78, 0.07),
            ),
            WidgetNode(
                id="send",
                kind="fab",
                bounds=_bb(0.84, 0.9, 0.12, 0.07),
                icon_name="send",
                style=Style(background_color="#0EA5E9", foreground_color="#FFFFFF"),
            ),
        ],
    )
    return WidgetTree(
        screens=[
            Screen(id="inbox", name="Inbox", root=inbox_root),
            Screen(id="chat", name="Chat", root=chat_root),
        ],
        interactions=[
            Interaction(kind="tap", source_widget_id="thread_0", target_screen_id="chat"),
            Interaction(kind="tap", source_widget_id="thread_1", target_screen_id="chat"),
            Interaction(kind="tap", source_widget_id="thread_2", target_screen_id="chat"),
        ],
        target_platform="mobile",
    )


def _calendar_flow() -> WidgetTree:
    month_root = WidgetNode(
        id="month_root",
        kind="column",
        bounds=_bb(0, 0, 1, 1),
        style=Style(background_color="#FFFFFF"),
        children=[
            WidgetNode(
                id="cal_app_bar",
                kind="app_bar",
                bounds=_bb(0, 0, 1, 0.08),
                text="May 2026",
                style=Style(background_color="#10B981", foreground_color="#FFFFFF"),
            ),
            WidgetNode(
                id="weekdays",
                kind="row",
                bounds=_bb(0, 0.1, 1, 0.05),
                children=[
                    WidgetNode(
                        id=f"wd_{d}",
                        kind="text",
                        text=d,
                        bounds=_bb(i * 0.14, 0, 0.14, 1),
                        style=Style(font_size=12, foreground_color="#64748B", text_align="center"),
                    )
                    for i, d in enumerate(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
                ],
            ),
            WidgetNode(
                id="grid",
                kind="list",
                bounds=_bb(0, 0.18, 1, 0.55),
                children=[
                    WidgetNode(
                        id=f"day_{n}",
                        kind="list_item",
                        bounds=_bb((n % 7) * 0.14, (n // 7) * 0.15, 0.14, 0.13),
                        text=str(n + 1),
                        style=Style(text_align="center", font_size=14),
                    )
                    for n in range(28)
                ],
            ),
            WidgetNode(
                id="next_event",
                kind="card",
                bounds=_bb(0.04, 0.78, 0.92, 0.15),
                style=Style(
                    background_color="#ECFDF5",
                    border_radius=16,
                    padding=(16, 16, 16, 16),
                ),
                children=[
                    WidgetNode(
                        id="event_title",
                        kind="text",
                        text="Next: Design review",
                        bounds=_bb(0, 0, 1, 0.4),
                        style=Style(font_size=16, font_weight="bold"),
                    ),
                    WidgetNode(
                        id="event_time",
                        kind="text",
                        text="Tomorrow, 10:00",
                        bounds=_bb(0, 0.45, 1, 0.4),
                        style=Style(font_size=13, foreground_color="#64748B"),
                    ),
                ],
            ),
        ],
    )
    detail_root = WidgetNode(
        id="event_detail_root",
        kind="column",
        bounds=_bb(0, 0, 1, 1),
        style=Style(background_color="#FFFFFF"),
        children=[
            WidgetNode(
                id="event_app_bar",
                kind="app_bar",
                bounds=_bb(0, 0, 1, 0.08),
                text="Design review",
                style=Style(background_color="#10B981", foreground_color="#FFFFFF"),
            ),
            WidgetNode(
                id="event_when",
                kind="text",
                text="Friday May 22, 10:00 — 11:00",
                bounds=_bb(0.05, 0.12, 0.9, 0.05),
                style=Style(font_size=16),
            ),
            WidgetNode(
                id="event_where",
                kind="text",
                text="Conference room B / Zoom",
                bounds=_bb(0.05, 0.18, 0.9, 0.05),
                style=Style(font_size=14, foreground_color="#64748B"),
            ),
            WidgetNode(
                id="join_button",
                kind="button",
                text="Join meeting",
                bounds=_bb(0.05, 0.3, 0.9, 0.07),
                style=Style(background_color="#10B981", foreground_color="#FFFFFF"),
            ),
        ],
    )
    return WidgetTree(
        screens=[
            Screen(id="month", name="Month", root=month_root),
            Screen(id="event_detail", name="Event Detail", root=detail_root),
        ],
        interactions=[
            Interaction(kind="tap", source_widget_id="next_event", target_screen_id="event_detail"),
        ],
        target_platform="mobile",
    )


def _ecommerce_flow() -> WidgetTree:
    def product(idx: int, title: str, price: str) -> WidgetNode:
        return WidgetNode(
            id=f"prod_{idx}",
            kind="card",
            bounds=_bb((idx % 2) * 0.48, (idx // 2) * 0.3, 0.46, 0.28),
            style=Style(
                background_color="#FFFFFF",
                border_radius=12,
                padding=(12, 12, 12, 12),
                shadow=True,
            ),
            children=[
                WidgetNode(
                    id=f"prod_img_{idx}",
                    kind="container",
                    bounds=_bb(0, 0, 1, 0.6),
                    style=Style(background_color="#E2E8F0", border_radius=8),
                ),
                WidgetNode(
                    id=f"prod_title_{idx}",
                    kind="text",
                    text=title,
                    bounds=_bb(0, 0.62, 1, 0.18),
                    style=Style(font_size=14, font_weight="500"),
                ),
                WidgetNode(
                    id=f"prod_price_{idx}",
                    kind="text",
                    text=price,
                    bounds=_bb(0, 0.82, 1, 0.15),
                    style=Style(
                        font_size=15,
                        font_weight="bold",
                        foreground_color="#E11D48",
                    ),
                ),
            ],
        )

    list_root = WidgetNode(
        id="catalog_root",
        kind="column",
        bounds=_bb(0, 0, 1, 1),
        style=Style(background_color="#F8FAFC"),
        children=[
            WidgetNode(
                id="catalog_app_bar",
                kind="app_bar",
                bounds=_bb(0, 0, 1, 0.08),
                text="Shop",
                style=Style(background_color="#FFFFFF", foreground_color="#0F172A"),
            ),
            WidgetNode(
                id="catalog_search",
                kind="text_field",
                placeholder="Search products",
                bounds=_bb(0.04, 0.1, 0.92, 0.06),
            ),
            WidgetNode(
                id="catalog_grid",
                kind="stack",
                bounds=_bb(0.02, 0.18, 0.96, 0.78),
                children=[
                    product(0, "Linen shirt", "$48"),
                    product(1, "Knit sweater", "$72"),
                    product(2, "Wool coat", "$195"),
                    product(3, "Cotton trousers", "$56"),
                ],
            ),
        ],
    )
    detail_root = WidgetNode(
        id="product_detail_root",
        kind="column",
        bounds=_bb(0, 0, 1, 1),
        style=Style(background_color="#FFFFFF"),
        children=[
            WidgetNode(
                id="detail_image",
                kind="container",
                bounds=_bb(0, 0, 1, 0.45),
                style=Style(background_color="#E2E8F0"),
            ),
            WidgetNode(
                id="detail_title",
                kind="text",
                text="Linen shirt",
                bounds=_bb(0.05, 0.48, 0.9, 0.06),
                style=Style(font_size=22, font_weight="bold"),
            ),
            WidgetNode(
                id="detail_price",
                kind="text",
                text="$48",
                bounds=_bb(0.05, 0.55, 0.9, 0.05),
                style=Style(font_size=18, foreground_color="#E11D48"),
            ),
            WidgetNode(
                id="detail_desc",
                kind="text",
                text="Soft, breathable linen with a relaxed cut. Ethically sourced.",
                bounds=_bb(0.05, 0.62, 0.9, 0.15),
                style=Style(font_size=14, foreground_color="#64748B"),
            ),
            WidgetNode(
                id="add_to_cart",
                kind="button",
                text="Add to cart",
                bounds=_bb(0.05, 0.88, 0.9, 0.07),
                style=Style(background_color="#0F172A", foreground_color="#FFFFFF"),
            ),
        ],
    )
    return WidgetTree(
        screens=[
            Screen(id="catalog", name="Catalog", root=list_root),
            Screen(id="product_detail", name="Product", root=detail_root),
        ],
        interactions=[
            Interaction(kind="tap", source_widget_id=f"prod_{i}", target_screen_id="product_detail")
            for i in range(4)
        ],
        target_platform="mobile",
    )


def _settings_screen() -> WidgetTree:
    root = WidgetNode(
        id="settings_root",
        kind="column",
        bounds=_bb(0, 0, 1, 1),
        style=Style(background_color="#F1F5F9"),
        children=[
            WidgetNode(
                id="settings_app_bar",
                kind="app_bar",
                bounds=_bb(0, 0, 1, 0.08),
                text="Settings",
                style=Style(background_color="#FFFFFF", foreground_color="#0F172A"),
            ),
            WidgetNode(
                id="profile_card",
                kind="card",
                bounds=_bb(0.04, 0.1, 0.92, 0.14),
                style=Style(background_color="#FFFFFF", border_radius=16, padding=(16, 16, 16, 16)),
                children=[
                    WidgetNode(
                        id="profile_name",
                        kind="text",
                        text="Vladimir",
                        bounds=_bb(0, 0, 1, 0.5),
                        style=Style(font_size=18, font_weight="bold"),
                    ),
                    WidgetNode(
                        id="profile_email",
                        kind="text",
                        text="vladimir@example.com",
                        bounds=_bb(0, 0.55, 1, 0.4),
                        style=Style(font_size=13, foreground_color="#64748B"),
                    ),
                ],
            ),
            WidgetNode(
                id="section_notifications",
                kind="card",
                bounds=_bb(0.04, 0.27, 0.92, 0.24),
                style=Style(background_color="#FFFFFF", border_radius=16, padding=(8, 16, 8, 16)),
                children=[
                    WidgetNode(
                        id="row_push",
                        kind="row",
                        bounds=_bb(0, 0, 1, 0.33),
                        children=[
                            WidgetNode(
                                id="push_label",
                                kind="text",
                                text="Push notifications",
                                bounds=_bb(0, 0, 0.75, 1),
                                style=Style(font_size=15),
                            ),
                            WidgetNode(
                                id="push_switch",
                                kind="switch",
                                bounds=_bb(0.78, 0.1, 0.2, 0.8),
                            ),
                        ],
                    ),
                    WidgetNode(
                        id="row_email",
                        kind="row",
                        bounds=_bb(0, 0.35, 1, 0.3),
                        children=[
                            WidgetNode(
                                id="email_label",
                                kind="text",
                                text="Email digest",
                                bounds=_bb(0, 0, 0.75, 1),
                                style=Style(font_size=15),
                            ),
                            WidgetNode(
                                id="email_switch",
                                kind="switch",
                                bounds=_bb(0.78, 0.1, 0.2, 0.8),
                            ),
                        ],
                    ),
                    WidgetNode(
                        id="row_dnd",
                        kind="row",
                        bounds=_bb(0, 0.7, 1, 0.3),
                        children=[
                            WidgetNode(
                                id="dnd_label",
                                kind="text",
                                text="Do not disturb",
                                bounds=_bb(0, 0, 0.75, 1),
                                style=Style(font_size=15),
                            ),
                            WidgetNode(
                                id="dnd_switch",
                                kind="switch",
                                bounds=_bb(0.78, 0.1, 0.2, 0.8),
                            ),
                        ],
                    ),
                ],
            ),
            WidgetNode(
                id="sign_out",
                kind="button",
                text="Sign out",
                bounds=_bb(0.04, 0.86, 0.92, 0.07),
                style=Style(background_color="#E11D48", foreground_color="#FFFFFF"),
            ),
        ],
    )
    return WidgetTree(
        screens=[Screen(id="settings", name="Settings", root=root)],
        target_platform="mobile",
    )


_FIXTURES = {
    "login": _login_screen(),
    "dashboard": _dashboard_flow(),
    "chat": _chat_flow(),
    "calendar": _calendar_flow(),
    "ecommerce": _ecommerce_flow(),
    "settings": _settings_screen(),
}


class MockVision(VisionProvider):
    """Returns hand-crafted fixtures keyed by `mock_name`.

    Convention: encode the desired fixture in `mock_name` (constructor arg).
    Default is "dashboard" — a two-screen flow that exercises navigation.
    """

    name = "mock"

    def __init__(self, fixture: str = "dashboard") -> None:
        if fixture not in _FIXTURES:
            raise ValueError(f"Unknown mock fixture {fixture!r}. Available: {sorted(_FIXTURES)}")
        self._fixture = fixture

    async def analyze(self, source: VisionInput) -> WidgetTree:
        return _FIXTURES[self._fixture].model_copy(deep=True)


def list_fixtures() -> list[str]:
    return sorted(_FIXTURES)


def get_fixture(name: str) -> WidgetTree:
    return _FIXTURES[name].model_copy(deep=True)
