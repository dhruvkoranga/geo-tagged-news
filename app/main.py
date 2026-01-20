from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

from app.keyword_store import add_keyword, list_active_keywords
from app.store import get_articles_by_location

app = FastAPI(title="GeoTaggedNews")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


app.mount("/", StaticFiles(directory="frontend", html=True), name="static")
