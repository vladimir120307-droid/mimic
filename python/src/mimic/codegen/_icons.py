"""Map semantic icon names to real per-target icon references.

Vision providers emit lowercase semantic names (`add`, `send`, `chevron_right`).
Each codegen target turns those into something a developer would actually
recognize:

- Flutter — `Icons.<name>` from Material Symbols
- HTML / React — inline Heroicons SVG path data (no external dependency)

Unknown names fall back to a sensible default (`Icons.circle` /
the question-mark icon). The fallback never produces a broken build.
"""

from __future__ import annotations

# Maps semantic name -> material symbol name (Flutter Icons.* identifier)
_FLUTTER_ICONS: dict[str, str] = {
    "add":              "add",
    "remove":           "remove",
    "close":            "close",
    "menu":             "menu",
    "search":           "search",
    "settings":         "settings",
    "home":             "home",
    "person":           "person",
    "people":           "people",
    "favorite":         "favorite",
    "star":             "star",
    "share":            "share",
    "send":             "send",
    "edit":             "edit",
    "delete":           "delete",
    "bolt":             "bolt",
    "flash":            "bolt",
    "lightning":        "bolt",
    "notifications":    "notifications",
    "bell":             "notifications",
    "calendar":         "calendar_today",
    "chat":             "chat_bubble_outline",
    "mail":             "mail_outline",
    "phone":            "phone",
    "camera":           "photo_camera",
    "image":            "image",
    "cart":             "shopping_cart",
    "shop":             "store",
    "lock":             "lock",
    "unlock":           "lock_open",
    "play":             "play_arrow",
    "pause":            "pause",
    "stop":             "stop",
    "check":            "check",
    "info":             "info_outline",
    "warning":          "warning_amber",
    "error":            "error_outline",
    "chevron_right":    "chevron_right",
    "chevron_left":     "chevron_left",
    "chevron_up":       "expand_less",
    "chevron_down":     "expand_more",
    "arrow_back":       "arrow_back",
    "arrow_forward":    "arrow_forward",
    "more_horiz":       "more_horiz",
    "more_vert":        "more_vert",
    "filter":           "filter_list",
    "sort":             "sort",
    "logout":           "logout",
    "login":            "login",
    "upload":           "upload",
    "download":         "download",
    "moon":             "dark_mode",
    "sun":              "light_mode",
    "wifi":             "wifi",
    "location":         "location_on",
    "globe":            "language",
    "world":            "language",
    "link":             "link",
}

# Heroicons-style (outline) 24x24 SVG path data. We embed only the `<path d="…" />`
# attribute so the surrounding `<svg viewBox="0 0 24 24">` stays uniform.
_HEROICON_PATHS: dict[str, str] = {
    "add":              "M12 4.5v15m7.5-7.5h-15",
    "close":            "M6 18L18 6M6 6l12 12",
    "search":           "m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z",
    "chevron_right":    "m8.25 4.5 7.5 7.5-7.5 7.5",
    "chevron_left":     "M15.75 19.5 8.25 12l7.5-7.5",
    "chevron_up":       "m4.5 15.75 7.5-7.5 7.5 7.5",
    "chevron_down":     "m19.5 8.25-7.5 7.5-7.5-7.5",
    "menu":             "M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5",
    "send":             "M6 12 3.269 3.125A59.769 59.769 0 0 1 21.485 12 59.768 59.768 0 0 1 3.27 20.875L5.999 12Zm0 0h7.5",
    "bolt":             "m3.75 13.5 10.5-11.25L12 10.5h8.25L9.75 21.75 12 13.5H3.75Z",
    "star":             "M11.48 3.499a.562.562 0 0 1 1.04 0l2.125 5.111a.563.563 0 0 0 .475.345l5.518.442c.499.04.701.663.321.988l-4.204 3.602a.563.563 0 0 0-.182.557l1.285 5.385a.562.562 0 0 1-.84.61l-4.725-2.885a.562.562 0 0 0-.586 0L6.982 20.54a.562.562 0 0 1-.84-.61l1.285-5.386a.562.562 0 0 0-.182-.557l-4.204-3.602a.562.562 0 0 1 .321-.988l5.518-.442a.563.563 0 0 0 .475-.345L11.48 3.5Z",
    "home":             "m2.25 12 8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25",
    "settings":         "M9.594 3.94c.09-.542.56-.94 1.11-.94h2.593c.55 0 1.02.398 1.11.94l.213 1.281c.063.374.313.686.645.87.074.04.147.083.22.127.325.196.72.257 1.075.124l1.217-.456a1.125 1.125 0 0 1 1.37.49l1.296 2.247a1.125 1.125 0 0 1-.26 1.431l-1.003.827c-.293.241-.438.613-.43.992a7.723 7.723 0 0 1 0 .255c-.008.378.137.75.43.991l1.004.827c.424.35.534.955.26 1.43l-1.298 2.247a1.125 1.125 0 0 1-1.369.491l-1.217-.456c-.355-.133-.75-.072-1.076.124a6.47 6.47 0 0 1-.22.128c-.331.183-.581.495-.644.869l-.213 1.281c-.09.543-.56.94-1.11.94h-2.594c-.55 0-1.019-.398-1.11-.94l-.213-1.281c-.062-.374-.312-.686-.644-.87a6.52 6.52 0 0 1-.22-.127c-.325-.196-.72-.257-1.076-.124l-1.217.456a1.125 1.125 0 0 1-1.369-.49l-1.297-2.247a1.125 1.125 0 0 1 .26-1.431l1.004-.827c.292-.24.437-.613.43-.991a6.932 6.932 0 0 1 0-.255c.007-.38-.138-.751-.43-.992l-1.004-.827a1.125 1.125 0 0 1-.26-1.43l1.297-2.247a1.125 1.125 0 0 1 1.37-.491l1.216.456c.356.133.751.072 1.076-.124.072-.044.146-.086.22-.128.332-.183.582-.495.644-.869l.214-1.28Z M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z",
    "person":           "M15.75 6a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0ZM4.501 20.118a7.5 7.5 0 0 1 14.998 0A17.933 17.933 0 0 1 12 21.75c-2.676 0-5.216-.584-7.499-1.632Z",
    "calendar":         "M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 0 1 2.25-2.25h13.5A2.25 2.25 0 0 1 21 7.5v11.25m-18 0A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75m-18 0v-7.5A2.25 2.25 0 0 1 5.25 9h13.5A2.25 2.25 0 0 1 21 11.25v7.5",
    "cart":             "M2.25 3h1.386c.51 0 .955.343 1.087.835l.383 1.437M7.5 14.25a3 3 0 0 0-3 3h15.75m-12.75-3h11.218c1.121-2.3 2.1-4.684 2.924-7.138a60.114 60.114 0 0 0-16.536-1.84M7.5 14.25 5.106 5.272M6 20.25a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Zm12.75 0a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Z",
    "chat":             "M2.25 12.76c0 1.6 1.123 2.994 2.707 3.227 1.087.16 2.185.283 3.293.369V21l4.184-4.183a1.14 1.14 0 0 1 .778-.332 48.294 48.294 0 0 0 5.83-.498c1.585-.233 2.708-1.626 2.708-3.228V6.741c0-1.602-1.123-2.995-2.707-3.228A48.394 48.394 0 0 0 12 3c-2.392 0-4.744.175-7.043.513C3.373 3.746 2.25 5.14 2.25 6.741v6.018Z",
    "delete":           "m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0",
    "edit":             "m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L6.832 19.82a4.5 4.5 0 0 1-1.897 1.13l-2.685.8.8-2.685a4.5 4.5 0 0 1 1.13-1.897L16.863 4.487Zm0 0L19.5 7.125",
    "check":            "m4.5 12.75 6 6 9-13.5",
    "play":             "M5.25 5.653c0-.856.917-1.398 1.667-.986l11.54 6.347a1.125 1.125 0 0 1 0 1.972l-11.54 6.347a1.125 1.125 0 0 1-1.667-.986V5.653Z",
    "pause":            "M15.75 5.25v13.5m-7.5-13.5v13.5",
    "stop":             "M5.25 7.5A2.25 2.25 0 0 1 7.5 5.25h9a2.25 2.25 0 0 1 2.25 2.25v9a2.25 2.25 0 0 1-2.25 2.25h-9a2.25 2.25 0 0 1-2.25-2.25v-9Z",
    "info":             "M11.25 11.25l.041-.02a.75.75 0 0 1 1.063.852l-.708 2.836a.75.75 0 0 0 1.063.853l.041-.021M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-3.75h.008v.008H12V8.25Z",
    "warning":          "M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126ZM12 15.75h.008v.008H12v-.008Z",
    "error":            "M12 9v3.75m9-.75a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 3.75h.008v.008H12v-.008Z",
    "lock":             "M16.5 10.5V6.75a4.5 4.5 0 1 0-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 0 0 2.25-2.25v-6.75a2.25 2.25 0 0 0-2.25-2.25H6.75a2.25 2.25 0 0 0-2.25 2.25v6.75a2.25 2.25 0 0 0 2.25 2.25Z",
    "favorite":         "M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12Z",
    "mail":             "M21.75 6.75v10.5a2.25 2.25 0 0 1-2.25 2.25h-15a2.25 2.25 0 0 1-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0 0 19.5 4.5h-15a2.25 2.25 0 0 0-2.25 2.25m19.5 0v.243a2.25 2.25 0 0 1-1.07 1.916l-7.5 4.615a2.25 2.25 0 0 1-2.36 0L3.32 8.91a2.25 2.25 0 0 1-1.07-1.916V6.75",
    "notifications":    "M14.857 17.082a23.848 23.848 0 0 0 5.454-1.31A8.967 8.967 0 0 1 18 9.75V9A6 6 0 0 0 6 9v.75a8.967 8.967 0 0 1-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 0 1-5.714 0m5.714 0a3 3 0 1 1-5.714 0",
}

_DEFAULT_HEROICON_PATH = (
    "M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-"
    "0.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 5.25h.008v.008H12v-.008Z"
)


def flutter_icon(name: str | None) -> str:
    """Return the Material Symbols identifier (without `Icons.` prefix)."""
    if not name:
        return "circle"
    n = _normalize(name)
    return _FLUTTER_ICONS.get(n, n if n.isidentifier() else "circle")


def heroicon_svg(name: str | None, *, classes: str = "w-5 h-5") -> str:
    """Return a complete `<svg>` element rendering the named icon."""
    path = _HEROICON_PATHS.get(_normalize(name or ""), _DEFAULT_HEROICON_PATH)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" '
        f'stroke-width="1.5" stroke="currentColor" class="{classes}" aria-hidden="true">'
        f'<path stroke-linecap="round" stroke-linejoin="round" d="{path}" />'
        f"</svg>"
    )


def _normalize(name: str) -> str:
    return "".join(c if c.isalnum() else "_" for c in name).lower().strip("_")
