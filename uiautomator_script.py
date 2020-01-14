import json
import redis
import uiautomator2 as u2
import time


class Auto(object):

    def __init__(self):
        self.d = u2.connect_usb('UHESY7W6NH')
        self.d.app_start('com.ss.android.ugc.aweme')

    def swipe_up(self):
        self.d(scrollable=True).scroll(steps=30)

    def swipe_down(self):
        self.d(scrollable=True).scroll.vert.backward()

    def swipe_left(self):
        self.d(scrollable=True).scroll.horiz.forward(steps=60)

    def swipe_right(self):
        self.d(scrollable=True).scroll.horiz.backward(steps=50)

    def search_return_index(self):
        # 返回首页推荐页面
        time.sleep(3)
        self.d.click(0.046, 0.056)
        time.sleep(1)
        self.d.click(0.951, 0.048)
        time.sleep(1)
        self.d.click(0.951, 0.048)

    def star(self):
        self.d.click(0.944, 0.616)

    def get_comment(self):
        """获取评论"""
        self.d.click(0.949, 0.693)
        self.d(scrollable=True).scroll.toEnd(60)
        self.d.click(0.463, 0.217)

    def comment(self, content):
        """
        @param content: 评论内容
        """
        # 获取视频的评论数
        like_count = self.d(resourceId='com.ss.android.ugc.aweme:id/ac5').get_text()
        time.sleep(1)
        self.d.click(0.949, 0.693)
        time.sleep(1)
        # 评论数为0直接跳出评论框，不为0需再次点击评论
        if like_count != '0':
            self.d.click(0.135, 0.922)
        time.sleep(1)
        self.d(resourceId='com.ss.android.ugc.aweme:id/a1b').send_keys(content)
        self.d(resourceId='com.ss.android.ugc.aweme:id/a1r').click()
        time.sleep(1)
        # 关闭评论
        self.d.click(0.463, 0.217)

    def search(self, keyword, category, aweme_id=None):
        """
        @param keyword: 搜索的关键字
        @param category: 搜索的类别
        @param aweme_id: 如搜索视频，需要视频id
        """
        # 打开搜索页面
        self.d.click(0.97, 0.051)
        self.d(resourceId='com.ss.android.ugc.aweme:id/ahw').send_keys(keyword)
        self.d.click(0.954, 0.77)
        if category == 0:
            # 综合搜索
            print('综合搜索')
        else:
            # 划到对应的搜索类别
            time.sleep(2)
            for _ in range(category):
                time.sleep(1)
                self.d.swipe(0.833, 0.483, 0.205, 0.487)
            time.sleep(3)
        # 视频搜索
        if category == 1:
            # 进入搜索的视频
            self.d.click(0.236, 0.323)
            self.search_return_index()
        # 用户搜索
        if category == 2:
            self.d.click(0.333, 0.157)
        # 话题搜索
        if category == 4:
            # 进入搜索的话题
            time.sleep(3)
            el = self.d(resourceId="com.ss.android.ugc.aweme:id/eiu", text=keyword)
            el.click()
            self.d(scrollable=True).scroll.toEnd(60)
            self.search_return_index()


auto = Auto()
keyword = '新年许心愿赢新衣'
coon = redis.Redis(host='127.0.0.1', port=6379)
coon.set('search_keyword', keyword)
auto.search(keyword, 1)

# sub = coon.pubsub()
# # 阻塞获取消息
# sub.psubscribe(['message'])
# for item in sub.listen():
#     message = item['data']
#     if message != 1:
#         message = str(message, encoding='utf-8')
#         message = eval(message)
#         if message['type'] == 'star':
#             auto.star()
#         elif message['type'] == 'get_comment':
#             auto.get_comment()
#         elif message['type'] == 'search':
#             auto.search('kfc', 4)
