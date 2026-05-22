from mimic.theme import extract
from mimic.vision.mock import get_fixture


def test_extract_returns_theme_with_palette():
    theme = extract(get_fixture("dashboard"))
    assert theme.background is not None
    assert any(c.startswith("#") for c in theme.named_colors().values())


def test_extract_picks_brand_color_as_primary():
    theme = extract(get_fixture("login"))
    assert theme.primary in {"#6E56CF", "#6e56cf"}


def test_extract_detects_chat_palette():
    theme = extract(get_fixture("chat"))
    assert theme.primary in {"#0EA5E9", "#0ea5e9"}


def test_extract_includes_typography_when_present():
    theme = extract(get_fixture("dashboard"))
    assert theme.body_font_size is not None
    assert theme.body_font_size > 0


def test_extract_handles_single_screen():
    theme = extract(get_fixture("settings"))
    assert theme.background is not None
