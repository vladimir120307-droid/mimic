"""Tailwind palette extraction: semantic colors instead of bg-[#hex]."""

from mimic.codegen.html import HtmlGenerator
from mimic.codegen.react import ReactGenerator
from mimic.vision.mock import get_fixture


def test_html_emits_tailwind_config_with_palette():
    src = HtmlGenerator().generate(get_fixture("login"))[0].content
    assert "tailwind.config" in src
    assert "extend" in src
    # The login fixture's primary color should be picked up
    assert "primary" in src


def test_html_uses_semantic_classes():
    src = HtmlGenerator().generate(get_fixture("dashboard"))[0].content
    # Background color of body uses semantic class
    assert "bg-background" in src
    # At least one widget got a semantic color class derived from the theme
    assert "bg-primary" in src or "text-primary" in src


def test_react_tailwind_config_has_colors_block():
    files = ReactGenerator(typescript=False).generate(get_fixture("login"))
    cfg = next(f for f in files if f.path == "tailwind.config.js")
    assert "extend" in cfg.content
    assert "primary" in cfg.content


def test_react_ts_tailwind_config_has_colors_block():
    files = ReactGenerator(typescript=True).generate(get_fixture("dashboard"))
    cfg = next(f for f in files if f.path == "tailwind.config.js")
    assert "primary" in cfg.content
