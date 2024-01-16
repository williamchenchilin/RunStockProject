# -*- coding: UTF-8 -*-
'''
******************************************************************
# 程式說明 : 主程式
# 程式型態 : 
# 備註     : 
#******************************************************************
# 日期          編輯人員              變更原因
# 2024/01/01    William              初始版本
******************************************************************
'''
# ----------------------
# 載入程式必要工具
# ----------------------
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from datetime import datetime

import pyodbc
import schedule
import time

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
PARAM = PARAM if PARAM is not None else ''







# ----------------------
# 主程式持續運行
# ----------------------
if __name__ == "__main__":
    app.run(port=5000)
    while True:
        schedule.run_pending()
        time.sleep(1)