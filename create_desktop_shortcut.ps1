$ErrorActionPreference = "Stop"

$projectDir = $PSScriptRoot
$desktop = [Environment]::GetFolderPath("Desktop")
$shortcutPath = Join-Path $desktop "Tomorrow Todo.lnk"

$target = Join-Path $projectDir "start_windows_silent.vbs"
if (-not (Test-Path $target)) {
    Write-Host "File not found: $target"
    exit 1
}

$wsh = New-Object -ComObject WScript.Shell
$shortcut = $wsh.CreateShortcut($shortcutPath)
$shortcut.TargetPath = $target
$shortcut.WorkingDirectory = $projectDir
$shortcut.Description = "Tomorrow Todo"

$iconPath = Join-Path $projectDir "assets\todo.ico"
if (Test-Path $iconPath) {
    $shortcut.IconLocation = $iconPath
} else {
    $exeIcon = Join-Path $projectDir "dist\TomorrowTodo.exe"
    if (Test-Path $exeIcon) {
        $shortcut.IconLocation = $exeIcon
    }
}

$shortcut.Save()
Write-Host "Shortcut created: $shortcutPath"
