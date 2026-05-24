# Changelog

All notable changes to mimic are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.3.0] — parameterized dedup + SwiftUI

### Added

- **SwiftUI target** (`--target swiftui`) — full Swift Package: `Package.swift`, `@main App` with `NavigationStack`, one `View` per `Screen`, `Color(hex:)` extension keyed off the extracted palette. Tap interactions become `NavigationLink`. Opens the iOS / macOS native audience.
- **Parameterized component dedup** — repeated subtrees that differ only in leaf content (`text`, `icon_name`, `image_url`, `placeholder`) are now hoisted into a shared widget with **typed constructor parameters**. The ecommerce fixture's 4 product cards collapse into one `_Shared1` widget; per-instance titles / prices / image URLs are passed through named slots and rendered verbatim. Restores the v0.1 "wow" demo without the v0.2 regression of dropping content.
- **Multi-child cards** — `card` / `container` / `scroll_view` widgets with more than one child now wrap children in a `Column(crossAxisAlignment: .start)` instead of silently keeping only the first.
- Snapshot suite grew to **36 cases** (6 fixtures × 6 targets, +6 over v0.2).

### Fixed

- Snapshot test now parameterizes over the full target set, including `swiftui`.

## [0.2.0] — quality + breadth

### Added

- **Vue 3 + Vite + Tailwind target** (`vue`) — single-file components under `src/views/`, `vue-router` with hash history, palette materialized in `tailwind.config.js`. Closes [#9](https://github.com/vladimir120307-droid/mimic/issues/9).
- **Material Symbols / Heroicons icon mapping** — `icon` widgets emit real `Icons.send`, `Icons.calendar_today`, etc. in Flutter; inline Heroicons SVG paths in HTML / React / Vue. No more bullet placeholders. Closes [#10](https://github.com/vladimir120307-droid/mimic/issues/10).
- **Image asset handling** in mock fixtures — ecommerce now references real `picsum.photos` URLs, generating `Image.network` (Flutter) and `<img>` (HTML/React/Vue) instead of placeholder containers.
- Snapshot suite expanded from 24 to 30 cases (6 fixtures × 5 targets).

### Changed

- **Dedup is now strict** — only collapses subtrees that are byte-for-byte identical (including text and icon names). Previous loose-skeleton matching silently dropped per-instance content like product titles. Trade-off: ecommerce fixture no longer shows `_Shared1` for product cards; their differing titles/prices are now preserved verbatim. Parameterized dedup (hoisting structure + passing leaf content as ctor args) is tracked for a future minor release.

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

[Unreleased]: https://github.com/vladimir120307-droid/mimic/compare/v0.3.0...HEAD
[0.3.0]:      https://github.com/vladimir120307-droid/mimic/releases/tag/v0.3.0
[0.2.0]:      https://github.com/vladimir120307-droid/mimic/releases/tag/v0.2.0
[0.1.0]:      https://github.com/vladimir120307-droid/mimic/releases/tag/v0.1.0
