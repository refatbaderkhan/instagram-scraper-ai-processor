import os
import json
import time
import random
from datetime import datetime
from config import TARGET_USERNAMES, OUTPUT_DIR, MAX_DELAY_SECONDS, MIN_DELAY_SECONDS
from instagram_scraper.scraper import InstagramScraper
from instagram_scraper.parser import parse_media_posts

def save_json_file(data, folder, filename_prefix):
    os.makedirs(folder, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    file_path = os.path.join(folder, f"{filename_prefix}_{timestamp}.json")
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    return file_path

def main():
    print("starting scraper...")
    scraper = InstagramScraper()
    
    all_processed_media = []
    all_raw_data = {}

    for i, username in enumerate(TARGET_USERNAMES):
        print(f"scraping profile: {username} ({i + 1}/{len(TARGET_USERNAMES)})")
        raw_user_data = scraper.get_user_profile(username)
        
        if raw_user_data:
            all_raw_data[username] = raw_user_data
            
            processed_posts = parse_media_posts(raw_user_data)
            for post in processed_posts:
                post['source_profile'] = username
            all_processed_media.extend(processed_posts)
            print(f"found {len(processed_posts)} posts for {username}.")
        else:
            print(f"could not retrieve data for {username}.")

        if i < len(TARGET_USERNAMES) - 1:
            delay = random.uniform(MIN_DELAY_SECONDS, MAX_DELAY_SECONDS)
            print(f"---- pausing for {delay:.2f} seconds ----")
            time.sleep(delay)

    scraper.close()

    if all_raw_data:
        raw_path = save_json_file(all_raw_data, OUTPUT_DIR, "raw_posts")
        print(f"successfully saved raw data for {len(all_raw_data)} profiles to '{raw_path}'")

    if all_processed_media:
        filtered_path = save_json_file(all_processed_media, OUTPUT_DIR, "filtered_posts")
        print(f"successfully saved {len(all_processed_media)} total posts to '{filtered_path}'")
    else:
        print("\nno data was scraped. exiting.")

if __name__ == "__main__":
    main()

