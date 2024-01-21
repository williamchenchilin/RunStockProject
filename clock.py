from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('cron', day_of_week='mon-fri', minute='*/10')
def scheduled_job():
    url = "https://stock-linebot.onrender.com"
    conn = urllib.request.urlopen(url)
        
    for key, value in conn.getheaders():
        print(key, value)

sched.start()