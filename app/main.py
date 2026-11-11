from pathlib import Path
import json
from urllib.request import Request, urlopen
from urllib.parse import quote
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


WIKIPEDIA_PAGES = {
    "sudan": "History_of_Sudan",
    "south-sudan": "History_of_South_Sudan",
}

@app.get("/api/library/wikipedia/{page_id}")
def wikipedia_article(page_id: str):
    """Fetch the full current Wikipedia article for in-app reading, with licence metadata."""
    title = WIKIPEDIA_PAGES.get(page_id)
    if not title:
        raise HTTPException(status_code=404, detail="Wikipedia article not found in the NILE HISTORY source library")
    url = f"https://en.wikipedia.org/w/rest.php/v1/page/{quote(title, safe='_')}/with_html"
    request = Request(url, headers={"User-Agent": "NILE-HISTORY/1.0 (in-app historical reading; contact via project repository)"})
    try:
        with urlopen(request, timeout=20) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except Exception as exc:
        raise HTTPException(status_code=502, detail="Wikipedia source is temporarily unavailable. Please try again later.") from exc
    return {
        "title": payload.get("title", title.replace("_", " ")),
        "html": payload.get("html", ""),
        "revision": payload.get("latest", {}).get("id"),
        "timestamp": payload.get("latest", {}).get("timestamp"),
        "license": payload.get("license", {}),
        "source_url": f"https://en.wikipedia.org/wiki/{title}",
        "history_url": f"https://en.wikipedia.org/w/index.php?title={title}&action=history",
        "attribution": "Wikipedia contributors",
    }
