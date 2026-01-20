import hashlib

_seen_fingerprints: set[str] = set()


def article_fingerprint(title: str, text: str) -> str:
    payload = f"{title}:{text[:500]}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def is_duplicate(fp: str) -> bool:
    if fp in _seen_fingerprints:
        return True

    _seen_fingerprints.add(fp)
    return False
