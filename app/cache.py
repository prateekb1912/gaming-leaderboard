import redis
import json

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

def cache_leaderboard(data):
    r.set("top_leaderboard", json.dumps(data), ex=3600)

def get_cached_leaderboard():
    val = r.get("top_leaderboard")
    return json.loads(val) if val else None

def invalidate_leaderboard_cache():
    r.delete("top_leaderboard")
