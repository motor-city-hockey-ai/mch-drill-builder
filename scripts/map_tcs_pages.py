import fitz, requests, json, re, unicodedata, os

PDFS={
 "2020 Virtual Hockey Summit Drill E-Book":"https://members.thecoachessite.com/videos/video_230619070227_v1340/video_230619070227_v1340.pdf",
 "2021 Global Skills Showcase Drill E-Book":"https://members.thecoachessite.com/videos/video_230619071227_v28c4/video_230619071227_v28c4.pdf",
 "2023 TCS Live Top 100 Drill Book":"https://join.thecoachessite.com/hubfs/TCS%20Live/Drill%20Book/2023/2023%20-%20TCS%20Live%20Drill%20Book.pdf",
}

def norm(s):
    s=unicodedata.normalize("NFKD",s or "").encode("ascii","ignore").decode()
    s=s.lower().replace(" vs ","v").replace(" v ","v")
    s=re.sub(r"[^a-z0-9]+"," ",s)
    return re.sub(r"\s+"," ",s).strip()

data=json.load(open("data/coaches-site/coaches-site-drills.json"))
bycol={}
for d in data: bycol.setdefault(d.get("source_collection",""),[]).append(d)

for coll,url in PDFS.items():
    r=requests.get(url,timeout=120); r.raise_for_status()
    doc=fitz.open(stream=r.content,filetype="pdf")
    pages=[]
    for i,p in enumerate(doc):
        t=norm(p.get_text("text"))
        pages.append((i+1,t))
    print("COLLECTION",coll,"PAGES",len(pages))
    for d in bycol.get(coll,[]):
        title=norm(d.get("title",""))
        toks=[x for x in title.split() if len(x)>=2]
        exact=[n for n,t in pages if title and title in t]
        best=None; bestscore=-1
        for n,t in pages:
            if not toks: score=0
            else: score=sum(1 for x in toks if x in t)/len(toks)
            # Prefer pages containing source number text too, but only as a tie-breaker.
            if score>bestscore:
                bestscore=score; best=n
        page=exact[0] if exact else best
        verified=bool(exact) or bestscore>=0.80
        print("MAP",json.dumps({
            "uid":d.get("uid"),"title":d.get("title"),"collection":coll,
            "page":page,"score":round(bestscore,3),"exact":bool(exact),"verified":verified,
            "url":url
        },ensure_ascii=False))
