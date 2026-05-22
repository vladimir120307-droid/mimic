# Examples gallery

Six reference fixtures, each generated for all four targets — **Flutter, HTML, React (JS), React (TypeScript)**. Browse the source directly on GitHub to see exactly what mimic produces.

| Example                                    | Screens | Demonstrates                                            |
| ------------------------------------------ | ------- | ------------------------------------------------------- |
| [login](login/notes.md)                    | 1       | Centered form, typography hierarchy, brand button       |
| [dashboard](dashboard/notes.md)            | 2       | App bar, hero card, list with navigation, FAB           |
| [chat](chat/notes.md)                      | 2       | Inbox list, message bubbles, composer with send FAB     |
| [calendar](calendar/notes.md)              | 2       | Month grid, weekday header, upcoming-event card         |
| [ecommerce](ecommerce/notes.md)            | 2       | Product grid (with **component dedup**), detail page    |
| [settings](settings/notes.md)              | 1       | Profile card, switch rows, destructive sign-out button  |

Each fixture lives at `examples/<name>/`:

```
examples/<name>/
  notes.md
  generated/
    flutter/       (Material 3 app with Navigator + ColorScheme)
    html/          (single-file Tailwind, inline palette config)
    react/         (Vite + react-router, JavaScript)
    react-ts/      (Vite + react-router, fully typed TypeScript)
```

## Regenerating

```bash
for fixture in login dashboard chat calendar ecommerce settings; do
  for target in flutter html react react-ts; do
    mimic gen any.png \
      --provider mock:$fixture \
      --target  $target \
      --out     examples/$fixture/generated/$target
  done
done
```

These outputs double as regression fixtures — see `python/tests/test_snapshots.py`. Drift is caught by `pytest`; refresh deliberately with `MIMIC_UPDATE_SNAPSHOTS=1 pytest`.

## What to look at to evaluate quality

1. **Flutter — `examples/ecommerce/generated/flutter/lib/widgets/shared.dart`**
   The 4 product cards were detected as a repeated structure and hoisted into a single `_Shared1` widget. The screen file is correspondingly smaller.

2. **Flutter — `examples/dashboard/generated/flutter/lib/main.dart`**
   `MaterialApp.routes` with `Navigator.pushNamed` wired through the screen and the FAB. Click the FAB in the running app, it navigates.

3. **HTML — `examples/chat/generated/html/index.html`**
   Single self-contained file with Tailwind CDN. Open it directly in a browser; the inline JS router toggles between Inbox and Chat sections.

4. **React — `examples/calendar/generated/react/`**
   Full Vite project. `npm install && npm run dev` and it runs.

## Adding your own example

1. Capture a screenshot.
2. `mimic gen screen.png --target flutter --out examples/<name>/generated/flutter`
3. Write `examples/<name>/notes.md` describing what the example shows and any quality observations.
4. PR. Examples are how we grow the test corpus and the gallery.
