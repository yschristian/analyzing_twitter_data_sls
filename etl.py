import json
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.database import SessionLocal, engine
from app.models import Base, User, Tweet, Hashtag, TweetHashtag
from app.utils import POPULAR_HASHTAGS

def parse_twitter_datetime(dt_string):
    return datetime.strptime(dt_string, '%a %b %d %H:%M:%S +0000 %Y')

def process_tweet(tweet_data, session):
    # Process user
    user_data = tweet_data['user']
    user = session.query(User).filter_by(id_str=user_data['id_str']).first()
    if not user:
        user = User(
            id_str=user_data['id_str'],
            name=user_data['name'],
            screen_name=user_data['screen_name'],
            description=user_data['description'],
            created_at=parse_twitter_datetime(user_data['created_at']),
            followers_count=user_data['followers_count'],
            friends_count=user_data['friends_count'],
            statuses_count=user_data['statuses_count'],
            lang=user_data['lang']
        )
        session.add(user)
        session.flush()

    # Process tweet
    tweet = Tweet(
        id_str=tweet_data['id_str'],
        created_at=parse_twitter_datetime(tweet_data['created_at']),
        text=tweet_data['text'],
        source=tweet_data['source'],
        in_reply_to_status_id=tweet_data['in_reply_to_status_id_str'],
        in_reply_to_user_id=tweet_data['in_reply_to_user_id_str'],
        in_reply_to_screen_name=tweet_data['in_reply_to_screen_name'],
        user_id=user.id,
        retweet_count=tweet_data['retweet_count'],
        favorite_count=tweet_data['favorite_count'],
        lang=tweet_data['lang']
    )
    session.add(tweet)
    session.flush()

    # Process hashtags
    for hashtag_data in tweet_data['entities']['hashtags']:
        hashtag_text = hashtag_data['text'].lower()
        if hashtag_text not in POPULAR_HASHTAGS:
            hashtag = session.query(Hashtag).filter_by(text=hashtag_text).first()
            if not hashtag:
                hashtag = Hashtag(text=hashtag_text)
                session.add(hashtag)
                session.flush()
            
            # Check if the tweet-hashtag pair already exists
            tweet_hashtag = TweetHashtag(tweet_id=tweet.id, hashtag_id=hashtag.id)
            session.add(tweet_hashtag)
            try:
                session.flush()
            except IntegrityError:
                session.rollback()

def main():
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()

    with open('query2_ref.txt', 'r') as f:
        for line in f:
            tweet_data = json.loads(line.strip())
            process_tweet(tweet_data, session)

    session.commit()
    session.close()

if __name__ == "__main__":
    main()
