"""HTML + Tailwind code generator.

Produces a single self-contained `index.html` with the Tailwind play CDN
script — drop it into a browser and it just works, no build step. When
there are multiple screens, navigation buttons toggle visibility of
sections at runtime via a tiny inline script.

The extracted theme palette is materialized as an inline
`tailwind.config = {...}` script tag so semantic classes like `bg-primary`
work without a build step.
"""

from __future__ import annotations

import html
import json

from mimic.codegen._icons import heroicon_svg
from mimic.codegen._tailwind import layout_classes, style_classes
from mimic.codegen.base import GeneratedFile, Target
from mimic.models import WidgetNode, WidgetTree
from mimic.theme import Theme
from mimic.theme import extract as extract_theme


class HtmlGenerator:
    target: Target = "html"

    def generate(self, tree: WidgetTree) -> list[GeneratedFile]:
        theme = extract_theme(tree)
        body = _emit_body(tree, theme)
        nav = _emit_nav(tree) if len(tree.screens) > 1 else ""
        script = _emit_script(tree) if len(tree.screens) > 1 else ""
        config = _emit_tailwind_config(theme)
        index = _PAGE_TEMPLATE.format(
            title="mimic — generated",
            config=config,
            nav=nav,
            body=body,
            script=script,
        )
        return [GeneratedFile("index.html", index, "html")]


_PAGE_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{title}</title>
  <script src="https://cdn.tailwindcss.com"></script>
  {config}
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }}
    .screen {{ display: none; }}
    .screen.active {{ display: block; }}
  </style>
</head>
<body class="min-h-screen bg-background text-on-surface antialiased">
{nav}
<main class="mx-auto max-w-md">
{body}
</main>
{script}
</body>
</html>
"""


def _emit_tailwind_config(theme: Theme) -> str:
    palette = theme.named_colors()
    if not palette:
        return ""
    colors_json = json.dumps(palette, indent=2).replace('"', "'")
    return (
        "<script>\n"
        "    tailwind.config = {\n"
        "      theme: { extend: { colors: " + colors_json + " } }\n"
        "    };\n"
        "  </script>"
    )


def _emit_nav(tree: WidgetTree) -> str:
    items = "\n".join(
        f'    <button data-target="{s.id}" '
        f'class="px-3 py-1 rounded hover:bg-slate-200">{html.escape(s.name)}</button>'
        for s in tree.screens
    )
    return (
        '<nav class="sticky top-0 z-10 bg-white border-b border-slate-200">\n'
        '  <div class="mx-auto max-w-md flex gap-2 px-4 py-2 overflow-x-auto">\n'
        f"{items}\n"
        "  </div>\n"
        "</nav>"
    )


def _emit_body(tree: WidgetTree, theme: Theme) -> str:
    parts: list[str] = []
    for i, screen in enumerate(tree.screens):
        active = " active" if i == 0 else ""
        bg = ""
        if screen.background_color:
            bg = f' style="background-color: {html.escape(screen.background_color)}"'
        parts.append(
            f'<section id="{screen.id}" class="screen{active} min-h-screen"{bg}>\n'
            f"{_emit_widget(screen.root, theme, indent=2)}\n"
            "</section>"
        )
    return "\n".join(parts)


def _emit_script(tree: WidgetTree) -> str:
    interaction_routes = ",".join(
        f'"{i.source_widget_id}":"{i.target_screen_id}"'
        for i in tree.interactions
        if i.kind == "tap" and i.target_screen_id
    )
    return f"""<script>
(() => {{
  const routes = {{{interaction_routes}}};
  const show = (id) => {{
    document.querySelectorAll('.screen').forEach(s => s.classList.toggle('active', s.id === id));
  }};
  document.querySelectorAll('nav button[data-target]').forEach(btn => {{
    btn.addEventListener('click', () => show(btn.dataset.target));
  }});
  document.body.addEventListener('click', e => {{
    const target = e.target.closest('[data-mimic-id]');
    if (!target) return;
    const dest = routes[target.dataset.mimicId];
    if (dest) show(dest);
  }});
}})();
</script>"""


def _emit_widget(node: WidgetNode, theme: Theme, indent: int = 0) -> str:
    pad = " " * indent
    cls = " ".join(layout_classes(node.kind) + style_classes(node.style, node.kind, theme))
    cls_attr = f' class="{cls}"' if cls else ""
    id_attr = f' data-mimic-id="{node.id}"'

    tag, inner = _tag_and_inner(node)

    if node.kind in {
        "row",
        "column",
        "stack",
        "list",
        "card",
        "scroll_view",
        "container",
        "app_bar",
    }:
        children = "\n".join(_emit_widget(c, theme, indent + 2) for c in node.children)
        body = ""
        if inner:
            body = f"\n{pad}  {inner}"
        if children:
            body = f"{body}\n{children}" if body else f"\n{children}"
        return f"{pad}<{tag}{id_attr}{cls_attr}>{body}\n{pad}</{tag}>"

    if node.kind == "icon":
        svg = heroicon_svg(node.icon_name, classes="w-6 h-6")
        return f'{pad}<span{id_attr}{cls_attr} aria-hidden="true">{svg}</span>'

    if node.kind == "text":
        return f"{pad}<{tag}{id_attr}{cls_attr}>{inner}</{tag}>"

    if node.kind == "button":
        return f'{pad}<button{id_attr}{cls_attr} type="button">{inner}</button>'

    if node.kind == "text_field":
        ph = html.escape(node.placeholder or "")
        return (
            f'{pad}<input{id_attr} type="text" placeholder="{ph}" '
            f'class="{cls} w-full px-3 py-2 rounded-lg border border-slate-300 '
            f'focus:outline-none focus:ring-2 focus:ring-violet-500" />'
        )

    if node.kind == "image":
        src = html.escape(node.image_url or "")
        alt = html.escape(node.semantic_label or "")
        return f'{pad}<img{id_attr} src="{src}" alt="{alt}" class="{cls}" />'

    if node.kind == "list_item":
        return (
            f'{pad}<div{id_attr} class="{cls} flex items-center justify-between py-3">'
            f"<span>{inner}</span>"
            f'<span class="text-slate-400">›</span>'
            f"</div>"
        )

    if node.kind == "fab":
        svg = heroicon_svg(node.icon_name or "add", classes="w-6 h-6")
        return f'{pad}<button{id_attr}{cls_attr} type="button" aria-label="action">{svg}</button>'

    if node.kind == "divider":
        return f"{pad}<hr{id_attr}{cls_attr} />"
    if node.kind == "spacer":
        return f'{pad}<div{id_attr} class="flex-1"></div>'

    children = "\n".join(_emit_widget(c, theme, indent + 2) for c in node.children)
    return f"{pad}<div{id_attr}{cls_attr}>\n{children}\n{pad}</div>"


def _tag_and_inner(node: WidgetNode) -> tuple[str, str]:
    text = html.escape(node.text or "")
    match node.kind:
        case "text":
            return ("p", text)
        case "icon":
            return ("span", text or "●")
        case "app_bar":
            return ("header", text)
        case "card":
            return ("article", "")
        case "list":
            return ("ul", "")
        case "row":
            return ("div", "")
        case "column":
            return ("div", "")
        case "container":
            return ("div", "")
        case _:
            return ("div", text)
