from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, func
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    join_date = Column(TIMESTAMP, server_default=func.now())

class GameSession(Base):
    __tablename__ = "game_sessions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    score = Column(Integer, nullable=False)
    game_mode = Column(String(50), nullable=False)
    timestamp = Column(TIMESTAMP, server_default=func.now())

class Leaderboard(Base):
    __tablename__ = "leaderboard"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    total_score = Column(Integer, nullable=False)
    rank = Column(Integer)

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "total_score": self.total_score,
            "rank": self.rank,
            "id": self.id
        }