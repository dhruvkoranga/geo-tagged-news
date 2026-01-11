from fastapi import FastAPI

app = FastAPI(title="GeoTaggedNews")

@app.get("/")
def health():
    return {"status": "ok"}
