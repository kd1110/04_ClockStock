import requests
from bs4 import BeautifulSoup
# 引用 BlockingScheduler 類別
from apscheduler.schedulers.blocking import BlockingScheduler

# 創建一個 Scheduler 物件實例
sched = BlockingScheduler()

def crawl_for_stock_price():
    url = 'https://goodinfo.tw/StockInfo/ShowK_ChartFlow.asp?RPT_CAT=PER&STOCK_ID=2412&CHT_CAT=YEAR'

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    }

    resp = requests.get(url, headers=headers)
    resp.encoding = 'utf-8'
    # 根據 HTTP header 的編碼解碼後的內容資料（ex. UTF-8）
    raw_html = resp.text

    # PE Ratio 簡寫 per
    soup = BeautifulSoup(raw_html, 'html.parser')
    per_rows = []
    eps_rows = []
    # 使用選擇器選取最近五年，CSS 選擇器 id #row 從第 0 開始到 5
    for row_line in range(0, 5):
        # 取出 td 標籤內的 EPS（在 index 4） text 取值
        eps_rows.append(soup.select(f'#row{row_line} td')[4].text)
        # 取出 td 標籤內的 PER 本益比（在 index 5） text 取值
        per_rows.append(soup.select(f'#row{row_line} td')[5].text)

    # 取出最高 EPS 和最低 EPS
    max_eps = max(eps_rows)
    min_eps = min(eps_rows)
    # 取出最高本益比和最低本益比
    max_per = max(per_rows)
    min_per = min(per_rows)

    print('max_eps', max_eps)
    print('min_eps', min_eps)


    print('max_per', max_per)
    print('min_per', min_per)

    """
    max_eps 5.16
    min_eps 4.3
    max_per 25.58
    min_per 19.67
    """

# decorator 設定 Scheduler 的類型和參數，例如 interval 間隔多久執行
@sched.scheduled_job('interval', minutes=5)
def timed_job():
    # 要注意不要太頻繁抓取
    print('每 5 分鐘執行一次程式工作區塊')
    crawl_for_stock_price()

# 開始執行
sched.start()