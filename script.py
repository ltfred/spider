import json
import time
from appium import webdriver
import os


class AutoControl(object):
    desired_caps = dict()
    desired_caps['platformName'] = 'Android'
    desired_caps['platformVersion'] = '5.1.1'
    desired_caps['deviceName'] = 'UHESY7W6NH'
    desired_caps['appPackage'] = 'com.ss.android.ugc.aweme'
    desired_caps['appActivity'] = 'com.ss.android.ugc.aweme.main.MainActivity'
    desired_caps['noReset'] = 'true'

    def __init__(self):
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', self.desired_caps)
        self.size = self.driver.get_window_size()
        self.width = self.size['width']
        self.height = self.size['height']
        self.duration = 500

    def swipe_up(self):
        x1 = self.width * 0.5
        y1 = self.height * 0.75
        y2 = self.height * 0.25
        self.driver.swipe(x1, y1, x1, y2, self.duration)

    def swipe_down(self):
        x1 = self.width * 0.5
        y1 = self.height * 0.25
        y2 = self.height * 0.75
        self.driver.swipe(x1, y1, x1, y2, self.duration)

    def swipe_left(self):
        x1 = self.width * 0.8
        y1 = self.height * 0.5
        x2 = self.width * 0.2
        self.driver.swipe(x1, y1, x2, y1, self.duration)

    def swipe_right(self):
        x1 = self.width * 0.3
        y1 = self.height * 0.5
        x2 = self.width * 0.6
        self.driver.swipe(x1, y1, x2, y1, self.duration)

    def follow(self):
        self.driver.tap([(557, 572), (581, 596)], 100)

    def star(self):
        self.driver.tap([(544, 612), (594, 662)], 100)

    def comment(self):
        self.driver.tap([(549, 689), (589, 729)], 100)

    def close_comment(self):
        self.driver.tap([(280, 216)], 100)
        self.driver.tap([(280, 200)], 100)

    def search(self, keyword):
        self.driver.tap([(22, 48)], 100)
        time.sleep(3)
        self.driver.find_element_by_id('com.ss.android.ugc.aweme:id/ahw').send_keys(keyword)
        time.sleep(2)
        self.driver.tap([(552, 785)], 100)



auto = AutoControl()
print('等待视频刷新中..............')
time.sleep(8)

while 1:
    auto.swipe_left()
    print('用户信息收集中。。。。。')
    time.sleep(5)
    try:
        with open('user_data.txt', 'r', encoding='utf-8') as r:
            content = r.read()
            user_dict = json.loads(content)
            count = user_dict['user']['aweme_count']
            short_id = user_dict['user']['short_id']
            if short_id == '0':
                short_id = user_dict['user']['unique_id']
            print('抖音号为：%s' % short_id )
            print('作品数量为：%s' % count)
            print('第1个视频')
    except:
        time.sleep(2)
        print('返回。。。')
        try:
            auto.driver.tap([(23, 53), (20, 50)], 100)
        except:
            auto.driver.tap([(23, 53), (20, 50)], 100)
        print('开始下一个。。。')
        time.sleep(2)
        auto.swipe_up()
        time.sleep(2)
        continue
    time.sleep(2)
    try:
        el1 = auto.driver.find_element_by_xpath('//android.widget.ImageView[@content-desc="视频1"]')
        el1.click()
    except:
        print('模拟点击')
        auto.driver.tap([(99, 742), (95, 750)], 100)
    time.sleep(2)
    auto.comment()
    time.sleep(2)
    auto.close_comment()
    for i in range(count - 1):
        print('第{}个视频'.format(i + 2))
        auto.swipe_up()
        time.sleep(2)
        auto.comment()
        time.sleep(2)
        auto.close_comment()
    if os.path.exists('user_data.txt'):
        os.remove('user_data.txt')
    time.sleep(2)
    print('返回。。。')
    try:
        auto.driver.tap([(23, 53), (20, 50)], 100)
    except:
        auto.driver.tap([(23, 53), (20, 50)], 100)
    print('开始下一个。。。')
    time.sleep(2)
    try:
        auto.driver.tap([(23, 53), (20, 50)], 100)
    except:
        auto.driver.tap([(23, 53), (20, 50)], 100)
    auto.swipe_up()
    time.sleep(2)


