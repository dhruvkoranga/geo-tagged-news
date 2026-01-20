import json
from typing import List
from app.models import Keyword

_KEYWORDS_FILE = "keywords.json"

def _load_keywords() -> List[Keyword]:
    try:
        with open(_KEYWORDS_FILE, "r") as f:
            keywords_data = json.load(f)
            return [Keyword(**data) for data in keywords_data]
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def _save_keywords(keywords: List[Keyword]):
    with open(_KEYWORDS_FILE, "w") as f:
        json.dump([k.dict() for k in keywords], f, indent=2)

def add_keyword(value: str) -> Keyword:
    keywords = _load_keywords()
    keyword = Keyword(
        id=len(keywords),
        value=value.lower().strip(),
        active=True
    )
    keywords.append(keyword)
    _save_keywords(keywords)
    return keyword

def list_active_keywords() -> List[Keyword]:
    keywords = _load_keywords()
    return [k for k in keywords if k.active]
