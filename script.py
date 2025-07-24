import requests, random, time

API_BASE_URL = "http://localhost:8000/api/leaderboard"

def submit_score(user_id):
    score = random.randint(100, 1000)
    requests.post(f"{API_BASE_URL}/submit", json={"user_id": user_id, "score": score})

def get_top_players():
    return requests.get(f"{API_BASE_URL}/top").json()

def get_user_rank(user_id):
    res = requests.get(f"{API_BASE_URL}/rank/{user_id}")

if __name__ == "__main__":
    while True:
        user_id = random.randint(1, 100000)
        submit_score(user_id)
        time.sleep(random.uniform(0.5, 2))
