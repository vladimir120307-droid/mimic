# Contributing

Thanks for considering a contribution. mimic is a young project and most things are still in flux — that means high-impact contributions are easy to find.

## Before you start

1. Check [open issues](https://github.com/vladimir120307-droid/mimic/issues), especially those tagged [`good first issue`](https://github.com/vladimir120307-droid/mimic/labels/good%20first%20issue) and [`help wanted`](https://github.com/vladimir120307-droid/mimic/labels/help%20wanted).
2. For anything bigger than a small fix, open an issue first describing what you want to do. We will tell you if we are already working on it, or if the design space is constrained.
3. Read [ARCHITECTURE.md](ARCHITECTURE.md). PRs that fight the architecture get pushed back; PRs that fit it get merged fast.

## Setting up

```bash
git clone https://github.com/vladimir120307-droid/mimic
cd mimic

# Python orchestrator
cd python
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -e ".[dev]"

# Native core
cd ../native
cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug
cmake --build build

# Flutter UI
cd ../ui
flutter pub get
```

Verify your setup:

```bash
cd python
pytest                   # all tests should pass
mimic --help             # CLI is on PATH
```

## Project conventions

### Code style

- **C++** — clang-format, style file in `native/.clang-format`. Run `clang-format -i` on touched files.
- **Python** — ruff for linting + formatting. `ruff check .` and `ruff format .` before committing.
- **Dart** — `dart format .` and `flutter analyze`.

### Commit messages

Conventional Commits style:

```
feat(codegen): support nested Material 3 buttons
fix(capture): handle DPI scaling on Windows
docs(readme): clarify install instructions
test(vision): add fixture for dark-mode screenshots
```

Scopes match top-level folders (`native`, `python`, `ui`, `docs`).

### Branches

- `main` — protected, releases tagged from here
- Feature branches: `feat/<short-description>` or `fix/<short-description>`
- One PR = one logical change. Multiple unrelated changes → multiple PRs.

### Tests

- Python: pytest, ≥80% coverage on `python/src/mimic`. Touched code needs a test.
- C++: GoogleTest in `native/tests`. Touched code needs a test if the platform supports the path.
- Dart: `flutter test` for unit/widget tests, optional but appreciated.

### What we will say no to

- Changes that hardcode a vendor (e.g. only Claude, no abstraction)
- New top-level dependencies without discussion (build time matters)
- Code generation that emits unreadable output ("works but ugly")
- Features that grow scope without a use case in [ROADMAP.md](ROADMAP.md)

## Reporting bugs

Open an issue with:

1. Your platform (OS + version)
2. mimic version (`mimic --version`)
3. Minimal reproducer (input file + command)
4. What you expected vs what happened

Screenshots / recordings welcome. Logs from `mimic --log-level debug` are gold.

## Reporting security issues

Do not open a public issue. Email security@mimic.dev (PGP key in [SECURITY.md](../SECURITY.md)).

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](../LICENSE).
