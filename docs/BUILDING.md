# Building from source

## Prerequisites

| Tool    | Minimum | Notes                                              |
| ------- | ------- | -------------------------------------------------- |
| CMake   | 3.20    | Native core build                                  |
| Python  | 3.10    | Orchestrator                                       |
| Flutter | 3.19    | Desktop UI (only needed if building the GUI)       |
| Ninja   | latest  | Recommended CMake generator                        |

Platform-specific:

- **Windows**: Visual Studio 2022 Build Tools (or full IDE), Windows 10 SDK 10.0.20348.0+
- **macOS**: Xcode Command Line Tools, macOS 12.3+ for ScreenCaptureKit
- **Linux**: gcc 11+ or clang 14+, `libpipewire-0.3-dev` (for capture portal)

## Quick build (everything)

```bash
# macOS / Linux
./scripts/build.sh

# Windows (PowerShell)
./scripts/build.ps1
```

This builds native, installs the Python package in editable mode, and runs `flutter pub get`. After this, `mimic` is available on PATH inside the activated venv.

## Step-by-step

### 1. Native core

```bash
cd native
cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Release
cmake --build build --parallel
```

Produces `native/build/libmimic_capture.{so,dylib,dll}` and Python bindings as `native/build/_mimic_capture*.{so,pyd}`.

### 2. Python orchestrator

```bash
cd python
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

The `[dev]` extras include pytest, ruff, mypy, and pybind11 stubs. Without them you can only run, not develop.

### 3. Flutter UI (optional)

```bash
cd ui
flutter config --enable-windows-desktop --enable-macos-desktop --enable-linux-desktop
flutter pub get
flutter run -d windows                 # or macos / linux
```

### 4. Verify

```bash
cd python
pytest -q                              # should pass
mimic --version
mimic gen ../examples/login_screen.png --target flutter --out /tmp/out
```

## Troubleshooting

- **`pybind11` not found**: install via `pip install pybind11` inside your venv, or via your system package manager.
- **DXGI capture fails on Windows**: ensure the Graphics adapter driver is recent (Windows 10 1809+). Some virtual displays do not expose duplication.
- **PipeWire missing on Linux**: install `libpipewire-0.3-dev`. On X11-only setups, mimic falls back to XCB shm; performance is lower.
- **Flutter desktop not enabled**: run `flutter config --enable-<platform>-desktop` and `flutter doctor`.

## Release builds

For distribution, use `scripts/release.sh` (writes to `dist/`). This produces a self-contained tarball with native libs, Python wheel, and Flutter binary per platform.
