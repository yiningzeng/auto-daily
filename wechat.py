# -*- coding:utf-8 -*-
# !/usr/bin/env python

from wxpy import *

# 可加入腾讯智能闲聊 https://ai.qq.com/product/nlpchat.shtml
# 参考接口
if __name__ == '__main__':
    bot = Bot(cache_path=True, console_qr=True)

    # 机器人账号自身
    myself = bot.self

    # 向文件传输助手发送消息
    bot.file_helper.send('Hello from wxpy!')

    # 打印来自其他好友、群聊和公众号的消息
    @bot.register()
    def print_others(msg):
        print(msg)

    # 回复 my_friend 的消息 (优先匹配后注册的函数!)
    @bot.register()
    def reply_my_friend(msg):
        return 'received: {} ({})'.format(msg.text, msg.type)

    # 自动接受新的好友请求
    @bot.register(msg_types=FRIENDS)
    def auto_accept_friends(msg):
        # 接受好友请求
        new_friend = msg.card.accept()
        # 向新的好友发送消息
        new_friend.send('哈哈，我自动接受了你的好友请求')

    # 堵塞线程
    embed()