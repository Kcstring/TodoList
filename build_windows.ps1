$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

python -m pip install -r requirements.txt

$iconPath = Join-Path $PSScriptRoot "assets\todo.ico"
if (Test-Path $iconPath) {
    python -m PyInstaller --noconfirm --windowed --onefile --name "TomorrowTodo" --icon "$iconPath" main.py
} else {
    python -m PyInstaller --noconfirm --windowed --onefile --name "TomorrowTodo" main.py
}

Write-Host "Build complete: $PSScriptRoot\dist\TomorrowTodo.exe"
