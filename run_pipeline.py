
import logging
import subprocess
import sys
import time
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
LOG_FILE = PROJECT_DIR / "pipeline.log"

PIPELINE_STEPS = [
    "quotes_scraper.py",
    "check_author_urls.py",
    "verify_author_urls.py",
    "verify_author_names.py",
    "enrich_quotes.py",
    "validate_quotes.py",
    "data_quality_report.py",
]


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(LOG_FILE, encoding="utf-8"),
        ],
        force=True,
    )


def main():
    setup_logging()
    pipeline_start = time.perf_counter()

    logging.info("=== DATA SCRAPING PIPELINE STARTED ===")

    for index, script in enumerate(PIPELINE_STEPS, start=1):
        script_path = PROJECT_DIR / script

        if not script_path.exists():
            logging.error("Script not found: %s", script)
            return 1

        logging.info(
            "[%s/%s] Starting %s",
            index,
            len(PIPELINE_STEPS),
            script,
        )

        step_start = time.perf_counter()

        try:
            subprocess.run(
                [sys.executable, str(script_path)],
                cwd=PROJECT_DIR,
                check=True,
            )
        except subprocess.CalledProcessError as error:
            elapsed = time.perf_counter() - step_start

            logging.error(
                "%s failed with exit code %s after %.2f seconds",
                script,
                error.returncode,
                elapsed,
            )
            logging.error("Pipeline stopped.")
            return error.returncode or 1

        elapsed = time.perf_counter() - step_start
        logging.info("%s completed in %.2f seconds", script, elapsed)

    total_elapsed = time.perf_counter() - pipeline_start

    logging.info(
        "=== PIPELINE COMPLETED SUCCESSFULLY in %.2f seconds ===",
        total_elapsed,
    )
    logging.info("Log saved to: %s", LOG_FILE)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
