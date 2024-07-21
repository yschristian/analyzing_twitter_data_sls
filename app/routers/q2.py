from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas, database
from urllib.parse import unquote
from dotenv import load_dotenv
import os

router = APIRouter()

load_dotenv()

TEAM_ID = os.getenv("TEAM_ID")
TEAM_AWS_ACCOUNT_ID = os.getenv("TEAM_AWS_ACCOUNT_ID")

@router.get("/q2", response_model=schemas.Q2Response)
def get_user_recommendations(
    user_id: int,
    type: str,
    phrase: str,
    hashtag: str,
    db: Session = Depends(database.get_db)
):
    if type not in ['reply', 'retweet', 'both']:
        raise HTTPException(status_code=400, detail="Invalid type. Must be 'reply', 'retweet', or 'both'.")
    
    decoded_phrase = unquote(phrase)
    recommendations = crud.get_user_recommendations(db, user_id, type, decoded_phrase, hashtag)

 # PUT team_id and team_aws_account_id    
 
    return schemas.Q2Response(
        team_id="TEAM_ID", 
        team_aws_account_id="TEAM_AWS_ACCOUNT_ID",
        recommendations=recommendations
    )