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



