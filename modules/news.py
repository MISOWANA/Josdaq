import feedparser
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote


def fetch_korean_news(query: str, max_items: int = 3) -> list[dict]:
    """네이버 뉴스 RSS로 국내 기사 수집"""
    encoded = quote(query)
    url = f"https://news.google.com/rss/search?q={encoded}&hl=ko&gl=KR&ceid=KR:ko"
    feed = feedparser.parse(url)

    articles = []
    for entry in feed.entries[:max_items]:
        articles.append({
            "title": entry.get("title", ""),
            "link": entry.get("link", ""),
            "published": entry.get("published", ""),
            "summary": entry.get("summary", ""),
            "lang": "ko",
        })
    return articles


def fetch_foreign_news(query: str, max_items: int = 3) -> list[dict]:
    """Google News RSS로 영문 기사 수집"""
    encoded = quote(query)
    url = f"https://news.google.com/rss/search?q={encoded}&hl=en&gl=US&ceid=US:en"
    feed = feedparser.parse(url)

    articles = []
    for entry in feed.entries[:max_items]:
        articles.append({
            "title": entry.get("title", ""),
            "link": entry.get("link", ""),
            "published": entry.get("published", ""),
            "summary": entry.get("summary", ""),
            "lang": "en",
        })
    return articles


def fetch_all_news(tickers: list[str]) -> dict:
    """종목별 국내·해외 뉴스 수집"""
    result = {}
    for ticker in tickers:
        result[ticker] = {
            "korean": fetch_korean_news(ticker),
            "foreign": fetch_foreign_news(ticker),
        }
    return result
