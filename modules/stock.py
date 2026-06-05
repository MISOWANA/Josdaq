import yfinance as yf
import pytz

KST = pytz.timezone("Asia/Seoul")


def get_stock_info(ticker: str) -> dict:
    stock = yf.Ticker(ticker)
    info = stock.info

    regular_close = info.get("regularMarketPrice") or info.get("previousClose")
    prev_close = info.get("regularMarketPreviousClose") or info.get("previousClose")

    if not regular_close or not prev_close:
        return {"ticker": ticker, "error": "데이터 없음"}

    change = regular_close - prev_close
    change_pct = (change / prev_close) * 100

    post_price = info.get("postMarketPrice")
    post_change_pct = info.get("postMarketChangePercent")

    short_pct = info.get("shortPercentOfFloat")
    short_ratio = info.get("shortRatio")

    result = {
        "ticker": ticker,
        "name": info.get("shortName", ticker),
        "regular_close": round(regular_close, 2),
        "prev_close": round(prev_close, 2),
        "change": round(change, 2),
        "change_pct": round(change_pct, 2),
        "short_pct": round(short_pct * 100, 2) if short_pct else None,
        "short_ratio": round(short_ratio, 1) if short_ratio else None,
    }

    if post_price:
        result["post_price"] = round(post_price, 2)
        result["post_change_pct"] = round(post_change_pct * 100, 2) if post_change_pct else None

    return result


def get_all_stocks(tickers: list[str]) -> list[dict]:
    results = []
    for ticker in tickers:
        try:
            results.append(get_stock_info(ticker))
        except Exception as e:
            results.append({"ticker": ticker, "error": str(e)})
    return results
