# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

This model will be called as "Match ur Mood 1.0"

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

"Match ur Mood" music recommender is intended to find a list of top 5 songs from the database to that synchronize with user's mood. 

Prompts:  

- What kind of recommendations does it generate  

It generates mood based recommendation over genre.

- What assumptions does it make about the user  

It assumes that the mood correlates directly with the energy/feel a user is actually asking for in the moment, so it's a more reliable predictor of "will this song feel right right now."

- Is this for real users or classroom exploration  

Match ur Mood 1.0 is currently in its first phase so I would called it as more of a classroom exploration than real user ready product.

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  

Freature used are: Mood, genre, energy and acousticness.

- What user preferences are considered  

Apart from regular preference, 5 adversarial user preferances such as conflicting preferences, values absent from the catalog, out-of-range inputs, Artist-loyalty overload,and messy string casing were considered to test the system.

- How does the model turn those into a score  

To score a song, the "Recommender" adds up points for every way it matches what the user asked for, but not all matches count equally. Mood and energy are weighted the heaviest on purpose, because my philosophy is to match user's mood in the moment, not lock onto a fixed identity.

- What changes did you make from the starter logic  

The significant change that I made is, mood and energy are weighted the heaviest on purpose, in order to match user's mood in the moment.

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  

There are total 23 songs in the catalog.

- What genres or moods are represented  

Genres in the catalog (17 unique):
pop, lofi, rock, ambient, jazz, synthwave, indie pop, classical, hip hop, folk, metal, R&B, country, EDM, reggae, blues, techno.

Moods in the catalog (16 unique):
happy, chill, intense, relaxed, moody, focused, melancholic, triumphant, nostalgic, aggressive, romantic, hopeful, euphoric, playful, somber, mysterious.

- Did you add or remove data  

I have added 13 new songs to the given data set.

- Are there parts of musical taste missing in the dataset  

The genres' like reggae, techno, EDM, classical, folk , metal etc, and the moods like somber, playful, euphoric, mysteriou etc. were missing in the given data set which were added later to make it more roburst.

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  

User with simple preferences (mood, energy, genre, and acousticness). 

- Any patterns you think your scoring captures correctly  

Mood matching is the pattern I believe the scoring captures correctly.

- Cases where the recommendations matched your intuition  

During the experiment of weight shift for genre and energy.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Rare-tag starvation: Some moods/genres only exist on one song, so users asking for those get almost no real choice. It would need a bigger catalog or fuzzy mood matching.

Prompts:  

- Features it does not consider 

Song data columns that scoring ignores entirely are tempo_bpm, valence, danceability, and artist/title (only used for the diversity cap, not for matching taste).

Also missing from the model itself:

No listening history or collaborative signal — every recommendation is a one-shot match against a static profile; nothing learns from what the user actually played/skipped/liked before.

No negative preferences choice. e.g. a user can say what genre/mood/energy they want, but can't say what to avoid.

No popularity, recency, or lyrical/cultural content — release date, trending status, language, or explicit content aren't modeled at all.


- Genres or moods that are underrepresented  

Counting occurrences across all 23 songs:

Genres — 12 of 17 appear in only 1 song (single point of failure):
rock, ambient, jazz, classical, hip hop, folk, metal, country, EDM, reggae, blues, techno.

Moods — 10 of 16 appear in only 1 song:
melancholic, triumphant, nostalgic, aggressive, romantic, hopeful, euphoric, playful, somber, mysterious

- Cases where the system overfits to one preference 

In the cases where the energy weightage doubled, in the absence of other feature match, the high energy points single handedly outscore the other recommendations with low energy points.

- Ways the scoring might unintentionally favor some users  

Songs and user profiles with exact mood and energy match.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  

Adversarial Profiles Tested:

"Conflicting mood vs. energy (wants melancholic AND high-energy)",
 {"genre": "classical", "mood": "melancholic", "energy": 0.9, "likes_acoustic": True},
        
"Genre & mood that don't exist in the catalog at all",
{"genre": "opera", "mood": "furious", "energy": 0.5},
        
"Out-of-range target energy (1.4, above the natural 0-1 scale)",
{"genre": "techno", "mood": "mysterious", "energy": 1.4, "likes_acoustic": False},
        
"Messy case/whitespace in genre & mood",
{"genre": "  PoP ", "mood": "HAPPY", "energy": 0.8, "likes_acoustic": None},
        
"Artist-loyalty overload (LoRoom dominates lofi/chill matches)",
{"genre": "lofi", "mood": "chill", "energy": 0.4, "likes_acoustic": True}


- What you looked for in the recommendations  

I mainly looked for the mood and the energy of the user in the current state and used genre as the tie breaker in the recommendation process.

- What surprised you  

The thing that really surprised me is that how the size of the data set determines the limitaions of the system.

- Any simple tests or comparisons you ran  

Before vs. After: what changed when energy started counting for more and genre for less

When a song already nailed both genre AND mood, nothing dethroned it. Winter Sonata (classical/melancholic), Hidden Frequencies (techno/mysterious), and Half Light (indie pop/relaxed) all stayed in 1st place before and after. A double exact-match is still hard to beat even with genre weakened, because mood alone is still worth 2 points.

Songs that only matched on genre (not mood) got shakier. In the "acoustic fence-sitter" test, Rooftop Lights held 3rd place before purely on its genre match. After the change, that genre match was worth less, and it got bumped out of the top spots by songs like Focus Flow, Midnight Coding, and Velvet Whisper — songs with no genre match at all, but whose energy level was simply closer to what the user asked for. In plain terms: being "close to the right vibe" now beats being "the right genre" more often than it used to.

When nothing matched genre or mood anyway, the whole list just got bigger scores, same order. In the "made-up genre/mood" test (opera/furious) and the "messy case" test (PoP/HAPPY), scores roughly doubled across the board, but the ranking of songs didn't move at all — because every song there was competing purely on energy, so everyone got the same boost.

The biggest shake-up was the deliberately "confused" profile (wants a sad, quiet mood and a high-energy song at the same time). Before, a few in-between songs (Dirt Road Sunrise, Coffee Shop Stories) squeaked into the top 5 on modest overall scores. After the change, they got pushed out entirely, replaced by loud, high-energy tracks (Storm Runner, Gym Hero, Sunrise City) that don't fit the mood at all but happen to match the energy target almost exactly. This is the clearest sign of the shift: when genre/mood can't settle the argument, energy now wins the tie-break much more decisively.

Bottom line: the system got more "vibe-driven" and less "genre-loyal." If two songs are otherwise close, the one that feels like the right energy level now has a much better shot at winning, even over one that's technically the right genre. That's good if users care more about mood/energy than genre labels — but it means genre fans (e.g., someone who specifically wants jazz) will more easily see off-genre songs creep into their recommendations if those songs happen to have the right energy.

No need for numeric metrics unless you created some.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  

Use of valence and danceability (loaded by load_songs but never scored). Add a target_valence or wants_danceable preference the same way target_energy/likes_acoustic work now, so users can say "upbeat and danceable" independent of raw energy.

- Better ways to explain recommendations  

Right now explain_recommendation only lists reasons that cleared a threshold (e.g. energy_closeness > 0.85), so a song scored mostly on energy with no reason text still says "closest overall match available" which is uninformative. Use of the score_breakdown dict (already computed in src/recommender.py:196) to always show the dominant contributor by name and magnitude, e.g. "mainly recommended for its energy match (+2.8 of 4.4 points)," even when it's below the current reason-text cutoff.

- Improving diversity among the top results  

Currently select_diverse_top_k only caps by artist — a user can still get 5 songs that are all the same genre+mood if MAX_SONGS_PER_ARTIST allows it. Extend the diversity cap to also limit repeats of genre or mood in the top-k (e.g. max 2 per genre), so a "lofi/chill" fan still sees some variety instead of a wall of near-identical tracks.

- Handling more complex user tastes  

The model assumes one favorite genre/mood/energy per user, but real tastes are contextual ("chill lofi for studying, high-energy EDM for the gym"). Let UserProfile/user_prefs accept a list of weighted preference profiles and score each song against whichever profile fits best, rather than forcing every song through a single fixed target.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems 

I got to learn the logic behind the song recommendations from the music app. How they score the song against the user preferences and comapred througg the data base of songs to hand the top most recommendations.

- Something unexpected or interesting you discovered  

The interesting fact that I discovered is the huge size and feature rich data set tends to provide the most accurate recommendation to the users' given preferences.

- How this changed the way you think about music recommendation apps  

This project forced me to think deeply about the possible ways to get the closest match to the users' preferences and faced systems' increasing complexity on the route.
