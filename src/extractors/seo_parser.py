thonpython
import requests
from bs4 import BeautifulSoup
import logging

class SEOParser:
    def __init__(self, url: str):
        self.url = url
        self.html = None
        self.soup = None
        self._fetch()

    def _fetch(self):
        try:
            resp = requests.get(self.url, timeout=10)
            resp.raise_for_status()
            self.html = resp.text
            self.soup = BeautifulSoup(self.html, "html.parser")
        except Exception as e:
            logging.error(f"Failed to fetch {self.url}: {e}")
            self.html = ""
            self.soup = BeautifulSoup("", "html.parser")

    def extract_meta(self):
        title = self.soup.title.string if self.soup.title else None
        description_tag = self.soup.find("meta", attrs={"name": "description"})
        description = description_tag["content"] if description_tag else None

        return {
            "title": title,
            "description": description,
            "title_length": len(title) if title else 0
        }

    def extract_keywords(self):
        text = self.soup.get_text(" ", strip=True)
        words = text.lower().split()
        freq = {}
        for w in words:
            if len(w) > 3:
                freq[w] = freq.get(w, 0) + 1

        top_keywords = sorted(freq.items(), key=lambda x: x[1], reverse=True)[:10]

        return {"top_keywords": top_keywords}