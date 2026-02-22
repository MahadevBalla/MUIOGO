@echo off
REM ─────────────────────────────────────────────────────────────────────────────
REM MUIOGO Development Environment Setup (Windows)
REM
REM Usage:
REM   scripts\setup.bat          &  full setup
REM   scripts\setup.bat --check  &  verification only
REM ─────────────────────────────────────────────────────────────────────────────
setlocal enabledelayedexpansion

set "SCRIPT_DIR=%~dp0"
set "PROJECT_ROOT=%SCRIPT_DIR%.."

REM Try python3 first, then python
where python3 >nul 2>&1
if %errorlevel% equ 0 (
    set "PYTHON=python3"
    goto :check_version
)

where python >nul 2>&1
if %errorlevel% equ 0 (
    set "PYTHON=python"
    goto :check_version
)

echo ERROR: Python 3.9+ is required but not found in PATH.
echo Install Python from https://www.python.org/downloads/ and try again.
exit /b 1

:check_version
for /f "tokens=*" %%i in ('!PYTHON! -c "import sys; print(sys.version_info >= (3, 9))"') do set "PY_OK=%%i"
if not "!PY_OK!"=="True" (
    echo ERROR: Python 3.9+ is required. Found:
    !PYTHON! --version
    exit /b 1
)

echo Using Python:
!PYTHON! --version

!PYTHON! "%SCRIPT_DIR%setup_dev.py" %*
