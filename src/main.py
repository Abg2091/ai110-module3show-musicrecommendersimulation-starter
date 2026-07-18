"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs, score_breakdown

# Edge-case / adversarial profiles designed to stress-test the scoring logic:
# conflicting preferences, values absent from the catalog, out-of-range inputs,
# and messy string casing.
ADVERSARIAL_PROFILES = [
    (
        "Conflicting mood vs. energy (wants melancholic AND high-energy)",
        {"genre": "classical", "mood": "melancholic", "energy": 0.9, "likes_acoustic": True},
    ),
    (
        "Genre & mood that don't exist in the catalog at all",
        {"genre": "opera", "mood": "furious", "energy": 0.5},
    ),
    (
        "Out-of-range target energy (1.4, above the natural 0-1 scale)",
        {"genre": "techno", "mood": "mysterious", "energy": 1.4, "likes_acoustic": False},
    ),
    (
        "Messy case/whitespace in genre & mood",
        {"genre": "  PoP ", "mood": "HAPPY", "energy": 0.8, "likes_acoustic": None},
    ),
    (
        "Artist-loyalty overload (LoRoom dominates lofi/chill matches)",
        {"genre": "lofi", "mood": "chill", "energy": 0.4, "likes_acoustic": True},
    ),
]

# Same base profile scored with opposing acoustic preferences, using a song near
# acousticness 0.5 (Half Light, 0.50) where the acoustic bonus is a wash either way.
ACOUSTIC_FENCE_SITTER_BASE = {"genre": "indie pop", "mood": "relaxed", "energy": 0.48}


def _print_profile_and_recommendations(label: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    recommendations = recommend_songs(user_prefs, songs, k=k)

    print(f"\n{label}")
    print("=" * 40)
    for key, value in user_prefs.items():
        print(f"{key}: {value}")

    print(f"\nTop {len(recommendations)} Recommendations")
    print("-" * 40)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n{rank}. {song['title']} ({song['artist']}) - Score: {score:.2f}")
        breakdown = score_breakdown(user_prefs, song)
        breakdown_str = ", ".join(f"{component}={value:+.2f}" for component, value in breakdown.items())
        print(f"   Breakdown: {breakdown_str}")
        for reason in explanation.split("; "):
            print(f"   - {reason}")


def main() -> None:
    """Loads the song catalog and prints the user profile alongside its top-k recommendations."""
    songs = load_songs("data/songs.csv")

    # Starter example profile
    user_prefs = {"genre": "lofi", "mood": "chill", "energy": 0.6, "likes_acoustic": True}
    _print_profile_and_recommendations("User Profile", user_prefs, songs)

    print("\n\n" + "#" * 40)
    print("Adversarial / Edge-Case Profiles")
    print("#" * 40)

    for label, adversarial_prefs in ADVERSARIAL_PROFILES:
        _print_profile_and_recommendations(label, adversarial_prefs, songs)

    print("\nAcoustic fence-sitter comparison (likes_acoustic=True vs. False)")
    print("=" * 40)
    _print_profile_and_recommendations(
        "likes_acoustic=True", {**ACOUSTIC_FENCE_SITTER_BASE, "likes_acoustic": True}, songs
    )
    _print_profile_and_recommendations(
        "likes_acoustic=False", {**ACOUSTIC_FENCE_SITTER_BASE, "likes_acoustic": False}, songs
    )


if __name__ == "__main__":
    main()
