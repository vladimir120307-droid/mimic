<div align="center">

<img src="assets/logo.svg" alt="mimic" width="160" />

# mimic

**Записал экран — получил рабочий код.**

Превращает запись экрана (или один скриншот) в чистый код на **Flutter**, **HTML/Tailwind** или **React** — вместе с распознанными кликами и переходами между экранами.

[English](README.md) · [Русский](README.ru.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Stars](https://img.shields.io/github/stars/Cyber-Lord/mimic?style=social)](https://github.com/Cyber-Lord/mimic/stargazers)
[![Discord](https://img.shields.io/badge/Discord-join-7289da)](https://discord.gg/mimic)
[![Made with Flutter](https://img.shields.io/badge/Made_with-Flutter-02569B?logo=flutter)](https://flutter.dev)

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

# скриншот → Flutter
mimic gen screenshot.png --target flutter --out lib/

# запись экрана → Flutter (15 секунд)
mimic record --duration 15 --target flutter --out lib/

# или десктоп-приложение
mimic ui
```

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

| Таргет           | Статус        | Заметки                            |
| ---------------- | ------------- | ---------------------------------- |
| Flutter          | 🟢 v0.1       | Главный — лучшее качество          |
| HTML + Tailwind  | 🟡 v0.2       | На очереди                         |
| React + Tailwind | 🟡 v0.2       | Компонентный вывод                 |
| SwiftUI          | ⚪ план       | Нативный iOS/macOS                 |
| Jetpack Compose  | ⚪ план       | Нативный Android                   |
| Vue              | ⚪ community  | Ждём контрибьюшен                  |

## Дорожная карта

См. [docs/ROADMAP.ru.md](docs/ROADMAP.ru.md). Кратко:

- **v0.1** — Скриншот → Flutter через Claude Vision (✅ в работе)
- **v0.2** — Захват видео, распознавание click-flow, HTML/React таргеты
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

PR приветствуются. Перед открытием прочти [docs/CONTRIBUTING.ru.md](docs/CONTRIBUTING.ru.md). Хорошие первые задачи помечены тегом [`good first issue`](https://github.com/Cyber-Lord/mimic/labels/good%20first%20issue).

## Лицензия

[MIT](LICENSE) — делай что хочешь, упоминание приветствуется.

---

<sub>Цель: "хочу этот UI" — единственная спецификация дизайна, которая тебе когда-либо понадобится.</sub>
