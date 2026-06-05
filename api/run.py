import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from http.server import BaseHTTPRequestHandler
from datetime import datetime
import pytz

from config import STOCKS
from modules.stock import get_all_stocks
from modules.news import fetch_all_news
from modules.ai_briefing import build_briefing
from modules.kakao import send_to_me

KST = pytz.timezone("Asia/Seoul")


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            now = datetime.now(KST).strftime("%Y-%m-%d %H:%M")
            stocks = get_all_stocks(STOCKS)
            news = fetch_all_news(STOCKS)
            briefing = build_briefing(stocks, news)
            message = f"📊 주식 브리핑 {now}\n{'─' * 30}\n{briefing}"
            send_to_me(message)

            self.send_response(200)
            self.send_header("Content-type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write("OK".encode())
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(str(e).encode())

    def log_message(self, format, *args):
        pass
