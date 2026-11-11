from pathlib import Path
import json
from urllib.request import Request, urlopen
from urllib.parse import quote
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse, PlainTextResponse
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
    "prehistory-sudan": "Prehistory_of_Sudan",
    "nubia": "Nubia",
    "kerma-culture": "Kerma_culture",
    "kingdom-kush": "Kingdom_of_Kush",
    "napata": "Napata",
    "meroe": "Meroe",
    "nobatia": "Nobatia",
    "makuria": "Makuria",
    "alodia": "Alodia",
    "funj-sultanate": "Funj_Sultanate",
    "darfur-sultanate": "Sultanate_of_Darfur",
    "turco-egyptian": "Turco-Egyptian_conquest_of_Sudan",
    "mahdist-war": "Mahdist_War",
    "anglo-egyptian": "Anglo-Egyptian_Sudan",
    "first-civil-war": "First_Sudanese_Civil_War",
    "second-civil-war": "Second_Sudanese_Civil_War",
    "peace-agreement": "Comprehensive_Peace_Agreement",
    "south-sudan-war": "South_Sudanese_Civil_War",
    "sudan-war": "War_in_Sudan_(2023)",
}
WIKIPEDIA_COLLECTION = [
    {"id":"prehistory-sudan","title":"Prehistory of Sudan","group":"Prehistory & archaeology"},
    {"id":"nubia","title":"Nubia","group":"Nubian history"},
    {"id":"kerma-culture","title":"Kerma culture","group":"Ancient kingdoms"},
    {"id":"kingdom-kush","title":"Kingdom of Kush","group":"Ancient kingdoms"},
    {"id":"napata","title":"Napata","group":"Ancient kingdoms"},
    {"id":"meroe","title":"Meroë","group":"Ancient kingdoms"},
    {"id":"nobatia","title":"Nobatia","group":"Christian Nubian kingdoms"},
    {"id":"makuria","title":"Makuria","group":"Christian Nubian kingdoms"},
    {"id":"alodia","title":"Alodia","group":"Christian Nubian kingdoms"},
    {"id":"funj-sultanate","title":"Funj Sultanate","group":"Sultanates & regional states"},
    {"id":"darfur-sultanate","title":"Sultanate of Darfur","group":"Sultanates & regional states"},
    {"id":"turco-egyptian","title":"Turco-Egyptian conquest of Sudan","group":"Modern history"},
    {"id":"mahdist-war","title":"Mahdist War","group":"Modern history"},
    {"id":"anglo-egyptian","title":"Anglo-Egyptian Sudan","group":"Modern history"},
    {"id":"first-civil-war","title":"First Sudanese Civil War","group":"Civil wars & peace"},
    {"id":"second-civil-war","title":"Second Sudanese Civil War","group":"Civil wars & peace"},
    {"id":"peace-agreement","title":"Comprehensive Peace Agreement","group":"Civil wars & peace"},
    {"id":"south-sudan-war","title":"South Sudanese Civil War","group":"Civil wars & peace"},
    {"id":"sudan-war","title":"War in Sudan (2023)","group":"Contemporary history"},
    {"id":"sudan","title":"History of Sudan","group":"Complete country histories"},
    {"id":"south-sudan","title":"History of South Sudan","group":"Complete country histories"},
]

@app.get("/api/library/catalog")
def wikipedia_catalog():
    return {"count": len(WIKIPEDIA_COLLECTION), "items": WIKIPEDIA_COLLECTION}


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


# Public-domain source books with verified catalogue metadata.
# Copyright status is territory-specific; this edition is marked public domain in the USA by Project Gutenberg.
HISTORICAL_BOOKS = {
    "anglo-egyptian-sudan-vol1": {
        "id": "anglo-egyptian-sudan-vol1",
        "title": "The Anglo-Egyptian Sudan: A Compendium, Volume I",
        "author": "Sudan. Wizarat al-Naql wa-al-Muwasalat",
        "editor": "Lord Edward Gleichen",
        "year": "1905",
        "publisher": "His Majesty's Stationery Office, London",
        "description": "A large contemporary government compendium covering geography, peoples, administration and a historical section from early periods through the end of the nineteenth century.",
        "source": "Project Gutenberg, eBook 74584",
        "source_url": "https://www.gutenberg.org/ebooks/74584",
        "text_url": "https://www.gutenberg.org/cache/epub/74584/pg74584.txt",
        "rights": "Project Gutenberg identifies this edition as public domain in the United States. Copyright rules differ by country; readers and redistributors outside the USA should check local law.",
        "editorial_warning": "Produced by colonial government officers in 1905. It is a valuable primary source for the period, but its descriptions, categories and political assumptions reflect the colonial administration. Read critically and compare with Sudanese scholarship, community histories and other independent sources.",
        "language": "English",
        "pages": "351 pages in Volume I, plus illustrations and appendices in the digitised edition"
    },
    "anglo-egyptian-sudan-vol2": {
        "id": "anglo-egyptian-sudan-vol2",
        "title": "The Anglo-Egyptian Sudan: A Compendium, Volume II — Routes",
        "author": "Sudan. Wizarat al-Naql wa-al-Muwasalat",
        "editor": "Lord Edward Gleichen",
        "year": "1905",
        "publisher": "His Majesty's Stationery Office, London",
        "description": "The second volume of the 1905 government compendium, focused on routes and travel information across the Sudan of its period.",
        "source": "Project Gutenberg, eBook 74585",
        "source_url": "https://www.gutenberg.org/ebooks/74585",
        "text_url": "https://www.gutenberg.org/cache/epub/74585/pg74585.txt",
        "rights": "Project Gutenberg identifies this edition as public domain in the United States. Copyright rules differ by country; readers and redistributors outside the USA should check local law.",
        "editorial_warning": "Produced by colonial government officers in 1905. Its route descriptions are a historical snapshot, not a current map or present-day travel guide. Read its descriptions and classifications critically.",
        "language": "English"
    },
    "incidents-nubia-darfur": {
        "id": "incidents-nubia-darfur",
        "title": "Incidents on a Journey through Nubia to Darfoor",
        "author": "F. Sidney Ensor",
        "editor": "Original 1881 edition",
        "year": "1881",
        "publisher": "W. H. Allen & Co., London",
        "description": "A nineteenth-century travel narrative describing a journey through Nubia toward Darfur. It is useful as a contemporary account of places, routes and encounters, but does not represent the perspectives of all the communities described.",
        "source": "Project Gutenberg, eBook 78526",
        "source_url": "https://www.gutenberg.org/ebooks/78526",
        "text_url": "https://www.gutenberg.org/cache/epub/78526/pg78526.txt",
        "rights": "Project Gutenberg identifies this edition as public domain in the United States. Copyright rules differ by country; readers and redistributors outside the USA should check local law.",
        "editorial_warning": "A Victorian travel narrative written by an outsider. Its observations, names and descriptions may reflect the author's assumptions and the conventions of nineteenth-century travel writing. Compare it with Sudanese oral histories, local scholarship and other sources.",
        "language": "English"
    }
    ,
    "ten-years-captivity-mahdi": {
        "id": "ten-years-captivity-mahdi",
        "title": "Ten Years' Captivity in the Mahdi's Camp, 1882–1892",
        "author": "Josef Ohrwalder",
        "editor": "Translated and edited by F. R. Wingate",
        "year": "1892",
        "publisher": "Sampson Low, Marston & Company, London",
        "description": "A first-person account by an Austrian missionary who was held in the Mahdist state. It offers evidence about captivity and the period through one author's experience, not a comprehensive account of Sudanese society or the Mahdist revolution.",
        "source": "Project Gutenberg, eBook 32875",
        "source_url": "https://www.gutenberg.org/ebooks/32875",
        "text_url": "https://www.gutenberg.org/cache/epub/32875/pg32875.txt",
        "rights": "Project Gutenberg identifies this edition as public domain in the United States. Copyright rules differ by country; readers and redistributors outside the USA should check local law.",
        "editorial_warning": "A missionary's captivity narrative, translated and edited in a colonial-era context. It is valuable testimony but reflects the author's religious and political position; compare it with Sudanese accounts, Mahdist sources and modern scholarship.",
        "language": "English"
    },
    "egyptian-campaigns-1882-1885": {
        "id": "egyptian-campaigns-1882-1885",
        "title": "The Egyptian Campaigns, 1882 to 1885",
        "author": "Charles Royle",
        "editor": "Original nineteenth-century edition",
        "year": "1886",
        "publisher": "Hurst and Blackett, London",
        "description": "A military and political narrative of the campaigns and events surrounding British intervention in Egypt and the Mahdist conflict. It is a period account, not a balanced modern history of Sudan.",
        "source": "Project Gutenberg, eBook 41744",
        "source_url": "https://www.gutenberg.org/ebooks/41744",
        "text_url": "https://www.gutenberg.org/cache/epub/41744/pg41744.txt",
        "rights": "Project Gutenberg identifies this edition as public domain in the United States. Copyright rules differ by country; readers and redistributors outside the USA should check local law.",
        "editorial_warning": "A nineteenth-century military account shaped by British imperial perspectives. Read its descriptions of Sudanese people and political movements critically and alongside Sudanese sources and later scholarship.",
        "language": "English"
    },
    "khartoum-blue-white-niles-vol1": {
        "id": "khartoum-blue-white-niles-vol1",
        "title": "Khartoum, and the Blue and White Niles, Volume I",
        "author": "George Melly",
        "editor": "Original edition",
        "year": "1851",
        "publisher": "Colburn & Co., London",
        "description": "A Victorian travel narrative following a journey from Egypt up the Nile toward Nubia and Khartoum, recording landscapes, antiquities and encounters through the author's own perspective.",
        "source": "Project Gutenberg, eBook 78014",
        "source_url": "https://www.gutenberg.org/ebooks/78014",
        "text_url": "https://www.gutenberg.org/cache/epub/78014/pg78014.txt",
        "rights": "Project Gutenberg identifies this edition as public domain in the United States. Copyright rules differ by country; readers and redistributors outside the USA should check local law.",
        "editorial_warning": "A nineteenth-century outsider's travelogue. Its depictions of people, religion, slavery and social life reflect the author's time and viewpoint; they should not be treated as neutral ethnography.",
        "language": "English"
    },
    "khartoum-blue-white-niles-vol2": {
        "id": "khartoum-blue-white-niles-vol2",
        "title": "Khartoum, and the Blue and White Niles, Volume II",
        "author": "George Melly",
        "editor": "Original edition",
        "year": "1851",
        "publisher": "Colburn & Co., London",
        "description": "The second volume of Melly's travel narrative, continuing the account of travel and observations along the Nile and in the region of Khartoum.",
        "source": "Project Gutenberg, eBook 78015",
        "source_url": "https://www.gutenberg.org/ebooks/78015",
        "text_url": "https://www.gutenberg.org/cache/epub/78015/pg78015.txt",
        "rights": "Project Gutenberg identifies this edition as public domain in the United States. Copyright rules differ by country; readers and redistributors outside the USA should check local law.",
        "editorial_warning": "A nineteenth-century outsider's travelogue. Its depictions of people, religion, slavery and social life reflect the author's time and viewpoint; they should not be treated as neutral ethnography.",
        "language": "English"
    }
}

@app.get("/api/library/books")
def historical_book_catalog():
    return {"count": len(HISTORICAL_BOOKS), "items": [
        {key: value for key, value in book.items() if key != "text_url"}
        for book in HISTORICAL_BOOKS.values()
    ]}

_BOOK_TEXT_CACHE = {}

@app.get("/api/library/books/{book_id}/text", response_class=PlainTextResponse)
def historical_book_text(book_id: str):
    book = HISTORICAL_BOOKS.get(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found in the NILE HISTORY collection")
    if book_id not in _BOOK_TEXT_CACHE:
        request = Request(book["text_url"], headers={"User-Agent": "NILE-HISTORY/1.0 (historical source reader)"})
        try:
            with urlopen(request, timeout=35) as response:
                text = response.read().decode("utf-8-sig")
        except Exception as exc:
            raise HTTPException(status_code=502, detail="The digitised book is temporarily unavailable. Please try again.") from exc
        if "*** START OF THE PROJECT GUTENBERG EBOOK" not in text:
            raise HTTPException(status_code=502, detail="The source text did not pass the expected edition check.")
        _BOOK_TEXT_CACHE[book_id] = text
    return PlainTextResponse(_BOOK_TEXT_CACHE[book_id], headers={"Cache-Control": "public, max-age=3600"})
