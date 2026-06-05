import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL", "")

STOCKS = [s.strip() for s in os.getenv("STOCKS", "NVDA").split(",") if s.strip()]

ALARM_HOUR = int(os.getenv("ALARM_HOUR", "8"))
ALARM_MINUTE = int(os.getenv("ALARM_MINUTE", "0"))
