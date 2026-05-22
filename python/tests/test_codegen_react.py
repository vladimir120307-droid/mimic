from mimic.codegen.react import ReactGenerator
from mimic.vision.mock import get_fixture


def test_react_emits_full_vite_project():
    files = ReactGenerator().generate(get_fixture("dashboard"))
    paths = {f.path for f in files}
    expected_core = {
        "package.json",
        "vite.config.js",
        "tailwind.config.js",
        "postcss.config.js",
        "index.html",
        "src/main.jsx",
        "src/index.css",
        "src/App.jsx",
    }
    assert expected_core.issubset(paths)


def test_react_emits_one_component_per_screen():
    files = ReactGenerator().generate(get_fixture("dashboard"))
    screen_files = [f for f in files if f.path.startswith("src/screens/")]
    assert {f.path for f in screen_files} == {
        "src/screens/Home.jsx",
        "src/screens/Activity.jsx",
    }


def test_react_app_imports_each_screen():
    files = ReactGenerator().generate(get_fixture("dashboard"))
    app = next(f for f in files if f.path == "src/App.jsx")
    assert 'import Home from "./screens/Home.jsx"' in app.content
    assert 'import Activity from "./screens/Activity.jsx"' in app.content
    assert '<Route path="/"' in app.content
    assert '<Route path="/details"' in app.content


def test_react_navigation_routes_are_emitted():
    files = ReactGenerator().generate(get_fixture("dashboard"))
    home = next(f for f in files if f.path == "src/screens/Home.jsx")
    assert "useNavigate" in home.content
    assert '"li1":"details"' in home.content
    assert "navigate(" in home.content


def test_react_single_screen_skips_navigation_imports():
    files = ReactGenerator().generate(get_fixture("login"))
    login = next(f for f in files if f.path == "src/screens/Login.jsx")
    assert "useNavigate" not in login.content
