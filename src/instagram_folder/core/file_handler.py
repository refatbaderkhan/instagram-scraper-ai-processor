import json
import logging
import os
from datetime import datetime

from config import OUTPUT_DIR


def save_json_file(data, filename_prefix: str) -> str:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(OUTPUT_DIR, f"{filename_prefix}_{timestamp}.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    logging.info(f"Successfully saved data to '{file_path}'")
    return file_path


def load_json_file(file_path: str) -> dict:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error(f"Error: The file '{file_path}' was not found.")
        return None
    except json.JSONDecodeError:
        logging.error(f"Error: Could not decode JSON from the file '{file_path}'.")
        return None
