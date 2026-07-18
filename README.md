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



