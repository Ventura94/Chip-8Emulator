import os

import requests

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class ROM:
    def __init__(self, url: str):
        self.BASE_DIR = BASE_DIR
        self.data = self._load_from_url(url)

    def _load_from_url(self, url):
        response = requests.get(url)
        if response.status_code != 200:
            raise ValueError(f"Failed to fetch ROM from URL: {url}")
        return response.content
