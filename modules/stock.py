import yfinance as yf
from datetime import datetime
import pytz

KST = pytz.timezone("Asia/Seoul")


def get_stock_info(ticker: str) -> dict:
    stock = yf.Ticker(ticker)
    info = stock.info
    hist = stock.history(period="2d")

    if hist.empty or len(hist) < 2:
        return {"ticker": ticker, "error": "데이터 없음"}

    prev_close = hist["Close"].iloc[-2]
    current = hist["Close"].iloc[-1]
    change = current - prev_close
    change_pct = (change / prev_close) * 100

    return {
        "ticker": ticker,
        "name": info.get("shortName", ticker),
        "current": round(current, 2),
        "prev_close": round(prev_close, 2),
        "change": round(change, 2),
        "change_pct": round(change_pct, 2),
        "volume": info.get("volume", 0),
        "market_cap": info.get("marketCap", 0),
    }


def get_all_stocks(tickers: list[str]) -> list[dict]:
    results = []
    for ticker in tickers:
        try:
            results.append(get_stock_info(ticker))
        except Exception as e:
            results.append({"ticker": ticker, "error": str(e)})
    return results


def format_stock_summary(stocks: list[dict]) -> str:
    lines = []
    for s in stocks:
        if "error" in s:
            lines.append(f"• {s['ticker']}: 오류 ({s['error']})")
            continue
        arrow = "▲" if s["change"] >= 0 else "▼"
        sign = "+" if s["change"] >= 0 else ""
        lines.append(
            f"• {s['name']} ({s['ticker']})\n"
            f"  ${s['current']} {arrow} {sign}{s['change']} ({sign}{s['change_pct']}%)"
        )
    return "\n".join(lines)
