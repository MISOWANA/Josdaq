"""
카카오 인증 토큰 최초 발급 스크립트
한 번만 실행하면 됩니다.

사용법:
  1. .env 파일에 KAKAO_REST_API_KEY 입력
  2. 카카오 개발자 콘솔에서 리다이렉트 URI를 http://localhost 로 설정
  3. python kakao_auth.py 실행
  4. 출력된 URL을 브라우저에서 열고 로그인
  5. 리다이렉트된 URL에서 code= 값을 복사해 붙여넣기
"""

import requests
import os
from dotenv import load_dotenv

load_dotenv()

REST_API_KEY = os.getenv("KAKAO_REST_API_KEY", "")
CLIENT_SECRET = os.getenv("KAKAO_CLIENT_SECRET", "")
REDIRECT_URI = "http://localhost"


def get_auth_code():
    auth_url = (
        f"https://kauth.kakao.com/oauth/authorize"
        f"?client_id={REST_API_KEY}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=talk_message"
    )
    print("=" * 60)
    print("아래 URL을 브라우저에서 열고 카카오 로그인 후")
    print("리다이렉트된 주소창의 URL 전체를 복사하세요.\n")
    print(auth_url)
    print("=" * 60)
    redirected = input("\n리다이렉트된 URL 또는 code 값 입력: ").strip()

    if "code=" in redirected:
        code = redirected.split("code=")[1].split("&")[0]
    else:
        code = redirected
    return code


def exchange_code_for_tokens(code: str):
    url = "https://kauth.kakao.com/oauth/token"
    data = {
        "grant_type": "authorization_code",
        "client_id": REST_API_KEY,
        "redirect_uri": REDIRECT_URI,
        "code": code,
    }
    if CLIENT_SECRET:
        data["client_secret"] = CLIENT_SECRET
    res = requests.post(url, data=data)
    if not res.ok:
        print(f"\n카카오 오류 응답: {res.status_code}")
        print(res.json())
        res.raise_for_status()
    return res.json()


def save_to_env(refresh_token: str):
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    lines = []
    found = False
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        for i, line in enumerate(lines):
            if line.startswith("KAKAO_REFRESH_TOKEN="):
                lines[i] = f"KAKAO_REFRESH_TOKEN={refresh_token}\n"
                found = True
                break
    if not found:
        lines.append(f"KAKAO_REFRESH_TOKEN={refresh_token}\n")
    with open(env_path, "w", encoding="utf-8") as f:
        f.writelines(lines)
    print(f"\n.env 파일에 KAKAO_REFRESH_TOKEN 저장 완료!")


if __name__ == "__main__":
    if not REST_API_KEY or REST_API_KEY == "...":
        print("오류: .env 파일에 KAKAO_REST_API_KEY를 먼저 입력해주세요.")
        exit(1)

    code = get_auth_code()
    tokens = exchange_code_for_tokens(code)
    print(f"\n액세스 토큰: {tokens.get('access_token', '')[:20]}...")
    print(f"리프레시 토큰: {tokens.get('refresh_token', '')[:20]}...")
    save_to_env(tokens["refresh_token"])
    print("\n인증 완료! 이제 main.py를 실행할 수 있습니다.")
