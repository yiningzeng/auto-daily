# -*- coding:utf-8 -*-
import datetime
from bs4 import BeautifulSoup
import requests
import os
import urllib
from wxpy import *
from apscheduler.schedulers.background import BackgroundScheduler

if __name__ == '__main__':
    bot = Bot(cache_path=True, console_qr=True)

    def create_daily():
        os.system('sh auto_create_daily.sh')
        # os.system('sh test.sh')
        print('Job1-create_daily:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        """
        echo "# -" >> README.md
        git init
        git add README.md
        git commit -m "first commit"
        git remote add origin https://github.com/yiningzeng/-.git
        git push -u origin master
        :return: 
        """
    def send_daily():
        print('send_daily:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        # 机器人账号自身
        myself = bot.self

        res = requests.get('https://github.com/yiningzeng/auto-daily/blob/master/' +
                           datetime.datetime.now().strftime('%Y-%m-%d') +
                           '/007.md')  # 获取目标网页
        soup = BeautifulSoup(res.text, 'html.parser')  # 爬取网页
        readme = soup.find(id="readme").text
        # 向文件传输助手发送消息
        bot.file_helper.send(readme)
        # groups = bot.groups(update=True, contact_only=True)
        # 查询群聊
        # my_group = ensure_one(bot.groups().search('日报'))
        # bot.file_helper.send('Hello from wxpy!')
        # my_group.send('发日报啦!')
        print('send_daily:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        print('------------------------------------------------------------------------')

    # 创建后台执行的 schedulers
    scheduler = BackgroundScheduler()
    # 添加调度任务
    # 调度方法为 timedTask，触发器选择 interval(间隔性)，间隔时长为 2 秒  0 15 10 ? * MON-FRI
    scheduler.add_job(send_daily, 'cron', second="0", minute="0", hour="18", day_of_week="MON-SAT")

    scheduler.add_job(create_daily, 'cron', second="0", minute="5", hour="1", day_of_week="MON-SUN")
    # 启动调度任务
    scheduler.start()
    bot.file_helper.send('小秘书已启动')
    # 堵塞线程
    # embed()
    bot.join()