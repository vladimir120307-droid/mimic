"""Vue 3 + Vite + Tailwind code generator.

Emits a complete Vite project tree: package.json, vite.config.js, tailwind +
postcss config, index.html, src/main.js, src/App.vue with vue-router, and one
single-file component per Screen.
"""

from __future__ import annotations

import html

from mimic.codegen._icons import heroicon_svg
from mimic.codegen._tailwind import layout_classes, style_classes
from mimic.codegen.base import GeneratedFile, Target
from mimic.models import Screen, WidgetNode, WidgetTree
from mimic.theme import Theme
from mimic.theme import extract as extract_theme


class VueGenerator:
    target: Target = "vue"

    def generate(self, tree: WidgetTree) -> list[GeneratedFile]:
        theme = extract_theme(tree)
        files: list[GeneratedFile] = [
            GeneratedFile("package.json", _emit_package_json(), "json"),
            GeneratedFile("vite.config.js", _emit_vite_config(), "javascript"),
            GeneratedFile("tailwind.config.js", _emit_tailwind_config(theme), "javascript"),
            GeneratedFile("postcss.config.js", _emit_postcss_config(), "javascript"),
            GeneratedFile("index.html", _emit_index_html(), "html"),
            GeneratedFile("src/main.js", _emit_main(tree), "javascript"),
            GeneratedFile("src/index.css", _emit_index_css(), "css"),
            GeneratedFile("src/App.vue", _emit_app(), "vue"),
        ]
        for screen in tree.screens:
            files.append(
                GeneratedFile(
                    f"src/views/{_pascal(screen.name)}.vue",
                    _emit_view(screen, tree, theme),
                    "vue",
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
    "vue":        "^3.4.0",
    "vue-router": "^4.3.0"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^5.0.0",
    "autoprefixer":       "^10.4.19",
    "postcss":            "^8.4.38",
    "tailwindcss":        "^3.4.4",
    "vite":               "^5.2.10"
  }
}
"""


def _emit_vite_config() -> str:
    return """import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
  plugins: [vue()],
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
  content: ['./index.html', './src/**/*.{{js,ts,vue}}'],
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


def _emit_index_html() -> str:
    return """<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>mimic — generated</title>
  </head>
  <body>
    <div id="app"></div>
    <script type="module" src="/src/main.js"></script>
  </body>
</html>
"""


def _emit_main(tree: WidgetTree) -> str:
    routes = ",\n".join(
        f'  {{ path: "{"/" if i == 0 else f"/{s.id}"}", component: () => import("./views/{_pascal(s.name)}.vue") }}'
        for i, s in enumerate(tree.screens)
    )
    return f"""import {{ createApp }} from 'vue';
import {{ createRouter, createWebHashHistory }} from 'vue-router';
import App from './App.vue';
import './index.css';

const routes = [
{routes},
];

const router = createRouter({{
  history: createWebHashHistory(),
  routes,
}});

createApp(App).use(router).mount('#app');
"""


def _emit_index_css() -> str:
    return """@tailwind base;
@tailwind components;
@tailwind utilities;
"""


def _emit_app() -> str:
    return """<template>
  <main class="min-h-screen bg-background text-on-surface antialiased">
    <router-view />
  </main>
</template>

<script setup>
</script>
"""


def _emit_view(screen: Screen, tree: WidgetTree, theme: Theme) -> str:
    body = _emit_widget(screen.root, tree, theme, indent=4)
    bg_attr = ""
    if screen.background_color:
        bg_attr = f" :style=\"{{ backgroundColor: '{screen.background_color}' }}\""

    routes_decl = ""
    nav_method = ""
    if any(i.kind == "tap" and i.target_screen_id for i in tree.interactions):
        route_entries = ",".join(
            f'"{i.source_widget_id}":"{i.target_screen_id}"'
            for i in tree.interactions
            if i.kind == "tap" and i.target_screen_id
        )
        routes_decl = f"const routes = {{{route_entries}}};\n"
        nav_method = "function onTap(id) {\n  if (routes[id]) router.push('/' + routes[id]);\n}\n"

    return f"""<template>
  <section class="mx-auto max-w-md min-h-screen"{bg_attr}>
{body}
  </section>
</template>

<script setup>
import {{ useRouter }} from 'vue-router';
const router = useRouter();
{routes_decl}{nav_method}</script>
"""


def _emit_widget(node: WidgetNode, tree: WidgetTree, theme: Theme, indent: int = 0) -> str:
    pad = " " * indent
    cls = " ".join(layout_classes(node.kind) + style_classes(node.style, node.kind, theme))
    cls_attr = f' class="{cls}"' if cls else ""
    on_click = f" @click='onTap(\"{node.id}\")'" if _has_tap_handler(node, tree) else ""

    if node.kind in {
        "row",
        "column",
        "stack",
        "list",
        "card",
        "container",
        "scroll_view",
        "app_bar",
    }:
        children = "\n".join(_emit_widget(c, tree, theme, indent + 2) for c in node.children)
        text_inline = ""
        if node.text:
            text_inline = f"\n{pad}  <span>{html.escape(node.text)}</span>"
        body = text_inline + ("\n" + children if children else "")
        return f"{pad}<div{cls_attr}{on_click}>{body}\n{pad}</div>"

    if node.kind == "text":
        return f"{pad}<p{cls_attr}>{html.escape(node.text or '')}</p>"

    if node.kind == "button":
        label = html.escape(node.text or "Button")
        return f'{pad}<button type="button"{cls_attr}{on_click}>{label}</button>'

    if node.kind == "text_field":
        ph = html.escape(node.placeholder or "")
        return (
            f'{pad}<input type="text" placeholder="{ph}" '
            f'class="{cls} w-full px-3 py-2 rounded-lg border border-slate-300 '
            f'focus:outline-none focus:ring-2 focus:ring-violet-500" />'
        )

    if node.kind == "icon":
        svg = heroicon_svg(node.icon_name, classes="w-6 h-6")
        return f'{pad}<span{cls_attr} aria-hidden="true">{svg}</span>'

    if node.kind == "image":
        src = html.escape(node.image_url or "")
        alt = html.escape(node.semantic_label or "")
        return f'{pad}<img src="{src}" alt="{alt}" class="{cls}" />'

    if node.kind == "list_item":
        text = html.escape(node.text or "")
        return (
            f'{pad}<div{cls_attr}{on_click} class="{cls} flex items-center '
            f'justify-between py-3 cursor-pointer">'
            f"<span>{text}</span>"
            f'<span class="text-slate-400">›</span>'
            "</div>"
        )

    if node.kind == "fab":
        svg = heroicon_svg(node.icon_name or "add", classes="w-6 h-6")
        return f'{pad}<button type="button"{cls_attr}{on_click} aria-label="action">{svg}</button>'

    if node.kind == "divider":
        return f"{pad}<hr{cls_attr} />"
    if node.kind == "spacer":
        return f'{pad}<div class="flex-1"></div>'

    if node.kind in {"switch", "checkbox"}:
        return (
            f'{pad}<label{cls_attr} class="{cls} inline-flex items-center cursor-pointer">'
            f'<input type="checkbox" class="sr-only peer" checked />'
            f'<div class="w-11 h-6 bg-slate-200 peer-checked:bg-primary '
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
