from sqlalchemy.orm import Session
from models import GameSession, Leaderboard
from sqlalchemy import func

def recalculate_leaderboard(db: Session, user_id: int):
    total_score = db.query(func.sum(GameSession.score)).filter(GameSession.user_id == user_id).scalar()
    
    existing = db.query(Leaderboard).filter(Leaderboard.user_id == user_id).first()
    if existing:
        existing.total_score = total_score
    else:
        db.add(Leaderboard(user_id=user_id, total_score=total_score))

    db.commit()

    # Re-rank
    sub = db.query(Leaderboard).order_by(Leaderboard.total_score.desc()).all()
    for idx, row in enumerate(sub, start=1):
        row.rank = idx
    db.commit()
