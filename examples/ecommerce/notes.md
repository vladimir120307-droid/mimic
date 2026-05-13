# Example: E-commerce catalog + product detail

A two-screen shopping flow with **repeated structures** — the highlight of this fixture.

- **Catalog** — app bar, search field, 2×2 grid of product cards
- **Product detail** — hero image, title, price, description, "Add to cart" CTA

## Reproduce

```bash
mimic gen any.png --provider mock:ecommerce --target flutter --out ./out
```

Then open `out/lib/widgets/shared.dart`.

## What's interesting

The four product cards share an identical *skeleton* (only the title and price text vary across instances). mimic's component-dedup analysis detects this and hoists the card into `_Shared1` in `lib/widgets/shared.dart`. The catalog screen references it as `const _Shared1()` instead of inlining the structure 4 times.

This is the single best demonstration of how mimic produces code that reads like it was hand-written, not auto-generated.

## Limitations

- Today the shared widget loses per-instance data (title / price) — v0.2 will pass these as constructor arguments instead of dropping them
- The image placeholder is rendered as a colored Container — when real images are detected (image URL), they're emitted as `Image.network(...)` automatically
