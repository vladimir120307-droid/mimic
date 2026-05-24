"""SwiftUI code generator.

Emits a buildable iOS / macOS app:

- `Package.swift` — minimum SwiftPM manifest
- `Sources/MimicApp/App.swift` — `@main` struct with `WindowGroup`/`NavigationStack`
- `Sources/MimicApp/<Name>View.swift` — one `View` per `Screen`
- Per-screen views use `NavigationLink` for tap-based navigation
"""

from __future__ import annotations

from mimic.codegen.base import GeneratedFile, Target
from mimic.models import Screen, Style, WidgetNode, WidgetTree
from mimic.theme import Theme
from mimic.theme import extract as extract_theme


class SwiftUIGenerator:
    target: Target = "swiftui"

    def generate(self, tree: WidgetTree) -> list[GeneratedFile]:
        theme = extract_theme(tree)
        files: list[GeneratedFile] = [
            GeneratedFile("Package.swift", _emit_package_swift(), "swift"),
            GeneratedFile("Sources/MimicApp/App.swift", _emit_app(tree), "swift"),
            GeneratedFile("Sources/MimicApp/Theme.swift", _emit_theme(theme), "swift"),
        ]
        for screen in tree.screens:
            files.append(
                GeneratedFile(
                    f"Sources/MimicApp/{_pascal(screen.name)}View.swift",
                    _emit_view(screen, tree, theme),
                    "swift",
                )
            )
        return files


def _emit_package_swift() -> str:
    return """// swift-tools-version:5.9
import PackageDescription

let package = Package(
    name: "MimicApp",
    platforms: [.iOS(.v16), .macOS(.v13)],
    products: [
        .executable(name: "MimicApp", targets: ["MimicApp"]),
    ],
    targets: [
        .executableTarget(name: "MimicApp", path: "Sources/MimicApp"),
    ]
)
"""


def _emit_app(tree: WidgetTree) -> str:
    initial = _pascal(tree.initial_screen.name) + "View"
    return f"""import SwiftUI

@main
struct MimicApp: App {{
    var body: some Scene {{
        WindowGroup {{
            NavigationStack {{
                {initial}()
            }}
        }}
    }}
}}
"""


def _emit_theme(theme: Theme) -> str:
    primary = theme.primary or "#6E56CF"
    background = theme.background or "#FFFFFF"
    surface = theme.surface or "#F8FAFC"
    error = theme.error or "#E11D48"
    on_surface = theme.on_surface or "#0F172A"
    return f"""import SwiftUI

extension Color {{
    static let mimicPrimary    = Color(hex: "{primary}")
    static let mimicBackground = Color(hex: "{background}")
    static let mimicSurface    = Color(hex: "{surface}")
    static let mimicError      = Color(hex: "{error}")
    static let mimicOnSurface  = Color(hex: "{on_surface}")

    init(hex: String) {{
        let h = hex.trimmingCharacters(in: CharacterSet(charactersIn: "#"))
        var v: UInt64 = 0
        Scanner(string: h).scanHexInt64(&v)
        let r = Double((v >> 16) & 0xFF) / 255.0
        let g = Double((v >>  8) & 0xFF) / 255.0
        let b = Double( v        & 0xFF) / 255.0
        self = Color(red: r, green: g, blue: b)
    }}
}}
"""


def _emit_view(screen: Screen, tree: WidgetTree, theme: Theme) -> str:
    class_name = _pascal(screen.name) + "View"
    body = _emit_widget(screen.root, tree, theme, indent=12)
    return f"""import SwiftUI

struct {class_name}: View {{
    var body: some View {{
        ScrollView {{
            VStack(alignment: .leading, spacing: 8) {{
{body}
            }}
            .padding()
        }}
        .background(Color.mimicBackground)
    }}
}}
"""


def _emit_widget(node: WidgetNode, tree: WidgetTree, theme: Theme, indent: int = 0) -> str:
    pad = " " * indent

    if node.kind == "text" and node.text is not None:
        modifiers = _text_modifiers(node.style)
        return f'{pad}Text("{_swift_escape(node.text)}"){modifiers}'

    if node.kind == "button":
        action = ""
        on_press = next(
            (
                i.target_screen_id
                for i in tree.interactions
                if i.kind == "tap" and i.source_widget_id == node.id
            ),
            None,
        )
        if on_press:
            action = (
                f"\n{pad}    NavigationLink(destination: "
                f"{_pascal(_screen_name(tree, on_press))}View()) {{\n"
                f'{pad}        Text("{_swift_escape(node.text or "Button")}")\n'
                f"{pad}    }}\n{pad}    .buttonStyle(.borderedProminent)"
            )
            return f"{pad}Group {{{action}\n{pad}}}"
        return (
            f'{pad}Button("{_swift_escape(node.text or "Button")}") {{}}\n'
            f"{pad}    .buttonStyle(.borderedProminent)"
        )

    if node.kind == "text_field":
        return (
            f'{pad}TextField("{_swift_escape(node.placeholder or "")}", text: .constant(""))\n'
            f"{pad}    .textFieldStyle(.roundedBorder)"
        )

    if node.kind == "icon":
        name = node.icon_name or "circle"
        return f'{pad}Image(systemName: "{_sf_symbol(name)}")'

    if node.kind == "image":
        url = node.image_url or ""
        return (
            f'{pad}AsyncImage(url: URL(string: "{_swift_escape(url)}")) {{ phase in\n'
            f"{pad}    phase.image?.resizable().aspectRatio(contentMode: .fill)\n"
            f"{pad}}}"
        )

    if node.kind in {"row"}:
        children = "\n".join(_emit_widget(c, tree, theme, indent + 4) for c in node.children)
        return f"{pad}HStack {{\n{children}\n{pad}}}"

    if node.kind in {"column", "list"}:
        children = "\n".join(_emit_widget(c, tree, theme, indent + 4) for c in node.children)
        return f"{pad}VStack(alignment: .leading) {{\n{children}\n{pad}}}"

    if node.kind == "stack":
        children = "\n".join(_emit_widget(c, tree, theme, indent + 4) for c in node.children)
        return f"{pad}ZStack {{\n{children}\n{pad}}}"

    if node.kind == "card":
        children = "\n".join(_emit_widget(c, tree, theme, indent + 4) for c in node.children)
        bg = node.style.background_color or "#FFFFFF"
        return (
            f"{pad}VStack(alignment: .leading) {{\n{children}\n{pad}}}\n"
            f"{pad}    .padding()\n"
            f'{pad}    .background(Color(hex: "{bg}"))\n'
            f"{pad}    .cornerRadius(12)\n"
            f"{pad}    .shadow(radius: 2)"
        )

    if node.kind == "app_bar":
        text = _swift_escape(node.text or "")
        return (
            f"{pad}HStack {{\n"
            f'{pad}    Text("{text}").font(.headline)\n'
            f"{pad}    Spacer()\n"
            f"{pad}}}\n"
            f"{pad}    .padding()\n"
            f"{pad}    .background(Color.mimicPrimary)\n"
            f"{pad}    .foregroundColor(.white)"
        )

    if node.kind == "list_item":
        on_tap = next(
            (
                i.target_screen_id
                for i in tree.interactions
                if i.kind == "tap" and i.source_widget_id == node.id
            ),
            None,
        )
        if on_tap:
            return (
                f"{pad}NavigationLink(destination: "
                f"{_pascal(_screen_name(tree, on_tap))}View()) {{\n"
                f"{pad}    HStack {{\n"
                f'{pad}        Text("{_swift_escape(node.text or "")}")\n'
                f"{pad}        Spacer()\n"
                f'{pad}        Image(systemName: "chevron.right").foregroundColor(.secondary)\n'
                f"{pad}    }}\n{pad}    .padding(.vertical, 8)\n{pad}}}"
            )
        return (
            f"{pad}HStack {{\n"
            f'{pad}    Text("{_swift_escape(node.text or "")}")\n'
            f"{pad}    Spacer()\n"
            f"{pad}}}\n{pad}    .padding(.vertical, 8)"
        )

    if node.kind == "fab":
        on_press = next(
            (
                i.target_screen_id
                for i in tree.interactions
                if i.kind == "tap" and i.source_widget_id == node.id
            ),
            None,
        )
        if on_press:
            return (
                f"{pad}NavigationLink(destination: "
                f"{_pascal(_screen_name(tree, on_press))}View()) {{\n"
                f'{pad}    Image(systemName: "{_sf_symbol(node.icon_name or "plus")}")\n'
                f"{pad}        .padding()\n"
                f"{pad}        .background(Color.mimicPrimary)\n"
                f"{pad}        .foregroundColor(.white)\n"
                f"{pad}        .clipShape(Circle())\n{pad}}}"
            )
        return (
            f"{pad}Button {{}} label: {{\n"
            f'{pad}    Image(systemName: "{_sf_symbol(node.icon_name or "plus")}")\n'
            f"{pad}}}\n"
            f"{pad}    .padding()\n"
            f"{pad}    .background(Color.mimicPrimary)\n"
            f"{pad}    .foregroundColor(.white)\n"
            f"{pad}    .clipShape(Circle())"
        )

    if node.kind in {"switch", "checkbox"}:
        return f'{pad}Toggle("", isOn: .constant(true)).labelsHidden()'

    if node.kind == "divider":
        return f"{pad}Divider()"

    if node.kind == "spacer":
        return f"{pad}Spacer()"

    if node.children:
        children = "\n".join(_emit_widget(c, tree, theme, indent + 4) for c in node.children)
        return f"{pad}VStack(alignment: .leading) {{\n{children}\n{pad}}}"

    return f'{pad}Text("{_swift_escape(node.text or "")}")'


def _text_modifiers(style: Style) -> str:
    parts: list[str] = []
    if style.font_size is not None:
        parts.append(f".font(.system(size: {style.font_size}))")
    if style.font_weight in {"bold", "700", "800", "900"}:
        parts.append(".fontWeight(.bold)")
    elif style.font_weight in {"500", "600", "medium", "semibold"}:
        parts.append(".fontWeight(.semibold)")
    if style.foreground_color:
        parts.append(f'.foregroundColor(Color(hex: "{style.foreground_color}"))')
    return "".join(parts)


def _screen_name(tree: WidgetTree, screen_id: str) -> str:
    for s in tree.screens:
        if s.id == screen_id:
            return s.name
    return screen_id


# Map common semantic icon names to SF Symbols. Default to `circle` so SwiftUI
# never fails to render.
_SF_SYMBOL_MAP: dict[str, str] = {
    "add": "plus",
    "remove": "minus",
    "close": "xmark",
    "menu": "line.3.horizontal",
    "search": "magnifyingglass",
    "settings": "gearshape",
    "home": "house",
    "person": "person",
    "people": "person.2",
    "favorite": "heart",
    "star": "star",
    "share": "square.and.arrow.up",
    "send": "paperplane",
    "edit": "pencil",
    "delete": "trash",
    "bolt": "bolt",
    "notifications": "bell",
    "calendar": "calendar",
    "chat": "bubble.left.and.bubble.right",
    "mail": "envelope",
    "phone": "phone",
    "camera": "camera",
    "image": "photo",
    "cart": "cart",
    "lock": "lock",
    "play": "play.fill",
    "pause": "pause.fill",
    "stop": "stop.fill",
    "check": "checkmark",
    "info": "info.circle",
    "warning": "exclamationmark.triangle",
    "error": "xmark.octagon",
    "chevron_right": "chevron.right",
    "chevron_left": "chevron.left",
    "chevron_up": "chevron.up",
    "chevron_down": "chevron.down",
    "arrow_back": "arrow.left",
    "arrow_forward": "arrow.right",
}


def _sf_symbol(name: str) -> str:
    key = "".join(c if c.isalnum() else "_" for c in name).lower().strip("_")
    return _SF_SYMBOL_MAP.get(key, "circle")


def _swift_escape(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")


def _pascal(name: str) -> str:
    parts = [p for p in name.replace("-", "_").replace(" ", "_").split("_") if p]
    return "".join(p[:1].upper() + p[1:] for p in parts) or "Generated"
