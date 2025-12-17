import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HIGHSCORES_PATH = os.path.join(BASE_DIR, "data", "highscores.json")

def load_highscores():
    try:
        with open(HIGHSCORES_PATH, "r") as f:
            data = json.load(f)
            # Ensure data is a list of dicts: [{"name": "Player", "score": 100}, ...]
            # Legacy support: if it was a single int or dict, convert it?
            # We controlled previous structure: {"high_score": 100, "history": []}.
            # Let's pivot to just keeping a list of high scores in the file for simplicity, 
            # or keep structure {"leaderboard": [...]}.
            if "leaderboard" in data:
                 return data["leaderboard"]
            return []
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_highscore(name, score):
    scores = load_highscores()
    new_entry = {
        "name": name,
        "score": score,
        "date": str(datetime.now().date())
    }
    scores.append(new_entry)
    # Sort descending by score
    scores.sort(key=lambda x: x["score"], reverse=True)
    # Keep top 10
    scores = scores[:10]
    
    try:
        with open(HIGHSCORES_PATH, "w") as f:
            json.dump({"highscores": scores}, f, indent=2)
    except Exception as e:
        print(f"[ERROR] Failed to save highscore: {e}")

def get_highest_score():
    scores = load_highscores()
    if scores:
        return scores[0]["score"]
    return 0
