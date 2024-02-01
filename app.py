# -*- coding: UTF-8 -*-
'''
******************************************************************
# 程式說明 : 主程式
# 程式型態 : 
# 備註     : 
#******************************************************************
# 日期          編輯人員              變更原因
# 2024/01/29    William              initial
******************************************************************
'''
# ----------------------
# 載入程式必要工具
# ----------------------
#1.外部工具載入
import inspect
if not hasattr(inspect, 'getargspec'):
    inspect.getargspec = inspect.getfullargspec
  #A.FLASK環境
from flask import Flask, request, abort
from flask import render_template
from flask import jsonify
from flask import redirect, url_for
from flask_sqlalchemy import SQLAlchemy

  #B.Line
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, StickerSendMessage, ImageSendMessage, LocationSendMessage
from datetime import datetime
  #C.爬網
import requests
from bs4 import BeautifulSoup
  #D.排程
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
  #E.SQL連結
from dotenv import load_dotenv
import psycopg2
import os
from .extensions import db
from .routes import main
#2.引入副程式
  #A.Line自動回覆
from message import handle_text_message  


#import pyodbc
#import schedule
#import time

# ----------------------
# 設定程式運行
# ----------------------
app = Flask(__name__)
load_dotenv()
# ----------------------
# 搭配 SQL 功能變數設定
# ----------------------
# 以下變數與執行狀態相關
JOB_START_TIME = datetime.now()       # 程式起始時間
JOB_END_TIME = datetime               # 程式結束時間
SRC_TBLNM = 'ODS_LF_Associate'        # 來源 TABLE，範例：SourceTable1||SourceTable2。
TGT_TBLNM = 'LF_FB_Associate'        # 目的 TABLE，範例：TargetTable。
INS_CNT = 0                          # 新增資料筆數
UPD_CNT = 0                          # 更新資料筆數
DEL_CNT = 0                          # 刪除資料筆數

# 以下變數為功能程式內自訂變數
# ----------------------
# 宣告功能變數
# ----------------------
ErrorMessage = ''       # 錯誤訊息
ErrorSeverity = 0       # 錯誤嚴重程度
ErrorState = 0          # 錯誤狀態
#1.Line設定
CAT = 'NKbDp9O6/M2EMnRFcOJcZjZfByb+7cPd3E1YPVm2BycjQ/yUhtyPEVDR9U3khmiFkeY7LhssAN+ucYQCczEye+7Fu+80dB+waO2DgxQO41I52NfooWS7UUKcsPmcnY6hYfkbvv1Q1YCI8+QUPKiyPgdB04t89/1O/w1cDnyilFU='
CS='c9031d7e26c12cf1388a8664bedfdf79'
line_bot_api = LineBotApi(CAT)
handler = WebhookHandler(CS)
#2.資料庫設定
app.cofig["SQLALCHEMY_DATABASE_URI"]=os.environ.get("DATABASE_URL")
#postgres://william:OksYLIKWCizAXTr5nPG0g0DLddNMu8ql@dpg-cmm7880l5elc73ca9p50-a.singapore-postgres.render.com/runstock
db.init_app(app)
app.register_blueprint(main)

#3.股票整檔資訊來源
Upd_Stock_Url = "https://tw.stock.yahoo.com/h/kimosel.php?tse=1&cat=ETF&form=menu&form_id=stock_id&form_name=stock_name&domain=0"


# ------------------------------
# 設定必輸入變數
# ------------------------------
# 執行狀態
SRC_TBLNM = 'ODS_LF_Associate'  # 有多個 Source Table 時使用<||>分隔符號區分
TGT_TBLNM = 'LF_FB_Associate'  # 通常只會填一個 Target Table


# ------------------------------
# 設定變數
# ------------------------------
# 執行狀態
JOB_START_TIME = datetime.now()  # 程式起始時間
JOB_END_TIME = datetime          # 程式結束時間
INS_CNT = 0                     # 新增資料筆數
UPD_CNT = 0                     # 更新資料筆數
DEL_CNT = 0                     # 刪除資料筆數
# OUT 回傳值
PARAM = ''
PARAM = PARAM if PARAM is not None else ''
# ----------------------
# 程式開始
# ----------------------
#1.設定定時在Render自動啟動,製造不間斷狀態
@app.route('/ping')
def ping():
    return jsonify({"status":"alive"}), 200
def keep_alive():
    try:
        response = requests.get(
            'https://stock-linebot.onrender.com/ping')
        if response.status_code == 200:
            print("Keep-Alive request sent seccessfully.")
        else:
            print("Keep-Alive request sent faild.")
    except Exception as e:
        print(f"Error during Keep-Alive request:{e}")
scheduler = BackgroundScheduler()
scheduler.add_job(func = keep_alive, trigger = "interval", minutes = 13)
scheduler.start()

#2.設定PostgreSQL整檔資料
  #使用者加入資料庫
main = Blurprint(main,__name__)
@main.route('/')
def index():
    users = User.query.all()
    users_list_html = [f"<li>{ user.username }</li>"for user in users]
    return f"<ul>{''.join(users_list_html)}</ul>"
  #資料庫中的使用者
@main.route('add/<username>')
def add_user(username):
    db.session.add(User(username=username))
    db.session.commit()
    return redirect(url_for("main.index"))


#2-A.定時每天早上爬股票資料名稱(用於更新)
'''
Sql_scheduler = BackgroundScheduler()

Sql_scheduler.add_job(func=Upd_Stock_Url_Fx, trigger='cron', hour=8, minute=0,args=(Upd_Stock_Url))  # 每天早上 8:00 執行一次
Sql_scheduler.start()
    #B.股票資料資訊更新程式開始
    '''


#3.Line還沒決定要做甚麼
@app.route("/callback", methods=['POST'])
def callback():
    #A.取得 Line 訊息的 X-Line-Signature Header
    signature = request.headers['X-Line-Signature']
    #B.取得 POST 資料
    body = request.get_data(as_text=True)
    #C.記錄 LINE 的事件
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

#4.訊息回覆機制設定
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    #A.獲取使用者相關資訊
    user_id      = event.source.user_id
    source_type  = event.source.type
    message_text = event.message.text
    #B.獲取profile資料
    user_profile = line_bot_api.get_profile(user_id)
    user_name = user_profile.display_name

    #C.根據不同的使用者進行回覆
    if source_type == "user":
        reply_message = handle_text_message(line_bot_api, event, message_text, user_name)
        
        line_bot_api.reply_message(event.reply_token, reply_message)
 
 
# ----------------------
# 主程式持續運行
# ----------------------
if __name__ == "__main__":
    app.run()
#https://ithelp.ithome.com.tw/articles/10331859?sc=rss.iron製作