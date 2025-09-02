from datetime import datetime

import jmespath

from ..config import MEDIA_QUERY


def parse_media_posts(raw_user_data: dict, username: str) -> list[dict]:
    if not raw_user_data:
        return []

    raw_posts = jmespath.search(MEDIA_QUERY, raw_user_data) or []
    processed_posts = []

    for post in raw_posts:
        timestamp = post.get("taken_at_timestamp", 0)
        readable_date = (
            datetime.fromtimestamp(timestamp).isoformat() if timestamp else None
        )

        photos = []
        if post.get("photos") and post["photos"].get("edges"):
            for edge in post["photos"]["edges"]:
                if edge.get("node") and edge["node"].get("display_url"):
                    photos.append(edge["node"]["display_url"])
        elif post.get("display_url"):
            photos.append(post.get("display_url"))

        processed_post = {
            "source": username,
            "shortcode": post.get("shortcode"),
            "post_url": f"https://www.instagram.com/p/{post.get('shortcode')}/",
            "display_url": post.get("display_url"),
            "post_date": readable_date,
            "timestamp": timestamp,
            "caption": post.get("caption"),
            "photos": photos,
        }
        processed_posts.append(processed_post)

    return processed_posts
