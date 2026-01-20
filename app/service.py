import logging
from app.parser import extract_article
from app.ner import detect_locations
from app.geocoder import resolve_location
from app.store import add_article
from app.models import GeoLocation
from app.dedup import article_fingerprint, is_duplicate

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



def _process_article(
    url: str,
    keyword: str | None = None,
    strict: bool = False
):
    logging.info(f"Processing article: {url}")
    article = extract_article(url)
    if not article:
        logging.warning(f"Could not extract article from {url}")
        if strict:
            raise ValueError("Article extraction failed")
        return None

    logging.info(f"Extracted title: {article['title']}")
    fp = article_fingerprint(article["title"], article["text"])
    if is_duplicate(fp):
        logging.info(f"Duplicate article found: {article['title']}")
        if strict:
            raise ValueError("Duplicate article")
        return None

    raw_locations = detect_locations(article["text"])
    logging.info(f"Detected {len(raw_locations)} raw locations: {raw_locations}")
    geo_locations = []

    for loc in raw_locations:
        geo = resolve_location(loc)
        if geo:
            logging.info(f"Resolved location '{loc}' to {geo}")
            geo_locations.append(GeoLocation(**geo))
        else:
            logging.warning(f"Could not resolve location: {loc}")

    if not geo_locations:
        logging.warning("No resolvable locations found in article.")
        if strict:
            raise ValueError("No resolvable locations found")
        return None

    return add_article(
        title=article["title"],
        text=article["text"],
        locations=geo_locations,
        keywords=[keyword] if keyword else []
    )


# -------- Public APIs -------- #

def process_article(url: str, keyword: str):
    """
    Used by background worker.
    Best-effort ingestion.
    Never raises.
    """
    try:
        return _process_article(url=url, keyword=keyword, strict=False)
    except Exception:
        return None


def ingest_article(url: str):
    """
    Used for manual / debug ingestion.
    Strict mode.
    Raises on failure.
    """
    return _process_article(url=url, strict=True)
