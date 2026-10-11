#!/usr/bin/env node
/* C-NEW-89 (run-223): pull ~24 months of Ask HN posts via HN Algolia
 * search_by_date paging (hitsPerPage=1000). Saves raw pages + a compact CSV.
 * Free public API, no key. Politeness: 350ms between calls. */
'use strict';
const fs = require('fs');
const path = require('path');
const OUT = path.join(__dirname, 'data');
fs.mkdirSync(OUT, { recursive: true });
const NOW = Math.floor(Date.now() / 1000);
const FROM = NOW - 24 * 30 * 86400; // ~24 months back
async function page(p) {
  const url = `https://hn.algolia.com/api/v1/search_by_date?tags=ask_hn&hitsPerPage=1000&page=${p}` +
    `&numericFilters=created_at_i>${FROM},created_at_i<${NOW}`;
  const res = await fetch(url, { headers: { 'User-Agent': 'pennyforge-research/0.1' } });
  if (!res.ok) throw new Error(`HTTP ${res.status} page ${p}`);
  return res.json();
}
(async () => {
  // HN Algolia caps retrieval at 1000 hits per query (page*hitsPerPage<=1000),
  // so slice the 24-month window into 2-day slices and page inside each.
  // CORRECTED (run-213): the first pull used ONE page per 2-day slice and was
  // silently truncated (real rate ~730/day > 1000/2days; page 0 = newest 1000 of
  // each window by date order). Now: 2-day slices, page INSIDE each slice until a
  // short page, and reconcile every slice's nbHits against rows actually taken.
  const SLICE = 2 * 86400;
  const rows = [];
  let pages = 0, slices = 0, truncated = 0, nbTotal = 0, mismatch = 0;
  const sliceLog = [];
  for (let lo = FROM; lo < NOW; lo += SLICE) {
    const hi = Math.min(lo + SLICE, NOW);
    slices++;
    let p = 0, taken = 0, sliceNb = 0;
    for (;;) {
      const url = `https://hn.algolia.com/api/v1/search_by_date?tags=ask_hn&hitsPerPage=1000&page=${p}` +
        `&numericFilters=created_at_i>=${lo},created_at_i<${hi}`;
      const res = await fetch(url, { headers: { 'User-Agent': 'pennyforge-research/0.1' } });
      if (!res.ok) throw new Error(`HTTP ${res.status} slice ${lo}`);
      const d = await res.json();
      pages++;
      if (p === 0) { sliceNb = d.nbHits || 0; nbTotal += sliceNb; }
      const hits = d.hits || [];
      for (const h of hits) {
        rows.push({
          id: h.objectID, title: (h.title || '').slice(0, 160), url: h.url || '',
          domain: h.url ? (h.url.match(/^https?:\/\/(?:www\.)?([^\/]+)/) || [])[1] || '' : '',
          points: h.points || 0, num_comments: h.num_comments || 0,
          created_at_i: h.created_at_i, created_at: h.created_at, author: h.author || '',
        });
      }
      taken += hits.length;
      if (hits.length < 1000 || p >= 9) break;
      p++;
      await new Promise((r) => setTimeout(r, 350));
    }
    if (taken !== sliceNb) { truncated++; mismatch += sliceNb - taken; }
    sliceLog.push({ lo, nb: sliceNb, taken });
    if (slices % 60 === 0) console.log(`slice ${slices}: rows ${rows.length}, nbTotal ${nbTotal}`);
    await new Promise((r) => setTimeout(r, 350));
  }
  fs.writeFileSync(path.join(OUT, 'showhn-24mo.json'), JSON.stringify({ pulled_at: new Date().toISOString(), window: { from: FROM, to: NOW }, pages, slices, nbHits_total: nbTotal, rows_taken: rows.length, truncated_slices: truncated, mismatch_rows: mismatch, complete: truncated === 0, sliceLog }, null, 1));
  const csv = ['id,created_at,created_at_i,points,num_comments,author,domain,title,url'];
  for (const r of rows) {
    const esc = (s) => `"${String(s).replace(/"/g, '""')}"`;
    csv.push([r.id, r.created_at, r.created_at_i, r.points, r.num_comments, esc(r.author), esc(r.domain), esc(r.title), esc(r.url)].join(','));
  }
  fs.writeFileSync(path.join(OUT, 'askhn-24mo.csv'), csv.join('\n'));
  console.log(`pages=${pages} rows=${rows.length}`);
})().catch((e) => { console.error('FATAL', String(e).slice(0, 200)); process.exit(3); });
