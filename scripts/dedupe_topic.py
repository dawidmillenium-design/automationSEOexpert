#!/usr/bin/env python3
"""Reduce exact-phrase repetition on alias pages by rotating in natural variants."""
import re, json

pages = json.load(open('scripts/seo_clusters.json'))['pages']

def variants(topic):
    out = [topic]
    short = topic
    for cut in [" for video virality"," and video virality"," for virality"," and virality",
                " in video virality"," for viral videos"," in viral videos"," for viral content",
                " in viral content"," around your video"," for your video"," of video virality"]:
        if short.endswith(cut):
            short = short[:-len(cut)].strip(); break
    if short != topic and len(short.split()) >= 2:
        out.append(short)
    return out

changed = 0
for f, (role, pillar) in pages.items():
    if role != 'alias':
        continue
    topic = f[:-5].replace('-', ' ')
    vs = variants(topic)
    html = open(f).read()
    bi = html.index('<article>')
    head, body = html[:bi], html[bi:]
    state = {'occ': 0}
    def repl(m):
        s = m.group(0); state['occ'] += 1
        if state['occ'] <= 2 or len(vs) == 1:
            return s
        v = vs[state['occ'] % len(vs)]
        # preserve capitalization pattern of the match
        if s[0].isupper():
            v = v[0].upper() + v[1:]
        return v
    body = re.compile(re.escape(topic), re.I).sub(repl, body)
    body = re.sub(r'  +', ' ', body)
    new = head + body
    if new != html:
        open(f, 'w').write(new); changed += 1
print("rewritten:", changed)
