import os
import json
import time
import random
import logging
import argparse
from datetime import datetime
from config import TARGET_USERNAMES, OUTPUT_DIR, MAX_DELAY_SECONDS, MIN_DELAY_SECONDS
from instagram_scraper.scraper import InstagramScraper
from instagram_scraper.parser import parse_media_posts
from processing.image_processor import extract_text_from_image_url
from processing.extractor import extract_hashtags, extract_urls
from logging_config import setup_logging

def save_json_file(data, folder, filename_prefix):
    os.makedirs(folder, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    file_path = os.path.join(folder, f"{filename_prefix}_{timestamp}.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    return file_path

def load_json_file(file_path: str) -> dict:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error(f"Error: The file '{file_path}' was not found.")
        return None
    except json.JSONDecodeError:
        logging.error(f"Error: Could not decode JSON from the file '{file_path}'.")
        return None
    
def process_posts(all_raw_data: dict) -> list:
    all_processed_media = []
    for username, raw_user_data in all_raw_data.items():
        logging.info(f"Processing posts for {username}...")
        processed_posts = parse_media_posts(raw_user_data)
        for post in processed_posts:
            post['source_profile'] = username
            
            image_urls_to_process = [post.get('display_url')]
            if post.get('photos'):
                image_urls_to_process.extend(post['photos'])
            
            unique_image_urls = sorted(list(set(filter(None, image_urls_to_process))))

            combined_image_text = []
            for url in unique_image_urls:
                image_text = extract_text_from_image_url(url)
                if image_text:
                    combined_image_text.append(image_text)
            
            post['image_text'] = "\n---\n".join(combined_image_text)

            caption = post.get('caption', '') or ''
            post['hashtags'] = extract_hashtags(caption)
            post['urls'] = extract_urls(caption)

        all_processed_media.extend(processed_posts)
        logging.info(f"Processed {len(processed_posts)} posts for {username}.")
    return all_processed_media



def main(args):
    setup_logging()
    all_raw_data = {}

    if args.offline:
        logging.info(f"--- Running in OFFLINE mode ---")
        logging.info(f"Loading data from {args.input_file}")
        all_raw_data = load_json_file(args.input_file)
        if not all_raw_data:
            return 
    else:
        logging.info("--- Running in ONLINE mode ---")
        scraper = InstagramScraper()
        for i, username in enumerate(TARGET_USERNAMES):
            logging.info(f"Scraping profile: {username} ({i + 1}/{len(TARGET_USERNAMES)})")
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
        
        if all_raw_data:
            raw_path = save_json_file(all_raw_data, OUTPUT_DIR, "raw_posts")
            logging.info(f"Successfully saved raw data for {len(all_raw_data)} profiles to '{raw_path}'")

    if not all_raw_data:
        logging.warning("No raw data available to process. Exiting.")
        return

    all_processed_media = process_posts(all_raw_data)

    if all_processed_media:
        filtered_path = save_json_file(all_processed_media, OUTPUT_DIR, "filtered_posts")
        logging.info(f"Successfully saved processed data for {len(all_processed_media)} posts to '{filtered_path}'")

    logging.info("Script finished.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape and process Instagram posts.")
    parser.add_argument(
        '--offline',
        action='store_true',
        help='Run the script in offline mode using a local raw data file.'
    )
    parser.add_argument(
        '--input-file',
        type=str,
        default='data/raw_posts_20250901_173640.json',
        help='Path to the raw JSON file to use in offline mode.'
    )
    args = parser.parse_args()
    main(args)