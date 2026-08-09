"""
Run all Yahoo Finance → MySQL ETL loaders in sequence.

Usage:
    python3 main.py
"""

import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent

# Order matters: master data first, then everything that reads from companies.
LOADERS = [
    "companies_load.py",
    "load_daily_prices.py",
    "load_intraday_prices.py",
    "load_fundamentals.py",
    "load_income_statements.py",
    "load_balance_sheet.py",
    "load_cash_flow.py",
    "load_corporate_actions.py",
]


def run_loader(script_name: str) -> None:
    script_path = SCRIPT_DIR / script_name
    print("\n" + "=" * 60)
    print(f"Running {script_name}")
    print("=" * 60 + "\n")

    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=SCRIPT_DIR,
    )

    if result.returncode != 0:
        raise SystemExit(f"{script_name} failed with exit code {result.returncode}")


def main() -> None:
    print("Starting full data load pipeline...")
    print(f"Python: {sys.executable}")
    print(f"Scripts: {len(LOADERS)}")

    for script_name in LOADERS:
        run_loader(script_name)

    print("\n" + "=" * 60)
    print("All loaders completed successfully.")
    print("=" * 60)


if __name__ == "__main__":
    main()
