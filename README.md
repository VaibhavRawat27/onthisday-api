# 🌍 OnThisDay API

> **Version:** v0.1.0  
> **Status:** Public API (Free)  
> **Hosted on:** Vercel  

A fast, simple, and developer-friendly **On This Day API** that provides important historical events, famous birthdays, death anniversaries, holidays, and observances for any given date — powered by Wikipedia.

---

## ✨ Features

- 📅 Get historical data for **any date**
- 🎉 Important historical events
- 🎂 Famous birthdays
- ⚰️ Death anniversaries
- 🎊 Holidays & observances
- ⚡ Fast responses with caching
- 🛡️ Built-in rate limiting
- 🌐 Public & free to use
- 🚀 Hosted on Vercel

---

## 🔗 Base URL

```
https://onthisday.vercel.app
```

---

## 📌 Endpoint

### Get data for a specific date

```
GET /onthisday
```

### Query Parameters

| Parameter | Type | Required | Description |
|---------|------|----------|-------------|
| `date` | string | No | Date in `YYYY-MM-DD` format. Defaults to today if not provided |

---

## 🧪 Example Requests

### Today’s data
```
GET /onthisday
```

### Custom date
```
GET /onthisday?date=2020-08-15
```

---

## 📦 Example Response

```json
{
  "date": {
    "day": 15,
    "month": 8,
    "formatted": "August 15",
    "weekday": "Saturday"
  },
  "events": [
    {
      "year": 1947,
      "description": "India gained independence from British rule."
    }
  ],
  "birthdays": [
    {
      "name": "Napoleon Bonaparte",
      "year": 1769,
      "description": "French military leader and emperor."
    }
  ],
  "deaths": [
    {
      "name": "Rabindranath Tagore",
      "year": 1941,
      "description": "Indian poet and Nobel laureate."
    }
  ],
  "holidays": [
    {
      "name": "Independence Day (India)"
    }
  ],
  "meta": {
    "source": "Wikipedia",
    "cached": true
  }
}
```

---

## 🛡️ Rate Limiting

- **20 requests per minute per IP**
- Exceeding the limit returns:
```json
{
  "error": "Rate limit exceeded. Try again later."
}
```

---

## ⚡ Caching

- Responses are cached for **24 hours**
- Improves performance & avoids Wikipedia rate limits
- Cache resets on cold starts (Vercel behavior)

---

## 🧠 Data Source

- 📚 **Wikipedia REST API**
- Data is fetched once and cached
- Proper User-Agent used (as per Wikipedia guidelines)

---

## 🧑‍💻 Tech Stack

- **FastAPI** – API framework
- **Python 3.9+**
- **SlowAPI** – Rate limiting
- **Requests** – HTTP client
- **Vercel** – Hosting

---

## 🚀 Local Development

### Install dependencies
```bash
pip install -r requirements.txt
```

### Run locally
```bash
uvicorn main:app --reload
```

Visit:
```
http://127.0.0.1:8000/onthisday
```

Swagger Docs:
```
http://127.0.0.1:8000/docs
```

---

## 📈 Roadmap

- [ ] Random date endpoint
- [ ] Country-specific observances (India-first)
- [ ] Language support
- [ ] API key system
- [ ] Redis / KV caching
- [ ] Usage analytics

---

## ⚠️ Disclaimer

This API uses data from **Wikipedia**.  
Data accuracy depends on Wikipedia contributors.

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

## 🙌 Author

Built with ❤️ for developers  
If you like this project, ⭐ the repo and share it!