from groq import Groq
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)


def build_briefing(stocks: list[dict], news: dict) -> str:
    stock_text = _format_stocks_for_prompt(stocks)
    news_text = _format_news_for_prompt(news)

    prompt = f"""당신은 주식 시장 브리핑 전문가입니다. 아래 데이터를 바탕으로 간결하고 유용한 아침 브리핑을 작성해주세요.

## 주가 현황
{stock_text}

## 관련 뉴스
{news_text}

## 작성 지침
- 전체 길이: 카카오톡 메시지에 적합하게 500자 이내
- 구성: 주가 요약 → 주요 뉴스 핵심 → 오늘의 시사점
- 영문 기사는 한국어로 번역하여 요약
- 숫자는 구체적으로 표기
- 이모지 사용 가능 (가독성 향상)
- 말투: 간결하고 전문적으로
- 한자(漢字) 절대 사용 금지, 순수 한글로만 작성

브리핑을 작성해주세요:"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1024,
    )
    return response.choices[0].message.content


def _format_stocks_for_prompt(stocks: list[dict]) -> str:
    lines = []
    for s in stocks:
        if "error" in s:
            lines.append(f"{s['ticker']}: 데이터 오류")
            continue
        sign = "+" if s["change"] >= 0 else ""
        lines.append(
            f"{s['name']} ({s['ticker']}): ${s['current']} "
            f"({sign}{s['change_pct']}%)"
        )
    return "\n".join(lines)


def _format_news_for_prompt(news: dict) -> str:
    lines = []
    for ticker, data in news.items():
        lines.append(f"\n[{ticker} 국내 뉴스]")
        for article in data["korean"]:
            lines.append(f"- {article['title']}")

        lines.append(f"\n[{ticker} 해외 뉴스]")
        for article in data["foreign"]:
            lines.append(f"- {article['title']}")
    return "\n".join(lines)
