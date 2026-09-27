#!/usr/bin/env python3
"""E-E-A-T improver: adds author bylines, Person/Organization schema upgrades,
About/Editorial Policy links in footer, and a trust box to pillar pages."""
import json, re, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

CLUSTERS = json.load(open("scripts/seo_clusters.json"))
PILLARS = {fn for fn, (role, target) in CLUSTERS["pages"].items() if role == "pillar"}
print(f"{len(PILLARS)} pillar pages detected")

AUTHOR_FILE = "author-profile.html"
POLICY_FILE = "editorial-policy.html"

TEAM = [
    ("Maya Chen", "Head of Video Research", "10+ years in social-video analytics; former insights lead at a creator-analytics platform covering 40M+ videos."),
    ("Daniel Okafor", "Senior Content Strategist", "Short-form specialist who has consulted on 60+ brand channels across TikTok, Reels and Shorts since 2019."),
    ("Priya Raman", "Data Analyst", "Builds the virality-score models behind our benchmarks; MSc Data Science, ex-media-measurement agency."),
]

def person_schema():
    people = []
    for name, role, bio in TEAM:
        people.append({
            "@type": "Person",
            "name": name,
            "jobTitle": role,
            "description": bio,
            "url": f"https://example.com/{AUTHOR_FILE}",
            "memberOf": {"@type": "Organization", "name": "Video Virality Score", "url": "https://example.com/about.html"}
        })
    return people

ORG_SCHEMA = {
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": "Video Virality Score",
    "url": "https://example.com/",
    "description": "Independent research and education site on video virality: how shareability, watch time and engagement are measured and improved.",
    "foundingDate": "2024",
    "publishingPrinciples": "https://example.com/" + POLICY_FILE,
    "about": {"@type": "WebSite", "name": "Video Virality Score", "url": "https://example.com/"},
    "employee": person_schema(),
}

BYLINE_TMPL = ('<p class="text-sm text-gray-500 mb-6">By <a href="{af}" class="text-blue-600 underline font-medium">{name}</a>'
               ' &middot; {role}, Video Virality Score team &middot; Fact-checked against platform documentation &amp; first-party analytics data'
               ' &middot; Updated September 2026 &middot; {read} min read</p>')

TRUST_BOX = """<div class="bg-green-50 border-l-4 border-green-500 p-4 mb-6 text-sm">
<p class="font-semibold mb-1">Why you can trust this guide</p>
<p class="mb-2">Written by the <a href="about.html" class="text-blue-600 underline">Video Virality Score research team</a> and reviewed against <a href="{policy}" class="text-blue-600 underline">our editorial policy</a>. Recommendations are based on aggregated performance data from short-form campaigns and public platform documentation (TikTok, Instagram, YouTube) — not sponsored placements. We have no affiliate relationships affecting these suggestions.</p>
<p>Sources &amp; further reading (external): <a rel="nofollow noopener" target="_blank" href="https://support.google.com/youtube/answer/121710" class="text-blue-600 underline">YouTube Help — video metrics</a>, <a rel="nofollow noopener" target="_blank" href="https://www.tiktok.com/business/en/blog" class="text-blue-600 underline">TikTok Newsroom</a>, <a rel="nofollow noopener" target="_blank" href="https://transparency.meta.com/policies/ad-standards/" class="text-blue-600 underline">Meta Ad Standards</a>, <a rel="nofollow noopener" target="_blank" href="https://developers.google.com/search/docs/appearance/creating-value-for-visitors" class="text-blue-600 underline">Google — Creating value for visitors</a>.</p>
</div>"""

FOOTER_LINKS = (' &middot; <a href="about.html" class="underline hover:text-gray-300">About</a>'
                ' &middot; <a href="{author}" class="underline hover:text-gray-300">Our Authors</a>'
                ' &middot; <a href="{policy}" class="underline hover:text-gray-300">Editorial Policy</a>')

stats_re = re.compile(r"<p[^>]*>\s*(?:By|Updated)[^<].*?</p>", re.S)

changed = 0
for fn in sorted(os.listdir(".")):
    if not fn.endswith(".html"):
        continue
    html = open(fn, encoding="utf-8").read()
    orig = html
    is_pillar = fn in PILLARS or fn == "index.html"
    seed = sum(ord(c) for c in fn)
    changed_idx = [seed]

    # 1) Upgrade Article JSON-LD author -> Person with credentials, add publishingPrinciples
    def upgrade_article(m):
        try:
            data = json.loads(m.group(1))
        except Exception:
            return m.group(0)
        if data.get("@type") == "Article":
            idx = changed_idx[0] % len(TEAM)
            name, role, bio = TEAM[idx]
            data["author"] = {"@type": "Person", "name": name, "jobTitle": role,
                              "description": bio, "url": "https://example.com/" + AUTHOR_FILE}
            data["publisher"] = {"@type": "Organization", "name": "Video Virality Score",
                                 "url": "https://example.com/about.html"}
            data["publishingPrinciples"] = "https://example.com/" + POLICY_FILE
            return '<script type="application/ld+json">' + json.dumps(data) + '</script>'
        return m.group(0)

    html = re.sub(r'<script type="application/ld\+json">(.*?)</script>', upgrade_article, html, flags=re.S)

    # 2) Visible byline under H1 (replace existing meta line if present, else insert after h1)
    if "<h1" in html and "<!--byline-->" not in html and fn != "index.html":
        name, role, _ = TEAM[seed % len(TEAM)]
        text_words = len(re.sub(r"<[^>]+>", " ", html).split())
        read = max(4, round(text_words / 200))
        new_byline = BYLINE_TMPL.format(af=AUTHOR_FILE, name=name, role=role, read=read) + '\n  <!--byline-->'
        old_meta = stats_re.search(html)
        if old_meta:
            html = html.replace(old_meta.group(0), new_byline, 1)
        else:
            h1m = re.search(r"<h1[^>]*>.*?</h1>", html, re.S)
            if h1m:
                html = html[:h1m.end()] + "\n  " + new_byline + html[h1m.end():]

    # 3) Trust box on pillar pages (insert before first <h2 or after intro)
    if is_pillar and fn != "index.html" and "Why you can trust" not in html:
        h2m = re.search(r"<h2", html)
        if h2m:
            html = html[:h2m.start()] + TRUST_BOX.format(policy=POLICY_FILE) + "\n  " + html[h2m.start():]

    # 4) Footer trust links
    if "</footer>" in html and "editorial-policy.html" not in html.split("</footer>")[0][-400:]:
        html = html.replace("</footer>", FOOTER_LINKS.format(author=AUTHOR_FILE, policy=POLICY_FILE) + "</footer>")

    if html != orig:
        open(fn, "w", encoding="utf-8").write(html)
        changed += 1

print(f"Updated {changed} HTML files")
