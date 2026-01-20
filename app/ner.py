import spacy

nlp = spacy.load("en_core_web_sm")


def detect_locations(text: str) -> set[str]:
    doc = nlp(text)
    locations = set()

    for ent in doc.ents:
        if ent.label_ in {"GPE", "LOC"}:
            cleaned = ent.text.strip()
            if len(cleaned) > 2:
                locations.add(cleaned)

    return locations
