# -*- coding: UTF-8 -*-
'''
******************************************************************
# 程式說明 : 定時任務和排程處理
# 程式型態 : 
# 備註     : 
#******************************************************************
# 日期          編輯人員              變更原因
# 2024/01/29    William              initial
******************************************************************
'''

import requests
from apscheduler.schedulers.background import BackgroundScheduler

# 設定定時任務
def keep_alive():
    try:
        response = requests.get('https://your-app-name.onrender.com/ping')
        if response.status_code == 200:
            print("Keep-Alive request sent successfully.")
        else:
            print("Keep-Alive request failed.")
    except Exception as e:
        print(f"Error during Keep-Alive request: {e}")

# 創建Scheduler並添加任務
def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=keep_alive, trigger="interval", minutes=13)
    scheduler.start()
    print("Scheduler started.")
