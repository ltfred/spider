from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("mysql+pymysql://logan:L123456@10.64.144.3:3306/vsblob")
Base = declarative_base()


class Video(Base):
    # 视频信息表
    __tablename__ = 'douyin_video'
    id = Column(Integer, primary_key=True)
    aweme_id = Column(String(64))
    desc = Column(String(255))
    short_id = Column(String(32))
    bp_time = Column(String(16))
    music_url = Column(String(255))
    video_url = Column(Text)
    comment_count = Column(Integer)
    digg_count = Column(Integer)
    share_count = Column(Integer)


class User(Base):
    # 用户信息表
    __tablename__ = 'douyin_user_info'
    id = Column(Integer, primary_key=True)
    short_id = Column(String(32))
    city = Column(String(16))
    country = Column(String(8))
    province = Column(String(8))
    nickname = Column(String(16))
    follower_count = Column(Integer)
    following_count = Column(Integer)
    aweme_count = Column(Integer)
    favoriting_count = Column(Integer)
    dongtai_count = Column(Integer)
    total_favorited_count = Column(Integer)
    birthday = Column(String(32))
    signature = Column(Text)


class Follower(Base):
    # 粉丝信息表
    __tablename__ = 'douyin_follower'
    id = Column(Integer, primary_key=True)
    following = Column(String(32))
    follower = Column(String(32))


class Following(Base):
    # 关注信息表
    __tablename__ = 'douyin_following'
    id = Column(Integer, primary_key=True)
    following = Column(String(32))
    follower = Column(String(32))


class Comment(Base):
    # 视频评论表
    __tablename__ = 'douyin_comment'
    id = Column(Integer, primary_key=True)
    aweme_id = Column(String(64))
    author = Column(String(32))
    content = Column(Text)
    time = Column(String(16))


Base.metadata.create_all(engine)