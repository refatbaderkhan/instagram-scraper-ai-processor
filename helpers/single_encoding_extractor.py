import re

def single_encoding_extractor(text: str) -> str:
    """
    Extracts the English part of a caption if available, otherwise returns the Arabic part.

    Args:
        text: The input string which may contain both English and Arabic text.

    Returns:
        The English part of the caption, or the Arabic part if no English is found.
    """
    if not isinstance(text, str):
        return ""

    english_lines = []
    arabic_lines = []
    
    # This regex pattern detects if a string contains any Arabic characters.
    arabic_pattern = re.compile(r'[\u0600-\u06FF]')

    for line in text.split(' '):
        # If the line contains any Arabic character, add it to the Arabic list.
        if arabic_pattern.search(line):
            arabic_lines.append(line)
        # Otherwise, add it to the English list.
        else:
            english_lines.append(line)
            
    # Join the lines back together and remove any leading/trailing whitespace.
    english_result = " ".join(english_lines).strip()
    arabic_result = " ".join(arabic_lines).strip()
    
    # Prioritize returning English text if it exists and is substantial.
    if english_result:
        return english_result
    else:
        return arabic_result
