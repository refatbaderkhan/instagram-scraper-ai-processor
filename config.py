TARGET_USERNAMES = [
    "zawyacinema",
    "adef.xyz",
    # "goetheinstitut_kairo",
    # "bwfcaravan",
    "eunicinegypt",
    ]

MIN_DELAY_SECONDS = 2
MAX_DELAY_SECONDS = 5

INSTAGRAM_HEADERS = {
    "x-ig-app-id": "936619743392459",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9,ru;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept": "*/*",
}

MEDIA_QUERY = (
    'edge_owner_to_timeline_media.edges[].node.'
    '{shortcode: shortcode, '
    'display_url: display_url, '
    'date: taken_at_timestamp, ' 
    'caption: edge_media_to_caption.edges[0].node.text,'
    'taken_at_timestamp: taken_at_timestamp, '
    'photos: edge_sidecar_to_children.edges[].node.display_url}'
)

OUTPUT_DIR = "data"