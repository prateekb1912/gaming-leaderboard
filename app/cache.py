from upstash_redis import Redis
import json
from dotenv import load_dotenv

load_dotenv()

r = Redis.from_env()

def cache_leaderboard(data):
    r.set("top_leaderboard", json.dumps(data), ex=3600)

def get_cached_leaderboard():
    val = r.get("top_leaderboard")
    return json.loads(val) if val else None

def invalidate_leaderboard_cache():
    r.delete("top_leaderboard")
