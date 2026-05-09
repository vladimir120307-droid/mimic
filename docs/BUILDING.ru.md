# Сборка из исходников

## Требования

| Инструмент | Минимум | Заметки                                            |
| ---------- | ------- | -------------------------------------------------- |
| CMake      | 3.20    | Сборка нативного ядра                              |
| Python     | 3.10    | Оркестратор                                        |
| Flutter    | 3.19    | Десктоп-UI (нужно только если собираем GUI)        |
| Ninja      | latest  | Рекомендуемый генератор CMake                      |

Платформенное:

- **Windows**: Visual Studio 2022 Build Tools (или полная IDE), Windows 10 SDK 10.0.20348.0+
- **macOS**: Xcode Command Line Tools, macOS 12.3+ для ScreenCaptureKit
- **Linux**: gcc 11+ или clang 14+, `libxcb1-dev` + `libxcb-shm0-dev` для X11-захвата. (Wayland через PipeWire — v0.2, см. docs/ROADMAP.ru.md.)

## Быстрая сборка (всё сразу)

```bash
# macOS / Linux
./scripts/build.sh

# Windows (PowerShell)
./scripts/build.ps1
```

Собирает нативный код, ставит Python-пакет в editable-режиме, запускает `flutter pub get`. После этого `mimic` доступен в PATH внутри активированного venv.

## По шагам

### 1. Нативное ядро

```bash
cd native
cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Release
cmake --build build --parallel
```

Выдаёт `native/build/libmimic_capture.{so,dylib,dll}` и Python-биндинги `native/build/_mimic_capture*.{so,pyd}`.

### 2. Python-оркестратор

```bash
cd python
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

Extras `[dev]` включают pytest, ruff, mypy и pybind11-stubs. Без них можно только запускать, но не разрабатывать.

### 3. Flutter UI (опционально)

```bash
cd ui
flutter config --enable-windows-desktop --enable-macos-desktop --enable-linux-desktop
flutter pub get
flutter run -d windows                 # или macos / linux
```

### 4. Проверка

```bash
cd python
pytest -q                              # должно пройти
mimic --version
mimic gen ../examples/login_screen.png --target flutter --out /tmp/out
```

## Траблшутинг

- **`pybind11` не найден**: установи через `pip install pybind11` в venv или через системный пакетный менеджер.
- **DXGI capture падает на Windows**: убедись что драйвер видеоадаптера свежий (Windows 10 1809+). Некоторые виртуальные дисплеи не поддерживают duplication.
- **PipeWire отсутствует на Linux**: поставь `libpipewire-0.3-dev`. На X11-only mimic падает на XCB shm — производительность ниже.
- **Flutter desktop не включён**: запусти `flutter config --enable-<platform>-desktop` и `flutter doctor`.

## Релизные сборки

Для дистрибуции — `scripts/release.sh` (пишет в `dist/`). Выдаёт self-contained tarball с нативными библиотеками, Python wheel и Flutter-бинарём для каждой платформы.
