import logging
from typing import Dict, List

from .extractor import extract_hashtags, extract_text_from_image_url, extract_urls


def transform_post_data(post: Dict) -> Dict:
    image_urls_to_process = [post.get("display_url")]
    if post.get("photos"):
        image_urls_to_process.extend(post["photos"])

    unique_image_urls = sorted(list(set(filter(None, image_urls_to_process))))

    combined_image_text = []
    for url in unique_image_urls:
        image_text = extract_text_from_image_url(url)
        if image_text:
            combined_image_text.append(image_text)

    post["image_text"] = "\\n---\\n".join(combined_image_text)

    caption = post.get("caption", "") or ""
    post["hashtags"] = extract_hashtags(caption)
    post["urls"] = extract_urls(caption)

    return post


def transform_all_posts(posts: List[Dict]) -> List[Dict]:
    transformed_posts = []
    for i, post in enumerate(posts):
        logging.info(
            f"Enriching post {i + 1}/{len(posts)} ({post.get('shortcode')})..."
        )
        transformed_post = transform_post_data(post)
        transformed_posts.append(transformed_post)
    return transformed_posts
