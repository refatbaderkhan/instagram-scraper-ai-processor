import argparse
import logging
import sys
from pathlib import Path

if __name__ == "__main__":
    project_root = Path(__file__).parent.parent
    sys.path.insert(0, str(project_root))

from logging_config import setup_logging

from .core.pipeline import run_pipeline


def main():
    setup_logging()
    setup_logging()

    parser = argparse.ArgumentParser(description="Scrape and process Instagram posts.")
    parser.add_argument(
        "--offline",
        action="store_true",
        help="Run the script in offline mode using a local raw data file.",
    )
    parser.add_argument(
        "--input-file",
        type=str,
        default="data/raw_posts.json",
        help="Path to the raw JSON file to use in offline mode.",
    )

    args = parser.parse_args()

    try:
        run_pipeline(args)
    except Exception as e:
        logging.critical(f"A critical error occurred: {e}", exc_info=True)


if __name__ == "__main__":
    main()
