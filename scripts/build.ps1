#requires -Version 5.1
$ErrorActionPreference = 'Stop'

$Root      = (Resolve-Path "$PSScriptRoot/..").Path
$BuildType = if ($env:BUILD_TYPE) { $env:BUILD_TYPE } else { 'Release' }

Write-Host "==> Building native core ($BuildType)" -ForegroundColor Cyan
cmake -S "$Root\native" -B "$Root\native\build" -G Ninja -DCMAKE_BUILD_TYPE=$BuildType
cmake --build "$Root\native\build" --parallel

Write-Host "==> Installing Python package (editable)" -ForegroundColor Cyan
Set-Location "$Root\python"
if (-not (Test-Path '.venv')) {
    python -m venv .venv
}
& '.\.venv\Scripts\Activate.ps1'
python -m pip install --upgrade pip
pip install -e ".[dev]"

Write-Host "==> Fetching Flutter packages" -ForegroundColor Cyan
Set-Location "$Root\ui"
flutter pub get

Write-Host "==> Done. To run:" -ForegroundColor Green
Write-Host "   mimic --help"
Write-Host "   cd $Root\ui ; flutter run -d windows"
