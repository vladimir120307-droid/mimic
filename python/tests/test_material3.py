"""Verify the Material 3 button heuristic picks the right Flutter button class."""

from mimic.codegen.flutter import FlutterGenerator
from mimic.models import (
    BoundingBox,
    Screen,
    Style,
    WidgetNode,
    WidgetTree,
)


def _tree_with_button(style: Style, *, text: str = "Tap", icon: str | None = None) -> WidgetTree:
    root = WidgetNode(
        id="root",
        kind="column",
        bounds=BoundingBox(x=0, y=0, width=1, height=1),
        children=[
            WidgetNode(
                id="btn",
                kind="button",
                bounds=BoundingBox(x=0, y=0, width=1, height=0.1),
                text=text or None,
                icon_name=icon,
                style=style,
            )
        ],
    )
    return WidgetTree(screens=[Screen(id="s", name="Home", root=root)])


def _screen_source(tree: WidgetTree) -> str:
    files = FlutterGenerator().generate(tree)
    return next(f for f in files if f.path == "lib/screens/home_screen.dart").content


def test_no_style_yields_text_button():
    src = _screen_source(_tree_with_button(Style()))
    assert "TextButton" in src
    assert "FilledButton" not in src


def test_border_only_yields_outlined_button():
    src = _screen_source(
        _tree_with_button(Style(border_color="#6E56CF", border_width=1))
    )
    assert "OutlinedButton" in src
    assert "BorderSide(color:" in src


def test_solid_background_yields_filled_button():
    src = _screen_source(
        _tree_with_button(Style(background_color="#6E56CF", foreground_color="#FFFFFF"))
    )
    assert "FilledButton" in src
    assert "ElevatedButton" not in src


def test_background_plus_shadow_yields_elevated_button():
    src = _screen_source(
        _tree_with_button(Style(background_color="#6E56CF", shadow=True))
    )
    assert "ElevatedButton" in src


def test_icon_only_yields_icon_button():
    src = _screen_source(_tree_with_button(Style(), text="", icon="star"))
    assert "IconButton" in src
    assert "Icons.star" in src
