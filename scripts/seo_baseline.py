#!/usr/bin/env python3
"""Idempotent SEO baseline fixer for automationSEOexpert static site.
Applies: canonical, robots meta, OG/Twitter cards, Article JSON-LD,
single-H1 enforcement, nav home link, related-articles + footer links,
full article listing in index.html, sitemap.xml, robots.txt.
Set SITE_BASE env var to override the production domain, then rerun.
"""
import os, re, html as htmllib, json, hashlib, datetime

BASE = os.environ.get("SITE_BASE", "https://dawidmillenium-design.github.io/automationSEOexpert").rstrip("/")
SITE = "Video Virality Score Articles"
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

files = sorted(f for f in os.listdir(D) if f.endswith(".html"))

def get_title(h, f):
    m = re.search(r"<title>(.*?)</title>", h, re.S)
    return m.group(1).strip() if m else f[:-5].replace("-", " ").title()

def get_desc(h):
    m = re.search(r'name="description" content="([^"]*)"', h)
    return m.group(1).strip() if m else ""

titles = {f: get_title(open(D + "/" + f, encoding="utf-8").read(), f) for f in files}

def fix_page(f):
    h = open(D + "/" + f, encoding="utf-8").read()
    h = h.replace("\\n", "\n")  # repair literal \n escapes
    title, desc, url = titles[f], get_desc(h), BASE + "/" + f
    # single H1: demote subsequent h1 pairs to h2
    h1s = list(re.finditer(r"<h1([^>]*)>(.*?)</h1>", h, re.S))
    for m in reversed(h1s[1:]):
        h = h[:m.start()] + "<h2%s>%s</h2>" % (m.group(1), m.group(2)) + h[m.end():]
    if 'rel="canonical"' not in h:
        inject = (
            '\n    <link rel="canonical" href="%s">'
            '\n    <meta name="robots" content="index, follow">'
            '\n    <meta property="og:type" content="article">'
            '\n    <meta property="og:title" content="%s">'
            '\n    <meta property="og:description" content="%s">'
            '\n    <meta property="og:url" content="%s">'
            '\n    <meta property="og:site_name" content="%s">'
            '\n    <meta name="twitter:card" content="summary">'
            '\n    <meta name="twitter:title" content="%s">'
            '\n    <meta name="twitter:description" content="%s">'
            '\n    <script type="application/ld+json">%s</script>'
        ) % (url, htmllib.escape(title, quote=True), htmllib.escape(desc, quote=True),
             url, SITE, htmllib.escape(title, quote=True), htmllib.escape(desc, quote=True),
             json.dumps({"@context": "https://schema.org", "@type": "Article",
                         "headline": title, "description": desc, "mainEntityOfPage": url,
                         "publisher": {"@type": "Organization", "name": SITE}}, ensure_ascii=False))
        h = h.replace("</head>", inject + "\n</head>", 1)
    if 'href="index.html"' not in h:
        h = re.sub(r"(<nav[^>]*>)", r'\1\n        <a href="index.html" class="text-white mr-4 underline">Home</a>', h, count=1)
    if "Related articles" not in h:
        others = [x for x in files if x != f and x != "index.html"]
        seed = int(hashlib.md5(f.encode()).hexdigest(), 16)
        rel = list(dict.fromkeys(others[(seed + i * 37) % len(others)] for i in range(5)))
        rel_html = ('\n    <section class="p-8 border-t mt-8"><h2 class="text-xl font-semibold mb-2">Related articles</h2>'
                    '<ul class="list-disc ml-6">'
                    + "".join('<li><a class="text-blue-600 underline" href="%s">%s</a></li>' % (r, htmllib.escape(titles[r])) for r in rel)
                    + "</ul></section>")
        footer = ('\n    <footer class="p-4 text-center text-sm text-gray-500 border-t">'
                  '<a class="text-blue-600 underline" href="index.html">Back to all articles</a></footer>')
        h = h.replace("</body>", rel_html + footer + "\n</body>", 1)
    return h

for f in files:
    content = fix_page(f)
    open(D + "/" + f, "w", encoding="utf-8").write(content)

# index.html lists every article
idx = open(D + "/index.html", encoding="utf-8").read()
listed = set(re.findall(r'href="([^"]+\.html)"', idx))
missing = [f for f in files if f != "index.html" and f not in listed]
if missing:
    idx = re.sub(r"(</ul>)", "".join('<li><a href="%s">%s</a></li>' % (f, htmllib.escape(titles[f])) for f in missing) + r"\1", idx, count=1)
    open(D + "/index.html", "w", encoding="utf-8").write(idx)

today = datetime.date.today().isoformat()
sitemap = ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           + "".join("  <url><loc>%s/%s</loc><lastmod>%s</lastmod></url>\n" % (BASE, f, today) for f in files)
           + "</urlset>\n")
open(D + "/sitemap.xml", "w", encoding="utf-8").write(sitemap)
open(D + "/robots.txt", "w", encoding="utf-8").write("User-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n" % BASE)

# verification: fail loudly if any check fails
issues = []
for f in files:
    h = open(D + "/" + f, encoding="utf-8").read()
    if 'rel="canonical"' not in h: issues.append((f, "canonical"))
    if 'property="og:title"' not in h: issues.append((f, "og"))
    if "application/ld+json" not in h: issues.append((f, "ld-json"))
    if len(re.findall(r"<h1[ >]", h)) != 1: issues.append((f, "h1"))
    if "Related articles" not in h and f != "index.html": issues.append((f, "related"))
    if 'href="index.html"' not in h: issues.append((f, "home-link"))
inbound = {f: 0 for f in files}
for f in files:
    for l in set(re.findall(r'href="([^"]+\.html)"', open(D + "/" + f, encoding="utf-8").read())):
        if l in inbound and l != f: inbound[l] += 1
issues += [(f, "orphan") for f, c in inbound.items() if c == 0]
if issues:
    raise SystemExit("SEO check FAILED: %r" % issues[:20])
print("SEO baseline OK: %d pages, 0 issues" % len(files))
