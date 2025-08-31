import os
import json
from config import TARGET_USERNAMES, OUTPUT_DIR
from instagram_scraper.scraper import InstagramScraper
from instagram_scraper.parser import parse_media_posts
from datetime import datetime


def main():
    print("starting scraper...")
    scraper = InstagramScraper()
    
    all_processed_media = []

    for username in TARGET_USERNAMES:
        print(f"scraping profile: {username}")
        raw_user_data = scraper.get_user_profile(username)
        
        if raw_user_data:
            processed_posts = parse_media_posts(raw_user_data)
            all_processed_media.extend(processed_posts)
            print(f"found {len(processed_posts)} posts for {username}.")
        else:
            print(f"could not retrieve data for {username}.")

    scraper.close()

    if all_processed_media:
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        file_path = os.path.join(OUTPUT_DIR, f"instagram_posts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(all_processed_media, f, indent=4, ensure_ascii=False)
            
        print(f"successfully saved {len(all_processed_media)} total posts to '{file_path}'")
    else:
        print("\nno data was scraped. Exiting.")

if __name__ == "__main__":
    main()