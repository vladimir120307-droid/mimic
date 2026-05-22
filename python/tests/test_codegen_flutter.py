from mimic.codegen.flutter import FlutterGenerator
from mimic.models import (
    BoundingBox,
    Screen,
    Style,
    WidgetNode,
    WidgetTree,
)


def _make_tree() -> WidgetTree:
    root = WidgetNode(
        id="root",
        kind="column",
        bounds=BoundingBox(x=0, y=0, width=1, height=1),
        style=Style(background_color="#FFFFFF"),
        children=[
            WidgetNode(
                id="title",
                kind="text",
                bounds=BoundingBox(x=0, y=0, width=1, height=0.1),
                text="Hello, mimic",
                style=Style(font_size=24, font_weight="bold"),
            ),
            WidgetNode(
                id="cta",
                kind="button",
                bounds=BoundingBox(x=0.25, y=0.5, width=0.5, height=0.1),
                text="Continue",
            ),
        ],
    )
    return WidgetTree(
        screens=[Screen(id="home", name="Home", root=root, background_color="#FFFFFF")],
        target_platform="mobile",
    )


def test_flutter_emits_expected_files():
    files = FlutterGenerator().generate(_make_tree())
    paths = {f.path for f in files}
    assert "lib/main.dart" in paths
    assert "lib/screens/home_screen.dart" in paths
    assert "pubspec.yaml" in paths


def test_flutter_main_imports_initial_screen():
    files = FlutterGenerator().generate(_make_tree())
    main = next(f for f in files if f.path == "lib/main.dart")
    assert "home_screen.dart" in main.content
    assert "HomeScreen" in main.content


def test_flutter_screen_contains_widgets():
    files = FlutterGenerator().generate(_make_tree())
    screen = next(f for f in files if f.path == "lib/screens/home_screen.dart")
    assert "Hello, mimic" in screen.content
    assert "Continue" in screen.content
    # button with no background/border styling falls through M3 heuristics to TextButton
    assert any(
        b in screen.content
        for b in ("TextButton", "FilledButton", "ElevatedButton", "OutlinedButton")
    )


def test_flutter_handles_empty_text_safely():
    tree = WidgetTree(
        screens=[
            Screen(
                id="s",
                name="Blank",
                root=WidgetNode(
                    id="r",
                    kind="container",
                    bounds=BoundingBox(x=0, y=0, width=1, height=1),
                ),
            )
        ],
    )
    files = FlutterGenerator().generate(tree)
    assert any("Container" in f.content for f in files)
