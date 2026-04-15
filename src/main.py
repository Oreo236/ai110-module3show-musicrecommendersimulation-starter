"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs

WIDTH = 50

def main() -> None:
    songs = load_songs("data/songs.csv")

    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8, "likes_acoustic": False}
    user_prefs2 = {"genre": "pop",  "mood": "happy",   "energy": 0.85, "likes_acoustic": False}
    user_prefs3 = {"genre": "lofi", "mood": "chill",   "energy": 0.38, "likes_acoustic": True}
    user_prefs4 = {"genre": "rock", "mood": "intense", "energy": 0.92, "likes_acoustic": False}

    # --- Adversarial / edge-case profiles ---
    # 1. Mood that doesn't exist in the catalog — mood score silently 0
    adv1 = {"genre": "pop",  "mood": "sad",   "energy": 0.8,  "likes_acoustic": False}
    # 2. High energy conflicts with acoustic/lofi genre — continuous beats categorical?
    adv2 = {"genre": "lofi", "mood": "chill", "energy": 0.9,  "likes_acoustic": True}
    # 3. Out-of-range energy (>1) — no clamping, energy contribution goes negative
    adv3 = {"genre": "pop",  "mood": "happy", "energy": 1.5,  "likes_acoustic": False}
    # 4. Wrong capitalisation — exact match passes, all categorical scores are 0
    adv4 = {"genre": "Pop",  "mood": "Happy", "energy": 0.8,  "likes_acoustic": False}
    # 5. Genre/mood absent from catalog + valence hardcoded to 0.70 ignores dark taste
    adv5 = {"genre": "metal", "mood": "angry", "energy": 0.97, "likes_acoustic": False}
    # 6. Empty profile — only the hardcoded valence anchor (0.70) ranks songs
    adv6 = {}

    # --- New feature profiles (test popularity, decade, detailed_mood, instrumentalness, liveness) ---
    # 7. Full EDM profile — all 5 new fields active, best-case scenario for Neon Overload
    new1 = {
        "genre": "edm", "mood": "euphoric", "energy": 0.96, "likes_acoustic": False,
        "likes_popular": True, "preferred_decade": 2010,
        "detailed_mood": "euphoric", "likes_instrumental": False, "likes_live": False,
    }
    # 8. Underground acoustic fan from the 2020s — prefers obscure, instrumental, studio lofi
    new2 = {
        "genre": "lofi", "mood": "chill", "energy": 0.38, "likes_acoustic": True,
        "likes_popular": False, "preferred_decade": 2020,
        "detailed_mood": "focused", "likes_instrumental": True, "likes_live": False,
    }
    # 9. Nostalgic 1980s rock listener — wants live-sounding, vocal, popular classic rock
    new3 = {
        "genre": "rock", "mood": "intense", "energy": 0.91, "likes_acoustic": False,
        "likes_popular": True, "preferred_decade": 1980,
        "detailed_mood": "aggressive", "likes_instrumental": False, "likes_live": True,
    }
    # 10. Jazz cafe listener — relaxed, live feel, vocal, popular, 1990s decade
    new4 = {
        "genre": "jazz", "mood": "relaxed", "energy": 0.37, "likes_acoustic": True,
        "likes_popular": True, "preferred_decade": 1990,
        "detailed_mood": "romantic", "likes_instrumental": False, "likes_live": True,
    }
    # 11. Decade only — no genre/mood, just wants 2020s songs (tests decade feature in isolation)
    new5 = {
        "preferred_decade": 2020,
    }
    # 12. Popularity vs decade conflict — wants very popular songs but from the 1960s (few exist)
    new6 = {
        "likes_popular": True, "preferred_decade": 1960,
    }

    all_profiles = [
        (user_prefs,  "Baseline — pop / happy / 0.8"),
        (user_prefs2, "Baseline 2 — pop / happy / 0.85"),
        (user_prefs3, "Baseline 3 — lofi / chill / 0.38 acoustic"),
        (user_prefs4, "Baseline 4 — rock / intense / 0.92"),
        (adv1, "ADV 1 — mood 'sad' doesn't exist in catalog"),
        (adv2, "ADV 2 — high energy conflicts with lofi/acoustic"),
        (adv3, "ADV 3 — out-of-range energy 1.5 (no clamping)"),
        (adv4, "ADV 4 — wrong capitalisation 'Pop'/'Happy'"),
        (adv5, "ADV 5 — genre 'metal' absent; valence hardcoded to 0.70"),
        (adv6, "ADV 6 — empty profile (only hardcoded valence runs)"),
        (new1, "NEW 1 — full EDM profile (all 5 new fields)"),
        (new2, "NEW 2 — underground lofi / instrumental / 2020s"),
        (new3, "NEW 3 — nostalgic 1980s rock / live / vocal"),
        (new4, "NEW 4 — jazz cafe / live feel / 1990s"),
        (new5, "NEW 5 — decade only: 2020s (no genre or mood)"),
        (new6, "NEW 6 — conflict: popular taste but 1960s decade"),
    ]

    for prefs, label in all_profiles:
        recommendations = recommend_songs(prefs, songs, k=5)
        genre = prefs.get("genre", "(none)")
        mood  = prefs.get("mood",  "(none)")
        energy = prefs.get("energy", "(none)")

        print("\n" + "=" * WIDTH)
        print(f" {label}")
        print(f" Genre: {genre}  |  Mood: {mood}  |  Energy: {energy}")
        print("=" * WIDTH)

        for rank, (song, score, explanation) in enumerate(recommendations, start=1):
            print(f"\n#{rank}  {song['title']} by {song['artist']}")
            print(f"    Score : {score:.2f} / 16.0")
            print(f"    Genre : {song['genre']}  |  Mood: {song['mood']}")
            print(f"    Why   : {explanation}")
            print("-" * WIDTH)


if __name__ == "__main__":
    main()
