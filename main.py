from apscheduler.schedulers.background import BackgroundScheduler
from TelegramBot import start_bot, stop_analysis, restart_analysis

if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    start_bot(scheduler)
    scheduler.start()
