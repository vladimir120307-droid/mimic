<div align="center">

<img src="assets/logo.svg" alt="mimic" width="160" />

# mimic

**Record your screen → get working code.**

Turn a screen recording (or a single screenshot) into clean **Flutter**, **HTML/Tailwind**, or **React** code — including detected click flows and state transitions.

[English](README.md) · [Русский](README.ru.md)

[![CI](https://img.shields.io/github/actions/workflow/status/vladimir120307-droid/mimic/ci.yml?branch=main&label=CI)](https://github.com/vladimir120307-droid/mimic/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PyPI](https://img.shields.io/pypi/v/mimic-cli?label=PyPI)](https://pypi.org/project/mimic-cli/)
[![Python](https://img.shields.io/pypi/pyversions/mimic-cli?label=python)](https://pypi.org/project/mimic-cli/)
[![Stars](https://img.shields.io/github/stars/vladimir120307-droid/mimic?style=social)](https://github.com/vladimir120307-droid/mimic/stargazers)
[![Made with Flutter](https://img.shields.io/badge/Made_with-Flutter-02569B?logo=flutter)](https://flutter.dev)
[![VS Code](https://img.shields.io/badge/VS_Code-Extension-007ACC?logo=visualstudiocode)](tooling/vscode-mimic)

<img src="assets/demo.gif" alt="mimic demo" width="720" />

</div>

---

## What is mimic?

**mimic** is an open-source tool that watches you use any UI and reproduces it as code. Drop in a screenshot or a screen recording — get back a working Flutter widget tree, a HTML/Tailwind page, or a React component, with detected interactions intact.

Existing screenshot-to-code tools handle static images. **mimic adds the dimension competitors don't have:**

- 🎥 **Video, not just screenshots** — captures whole click flows, transitions, and state changes
- 🦋 **Flutter as a first-class target** — written by people who actually ship Flutter
- 🖥️ **Native screen capture in C++** — sub-millisecond per frame, doesn't fry your fan like Electron-based tools
- 🔌 **Pluggable models** — works with Claude, GPT-4V out of the box, local vision models (Florence-2, Llava) coming
- 🔒 **Local-first option** — no cloud round-trip required, your screen never leaves your machine

## Quickstart

```bash
# install
pip install mimic-cli

# try without an API key — uses a hand-crafted fixture
mimic gen any.png --provider mock:dashboard --target react-ts --out ./demo

# screenshot → Flutter (needs ANTHROPIC_API_KEY)
mimic gen screenshot.png --target flutter --out lib/

# scaffold a brand-new project pre-seeded with an example
mimic init my-app --fixture ecommerce --target react-ts

# record screen → Flutter (15 seconds)
mimic record --duration 15 --target flutter --out lib/

# preview without writing files
mimic gen screenshot.png --target html --dry-run

# diagnose your environment
mimic doctor

# benchmark the codegen pipeline
mimic bench --target flutter
```

> No API key? Use `--provider mock:login` or `--provider mock:dashboard`
> to generate from a built-in fixture. See [examples/](examples/) for the
> kind of output mimic produces, all three targets included.

## How it works

```
┌────────────────────┐    ┌─────────────────────┐    ┌──────────────────────┐
│  Native capture    │ →  │  Vision + segmenter │ →  │  Code generator      │
│  (C++ / DXGI /     │    │  (Claude / GPT-4V / │    │  (Flutter / HTML /   │
│   AVFoundation)    │    │   local)            │    │   React)             │
└────────────────────┘    └─────────────────────┘    └──────────────────────┘
       fast frames           widget tree                  clean source code
```

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for the full design.

## Output targets

| Target              | Status        | Notes                                              |
| ------------------- | ------------- | -------------------------------------------------- |
| Flutter             | 🟢 v0.1       | Material 3 buttons, ColorScheme, Navigator routes  |
| HTML + Tailwind     | 🟢 v0.1       | Single-file, inline `tailwind.config` palette      |
| React + Tailwind    | 🟢 v0.1       | Vite + react-router + theme.extend palette         |
| **React + TypeScript** | 🟢 v0.1    | `.tsx`, typed RouteMap, full tsconfig              |
| SwiftUI             | ⚪ planned    | iOS/macOS native                                   |
| Jetpack Compose     | ⚪ planned    | Android native                                     |
| Vue                 | ⚪ community  | Contributions welcome                              |

## Roadmap

See [docs/ROADMAP.md](docs/ROADMAP.md). Highlights:

- **v0.1** — Screenshot → Flutter / HTML / React via Claude Vision (✅ shipped: scaffolding, codegen, native DXGI capture, mock provider, JSON-RPC server, doctor)
- **v0.2** — Video capture polish, click-flow detection in vision prompts, PipeWire/Wayland for Linux
- **v0.3** — Live preview window — see code emerge as you record
- **v0.4** — Local vision model option (Florence-2 / Llava)
- **v1.0** — Component library awareness (Material 3, shadcn/ui, etc.)

## Project layout

```
mimic/
├── native/          # C++ screen-capture core (DXGI / AVFoundation / PipeWire)
├── python/          # Orchestrator: vision + codegen, CLI entry point
├── ui/              # Flutter desktop application
├── docs/            # Architecture, roadmap, contribution guide
└── examples/        # Sample inputs and generated outputs
```

## Building from source

Requires CMake ≥ 3.20, Python ≥ 3.10, Flutter ≥ 3.19.

```bash
# all-in-one
./scripts/build.sh        # macOS / Linux
./scripts/build.ps1       # Windows
```

Component-by-component instructions are in [docs/BUILDING.md](docs/BUILDING.md).

## Contributing

PRs welcome. Read [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) before opening one. Good first issues are tagged [`good first issue`](https://github.com/vladimir120307-droid/mimic/labels/good%20first%20issue).

## License

[MIT](LICENSE) — do whatever you want, attribution appreciated.

---

<sub>Built with the goal of making "I want this UI" the only design spec you ever need.</sub>
