# Instagram Scraper & AI Processor

A Python-based tool that scrapes public Instagram profiles, extracts post data, performs OCR (Optical Character Recognition) on post images to extract embedded text, and outputs structured, enriched JSON data ready for downstream analysis.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Installation & Setup](#installation--setup)
- [Usage Manual](#usage-manual)
- [Pipeline Workflow](#pipeline-workflow)
- [File-by-File Documentation](#file-by-file-documentation)
- [Output Format](#output-format)
- [Configuration](#configuration)
- [Dependencies](#dependencies)

---

## Overview

This project automates the collection and enrichment of Instagram post data. It:

1. **Scrapes** public Instagram profiles using Instagram's private web API.
2. **Parses** the raw API response, extracting structured post metadata (captions, dates, image URLs, shortcodes).
3. **Transforms** each post by:
   - Downloading post images and running OCR to extract text embedded in images (supports English and Arabic).
   - Extracting hashtags and URLs from captions.
4. **Saves** both the raw scraped data and the final enriched/filtered data as timestamped JSON files in the `data/` directory.

The tool supports both **online mode** (live scraping from Instagram) and **offline mode** (processing from a previously saved raw JSON file).

---

## Architecture

```
instagram-scraper-ai-processor/
├── run.py                  # Entry point script
├── logging_config.py       # Centralized logging setup
├── pyproject.toml          # Project metadata
├── requirements.txt        # Python dependencies
├── scraper.log             # Runtime log output
├── data/                   # Output directory for JSON files
├── src/
│   ├── __init__.py
│   ├── config.py           # Global configuration & constants
│   ├── main.py             # CLI argument parsing & app bootstrap
│   ├── core/
│   │   ├── __init__.py
│   │   ├── pipeline.py     # Main orchestration pipeline
│   │   └── file_handler.py # JSON file I/O utilities
│   ├── scraper/
│   │   ├── __init__.py
│   │   ├── scraper.py      # HTTP client for Instagram API
│   │   └── parser.py       # Raw API response parser
│   └── processing/
│       ├── __init__.py
│       ├── extractor.py    # Hashtag, URL, and OCR extraction
│       ├── transformer.py  # Post enrichment & transformation
│       └── cleaner.py      # Bilingual text cleaning utility
```

The codebase follows a **layered pipeline architecture** with three distinct layers:

| Layer | Package | Responsibility |
|---|---|---|
| **Scraping** | `src/scraper/` | Fetch raw data from Instagram's API and parse it into structured dicts |
| **Processing** | `src/processing/` | Enrich posts with OCR text, hashtags, and URLs |
| **Core** | `src/core/` | Orchestrate the pipeline and handle file I/O |

---

## Installation & Setup

### Prerequisites

- **Python 3.9+**
- **Tesseract OCR** must be installed on your system for image text extraction.

#### Install Tesseract

- **macOS**: `brew install tesseract`
- **Ubuntu/Debian**: `sudo apt install tesseract-ocr tesseract-ocr-ara`
- **Windows**: Download installer from [Tesseract GitHub](https://github.com/UB-Mannheim/tesseract/wiki)

Make sure the Arabic language pack (`ara`) is installed for bilingual OCR support.

### Project Setup

```bash
# Clone the repository
git clone <repo-url>
cd instagram-scraper-ai-processor

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate    # macOS/Linux
# venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

---

## Usage Manual

### Online Mode (Live Scraping)

Scrapes the Instagram profiles defined in `src/config.py` and processes the results:

```bash
python run.py
```

This will:
1. Scrape each target username from Instagram's API.
2. Save raw data to `data/raw_posts_<timestamp>.json`.
3. Parse, transform, and enrich each post (including OCR on images).
4. Save the final output to `data/filtered_posts_<timestamp>.json`.

### Offline Mode (Process Existing Data)

Re-process a previously scraped raw JSON file without making any network requests to Instagram:

```bash
python run.py --offline
```

This uses the default input file at `data/raw_posts.json`. To specify a different file:

```bash
python run.py --offline --input-file path/to/your/raw_data.json
```

### CLI Arguments

| Argument | Type | Default | Description |
|---|---|---|---|
| `--offline` | flag | `false` | Run in offline mode using a local JSON file instead of scraping Instagram |
| `--input-file` | string | `data/raw_posts.json` | Path to the raw JSON file to use in offline mode |

### Configuring Target Accounts

Edit the `TARGET_USERNAMES` list in `src/config.py` to add or remove Instagram accounts to scrape:

```python
TARGET_USERNAMES = [
    "zawyacinema",
    "adef.xyz",
    "eunicinegypt",
]
```

### Logs

All activity is logged to both the console and `scraper.log` in the project root.

---

## Pipeline Workflow

The following describes the step-by-step flow when you run the tool:

```
┌─────────────────────────────────────────────────────────┐
│  1. SCRAPE (online) or LOAD (offline)                   │
│     - Online: hit Instagram API for each target user    │
│     - Offline: load from local JSON file                │
│     - Save raw data to data/raw_posts_<ts>.json         │
├─────────────────────────────────────────────────────────┤
│  2. PARSE                                               │
│     - Extract posts from nested API response via JMESPath│
│     - Normalize timestamps, build post URLs             │
│     - Collect all photo URLs (single & carousel posts)  │
├─────────────────────────────────────────────────────────┤
│  3. TRANSFORM                                           │
│     - For each post:                                    │
│       a. Download each photo and run OCR (eng+ara)      │
│       b. Extract hashtags from caption                  │
│       c. Extract URLs from caption                      │
│     - Restructure photo data into media[] array         │
├─────────────────────────────────────────────────────────┤
│  4. SAVE                                                │
│     - Write enriched posts to                           │
│       data/filtered_posts_<ts>.json                     │
└─────────────────────────────────────────────────────────┘
```

---

## File-by-File Documentation

### `run.py` — Entry Point

The top-level script that bootstraps the application. It imports and calls `main()` from `src/main.py`. This file exists so you can run the project simply with `python run.py` from the project root.

---

### `logging_config.py` — Logging Configuration

Sets up Python's built-in logging with:
- **Log level**: `INFO`
- **Format**: `timestamp - logger_name - level - message`
- **Handlers**:
  - `FileHandler` — writes to `scraper.log`
  - `StreamHandler` — prints to stdout (console)

Called at application startup to ensure consistent logging across all modules.

---

### `pyproject.toml` — Project Metadata

Minimal Python project configuration file. Defines the project name (`scraper`) and version (`0.1.0`), and configures setuptools to find packages in the `src/` directory.

---

### `requirements.txt` — Dependencies

Lists the four external Python packages required:

| Package | Purpose |
|---|---|
| `httpx` | Modern async-capable HTTP client used to call the Instagram API and download images |
| `jmespath` | JSON query language used to extract specific fields from deeply nested API responses |
| `pytesseract` | Python wrapper for Tesseract OCR engine |
| `Pillow` | Image processing library (PIL fork), used to open downloaded images for OCR |

---

### `src/config.py` — Global Configuration

Central configuration file containing all tunable constants:

| Constant | Description |
|---|---|
| `TARGET_USERNAMES` | List of Instagram usernames to scrape |
| `MIN_DELAY_SECONDS` | Minimum random delay between scraping each profile (2s) — avoids rate limiting |
| `MAX_DELAY_SECONDS` | Maximum random delay between scraping each profile (5s) |
| `INSTAGRAM_HEADERS` | HTTP headers sent with each API request, including `x-ig-app-id` and a browser User-Agent to mimic a real browser session |
| `MEDIA_QUERY` | JMESPath expression that extracts post data (shortcode, display URL, timestamp, caption, carousel photos) from the raw API response |
| `OUTPUT_DIR` | Directory where output JSON files are saved (`data/`) |

---

### `src/main.py` — CLI & Application Bootstrap

Handles command-line argument parsing using `argparse` and kicks off the pipeline:

- Configures logging via `setup_logging()`
- Defines two CLI arguments: `--offline` and `--input-file`
- Calls `run_pipeline(args)` inside a try/except that catches and logs critical errors
- Can also be run directly with `python -m src.main`

---

### `src/core/pipeline.py` — Pipeline Orchestrator

The central orchestration module that ties the entire workflow together. The `run_pipeline(args)` function:

1. **Data acquisition**: Either scrapes Instagram (online) or loads from a JSON file (offline).
   - In online mode, iterates over `TARGET_USERNAMES`, scrapes each with random delays between requests, and saves raw data.
2. **Parsing**: For each username's raw data, calls `parse_media_posts()` to extract structured post dicts.
3. **Transformation**: Calls `transform_all_posts()` to enrich all parsed posts with OCR text, hashtags, and URLs.
4. **Output**: Saves the final enriched data to a timestamped JSON file.

---

### `src/core/file_handler.py` — File I/O Utilities

Provides two helper functions for JSON file operations:

- **`save_json_file(data, filename_prefix)`**: Saves data to `data/<prefix>_<YYYYMMDD_HHMMSS>.json` with UTF-8 encoding and 4-space indentation. Creates the output directory if it doesn't exist.
- **`load_json_file(file_path)`**: Loads and returns a JSON file. Returns `None` with a logged error if the file is not found or contains invalid JSON.

---

### `src/scraper/scraper.py` — Instagram API Client

Contains the `InstagramScraper` class that communicates with Instagram's private web API:

- **`__init__()`**: Creates an `httpx.Client` with the configured Instagram headers (browser-like User-Agent, app ID).
- **`get_user_profile(username)`**: Sends a GET request to `https://i.instagram.com/api/v1/users/web_profile_info/?username={username}` and returns the `data.user` object from the response. Returns `None` on any HTTP or parsing error.
- **`close()`**: Closes the underlying HTTP client connection.

---

### `src/scraper/parser.py` — API Response Parser

Parses the raw user profile data into a clean list of post dictionaries:

- **`parse_media_posts(raw_user_data, username)`**: Uses JMESPath to query the nested Instagram API response structure. For each post, it:
  - Converts Unix timestamps to ISO 8601 date strings
  - Collects all photo URLs (handles both single-image posts and carousel/sidecar posts with multiple images)
  - Builds the public Instagram post URL from the shortcode
  - Returns a list of dicts with keys: `source`, `shortcode`, `post_url`, `display_url`, `post_date`, `timestamp`, `caption`, `photos`

---

### `src/processing/extractor.py` — Data Extraction Utilities

Contains three extraction functions:

- **`extract_hashtags(text)`**: Uses regex `#(\w+)` to find all hashtags in a text string. Returns a list of hashtag strings (without the `#` symbol).
- **`extract_urls(text)`**: Uses regex `https?://\S+` to find all URLs in a text string.
- **`extract_text_from_image_url(image_url)`**: Downloads an image from a URL, opens it with Pillow, and runs Tesseract OCR with both English and Arabic language support (`eng+ara`). Returns the extracted text or an empty string on failure.

---

### `src/processing/transformer.py` — Post Transformation

Enriches parsed posts with additional extracted data:

- **`transform_post_data(post)`**: For a single post:
  - Downloads each photo URL and runs OCR to extract embedded text
  - Restructures the flat `photos` list into a `media` array of `{url, text}` objects
  - Extracts hashtags and URLs from the caption
  - Returns the enriched post dict
- **`transform_all_posts(posts)`**: Iterates over all posts, calling `transform_post_data()` on each with progress logging.

---

### `src/processing/cleaner.py` — Bilingual Text Cleaner

A utility for separating bilingual (English/Arabic) text:

- **`clean_bilingual_text(text)`**: Splits text into lines, classifies each line as Arabic (if it contains Arabic Unicode characters `\u0600-\u06FF`) or English, and returns the English portion. Falls back to the Arabic portion if no English text is found. This is useful for cleaning OCR output from bilingual Instagram posts.

> **Note**: This function is defined but not currently wired into the pipeline. It can be used for post-processing OCR results.

---

## Output Format

### Raw Posts (`data/raw_posts_<timestamp>.json`)

The unmodified API response for each scraped user, keyed by username:

```json
{
    "zawyacinema": { /* raw Instagram API user object */ },
    "adef.xyz": { /* ... */ }
}
```

### Filtered/Enriched Posts (`data/filtered_posts_<timestamp>.json`)

A flat array of enriched post objects:

```json
[
    {
        "source": "zawyacinema",
        "shortcode": "ABC123",
        "post_url": "https://www.instagram.com/p/ABC123/",
        "display_url": "https://...",
        "post_date": "2025-10-15T14:30:00",
        "timestamp": 1697376600,
        "caption": "Event tonight! #cinema #art",
        "media": [
            {
                "url": "https://...",
                "text": "Text extracted from image via OCR"
            }
        ],
        "hashtags": ["cinema", "art"],
        "urls": []
    }
]
```

---

## Configuration

All configuration lives in `src/config.py`. Key settings you may want to change:

| Setting | What to change | Why |
|---|---|---|
| `TARGET_USERNAMES` | Add/remove Instagram usernames | Control which accounts are scraped |
| `MIN_DELAY_SECONDS` / `MAX_DELAY_SECONDS` | Adjust delay range | Balance between speed and avoiding rate limits |
| `INSTAGRAM_HEADERS` | Update `x-ig-app-id` or User-Agent | If Instagram changes their API requirements |
| `MEDIA_QUERY` | Modify JMESPath expression | If the API response structure changes |
| `OUTPUT_DIR` | Change output directory | Save files to a different location |

---

## Dependencies

| Package | Version | Purpose |
|---|---|---|
| [httpx](https://www.python-httpx.org/) | latest | HTTP client for API requests and image downloads |
| [jmespath](https://jmespath.org/) | latest | JSON query language for parsing API responses |
| [pytesseract](https://github.com/madmaze/pytesseract) | latest | Python wrapper for Tesseract OCR |
| [Pillow](https://pillow.readthedocs.io/) | latest | Image processing for OCR input |

**System dependency**: [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) must be installed separately (see Installation section).
