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
        follower_url = 'https://aweme-ipv6.snssdk.com/aweme/v1/user/follower/list/'
        following_url = 'https://aweme-ipv6.snssdk.com/aweme/v1/user/following/list/'
        comment_url = 'https://aweme-ipv6.snssdk.com/aweme/v2/comment/list/'
        comment_reply_url = 'https://aweme-ipv6.snssdk.com/aweme/v1/comment/list/reply/'
        if flow.request.url.startswith(video_url):
            print('视频信息-----------')
            response = flow.response.get_text()
            self.parse_video_response(response)
        elif flow.request.url.startswith(user_info_url):
            print('用户信息------------')
            response = flow.response.get_text()
            self.parse_user_info_response(response)
        elif flow.request.url.startswith(follower_url):
            print('用户粉丝------------')
            response = flow.response.get_text()
            self.parse_user_follower_response(response)
        elif flow.request.url.startswith(comment_url):
            print('视频评论------------')
            response = flow.response.get_text()
            self.parse_comment_response(response)
        elif flow.request.url.startswith(following_url):
            print('用户关注-------------')
            response = flow.response.get_text()
            self.parse_user_following_response(response)
        elif flow.request.url.startswith(comment_reply_url):
            print('评论回复-------------')
            response = flow.response.get_text()
            self.parse_comment_reply_response(response)

    def parse_video_response(self, response):
        print('running ....... parse video response')
        json_dict = json.loads(response)
        aweme_list = json_dict['aweme_list']
        for aweme in aweme_list:
            obj = Video(aweme_id=aweme['aweme_id'], desc=aweme['desc'], bp_time=aweme['create_time'],
                        music_url=str(aweme['music']['play_url']['uri']),
                        video_url=aweme['video']['play_addr']['url_list'][0],
                        comment_count=int(aweme['statistics']['comment_count']),
                        digg_count=int(aweme['statistics']['digg_count']),
                        share_count=int(aweme['statistics']['share_count']))
            if aweme['author']['unique_id'] != '':
                obj.short_id = str(aweme['author']['unique_id'])
            else:
                obj.short_id = str(aweme['author']['short_id'])
            session.add(obj)
            session.commit()

    def parse_user_info_response(self, response):
        print('running ....... parse user info response')
        with open('user_data.txt', 'w') as w:
            w.write(response)
        user_dict = json.loads(response)
        obj = User(city=user_dict['user']['city'], country=user_dict['user']['country'],
                   province=user_dict['user']['province'], nickname=user_dict['user']['nickname'],
                   follower_count=user_dict['user']['follower_count'], following_count=user_dict['user']['following_count'],
                   aweme_count=user_dict['user']['aweme_count'], favoriting_count=user_dict['user']['favoriting_count'],
                   dongtai_count=user_dict['user']['dongtai_count'],
                   total_favorited_count=user_dict['user']['total_favorited'], birthday=user_dict['user']['birthday'],
                   signature=user_dict['user']['signature'])
        if user_dict['user']['short_id'] == '0':
            obj.short_id = user_dict['user']['unique_id']
        else:
            obj.short_id = user_dict['user']['short_id']
        session.add(obj)
        session.commit()

    def parse_user_follower_response(self, response):
        print('running ....... parse user follow response')
        with open('user_follower_data.txt', 'w') as w:
            w.write(response)

    def parse_comment_response(self, response):
        print('running parse comment function .......')
        comment_dict = json.loads(response)
        comments = comment_dict['comments']
        if len(comments) != 0:
            for comment in comments:
                obj = Comment(aweme_id=comment['aweme_id'], content=comment['text'], time=str(comment['create_time']))
                if comment['user']['short_id'] != '0':
                    obj.author = comment['user']['short_id']
                else:
                    obj.author = author=comment['user']['unique_id']
                session.add(obj)
                session.commit()

    def parse_user_following_response(self, response):
        print('running ....... parse user following response')
        with open('user_following_data.txt', 'w') as w:
            w.write(response)

    def parse_comment_reply_response(self, response):
        print('running ....... parse user following response')
        with open('comment_reply_data.txt', 'w') as w:
            w.write(response)


addons = [
    Spider()
]
