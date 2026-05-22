"""`mimic doctor` — diagnose the local environment.

Checks listed in the order users typically run into problems with them.
Each check returns a `CheckResult` with status + remediation hint.
"""

from __future__ import annotations

import importlib
import os
import shutil
import sys
from dataclasses import dataclass
from typing import Literal

Status = Literal["ok", "warn", "fail"]


@dataclass
class CheckResult:
    name: str
    status: Status
    detail: str
    fix: str | None = None


def run_all() -> list[CheckResult]:
    return [
        check_python(),
        check_required_packages(),
        check_native_module(),
        check_fallback_capture(),
        check_anthropic_key(),
        check_openai_key(),
        check_flutter_sdk(),
    ]


def check_python() -> CheckResult:
    v = sys.version_info
    if v >= (3, 10):
        return CheckResult(
            "Python version",
            "ok",
            f"Python {v.major}.{v.minor}.{v.micro}",
        )
    return CheckResult(
        "Python version",
        "fail",
        f"Python {v.major}.{v.minor} found, need 3.10+",
        fix="Install Python 3.10 or newer from https://python.org",
    )


def check_required_packages() -> CheckResult:
    required = ["anthropic", "pydantic", "PIL", "numpy", "rich", "typer"]
    missing = [
        name for name in required if importlib.util.find_spec(name) is None  # type: ignore[attr-defined]
    ]
    if not missing:
        return CheckResult("Python packages", "ok", f"All {len(required)} present")
    return CheckResult(
        "Python packages",
        "fail",
        f"Missing: {', '.join(missing)}",
        fix="pip install -e \".[dev]\" from the python/ directory",
    )


def check_native_module() -> CheckResult:
    if importlib.util.find_spec("_mimic_capture") is None:  # type: ignore[attr-defined]
        return CheckResult(
            "Native capture module",
            "warn",
            "_mimic_capture not built — falling back to mss (slower)",
            fix="Build native/ (see docs/BUILDING.md), then add native/build/python to PYTHONPATH",
        )
    return CheckResult("Native capture module", "ok", "Native module importable")


def check_fallback_capture() -> CheckResult:
    if importlib.util.find_spec("mss") is None:  # type: ignore[attr-defined]
        return CheckResult(
            "Fallback capture (mss)",
            "fail",
            "mss not installed — no capture path available",
            fix="pip install mss",
        )
    return CheckResult("Fallback capture (mss)", "ok", "mss available")


def check_anthropic_key() -> CheckResult:
    if os.environ.get("ANTHROPIC_API_KEY"):
        return CheckResult("ANTHROPIC_API_KEY", "ok", "Set")
    return CheckResult(
        "ANTHROPIC_API_KEY",
        "warn",
        "Not set — Claude vision provider will not work",
        fix="export ANTHROPIC_API_KEY=sk-ant-... (or use --provider mock for offline)",
    )


def check_openai_key() -> CheckResult:
    if os.environ.get("OPENAI_API_KEY"):
        return CheckResult("OPENAI_API_KEY", "ok", "Set")
    return CheckResult(
        "OPENAI_API_KEY",
        "warn",
        "Not set — OpenAI vision provider will not work",
        fix="Optional. export OPENAI_API_KEY=sk-... if you want to use --provider openai",
    )


def check_flutter_sdk() -> CheckResult:
    flutter = shutil.which("flutter")
    if flutter:
        return CheckResult("Flutter SDK", "ok", f"Found at {flutter}")
    return CheckResult(
        "Flutter SDK",
        "warn",
        "flutter not on PATH — desktop UI cannot be built locally",
        fix="Install Flutter: https://flutter.dev/docs/get-started/install (optional)",
    )
