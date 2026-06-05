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
- [언어 규칙 - 반드시 준수] 출력 텍스트는 순수 한글, 영문, 숫자, 특수문자만 사용하세요. 한자(漢字)는 단 한 글자도 사용 금지입니다. 株, 価, 場, 証, 業, 率, 益, 損, 額, 高, 低, 落, 騰 등 어떤 한자도 절대 출력하지 마세요. 한자가 필요한 단어는 반드시 한글로 바꿔 쓰세요.

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
        line = (
            f"{s['name']} ({s['ticker']}): "
            f"정규장 종가 ${s['regular_close']} ({sign}{s['change_pct']}%)"
        )
        if s.get("post_price"):
            post_sign = "+" if (s.get("post_change_pct") or 0) >= 0 else ""
            post_info = f"  애프터 현재가 ${s['post_price']}"
            if s.get("post_change_pct") is not None:
                post_info += f" ({post_sign}{s['post_change_pct']}%)"
            line += f"\n{post_info}"
        lines.append(line)
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
