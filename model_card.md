# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

**EnergyMatch 1.0**

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

This is for classroom exploration. I wouldn't consider it as a real streaming or recommender app yet as the data is really limited. It takes four preferences from a user (favorite genre, favorite mood, preferred energy level, and whether they like acoustic music) and returns the five best-matching songs from a small catalog. It assumes the user knows their preferences well enough to name a genre and mood, and that those labels match exactly what is in the catalog. It does not learn from listening history and does not personalize over time.

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  


Every song gets a score out of 10. Points are added based on four things:

- Genre match (1.5 pts): If the song's genre exactly matches what you asked for, it earns 1.5 points. No partial credit.
- Mood match (2.5 pts): Same idea — exact match earns 2.5 points, no match earns 0.
- Energy proximity (up to 4 pts): The closer the song's energy is to your target, the more points it earns. A perfect match gives all 4. A big gap gives close to 0. This is the heaviest single factor.
- Acousticness proximity (up to 1.5 pts): If you like acoustic music, songs with high acousticness score better. If not, low acousticness scores better. Same distance math as energy.
- Valence bonus (up to 0.5 pts): Every song gets a small bonus based on how emotionally positive it sounds. This is fixed at a target of 0.70 — the user cannot change it.

The five songs with the highest totals are returned. One change from the starter logic was that the energy weight was doubled (from 2.0 to 4.0) and the genre weight was halved (from 3.0 to 1.5) to reduce how easily a genre label match could override a strong energy mismatch.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

The catalog has 17 songs. Each song has a genre label, a mood label, and numeric values for energy, tempo, valence, danceability, and acousticness. There are 15 different genres — only lofi appears more than once (3 songs). Most moods appear exactly once.

No songs were added or removed from the starter dataset.

What is missing: no Latin, K-pop, or R&B subgenres. No "sad" or "melancholic" mood options on pop or rock songs. The energy range is uneven — most songs cluster at the low end (lofi, classical) or high end (EDM, metal), with few songs in the 0.5–0.65 middle range. With only one song per genre in most cases, so if a genre mismatch happens, there is nothing else to fall back on.

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

The system works best when a user's preferences align closely with what the catalog has. A lofi study listener gets strong results — three lofi songs exist, they all have low energy and high acousticness, and they score consistently well. A rock listener asking for intense high-energy music gets Storm Runner at the top, which feels like exactly the right call.

The scoring is fully transparent. Every reason a song ranked where it did is printed in the output. Nothing is hidden or guessed. That makes it easy to check whether the system is doing the right thing — or catch it when it is not.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

The current system creates a categorical filter bubble around genre and mood labels: because genre and mood together contribute up to 4.0 out of 10.0 points while the energy term contributes at most 4.0 points only when the match is near-perfect. So a user who wants a high-energy version of a typically low-energy genre (e.g., lofi at energy 0.9) will still receive low-energy lofi songs ranked first — the label match overrides their explicit energy preference entirely. This means users whose taste crosses genre boundaries are invisible in the scoring and will always receive recommendations that satisfy the label but contradict the feeling they asked for. 

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

Ten user profiles were tested in total: four baseline profiles covering realistic listener types (happy pop fan, lofi study listener, rock/intense workout listener, and a near-identical pop variant) and six adversarial profiles designed to stress-test the scoring logic (a mood that doesn't exist in the catalog, a lofi listener who wants high energy, an out-of-range energy value of 1.5, wrong capitalisation on genre and mood, a metal listener whose genre is absent from the dataset, and a completely empty profile with no preferences at all).

What we looked for was whether the top-ranked song actually matched the spirit of the request — not just which song scored highest, but whether a real person would agree it was a reasonable recommendation. For normal profiles, the results were intuitive: the lofi study listener got quiet acoustic songs, the rock listener got Storm Runner. The surprises appeared in the adversarial cases. The most unexpected result was the capitalisation test: typing "Pop" instead of "pop" caused the system to silently ignore the genre entirely, and a hip-hop song (Block Party Anthem) tied for first place with the actual pop song the user wanted — with no error or explanation. A second surprise was the empty profile: with no preferences set at all, the scorer still returned a ranked list, placing Coffee Shop Stories at the top purely because its emotional tone (valence) happened to be close to an invisible default value hardcoded in the formula. The system behaved as if it had a preference the user never expressed.

Testing also revealed that "Gym Hero" — a high-energy pop workout track — consistently appeared in the top three for happy pop listeners even though its mood is listed as "intense," not "happy." This happens because the genre label ("pop") earns it points, and its energy (0.93) is numerically close enough to a target of 0.80 that the energy component adds to its score rather than hurting it. In plain terms, the system sees "it's a pop song and its tempo roughly matches what you asked for" and promotes it, without understanding that a user who wants happy background music probably doesn't want a track designed for sprinting. The scorer has no concept of whether a song's purpose fits a listener's context — only whether its numbers are in the right range.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

1. Let users express a valence preference
Right now valence is hardcoded to target 0.70. A dark-music fan is quietly penalized on every song without knowing it. Adding a "mood brightness" input would fix this and make the scorer honest.

2. Grow and balance the catalog
Most genres have only one song. Adding 3–5 songs per genre would give energy and mood room to actually differentiate results within a genre — which is what a real recommender needs to do.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

Building this made me understand how much a scoring system can look like it is working while quietly ignoring what the user asked for. Something unexpected that happened was when I previously had a capitalisation bug and the output looked completely normal, scores were printed, and nothing flagged an error. In a real app, a user would just assume the recommendations were bad and leave, never knowing their input was thrown away.
This didn't really change the way I though about music recommendation apps. I don't follow their recommendations often but I believe one of the shifts in my thinking was that real recommenders inputs are not just math. They encode assumptions about what "good music" means. Those assumptions can exclude whole categories of users without anyone noticing. Making the scoring logic visible and testable is one of the most important things a system like this can do.

How did using AI tools help you, and when did you need to double-check them?
What would you try next if you extended this project?
Using AI tools helped in understanding how the big recommender apps such as Spotify work and how my current implementation differs from them.
I will add a variance input for users just so listeners who love sad or solemn music don't get penalized as often.