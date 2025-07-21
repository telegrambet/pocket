from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()

def tarefa_exemplo():
    print("📌 Executando tarefa agendada...")

def start_schedulers(app):
    scheduler.add_job(tarefa_exemplo, 'interval', minutes=5)
    scheduler.start()
    print("⏰ Scheduler iniciado.")

def stop_bot():
    if scheduler.running:
        scheduler.shutdown()
        print("⛔ Bot pausado via scheduler.")

def restart_bot():
    if not scheduler.running:
        scheduler.start()
        print("✅ Bot reiniciado via scheduler.")
