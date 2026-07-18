"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    """Loads the song catalog and prints the user profile alongside its top-k recommendations."""
    songs = load_songs("data/songs.csv")

    # Starter example profile
    user_prefs = {"genre": "lofi", "mood": "chill", "energy": 0.6, "likes_acoustic": True}

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nUser Profile")
    print("=" * 40)
    for key, value in user_prefs.items():
        print(f"{key}: {value}")

    print(f"\nTop {len(recommendations)} Recommendations")
    print("=" * 40)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n{rank}. {song['title']} ({song['artist']}) - Score: {score:.2f}")
        for reason in explanation.split("; "):
            print(f"   - {reason}")


if __name__ == "__main__":
    main()
