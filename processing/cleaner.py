import re

def clean_bilingual_text(text: str) -> str:
    if not isinstance(text, str):
        return ""

    english_lines = []
    arabic_lines = []

    arabic_pattern = re.compile(r'[\u0600-\u06FF]')

    for line in text.splitlines():
        if arabic_pattern.search(line):
            arabic_lines.append(line)
        else:
            english_lines.append(line)

    english_result = "\n".join(english_lines).strip()
    arabic_result = "\n".join(arabic_lines).strip()

    return english_result if english_result else arabic_result

# def remove_hashtags(text: str) -> str:
#     return re.sub(r'#\w+', '', text).strip()

# def remove_urls(text: str) -> str:
#     return re.sub(r'https?://\S+', '', text).strip()

# def clean_text(text: str) -> str:
#     text = remove_urls(text)
#     text = remove_hashtags(text)
#     return text