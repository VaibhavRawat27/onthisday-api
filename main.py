from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
import requests
from fastapi.responses import RedirectResponse
# Rate limiting
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

app = FastAPI(title="On This Day API – V1")

# ---------------- RATE LIMIT ----------------
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.exception_handler(RateLimitExceeded)
def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"error": "Rate limit exceeded. Try again later."},
    )

# ---------------- CACHE (IN-MEMORY) ----------------
CACHE = {}
CACHE_EXPIRY = timedelta(hours=24)

def get_cache(key):
    data = CACHE.get(key)
    if not data:
        return None
    if datetime.utcnow() > data["expires"]:
        del CACHE[key]
        return None
    return data["value"]

def set_cache(key, value):
    CACHE[key] = {
        "value": value,
        "expires": datetime.utcnow() + CACHE_EXPIRY
    }

# ---------------- WIKIPEDIA FETCH ----------------
HEADERS = {
    "User-Agent": "OnThisDayAPI/1.0 (contact: example@email.com)"
}

def fetch_wikipedia(month, day):
    base = f"https://en.wikipedia.org/api/rest_v1/feed/onthisday"
    urls = {
        "events": f"{base}/events/{month}/{day}",
        "births": f"{base}/births/{month}/{day}",
        "deaths": f"{base}/deaths/{month}/{day}",
        "holidays": f"{base}/holidays/{month}/{day}"
    }

    data = {}
    for key, url in urls.items():
        res = requests.get(url, headers=HEADERS)
        data[key] = res.json().get(key, [])

    return data

# ---------------- MAIN ENDPOINT ----------------
@app.get("/onthisday")
@limiter.limit("20/minute")
def on_this_day(request: Request, date: str = None):
    # Parse date
    try:
        if date:
            selected_date = datetime.strptime(date, "%Y-%m-%d")
        else:
            selected_date = datetime.utcnow()
    except ValueError:
        return JSONResponse(
            status_code=400,
            content={"error": "Invalid date format. Use YYYY-MM-DD"}
        )

    month = selected_date.month
    day = selected_date.day
    cache_key = f"{month}-{day}"

    # Cache check
    cached = get_cache(cache_key)
    if cached:
        return cached

    # Fetch data
    wiki_data = fetch_wikipedia(month, day)

    response = {
        "date": {
            "day": day,
            "month": month,
            "formatted": selected_date.strftime("%B %d"),
            "weekday": selected_date.strftime("%A")
        },
        "events": [
            {
                "year": e.get("year"),
                "description": e.get("text")
            } for e in wiki_data["events"][:10]
        ],
        "birthdays": [
            {
                "name": b["pages"][0]["title"] if b.get("pages") else None,
                "year": b.get("year"),
                "description": b.get("text")
            } for b in wiki_data["births"][:10]
        ],
        "deaths": [
            {
                "name": d["pages"][0]["title"] if d.get("pages") else None,
                "year": d.get("year"),
                "description": d.get("text")
            } for d in wiki_data["deaths"][:10]
        ],
        "holidays": [
            {
                "name": h.get("text")
            } for h in wiki_data["holidays"]
        ],
        "meta": {
            "source": "Wikipedia",
            "cached": False
        }
    }

    set_cache(cache_key, response)
    response["meta"]["cached"] = True

    return response

@app.get("/")
def root():
    return RedirectResponse(url="/docs")

