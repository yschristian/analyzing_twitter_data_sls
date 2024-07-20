from pydantic import BaseModel
from typing import List

class UserRecommendation(BaseModel):
    user_id: int
    screen_name: str
    description: str
    contact_tweet_text: str

class Q2Response(BaseModel):
    team_id: str
    team_aws_account_id: str
    recommendations: List[UserRecommendation]

class Config:
    orm_mode = True