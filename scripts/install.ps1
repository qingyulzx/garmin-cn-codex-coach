[CmdletBinding()]
param([string]$PythonExecutable)

$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$runtimePython = Join-Path $projectRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $runtimePython)) {
    $selectedPython = $PythonExecutable
    if ($selectedPython) {
        & $selectedPython -c 'import sys; assert sys.version_info >= (3, 12)'
        if ($LASTEXITCODE -ne 0) { throw 'The selected interpreter must be Python 3.12+.' }
    }
    if (-not $selectedPython -and (Get-Command py -ErrorAction SilentlyContinue)) {
        foreach ($version in @('3.12', '3.13', '3.14')) {
            try { $candidate = & py "-$version" -c 'import sys; print(sys.executable)' 2>$null } catch { continue }
            if ($LASTEXITCODE -eq 0 -and $candidate) { $selectedPython = $candidate.Trim(); break }
        }
    }
    if (-not $selectedPython -and (Get-Command python -ErrorAction SilentlyContinue)) {
        try { $candidate = & python -c 'import sys; assert sys.version_info >= (3, 12); print(sys.executable)' 2>$null } catch { $candidate = $null }
        if ($LASTEXITCODE -eq 0 -and $candidate) { $selectedPython = $candidate.Trim() }
    }
    if (-not $selectedPython) {
        Write-Host 'Python 3.12+ is required. Install from https://www.python.org/downloads/windows/ with Tcl/Tk enabled, then retry.'
        exit 1
    }
    & $selectedPython -m venv (Join-Path $projectRoot '.venv')
    if ($LASTEXITCODE -ne 0) { throw 'Could not create the Python environment.' }
}
& $runtimePython -m pip --disable-pip-version-check install -r (Join-Path $projectRoot 'requirements.txt')
if ($LASTEXITCODE -ne 0) { throw 'Dependency installation failed. Check your network and retry.' }
& $runtimePython -c 'import tkinter, garminconnect, mcp; print("Dependencies ready.")'
if ($LASTEXITCODE -ne 0) { throw 'Python needs Tcl/Tk support for the login window.' }
Write-Host 'Installation complete. Next: double-click 02-login.cmd.'
