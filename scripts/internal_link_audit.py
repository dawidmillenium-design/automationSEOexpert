import re, os, glob, collections, statistics

files = sorted(glob.glob('*.html'))
anchor_re = re.compile(r'<a\s+[^>]*href="([^"]+)"[^>]*>(.*?)</a>', re.I|re.S)

links_out = {}   # file -> list of (target, text)
for f in files:
    html = open(f, encoding='utf-8').read()
    outs = []
    for href, text in anchor_re.findall(html):
        if href.startswith(('http://','https://','mailto:','#')): continue
        t = href.split('#')[0].split('?')[0]
        if not t.endswith('.html') and '/' not in t and '.' not in t:
            t += '.html'
        if t == f: continue
        clean = re.sub(r'<[^>]+>','',text).strip()[:40]
        outs.append((t, clean))
    links_out[f] = outs

inbound = collections.Counter()
for f, outs in links_out.items():
    for t,_ in outs:
        inbound[t]+=1

broken = []
for f, outs in links_out.items():
    for t,_ in outs:
        if t not in os.listdir('.') or not t.endswith('.html'):
            broken.append((f,t))

# Page type detection
clusters = set()
cj = json_path = 'scripts/seo_clusters.json'
import json
alias_map = {}
if os.path.exists(cj):
    data = json.load(open(cj))
    if isinstance(data, dict):
        for pillar, pages in data.items():
            if isinstance(pages, list):
                alias_map[pillar]=pillar
                for p in pages: alias_map[p]=pillar

def ptype(f):
    if f=='index.html': return 'Hub index'
    if f in ('about.html','author-profile.html','editorial-policy.html'): return 'Trust page'
    if f in alias_map and alias_map[f]!=f: return 'Alias/hub'
    return 'Pillar/article'

rows=[]
for f in files:
    html=open(f,encoding='utf-8').read()
    words=len(re.sub(r'<[^>]+>',' ',html.split('<body')[-1]).split())
    inb=inbound.get(f,0)
    out_set={t for t,_ in links_out[f]}
    distinct_out=len(out_set)
    # contextual links = outbound links inside <article>/<main> body (exclude nav/footer/header)
    body=re.sub(r'<(header|nav|footer)\b.*?</\1>','',html,flags=re.S|re.I)
    ctx=len([1 for href,text in anchor_re.findall(body) if not href.startswith(('http','mailto:','#'))])
    score_in=min(inb*5,50); score_out=min(distinct_out*5,50)
    total=score_in+score_out
    rows.append(dict(file=f,type=ptype(f),words=words,inbound=inb,outbound=distinct_out,ctx=ctx,score=total))

# Write markdown + csv
with open('internal_link_audit.md','w') as fh:
    fh.write('# Internal Link Audit — automationSEOexpert\n\n')
    fh.write(f'Scanned: {len(files)} HTML pages on `main` @ commit 225dc50 (includes Retro Wave global nav + wave footer).\n\n')
    fh.write('**Scoring:** inbound points = min(inbound×5, 50); outbound points = min(distinct internal targets×5, 50); max 100.\n\n')
    ins=[r['inbound'] for r in rows]; outs=[r['outbound'] for r in rows]; sc=[r['score'] for r in rows]
    orphans=[r['file'] for r in rows if r['inbound']==0]
    fh.write(f'- Site average internal-link score: **{statistics.mean(sc):.0f}/100** (median {statistics.median(sc)})\n')
    fh.write(f'- Inbound links per page: mean {statistics.mean(ins):.1f}, median {statistics.median(ins)}, min {min(ins)}, max {max(ins)}\n')
    fh.write(f'- Distinct outbound internal targets per page: mean {statistics.mean(outs):.1f}, median {statistics.median(outs)}\n')
    fh.write(f'- Orphan pages (0 inbound): **{len(orphans)}** {orphans if orphans else ""}\n')
    fh.write(f'- Broken internal links: **{len(broken)}** {broken[:5] if broken else ""}\n\n')
    tiers=collections.Counter()
    for r in rows: tiers[(r['score']>=80,'A' if r['score']>=80 else 'B' if r['score']>=60 else 'C' if r['score']>=40 else 'D')]+=1
    fh.write('| Tier | Range | Pages |\n|---|---|---|\n')
    fh.write(f'| A | 80–100 | {sum(1 for r in rows if r["score"]>=80)} |\n')
    fh.write(f'| B | 60–79 | {sum(1 for r in rows if 60<=r["score"]<80)} |\n')
    fh.write(f'| C | 40–59 | {sum(1 for r in rows if 40<=r["score"]<60)} |\n')
    fh.write(f'| D | 0–39 | {sum(1 for r in rows if r["score"]<40)} |\n\n')
    fh.write('## All pages\n\n| # | File | Type | Words | Inbound | Outbound | Contextual | Score |\n|---|---|---|---|---|---|---|---|\n')
    for i,r in enumerate(sorted(rows,key=lambda x:-x['score']),1):
        fh.write(f'| {i} | {r["file"]} | {r["type"]} | {r["words"]} | {r["inbound"]} | {r["outbound"]} | {r["ctx"]} | {r["score"]} |\n')

import csv
with open('internal_link_audit.csv','w',newline='') as fh:
    w=csv.DictWriter(fh,fieldnames=['rank','file','type','words','inbound','outbound','contextual_links','score'])
    w.writeheader()
    for i,r in enumerate(sorted(rows,key=lambda x:-x['score']),1):
        rr=dict(r); rr['rank']=i; del rr['type']; rr['type']=r['type']
        w.writerow({'rank':i,'file':r['file'],'type':r['type'],'words':r['words'],'inbound':r['inbound'],'outbound':r['outbound'],'contextual_links':r['ctx'],'score':r['score']})

print(f"pages={len(rows)} avg_score={statistics.mean(sc):.1f} median={statistics.median(sc)}")
print(f"inbound mean={statistics.mean(ins):.1f} median={statistics.median(ins)} min={min(ins)} max={max(ins)}")
print(f"outbound mean={statistics.mean(outs):.1f} median={statistics.median(outs)}")
print(f"orphans={len(orphans)} broken={len(broken)}")
print("tiers: A",sum(1 for r in rows if r['score']>=80),"B",sum(1 for r in rows if 60<=r['score']<80),"C",sum(1 for r in rows if 40<=r['score']<60),"D",sum(1 for r in rows if r['score']<40))
low=sorted(rows,key=lambda x:x['score'])[:12]
for r in low: print("LOW:",r['file'],r['type'],r['score'],"in",r['inbound'],"out",r['outbound'])
hi=sorted(rows,key=lambda x:-x['score'])[:8]
for r in hi: print("HIGH:",r['file'],r['type'],r['score'],"in",r['inbound'],"out",r['outbound'])
by_type=collections.defaultdict(list)
for r in rows: by_type[r['type']].append(r['score'])
for t,v in by_type.items(): print("TYPE:",t,len(v),round(statistics.mean(v),1))
