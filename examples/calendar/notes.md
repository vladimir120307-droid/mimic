# Example: Calendar with event detail

A two-screen flow showing a month grid and an event detail screen.

- **Month** — weekday header row + 4-week grid + upcoming-event card at the bottom
- **Event detail** — branded app bar, when/where text, primary "Join meeting" button

## Reproduce

```bash
mimic gen any.png --provider mock:calendar --target react --out ./out
cd ./out && npm install && npm run dev
```

## What to look at

- The 28-day grid is generated programmatically in the fixture but renders as a flat list — codegen handles this without complaint
- Tap on the "upcoming event" card navigates to the detail screen
- The brand color (`#10B981` emerald) propagates into both the AppBar background and the join-button background, then is detected by `theme.extract` as the primary

## Limitations

- The weekday header is a `row` with raw text labels — no special semantic kind
- "Next event" card is a single instance, so no component dedup triggers (try the ecommerce fixture for that)
