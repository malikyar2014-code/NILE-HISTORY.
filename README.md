# NILE HISTORY — v0.1

A mobile-first historical encyclopedia for Sudan 🇸🇩 and South Sudan 🇸🇸.

## Run locally (Python 3.10+)
```bash
python -m venv .venv
# Linux/macOS/Termux
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
Open http://127.0.0.1:8000

## Android
Run in Termux or deploy to a Python-capable host. Serve over HTTPS for PWA installation; open in Chrome and choose Install app / Add to Home screen.

## Project structure
- `app/main.py` — FastAPI API and web routes
- `app/data.py` — starter historical records
- `app/static/` — responsive PWA interface, manifest, service worker and icon

## Research integrity
This is a starter archive, not a complete history. Source leads are not proof that every detail is verified. Expand entries only after checking primary and academic sources and recording exact bibliographic details, page numbers or stable URLs.