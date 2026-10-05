@echo off
chcp 65001 >nul
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
    echo Please run 01-install.cmd first.
    pause
    exit /b 1
)
".venv\Scripts\python.exe" -B "scripts\check_mcp.py"
pause
