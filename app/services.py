from sqlalchemy.orm import Session
from models import GameSession, Leaderboard
from utils import recalculate_leaderboard

def submit_score(db: Session, user_id: int, score: int):
    session = GameSession(user_id=user_id, score=score, game_mode='solo')
    db.add(session)
    db.commit()
    recalculate_leaderboard(db, user_id)

def get_top_players(db: Session, limit=10):
    return db.query(Leaderboard).order_by(Leaderboard.total_score.desc()).limit(limit).all()

def get_user_rank(db: Session, user_id: int):
    return db.query(Leaderboard).filter(Leaderboard.user_id == user_id).first()
