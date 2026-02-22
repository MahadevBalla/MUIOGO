#!/usr/bin/env python3
"""
MUIOGO Cross-Platform Development Setup Script

Sets up a complete development environment for MUIOGO:
  1. Creates or validates a Python virtual environment (venv)
  2. Installs Python dependencies from requirements.txt
  3. Installs solver dependencies (GLPK, CBC) via OS package managers
  4. Runs post-setup verification checks

Usage:
    python scripts/setup_dev.py          # full setup
    python scripts/setup_dev.py --check  # verification only (skip install)

Supports: macOS, Linux (apt/dnf/pacman), Windows
"""

import argparse
import os
import platform
import shutil
import subprocess
import sys
import textwrap
import venv
from pathlib import Path

# ──────────────────────────────────────────────────────────────────────────────
# Constants
# ──────────────────────────────────────────────────────────────────────────────

PROJECT_ROOT = Path(__file__).resolve().parent.parent
VENV_DIR = PROJECT_ROOT / "venv"
REQUIREMENTS = PROJECT_ROOT / "requirements.txt"
SYSTEM = platform.system()  # 'Darwin', 'Linux', 'Windows'

# Core packages that must be importable after setup
REQUIRED_IMPORTS = [
    "flask",
    "flask_cors",
    "pandas",
    "numpy",
    "openpyxl",
    "waitress",
    "dotenv",
]

# ──────────────────────────────────────────────────────────────────────────────
# Utilities
# ──────────────────────────────────────────────────────────────────────────────

BOLD = "\033[1m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

# Disable colours when not in a real terminal (CI, pipes, Windows without ANSI)
if not sys.stdout.isatty():
    BOLD = GREEN = YELLOW = RED = RESET = ""


def _print_header(msg: str) -> None:
    print(f"\n{BOLD}{'=' * 60}")
    print(f"  {msg}")
    print(f"{'=' * 60}{RESET}\n")


def _print_pass(label: str, detail: str = "") -> None:
    suffix = f"  ({detail})" if detail else ""
    print(f"  {GREEN}[PASS]{RESET} {label}{suffix}")


def _print_fail(label: str, detail: str = "") -> None:
    suffix = f"  ({detail})" if detail else ""
    print(f"  {RED}[FAIL]{RESET} {label}{suffix}")


def _print_warn(label: str, detail: str = "") -> None:
    suffix = f"  ({detail})" if detail else ""
    print(f"  {YELLOW}[WARN]{RESET} {label}{suffix}")


def _run(cmd: list[str], **kwargs) -> subprocess.CompletedProcess:
    """Run a command, printing it first, and return the result."""
    print(f"  $ {' '.join(cmd)}")
    return subprocess.run(cmd, **kwargs)


def _which(name: str) -> str | None:
    """Cross-platform shutil.which wrapper."""
    return shutil.which(name)


# ──────────────────────────────────────────────────────────────────────────────
# Step 1 – Python virtual environment
# ──────────────────────────────────────────────────────────────────────────────

def _venv_python() -> Path:
    """Return the path to the venv Python interpreter."""
    if SYSTEM == "Windows":
        return VENV_DIR / "Scripts" / "python.exe"
    return VENV_DIR / "bin" / "python"


def _venv_pip() -> Path:
    if SYSTEM == "Windows":
        return VENV_DIR / "Scripts" / "pip.exe"
    return VENV_DIR / "bin" / "pip"


def setup_venv() -> bool:
    """Create a Python venv if one does not already exist."""
    _print_header("Step 1: Python virtual environment")

    if _venv_python().exists():
        print(f"  Virtual environment already exists at {VENV_DIR}")
        return True

    print(f"  Creating virtual environment at {VENV_DIR} ...")
    try:
        venv.create(str(VENV_DIR), with_pip=True)
        print(f"  {GREEN}Virtual environment created.{RESET}")
        return True
    except Exception as exc:
        _print_fail("Could not create venv", str(exc))
        return False


# ──────────────────────────────────────────────────────────────────────────────
# Step 2 – Python dependencies
# ──────────────────────────────────────────────────────────────────────────────

def install_python_deps() -> bool:
    """Install Python dependencies from requirements.txt into the venv."""
    _print_header("Step 2: Python dependencies")

    if not REQUIREMENTS.exists():
        _print_fail("requirements.txt not found", str(REQUIREMENTS))
        return False

    pip = str(_venv_pip())
    python = str(_venv_python())

    # Upgrade pip first
    _run([python, "-m", "pip", "install", "--upgrade", "pip"],
         capture_output=True)

    result = _run(
        [pip, "install", "-r", str(REQUIREMENTS)],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        _print_fail("pip install failed")
        print(result.stderr[-2000:] if result.stderr else "(no stderr)")
        return False

    print(f"  {GREEN}Python dependencies installed.{RESET}")
    return True


# ──────────────────────────────────────────────────────────────────────────────
# Step 3 – Solver dependencies (GLPK & CBC)
# ──────────────────────────────────────────────────────────────────────────────

def _detect_linux_pkg_manager() -> tuple[str, list[str], list[str]] | None:
    """
    Detect the Linux package manager and return
    (manager_name, glpk_install_cmd, cbc_install_cmd) or None.
    """
    if _which("apt-get"):
        return (
            "apt",
            ["sudo", "apt-get", "install", "-y", "glpk-utils"],
            ["sudo", "apt-get", "install", "-y", "coinor-cbc"],
        )
    if _which("dnf"):
        return (
            "dnf",
            ["sudo", "dnf", "install", "-y", "glpk-utils"],
            ["sudo", "dnf", "install", "-y", "coin-or-Cbc"],
        )
    if _which("pacman"):
        return (
            "pacman",
            ["sudo", "pacman", "-S", "--noconfirm", "glpk"],
            ["sudo", "pacman", "-S", "--noconfirm", "coin-or-cbc"],
        )
    return None


def install_solvers() -> bool:
    """Install GLPK and CBC solver binaries using OS package managers."""
    _print_header("Step 3: Solver dependencies (GLPK & CBC)")

    glpk_ok = _which("glpsol") is not None
    cbc_ok = _which("cbc") is not None

    if glpk_ok and cbc_ok:
        print("  Both solvers already installed — skipping.")
        return True

    success = True

    # ── macOS (Homebrew) ──────────────────────────────────────────────────
    if SYSTEM == "Darwin":
        if not _which("brew"):
            _print_fail(
                "Homebrew not found",
                "Install from https://brew.sh then re-run this script.",
            )
            return False

        if not glpk_ok:
            r = _run(["brew", "install", "glpk"], capture_output=True, text=True)
            if r.returncode != 0:
                _print_fail("brew install glpk", r.stderr.strip())
                success = False

        if not cbc_ok:
            r = _run(["brew", "install", "cbc"], capture_output=True, text=True)
            if r.returncode != 0:
                _print_fail("brew install cbc", r.stderr.strip())
                success = False

    # ── Linux ─────────────────────────────────────────────────────────────
    elif SYSTEM == "Linux":
        pkg = _detect_linux_pkg_manager()
        if pkg is None:
            _print_fail(
                "No supported package manager found (apt, dnf, pacman)",
                "Install GLPK and CBC manually, then re-run with --check.",
            )
            return False

        mgr_name, glpk_cmd, cbc_cmd = pkg
        print(f"  Detected package manager: {mgr_name}")

        if not glpk_ok:
            r = _run(glpk_cmd, capture_output=True, text=True)
            if r.returncode != 0:
                _print_fail(" ".join(glpk_cmd), r.stderr.strip())
                success = False

        if not cbc_ok:
            r = _run(cbc_cmd, capture_output=True, text=True)
            if r.returncode != 0:
                _print_fail(" ".join(cbc_cmd), r.stderr.strip())
                success = False

    # ── Windows ───────────────────────────────────────────────────────────
    elif SYSTEM == "Windows":
        if _which("choco"):
            if not glpk_ok:
                r = _run(["choco", "install", "glpk", "-y"],
                         capture_output=True, text=True)
                if r.returncode != 0:
                    _print_fail("choco install glpk", r.stderr.strip())
                    success = False

            if not cbc_ok:
                r = _run(["choco", "install", "coinor-cbc", "-y"],
                         capture_output=True, text=True)
                if r.returncode != 0:
                    _print_fail("choco install coinor-cbc", r.stderr.strip())
                    success = False

        elif _which("winget"):
            _print_warn(
                "winget detected but GLPK/CBC may not be in winget repos",
                "Falling back to manual install instructions.",
            )
            success = False
        else:
            _print_fail(
                "No supported package manager (choco) found on Windows",
                "Install Chocolatey (https://chocolatey.org/) or install GLPK and CBC manually.",
            )
            success = False

    if success:
        print(f"  {GREEN}Solver dependencies installed.{RESET}")
    else:
        _print_warn("Some solvers could not be installed automatically.")
        _print_solver_manual_instructions()

    return success


def _print_solver_manual_instructions() -> None:
    """Print manual installation instructions for solvers."""
    print(textwrap.dedent(f"""
    {YELLOW}Manual solver installation:{RESET}

    GLPK:
      macOS:   brew install glpk
      Ubuntu:  sudo apt-get install -y glpk-utils
      Fedora:  sudo dnf install -y glpk-utils
      Arch:    sudo pacman -S glpk
      Windows: choco install glpk
               or download from https://www.gnu.org/software/glpk/

    CBC (COIN-OR):
      macOS:   brew install cbc
      Ubuntu:  sudo apt-get install -y coinor-cbc
      Fedora:  sudo dnf install -y coin-or-Cbc
      Arch:    sudo pacman -S coin-or-cbc
      Windows: choco install coinor-cbc
               or download from https://github.com/coin-or/Cbc/releases
    """))


# ──────────────────────────────────────────────────────────────────────────────
# Step 4 – Post-setup verification
# ──────────────────────────────────────────────────────────────────────────────

def run_checks() -> bool:
    """Run all verification checks and return True if everything passes."""
    _print_header("Step 4: Verification checks")

    all_ok = True
    python = str(_venv_python())

    # 4a – venv Python exists
    if _venv_python().exists():
        _print_pass("Python venv exists", str(_venv_python()))
    else:
        _print_fail("Python venv not found", str(_venv_python()))
        all_ok = False

    # 4b – Key Python packages importable
    print()
    print("  Checking Python imports:")
    for pkg in REQUIRED_IMPORTS:
        result = subprocess.run(
            [python, "-c", f"import {pkg}"],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            _print_pass(f"import {pkg}")
        else:
            _print_fail(f"import {pkg}", result.stderr.strip().split("\n")[-1])
            all_ok = False

    # 4c – Solver binaries
    print()
    print("  Checking solver binaries:")

    # GLPK: glpsol --version works normally
    glpsol_path = _which("glpsol")
    if glpsol_path:
        r = subprocess.run(
            ["glpsol", "--version"],
            capture_output=True,
            text=True,
        )
        version_line = (r.stdout or r.stderr or "").strip().split("\n")[0]
        _print_pass("GLPK (glpsol)", version_line)
    else:
        _print_fail("GLPK (glpsol)", "'glpsol' not found in PATH")
        all_ok = False

    # CBC: `cbc --version` opens an interactive prompt, so pipe "quit" instead
    cbc_path = _which("cbc")
    if cbc_path:
        r = subprocess.run(
            ["cbc"],
            input="quit\n",
            capture_output=True,
            text=True,
            timeout=10,
        )
        # The first line is "Welcome to the CBC MILP Solver", version on line 2
        lines = (r.stdout or "").strip().split("\n")
        version_info = lines[1].strip() if len(lines) > 1 else lines[0].strip()
        _print_pass("CBC", version_info)
    else:
        _print_fail("CBC", "'cbc' not found in PATH")
        all_ok = False

    # 4d – Basic app startup check (import the Flask app module)
    print()
    print("  Checking app startup:")
    startup_check = subprocess.run(
        [
            python, "-c",
            (
                "import sys, os; "
                f"os.chdir({str(PROJECT_ROOT)!r}); "
                "sys.path.insert(0, 'API'); "
                "from flask import Flask; "
                "print('Flask app module loadable')"
            ),
        ],
        capture_output=True,
        text=True,
        cwd=str(PROJECT_ROOT),
    )
    if startup_check.returncode == 0:
        _print_pass("Flask app module loads without error")
    else:
        err = startup_check.stderr.strip().split("\n")[-1] if startup_check.stderr else "unknown"
        _print_fail("Flask app module failed to load", err)
        all_ok = False

    return all_ok


# ──────────────────────────────────────────────────────────────────────────────
# Summary and next steps
# ──────────────────────────────────────────────────────────────────────────────

def _print_summary(results: dict[str, bool]) -> None:
    """Print a final summary table and actionable next steps."""
    _print_header("Setup Summary")

    all_ok = all(results.values())

    for step, passed in results.items():
        if passed:
            _print_pass(step)
        else:
            _print_fail(step)

    print()

    if all_ok:
        activate_cmd = (
            r"venv\Scripts\activate" if SYSTEM == "Windows"
            else "source venv/bin/activate"
        )
        print(textwrap.dedent(f"""\
        {GREEN}{BOLD}All checks passed! Your MUIOGO environment is ready.{RESET}

        Next steps:
          1. Activate the virtual environment:
               {activate_cmd}
          2. Start the app:
               cd API && python app.py
          3. Open http://127.0.0.1:5002 in your browser.
        """))
    else:
        print(textwrap.dedent(f"""\
        {RED}{BOLD}Some checks failed.{RESET}

        Next steps:
          - Review the [FAIL] items above.
          - Fix the issues and re-run:
               python scripts/setup_dev.py --check
          - If solver install failed, see manual instructions above or run:
               python scripts/setup_dev.py
            after installing the solvers manually.
          - For help, see CONTRIBUTING.md or open an issue.
        """))


# ──────────────────────────────────────────────────────────────────────────────
# Main entry point
# ──────────────────────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(
        description="MUIOGO cross-platform development environment setup",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Run verification checks only (skip install steps)",
    )
    args = parser.parse_args()

    print(f"\n{BOLD}MUIOGO Development Environment Setup{RESET}")
    print(f"  Platform : {SYSTEM} ({platform.machine()})")
    print(f"  Python   : {sys.version.split()[0]}")
    print(f"  Project  : {PROJECT_ROOT}")

    if args.check:
        ok = run_checks()
        return 0 if ok else 1

    results: dict[str, bool] = {}

    results["Python virtual environment"] = setup_venv()

    if results["Python virtual environment"]:
        results["Python dependencies"] = install_python_deps()
    else:
        results["Python dependencies"] = False
        _print_fail("Skipping Python deps (venv setup failed)")

    results["Solver dependencies (GLPK & CBC)"] = install_solvers()

    results["Verification checks"] = run_checks()

    _print_summary(results)

    return 0 if all(results.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
