import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

GENRE_WEIGHT = 1.0
MOOD_WEIGHT = 2.0
ENERGY_WEIGHT = 1.5
ACOUSTIC_WEIGHT = 1.0

MAX_SONGS_PER_ARTIST = 2


def _normalize(value: str) -> str:
    """Case/whitespace-insensitive comparison so 'R&B' vs 'r&b' still matches."""
    return value.strip().lower()


def _score_song(
    genre: str,
    mood: str,
    energy: float,
    acousticness: float,
    fav_genre: str,
    fav_mood: str,
    target_energy: float,
    likes_acoustic: Optional[bool] = None,
) -> Tuple[float, List[str]]:
    """
    Shared scoring logic for both the dict-based and dataclass-based recommendation paths.
    likes_acoustic=None means no acoustic preference was given, so that term is skipped.
    """
    reasons = []
    score = 0.0

    if _normalize(genre) == _normalize(fav_genre):
        score += GENRE_WEIGHT
        reasons.append(f"genre '{genre}' matches your favorite")

    if _normalize(mood) == _normalize(fav_mood):
        score += MOOD_WEIGHT
        reasons.append(f"mood '{mood}' fits what you're looking for")

    energy_closeness = 1 - abs(energy - target_energy)
    score += ENERGY_WEIGHT * energy_closeness
    if energy_closeness > 0.85:
        reasons.append(f"energy ({energy:.2f}) is close to your target ({target_energy:.2f})")

    if likes_acoustic is not None:
        acoustic_fit = acousticness if likes_acoustic else (1 - acousticness)
        score += ACOUSTIC_WEIGHT * acoustic_fit
        if acoustic_fit > 0.7:
            reasons.append("acoustic level fits your preference")

    if not reasons:
        reasons.append("closest overall match available")

    return score, reasons


def _select_diverse_top_k(scored: List, k: int, get_artist) -> List:
    """
    Picks the top k from a list already sorted descending by score, skipping any
    song once its artist has reached MAX_SONGS_PER_ARTIST, so one prolific artist
    can't crowd out the rest of the recommendations. This is ranking logic, not
    scoring logic - it never changes any song's score, only which ones get shown.
    """
    selected = []
    artist_counts = {}
    for item in scored:
        artist = get_artist(item)
        if artist_counts.get(artist, 0) >= MAX_SONGS_PER_ARTIST:
            continue
        selected.append(item)
        artist_counts[artist] = artist_counts.get(artist, 0) + 1
        if len(selected) == k:
            break
    return selected

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
        scored = [
            (
                _score_song(
                    song.genre,
                    song.mood,
                    song.energy,
                    song.acousticness,
                    user.favorite_genre,
                    user.favorite_mood,
                    user.target_energy,
                    user.likes_acoustic,
                )[0],
                song,
            )
            for song in self.songs
        ]
        scored.sort(key=lambda pair: pair[0], reverse=True)
        selected = _select_diverse_top_k(scored, k, get_artist=lambda pair: pair[1].artist)
        return [song for _, song in selected]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        _, reasons = _score_song(
            song.genre,
            song.mood,
            song.energy,
            song.acousticness,
            user.favorite_genre,
            user.favorite_mood,
            user.target_energy,
            user.likes_acoustic,
        )
        return "; ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    numeric_fields = ("energy", "tempo_bpm", "valence", "danceability", "acousticness")
    with open(csv_path, newline="", encoding="utf-8") as f:
        songs = []
        for row in csv.DictReader(f):
            row["id"] = int(row["id"])
            for field in numeric_fields:
                row[field] = float(row[field])
            songs.append(row)
        print(f"Loaded {len(songs)} songs from {csv_path}.")
        return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    return _score_song(
        song["genre"],
        song["mood"],
        song["energy"],
        song["acousticness"],
        user_prefs["genre"],
        user_prefs["mood"],
        user_prefs["energy"],
        user_prefs.get("likes_acoustic"),
    )

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored = [(song, *score_song(user_prefs, song)) for song in songs]
    scored.sort(key=lambda triple: triple[1], reverse=True)
    selected = _select_diverse_top_k(scored, k, get_artist=lambda triple: triple[0]["artist"])
    return [(song, score, "; ".join(reasons)) for song, score, reasons in selected]
