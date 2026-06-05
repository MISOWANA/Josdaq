# 주식 알람 브리핑

매일 아침 해외 주가 + 국내/해외 뉴스를 Claude AI가 요약해서 카카오톡으로 전송합니다.

## 구조

```
Alam/
├── main.py              # 메인 실행 파일 (스케줄러)
├── kakao_auth.py        # 카카오 인증 토큰 발급 (최초 1회)
├── config.py            # 환경변수 로드
├── .env                 # API 키 설정 (직접 생성)
├── .env.example         # .env 템플릿
├── requirements.txt     # 패키지 목록
└── modules/
    ├── stock.py         # 주가 수집 (yfinance)
    ├── news.py          # 뉴스 수집 (Google News RSS)
    ├── ai_briefing.py   # Claude AI 브리핑 생성
    └── kakao.py         # 카카오톡 전송
```

## 설치 및 설정

### 1. 패키지 설치
```
pip install -r requirements.txt
```

### 2. .env 파일 생성
`.env.example`을 복사해서 `.env`로 저장 후 값 입력:
```
ANTHROPIC_API_KEY=sk-ant-...
KAKAO_REST_API_KEY=...
STOCKS=NVDA,AAPL,TSLA
ALARM_HOUR=8
ALARM_MINUTE=0
```

### 3. API 키 발급

**Anthropic API 키**
- https://console.anthropic.com → API Keys → Create Key

**카카오 REST API 키**
- https://developers.kakao.com → 내 애플리케이션 → 앱 추가
- 앱 이름 자유 입력 → 생성 후 **REST API 키** 복사
- 카카오 로그인 → 활성화
- 리다이렉트 URI: `http://localhost` 추가
- 동의항목: `카카오톡 메시지 전송` 체크

### 4. 카카오 인증 (최초 1회)
```
python kakao_auth.py
```
출력된 URL을 브라우저에서 열고 로그인 → 리다이렉트 URL 붙여넣기

### 5. 테스트 실행
```
python main.py --now
```

### 6. 스케줄러 시작 (매일 아침 자동 실행)
```
python main.py
```

## 종목 변경
`.env` 파일에서 `STOCKS` 값 수정:
```
STOCKS=NVDA,MSFT,AMZN,GOOGL
```
