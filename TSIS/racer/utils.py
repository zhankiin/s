import json
import os
from config import LEADERBOARD_FILE


def load_leaderboard():
    """Load leaderboard from JSON file."""
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE) as f:
            return json.load(f)
    return []


def save_leaderboard(data):
    """Save leaderboard to JSON file."""
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(data, f, indent=4)


def add_score(score, distance):
    """Add a new score and keep top 10."""
    data = load_leaderboard()
    data.append({"name": "Player", "score": score, "dist": distance})
    data = sorted(data, key=lambda x: x["score"], reverse=True)[:10]
    save_leaderboard(data)
