import re, glob, sys

TOP = '''<header class="rw-topbar" id="rwTop">
<a class="rw-logo" href="index.html">Video <em>Virality</em> Score</a>
<nav aria-label="Main navigation"><ul>
<li><a href="index.html">Home</a></li>
<li><a href="what-is-video-virality-score.html">Score Basics</a></li>
<li><a href="how-to-improve-video-virality-score.html">Growth Tactics</a></li>
<li><a href="understanding-video-virality-analytics.html">Analytics</a></li>
<li><a href="viral-video-trends-in-2026.html">Trends 2026</a></li>
<li><a href="about.html">About</a></li>
</ul></nav>
</header>
<div class="rw-strip" aria-hidden="true"><span class="rw-track">&#9733; New: 2026 Virality Benchmarks &#9733; Mobile Optimization Playbook updated &#9733; Free virality score guide &#9733;&nbsp;&nbsp;&#9733; New: 2026 Virality Benchmarks &#9733; Mobile Optimization Playbook updated &#9733; Free virality score guide &#9733;&nbsp;&nbsp;</span></div>
'''

FOOT = '''<footer class="rw-wavefoot">
<svg class="rw-waves" viewBox="0 0 1440 40" preserveAspectRatio="none" aria-hidden="true">
<path d="M0 20 Q60 0 120 20 T240 20 T360 20 T480 20 T600 20 T720 20 T840 20 T960 20 T1080 20 T1200 20 T1320 20 T1440 20 V40 H0 Z" fill="#1e1b4b"/>
<path d="M0 26 Q60 8 120 26 T240 26 T360 26 T480 26 T600 26 T720 26 T840 26 T960 26 T1080 26 T1200 26 T1320 26 T1440 26 V40 H0 Z" fill="#1e1b4b"/>
</svg>
<div class="rw-btnrow">
<a href="what-is-video-virality-score.html">What is the Score?</a>
<a href="how-to-improve-video-virality-score.html">Improve Your Score</a>
<a href="calculating-virality-score.html">Calculate</a>
<a href="viral-video-trends-in-2026.html">2026 Trends</a>
<a href="author-profile.html">Our Authors</a>
<a href="editorial-policy.html">Editorial Policy</a>
</div>
<p style="text-align:center;font-size:11px;margin:10px 0 0;opacity:.7">&copy; 2026 Video Virality Score &middot; <a href="index.html" style="color:#facc15">All articles</a> &middot; <a href="about.html" style="color:#facc15">About</a> &middot; <a href="editorial-policy.html" style="color:#facc15">Editorial Policy</a></p>
</footer>
<script src="assets/retro-wave-nav.js"></script>
'''

CSSLINK = '<link rel="stylesheet" href="assets/retro-wave-nav.css"/>\n'

changed = 0
for path in sorted(glob.glob('*.html')) + sorted(glob.glob('*/*.html')):
    if path.startswith('design-proposals/'):
        continue
    s = open(path, encoding='utf-8').read()
    orig = s
    if 'id="rwTop"' in s:
        continue
    # remove old top nav (simple 2-link nav) OR add body padding for pages with mega-nav (index)
    m = re.search(r'<nav class="bg-blue-600[^"]*"[^>]*>.*?</nav>\s*', s, re.S)
    has_mega_nav = False
    if m:
        inner = m.group(0)
        if inner.count('<a ') <= 3:
            s = s.replace(inner, TOP, 1)
        else:
            has_mega_nav = True  # index.html full archive nav: keep it below header
    else:
        has_mega_nav = True
    if not m or has_mega_nav:
        # insert header at start of body
        bm = re.search(r'<body[^>]*>', s)
        if not bm:
            print('NO BODY', path); continue
        tag = bm.group(0)
        newtag = tag[:-1] + ' class="rw-body">' if 'class=' not in tag else tag.replace('class="', 'class="rw-body ', 1)
        s = s.replace(tag, newtag + '\n' + TOP + ('\n<div class="rw-mega">\n' if False else ''), 1)
    # replace footer
    fm = re.search(r'<footer class="bg-gray-800[^"]*"[^>]*>.*?</footer>\s*', s, re.S)
    if fm:
        s = s.replace(fm.group(0), FOOT, 1)
    else:
        s = s.replace('</body>', FOOT + '</body>', 1)
    # add css link after tailwind stylesheet link
    if 'assets/retro-wave-nav.css' not in s:
        tm = re.search(r'<link[^>]*tailwind[^>]*/?>', s)
        if tm:
            s = s.replace(tm.group(0), tm.group(0) + '\n' + CSSLINK.rstrip('\n'), 1)
        else:
            s = s.replace('</head>', CSSLINK + '</head>', 1)
    if s != orig:
        open(path, 'w', encoding='utf-8').write(s)
        changed += 1
print('pages updated:', changed)
