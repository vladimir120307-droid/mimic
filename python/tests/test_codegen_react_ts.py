"""Verify the TypeScript variant of the React generator."""

from mimic.codegen import get_generator
from mimic.vision.mock import get_fixture


def test_react_ts_emits_tsx_files():
    files = get_generator("react-ts").generate(get_fixture("dashboard"))
    paths = {f.path for f in files}
    assert "tsconfig.json" in paths
    assert "tsconfig.node.json" in paths
    assert "src/types.ts" in paths
    assert "src/main.tsx" in paths
    assert "src/App.tsx" in paths
    assert "src/screens/Home.tsx" in paths
    assert "src/screens/Activity.tsx" in paths


def test_react_ts_app_has_jsx_element_return():
    files = get_generator("react-ts").generate(get_fixture("login"))
    app = next(f for f in files if f.path == "src/App.tsx")
    assert "React.JSX.Element" in app.content


def test_react_ts_screen_types_navigate_callback():
    files = get_generator("react-ts").generate(get_fixture("dashboard"))
    home = next(f for f in files if f.path == "src/screens/Home.tsx")
    assert "Record<string, string>" in home.content
    assert "(id: string)" in home.content


def test_react_js_does_not_emit_typescript_artifacts():
    files = get_generator("react").generate(get_fixture("dashboard"))
    paths = {f.path for f in files}
    assert "tsconfig.json" not in paths
    assert "src/types.ts" not in paths


def test_react_ts_package_json_has_typescript_dev_dep():
    files = get_generator("react-ts").generate(get_fixture("login"))
    pkg = next(f for f in files if f.path == "package.json")
    assert '"typescript":' in pkg.content
    assert "@types/react" in pkg.content
