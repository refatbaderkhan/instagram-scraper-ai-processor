import json
import httpx
import jmespath
from helpers.single_encoding_extractor import single_encoding_extractor

client = httpx.Client(
    headers={
        "x-ig-app-id": "936619743392459",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9,ru;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept": "*/*",
    }
)

def scrape_user(username: str):
    try:
        result = client.get(
            f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}",
        )
        result.raise_for_status()
        data = result.json()
        return data["data"]["user"]
    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred: {e}")
        return None
    except KeyError:
        print("Could not find 'user' data in the response.")
        return None

user_data = scrape_user("zawyacinema")

if user_data:
    # JMESPath query to get the raw post data
    query = (
        'edge_owner_to_timeline_media.edges[].node.'
        '{shortcode: shortcode, '
        'display_url: display_url, '
        'accessibility_caption: accessibility_caption, '
        'caption: edge_media_to_caption.edges[0].node.text,'
        'photos: edge_sidecar_to_children.edges[].node.display_url}'
    )

    parsed_media = jmespath.search(query, user_data)
    media = jmespath.search(query, user_data)
    processed_media = []

    if parsed_media:
        for post in parsed_media:
            acc_caption = post.get("accessibility_caption") or ""
            main_caption = post.get("caption") or ""

            # --- Using the new trimmer ---
            # Remove Arabic from the accessibility caption
            acc_caption = single_encoding_extractor(acc_caption)

            # Separate the main caption into English and Arabic
            caption = single_encoding_extractor(main_caption)

            # Create the new, structured dictionary
            processed_post = {
                "shortcode": post.get("shortcode"),
                "display_url": post.get("display_url"),
                "accessibility_full": post.get("accessibility_caption"),
                "accessibility": acc_caption,
                "caption_full": post.get("caption"),
                "caption": caption,
                "photos": post.get("photos")
            }
            processed_media.append(processed_post)

    # Save the file with UTF-8 encoding
    with open("zawyacinema_media_final.json", "w", encoding="utf-8") as f:
        json.dump(processed_media, f, indent=4, ensure_ascii=False)
    
    print("✅ Successfully processed and saved data to 'zawyacinema_media_final.json'")

else:
    print("No user data found.")

