"""
주식 알람 - 매일 아침 자동 브리핑
실행: python main.py          → 스케줄러 시작 (백그라운드 유지)
실행: python main.py --now    → 즉시 1회 실행 (테스트용)
"""

import sys
import logging
from datetime import datetime
import pytz
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from config import STOCKS, ALARM_HOUR, ALARM_MINUTE
from modules.stock import get_all_stocks
from modules.news import fetch_all_news
from modules.ai_briefing import build_briefing
from modules.kakao import send_to_me

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)

KST = pytz.timezone("Asia/Seoul")


def run_briefing():
    now = datetime.now(KST).strftime("%Y-%m-%d %H:%M")
    log.info(f"브리핑 시작 — {now}")

    log.info(f"주가 수집: {STOCKS}")
    stocks = get_all_stocks(STOCKS)

    log.info("뉴스 수집 중...")
    news = fetch_all_news(STOCKS)

    log.info("AI 브리핑 생성 중...")
    briefing = build_briefing(stocks, news)

    header = f"📊 주식 브리핑 {now}\n{'─' * 30}\n"
    message = header + briefing

    log.info("카카오톡 전송 중...")
    success = send_to_me(message)

    if success:
        log.info("전송 완료!")
    else:
        log.error("카카오톡 전송 실패")
        print("\n[브리핑 내용]\n" + message)


if __name__ == "__main__":
    if "--now" in sys.argv:
        run_briefing()
    else:
        scheduler = BlockingScheduler(timezone=KST)
        scheduler.add_job(
            run_briefing,
            trigger=CronTrigger(hour=ALARM_HOUR, minute=ALARM_MINUTE, timezone=KST),
        )
        next_run = scheduler.get_jobs()[0].next_run_time
        log.info(f"스케줄러 시작 — 매일 {ALARM_HOUR:02d}:{ALARM_MINUTE:02d} KST 실행")
        log.info(f"다음 실행: {next_run}")
        log.info("종료하려면 Ctrl+C")
        try:
            scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            log.info("스케줄러 종료")
