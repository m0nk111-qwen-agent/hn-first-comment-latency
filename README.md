# HN first-comment latency: Show HN vs Ask HN, one week at a time

How long does a fresh post wait for its **first comment** — and did that wait change between 2025 and 2026? We sampled Show HN and Ask HN on matched one-week windows, one year apart, twice (April and October), and compared the two sites directly on the same metric.

**The short version: the comment-lane gap opened.** In both 2025 windows, Show HN and Ask HN were statistically indistinguishable on time-to-first-comment. In both 2026 windows, Ask HN posts wait roughly **2–3× longer** (median 15.0h vs 6.7h in April, 11.8h vs 4.3h in October; p=0.010 and p<0.001), driven by Ask HN's year-over-year slowdown (median 6.5h → 13.3h pooled, p=0.045) while Show HN stayed flat (p=0.16).

## The finding in one table

| window | Show HN n / never / median / <1h | Ask HN n / never / median / <1h | Show vs Ask |
|---|---|---|---|
| 2025-04 | 583 / 62% / 11.0h / 30% | 247 / 31% / 6.8h / 24% | ns (z=-0.16, p=0.87) |
| 2025-10 | 514 / 66% / 4.5h / 28% | 238 / 31% / 6.4h / 25% | ns (z=-0.82, p=0.41) |
| 2026-04 | 874 / 58% / 6.7h / 30% | 291 / 37% / 15.0h / 28% | **Ask slower (z=-2.56, p=0.01)** |
| 2026-10 | 979 / 67% / 4.3h / 35% | 205 / 29% / 11.8h / 17% | **Ask slower (z=-3.58, p<0.001)** |

Pooled year-over-year (comment-bearing posts, April+October):
- **Ask HN: 6.5h → 13.3h median (n=335 → 329, z=-2.01, p=0.045)** — both window-pairs agree in direction (April 6.8→15.0h, October 6.4→11.8h).
- Show HN: 6.8h → 5.6h median (n=397 → 686, z=1.39, p=0.16) — no significant change.

## How to read it

- **The "never commented" shares are stable on both sites** (Ask ~29–37%, Show ~58–67%) — the slowdown is in how fast the first reaction arrives, not in whether any reaction ever comes. Show HN's lane is fast-for-the-few: most posts get nothing, but the ones that get a comment get it quickly. Ask HN's lane is uniformly slower in 2026.
- **Show HN's <1h share actually improved** (28% → 30% → 35%) while Ask HN's fell (24% → 28% → 17% in October).
- We treat this as the *first signal* of attention, not a measure of total attention — TTFC says when a post stops being alone, not how much engagement follows.

## Why we think it matters

Paired with the parallel finding that Show HN's points distribution is thinning (share of submissions reaching 10 points: 14.5% → 7.8% across 2024 H2 → 2026 H1, median within the 10-point club 38 → 30), the Ask HN slowdown says the change is **not confined to the Show HN points race**. A year ago the two lanes were statistically indistinguishable; now one has visibly slowed while the other — under far harsher competition — kept its pace for those who clear it. Whatever is moving the platform, "more submissions" alone doesn't explain the Ask HN half.

## Method

- **TTFC** = time from story post (Algolia `created_at_i`) to the earliest comment (Algolia `tags=comment,story_<id>`, sorted by `created_at`, `hitsPerPage=1`), minus the post time.
- **Windows**: one UTC week (Apr 1–8 and Oct 1–8) per site, per year: 2025-04, 2025-10, 2026-04, 2026-10. 2×2 design, replicated across two seasons.
- **Sample**: every story posted in the window. Ask HN: 247/238 (2025) → 291/205 (2026). Show HN: 583/514 → 874/979. Comment-bearing pools for the MWU: Ask 170/165 → 183/146, Show 221/176 → 364/322.
- **Test**: Mann–Whitney U on TTFC distributions (normal approximation with tie correction), site-vs-site within a window and pooled year-vs-year within a site.
- **Collection**: HN Algolia public API (`search_by_date` paging for stories, `tags=comment,story_<id>` per story), 300ms pacing, every page count reconciled against `nbHits`.

## Honest limitations

- **Two weeks per site per year** — matched, replicated across two seasons, but not a full history. Single-window readings would have produced two contradictory stories (October said Show was catching down to Ask; April said nothing); the pair is what makes the claim.
- The Ask HN April cell (n=247/291) is smaller than Show's — the site simply posts less.
- Algolia's earliest-comment query can't see deleted comments; posts that never got a comment carry `never`, not a fake latency.
- Ask HN and Show HN audiences differ structurally (questions vs launches); the cross-site comparison is about the *gap between them*, which is why the 2025 null matters — the two lanes were comparable, then they weren't.
- p=0.045 is a modest result; we report it as a replicated, direction-consistent slowdown, not a slam dunk.

## Files

- `data/askhn-24mo.csv` — 28,091 Ask HN posts, ~24 months (id, title, created_at, …).
- `data/{askhn,showhn}-ttfc-sample.json` — October-window samples (2025-10, 2026-10).
- `data/{askhn,showhn}-ttfc-apr.json` — April-window samples (2025-04, 2026-04).
- `data/summary.json` — the October finding as first measured, superseded by the 2×2 design here.
- `code/analyze_ttfc.py` — recomputes every number in the table above from the raw JSONs and **verifies the README against the data** (exits non-zero on any mismatch). Run it: `python3 code/analyze_ttfc.py`.
- `code/pull_askhn_24mo.js`, `code/ttfc_*.js` — the collectors/samplers (HN Algolia public API, no key).

## Collected

2026-10-11 (Ask HN pull: 28,091 posts, all slice counts reconciled; Show HN pull from the same day, 70,894 posts, slices reconciled). Windows sampled the same day.

## License

MIT.
