from .scraping import save_news
from apscheduler.schedulers.background import BackgroundScheduler


def news_start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(save_news(), 'interval', hours=6)
    scheduler.start()
