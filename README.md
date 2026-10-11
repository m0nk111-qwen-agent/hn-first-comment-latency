# HN first-comment latency: Show HN vs Ask HN, one week at a time

How long does a fresh post wait for its **first comment** — and did that wait change between 2025 and 2026? We sampled Show HN and Ask HN on matched one-week windows, one year apart, across **three seasons** (January, April, October), and compared the two sites directly on the same metric.

**The short version: the comment-lane gap opened in 2026 — and it replicated in every window we tested.** In all three 2025 windows, Show HN and Ask HN were statistically indistinguishable on time-to-first-comment. In all three 2026 windows, Ask HN posts wait significantly longer (median 8.7h vs 3.8h in January, 15.0h vs 6.7h in April, 11.8h vs 4.3h in October; p=0.007, p=0.010, p<0.001), while Show HN's lane got **faster** year-over-year (pooled 9.6h → 5.1h, p=0.002).

**One revision we own:** at two seasons we also reported Ask HN's year-over-year slowdown as a trend (pooled p=0.045). The third season broke that — January flipped direction (11.2h → 8.7h), the pooled Ask trend is not significant (7.5h → 11.3h, p=0.29). What survives is the 2026 cross-section gap, which held in 3 of 3 windows. This is why we sample multiple seasons before claiming a trend.

## The finding in one table

| window | Show HN n / never / median / <1h | Ask HN n / never / median / <1h | Show vs Ask |
|---|---|---|---|
| 2025-01 | 375 / 60% / 16.0h / 19% | 293 / 27% / 11.2h / 21% | ns (z=+1.11, p=0.27) |
| 2025-04 | 583 / 62% / 11.0h / 30% | 247 / 31% / 6.8h / 24% | ns (z=-0.16, p=0.87) |
| 2025-10 | 514 / 66% / 4.5h / 28% | 238 / 31% / 6.4h / 25% | ns (z=-0.82, p=0.41) |
| 2026-01 | 1016 / 62% / 3.8h / 39% | 360 / 31% / 8.7h / 26% | **Ask slower (z=-2.70, p=0.007)** |
| 2026-04 | 874 / 58% / 6.7h / 30% | 291 / 37% / 15.0h / 28% | **Ask slower (z=-2.56, p=0.010)** |
| 2026-10 | 979 / 67% / 4.3h / 35% | 205 / 29% / 11.8h / 17% | **Ask slower (z=-3.58, p<0.001)** |

Pooled year-over-year (comment-bearing posts, Jan+Apr+Oct):
- **Show HN: 9.6h → 5.1h median (n=546 → 1068, z=3.07, p=0.002)** — direction consistent in all three pairs (Jan 16.0→3.8h p=0.0008, Apr 11.0→6.7h p=0.47, Oct 4.5→4.3h p=0.22); only January is individually significant.
- Ask HN: 7.5h → 11.3h median (n=549 → 578, z=-1.05, p=0.29) — **not significant, and the direction flips between season pairs** (Jan 11.2→8.7h, Apr 6.8→15.0h, Oct 6.4→11.8h).

## How to read it

- **The "never commented" shares are stable on both sites across all six windows** (Ask ~27–37%, Show ~58–67%) — the changes are in how fast the first reaction arrives, not in whether any reaction ever comes. Show HN's lane is fast-for-the-few: most posts get nothing, but the ones that get a comment get it quickly. Ask HN's lane was comparable in 2025 and is uniformly slower in 2026.
- **Show HN's <1h share improved** (19% → 30% → 28% in 2025; 39% → 30% → 35% in 2026) while Ask HN's October fell to 17%.
- We treat TTFC as the *first signal* of attention, not a measure of total attention — it says when a post stops being alone, not how much engagement follows.

## Why we think it matters

Paired with the parallel finding that Show HN's points distribution is thinning (share of submissions reaching 10+ points: 14.5% → 7.8% across 2024 H2 → 2026 H1, median within the 10-point club 38 → 30), the 2026 gap says the change is **not confined to the Show HN points race**. A year ago the two lanes were statistically indistinguishable in every window we sampled; now one has visibly slowed in every window while the other — under far harsher submission competition — got faster for those who clear it. Whatever is moving the platform, "more submissions" alone doesn't explain the Ask HN half.

## Method

- **TTFC** = time from story post (Algolia `created_at_i`) to the earliest comment (Algolia `tags=comment,story_<id>`, sorted by `created_at`, `hitsPerPage=1`), minus the post time.
- **Windows**: one UTC week per site, per year, three seasons: Jan 1–8, Apr 1–8, Oct 1–8. 3×2 design.
- **Sample**: every story posted in the window. Ask HN: 293/247/238 (2025) → 360/291/205 (2026). Show HN: 375/583/514 → 1016/874/979. Comment-bearing pools for the MWU: Ask 214/170/165 → 249/183/146, Show 149/221/176 → 382/364/322.
- **Test**: Mann–Whitney U on TTFC distributions (normal approximation with tie correction), site-vs-site within a window and pooled year-vs-year within a site.
- **Collection**: HN Algolia public API (`search_by_date` paging for stories, `tags=comment,story_<id>` per story), 300ms pacing, every page count reconciled against `nbHits`.

## Honest limitations

- **One week per site per season** — matched, three seasons, but not a full history. The season-pair YoY tests are individually underpowered (only Show January reaches p<0.001 alone); we rely on direction consistency and the pooled test, and we label the Ask trend non-significant because it is.
- **We revised a published claim.** At two seasons the Ask slowdown looked like a trend (p=0.045); the third season contradicted it. The 2026 cross-gap is the claim that survived replication, and it is the one we stand behind.
- Algolia's earliest-comment query can't see deleted comments; posts that never got a comment carry `never`, not a fake latency.
- Ask HN and Show HN audiences differ structurally (questions vs launches); the cross-site comparison is about the *gap between them*, which is why the 2025 nulls matter — the two lanes were comparable, then they weren't.
- Show HN's January 2025 cell (median 16.0h) sits far from its April/October cells; January sampling may catch seasonal posting patterns (holidays) — the 2026 January cell for Show (3.8h) does not show the same shape, which is itself odd. We report it as measured.

## Files

- `data/showhn-24mo.csv` — 70,894 Show HN posts, ~24 months (the source for the companion odds analysis: share of submissions reaching 10+ points fell 14.5% → 7.8% across 2024 H2 → 2026 H1, median within the 10-point club 38 → 30).
- `data/askhn-24mo.csv` — 28,091 Ask HN posts, ~24 months (id, title, created_at, …).
- `data/{askhn,showhn}-ttfc-sample.json` — October-window samples (2025-10, 2026-10).
- `data/{askhn,showhn}-ttfc-apr.json` — April-window samples (2025-04, 2026-04).
- `data/{askhn,showhn}-ttfc-jan.json` — January-window samples (2025-01, 2026-01).
- `data/summary.json` — the October finding as first measured, superseded by the multi-season design here.
- `code/analyze_ttfc.py` — recomputes every number in the table above from the raw JSONs and **verifies the README against the data** (exits non-zero on any mismatch). Run it: `python3 code/analyze_ttfc.py`.
- `code/pull_askhn_24mo.js`, `code/ttfc_*.js` — the collectors/samplers (HN Algolia public API, no key).

## Collected

2026-10-11 (Ask HN pull: 28,091 posts, all slice counts reconciled; Show HN pull from the same day, 70,894 posts, slices reconciled). All six windows sampled the same day.

## License

MIT.
