from pathlib import Path
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from app.data import ARTICLES

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
app = FastAPI(title="NILE HISTORY API", version="0.1.0")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/", response_class=HTMLResponse)
def home():
    return (STATIC_DIR / "index.html").read_text(encoding="utf-8")

@app.get("/api/health")
def health():
    return {"status": "ok", "app": "NILE HISTORY", "version": "0.1.0"}

@app.get("/api/articles")
def articles(q: str = Query(default="", max_length=100), category: str = ""):
    q = q.strip().casefold()
    results = ARTICLES
    if category:
        results = [a for a in results if a["category"].casefold() == category.casefold()]
    if q:
        results = [a for a in results if q in " ".join(
            [a["title"], a["period"], a["region"], a["category"], a["summary"]]
        ).casefold()]
    return {"count": len(results), "items": results}

@app.get("/api/articles/{article_id}")
def article(article_id: str):
    for item in ARTICLES:
        if item["id"] == article_id:
            return item
    raise HTTPException(status_code=404, detail="Article not found")
