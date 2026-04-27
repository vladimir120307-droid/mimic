from mimic.codegen.html import HtmlGenerator
from mimic.vision.mock import get_fixture


def test_single_screen_emits_one_index_html():
    files = HtmlGenerator().generate(get_fixture("login"))
    assert {f.path for f in files} == {"index.html"}


def test_multi_screen_includes_nav_and_router_script():
    html = HtmlGenerator().generate(get_fixture("dashboard"))[0].content
    assert "<nav" in html
    assert 'data-target="home"' in html
    assert 'data-target="details"' in html
    assert "routes = " in html
    assert '"li1":"details"' in html


def test_html_includes_tailwind_cdn():
    html = HtmlGenerator().generate(get_fixture("login"))[0].content
    assert "cdn.tailwindcss.com" in html


def test_html_widgets_render_text_content():
    html = HtmlGenerator().generate(get_fixture("login"))[0].content
    assert "Welcome back" in html
    assert "Sign in" in html


def test_html_passes_basic_structure_check():
    html = HtmlGenerator().generate(get_fixture("dashboard"))[0].content
    assert html.startswith("<!doctype html>")
    assert html.count("<section") == 2
    assert html.count("</section>") == 2
