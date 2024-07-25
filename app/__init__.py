# -*- coding: UTF-8 -*-
'''
******************************************************************
# 程式說明 : Flask 應用程式初始化
# 程式型態 : 
# 備註     : 
#******************************************************************
# 日期          編輯人員              變更原因
# 2024/01/29    William              Initial
# 2024/07/25    William              添加藍圖註冊
******************************************************************
'''

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# 設定 SQLAlchemy
db = SQLAlchemy()

def create_app():
    # 初始化 Flask 應用程式
    app = Flask(__name__)
    
    # 載入環境變數
    load_dotenv()
    
    # 設定資料庫連結
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # 初始化 SQLAlchemy
    db.init_app(app)
    
    # 導入並註冊藍圖
    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    # 可以在這裡添加其他藍圖或擴展初始化代碼
    
    return app
