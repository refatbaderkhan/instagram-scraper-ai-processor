import logging
from typing import Dict, List

from .extractor import extract_hashtags, extract_text_from_image_url, extract_urls


def transform_post_data(post: Dict) -> Dict:
    photo_urls = post.get("photos", [])

    media_items = []
    for url in photo_urls:
        if not isinstance(url, str):
            continue
        logging.info(f"  - Processing image: {url}...")
        image_text = extract_text_from_image_url(url)

        media_items.append(
            {"url": url, "text": image_text.strip() if image_text else ""}
        )

    post.pop("photos", None)
    post["media"] = media_items
    caption = post.get("caption", "") or ""
    post["hashtags"] = extract_hashtags(caption)
    post["urls"] = extract_urls(caption)

    return post


def transform_all_posts(posts: List[Dict]) -> List[Dict]:
    transformed_posts = []
    for i, post in enumerate(posts):
        logging.info(
            f"Transforming post {i + 1}/{len(posts)} ({post.get('shortcode')})..."
        )
        transformed_post = transform_post_data(post)
        transformed_posts.append(transformed_post)
    return transformed_posts
