import requests
import os
from config import KAKAO_REST_API_KEY, KAKAO_REFRESH_TOKEN
KAKAO_CLIENT_SECRET = os.getenv("KAKAO_CLIENT_SECRET", "")


def refresh_access_token() -> str:
    """리프레시 토큰으로 액세스 토큰 갱신"""
    url = "https://kauth.kakao.com/oauth/token"
    data = {
        "grant_type": "refresh_token",
        "client_id": KAKAO_REST_API_KEY,
        "refresh_token": KAKAO_REFRESH_TOKEN,
    }
    if KAKAO_CLIENT_SECRET:
        data["client_secret"] = KAKAO_CLIENT_SECRET
    res = requests.post(url, data=data)
    if not res.ok:
        print(f"카카오 토큰 갱신 실패: {res.status_code} {res.json()}")
        res.raise_for_status()
    token_data = res.json()

    # 새 리프레시 토큰이 발급되면 .env 업데이트
    if "refresh_token" in token_data:
        _update_env("KAKAO_REFRESH_TOKEN", token_data["refresh_token"])

    return token_data["access_token"]


def send_to_me(message: str) -> bool:
    """나에게 카카오톡 메시지 전송"""
    access_token = refresh_access_token()

    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {
        "template_object": str({
            "object_type": "text",
            "text": message,
            "link": {"web_url": "", "mobile_web_url": ""},
        }).replace("'", '"')
    }

    res = requests.post(url, headers=headers, data=data)
    if res.status_code == 200:
        return True
    else:
        print(f"카카오 전송 실패: {res.status_code} {res.text}")
        return False


def _update_env(key: str, value: str):
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
    lines = []
    found = False
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        for i, line in enumerate(lines):
            if line.startswith(f"{key}="):
                lines[i] = f"{key}={value}\n"
                found = True
                break
    if not found:
        lines.append(f"{key}={value}\n")
    with open(env_path, "w", encoding="utf-8") as f:
        f.writelines(lines)
