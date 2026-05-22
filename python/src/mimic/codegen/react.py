"""React + Vite + Tailwind code generator.

Emits a complete Vite project tree. Supports both JavaScript (.jsx) and
TypeScript (.tsx) outputs; pick via the `typescript` constructor argument.

The TS variant adds a `tsconfig.json`, replaces `vite.config.js` with
`vite.config.ts`, and types the navigation router shape.

Theme extraction is materialized as a `theme.extend.colors` block in
`tailwind.config.js`, so generated classes look like `bg-primary` instead
of arbitrary-value `bg-[#6E56CF]`.
"""

from __future__ import annotations

import html

from mimic.codegen._tailwind import layout_classes, style_classes
from mimic.codegen.base import GeneratedFile, Target
from mimic.models import Screen, WidgetNode, WidgetTree
from mimic.theme import Theme, extract as extract_theme


class ReactGenerator:
    target: Target = "react"

    def __init__(self, *, typescript: bool = False) -> None:
        self.typescript = typescript
        self.target = "react-ts" if typescript else "react"

    @property
    def ext(self) -> str:
        return "tsx" if self.typescript else "jsx"

    def generate(self, tree: WidgetTree) -> list[GeneratedFile]:
        theme = extract_theme(tree)
        config_ext = "ts" if self.typescript else "js"
        files: list[GeneratedFile] = [
            GeneratedFile("package.json",       _emit_package_json(self.typescript), "json"),
            GeneratedFile(f"vite.config.{config_ext}",
                          _emit_vite_config(),       "typescript" if self.typescript else "javascript"),
            GeneratedFile("tailwind.config.js", _emit_tailwind_config(theme),       "javascript"),
            GeneratedFile("postcss.config.js",  _emit_postcss_config(),             "javascript"),
            GeneratedFile("index.html",         _emit_index_html(self.ext),         "html"),
            GeneratedFile(f"src/main.{self.ext}",  _emit_main(self.ext),            self.ext),
            GeneratedFile("src/index.css",      _emit_index_css(),                  "css"),
            GeneratedFile(f"src/App.{self.ext}",   _emit_app(tree, self.ext, self.typescript),
                          self.ext),
        ]
        if self.typescript:
            files.append(GeneratedFile("tsconfig.json",       _emit_tsconfig(),     "json"))
            files.append(GeneratedFile("tsconfig.node.json",  _emit_tsconfig_node(),"json"))
            files.append(GeneratedFile("src/types.ts",        _emit_types(),        "typescript"))

        for screen in tree.screens:
            files.append(
                GeneratedFile(
                    f"src/screens/{_pascal(screen.name)}.{self.ext}",
                    _emit_screen(screen, tree, theme, self.typescript),
                    self.ext,
                )
            )
        return files


def _emit_package_json(typescript: bool) -> str:
    devs = '''    "@vitejs/plugin-react": "^4.3.0",
    "autoprefixer":         "^10.4.19",
    "postcss":              "^8.4.38",
    "tailwindcss":          "^3.4.4",
    "vite":                 "^5.2.10"'''
    if typescript:
        devs = (
            devs.rstrip()
            + ',\n'
            '    "@types/react":             "^18.2.0",\n'
            '    "@types/react-dom":         "^18.2.0",\n'
            '    "typescript":               "^5.4.0"'
        )
    return """{
  "name": "mimic-generated",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "dev":     "vite",
    "build":   "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react":           "^18.3.1",
    "react-dom":       "^18.3.1",
    "react-router-dom":"^6.23.0"
  },
  "devDependencies": {
""" + devs + """
  }
}
"""


def _emit_vite_config() -> str:
    return """import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
});
"""


def _emit_tailwind_config(theme: Theme) -> str:
    palette = theme.named_colors()
    if palette:
        colors_lines = ",\n".join(f"        {k}: '{v}'" for k, v in palette.items())
        colors_block = "{\n" + colors_lines + ",\n      }"
    else:
        colors_block = "{}"
    return f"""/** @type {{import('tailwindcss').Config}} */
export default {{
  content: ['./index.html', './src/**/*.{{js,jsx,ts,tsx}}'],
  theme:   {{
    extend: {{
      colors: {colors_block},
    }},
  }},
  plugins: [],
}};
"""


def _emit_postcss_config() -> str:
    return """export default {
  plugins: { tailwindcss: {}, autoprefixer: {} },
};
"""


def _emit_index_html(ext: str) -> str:
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>mimic — generated</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.{ext}"></script>
  </body>
</html>
"""


def _emit_main(ext: str) -> str:
    return f"""import React from 'react';
import ReactDOM from 'react-dom/client';
import {{ BrowserRouter }} from 'react-router-dom';
import App from './App.{ext}';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </React.StrictMode>,
);
""" if ext == "tsx" else """import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import App from './App.jsx';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </React.StrictMode>,
);
"""


def _emit_index_css() -> str:
    return """@tailwind base;
@tailwind components;
@tailwind utilities;
"""


def _emit_tsconfig() -> str:
    return """{
  "compilerOptions": {
    "target":                "ES2022",
    "lib":                   ["DOM", "DOM.Iterable", "ES2022"],
    "module":                "ESNext",
    "moduleResolution":      "bundler",
    "skipLibCheck":          true,
    "allowSyntheticDefaultImports": true,
    "esModuleInterop":       true,
    "allowImportingTsExtensions": true,
    "isolatedModules":       true,
    "noEmit":                true,
    "jsx":                   "react-jsx",
    "strict":                true,
    "noUnusedLocals":        true,
    "noUnusedParameters":    true,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
"""


def _emit_tsconfig_node() -> str:
    return """{
  "compilerOptions": {
    "composite": true,
    "skipLibCheck": true,
    "module": "ESNext",
    "moduleResolution": "bundler",
    "allowSyntheticDefaultImports": true,
    "strict": true
  },
  "include": ["vite.config.ts"]
}
"""


def _emit_types() -> str:
    return """export type RouteMap = Readonly<Record<string, string>>;
"""


def _emit_app(tree: WidgetTree, ext: str, typescript: bool) -> str:
    imports = "\n".join(
        f'import {_pascal(s.name)} from "./screens/{_pascal(s.name)}.{ext}";'
        for s in tree.screens
    )
    routes = "\n".join(
        f'        <Route path="{"/" if i == 0 else f"/{s.id}"}" element={{<{_pascal(s.name)} />}} />'
        for i, s in enumerate(tree.screens)
    )
    signature = "App(): React.JSX.Element" if typescript else "App()"
    return f"""import React from 'react';
import {{ Routes, Route }} from 'react-router-dom';
{imports}

export default function {signature} {{
  return (
    <main className="min-h-screen bg-background text-on-surface antialiased">
      <Routes>
{routes}
      </Routes>
    </main>
  );
}}
"""


def _emit_screen(
    screen: Screen, tree: WidgetTree, theme: Theme, typescript: bool
) -> str:
    class_name = _pascal(screen.name)
    body = _emit_widget(screen.root, tree, theme, indent=6)
    bg_style = ""
    if screen.background_color:
        bg_style = f' style={{{{ backgroundColor: "{screen.background_color}" }}}}'

    nav_imports = ""
    on_tap_handler = ""
    if any(i.kind == "tap" and i.target_screen_id for i in tree.interactions):
        nav_imports = "\nimport { useNavigate } from 'react-router-dom';"
        route_entries = ",".join(
            f'"{i.source_widget_id}":"{i.target_screen_id}"'
            for i in tree.interactions
            if i.kind == "tap" and i.target_screen_id
        )
        routes_decl = (
            f"const routes: Record<string, string> = {{{route_entries}}};"
            if typescript
            else f"const routes = {{{route_entries}}};"
        )
        on_tap_param = "(id: string)" if typescript else "(id)"
        on_tap_handler = f"""
  const navigate = useNavigate();
  {routes_decl}
  const onTap = {on_tap_param} => {{
    if (routes[id]) navigate("/" + routes[id]);
  }};"""

    signature = (
        f"{class_name}(): React.JSX.Element" if typescript else f"{class_name}()"
    )
    return f"""import React from 'react';{nav_imports}

export default function {signature} {{{on_tap_handler}
  return (
    <section className="mx-auto max-w-md min-h-screen"{bg_style}>
{body}
    </section>
  );
}}
"""


def _emit_widget(
    node: WidgetNode, tree: WidgetTree, theme: Theme, indent: int = 0
) -> str:
    pad = " " * indent
    cls = " ".join(layout_classes(node.kind) + style_classes(node.style, node.kind, theme))
    cls_attr = f' className="{cls}"' if cls else ""
    on_click = f' onClick={{() => onTap("{node.id}")}}' if _has_tap_handler(node, tree) else ""

    if node.kind in {"row", "column", "stack", "list", "card", "container",
                     "scroll_view", "app_bar"}:
        children = "\n".join(_emit_widget(c, tree, theme, indent + 2) for c in node.children)
        text_inline = ""
        if node.text:
            text_inline = f"\n{pad}  <span>{html.escape(node.text)}</span>"
        body = text_inline + ("\n" + children if children else "")
        return f"{pad}<div{cls_attr}{on_click}>{body}\n{pad}</div>"

    if node.kind == "text":
        return f'{pad}<p{cls_attr}>{html.escape(node.text or "")}</p>'

    if node.kind == "button":
        label = html.escape(node.text or "Button")
        return (
            f'{pad}<button type="button"{cls_attr}{on_click}>{label}</button>'
        )

    if node.kind == "text_field":
        ph = html.escape(node.placeholder or "")
        return (
            f'{pad}<input type="text" placeholder="{ph}" '
            f'className="{cls} w-full px-3 py-2 rounded-lg border border-slate-300 '
            f'focus:outline-none focus:ring-2 focus:ring-violet-500" />'
        )

    if node.kind == "icon":
        return f'{pad}<span{cls_attr} aria-hidden="true">●</span>'

    if node.kind == "image":
        src = html.escape(node.image_url or "")
        alt = html.escape(node.semantic_label or "")
        return f'{pad}<img src="{src}" alt="{alt}" className="{cls}" />'

    if node.kind == "list_item":
        text = html.escape(node.text or "")
        return (
            f'{pad}<div{cls_attr}{on_click} className="{cls} flex items-center '
            f'justify-between py-3 cursor-pointer">'
            f"<span>{text}</span>"
            f'<span className="text-slate-400">›</span>'
            "</div>"
        )

    if node.kind == "fab":
        return (
            f'{pad}<button type="button"{cls_attr}{on_click} aria-label="action">'
            '<span className="text-2xl">+</span></button>'
        )

    if node.kind == "divider":
        return f"{pad}<hr{cls_attr} />"
    if node.kind == "spacer":
        return f'{pad}<div className="flex-1"></div>'

    if node.kind in {"switch", "checkbox"}:
        return (
            f'{pad}<label{cls_attr} className="{cls} inline-flex items-center cursor-pointer">'
            f'<input type="checkbox" className="sr-only peer" defaultChecked />'
            f'<div className="w-11 h-6 bg-slate-200 peer-checked:bg-primary '
            f'rounded-full transition-colors"></div>'
            f"</label>"
        )

    return f"{pad}<div{cls_attr}>{html.escape(node.text or '')}</div>"


def _has_tap_handler(node: WidgetNode, tree: WidgetTree) -> bool:
    return any(
        i.kind == "tap" and i.source_widget_id == node.id and i.target_screen_id
        for i in tree.interactions
    )


def _pascal(name: str) -> str:
    parts = [p for p in name.replace("-", "_").replace(" ", "_").split("_") if p]
    return "".join(p[:1].upper() + p[1:] for p in parts) or "Generated"
