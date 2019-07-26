# -*- coding:utf-8 -*-
import datetime
from bs4 import BeautifulSoup
import requests
import os
import urllib
import sys
import logging as log
from wxpy import *
from apscheduler.schedulers.background import BackgroundScheduler

if __name__ == '__main__':

    log.basicConfig(level=log.INFO,  # 控制台打印的日志级别
                        filename='wechat.log',
                        filemode='a',  ##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                        # a是追加模式，默认如果不写的话，就是追加模式
                        format=
                        '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                        # 日志格式
                        )


    bot = Bot(cache_path=True, console_qr=True)
    myself = bot.self

    is_reply = sys.argv[1]
    log.info("群聊@提醒开启状态：%s" % is_reply)

    # 打印来自其他好友、群聊和公众号的消息
    @bot.register()
    def print_others(msg):
        global is_reply
        log.info(msg)
        if msg.is_at:
            os.system("notify-send '%s - %s' '%s' -t %d" % (msg.sender, msg.create_time, msg, 100000))
            pre = msg.member.name + " " + msg.member.display_name + ' @提醒: '
            msg.forward(bot.file_helper, prefix=pre)
            if is_reply == "1":
                return "收到👌"
        else:
            os.system("notify-send '%s - %s' '%s' -t %d" % (msg.sender, msg.create_time, msg, 10000))

    def remind():
        i = 0
        while i < 20:
            os.system("notify-send '%s' '%s' -t %d" % ('写日报', '写日报', 100000))
            i = i + 1

    def create_daily():
        os.system('sh auto_create_daily.sh')
        log.info('Job-create_daily:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        # os.system('sh test.sh')
        # print('Job-create_daily:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

    def push_daily():
        os.system('sh auto_push_daily.sh')
        bot.file_helper.send("已经push日志，如果已经填写，请忽略。20:30分准时发日报")
        # os.system('sh test.sh')
        log.info('Job-push_daily:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        # print('Job-push_daily:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
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
        log.info('start > send_daily:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        # print('send_daily:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        # 机器人账号自身
        res = requests.get('https://github.com/yiningzeng/auto-daily/blob/master/' +
                           datetime.datetime.now().strftime('%Y-%m-%d') +
                           '/README.md')  # 获取目标网页
        soup = BeautifulSoup(res.text, 'html.parser')  # 爬取网页
        readme = soup.find(id="readme").text
        # 向文件传输助手发送消息
        bot.file_helper.send(readme)
        daily_group = ensure_one(bot.groups().search('轻蜓日报'))
        daily_group.send(readme)
        # groups = bot.groups(update=True, contact_only=True)
        # 查询群聊
        # my_group = ensure_one(bot.groups().search('日报'))
        # bot.file_helper.send('Hello from wxpy!')
        # my_group.send('发日报啦!')
        log.info('end > send_daily:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        log.info('------------------------------------------------------------------------')
        # print('send_daily:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        # print('------------------------------------------------------------------------')

    # 创建后台执行的 schedulers
    scheduler = BackgroundScheduler()
    # 添加调度任务

    # 提醒写日报
    scheduler.add_job(remind, 'cron', second="0", minute="40", hour="18", day_of_week="MON-SAT")

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