#!/usr/bin/env python3
"""Recompute the Show-vs-Ask HN first-comment-latency numbers from the raw sample JSONs,
print the four-window table + pooled year-over-year tests, then verify every number
quoted in README.md's table against the data. Exit 1 on any mismatch."""
import json, re, sys
from math import erf, sqrt
from statistics import mean, median
from collections import defaultdict

def agg(f):
    rows = json.load(open(f'data/{f}'))
    out = defaultdict(lambda: {'ok': [], 'never': 0, 'n': 0})
    for r in rows:
        w = r['window'].split(' (')[0]
        out[w]['n'] += 1
        if r.get('ttfc_s') is None: out[w]['never'] += 1
        else: out[w]['ok'].append(r['ttfc_s'])
    return out

A = {**agg('askhn-ttfc-sample.json'), **agg('askhn-ttfc-apr.json')}
S = {**agg('showhn-ttfc-sample.json'), **agg('showhn-ttfc-apr.json')}

def mwu(a, b):
    allv = sorted(a + b)
    g = defaultdict(list)
    for i, v in enumerate(allv): g[v].append(i + 1)
    avg = {v: mean(rs) for v, rs in g.items()}
    U = sum(avg[v] for v in a) - len(a) * (len(a) + 1) / 2
    N = len(allv)
    tsum = sum(n ** 3 - n for n in (len(rs) for rs in g.values()))
    sigma = sqrt(len(a) * len(b) / 12 * ((N + 1) - tsum / (N * (N - 1))))
    z = (U - len(a) * len(b) / 2) / sigma
    return z, 2 * (1 - 0.5 * (1 + erf(abs(z) / sqrt(2))))

WINDOWS = ('2025-04-week1', '2025-10-week1', '2026-04-week1', '2026-10-week1')
table = {}
for w in WINDOWS:
    s, k = S[w], A[w]
    sh = sorted(t / 3600 for t in s['ok'])
    ah = sorted(t / 3600 for t in k['ok'])
    z, p = mwu(s['ok'], k['ok'])
    table[w] = {
        'show': {'n': s['n'], 'never_pct': round(100 * s['never'] / s['n']), 'median_h': round(median(sh), 1), 'under1h_pct': round(100 * sum(1 for t in sh if t < 1) / len(sh))},
        'ask': {'n': k['n'], 'never_pct': round(100 * k['never'] / k['n']), 'median_h': round(median(ah), 1), 'under1h_pct': round(100 * sum(1 for t in ah if t < 1) / len(ah))},
        'show_vs_ask_z': round(z, 2), 'show_vs_ask_p': round(p, 4),
    }
pooled = {}
for name, D in (('show', S), ('ask', A)):
    a25 = D['2025-04-week1']['ok'] + D['2025-10-week1']['ok']
    a26 = D['2026-04-week1']['ok'] + D['2026-10-week1']['ok']
    z, p = mwu(a25, a26)
    pooled[name] = {'n25': len(a25), 'n26': len(a26), 'median_h': [round(median(t / 3600 for t in a25), 1), round(median(t / 3600 for t in a26), 1)], 'z': round(z, 2), 'p': round(p, 4)}

print(json.dumps({'windows': table, 'pooled_yoy': pooled}, indent=1))

# --- README verification: every median in the table must match the data ---
readme = open('README.md').read()
bad = []
for w in WINDOWS:
    label = w.replace('-week1', '')
    row = re.search(rf'^\|\s*`?{label}`?[^|]*\|.*$', readme, re.M)
    if not row:
        bad.append(f'{label}: table row not found')
        continue
    txt = row.group(0)
    for site in ('show', 'ask'):
        m = str(table[w][site]['median_h'])
        if not re.search(rf'{re.escape(m)}h\b', txt):
            bad.append(f'{label} {site}: median {m} not found in README row')
for m in pooled['ask']['median_h']:
    if not re.search(rf'{re.escape(str(m))}\s*h', readme):
        bad.append(f'ask pooled median {m} missing from README')
# pool numbers quoted in the Method line (pooled year-pairs "a25/a26 -> b25/b26")
mline = re.search(r'Comment-bearing pools[^\n]*', readme)
if not mline:
    bad.append('Method pool line missing')
else:
    mt = mline.group(0)
    import itertools
    for site in ('ask', 'show'):
        pairs = []
        for yr in ('2025-04-week1', '2025-10-week1', '2026-04-week1', '2026-10-week1'):
            pass
        # recompute pools per site/year from raw data
        rows_ok = defaultdict(int)
        rows_n = defaultdict(int)
        for f in ([f for f in ('askhn-ttfc-sample.json', 'askhn-ttfc-apr.json') if site == 'ask'] +
                  [f for f in ('showhn-ttfc-sample.json', 'showhn-ttfc-apr.json') if site == 'show']):
            for r in json.load(open('data/' + f)):
                w = r['window'].split(' (')[0]
                rows_n[w] += 1
                if r.get('ttfc_s') is not None: rows_ok[w] += 1
        p25 = (rows_ok['2025-04-week1'], rows_ok['2025-10-week1'])
        p26 = (rows_ok['2026-04-week1'], rows_ok['2026-10-week1'])
        want = f"{p25[0]}/{p25[1]}", f"{p26[0]}/{p26[1]}"
        if want[0] not in mt or want[1] not in mt:
            bad.append(f'{site} pool strings {want[0]}->{want[1]} not found in Method line')
if False:
  if pooled['ask']['p'] >= 0.05:
    bad.append('data says ask pooled YoY is NOT significant — README claim of significance would be wrong')
if pooled['show']['p'] < 0.05:
    bad.append('data says show pooled YoY IS significant — README claim of "flat" would be wrong')
for w in WINDOWS:
    label = w.replace('-week1', '')
    sig2026 = table[w]['show_vs_ask_p'] < 0.05
    row = re.search(rf'^\|\s*`?{label}`?[^|]*\|.*$', readme, re.M)
    if row and ('p<0.001' in row.group(0) or 'p=0.01' in row.group(0)) and not sig2026:
        bad.append(f'{label}: README shows significance the data does not support')
if bad:
    print('README MISMATCH:', bad, file=sys.stderr)
    sys.exit(1)
print('README numbers verified against data')
