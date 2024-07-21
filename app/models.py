from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    id_str = Column(String, unique=True, index=True)
    name = Column(String)
    screen_name = Column(String, index=True)
    description = Column(Text)
    created_at = Column(DateTime)
    followers_count = Column(Integer)
    friends_count = Column(Integer)
    statuses_count = Column(Integer)
    lang = Column(String)

    tweets = relationship("Tweet", back_populates="user")

class Tweet(Base):
    __tablename__ = "tweets"

    id = Column(Integer, primary_key=True, index=True)
    id_str = Column(String, unique=True, index=True)
    created_at = Column(DateTime)
    text = Column(Text)
    source = Column(String)
    in_reply_to_status_id = Column(String)
    in_reply_to_user_id = Column(String)
    in_reply_to_screen_name = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    retweet_count = Column(Integer)
    favorite_count = Column(Integer)
    lang = Column(String)

    user = relationship("User", back_populates="tweets")
    hashtags = relationship("Hashtag", secondary="tweet_hashtags")

class Hashtag(Base):
    __tablename__ = "hashtags"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, unique=True, index=True)

class TweetHashtag(Base):
    __tablename__ = "tweet_hashtags"

    tweet_id = Column(Integer, ForeignKey("tweets.id"), primary_key=True)
    hashtag_id = Column(Integer, ForeignKey("hashtags.id"), primary_key=True)
    