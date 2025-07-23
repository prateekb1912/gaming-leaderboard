from contextlib import contextmanager
from time import sleep
from sqlalchemy import func, update
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from .models import GameSession, Leaderboard

@contextmanager
def serializable_transaction(db: Session):
    db.execute(text("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE"))
    try:
        yield 
        db.commit()
    except Exception as e:
        db.rollback()
        raise e

def recalculate_leaderboard(db: Session, user_id: int, max_retries: int = 3):
    for _ in range(max_retries):
        try:
            with serializable_transaction(db):
                update_ranking(db, user_id)
            break
        except OperationalError as e:
            if "could not serialize access" in str(e):
                sleep(0.1)
                continue
            raise 

def update_ranking(db: Session, user_id: int):
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
    
    db.execute(stmt.execution_options(synchronize_session=False))