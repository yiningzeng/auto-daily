# -*- coding:utf-8 -*-
# !/usr/bin/env python

from wxpy import *

# 可加入腾讯智能闲聊 https://ai.qq.com/product/nlpchat.shtml
# 参考接口
if __name__ == '__main__':
    bot = Bot(cache_path=True, console_qr=True)


    # 定义需要检测的操作
    def action():
        bot.file_helper.send()


    # 执行检测
    # result = detect_freq_limit(action)
    # 查看结果
    # print(result)
    # 限制次数, 限制周期(秒数)
    # (27, 5.388065576553345)

    # 机器人账号自身
    myself = bot.self
    # 查询朋友
    my_friends = bot.friends().search('wutuo')
    # 确保搜索结果是唯一的，并取出唯一结果
    one_friend = ensure_one(my_friends)

    one_friend.send('Hello, WeChat!')

    groups = bot.groups(update=True, contact_only=True)
    # 查询群聊
    my_group = ensure_one(groups)
    # 向文件传输助手发送消息
    bot.file_helper.send('私人助理启动啦!')
    bot.file_helper.send('https://wxpy.readthedocs.io/zh/latest/chats.html')

    my_group.send('Hello, WeChat!')

    # 打印来自其他好友、群聊和公众号的消息
    @bot.register()
    def print_others(msg):
        print(msg)

    # 回复 my_friend 的消息 (优先匹配后注册的函数!)
    @bot.register()
    def reply_my_friend(msg):
        return 'received: {} ({})'.format(msg.text, msg.type)

    @bot.register(my_group)
    def auto_reply(msg):
        # 如果是群聊，但没有被 @，则不回复
        if isinstance(msg.chat, my_group) and not msg.is_at:
            return '收到消息: {} ({})'.format(msg.text, msg.type)
        else:
            # 回复消息内容和类型
            return '收到消息: {} ({})'.format(msg.text, msg.type)

    # 自动接受新的好友请求
    @bot.register(msg_types=FRIENDS)
    def auto_accept_friends(msg):
        # 接受好友请求
        new_friend = msg.card.accept()
        # 向新的好友发送消息
        new_friend.send('哈哈，我自动接受了你的好友请求')


    # 定位公司群
    company_group = ensure_one(bot.groups().search('小柠檬'))

    # 定位老板
    boss = ensure_one(company_group.search('wutuo'))


    # # 将老板的消息转发到文件传输助手
    # @bot.register(company_group)
    # def forward_boss_message(msg):
    #     if msg.member == boss:
    #         msg.forward(bot.file_helper, prefix='老板发言')


    # 堵塞线程
    embed()


    # 堵塞进程，直到结束消息监听 (例如，机器人被登出时)
    # bot.join()
