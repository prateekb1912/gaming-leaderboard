from sqlalchemy.orm import Session
from .models import GameSession, Leaderboard, User
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
        return None

def get_top_players(db: Session, limit=10):
    cached = get_cached_leaderboard()
    if cached:
        return cached
    else:
        try:
            results = db.query(Leaderboard, User.username).join(User, Leaderboard.user_id == User.id).order_by(Leaderboard.total_score.desc()).limit(limit).all()
        except Exception as e:
            return []

        players = []
        for leaderboard_entry, username in results:
            player_data = {
                "user_id": leaderboard_entry.user_id,
                "username": username,
                "total_score": leaderboard_entry.total_score,
                "rank": leaderboard_entry.rank
            }
            players.append(player_data)

        cache_leaderboard(players)

        return players

def get_user_rank(db: Session, user_id: int):
    try:
        res =  db.query(Leaderboard, User.username).filter(Leaderboard.user_id == user_id).join(User, Leaderboard.user_id == User.id).first()
    except Exception as e:
        return None

    leaderboard, username = res

    return {
        "user_id": leaderboard.user_id,
        "username": username,
        "total_score": leaderboard.total_score,
        "rank": leaderboard.rank
    }
