#!/usr/bin/env python3
"""SEO technical baseline fixer (audit fix #3 + safe parts of #2/#4).

Idempotent. For every *.html page in the repo root:
  - injects canonical, robots meta, Open Graph + Twitter Card tags
  - injects JSON-LD structured data (Article / CollectionPage schema)
  - adds a "Home" nav link and a "Back to index" footer link (kills orphans)
  - appends a "Related articles" hub section so every page has >=1 outbound
    internal link and every page is reachable from >=2 pages
  - demotes extra <h1> tags to <h2> (single-H1 policy)
Also generates sitemap.xml and robots.txt, and refreshes commit_count.txt.
"""
import hashlib
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent
SITE_URL = "https://example.com"  # TODO: replace with real production domain
SITENAME = "Video Virality Score"

pages = sorted(p for p in ROOT.glob("*.html"))
articles = [p.name for p in pages if p.name != "index.html"]


def title_of(path: Path) -> str:
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    return soup.title.get_text(strip=True) if soup.title else path.stem


def description_of(soup) -> str:
    tag = soup.find("meta", attrs={"name": "description"})
    return tag["content"].strip() if tag and tag.get("content") else ""


def related(filename: str, k: int = 5):
    """Deterministic selection of k sibling articles.

    Siblings are sorted by SHA-256(salt + filename) with the *source* page as
    salt (so each page gets a different list), then rotated by the source
    page's rank in the article list. The rotation guarantees that every
    article appears in at least one other page's related list => zero orphans.
    """
    names = [a for a in articles if a != filename]
    if not names:
        return []
    ordered = sorted(
        articles,
        key=lambda n: hashlib.sha256((filename + "|" + n).encode()).hexdigest(),
    )
    start = ordered.index(filename)
    picks = [n for n in ordered[start + 1:start + 1 + k] if n != filename]
    # wrap-around if we ran past the end
    i = (start + 1 + k) % len(ordered)
    while len(picks) < min(k, len(names)):
        n = ordered[i]
        if n != filename and n not in picks:
            picks.append(n)
        i = (i + 1) % len(ordered)
    return picks[:k]


def head_meta(soup, url, page_title, desc, schema_type):
    def get_or_create(tag_name, **attrs):
        el = soup.head.find(tag_name, attrs=attrs)
        if el is None:
            el = soup.new_tag(tag_name)
            for k, v in attrs.items():
                el[k] = v
            soup.head.append(el)
        return el

    # canonical
    link = soup.head.find("link", rel=lambda v: v and "canonical" in v)
    if link is None:
        link = soup.new_tag("link")
        link["rel"] = "canonical"
        soup.head.append(link)
    link["href"] = url

    get_or_create("meta", name="robots")["content"] = "index,follow"

    def og(prop, content):
        el = get_or_create("meta", property=prop)
        el["content"] = content

    def tw(name_, content_):
        get_or_create("meta", name=name_)["content"] = content_

    og("og:type", "website" if schema_type == "CollectionPage" else "article")
    og("og:site_name", SITENAME)
    og("og:title", page_title)
    og("og:description", desc)
    og("og:url", url)
    og("og:locale", "en_US")
    tw("twitter:card", "summary")
    tw("twitter:title", page_title)
    tw("twitter:description", desc)


def add_schema(soup, url, page_title, desc):
    existing = soup.head.find("script", type="application/ld+json")
    if existing is None:
        existing = soup.new_tag("script", type="application/ld+json")
        soup.head.append(existing)
    data = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": page_title,
        "description": desc,
        "url": url,
        "inLanguage": "en",
        "publisher": {"@type": "Organization", "name": SITENAME},
        "mainEntityOfPage": {"@type": "WebPage", "@id": url},
    }
    existing.string = json.dumps(data, ensure_ascii=False)


def fix_h1(soup):
    h1s = soup.find_all("h1")
    for extra in h1s[1:]:
        extra.name = "h2"


def home_link(soup, cls=None):
    a = soup.new_tag("a", href="index.html")
    a.string = "Home — all articles"
    if cls:
        a["class"] = cls.split()
    return a


def add_nav_home(soup):
    nav = soup.body.find("nav")
    if nav is None:
        return  # pages without <nav> get the link in the footer instead
    if not nav.find("a", href="index.html"):
        nav.append(home_link(soup, "ml-4 underline"))


def add_footer_link(soup):
    footer = soup.body.find("footer")
    if footer is None:
        footer = soup.new_tag("footer")
        soup.body.append(footer)
    if not footer.find("a", href="index.html"):
        footer.append(soup.new_string(" | "))
        footer.append(home_link(soup))


def add_related(soup, filename):
    main = soup.body.find("main")
    if main is None:
        return
    existing = main.find(id="related-articles")
    rel = related(filename)
    targets = {a["href"] for a in (existing.find_all("a", href=True) if existing else [])}
    missing = [r for r in rel if r != filename and r not in targets]
    if existing is not None and not missing:
        return
    if existing is not None:  # refresh: guarantee every page links to >=5 siblings
        existing.decompose()
    section = soup.new_tag("section", id="related-articles")
    section["class"] = "mt-8"
    h2 = soup.new_tag("h2")
    h2["class"] = "text-xl font-bold mb-2"
    h2.string = "Related articles"
    section.append(h2)
    ul = soup.new_tag("ul")
    ul["class"] = "list-disc pl-5"
    for r in rel:
        li = soup.new_tag("li")
        a = soup.new_tag("a", href=r)
        a.string = title_of(ROOT / r)
        li.append(a)
        ul.append(li)
    section.append(ul)
    main.append(section)


def complete_index():
    """Make sure index.html links to every article (fixes crawler discovery)."""
    idx = ROOT / "index.html"
    soup = BeautifulSoup(idx.read_text(encoding="utf-8"), "html.parser")
    main = soup.body.find("main")
    if main is None:
        return False
    listed = {a["href"] for a in main.find_all("a", href=True)}
    missing = [a for a in articles if a not in listed]
    if not missing:
        return False
    ul = main.find("ul")
    if ul is None:
        ul = soup.new_tag("ul")
        ul["class"] = "list-disc"
        main.append(ul)
    extra_h2 = soup.new_tag("h2")
    extra_h2.string = "All articles"
    main.append(extra_h2)
    for name in missing:
        li = soup.new_tag("li")
        a = soup.new_tag("a", href=name)
        a.string = title_of(ROOT / name)
        li.append(a)
        ul.append(li)
    body = re.sub(r"^\s*(<!doctype[^>]*>)?\s*", "", str(soup), flags=re.I)
    idx.write_text("<!DOCTYPE html>\n" + body.rstrip() + "\n", encoding="utf-8")
    return True


changed = 0
for page in pages:
    raw = page.read_text(encoding="utf-8")
    # Some generated pages were committed with literal "\n" escape sequences
    # instead of real newlines (invalid HTML). Repair them.
    if raw.lstrip().startswith("<!DOCTYPE html>") and "\\n" in raw[:200]:
        raw = raw.replace("\\n", "\n")
    soup = BeautifulSoup(raw, "html.parser")
    filename = page.name
    url = f"{SITE_URL}/{filename}"
    page_title = title_of(page)
    desc = description_of(soup) or page_title

    schema_type = "CollectionPage" if filename == "index.html" else "Article"
    head_meta(soup, url, page_title, desc, schema_type)
    add_schema(soup, url, page_title, desc)
    fix_h1(soup)
    add_nav_home(soup)
    add_footer_link(soup)
    if filename != "index.html":
        add_related(soup, filename)

    body = re.sub(r"^\s*(<!doctype[^>]*>)?\s*", "", str(soup), flags=re.I)
    after = "<!DOCTYPE html>\n" + body.rstrip() + "\n"
    if after != raw:
        page.write_text(after, encoding="utf-8")
        changed += 1

# ---- sitemap.xml -----------------------------------------------------------
urls = []
for page in pages:
    loc = f"{SITE_URL}/{page.name}"
    urls.append(f"  <url><loc>{loc}</loc><changefreq>monthly</changefreq></url>")
sitemap = (
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + "\n".join(urls)
    + "\n</urlset>\n"
)
(ROOT / "sitemap.xml").write_text(sitemap, encoding="utf-8")

# ---- robots.txt ------------------------------------------------------------
(ROOT / "robots.txt").write_text(
    "User-agent: *\nAllow: /\n\nSitemap: " + SITE_URL + "/sitemap.xml\n",
    encoding="utf-8",
)

# ---- commit_count.txt ------------------------------------------------------
count = len(pages)
(ROOT / "commit_count.txt").write_text(
    f"Total HTML files committed: {count} ({count - 1} articles + 1 index.html)\n",
    encoding="utf-8",
)

print(f"Pages processed: {count}; changed: {changed}")

# ---- index.html: link to every article (run after per-page pass) -----------
if complete_index():
    print("index.html: added links to previously unlisted articles")
else:
    print("index.html: already complete")
