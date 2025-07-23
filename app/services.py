from sqlalchemy.orm import Session
from .models import GameSession, Leaderboard
from .utils import recalculate_leaderboard
from .cache import get_cached_leaderboard, cache_leaderboard, invalidate_leaderboard_cache

def submit_score(db: Session, user_id: int, score: int):
    try:
        session = GameSession(user_id=user_id, score=score, game_mode='solo')
        db.add(session)
        db.commit()
        recalculate_leaderboard(db, user_id)
        invalidate_leaderboard_cache()
    except Exception:
        db.rollback()
        raise

def get_top_players(db: Session, limit=10):
    cached = get_cached_leaderboard()
    if cached:
        return cached
    else:
        players = db.query(Leaderboard).order_by(Leaderboard.total_score.desc()).limit(limit).all()
        cache_leaderboard([player.to_dict() for player in players])
        return players

def get_user_rank(db: Session, user_id: int):
    return db.query(Leaderboard).filter(Leaderboard.user_id == user_id).first()
