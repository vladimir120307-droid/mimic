<div align="center">

<img src="assets/logo.svg" alt="mimic" width="160" />

# mimic

**Записал экран — получил рабочий код.**

Превращает запись экрана (или один скриншот) в чистый код на **Flutter**, **HTML/Tailwind** или **React** — вместе с распознанными кликами и переходами между экранами.

[English](README.md) · [Русский](README.ru.md)

[![CI](https://img.shields.io/github/actions/workflow/status/vladimir120307-droid/mimic/ci.yml?branch=main&label=CI)](https://github.com/vladimir120307-droid/mimic/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PyPI](https://img.shields.io/pypi/v/mimic-cli?label=PyPI)](https://pypi.org/project/mimic-cli/)
[![Python](https://img.shields.io/pypi/pyversions/mimic-cli?label=python)](https://pypi.org/project/mimic-cli/)
[![Stars](https://img.shields.io/github/stars/vladimir120307-droid/mimic?style=social)](https://github.com/vladimir120307-droid/mimic/stargazers)
[![Made with Flutter](https://img.shields.io/badge/Made_with-Flutter-02569B?logo=flutter)](https://flutter.dev)
[![VS Code](https://img.shields.io/badge/VS_Code-Extension-007ACC?logo=visualstudiocode)](tooling/vscode-mimic)

**📺 [Живая галерея примеров](https://vladimir120307-droid.github.io/mimic/)** — кликни любую фикстуру и увидишь HTML, который mimic сгенерировал, прямо в браузере.

<img src="assets/demo.gif" alt="mimic demo" width="720" />

</div>

---

## Что это такое

**mimic** — open-source инструмент, который смотрит как ты пользуешься любым UI и воспроизводит его в виде кода. Бросаешь скриншот или запись экрана — на выходе получаешь рабочее Flutter-дерево виджетов, HTML/Tailwind-страницу или React-компонент, и распознанные интеракции сохраняются.

Существующие screenshot-to-code инструменты работают только со статичными картинками. **mimic добавляет измерение, которого нет у конкурентов:**

- 🎥 **Видео, а не только скриншоты** — записывает целые сценарии: клики, переходы, изменения состояний
- 🦋 **Flutter как основной таргет** — пишется людьми, которые реально шипят на Flutter
- 🖥️ **Нативный захват экрана на C++** — суб-миллисекунда на кадр, не жжёт кулер как Electron-based инструменты
- 🔌 **Сменные модели** — из коробки Claude и GPT-4V, локальные vision-модели (Florence-2, Llava) в ближайших релизах
- 🔒 **Локальный режим** — облако не обязательно, твой экран не покидает машину

## Быстрый старт

```bash
# установка
pip install mimic-cli

# попробовать без API-ключа — на встроенной фикстуре
mimic gen any.png --provider mock:dashboard --target react-ts --out ./demo

# скриншот → Flutter (нужен ANTHROPIC_API_KEY)
mimic gen screenshot.png --target flutter --out lib/

# создать новый проект из примера
mimic init my-app --fixture ecommerce --target react-ts

# запись экрана → Flutter (15 секунд)
mimic record --duration 15 --target flutter --out lib/

# превью без записи на диск
mimic gen screenshot.png --target html --dry-run

# диагностика окружения
mimic doctor

# бенчмарк скорости кодогенерации
mimic bench --target flutter
```

> Нет API-ключа? Используй `--provider mock:login` или `--provider mock:dashboard`,
> чтобы сгенерировать из встроенной фикстуры. См. [examples/](examples/) —
> там примеры что mimic выдаёт на всех трёх таргетах.

## Как это работает

```
┌────────────────────┐    ┌─────────────────────┐    ┌──────────────────────┐
│  Нативный захват   │ →  │  Vision + сегментер │ →  │  Генератор кода      │
│  (C++ / DXGI /     │    │  (Claude / GPT-4V / │    │  (Flutter / HTML /   │
│   AVFoundation)    │    │   локально)         │    │   React)             │
└────────────────────┘    └─────────────────────┘    └──────────────────────┘
   быстрые кадры          дерево виджетов              чистый исходник
```

Подробнее — в [docs/ARCHITECTURE.ru.md](docs/ARCHITECTURE.ru.md).

## Выходные таргеты

| Таргет                 | Статус        | Заметки                                                |
| ---------------------- | ------------- | ------------------------------------------------------ |
| Flutter                | 🟢 v0.1       | Material 3 кнопки, ColorScheme, Navigator маршруты     |
| HTML + Tailwind        | 🟢 v0.1       | Один файл, inline `tailwind.config` с палитрой         |
| React + Tailwind       | 🟢 v0.1       | Vite + react-router + theme.extend палитра             |
| React + TypeScript     | 🟢 v0.1       | `.tsx`, типизированный RouteMap, полный tsconfig       |
| **Vue 3 + Tailwind**   | 🟢 v0.2       | Vite + vue-router + однофайловые `.vue` компоненты     |
| SwiftUI                | ⚪ план       | Нативный iOS/macOS                                     |
| Jetpack Compose        | ⚪ план       | Нативный Android                                       |

## Сравнение с альтернативами

| Инструмент                                                              | Видео-ввод | Flutter | TypeScript | Дедуп компонентов | Open source | Self-hosted |
| ----------------------------------------------------------------------- | :--------: | :-----: | :--------: | :---------------: | :---------: | :---------: |
| **mimic** (этот проект)                                                 |    ✅      |   ✅    |     ✅     |        ✅          |    MIT      |     ✅      |
| [abi/screenshot-to-code](https://github.com/abi/screenshot-to-code)     |    ❌      |   ❌    |     ✅     |        ❌          |   MIT       |     ✅      |
| [Locofy](https://www.locofy.ai/)                                        |    ❌      |   ✅    |     ✅     |     частично       |  закрытый   |     ❌      |
| [Anima](https://www.animaapp.com/)                                      |    ❌      |   ❌    |     ✅     |     частично       |  закрытый   |     ❌      |
| [Builder.io Visual Copilot](https://www.builder.io/m/visual-copilot)    |    ❌      |   ❌    |     ✅     |     частично       |  закрытый   |     ❌      |

mimic — единственный open-source инструмент, который **поддерживает Flutter как основной таргет** и принимает **видео**, а не только статичный скриншот. Всё работает **локально** — Figma-файл не требуется, в облако ничего не уходит.

## Дорожная карта

См. [docs/ROADMAP.ru.md](docs/ROADMAP.ru.md). Кратко:

- **v0.1** — Скриншот → Flutter / HTML / React через Claude Vision (✅ зашиплено: скелет, codegen, нативный DXGI-захват, mock-провайдер, JSON-RPC сервер, doctor)
- **v0.2** — Полировка видео-захвата, распознавание click-flow в vision-промптах, PipeWire/Wayland для Linux
- **v0.3** — Живой preview — видишь код по мере записи
- **v0.4** — Локальная vision-модель (Florence-2 / Llava)
- **v1.0** — Знание UI-библиотек (Material 3, shadcn/ui и т.д.)

## Структура проекта

```
mimic/
├── native/          # C++ ядро захвата экрана (DXGI / AVFoundation / PipeWire)
├── python/          # Оркестратор: vision + codegen, точка входа CLI
├── ui/              # Десктоп-приложение на Flutter
├── docs/            # Архитектура, дорожная карта, гайд для контрибьюторов
└── examples/        # Примеры входов и сгенерированных выходов
```

## Сборка из исходников

Нужны CMake ≥ 3.20, Python ≥ 3.10, Flutter ≥ 3.19.

```bash
# всё сразу
./scripts/build.sh        # macOS / Linux
./scripts/build.ps1       # Windows
```

Покомпонентные инструкции — [docs/BUILDING.ru.md](docs/BUILDING.ru.md).

## Вклад в проект

PR приветствуются. Перед открытием прочти [docs/CONTRIBUTING.ru.md](docs/CONTRIBUTING.ru.md). Хорошие первые задачи помечены тегом [`good first issue`](https://github.com/vladimir120307-droid/mimic/labels/good%20first%20issue).

## Лицензия

[MIT](LICENSE) — делай что хочешь, упоминание приветствуется.

---

<sub>Цель: "хочу этот UI" — единственная спецификация дизайна, которая тебе когда-либо понадобится.</sub>
