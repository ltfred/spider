import json
from mitmproxy import http
from sqlalchemy.orm import sessionmaker
from models import engine, Video, User, Comment

Session_class = sessionmaker(bind=engine)
session = Session_class()


class Spider(object):

    def response(self, flow: http.HTTPFlow):
        video_url = 'https://aweme-ipv6.snssdk.com/aweme/v1/aweme/post/'
        user_info_url = 'https://aweme-eagle-ipv6.snssdk.com/aweme/v1/user/'
        following_url = 'https://aweme-ipv6.snssdk.com/aweme/v1/user/follower/list/'
        comment_url = 'https://aweme-ipv6.snssdk.com/aweme/v2/comment/list/'
        if flow.request.url.startswith(video_url):
            print('视频-----------')
            response = flow.response.get_text()
            self.parse_video_response(response)
        elif flow.request.url.startswith(user_info_url):
            print('用户信息------------')
            response = flow.response.get_text()
            self.parse_user_info_response(response)
        elif flow.request.url.startswith(following_url):
            print('用户粉丝------------')
            response = flow.response.get_text()
            self.parse_user_follow_response(response)
        elif flow.request.url.startswith(comment_url):
            print('视频评论------------')
            response = flow.response.get_text()
            self.parse_comment_response(response)

    def parse_video_response(self, response):
        print('running ....... parse video response')
        json_dict = json.loads(response)
        aweme_list = json_dict['aweme_list']
        for aweme in aweme_list:
            if aweme['author']['unique_id'] != '':
                obj = Video(aweme_id=aweme['aweme_id'], desc=aweme['desc'], bp_time=aweme['create_time'],
                            short_id=str(aweme['author']['unique_id']), music=str(aweme['music']['play_url']['uri']),
                            video=aweme['video']['play_addr']['url_list'][0],
                            comment_count=int(aweme['statistics']['comment_count']),
                            digg_count=int(aweme['statistics']['digg_count']),
                            share_count=int(aweme['statistics']['share_count']))
            else:
                obj = Video(aweme_id=aweme['aweme_id'], desc=aweme['desc'], bp_time=aweme['create_time'],
                            short_id=str(aweme['author']['short_id']), music=str(aweme['music']['play_url']['uri']),
                            video=aweme['video']['play_addr']['url_list'][0],
                            comment_count=int(aweme['statistics']['comment_count']),
                            digg_count=int(aweme['statistics']['digg_count']),
                            share_count=int(aweme['statistics']['share_count']))
            session.add(obj)
            session.commit()

    def parse_user_info_response(self, response):
        print('running ....... parse user info response')
        with open('user_data.txt', 'w') as w:
            w.write(response)
        dict = json.loads(response)
        if dict['user']['short_id'] == '0':
            obj = User(short_id=dict['user']['unique_id'], city=dict['user']['city'],
                       nickname=dict['user']['nickname'], follower_count=dict['user']['follower_count'])
        else:
            obj = User(short_id=dict['user']['short_id'], city=dict['user']['city'],
                       nickname=dict['user']['nickname'], follower_count=dict['user']['follower_count'])
        session.add(obj)
        session.commit()

    def parse_user_follow_response(self, response):
        print('running ....... parse user follow response')
        with open('user_follow_data.txt', 'w') as w:
            w.write(response)

    def parse_comment_response(self, response):
        print('running parse comment function .......')
        dict = json.loads(response)
        comments = dict['comments']
        for comment in comments:
            if comment['user']['short_id'] != '0':
                obj = Comment(aweme_id=comment['aweme_id'], content=comment['text'], time=str(comment['create_time']), author=comment['user']['short_id'])
            else:
                obj = Comment(aweme_id=comment['aweme_id'], content=comment['text'], time=str(comment['create_time']),
                              author=comment['user']['unique_id'])
            session.add(obj)
            session.commit()


addons = [
    Spider()
]
