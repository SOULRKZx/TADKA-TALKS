from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os

# Import your functions
from utils.fetch_news import get_news
from utils.generate_summary import generate_summary

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Store last news and topic for context ---
last_news_cache = {
    "topic": None,
    "raw_news": None
}

@app.get("/")
def home():
    return FileResponse(os.path.join(BASE_DIR, "static", "index.html"))

@app.get("/news")
async def get_tadka_news(topic: str = Query(...), style: str = Query("tadka")):
    global last_news_cache

    # Detect if user is asking for continuation
    if topic.lower().strip() in ["aur", "aur bata", "tell me more", "continue", "phir kya"]:
        if last_news_cache["raw_news"] is None:
            return {"error": "No previous news found to continue from 😓"}
        
        summary = generate_summary(last_news_cache["raw_news"], style)
        return {
            "topic": last_news_cache["topic"] + " (continued)",
            "summary": summary
        }

    # Otherwise, fetch new news
    raw_news = get_news(topic)
    if not raw_news:
        return {"error": "No news found 🫤"}

    # Save for context-aware follow-ups
    last_news_cache["topic"] = topic
    last_news_cache["raw_news"] = raw_news

    summary = generate_summary(raw_news, style)
    return {"topic": topic, "summary": summary}
