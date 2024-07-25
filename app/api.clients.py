# -*- coding: UTF-8 -*-
'''
******************************************************************
# 程式說明 : 外部 API 客戶端
# 程式型態 : 
# 備註     : 
#******************************************************************
# 日期          編輯人員              變更原因
# 2024/01/29    William              Initial
******************************************************************
'''

import os
import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage

# ------------------------------
# LINE API 客戶端
# ------------------------------
class LineClient:
    def __init__(self):
        self.line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
        self.handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))

    def get_profile(self, user_id):
        return self.line_bot_api.get_profile(user_id)

    def reply_message(self, reply_token, message):
        self.line_bot_api.reply_message(reply_token, message)

# ------------------------------
# Yahoo 股票數據 API 客戶端
# ------------------------------
class YahooStockClient:
    def __init__(self):
        self.base_url = "https://tw.stock.yahoo.com"

    def fetch_stock_info(self, stock_code):
        url = f"{self.base_url}/quote/{stock_code}.TW"
        response = requests.get(url)
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            span_elements = soup.find_all('span', {'class': 'C($c-icon) Fz(24px) Mend(20px)'})
            return [span.get_text() for span in span_elements]
        return []

    def get_stock_data(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            pattern = r'<td class="c3"[^>]*><a href="([^"]+)"[^>]*>([^<]+)</a></td>'
            matches = re.findall(pattern, html)
            return [{'Category': text, 'url': urljoin(self.base_url, link)} for link, text in matches]
        return []
