import re
from typing import List

def extract_hashtags(text: str) -> List[str]:
    if not isinstance(text, str):
        return []
    return re.findall(r'#(\w+)', text)

def extract_urls(text: str) -> List[str]:
    if not isinstance(text, str):
        return []
    return re.findall(r'https?://\S+', text)