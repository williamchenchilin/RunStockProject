# -*- coding: UTF-8 -*-
'''
******************************************************************
# 程式說明 : 主程式
# 程式型態 : 
# 備註     : 
#******************************************************************
# 日期          編輯人員              變更原因
# 2024/01/29    William              initial
# 2024/07/25    William              更新以整合功能模塊
******************************************************************
'''

# ----------------------
# 載入程式必要工具
# ----------------------
#这段代码的目的是为了确保在 Python 版本较老的环境中，inspect 模块能够提供 getargspec 函数
import inspect
if not hasattr(inspect, 'getargspec'):
    inspect.getargspec = inspect.getfullargspec

# A. FLASK環境
from flask import Flask, request, abort, jsonify, redirect, url_for, Blueprint
from apscheduler.schedulers.background import BackgroundScheduler

# B. Line
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

# C. 爬網
import requests
from app.stock_utils import Upd_Stock_Url_Fx  # 导入股票更新函数
from app.api_clients import LineClient, YahooStockClient  # 导入 API 客户端
import os
from dotenv import load_dotenv

# D. SQL連結
from app.models import db, User

# ----------------------
# 設定程式運行
# ----------------------
app = Flask(__name__)
load_dotenv()

# 初始化 API 客户端
line_client = LineClient()
yahoo_stock_client = YahooStockClient()

# 設定SQLAlchemy連結資料庫
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# 定義藍圖
main = Blueprint('main', __name__)

# ------------------------------
# 定時維持Render服務器在線
# ------------------------------
@app.route('/ping')
def ping():
    return jsonify({"status": "alive"}), 200

def keep_alive():
    try:
        response = requests.get('https://your-app-name.onrender.com/ping')
        if response.status_code == 200:
            print("Keep-Alive request sent successfully.")
        else:
            print("Keep-Alive request failed.")
    except Exception as e:
        print(f"Error during Keep-Alive request: {e}")

scheduler = BackgroundScheduler()
scheduler.add_job(func=keep_alive, trigger="interval", minutes=13)
scheduler.start()

# ------------------------------
# 使用者資料管理
# ------------------------------
@main.route('/')
def index():
    users = User.query.all()
    users_list_html = [f"<li>{user.username}</li>" for user in users]
    return f"<ul>{''.join(users_list_html)}</ul>"

@main.route('/add/<username>')
def add_user(username):
    db.session.add(User(username=username))
    db.session.commit()
    return redirect(url_for("main.index"))

# ------------------------------
# LINE Bot Webhook處理
# ------------------------------
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        line_client.handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@line_client.handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    message_text = event.message.text
    user_profile = line_client.get_profile(user_id)
    user_name = user_profile.display_name

    reply_message = handle_text_message(line_client, event, message_text, user_name)
    line_client.reply_message(event.reply_token, reply_message)

# ----------------------
# 主程式持續運行
# ----------------------
if __name__ == "__main__":
    app.run()
