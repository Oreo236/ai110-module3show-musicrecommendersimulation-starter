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

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\n" + "=" * WIDTH)
    print(" MUSIC RECOMMENDER — TOP PICKS FOR YOU")
    print(f" Genre: {user_prefs['genre']}  |  Mood: {user_prefs['mood']}  |  Energy: {user_prefs['energy']}")
    print("=" * WIDTH)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n#{rank}  {song['title']} by {song['artist']}")
        print(f"    Score : {score:.2f} / 9.5")
        print(f"    Genre : {song['genre']}  |  Mood: {song['mood']}")
        print(f"    Why   : {explanation}")
        print("-" * WIDTH)


if __name__ == "__main__":
    main()
