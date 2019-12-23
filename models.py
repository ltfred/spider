from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("mysql+pymysql://logan:L123456@10.64.144.3:3306/vsblob")
Base = declarative_base()

class Video(Base):
    __tablename__ = 'douyin_video'
    id = Column(Integer, primary_key=True)
    aweme_id = Column(String(64))
    desc = Column(String(255))
    short_id = Column(String(32))
    bp_time = Column(String(16))
    music = Column(String(255))
    video = Column(Text)
    comment_count = Column(Integer)
    digg_count = Column(Integer)
    share_count = Column(Integer)


class User(Base):
    __tablename__ = 'douyin_user_info'
    id = Column(Integer, primary_key=True)
    short_id = Column(String(32))
    city = Column(String(16))
    nickname = Column(String(16))
    follower_count = Column(Integer)


class Follow(Base):
    __tablename__ = 'douyin_follow'
    id = Column(Integer, primary_key=True)
    following = Column(String(16))
    follower = Column(String(16))



class Comment(Base):
    __tablename__ = 'douyin_comment'
    uid = Column(Integer, primary_key=True)
    aweme_id = Column(String(64))
    author = Column(String(32))
    content = Column(Text)
    time = Column(String(16))


Base.metadata.create_all(engine)