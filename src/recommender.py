import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Parse a CSV file of songs and return a list of dicts with typed numeric fields."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id":           int(row["id"]),
                "title":        row["title"],
                "artist":       row["artist"],
                "genre":        row["genre"],
                "mood":         row["mood"],
                "energy":       float(row["energy"]),
                "tempo_bpm":    float(row["tempo_bpm"]),
                "valence":      float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against user preferences and return (total_score, reason_strings)."""
    score = 0.0
    reasons = []

    # Genre match — exact, weight 3.0
    if song["genre"] == user_prefs.get("genre"):
        score += 3.0
        reasons.append(f"matched genre: {song['genre']}")

    # Mood match — exact, weight 2.5
    if song["mood"] == user_prefs.get("mood"):
        score += 2.5
        reasons.append(f"matched mood: {song['mood']}")

    # Energy proximity — squared distance, weight 2.0
    if "energy" in user_prefs:
        energy_sim = 1 - (song["energy"] - user_prefs["energy"]) ** 2
        score += energy_sim * 2.0
        reasons.append(f"energy {song['energy']:.2f} vs your target {user_prefs['energy']:.2f}")

    # Acousticness proximity — squared distance, weight 1.5
    # likes_acoustic=True targets 0.80, False targets 0.15
    if "likes_acoustic" in user_prefs:
        target_acoustic = 0.80 if user_prefs["likes_acoustic"] else 0.15
        acoustic_sim = 1 - (song["acousticness"] - target_acoustic) ** 2
        score += acoustic_sim * 1.5
        label = "acoustic" if user_prefs["likes_acoustic"] else "non-acoustic"
        reasons.append(f"acousticness {song['acousticness']:.2f} suits a {label} preference")

    # Valence proximity — squared distance against fixed 0.70, weight 0.5
    valence_sim = 1 - (song["valence"] - 0.70) ** 2
    score += valence_sim * 0.5
    reasons.append(f"valence {song['valence']:.2f}")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song, sort by score descending, and return the top k as (song, score, explanation)."""
    scored = [
        (song, score, ", ".join(reasons))
        for song in songs
        for score, reasons in [score_song(user_prefs, song)]
    ]
    return sorted(scored, key=lambda x: x[1], reverse=True)[:k]
