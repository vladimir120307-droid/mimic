# Architecture

mimic is a three-layer system. Each layer is a separate component with a stable interface so layers can be swapped independently — replace Claude with a local model, swap the C++ capture for a Python fallback, target a new framework without touching capture or vision.

```
┌──────────────────────────────────────────────────────────────┐
│                  Layer 3: Flutter Desktop UI                 │
│  Recording controls · live preview · code editor · export    │
└─────────────────────────┬────────────────────────────────────┘
                          │ FFI / local IPC
┌─────────────────────────▼────────────────────────────────────┐
│                  Layer 2: Python Orchestrator                │
│  Vision API · widget-tree builder · code generators · CLI    │
└────────────┬─────────────────────────────────┬───────────────┘
             │ pybind11                        │ HTTP / SDK
┌────────────▼────────────┐         ┌──────────▼───────────────┐
│   Layer 1: Native C++   │         │   Vision provider        │
│   Screen capture core   │         │   (Claude · GPT-4V ·     │
│   DXGI · AVFoundation · │         │    local Florence/Llava) │
│   PipeWire · frame dedup│         └──────────────────────────┘
└─────────────────────────┘
```

## Layer 1: Native capture core (`native/`)

Written in C++20. The only job of this layer is to deliver frames to Python as fast as possible without burning CPU. Platform-specific implementations behind a single C ABI.

- **Windows** — `IDXGIOutputDuplication` for tear-free capture, copy to staging texture, hand off as raw BGRA.
- **macOS** — `ScreenCaptureKit` (macOS 12.3+), fallback to `CGDisplayStream` for older versions.
- **Linux** — `PipeWire` portal API (Wayland-native, X11 via XCB shm fallback).

Critical optimizations done in C++ before frames cross into Python:

1. **Frame deduplication** — perceptual hash + early reject if `dhash` distance < threshold. Drops ~95% of frames in typical recordings.
2. **Region of interest** — when the user records a single window, mask out the rest.
3. **Mouse/click overlay** — overlays a synthetic cursor with click events on the frame, so the vision model can reason about "where the user pointed" without a separate event stream.

Python sees frames via `pybind11` bindings as `numpy.ndarray`.

## Layer 2: Python orchestrator (`python/`)

The brain. Receives frames (or single screenshots), reasons about UI structure, emits code.

Pipeline:

```
frames ─► dedup ─► segmentation ─► widget-tree ─► codegen ─► files
                       │                │
                       └─► vision API ◄─┘
```

- **Vision adapters** (`vision/`) — common interface, concrete backends for Claude / OpenAI / local. Each backend returns a structured `WidgetTree` (Pydantic model) — not raw text. Models are prompted with strict JSON schema to force structure.
- **Segmentation** — when video is the input, identifies stable UI states across frames (frame clustering by perceptual hash) and labels transitions as interactions.
- **Code generators** (`codegen/`) — each target framework is a `WidgetTree → SourceFile[]` function. Generators are pure: same tree in → same code out. No I/O inside generators.
- **CLI** — `mimic gen`, `mimic record`, `mimic ui` are thin wrappers over the pipeline.

## Layer 3: Flutter desktop UI (`ui/`)

Cross-platform desktop app (Windows / macOS / Linux). Subscribes to the orchestrator via a local IPC channel (default: 127.0.0.1:54321, JSON-RPC). Three main screens:

- **Capture** — region picker, record / stop, target framework toggle.
- **Preview** — split view: rendered preview of the generated UI on the left, source code on the right with syntax highlighting and inline edit.
- **Library** — recent recordings with their generated artifacts, organized by project.

UI is intentionally thin. All logic lives in Python — Flutter is a window onto the pipeline. This lets headless / CI use the same backend.

## Why these technology choices

| Decision                       | Reason                                                       | Alternative considered                |
| ------------------------------ | ------------------------------------------------------------ | ------------------------------------- |
| C++ for capture                | Sub-ms per frame, native zero-copy paths                     | Rust (similar perf, smaller ecosystem) |
| Python for orchestration       | Vision SDK ecosystem lives here, prototyping speed           | Go / Rust (worse for ML iteration)    |
| Flutter for UI                 | Single codebase, native performance, matches Flutter target  | Electron (heavy), Tauri (less mature) |
| JSON-RPC over local TCP        | Lets Flutter app be language-agnostic and detachable         | Direct FFI (couples them tighter)     |
| Pluggable vision provider      | Avoids lock-in, enables local-first                          | Single provider (easier but fragile)  |

## Data flow: a 15-second recording

1. User hits Record in the Flutter app.
2. Flutter sends `start_recording` over JSON-RPC.
3. Python calls into native via pybind11 — frames stream into a ring buffer.
4. Native dedup drops ~95% of frames; remaining ~5 frames/sec go to Python.
5. Python segments the run into ~3-5 distinct UI states.
6. For each unique state, vision API returns a `WidgetTree`.
7. Transitions between states are annotated as interactions (`onTap`, `onScroll`, etc.).
8. Flutter codegen walks the tree → emits `lib/screens/*.dart`, `lib/widgets/*.dart`, `lib/main.dart`.
9. Files appear in the Flutter UI's preview pane; user can edit before exporting.

End-to-end target latency for v0.2: under 10 seconds for a 15-second clip on a typical laptop.

## Non-goals

- We do not aim to be a Figma replacement. mimic generates code from observed UI, not from design intent.
- We do not generate full applications. mimic generates UI scaffolding; business logic, routing, and data layer are still on you.
- We do not record audio or keystrokes (beyond what's visible in the UI). Privacy and scope.
