
import subprocess
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent

PIPELINE_STEPS = [
    "quotes_scraper.py",
    "check_author_urls.py",
    "verify_author_urls.py",
    "verify_author_names.py",
    "enrich_quotes.py",
    "validate_quotes.py",
    "data_quality_report.py",
]


def main():
    print("=== DATA SCRAPING PIPELINE ===")

    for index, script in enumerate(PIPELINE_STEPS, start=1):
        script_path = PROJECT_DIR / script

        if not script_path.exists():
            print(f"\nERROR: Script not found: {script}")
            return 1

        print(f"\n[{index}/{len(PIPELINE_STEPS)}] Running {script}")

        try:
            subprocess.run(
                [sys.executable, str(script_path)],
                cwd=PROJECT_DIR,
                check=True,
            )
        except subprocess.CalledProcessError as error:
            print(
                f"\nPIPELINE FAILED: {script} "
                f"exited with code {error.returncode}"
            )
            return error.returncode or 1

    print("\n=== PIPELINE COMPLETED SUCCESSFULLY ===")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
