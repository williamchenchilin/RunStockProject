# -*- coding: UTF-8 -*-
'''
******************************************************************
# 程式說明 : 主程式
# 程式型態 : 
# 備註     : 
#******************************************************************
# 日期          編輯人員              變更原因
# 2024/01/01    William              建立範本
# 2024/01/16    William              新增主要line程式
******************************************************************
'''
# ----------------------
# 載入程式必要工具
# ----------------------
import inspect
if not hasattr(inspect, 'getargspec'):
    inspect.getargspec = inspect.getfullargspec

from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, StickerSendMessage, ImageSendMessage, LocationSendMessage
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from flask import render_template
from apscheduler.schedulers.background import BackgroundScheduler


#import pyodbc
#import schedule
#import time

# ----------------------
# 設定程式運行
# ----------------------
app = Flask(__name__)

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
CAT = 'NKbDp9O6/M2EMnRFcOJcZjZfByb+7cPd3E1YPVm2BycjQ/yUhtyPEVDR9U3khmiFkeY7LhssAN+ucYQCczEye+7Fu+80dB+waO2DgxQO41I52NfooWS7UUKcsPmcnY6hYfkbvv1Q1YCI8+QUPKiyPgdB04t89/1O/w1cDnyilFU='
CS='c9031d7e26c12cf1388a8664bedfdf79'
line_bot_api = LineBotApi(CAT)
handler = WebhookHandler(CS)

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
'''
# Health Check Path
@app.route('/health', methods=['GET'])
def health_check():
    return 'OK', 200

@app.route("/")
def home():
    return render_template("home.html")'''
@app.route('/ping')
def ping():
    return jsonify({"status":"alive"}), 200

def keep_alive():
    try:
        response = requests.get(
            'https://stock-linebot.onrender.com/ping')
        if respond.status_code == 200:
            print("Keep-Alive request sent seccessfully.")
        else:
            print("Keep-Alive request sent faild.")
    except Exception as e:
        print(f"Error during Keep-Alive request:{e}")

schedueler = BackgroundScheduler()
scheduler.add_job(func=keep_alive, trigger="interval",munites = 13)
scheduler.stare()

@app.route("/callback", methods=['POST'])
def callback():
    # 取得 Line 訊息的 X-Line-Signature Header
    signature = request.headers['X-Line-Signature']

    # 取得 POST 資料
    body = request.get_data(as_text=True)

    # 記錄 LINE 的事件
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 獲取使用者相關資訊
    user_id      = event.source.user_id
    source_type  = event.source.type
    message_text = event.message.text
    #獲取profile資料
    user_profile = line_bot_api.get_profile(user_id)
    user_name = user_profile.display_name

    # 根據不同的使用者進行回覆
    if source_type == "user":
        #若回覆為數字
        if message_text.isdigit(): 
            int_message_text = f"HI,{user_name}! 您要查詢的股票代號為{message_text}"
            web_site = f"https://tw.stock.yahoo.com/quote/{message_text}.TW"
            response = requests.get(web_site)
            #若回覆為數字且正確解讀
            if response.status_code == 200:
                html = response.text
                soup = BeautifulSoup(html, 'html.parser')
                selected_span = soup.find_all('span', {'class' : 'C($c-icon) Fz(24px) Mend(20px)'})
                span = [span.get_text() for span in selected_span]
                compare_stock = "['"+str(message_text)+"']"
                #正確股票資訊
                if str(span) == compare_stock:
                    reply_text = f"{int_message_text},\n代號網址：{web_site}"
                else:
                    reply_text = f"找不到代碼：「{message_text}」的股票"
            else:
                reply_text = f"找不到代碼：{message_text}的股票"
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))
        else:
            reply_text = f"{user_name}好,「{message_text}」不是股票代號,請輸入正確代號~"
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))
'''    elif source_type == "group":
        reply_text = f"這是來自群組 {user_id} 的訊息: {message_text},訊息編號為{event.reply_token}"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))
    elif source_type == "room":
        reply_text = f"這是來自聊天室 {user_id} 的訊息: {message_text},訊息編號為{event.reply_token}"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))
'''

# ----------------------
# 主程式持續運行
# ----------------------
if __name__ == "__main__":
    app.run()
'''    while True:
        schedule.run_pending()
        time.sleep(1)'''
#https://ithelp.ithome.com.tw/articles/10331859?sc=rss.iron製作