import re
from io import BytesIO
from typing import List

import httpx
import pytesseract
from PIL import Image


def extract_hashtags(text: str) -> List[str]:
    if not isinstance(text, str):
        return []
    return re.findall(r"#(\w+)", text)


def extract_urls(text: str) -> List[str]:
    if not isinstance(text, str):
        return []
    return re.findall(r"https?://\S+", text)


def extract_text_from_image_url(image_url: str) -> str:
    if not image_url:
        return ""
    try:
        response = httpx.get(image_url, timeout=10.0)
        response.raise_for_status()
        image = Image.open(BytesIO(response.content))
        text = pytesseract.image_to_string(image, lang="eng+ara")
        return text.strip()
    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred while fetching image {image_url}: {e}")
        return ""
    except Exception as e:
        print(f"An error occurred during OCR for image {image_url}: {e}")
        return ""
