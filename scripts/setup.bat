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

REM Prefer specific minor versions first to avoid unsupported interpreters.
where python3.12 >nul 2>&1
if %errorlevel% equ 0 (
    set "PYTHON=python3.12"
    goto :check_version
)

where python3.11 >nul 2>&1
if %errorlevel% equ 0 (
    set "PYTHON=python3.11"
    goto :check_version
)

where python3.10 >nul 2>&1
if %errorlevel% equ 0 (
    set "PYTHON=python3.10"
    goto :check_version
)

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

REM Fall back to Windows Python launcher if direct python commands are unavailable.
where py >nul 2>&1
if %errorlevel% equ 0 (
    py -3.12 -c "import sys" >nul 2>&1
    if %errorlevel% equ 0 (
        set "PYTHON=py -3.12"
        goto :check_version
    )
    py -3.11 -c "import sys" >nul 2>&1
    if %errorlevel% equ 0 (
        set "PYTHON=py -3.11"
        goto :check_version
    )
    py -3.10 -c "import sys" >nul 2>&1
    if %errorlevel% equ 0 (
        set "PYTHON=py -3.10"
        goto :check_version
    )
    set "PYTHON=py"
    goto :check_version
)

echo ERROR: A supported Python interpreter was not found in PATH.
echo MUIOGO setup currently supports Python ^>=3.10 and ^<3.13 (recommended: 3.11).
exit /b 1

:check_version
for /f "tokens=*" %%i in ('!PYTHON! -c "import sys; print((3, 10) <= sys.version_info[:2] < (3, 13))"') do set "PY_OK=%%i"
if not "!PY_OK!"=="True" (
    echo ERROR: Unsupported Python version. Found:
    !PYTHON! --version
    echo MUIOGO setup currently supports Python ^>=3.10 and ^<3.13.
    exit /b 1
)

echo Using Python:
!PYTHON! --version

!PYTHON! "%SCRIPT_DIR%setup_dev.py" %*
