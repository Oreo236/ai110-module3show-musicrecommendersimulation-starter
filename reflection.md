# Reflection: Profile Pair Comparisons

Each section below compares two user profiles and explains what changed in the output and why.

---

## Pair 1 — Baseline pop/happy/0.8 vs. Baseline pop/happy/0.85

**Top results were nearly identical.** Sunrise City held first place at 9.99 for both. Rooftop Lights stayed second, and Gym Hero stayed third. The only meaningful difference was that Gym Hero scored slightly higher for the 0.85 target (7.46 vs 7.41) because its energy of 0.93 is a little closer to 0.85 than it is to 0.80. This makes sense: the scoring formula rewards closeness, and 0.08 gap is smaller than 0.13 gap. The takeaway is that small changes in the energy target barely affect recommendations when the catalog doesn't have songs between those two values — the same songs win in the same order.

---

## Pair 2 — pop/happy/0.8 (baseline) vs. pop/sad/0.8 (ADV 1 — mood doesn't exist)

**Sunrise City dropped from 9.99 to 7.49.** In the baseline, it earned points for both genre ("pop") and mood ("happy"). In the sad-mood profile, mood never matched anything in the catalog — "sad" simply doesn't exist as a label. So every song lost 2.5 points off its potential score, and the system returned a ranking based purely on genre and energy proximity. Rooftop Lights, which had ranked second in the baseline by riding a mood match, fell out of the top 5 entirely because it is listed as "indie pop" (not "pop") and now had nothing to earn points from. The system gave no warning that the mood preference was unmet — it just quietly returned lower scores and acted as if everything was fine.

---

## Pair 3 — lofi/chill/0.38 acoustic (baseline) vs. lofi/chill/0.9 acoustic (ADV 2 — energy conflict)

**The same two songs ranked first and second, but their scores dropped noticeably.** Library Rain and Midnight Coding are the two lofi-chill songs in the catalog, so they matched on genre and mood in both cases. The difference is energy: at target 0.38, Library Rain (energy 0.35) is nearly a perfect match and scores 9.99. At target 0.90, that same song has an energy gap of 0.55, which pulls its score down to 8.78. The lofi songs still win because the genre+mood labels together outweigh the energy penalty — but the gap between first place and the rest of the list narrowed significantly. This reveals the filter bubble: a user who wants the calm aesthetic of lofi but the physical intensity of a workout track will still receive sleepy study music, just with a slightly lower score.

---

## Pair 4 — pop/happy/0.8 (baseline) vs. Pop/Happy/0.8 (ADV 4 — capitalisation)

**This is the most dramatic difference of any pair.** The baseline profile returns Sunrise City at 9.99 with confident genre and mood matches. The capitalised profile returns Sunrise City at only 3.99 — tied with Block Party Anthem, a hip-hop song. The entire difference is a capital P and a capital H. The system uses exact string comparison, so "Pop" ≠ "pop" and "Happy" ≠ "happy." With no categorical matches at all, every song scored exactly the same on genre and mood (zero), and the ranking collapsed into a tiebreaker contest driven only by energy proximity and acousticness. Block Party Anthem crept into first place not because it's a good match, but because its energy (0.85) happened to be close to the target and its acousticness was low. This shows the system has no tolerance for user input variation and no way to tell the user their preferences were silently ignored.

---

## Pair 5 — rock/intense/0.92 (baseline) vs. metal/angry/0.97 (ADV 5 — genre absent from catalog)

**Both profiles want aggressive, high-energy music, and both got reasonable results — but for different reasons.** The rock profile found Storm Runner (the only rock song) and placed it first at 9.97 with a clean genre and mood match. The metal profile found Iron Curtain Fall (the only metal song) and also placed it first at 9.41. The surprise here is that the metal profile's #2 result was Gym Hero (pop/intense, 3.98) — not another metal or heavy song. Once Iron Curtain Fall used up the genre and mood points, the rest of the list was decided by energy alone, and Gym Hero's energy (0.93) was the closest to 0.97 among the remaining songs. Two very different songs (a metal track and a pop gym anthem) share the same energy range, so they end up as neighbours in the ranking despite having nothing else in common.

---

## Pair 6 — pop/happy/0.8 (baseline) vs. empty profile {} (ADV 6 — no preferences)

**The baseline returns meaningful, genre-appropriate songs. The empty profile returns a meaningless list tied at 0.50.** In the baseline, Sunrise City wins convincingly because it matches on genre, mood, energy, and acousticness. In the empty profile, there is no genre, no mood, and no energy preference — but the system still runs and still returns a ranked list. Coffee Shop Stories (a jazz track) ranked first. It didn't win because it's a good fit for the user; it won because its valence (0.71) is one of the closest values to 0.70, which is the hidden fixed target baked into the scoring formula. The user expressed zero preferences, but the system behaved as if they had asked for emotionally balanced music. This is a hidden bias: the valence default quietly steers every recommendation, including this one, toward a particular emotional tone that was never requested.
