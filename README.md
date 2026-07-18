# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Explain your design in plain language.

Real-world music apps like Spotify don't actually know what user want. They watch what you've listened to before, compare it against millions of other songs, and guess based on patterns. My design works the same basic way, just much smaller and completely see-through. Instead of learning from years of history, it takes a quick snapshot of what user is in the mood for right now and does the matching math.

Some prompts to answer:

- What features does each `Song` use in your system

Each Song carries four traits/features that matter for matching: "genre" (the broad style, like pop or lofi), "mood" (the vibe, like happy or chill), "energy" (how intense it feels, from calm to high-energy), and "acousticness" (how stripped-down/acoustic vs. produced it sounds). Two other columns exist in the data i.e. "tempo_bpm" and "danceability" which aren't used, because in this catalog they basically move in step with "energy"; including them would just count the same thing twice.

  
- What information does your `UserProfile` store

The "UserProfile" isn't a listening history rather it's a one-time snapshot of what user want right now: "favorite_genre", "mood", a "target_energy" the user is aiming for, and whether the user likes "acoustic" sounds.

- How does your `Recommender` compute a score for each song

To score a song, the "Recommender" adds up points for every way it matches what the user asked for, but not all matches count equally. Mood and energy are weighted the heaviest on purpose, because my philosophy is to match user's mood in the moment, not lock onto a fixed identity like "you are a pop fan." Genre mostly breaks ties between songs that already feel right.

- How do you choose which songs to recommend

A single score means nothing on its own. It only matters compared to every other song's score, which is why scoring one song and ranking the whole list are two separate steps, and together will be used to recommend a song.

You can include a simple diagram or bullet list if helpful.

Design biases identified and their fixes:

1. Rare-tag starvation: Some moods/genres only exist on one song, so users asking for those get almost no real choice. (not fixed — would need a bigger catalog or fuzzy mood matching)

2. Typo/case sensitivity:"R&B" vs "r&b" would count as no match at all, even though they're the same thing. ✅ Fixed — comparisons now ignore case/spacing.

3. Mood matters more than genre: A deliberate design choice, but it means genre-loyal users get less weight than mood-driven users. (not fixed — this is the philosophy we chose on purpose)

4. Energy "dead zone": The catalog had almost no songs in the middle energy range, so anyone wanting medium energy got a poor match. ✅ Fixed — added 3 songs to fill that gap.

5. Inconsistent acoustic preference: The demo profile wasn't actually passing the acoustic preference correctly, so that whole part of the score was silently doing nothing. ✅ Fixed — corrected so it now works as intended.

6. Same-artist pileup — nothing stopped one artist from taking multiple spots in the top results. ✅ Fixed — recommendations now cap out at 2 songs per artist.

Bottom line: Fixed the "silent bugs" (typos, the broken acoustic setting, one artist crowding the list) and improved the data (filled the energy gap). Left the two things that are really just design opinions — mood mattering more than genre, and rare tags being rare — since those are conscious trade-offs, not mistakes.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:
Terminal Ouput: 

```````````````````````````````````````````````````````````

User Profile
========================================
genre: lofi
mood: chill
energy: 0.6
likes_acoustic: True

Top 5 Recommendations
========================================

1. Library Rain (Paper Lanterns) - Score: 4.99
   - genre 'lofi' matches your favorite
   - mood 'chill' fits what you're looking for
   - acoustic level fits your preference

2. Midnight Coding (LoRoom) - Score: 4.94
   - genre 'lofi' matches your favorite
   - mood 'chill' fits what you're looking for
   - acoustic level fits your preference

3. Spacewalk Thoughts (Orbit Bloom) - Score: 3.94
   - mood 'chill' fits what you're looking for
   - acoustic level fits your preference

4. Focus Flow (LoRoom) - Score: 2.98
   - genre 'lofi' matches your favorite
   - acoustic level fits your preference

5. Dirt Road Sunrise (Hazel County) - Score: 2.07
   - energy (0.62) is close to your target (0.60)

`````````````````````````````````````````````````````````````````````````````

Commit Message for summary of implementation:

Implement scoring and ranking for a working CLI-first recommender simulation

- Add mood-first weighted scoring (_score_song) shared by both the
  dict-based (score_song/recommend_songs) and dataclass-based
  (Recommender) code paths, per the "match the moment" philosophy
  (mood=2.0 > energy=1.5 > genre=1.0 = acousticness=1.0)
- Add artist-diversity capped ranking (_select_diverse_top_k) so one
  prolific artist can't crowd out the top-k results
- Implement load_songs CSV parsing with numeric field casting
- Normalize genre/mood string comparisons to avoid case/whitespace
  mismatches
- Expand the catalog to 23 songs for broader genre/mood/energy coverage
- Reformat main.py's terminal output into a numbered, readable report
  showing the user profile and each recommendation's score and reasons

Running `python src/main.py` now demonstrates a fully working,
CLI-first simulation of the recommender end to end.


########################################
Adversarial / Edge-Case Profiles
########################################

Conflicting mood vs. energy (wants melancholic AND high-energy)
========================================
genre: classical
mood: melancholic
energy: 0.9
likes_acoustic: True

Top 5 Recommendations
----------------------------------------

1. Winter Sonata (Aria Wren) - Score: 4.40
   Breakdown: genre=+1.00, mood=+2.00, energy=+0.45, acoustic=+0.95
   - genre 'classical' matches your favorite
   - mood 'melancholic' fits what you're looking for
   - acoustic level fits your preference

2. Dirt Road Sunrise (Hazel County) - Score: 1.68
   Breakdown: genre=+0.00, mood=+0.00, energy=+1.08, acoustic=+0.60
   - closest overall match available

3. Rooftop Lights (Indigo Parade) - Score: 1.64
   Breakdown: genre=+0.00, mood=+0.00, energy=+1.29, acoustic=+0.35
   - energy (0.76) is close to your target (0.90)

4. Coffee Shop Stories (Slow Stereo) - Score: 1.59
   Breakdown: genre=+0.00, mood=+0.00, energy=+0.70, acoustic=+0.89
   - acoustic level fits your preference

5. Storm Runner (Voltline) - Score: 1.58
   Breakdown: genre=+0.00, mood=+0.00, energy=+1.48, acoustic=+0.10
   - energy (0.91) is close to your target (0.90)

Genre & mood that don't exist in the catalog at all
========================================
genre: opera
mood: furious
energy: 0.5

Top 5 Recommendations
----------------------------------------

1. Half Light (Sable Lane) - Score: 1.47
   Breakdown: genre=+0.00, mood=+0.00, energy=+1.47
   - energy (0.48) is close to your target (0.50)

2. Velvet Whisper (Marlo Reyes) - Score: 1.42
   Breakdown: genre=+0.00, mood=+0.00, energy=+1.42
   - energy (0.55) is close to your target (0.50)

3. Island Sway (Kalo Roots) - Score: 1.38
   Breakdown: genre=+0.00, mood=+0.00, energy=+1.38
   - energy (0.58) is close to your target (0.50)

4. Midnight Coding (LoRoom) - Score: 1.38
   Breakdown: genre=+0.00, mood=+0.00, energy=+1.38
   - energy (0.42) is close to your target (0.50)

5. Focus Flow (LoRoom) - Score: 1.35
   Breakdown: genre=+0.00, mood=+0.00, energy=+1.35
   - energy (0.40) is close to your target (0.50)

Out-of-range target energy (1.4, above the natural 0-1 scale)
========================================
genre: techno
mood: mysterious
energy: 1.4
likes_acoustic: False

Top 5 Recommendations
----------------------------------------

1. Hidden Frequencies (Vex Silo) - Score: 4.52
   Breakdown: genre=+1.00, mood=+2.00, energy=+0.57, acoustic=+0.95
   - genre 'techno' matches your favorite
   - mood 'mysterious' fits what you're looking for
   - acoustic level fits your preference

2. Iron Verdict (Grave Circuit) - Score: 1.83
   Breakdown: genre=+0.00, mood=+0.00, energy=+0.86, acoustic=+0.97
   - acoustic level fits your preference

3. Pulse Ignition (DJ Kinetic) - Score: 1.81
   Breakdown: genre=+0.00, mood=+0.00, energy=+0.83, acoustic=+0.98
   - acoustic level fits your preference

4. Gym Hero (Max Pulse) - Score: 1.75
   Breakdown: genre=+0.00, mood=+0.00, energy=+0.80, acoustic=+0.95
   - acoustic level fits your preference

5. Storm Runner (Voltline) - Score: 1.67
   Breakdown: genre=+0.00, mood=+0.00, energy=+0.77, acoustic=+0.90
   - acoustic level fits your preference

Messy case/whitespace in genre & mood
========================================
genre:   PoP 
mood: HAPPY
energy: 0.8
likes_acoustic: None

Top 5 Recommendations
----------------------------------------

1. Sunrise City (Neon Echo) - Score: 4.47
   Breakdown: genre=+1.00, mood=+2.00, energy=+1.47
   - genre 'pop' matches your favorite
   - mood 'happy' fits what you're looking for
   - energy (0.82) is close to your target (0.80)

2. Rooftop Lights (Indigo Parade) - Score: 3.44
   Breakdown: genre=+0.00, mood=+2.00, energy=+1.44
   - mood 'happy' fits what you're looking for
   - energy (0.76) is close to your target (0.80)

3. Gym Hero (Max Pulse) - Score: 2.30
   Breakdown: genre=+1.00, mood=+0.00, energy=+1.30
   - genre 'pop' matches your favorite
   - energy (0.93) is close to your target (0.80)

4. Crown Up (Big Mecca) - Score: 1.50
   Breakdown: genre=+0.00, mood=+0.00, energy=+1.50
   - energy (0.80) is close to your target (0.80)

5. Hidden Frequencies (Vex Silo) - Score: 1.47
   Breakdown: genre=+0.00, mood=+0.00, energy=+1.47
   - energy (0.78) is close to your target (0.80)

Artist-loyalty overload (LoRoom dominates lofi/chill matches)
========================================
genre: lofi
mood: chill
energy: 0.4
likes_acoustic: True

Top 5 Recommendations
----------------------------------------

1. Library Rain (Paper Lanterns) - Score: 5.29
   Breakdown: genre=+1.00, mood=+2.00, energy=+1.42, acoustic=+0.86
   - genre 'lofi' matches your favorite
   - mood 'chill' fits what you're looking for
   - energy (0.35) is close to your target (0.40)
   - acoustic level fits your preference

2. Midnight Coding (LoRoom) - Score: 5.18
   Breakdown: genre=+1.00, mood=+2.00, energy=+1.47, acoustic=+0.71
   - genre 'lofi' matches your favorite
   - mood 'chill' fits what you're looking for
   - energy (0.42) is close to your target (0.40)
   - acoustic level fits your preference

3. Spacewalk Thoughts (Orbit Bloom) - Score: 4.24
   Breakdown: genre=+0.00, mood=+2.00, energy=+1.32, acoustic=+0.92
   - mood 'chill' fits what you're looking for
   - energy (0.28) is close to your target (0.40)
   - acoustic level fits your preference

4. Focus Flow (LoRoom) - Score: 3.28
   Breakdown: genre=+1.00, mood=+0.00, energy=+1.50, acoustic=+0.78
   - genre 'lofi' matches your favorite
   - energy (0.40) is close to your target (0.40)
   - acoustic level fits your preference

5. Coffee Shop Stories (Slow Stereo) - Score: 2.35
   Breakdown: genre=+0.00, mood=+0.00, energy=+1.46, acoustic=+0.89
   - energy (0.37) is close to your target (0.40)
   - acoustic level fits your preference

Acoustic fence-sitter comparison (likes_acoustic=True vs. False)
========================================

likes_acoustic=True
========================================
genre: indie pop
mood: relaxed
energy: 0.48
likes_acoustic: True

Top 5 Recommendations
----------------------------------------

1. Half Light (Sable Lane) - Score: 5.00
   Breakdown: genre=+1.00, mood=+2.00, energy=+1.50, acoustic=+0.50
   - genre 'indie pop' matches your favorite
   - mood 'relaxed' fits what you're looking for
   - energy (0.48) is close to your target (0.48)

2. Coffee Shop Stories (Slow Stereo) - Score: 4.22
   Breakdown: genre=+0.00, mood=+2.00, energy=+1.33, acoustic=+0.89
   - mood 'relaxed' fits what you're looking for
   - energy (0.37) is close to your target (0.48)
   - acoustic level fits your preference

3. Rooftop Lights (Indigo Parade) - Score: 2.43
   Breakdown: genre=+1.00, mood=+0.00, energy=+1.08, acoustic=+0.35
   - genre 'indie pop' matches your favorite

4. Old Porch Letters (Willow Creek) - Score: 2.18
   Breakdown: genre=+0.00, mood=+0.00, energy=+1.28, acoustic=+0.90
   - energy (0.33) is close to your target (0.48)
   - acoustic level fits your preference

5. Library Rain (Paper Lanterns) - Score: 2.17
   Breakdown: genre=+0.00, mood=+0.00, energy=+1.30, acoustic=+0.86
   - energy (0.35) is close to your target (0.48)
   - acoustic level fits your preference

likes_acoustic=False
========================================
genre: indie pop
mood: relaxed
energy: 0.48
likes_acoustic: False

Top 5 Recommendations
----------------------------------------

1. Half Light (Sable Lane) - Score: 5.00
   Breakdown: genre=+1.00, mood=+2.00, energy=+1.50, acoustic=+0.50
   - genre 'indie pop' matches your favorite
   - mood 'relaxed' fits what you're looking for
   - energy (0.48) is close to your target (0.48)

2. Coffee Shop Stories (Slow Stereo) - Score: 3.44
   Breakdown: genre=+0.00, mood=+2.00, energy=+1.33, acoustic=+0.11
   - mood 'relaxed' fits what you're looking for
   - energy (0.37) is close to your target (0.48)

3. Rooftop Lights (Indigo Parade) - Score: 2.73
   Breakdown: genre=+1.00, mood=+0.00, energy=+1.08, acoustic=+0.65
   - genre 'indie pop' matches your favorite

4. Velvet Whisper (Marlo Reyes) - Score: 2.09
   Breakdown: genre=+0.00, mood=+0.00, energy=+1.40, acoustic=+0.70
   - energy (0.55) is close to your target (0.48)

5. Hidden Frequencies (Vex Silo) - Score: 2.00
   Breakdown: genre=+0.00, mood=+0.00, energy=+1.05, acoustic=+0.95
   - acoustic level fits your preference


**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



