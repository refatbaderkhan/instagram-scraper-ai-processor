import jmespath
from config import MEDIA_QUERY
from helpers.text_utils import clean_bilingual_text # <-- Import the shared function

def parse_media_posts(raw_user_data: dict) -> list[dict]:

    if not raw_user_data:
        return []

    raw_posts = jmespath.search(MEDIA_QUERY, raw_user_data) or []
    processed_posts = []

    for post in raw_posts:
        processed_post = {
            "shortcode": post.get("shortcode"),
            "display_url": post.get("display_url"),
            "accessibility_full": post.get("accessibility_caption"),
            "accessibility": clean_bilingual_text(post.get("accessibility_caption")),
            "caption_full": post.get("caption"),
            "caption": clean_bilingual_text(post.get("caption")),
            "photos": post.get("photos")
        }
        processed_posts.append(processed_post)

    return processed_posts