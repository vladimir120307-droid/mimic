#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BUILD_TYPE="${BUILD_TYPE:-Release}"

echo "==> Building native core ($BUILD_TYPE)"
cmake -S "$ROOT/native" -B "$ROOT/native/build" -G Ninja -DCMAKE_BUILD_TYPE="$BUILD_TYPE"
cmake --build "$ROOT/native/build" --parallel

echo "==> Installing Python package (editable)"
cd "$ROOT/python"
if [[ ! -d .venv ]]; then python3 -m venv .venv; fi
# shellcheck disable=SC1091
source .venv/bin/activate
pip install --upgrade pip
pip install -e ".[dev]"

echo "==> Fetching Flutter packages"
cd "$ROOT/ui"
flutter pub get

echo "==> Done. To run:"
echo "   mimic --help"
echo "   cd $ROOT/ui && flutter run -d \$(uname | tr '[:upper:]' '[:lower:]')"
