from groq import Groq
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)


def build_briefing(stocks: list[dict], news: dict) -> str:
    stock_text = _format_stocks_for_prompt(stocks)
    news_text = _format_news_for_prompt(news)

    prompt = f"""당신은 전문 주식 시장 브리핑 애널리스트입니다. 아래 데이터를 분석하여 투자자를 위한 아침 브리핑을 작성하세요.

[언어 규칙 - 최우선 준수사항]
출력은 반드시 순수 한글, 영문, 숫자, 특수문자만 사용합니다.
한자(漢字)는 단 한 글자도 절대 금지입니다. 株, 価, 場, 証, 率, 益, 損, 額, 高, 低, 落, 騰, 業, 財, 産, 資, 金, 市 등 모든 한자 출력 불가.
한자 대신 반드시 순수 한글 단어를 사용하세요.

[주가 데이터]
{stock_text}

[관련 뉴스]
{news_text}

[출력 형식 - 반드시 아래 구조를 그대로 사용하세요]

*📈 종목 현황*
(각 종목마다 아래 항목을 포함)
• 종목명 (티커)
  - 정규장 종가: $X.XX  전일 대비 ▲/▼ X.XX%
  - 애프터장 현재가: $X.XX  ▲/▼ X.XX%  (데이터 없으면 생략)
  - 공매도 비율: X.X%  (데이터 없으면 생략)
  - 한 줄 코멘트: 오늘 주가 움직임의 핵심 원인 한 문장

*📰 뉴스 요약*
(종목별 핵심 뉴스 1~2개, 영문은 한국어로 번역 요약)
• [종목] 뉴스 내용 요약

*💡 시사점*
전체 흐름과 내일 주목할 포인트를 2~3문장으로 작성

[작성 규칙]
- 전체 800자 이내로 Slack 메시지에 최적화
- 수치는 반드시 구체적으로 (소수점 2자리)
- 추측이나 불확실한 내용은 제외, 데이터 기반으로만 작성
- 말투: 간결하고 전문적"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1500,
    )
    return response.choices[0].message.content


def _format_stocks_for_prompt(stocks: list[dict]) -> str:
    lines = []
    for s in stocks:
        if "error" in s:
            lines.append(f"• {s['ticker']}: 데이터 오류")
            continue

        sign = "+" if s["change"] >= 0 else ""
        lines.append(f"• {s['name']} ({s['ticker']})")
        lines.append(f"  정규장 종가: ${s['regular_close']}  전일 대비 {sign}{s['change_pct']}% ({sign}${s['change']})")

        if s.get("post_price"):
            post_sign = "+" if (s.get("post_change_pct") or 0) >= 0 else ""
            post_line = f"  애프터장 현재가: ${s['post_price']}"
            if s.get("post_change_pct") is not None:
                post_line += f"  {post_sign}{s['post_change_pct']}%"
            lines.append(post_line)

        if s.get("short_pct") is not None:
            lines.append(f"  공매도 비율: {s['short_pct']}%  (숏 커버일: {s.get('short_ratio', 'N/A')}일)")

    return "\n".join(lines)


def _format_news_for_prompt(news: dict) -> str:
    lines = []
    for ticker, data in news.items():
        if data["korean"]:
            lines.append(f"\n[{ticker} 국내 뉴스]")
            for article in data["korean"]:
                lines.append(f"- {article['title']}")
        if data["foreign"]:
            lines.append(f"\n[{ticker} 해외 뉴스]")
            for article in data["foreign"]:
                lines.append(f"- {article['title']}")
    return "\n".join(lines)
