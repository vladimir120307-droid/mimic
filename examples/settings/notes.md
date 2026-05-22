# Example: Settings panel

A single-screen settings page exercising more form-y widgets.

- App bar
- Profile card (name + email)
- Notifications group with three toggle rows (`switch` widgets)
- Destructive sign-out button at the bottom

## Reproduce

```bash
mimic gen any.png --provider mock:settings --target react --out ./out
```

## What to look at

- The `switch` widget kind maps to `Switch` (Flutter), an `<input type="checkbox">`-equivalent (HTML), and a Tailwind-styled component (React) — same model, three idiomatic outputs
- Sign-out button uses `#E11D48` (destructive red), detected by `theme.extract` and would be assigned to `ColorScheme.error` in Flutter

## Limitations

- The switches default to `value: true`/`checked` without per-row state inference — fixtures don't currently encode dynamic state
- The destructive button doesn't yet emit a confirmation dialog hook
