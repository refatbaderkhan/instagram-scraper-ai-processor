import jmespath
from datetime import datetime
from config import MEDIA_QUERY

def parse_media_posts(raw_user_data: dict) -> list[dict]:
    if not raw_user_data:
        return []

    raw_posts = jmespath.search(MEDIA_QUERY, raw_user_data) or []
    processed_posts = []

    for post in raw_posts:

        timestamp = post.get("taken_at_timestamp", 0)
        readable_date = datetime.fromtimestamp(timestamp).isoformat() if timestamp else None

        photos = post.get("photos") or []
        if isinstance(photos, list):
            photos = [p for p in photos if p]

        processed_post = {
            "shortcode": post.get("shortcode"),
            "post_url": f"https://www.instagram.com/p/{post.get('shortcode')}/",
            "display_url": post.get("display_url"),
            "post_date": readable_date,
            "timestamp": timestamp,
            "caption": post.get("caption"),
            "photos": post.get("photos")
        }
        processed_posts.append(processed_post)

    return processed_posts

