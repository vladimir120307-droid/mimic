"""React + Vite + Tailwind code generator.

Emits a complete Vite project tree: package.json, vite/tailwind/postcss config,
index.html, src/main.jsx, src/App.jsx with React Router, and one component
file per screen. The output is buildable with `npm install && npm run dev`.
"""

from __future__ import annotations

import html

from mimic.codegen._tailwind import layout_classes, style_classes
from mimic.codegen.base import GeneratedFile, Target
from mimic.models import Screen, WidgetNode, WidgetTree


class ReactGenerator:
    target: Target = "react"

    def generate(self, tree: WidgetTree) -> list[GeneratedFile]:
        files: list[GeneratedFile] = [
            GeneratedFile("package.json",        _emit_package_json(),      "json"),
            GeneratedFile("vite.config.js",      _emit_vite_config(),       "javascript"),
            GeneratedFile("tailwind.config.js",  _emit_tailwind_config(),   "javascript"),
            GeneratedFile("postcss.config.js",   _emit_postcss_config(),    "javascript"),
            GeneratedFile("index.html",          _emit_index_html(),        "html"),
            GeneratedFile("src/main.jsx",        _emit_main(),              "jsx"),
            GeneratedFile("src/index.css",       _emit_index_css(),         "css"),
            GeneratedFile("src/App.jsx",         _emit_app(tree),           "jsx"),
        ]
        for screen in tree.screens:
            files.append(
                GeneratedFile(
                    f"src/screens/{_pascal(screen.name)}.jsx",
                    _emit_screen(screen, tree),
                    "jsx",
                )
            )
        return files


def _emit_package_json() -> str:
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
    "@vitejs/plugin-react": "^4.3.0",
    "autoprefixer":         "^10.4.19",
    "postcss":              "^8.4.38",
    "tailwindcss":          "^3.4.4",
    "vite":                 "^5.2.10"
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


def _emit_tailwind_config() -> str:
    return """/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx,ts,tsx}'],
  theme:   { extend: {} },
  plugins: [],
};
"""


def _emit_postcss_config() -> str:
    return """export default {
  plugins: { tailwindcss: {}, autoprefixer: {} },
};
"""


def _emit_index_html() -> str:
    return """<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>mimic — generated</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
"""


def _emit_main() -> str:
    return """import React from 'react';
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


def _emit_app(tree: WidgetTree) -> str:
    imports = "\n".join(
        f'import {_pascal(s.name)} from "./screens/{_pascal(s.name)}.jsx";'
        for s in tree.screens
    )
    routes = "\n".join(
        f'        <Route path="{"/" if i == 0 else f"/{s.id}"}" element={{<{_pascal(s.name)} />}} />'
        for i, s in enumerate(tree.screens)
    )
    return f"""import React from 'react';
import {{ Routes, Route }} from 'react-router-dom';
{imports}

export default function App() {{
  return (
    <main className="min-h-screen bg-slate-50 text-slate-900 antialiased">
      <Routes>
{routes}
      </Routes>
    </main>
  );
}}
"""


def _emit_screen(screen: Screen, tree: WidgetTree) -> str:
    class_name = _pascal(screen.name)
    body = _emit_widget(screen.root, tree, indent=6)
    bg_style = ""
    if screen.background_color:
        bg_style = f' style={{{{ backgroundColor: "{screen.background_color}" }}}}'

    nav_imports = ""
    on_tap_handler = ""
    if any(i.kind == "tap" and i.target_screen_id for i in tree.interactions):
        nav_imports = "\nimport { useNavigate } from 'react-router-dom';"
        routes = "{"
        routes += ",".join(
            f'"{i.source_widget_id}":"{i.target_screen_id}"'
            for i in tree.interactions
            if i.kind == "tap" and i.target_screen_id
        )
        routes += "}"
        on_tap_handler = f"""
  const navigate = useNavigate();
  const routes = {routes};
  const onTap = (id) => {{
    if (routes[id]) navigate("/" + routes[id]);
  }};"""

    return f"""import React from 'react';{nav_imports}

export default function {class_name}() {{{on_tap_handler}
  return (
    <section className="mx-auto max-w-md min-h-screen"{bg_style}>
{body}
    </section>
  );
}}
"""


def _emit_widget(node: WidgetNode, tree: WidgetTree, indent: int = 0) -> str:
    pad = " " * indent
    cls = " ".join(layout_classes(node.kind) + style_classes(node.style, node.kind))
    cls_attr = f' className="{cls}"' if cls else ""
    on_click = f' onClick={{() => onTap("{node.id}")}}' if _has_tap_handler(node, tree) else ""

    if node.kind in {"row", "column", "stack", "list", "card", "container",
                     "scroll_view", "app_bar"}:
        children = "\n".join(_emit_widget(c, tree, indent + 2) for c in node.children)
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

    return f"{pad}<div{cls_attr}>{html.escape(node.text or '')}</div>"


def _has_tap_handler(node: WidgetNode, tree: WidgetTree) -> bool:
    return any(
        i.kind == "tap" and i.source_widget_id == node.id and i.target_screen_id
        for i in tree.interactions
    )


def _pascal(name: str) -> str:
    parts = [p for p in name.replace("-", "_").split("_") if p]
    return "".join(p[:1].upper() + p[1:] for p in parts) or "Generated"
