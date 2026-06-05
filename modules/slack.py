import requests
import os

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL", "")


def send_message(message: str) -> bool:
    if not SLACK_WEBHOOK_URL:
        raise ValueError("SLACK_WEBHOOK_URL이 설정되지 않았습니다.")
    res = requests.post(SLACK_WEBHOOK_URL, json={"text": message})
    if not res.ok:
        raise RuntimeError(f"Slack 전송 실패: {res.status_code} {res.text}")
    return True
