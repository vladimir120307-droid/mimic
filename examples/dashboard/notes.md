# Example: Dashboard with navigation

A two-screen flow:

1. **Home** — branded app bar, hero card greeting, list of categories, floating action button
2. **Activity** — destination reached by tapping a list item or the FAB. Simple app bar + empty-state text.

Demonstrates everything in the login example **plus**:

- Multi-screen `WidgetTree` (two `Screen` objects)
- `Interaction` entries linking source widgets (`li1`, `fab`) to a target screen
- Navigation generated automatically in all three targets:
  - Flutter — `Navigator.push` (TODO: routing scaffold)
  - HTML — inline JS router showing/hiding sections
  - React — `react-router-dom` + `useNavigate`

## Reproduce

```bash
mimic gen <any-input-image> --provider mock:dashboard --target react --out ./out
cd ./out && npm install && npm run dev
```

Open the resulting localhost URL; click the list item — `react-router` navigates to `/details`.

## Quality notes

What works:
- Cross-screen widget reuse (interactions correctly target widgets by ID)
- All three targets emit functioning navigation, not just static pages
- Tailwind classes map cleanly even for unusual brand colors (arbitrary-value syntax `bg-[#6E56CF]`)

Known limitations:
- Interaction inference uses tap targets only — no scroll/drag/text-input in mock fixtures yet
- Generated `lib/main.dart` for Flutter doesn't yet wire `Navigator`; user must connect screens manually for v0.1
- HTML router is intentionally tiny (~10 lines) — for richer transitions, switch to React target
