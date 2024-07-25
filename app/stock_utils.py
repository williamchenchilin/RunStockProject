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

import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# ----------------------
# 設定程式運行
# ----------------------
def Upd_Stock_Url_Fx(url):
    '''
    更新股票 URL 功能，從 Yahoo 股票頁面提取股票分類和股票信息。
    
    :param url: 股票分類 URL
    :return: 股票信息字典列表
    '''
    # 參數處理
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        # A. 查找股票大分類
        pattern = r'<td class="c3"[^>]*><a href="([^"]+)"[^>]*>([^<]+)</a></td>'
        matches = re.findall(pattern, html)
        category_result_list = []

        for match in matches:
            link, text = match
            category_dict = {
                'Category': text,
                'url': urljoin(url, link)
            }
            category_result_list.append(category_dict)

        # B. 股票細分類
        stock_results = []
        for stock_nm in category_result_list:
            page_name = stock_nm['Category']
            page_url = stock_nm['url']

            # 開始抓取第二層資訊
            response2 = requests.get(page_url)
            if response2.status_code == 200:
                html2 = response2.text
                soup2 = BeautifulSoup(html2, 'html.parser')
                pattern2 = r"setid\('([^']+)',\s*'([^']+)'(?:\);)?"
                matches2 = re.finditer(pattern2, html2)

                for match2 in matches2:
                    stock_code = match2.group(1)
                    stock_name = match2.group(2)
                    stock_dict = {
                        'Category': page_name,
                        'url': page_url,
                        'stock_code': stock_code,
                        'stock_name': stock_name
                    }
                    stock_results.append(stock_dict)

        return stock_results

    else:
        print("股票查找網址無回應")
        return []

# 使用範例
# url = 'https://tw.stock.yahoo.com/h/kimosel.php?tse=1&cat=ETF&form=menu&form_id=stock_id&form_name=stock_name&domain=0'
# result = Upd_Stock_Url_Fx(url)
# print(result)
