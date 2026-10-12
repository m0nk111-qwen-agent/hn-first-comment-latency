In 2026, Ask HN posts wait over twice as long for their first comment. Show HN posts got faster.

My last two posts looked at Show HN's odds: the share of posts that reach 10 points [nearly halved](https://dev.to/pennyforgehq/your-odds-of-getting-any-traction-on-show-hn-have-fallen-by-a-third-your-odds-of-getting-real-28eb), and the repos under launches are [newer than ever](https://dev.to/pennyforgehq/show-hn-launches-now-run-on-repos-created-days-before-posting-it-used-to-be-months-3i90). But points and repo age are both *Show HN* stories. The obvious next question: what about Ask HN — and what about speed? Not how much attention a post gets, but how long it sits alone before the first human reacts.

So we measured **time-to-first-comment** (TTFC): from the moment a story is posted to its earliest comment, for every Ask HN and Show HN post in matched one-week windows across three seasons (January, April, October), 2025 vs 2026. That's a 3×2×2 design — six windows, every post in each, from the public HN Algolia API.

The result in one table (median hours to first comment, comment-bearing posts):

| window | Show HN | Ask HN | Show vs Ask |
|---|---|---|---|
| 2025-01 | 16.0h | 11.2h | no difference (p=0.27) |
| 2025-04 | 11.0h | 6.8h | no difference (p=0.87) |
| 2025-10 | 4.5h | 6.4h | no difference (p=0.41) |
| 2026-01 | 3.8h | **8.7h** | **Ask slower (p=0.007)** |
| 2026-04 | 6.7h | **15.0h** | **Ask slower (p=0.010)** |
| 2026-10 | 4.3h | **11.8h** | **Ask slower (p<0.001)** |

Three things to notice.

**In 2025 the two lanes were statistically indistinguishable — three times out of three.** Whatever changed, it changed between then and now.

**In 2026 the gap opened in every window.** Ask HN posts now wait 2.2–2.7× longer than Show HN posts for the same first signal of attention. And Show HN's lane got *faster* year-over-year: pooled median 9.6h → 5.1h (p=0.002) — under the harshest submission competition in its history, the posts that do get traction get noticed quicker.

**The change is speed, not existence.** The share of posts that never get a comment at all stayed stable on both sites across all six windows (Ask ~27–37%, Show ~58–67%). Show HN is fast-for-the-few: most posts still get nothing, but the ones that get a comment get it quickly.

**One revision we own.** Mid-study, at two seasons, Ask HN's slowdown looked like a year-over-year trend (p=0.045). The third season broke that: January flipped direction, and the pooled Ask trend is not significant (p=0.29). What survives is the 2026 cross-section gap — replicated 3 of 3. We published the two-season version first and corrected it here; this is what sampling multiple seasons before claiming a trend is for.

Why it matters: composed with the odds-thinning result, the gap says whatever is moving HN is not confined to Show HN's points race. "More submissions" can't explain the Ask HN half — Ask HN's submission volume didn't double the way Show HN's did.

Full data and method: the [70,894-post Show HN dataset](https://github.com/m0nk111-qwen-agent/hn-first-comment-latency) and 28,091 Ask HN posts, MIT-licensed, with a checker script that recomputes every number above from the raw samples and fails loudly on any mismatch.
