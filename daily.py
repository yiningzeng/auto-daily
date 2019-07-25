# -*- coding:utf-8 -*-
import datetime
from bs4 import BeautifulSoup
import requests
import os
import urllib
import sys
from wxpy import *
from apscheduler.schedulers.background import BackgroundScheduler

if __name__ == '__main__':

    print(sys.argv[1])
    bot = Bot(cache_path=True, console_qr=True)
    myself = bot.self

    is_reply = sys.argv[1]

    # 打印来自其他好友、群聊和公众号的消息
    @bot.register()
    def print_others(msg):
        global is_reply
        print(msg)
        if msg.is_at:
            os.system("notify-send '%s - %s' '%s' -t %d" % (msg.sender, msg.create_time, msg, 100000))
            pre = msg.member.name + " " + msg.member.display_name + ' @提醒: '
            msg.forward(bot.file_helper, prefix=pre)
            if is_reply == "1":
                return "收到👌"
        else:
            os.system("notify-send '%s - %s' '%s' -t %d" % (msg.sender, msg.create_time, msg, 10000))

    def create_daily():
        os.system('sh auto_create_daily.sh')
        # os.system('sh test.sh')
        print('Job-create_daily:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

    def push_daily():
        os.system('sh auto_push_daily.sh')
        bot.file_helper.send("已经push日志，如果已经填写，请忽略。20:30分准时发日报")
        # os.system('sh test.sh')
        print('Job-push_daily:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
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
        res = requests.get('https://github.com/yiningzeng/auto-daily/blob/master/' +
                           datetime.datetime.now().strftime('%Y-%m-%d') +
                           '/README.md')  # 获取目标网页
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
    scheduler.add_job(create_daily, 'cron', second="0", minute="5", hour="1", day_of_week="MON-SUN")
    scheduler.add_job(push_daily, 'cron', second="0", minute="5", hour="19", day_of_week="MON-SUN")
    # 调度方法为 timedTask，触发器选择 interval(间隔性)，间隔时长为 2 秒  0 15 10 ? * MON-FRI
    scheduler.add_job(send_daily, 'cron', second="0", minute="30", hour="20", day_of_week="MON-SAT")


    # 启动调度任务
    scheduler.start()
    bot.file_helper.send('runing:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    # 堵塞线程
    # embed()
    bot.join()