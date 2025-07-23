from sqlalchemy.orm import Session
from models import GameSession, Leaderboard
from sqlalchemy import func, update

def recalculate_leaderboard(db: Session, user_id: int):
    """
    Recalculate the leaderboard after a user's score has been updated.
    """
    total_score = db.query(func.sum(GameSession.score)).filter(GameSession.user_id == user_id).scalar() or 0
    existing = db.query(Leaderboard).filter(Leaderboard.user_id == user_id).first()
    
    if existing:
        existing.total_score = total_score
        old_rank = existing.rank
    else:
        existing = Leaderboard(user_id=user_id, total_score=total_score)
        db.add(existing)
        old_rank = None    
    
    db.commit()
    
    new_rank = db.query(Leaderboard).filter(Leaderboard.total_score > total_score).count() + 1
    existing.rank = new_rank
    
    if old_rank is None or new_rank == old_rank:
        db.commit()
        return

    if new_rank < old_rank:
        stmt = update(Leaderboard).where(
            Leaderboard.rank >= new_rank,
            Leaderboard.rank < old_rank,
            Leaderboard.user_id != user_id
        ).values(rank=Leaderboard.rank + 1)
    else:
        stmt = update(Leaderboard).where(
            Leaderboard.rank > old_rank,
            Leaderboard.rank <= new_rank,
            Leaderboard.user_id != user_id
        ).values(rank=Leaderboard.rank - 1)
    
    db.execute(stmt)
    db.commit()