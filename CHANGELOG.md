# Changelog

All notable changes to mimic are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- VS Code extension `vscode-mimic` in `tooling/vscode-mimic/` — right-click any screenshot in the explorer to generate code. Configurable target / provider / output directory.
- Six mock fixtures (`login`, `dashboard`, `chat`, `calendar`, `ecommerce`, `settings`) — selectable via `--provider mock:<name>` for offline demos and as test fixtures.
- `theme.extract()` — derives a named palette and typography from any `WidgetTree`, used by codegen targets to emit `ColorScheme.fromSeed` (Flutter) and Tailwind theme tokens.
- Component deduplication — repeated subtrees (e.g. product cards) are hoisted into a shared `_SharedN` widget in the Flutter target.
- Flutter generator now emits real `MaterialApp.routes` with `Navigator.pushNamed` wiring for every `tap` interaction.

### Tests

- 42 Python tests pass; 10 native tests pass on Windows.

## [0.1.0] — initial release

### Added

- Three-layer monorepo (native C++, Python orchestrator, Flutter desktop UI).
- Bilingual EN/RU documentation (README, ARCHITECTURE, ROADMAP, CONTRIBUTING, BUILDING).
- C++20 capture core:
  - Windows: real `IDXGIOutputDuplication` implementation with cursor compositing and DPI-aware enumeration.
  - macOS: `ScreenCaptureKit` (`SCStream`) implementation.
  - Linux: XCB + MIT-SHM implementation (X11; PipeWire/Wayland in v0.2).
  - `dhash` perceptual hash + `Deduplicator` for native frame dedup.
  - `pybind11` Python bindings.
- Python orchestrator (`mimic-cli`):
  - Vision providers: Anthropic Claude, OpenAI GPT-4V, deterministic mock fixtures, local model stub.
  - Code generators: Flutter (Material 3), HTML + Tailwind, React + Vite + react-router.
  - Multi-frame `segmentation` clusters captures into distinct UI states.
  - `mimic doctor` diagnostics, `mimic serve` JSON-RPC server for the desktop UI.
- Flutter desktop UI scaffold (Riverpod + go_router).
- GitHub Actions CI matrix: Ubuntu/macOS/Windows × Python 3.10/3.11/3.12 + native build + Flutter analyze/test.

[Unreleased]: https://github.com/Cyber-Lord/mimic/compare/v0.1.0...HEAD
[0.1.0]:      https://github.com/Cyber-Lord/mimic/releases/tag/v0.1.0
