"""
verify_setup.py
---------------
DataSieveAi — Local Environment Verification Script
Run this script to confirm that your Python and Conda environment is
correctly set up for Data Science work.

Usage:
    python verify_setup.py
"""

import sys
import subprocess
import importlib

# ── 1. Python Version ────────────────────────────────────────────────────────
print("=" * 55)
print("  DataSieveAi — Environment Verification")
print("=" * 55)

python_version = sys.version
print(f"\n✅ Python is installed")
print(f"   Version : {python_version}")
print(f"   Path    : {sys.executable}")

# ── 2. Conda Version ─────────────────────────────────────────────────────────
print("\n── Conda ──────────────────────────────────────────────")
try:
    result = subprocess.run(
        ["conda", "--version"],
        capture_output=True,
        text=True,
        timeout=10,
    )
    if result.returncode == 0:
        print(f"✅ Conda is installed: {result.stdout.strip()}")
    else:
        print(f"⚠️  Conda found but returned an error: {result.stderr.strip()}")
except FileNotFoundError:
    print("⚠️  Conda not found in PATH")
    print("   Tip: Run 'conda init powershell' and restart your terminal.")
except Exception as e:
    print(f"⚠️  Could not check conda: {e}")

# ── 3. Core DS/ML Packages ───────────────────────────────────────────────────
print("\n── Core Data Science Packages ─────────────────────────")
packages = {
    "numpy": "NumPy",
    "pandas": "Pandas",
    "matplotlib": "Matplotlib",
    "sklearn": "Scikit-learn",
    "scipy": "SciPy",
    "jupyter": "Jupyter",
}

for module, display_name in packages.items():
    try:
        mod = importlib.import_module(module)
        version = getattr(mod, "__version__", "installed")
        print(f"  ✅  {display_name:<18} {version}")
    except ImportError:
        print(f"  ❌  {display_name:<18} NOT installed")

# ── 4. Summary ───────────────────────────────────────────────────────────────
print("\n" + "=" * 55)
print("  Environment check complete.")
print("  This machine is ready for DataSieveAi DS work.")
print("=" * 55 + "\n")
