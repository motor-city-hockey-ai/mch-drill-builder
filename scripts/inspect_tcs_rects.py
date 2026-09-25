import fitz, requests, json, collections, re, unicodedata
data=json.load(open("data/coaches-site/coaches-site-drills.json"))
pdf_cache={}

def norm(s):
    s=unicodedata.normalize("NFKD",s or "").encode("ascii","ignore").decode().lower()
    s=s.replace(" vs "," v ").replace("v0","v0")
    s=re.sub(r"[^a-z0-9]+"," ",s)
    return re.sub(r"\\s+"," ",s).strip()

def getdoc(url):
    if url not in pdf_cache:
        r=requests.get(url,timeout=120); r.raise_for_status()
        pdf_cache[url]=fitz.open(stream=r.content,filetype="pdf")
    return pdf_cache[url]

# Re-map source-numbered 2020/2021 drills using the printed drill number as the strongest signal.
for d in data:
    if d.get("source_number") is None: continue
    doc=getdoc(d["source_url"])
    title=norm(d.get("title","")); toks=[t for t in title.split() if len(t)>=2]
    num=str(d["source_number"])
    best=None; bestscore=-1
    for i,p in enumerate(doc):
        txt=norm(p.get_text("text"))
        numhit=bool(re.search(r"(?<!\\d)"+re.escape(num)+r"(?!\\d)",txt))
        tok_score=sum(1 for t in toks if t in txt)/max(1,len(toks))
        score=tok_score + (1.5 if numhit else 0)
        if score>bestscore:
            bestscore=score; best=i+1
    d["source_page"]=best

# Manual verified source-page correction for 2023 Passing SAG.
for d in data:
    if d.get("uid")=="coaches-0127":
        d["source_page"]=38
        d["source_url"]="https://join.thecoachessite.com/hubfs/TCS%20Live/Drill%20Book/2023/2023%20-%20TCS%20Live%20Drill%20Book.pdf"

# Group by PDF/page, identify source diagram images, and assign them in page reading order.
groups=collections.defaultdict(list)
for d in data:
    if d.get("diagram_verified") and d.get("source_url") and d.get("source_page"):
        groups[(d["source_url"],int(d["source_page"]))].append(d)

mapping={}
problems=[]
for (url,pageno),items in groups.items():
    doc=getdoc(url); page=doc[pageno-1]
    candidates=[]
    for info in page.get_image_info(xrefs=True):
        x0,y0,x1,y1=map(float,info["bbox"])
        area=(x1-x0)*(y1-y0)
        if area < 20000 or (x1-x0)<120 or (y1-y0)<90: continue
        # The two landscape e-books use coach portraits in the upper band; drills sit lower.
        if page.rect.width>1000 and page.rect.height<500 and y0<100: continue
        candidates.append([x0,y0,x1,y1])
    if page.rect.width>1000 and page.rect.height<500:
        candidates.sort(key=lambda b:b[0])
        items.sort(key=lambda d:(d.get("source_number") if d.get("source_number") is not None else d["number"]))
    else:
        candidates.sort(key=lambda b:(b[1],b[0]))
        items.sort(key=lambda d:d["number"])
    if len(candidates)<len(items):
        problems.append({"page":pageno,"url":url,"items":[x["uid"] for x in items],"candidates":candidates})
        continue
    # If a page has extra images, use the largest sensible set in reading order.
    # For portrait pages with stacked practice-plan diagrams, all candidates are drill diagrams.
    chosen=candidates[:len(items)]
    for d,b in zip(items,chosen):
        pad=3
        rect=[max(0,round(b[0]-pad,2)),max(0,round(b[1]-pad,2)),min(round(page.rect.width,2),round(b[2]+pad,2)),min(round(page.rect.height,2),round(b[3]+pad,2))]
        mapping[d["uid"]]={
            "source_page":pageno,
            "diagram_rect":rect,
            "page_size":[round(page.rect.width,2),round(page.rect.height,2)]
        }

print("RESULT",json.dumps({"mapping":mapping,"problems":problems},separators=(",",":")))
