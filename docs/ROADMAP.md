# Roadmap

Versioned, opinionated, and intentionally short. We ship one thing at a time.

## v0.1 — Screenshot → Flutter (target: this month)

The smallest possible MVP that proves the thesis.

- [x] Project scaffolding
- [ ] `mimic gen IMAGE --target flutter` working end-to-end
- [ ] Claude Vision adapter with structured-output prompting
- [ ] Flutter generator: produces compileable `main.dart` for ~10 reference inputs
- [ ] Basic CLI with `gen` subcommand
- [ ] First demo GIF for README

**Definition of done:** drop a screenshot of any reasonable mobile UI, get a Flutter file that compiles and renders something visibly similar (90%+ structural match).

## v0.2 — Video & multi-target (target: +6 weeks)

Adds the real differentiator and broadens reach.

- [ ] Native screen capture (Windows DXGI first, then macOS, then Linux)
- [ ] Frame dedup in C++ (perceptual hash threshold)
- [ ] Click-flow detection — multiple states stitched into one Flutter app
- [ ] HTML + Tailwind generator
- [ ] React + Tailwind generator
- [ ] `mimic record` CLI subcommand

**Definition of done:** 15-second recording of a multi-screen flow produces a Flutter app with navigation between screens.

## v0.3 — Flutter desktop UI (target: +10 weeks)

Make it accessible to non-CLI users.

- [ ] Flutter app: region picker, record/stop, preview pane
- [ ] Live preview — generated UI rendered as code is produced
- [ ] Inline source editor with syntax highlighting
- [ ] Library view of past recordings
- [ ] Installer for Windows / macOS / Linux

**Definition of done:** a developer can install, click record, and export a working Flutter file without touching a terminal.

## v0.4 — Local model (target: +14 weeks)

Privacy and cost story.

- [ ] Florence-2 adapter (CPU + CUDA)
- [ ] Llava adapter via Ollama
- [ ] Quality regression suite — known-good outputs for each input, % structural match across providers
- [ ] Switchable in CLI flag and UI toggle

**Definition of done:** entire pipeline runs with no network access; quality within 80% of Claude on the regression suite.

## v1.0 — Library awareness (target: end of year)

The polish that separates a popular tool from a default tool.

- [ ] Material 3 component recognition for Flutter target
- [ ] shadcn/ui component recognition for React target
- [ ] Tailwind class deduplication / theme extraction
- [ ] Component reuse — repeated UI elements emitted as shared widgets
- [ ] Plugin API for community-contributed targets (SwiftUI, Compose, Vue)

**Definition of done:** generated code reads like it was written by a Flutter developer, not by a robot.

## Out of scope (for now)

- Mobile-side recording (Android/iOS as recording source)
- Browser-extension version
- Hosted / SaaS version
- Audio/voice annotation of recordings

These may happen later. They are explicitly not blocking v1.0.

## How priority is decided

1. Does it unlock a use case that drives stars / installs?
2. Is the alternative tool worse than ours at it?
3. Can we ship it in under 4 weeks of work?

If yes to all three, it goes near the top. Otherwise it waits.
