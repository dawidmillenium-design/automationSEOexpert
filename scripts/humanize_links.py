"""Idempotent installer: adds 2 humanized contextual-link paragraphs (data-human-note)
to every content page. Targets chosen topically: link #1 = same-cluster sibling,
link #2 = same semantic bucket from a different cluster. Anchor text uses cleaned titles."""
import json, glob, re, random, hashlib

c = json.load(open('scripts/seo_clusters.json'))
pages = c['pages']
members = {}
for f,(role,pil) in pages.items(): members.setdefault(pil, []).append(f)

def title_of(fn):
    t = re.search(r'<title>(.*?)</title>', open(fn).read(), re.S|re.I).group(1).strip()
    t = re.split(r'\s*[—|]\s*', t)[0]
    return re.sub(r'(: 2026 Topic Guide| — Topic Guide| — Complete Guide)$','',t,flags=re.I).strip().title()

BUCKETS = {'metrics':['metric','analyz','measure','track','score-across','data'],'emotion':['emotion','psycholog'],
 'story':['stori','narrative','intro','copywrit','title'],'thumb':['thumbnail'],'length':['length'],
 'social':['social','hashtag','tiktok','platform','algorithm','promot','cross-platform'],
 'community':['communit','comment','engagement','engaging','friends-and-family','feedback'],
 'ugc':['user-generated','testimonial','co-creating','challenge'],'collab':['collab','influencer'],
 'trend':['trend','future','evolution','history','2026','calendar','holiday','time-of','timing','live-stream','ar-and-vr','niche','genre','format','idea','educational','music'],
 'brand':['brand','marketing','budget','advertis','regulat','compliance','social-change','benefits']}
def bucket(fn):
    low=fn.lower(); best,score='basics',0
    for b,kws in BUCKETS.items():
        s=sum(len(k) for k in kws if k in low)
        if s>score: best,score=b,s
    return best

OPENERS=["Honestly, the part people underestimate here is how much context does the heavy lifting — ","Here's something we keep seeing in our own tests: ","In plain terms? This works only when you pair it with ","From experience, the fastest wins come from combining this with ","One thing worth saying out loud: nobody nails this alone — start reading ","If you take one practical tip from this page, make it this: cross-check your work against ","We learned this the hard way after reviewing dozens of accounts; the companion piece ","Real talk — the numbers only make sense once you line them up next to ","A quick side note before you move on: ","What usually surprises creators is how well this clicks once you add "]
CLOSERS=[" — it answers the follow-up questions most readers skip."," and keep both open in separate tabs while you plan.","; we've referenced it in three other guides for good reason."," before you publish anything."," — roughly ten minutes, and it changes how you read the rest of this page."," and treat them as one workflow, not two articles.","; the examples there make this section far less abstract.",". Start there if anything above felt thin."]

allfiles=[f for f in sorted(glob.glob('*.html')) if f in pages]
pool={}
for f in allfiles: pool.setdefault(bucket(f),[]).append(f)

changed=0
for f in allfiles:
    s=open(f).read()
    if 'data-human-note' in s: continue
    rng=random.Random(int(hashlib.md5(f.encode()).hexdigest(),16))
    pil=pages[f][1]; sib=[x for x in members.get(pil,[]) if x!=f]
    alt=[x for x in pool.get(bucket(f),[]) if pages[x][1]!=pil and x!=f]
    a=rng.choice(sib) if sib else (pil if pil!=f else rng.choice(alt or allfiles))
    second=[x for x in alt if x!=a] or [x for x in pool['basics'] if x not in (a,f)]
    b=rng.choice(second)
    o1,c1=rng.choice(OPENERS),rng.choice(CLOSERS)
    o2=OPENERS[(OPENERS.index(o1)+3)%len(OPENERS)]; c2=CLOSERS[(CLOSERS.index(c1)+4)%len(CLOSERS)]
    mk=lambda t,h,o,cl:f"<p class=\"text-gray-700 mb-4\" data-human-note>{o}<a href=\"{h}\" class=\"text-blue-600 underline\">{t}</a>{cl}</p>"
    block="\n"+mk(title_of(a),a,o1,c1)+"\n"+mk(title_of(b),b,o2,c2)+"\n"
    tag='</article>' if '</article>' in s else ('</main>' if '</main>' in s else None)
    if not tag: continue
    open(f,'w').write(s.replace(tag,block+tag,1)); changed+=1
print("installed on",changed,"pages")
