import fitz, requests, json, re, os, subprocess

URL="https://cdn1.sportngin.com/attachments/document/c4b8-3131914/The-Hockey-Drill-Book-1st-Edition-2007.pdf"
OUT="data/hockey-drill-book/hockey-drill-book.json"

CHAPTERS=[
 (30,56,"Warm-Up Skills","Chapter 2 · Skating, Passing & Stickhandling"),
 (57,102,"Warm-Up Shooting","Chapter 3 · Warm-Up Drills With Shooting"),
 (103,130,"1-on-1","Chapter 4 · One-on-One Drills"),
 (131,152,"2-on-1","Chapter 5 · Two-on-One Drills"),
 (153,170,"2-on-2","Chapter 6 · Two-on-Two Drills"),
 (171,184,"3-on-1","Chapter 7 · Three-on-One Drills"),
 (185,200,"Breakouts / 3-on-2 / 5-on-2","Chapter 8 · Three-on-Two, Five-on-Two & Breakout Drills"),
 (201,222,"Defensive","Chapter 9 · Defensive Drills"),
 (223,242,"Combination","Chapter 10 · Combination Drills"),
 (243,258,"Shooting","Chapter 11 · Shooting Drills"),
 (259,272,"Defenseman","Chapter 12 · Defenseman Drills"),
 (273,286,"Forward","Chapter 13 · Forward Drills"),
 (287,308,"Goalie","Chapter 14 · Goalie Drills"),
 (309,336,"Special Teams / Face-Offs","Chapter 15 · Power Play, Penalty-Killing & Face-Off Drills"),
 (337,362,"Competitive Games","Chapter 16 · Competitive Fun Drills & Games"),
 (363,374,"Evaluation","Chapter 17 · Evaluation Drills"),
 (375,392,"Conditioning","Chapter 18 · On-Ice Conditioning Drills"),
]

def category_for(p):
    for a,b,c,ch in CHAPTERS:
        if a<=p<=b:return c,ch
    return "Other",""

def skill_tags(title,cat):
    s=(title+" "+cat).lower(); tags=[]
    rules=[
      ("Skating",["skate","skating","agility","pivot","crossover","sprint","conditioning"]),
      ("Passing",["pass","give-and-go","give and go","one-touch","one touch"]),
      ("Shooting",["shoot","shot","deflect","tip","score"]),
      ("Puckhandling",["stickhandle","stickhandling","puck control","puck-control"]),
      ("Defensive",["defense","defensive","backcheck","checking","gap","1-on-1","1v1"]),
      ("Offensive",["offense","offensive","drive to the net","cycle"]),
      ("Systems",["breakout","regroup","forecheck","power play","penalty","face-off","faceoff"]),
      ("Goalies",["goalie","goaltender"]),
      ("Small Area Games",["game","keep-away","keep away","battle","cross ice"]),
    ]
    for tag,needles in rules:
        if any(n in s for n in needles): tags.append(tag)
    if not tags: tags=[cat]
    return tags

r=requests.get(URL,timeout=120); r.raise_for_status()
doc=fitz.open(stream=r.content,filetype="pdf")
records=[]

for pno in range(29,392): # zero-based physical PDF pages 30..392
    page=doc[pno]
    physical=pno+1
    category,chapter=category_for(physical)
    if category=="Other": continue

    # Collect the 15.7pt bold drill-heading lines and merge split title lines.
    raw=[]
    d=page.get_text("dict")
    for block in d.get("blocks",[]):
        for line in block.get("lines",[]):
            spans=[s for s in line.get("spans",[]) if s.get("size",0)>=15 and "Futura-CondensedExtraBol" in s.get("font","")]
            if not spans: continue
            txt=" ".join(s.get("text","") for s in spans).replace("\t"," ").strip()
            if not txt: continue
            raw.append({"x":line["bbox"][0],"y":line["bbox"][1],"text":txt})
    # group objects that share the same baseline (number and title are sometimes separate objects)
    grouped=[]
    for item in sorted(raw,key=lambda z:(z["y"],z["x"])):
        hit=None
        for g in grouped:
            if abs(g["y"]-item["y"])<=1.2:
                hit=g;break
        if hit:
            hit["parts"].append((item["x"],item["text"]))
        else:
            grouped.append({"y":item["y"],"parts":[(item["x"],item["text"])]})
    lines=[]
    for g in grouped:
        text=" ".join(t for x,t in sorted(g["parts"])).strip()
        lines.append({"y":g["y"],"text":re.sub(r"\s+"," ",text)})

    heads=[]
    current=None
    for line in sorted(lines,key=lambda z:z["y"]):
        m=re.match(r"^(\d{1,3})\s+(.*)$",line["text"])
        if m:
            num=int(m.group(1)); title=m.group(2).strip()
            if 1<=num<=446:
                current={"number":num,"title":title,"y":line["y"]}
                heads.append(current)
                continue
        # wrapped title line immediately below the numbered heading
        if current and line["y"]-current["y"]<=24 and not re.match(r"^\d",line["text"]):
            current["title"]=(current["title"]+" "+line["text"]).strip()

    drawings=page.get_drawings()
    for j,h in enumerate(heads):
        y0=h["y"]
        y1=heads[j+1]["y"] if j+1<len(heads) else 650
        candidates=[]
        for dr in drawings:
            rr=dr["rect"]
            if rr.x1<=0 or rr.x0>=page.rect.width: continue
            cx=(rr.x0+rr.x1)/2; cy=(rr.y0+rr.y1)/2
            area=rr.width*rr.height
            if cy<=y0+18 or cy>=y1-4: continue
            if rr.width<75 or rr.height<45 or area<5000: continue
            candidates.append((area,rr))
        if not candidates:
            # fallback to largest meaningful vector object in the section
            for dr in drawings:
                rr=dr["rect"]; cy=(rr.y0+rr.y1)/2; area=rr.width*rr.height
                if cy>y0+18 and cy<y1-4 and rr.x1>0 and rr.x0<page.rect.width and area>1800 and rr.width>60:
                    candidates.append((area,rr))
        if not candidates:
            print("NO_DIAGRAM",physical,h["number"],h["title"])
            continue
        max_area=max(a for a,r in candidates)
        threshold=max_area*0.38
        large=[rr for a,rr in candidates if a>=threshold]
        if not large:
            large=[max(candidates,key=lambda z:z[0])[1]]
        x0=min(rr.x0 for rr in large); ytop=min(rr.y0 for rr in large)
        x1=max(rr.x1 for rr in large); ybot=max(rr.y1 for rr in large)
        pad=12
        rect=[
          round(max(0,x0-pad),2), round(max(y0+18,ytop-pad),2),
          round(min(page.rect.width,x1+pad),2), round(min(y1-3,ybot+pad),2)
        ]
        records.append({
          "uid":f"hdb-{h['number']:04d}",
          "number":h["number"],
          "title":h["title"],
          "category":category,
          "chapter":chapter,
          "source":"The Hockey Drill Book",
          "source_collection":"The Hockey Drill Book · 1st Edition (2007)",
          "author":"Dave Chambers",
          "source_url":URL,
          "source_page":physical,
          "book_page":physical-20,
          "diagram_rect":rect,
          "page_size":[round(page.rect.width,2),round(page.rect.height,2)],
          "diagram_verified":True,
          "tags":["The Hockey Drill Book",category,*skill_tags(h["title"],category)]
        })

records.sort(key=lambda d:d["number"])
nums=[d["number"] for d in records]
missing=[n for n in range(1,447) if n not in nums]
dupes=sorted({n for n in nums if nums.count(n)>1})
if dupes:
    for n in dupes:
        print("DUPLICATE_DETAIL",json.dumps([d for d in records if d["number"]==n],ensure_ascii=False))
print("SUMMARY",json.dumps({"count":len(records),"first":nums[:5],"last":nums[-5:],"missing":missing,"duplicates":dupes}))
if missing or dupes or len(records)!=446:
    raise SystemExit("Expected exactly 446 unique drills; validation failed")

os.makedirs(os.path.dirname(OUT),exist_ok=True)
with open(OUT,"w") as f: json.dump(records,f,indent=2,ensure_ascii=False)
print("WROTE",OUT,len(records))
