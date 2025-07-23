import redis
import json
import os
from dotenv import load_dotenv

load_dotenv()

r = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=os.getenv("REDIS_PORT", "6379"),
    decode_responses=True,
    password=os.getenv("REDIS_PASSWORD", ""),
)

def cache_leaderboard(data):
    r.set("top_leaderboard", json.dumps(data), ex=3600)

def get_cached_leaderboard():
    val = r.get("top_leaderboard")
    return json.loads(val) if val else None

def invalidate_leaderboard_cache():
    r.delete("top_leaderboard")
