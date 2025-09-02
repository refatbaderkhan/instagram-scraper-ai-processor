from typing import Union

import httpx

from config import INSTAGRAM_HEADERS


class InstagramScraper:
    _BASE_URL = (
        "https://i.instagram.com/api/v1/users/web_profile_info/?username={username}"
    )

    def __init__(self):
        self.client = httpx.Client(headers=INSTAGRAM_HEADERS)

    def get_user_profile(self, username: str) -> Union[dict, None]:
        try:
            url = self._BASE_URL.format(username=username)
            response = self.client.get(url)
            response.raise_for_status()
            data = response.json()
            return data.get("data", {}).get("user")
        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred while fetching {username}: {e}")
            return None
        except (KeyError, TypeError):
            print(f"could not find valid user data in the response for {username}.")
            return None
        except Exception as e:
            print(f"an unexpected error occurred: {e}")
            return None

    def close(self):
        self.client.close()
