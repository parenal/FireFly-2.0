# PowerShell script to build a single-file Windows executable using PyInstaller
# Usage (from project root, with venv activated):
#   ./scripts/build_windows_exe.ps1

param(
    [string]$Name = "FireFly",
    [string]$Entry = "run_gui.py",
    [switch]$NoConsole
)

Write-Host "Building executable: $Name from $Entry"

# Ensure PyInstaller is installed in the active environment
# Prefer using the project's virtualenv Python if present so we run/install in the right env
$projectRoot = Split-Path -Parent $PSScriptRoot
$venvPython = Join-Path $projectRoot "venv\Scripts\python.exe"
if (Test-Path $venvPython) {
    Write-Host "Using venv python: $venvPython"
    & $venvPython -m pip install --upgrade pip
    & $venvPython -m pip install pyinstaller
} else {
    try {
        pyinstaller --version > $null 2>&1
    } catch {
        Write-Host "PyInstaller not found. Installing system-wide (may require privileges)..."
        python -m pip install --user pyinstaller
    }
}

# Prepare add-data arguments for bundling the data folder (Windows path separator is ';')
$addData = "data;data"

$consoleFlag = ''
if ($NoConsole) {
    $consoleFlag = '--noconsole'
}

# Run PyInstaller
$hiddenImports = @(
    'passlib',
    'passlib.handlers.argon2',
    'passlib.utils',
    'passlib.handlers.pbkdf2',
    'passlib.handlers.bcrypt',
    'argon2',
    'argon2.low_level'
)

$hiddenArgs = $hiddenImports | ForEach-Object { "--hidden-import `"$_`"" } | Out-String
$hiddenArgs = $hiddenArgs -replace "\r\n", " "

$cmd = "--onefile $consoleFlag --name $Name --add-data `"$addData`" $hiddenArgs $Entry"
if (Test-Path $venvPython) {
    $run = "& `"$venvPython`" -m PyInstaller $cmd"
    Write-Host "Running (venv): $run"
    Invoke-Expression $run
} else {
    $run = "pyinstaller $cmd"
    Write-Host "Running: $run"
    Invoke-Expression $run
}

if ($LASTEXITCODE -ne 0) {
    Write-Host "Build failed (exit code $LASTEXITCODE)" -ForegroundColor Red
    exit $LASTEXITCODE
}

Write-Host "Build finished. The executable is in the 'dist' folder." -ForegroundColor Green
