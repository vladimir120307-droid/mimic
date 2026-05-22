# Вклад в проект

Спасибо что рассматриваешь возможность участвовать. mimic — молодой проект, многое ещё в движении — это значит, что задачи с высоким импактом легко найти.

## Перед началом

1. Посмотри [открытые issue](https://github.com/vladimir120307-droid/mimic/issues), особенно с тегами [`good first issue`](https://github.com/vladimir120307-droid/mimic/labels/good%20first%20issue) и [`help wanted`](https://github.com/vladimir120307-droid/mimic/labels/help%20wanted).
2. Для всего крупнее мелкого фикса — открой issue с описанием, что хочешь сделать. Скажем, делает ли это уже кто-то, и есть ли ограничения по архитектуре.
3. Прочитай [ARCHITECTURE.ru.md](ARCHITECTURE.ru.md). PR, которые ломают архитектуру, отвергаются; PR, которые вписываются, мёрджатся быстро.

## Настройка окружения

```bash
git clone https://github.com/vladimir120307-droid/mimic
cd mimic

# Python-оркестратор
cd python
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -e ".[dev]"

# Нативное ядро
cd ../native
cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug
cmake --build build

# Flutter UI
cd ../ui
flutter pub get
```

Проверка установки:

```bash
cd python
pytest                   # все тесты должны проходить
mimic --help             # CLI доступна в PATH
```

## Конвенции проекта

### Стиль кода

- **C++** — clang-format, файл стиля в `native/.clang-format`. Запускай `clang-format -i` на изменённых файлах.
- **Python** — ruff для линтинга + форматирования. `ruff check .` и `ruff format .` перед коммитом.
- **Dart** — `dart format .` и `flutter analyze`.

### Сообщения коммитов

Стиль Conventional Commits:

```
feat(codegen): support nested Material 3 buttons
fix(capture): handle DPI scaling on Windows
docs(readme): clarify install instructions
test(vision): add fixture for dark-mode screenshots
```

Scope совпадает с папками верхнего уровня (`native`, `python`, `ui`, `docs`).

### Ветки

- `main` — защищённая, релизы тегаются отсюда
- Feature-ветки: `feat/<краткое-описание>` или `fix/<краткое-описание>`
- Один PR = одно логическое изменение. Несколько несвязанных изменений → несколько PR.

### Тесты

- Python: pytest, покрытие ≥80% на `python/src/mimic`. Изменённый код требует теста.
- C++: GoogleTest в `native/tests`. Изменённый код требует тест, если платформа поддерживает путь.
- Dart: `flutter test` для unit/widget-тестов, опционально но приветствуется.

### На что скажем нет

- Изменения, хардкодящие вендора (например только Claude без абстракции)
- Новые top-level зависимости без обсуждения (время сборки важно)
- Кодогенерация, выдающая нечитаемый вывод ("работает но уродливо")
- Фичи, раздувающие scope без use case в [ROADMAP.ru.md](ROADMAP.ru.md)

## Багрепорты

Открой issue с:

1. Платформа (OS + версия)
2. Версия mimic (`mimic --version`)
3. Минимальный репродьюсер (входной файл + команда)
4. Что ожидал vs что получил

Скриншоты / записи приветствуются. Логи `mimic --log-level debug` — золото.

## Уязвимости безопасности

Не открывай публичный issue. Пиши на security@mimic.dev (PGP-ключ в [SECURITY.md](../SECURITY.md)).

## Лицензия

Контрибьютя, ты соглашаешься что твой код лицензируется под [MIT License](../LICENSE).
