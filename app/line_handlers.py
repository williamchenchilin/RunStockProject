# -*- coding: UTF-8 -*-
'''
******************************************************************
# 程式說明 : Handle_Text_Message
# 程式型態 : 
# 備註     : 
#******************************************************************
# 日期          編輯人員              變更原因
# 2024/01/01    William              建立範本
# 2024/01/16    William              新增主要line程式
# 2024/01/29    William              新增主要副程式
******************************************************************
'''

import requests
from bs4 import BeautifulSoup
from linebot.models import TextSendMessage

def handle_text_message(line_bot_api, event, message_text, user_name):
    '''
    處理文本消息，查詢股票資訊或返回錯誤信息
    '''
    # 若回覆為數字
    if message_text.isdigit():
        int_message_text = f"HI,{user_name}! 您要查詢的股票代號為{message_text}"
        web_site = f"https://tw.stock.yahoo.com/quote/{message_text}.TW"
        response = requests.get(web_site)
        # 若回覆為數字且正確解讀
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            selected_span = soup.find_all('span', {'class': 'C($c-icon) Fz(24px) Mend(20px)'})
            span = [span.get_text() for span in selected_span]
            compare_stock = "['" + str(message_text) + "']"
            # 正確股票資訊
            if str(span) == compare_stock:
                reply_text = f"{int_message_text},\n代號網址：{web_site}"
            else:
                reply_text = f"找不到代碼：「{message_text}」的股票"
        else:
            reply_text = f"找不到代碼：{message_text}的股票"
    else:
        reply_text = f"{user_name}好,「{message_text}」不是股票代號,請輸入正確代號~"

    # 返回的消息
    return TextSendMessage(text=reply_text)
