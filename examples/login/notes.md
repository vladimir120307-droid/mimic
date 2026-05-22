# Example: Login screen

A single-screen sign-in form — logo, title, subtitle, email + password inputs, primary CTA button, sign-up hint link. Demonstrates:

- Centered vertical layout (`column`)
- Typographic hierarchy via `font_size` / `font_weight` styles
- Form inputs (`text_field`)
- Brand-colored primary button
- Subtle helper text

## Reproduce

```bash
mimic gen <any-input-image> --provider mock:login --target flutter --out ./out
```

(Provider `mock:login` returns a hand-crafted `WidgetTree` — `<any-input-image>` is ignored, just needs to be a valid file path. Useful for showing what the codegen layer produces for a known input.)

## What to look at

- `generated/flutter/lib/screens/login_screen.dart` — clean `StatelessWidget` with `Scaffold` → `SafeArea` → `Column` with all elements
- `generated/html/index.html` — drop in a browser, works
- `generated/react/src/screens/Login.jsx` — functional component, Tailwind classes inline

## Quality notes

What works:
- Layout hierarchy preserved
- Colors carried over from style (`#6E56CF` brand color visible on the button)
- Text content faithful

Known limitations (will improve in v0.2):
- No detection of form validation — just placeholder static inputs
- Icon rendering is generic (we emit `Icons.bolt` by name) — better Material 3 mapping coming
- No dark-mode variant
