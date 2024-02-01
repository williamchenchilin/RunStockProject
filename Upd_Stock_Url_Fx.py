# -*- coding: UTF-8 -*-
'''
******************************************************************
# 程式說明 : Upd_Stock_Url_Fx
# 程式型態 : 
# 備註     : 
#******************************************************************
# 日期          編輯人員              變更原因
# 2024/01/29    William              Initial
******************************************************************
'''
# ----------------------
# 載入程式必要工具
# ----------------------
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
import datetime
import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from urllib.parse import urljoin
from flask import Flask, jsonify


#import pyodbc
#import schedule
#import time
'''
url = 'https://tw.stock.yahoo.com/h/kimosel.php?tse=1&cat=ETF&form=menu&form_id=stock_id&form_name=stock_name&domain=0'
response = requests.get(url)
html = response.text
soup = BeautifulSoup(html,'html.parser')
pattern = r'<td class="c3"[^>]*><a href="([^"]+)"[^>]*>([^<]+)</a></td>'
matches = re.findall(pattern, html)
result = ()
for match in matches:
    link, text = match
    result[text] = link

print(result)'''
# ----------------------
# 設定程式運行
# ----------------------
def Upd_Stock_Url_Fx(Url):
# ----------------------
# 搭配 SQL 功能變數設定
# ----------------------
# 以下變數與執行狀態相關
# 以下變數為功能程式內自訂變數
# ----------------------
# 宣告功能變數
# ----------------------
# ------------------------------
# 設定必輸入變數
# ------------------------------
# 執行狀態

# ------------------------------
# 設定變數
# ------------------------------
# 執行狀態

# ----------------------
# 程式開始
# ----------------------
#1.參數處理
    response = requests.get(Url)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        #A.yahoo查找股票大分類
        pattern = r'<td class="c3"[^>]*><a href="([^"]+)"[^>]*>([^<]+)</a></td>'#正則表達式
        matches = re.findall(pattern, html)
        Category_result_list = []

        for match in matches:
            link, text = match
            Category_dict = {'Category': text
                            ,'url'     : urljoin(url, link)
                             }
            Category_result_list.append(Category_dict)   
        #B. 股票細分類 
        for Stock_Nm in Category_result_list:
            page_name = Stock_Nm['Category']
            page_url  = Stock_Nm['url']
            #開始爬取得第二層資訊
            response2 = requests.get(page_url)
            html2 = response2.text
            soup2 = BeautifulSoup(html2,'html.parser')
            pattern2 = r"setid\('([^']+)',\s*'([^']+)'(?:\);)?"
            matches2 = re.finditer(pattern2, html2)
            Stock_Result_List = []
            for match2 in matches2:
                stock_code = match2.group(1)
                stock_name = match2.group(2)
                Stock_dict =  {'Category'   :page_name
                              ,'url'        :page_url
                              ,'stock_code' :stock_code
                              ,'stock_name' :stock_name
                                }
                print(Reply_Message)
                return Stock_dict
    else:
         Reply_Message = "股票查找網址無回應"
         print(Reply_Message)


    DATABASE_URL = os.environ.get('postgres://william:OksYLIKWCizAXTr5nPG0g0DLddNMu8ql@dpg-cmm7880l5elc73ca9p50-a/runstock')

    if DATABASE_URL is None:
        print("DATABASE_URL environment variable is not set")

    conn = None
    try:
        url = urlparse(DATABASE_URL)
        conn = psycopg2.connect(
               dbname='runstock',
               user=url.username,
               password=url.password,
               host=url.hostname,
               port=url.port
        )
            # 測試連接是否成功
        cur = conn.cursor()
        cur.execute("SELECT version()")
        version = cur.fetchone()
        print("Connected to the database. PostgreSQL version:", version)

    # 在這裡添加其他測試操作

    except psycopg2.Error as e:
        print("Unable to connect to the database:", e)

    finally:
    # 無論是否連接成功都關閉連接
        if conn is not None:
            cur.close()
            conn.close()
    conn = psycopg2.connect(DATABASE_URL)


    cur = conn.cursor()


    for stock_data in Stock_Result_List:
        cur.execute('''
            INSERT INTO Lf_Stock_Var 
                        (Category, url, stock_code, stock_name, Src_Dt)
                    VALUES 
                        (%s, %s, %s, %s ,now())
                      '''
                      , (stock_data['Category']
                       , stock_data['url']
                       , stock_data['stock_code']
                       , stock_data['stock_name']))

    # 提交更改
    conn.commit()

    # 关闭连接
    cur.close()
    conn.close()

        # 將資訊存入 PostgreSQL
        #with Session() as session:
            # 使用 SQLAlchemy 將資料寫入 PostgreSQL
            # ...
            
        #current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #print(f"定時任務執行成功，時間：{current_time}")

# OUT 回傳值
    return ('完成本次更新')
