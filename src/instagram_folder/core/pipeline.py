import logging
import random
import time

from processing.transformer import transform_all_posts
from scraper.parser import parse_media_posts
from scraper.scraper import InstagramScraper
from src.instagram_scraper.config import (
    MAX_DELAY_SECONDS,
    MIN_DELAY_SECONDS,
    TARGET_USERNAMES,
)

from .file_handler import load_json_file, save_json_file


def run_pipeline(args):
    all_raw_data = {}

    if args.offline:
        logging.info("--- Running in OFFLINE mode ---")
        logging.info(f"Loading data from {args.input_file}")
        all_raw_data = load_json_file(args.input_file)

    else:
        logging.info("--- Running in ONLINE mode ---")
        scraper = InstagramScraper()
        for i, username in enumerate(TARGET_USERNAMES):
            logging.info(
                f"Scraping profile: {username} ({i + 1}/{len(TARGET_USERNAMES)})"
            )
            raw_user_data = scraper.get_user_profile(username)
            if raw_user_data:
                all_raw_data[username] = raw_user_data
            else:
                logging.warning(f"Could not retrieve data for {username}.")

            if i < len(TARGET_USERNAMES) - 1:
                delay = random.uniform(MIN_DELAY_SECONDS, MAX_DELAY_SECONDS)
                logging.info(f"---- Pausing for {delay:.2f} seconds ----")
                time.sleep(delay)
        scraper.close()
        save_json_file(all_raw_data, "raw_posts")

    if not all_raw_data:
        logging.warning("No raw data available to process. Exiting.")
        return

    all_parsed_posts = []
    for username, raw_user_data in all_raw_data.items():
        logging.info(f"Parsing posts for {username}...")
        parsed_posts = parse_media_posts(raw_user_data)
        for post in parsed_posts:
            post["source_profile"] = username
        all_parsed_posts.extend(parsed_posts)

    logging.info(f"Starting enrichment for {len(all_parsed_posts)} posts...")
    all_enriched_posts = transform_all_posts(all_parsed_posts)

    if all_enriched_posts:
        save_json_file(all_enriched_posts, "filtered_posts")

    logging.info("Pipeline finished.")
