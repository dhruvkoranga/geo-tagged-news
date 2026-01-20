import json
import os
from typing import List
from app.models import GeoLocation

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

ARTICLES_FILE = os.path.join(BASE_DIR, "articles.json")
LOCATION_INDEX_FILE = os.path.join(BASE_DIR, "location_index.json")


def _load_json(path, default):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def _save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def add_article(
    title: str,
    text: str,
    locations: List[GeoLocation],
    keywords: List[str],
):
    articles = _load_json(ARTICLES_FILE, [])
    location_index = _load_json(LOCATION_INDEX_FILE, {})

    article_id = len(articles)

    article = {
        "id": article_id,
        "title": title,
        "text": text,
        "keywords": keywords,
        "locations": [loc.model_dump() for loc in locations],
    }

    articles.append(article)

    for loc in locations:
        key = loc.name.lower()
        location_index.setdefault(key, []).append(article_id)

    _save_json(ARTICLES_FILE, articles)
    _save_json(LOCATION_INDEX_FILE, location_index)

    return article
