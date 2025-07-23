from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import SessionLocal
from schemas import ScoreSubmissionInput
from services import submit_score, get_top_players, get_user_rank

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/api/leaderboard/submit")
def submit(payload: ScoreSubmissionInput, db: Session = Depends(get_db)):
    submit_score(db, payload.user_id, payload.score)
    return {"status": "success"}

@app.get("/api/leaderboard/top")
def top_players(db: Session = Depends(get_db)):
    players = get_top_players(db)
    return players

@app.get("/api/leaderboard/rank/{user_id}")
def user_rank(user_id: int, db: Session = Depends(get_db)):
    return get_user_rank(db, user_id)
