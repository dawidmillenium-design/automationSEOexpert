#!/usr/bin/env python3
"""Install animated HERO (H1 on top, div-based moving objects: video/youtube/tiktok/laptop/smartphone) into all HTML pages."""
import re, glob, html

SCENE = '''<div class="hero-scene" aria-hidden="true">
<div class="hero-blob b1"></div><div class="hero-blob b2"></div><div class="hero-blob b3"></div>
<span class="hero-obj hero-play"></span>
<div class="hero-obj hero-yt"><div class="hero-yt-badge"></div></div>
<div class="hero-obj hero-tk"><div class="hero-tk-note"><span>♪</span></div></div>
<div class="hero-obj hero-laptop"><div class="hero-lap-screen"><div class="hero-lap-notch"></div><div class="hero-scrim"></div><div class="hero-strip"></div></div><div class="hero-lap-base"></div></div>
<div class="hero-obj hero-phone"><div class="hero-phone-body"><div class="hero-phone-notch"></div><div class="hero-phone-screen"></div></div></div>
</div>
<div class="hero-shine" aria-hidden="true"></div>'''

def kicker_for(fname):
    if fname == "index.html": return "Video Virality Score — Research Hub"
    h = html.unescape(re.sub(r"[-_]+", " ", fname.replace(".html",""))).strip().title()
    for w in ("How To","Tiktok","Youtube","Faq"): pass
    h = re.sub(r"\bTo\b|\bOf\b|\bAnd\b|\bThe\b|\bIn\b|\bFor\b|\bA\b(?=\s)", lambda m: m.group(0).lower(), h)
    h = h.replace("Tiktok","TikTok").replace("Youtub","YouTu")
    return "Guide · " + h[:70]

n_changed = 0
for f in sorted(glob.glob("*.html")):
    src = open(f, encoding="utf-8").read()
    if 'class="hero"' in src:   # idempotent
        continue
    m = re.search(r'<h1([^>]*)>(.*?)</h1>', src, re.S)
    if not m:
        print("SKIP (no h1):", f); continue
    h1_open_attrs = m.group(1)
    h1_text = m.group(2).strip()
    # remove old h1 from article body
    src = src[:m.start()] + src[m.end():]
    # strip any leftover byline p that immediately followed? keep it; just remove classes referencing mb-2 spacing issue - fine.
    hero = ('<section class="hero">\n'
            f'<div class="hero-inner"><p class="hero-kicker">{kicker_for(f)}</p>\n'
            f'<h1{h1_open_attrs}>{h1_text}</h1>\n'
            '<p>Watch what moves on this screen: a laptop streaming video, a smartphone mid-scroll, YouTube and TikTok signals — the exact surfaces where virality is won.</p>\n'
            '</div>\n' + SCENE + '\n</section>\n')
    # insert right after <main ...> opening tag
    mm = re.search(r'(<main[^>]*>)', src)
    if mm:
        src = src[:mm.end()] + "\n" + hero + src[mm.end():]
    else:
        mb = re.search(r'(<article[^>]*>)', src)
        src = src[:mb.end()] + "\n" + hero + src[mb.end():]
    # add stylesheet link after retro css link (or before </head>)
    if 'assets/hero.css' not in src:
        src = src.replace('<link rel="stylesheet" href="assets/retro-wave-nav.css"/>',
                          '<link rel="stylesheet" href="assets/retro-wave-nav.css"/>\n<link rel="stylesheet" href="assets/hero.css"/>', 1)
        if 'assets/hero.css' not in src:
            src = src.replace('</head>', '<link rel="stylesheet" href="assets/hero.css"/>\n</head>', 1)
    open(f, "w", encoding="utf-8").write(src)
    n_changed += 1
print("pages updated:", n_changed)
