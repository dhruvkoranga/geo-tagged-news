from fastapi import FastAPI, HTTPException
from app.keyword_store import add_keyword, list_active_keywords
from app.store import get_articles_by_location

app = FastAPI(title="GeoTaggedNews")


@app.post("/keywords")
def create_keyword(value: str):
    if not value or len(value) < 3:
        raise HTTPException(status_code=400, detail="Invalid keyword")

    return add_keyword(value)


@app.get("/keywords")
def get_keywords():
    return list_active_keywords()


@app.get("/articles/by-location")
def articles_by_location(location: str):
    return get_articles_by_location(location)
