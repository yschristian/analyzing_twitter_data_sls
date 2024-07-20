from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from . import models, schemas
from .utils import POPULAR_HASHTAGS

def get_user_recommendations(db: Session, user_id: int, contact_type: str, phrase: str, hashtag: str):
    # Calculate interaction score
    interaction_subquery = db.query(
        models.Tweet.user_id.label('contacted_user_id'),
        func.count(models.Tweet.id).label('interaction_count')
    ).filter(
        (models.Tweet.in_reply_to_user_id == str(user_id)) |
        (models.Tweet.id_str.in_(
            db.query(models.Tweet.in_reply_to_status_id)
            .filter(models.Tweet.user_id == user_id)
        ))
    ).group_by(models.Tweet.user_id).subquery()

    # Calculate hashtag score
    hashtag_subquery = db.query(
        models.Tweet.user_id.label('user_id'),
        func.count(models.Hashtag.id).label('hashtag_count')
    ).join(models.TweetHashtag).join(models.Hashtag).filter(
        models.Hashtag.text.notin_(POPULAR_HASHTAGS)
    ).group_by(models.Tweet.user_id).subquery()

    # Calculate keyword score
    keyword_subquery = db.query(
        models.Tweet.user_id.label('user_id'),
        func.count(models.Tweet.id).label('keyword_count')
    ).filter(
        (models.Tweet.text.ilike(f'%{phrase}%')) |
        (models.Tweet.id.in_(
            db.query(models.TweetHashtag.tweet_id)
            .join(models.Hashtag)
            .filter(func.lower(models.Hashtag.text) == hashtag.lower())
        ))
    )
    if contact_type == 'reply':
        keyword_subquery = keyword_subquery.filter(models.Tweet.in_reply_to_user_id == str(user_id))
    elif contact_type == 'retweet':
        keyword_subquery = keyword_subquery.filter(models.Tweet.id_str.in_(
            db.query(models.Tweet.in_reply_to_status_id)
            .filter(models.Tweet.user_id == user_id)
        ))
    keyword_subquery = keyword_subquery.group_by(models.Tweet.user_id).subquery()

    # Combine scores and get user recommendations
    recommendations = db.query(
        models.User.id,
        models.User.screen_name,
        models.User.description,
        models.Tweet.text.label('contact_tweet_text'),
        (func.log(1 + 2 * func.coalesce(interaction_subquery.c.interaction_count, 0)) *
         func.greatest(1, 1 + func.log(1 + func.coalesce(hashtag_subquery.c.hashtag_count, 0) - 10)) *
         (1 + func.log(func.coalesce(keyword_subquery.c.keyword_count, 0) + 1))).label('score')
    ).join(interaction_subquery, models.User.id == interaction_subquery.c.contacted_user_id, isouter=True
    ).join(hashtag_subquery, models.User.id == hashtag_subquery.c.user_id, isouter=True
    ).join(keyword_subquery, models.User.id == keyword_subquery.c.user_id, isouter=True
    ).join(models.Tweet, models.User.id == models.Tweet.user_id
    ).filter(models.User.id != user_id
    ).order_by(desc('score'), desc(models.User.id)
    ).limit(10).all()

    return [
        schemas.UserRecommendation(
            user_id=r.id,
            screen_name=r.screen_name,
            description=r.description,
            contact_tweet_text=r.contact_tweet_text
        ) for r in recommendations if r.score > 0
    ]