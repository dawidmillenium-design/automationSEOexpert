import re, os, glob, json, html.parser

files = sorted(glob.glob("*.html"))
data = {}
for f in files:
    s = open(f, encoding="utf-8").read()
    data[f] = s

# inbound links
inbound = {f: 0 for f in files}
outlinks = {}
for f, s in data.items():
    hrefs = re.findall(r'href="([^"#?]+\.html)"', s)
    hrefs = [h.split("/")[-1] for h in hrefs]
    ext = set(hrefs)
    outlinks[f] = ext
    for t in ext:
        if t in inbound and t != f:
            inbound[t] += 1

def wordcount(s):
    body = re.sub(r'<script.*?</script>|<style.*?</style>', '', s, flags=re.S)
    text = re.sub(r'<[^>]+>', ' ', body)
    text = html.unescape(text)
    return len([w for w in text.split() if re.search(r'\w', w)])

def title(s):
    m = re.search(r'<title>(.*?)</title>', s, re.S)
    return m.group(1).strip() if m else ""

def meta_desc(s):
    m = re.search(r'<meta name="description" content="(.*?)"', s)
    return html.unescape(m.group(1)) if m else ""

rows = []
titles = [title(data[f]) for f in files]
descs = [meta_desc(data[f]) for f in files]
from collections import Counter
tc, dc = Counter(titles), Counter(descs)

for i, f in enumerate(files):
    s = data[f]
    wc = wordcount(s)
    # on-page components
    op = 0; det = {}
    t = titles[i]; d = descs[i]
    ok_title = bool(t) and 30 <= len(t) <= 70 and tc[t] == 1
    ok_desc  = bool(d) and 70 <= len(d) <= 165 and dc[d] == 1
    ok_canon = 'rel="canonical"' in s
    ok_og    = 'property="og:title"' in s and 'property="og:description"' in s
    ok_tw    = 'name="twitter:card"' in s
    ok_lang  = 'lang="en"' in s
    ok_view  = 'viewport' in s
    h1s = len(re.findall(r'<h1[\s>]', s))
    ok_h1 = h1s == 1
    h2s = len(re.findall(r'<h2[\s>]', s))
    ok_struct = h2s >= 2
    ok_wc = wc >= 600
    ok_schema = '"@type"' in s
    ok_author = ('author-profile.html' in s or 'editorial-policy.html' in s) and 'By ' in s
    comps = [ok_title, ok_desc, ok_canon, ok_og, ok_tw, ok_lang, ok_view, ok_h1, ok_struct, ok_wc, ok_schema, ok_author]
    weights = [10, 10, 10, 8, 6, 4, 4, 8, 8, 12, 10, 12]
    op = sum(w for c, w in zip(comps, weights) if c)
    # internal link score (0-100)
    ib = inbound[f]; ob = len(outlinks[f])
    ib_pts = min(ib, 10) * 5          # up to 50
    ob_pts = min(ob, 10) * 5          # up to 50
    il = ib_pts + ob_pts
    rows.append((f, wc, ib, op, il, "pillar/standalone" if wc >= 600 else "alias/hub"))

rows.sort(key=lambda r: (-r[3], -r[4]))
with open("/tmp/scores.json", "w") as fh:
    json.dump(rows, fh)
print(f"pages={len(rows)} avg_onpage={sum(r[3] for r in rows)/len(rows):.1f} avg_int={sum(r[4] for r in rows)/len(rows):.1f}")
print("min/max onpage:", min(r[3] for r in rows), max(r[3] for r in rows))
print("min/max intlink:", min(r[4] for r in rows), max(r[4] for r in rows))
