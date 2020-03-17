# 引用 BlockingScheduler 類別
from apscheduler.schedulers.blocking import BlockingScheduler

# 創建一個 Scheduler 物件實例
sched = BlockingScheduler()

# decorator 設定 Scheduler 的類型和參數，例如 interval 間隔多久執行
@sched.scheduled_job('interval', seconds=1)
def timed_job():
    print('每 1 秒鐘執行一次程式工作區塊')

# decorator 設定 Scheduler 為 cron 固定每週週間 6pm. 執行此程式工作區塊（但要注意的是 heroku server 上的時區為 UTC+0，所以台灣時間會是再加約 8 小時，變成隔天凌晨 2 點）
@sched.scheduled_job('cron', day_of_week='mon-fri', hour=18)
def scheduled_job():
    print('每週週間 6 PM UTC+0，2 AM UTC+8. 執行此程式工作區塊')

# 開始執行
sched.start()