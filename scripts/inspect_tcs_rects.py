import fitz, requests, json, collections, os, re
data=json.load(open("data/coaches-site/coaches-site-drills.json"))
groups=collections.defaultdict(list)
for d in data:
    if d.get("diagram_verified") and d.get("source_url") and d.get("source_page"):
        groups[d["source_url"]].append(d)
for url,drills in groups.items():
    r=requests.get(url,timeout=120); r.raise_for_status()
    doc=fitz.open(stream=r.content,filetype="pdf")
    print("PDF",url,"pages",doc.page_count)
    bypage=collections.defaultdict(list)
    for d in drills: bypage[int(d["source_page"])].append(d)
    for page_num, items in sorted(bypage.items()):
        p=doc[page_num-1]
        infos=[]
        for info in p.get_image_info(xrefs=True):
            x0,y0,x1,y1=info["bbox"]
            w=x1-x0; h=y1-y0
            if w*h > p.rect.width*p.rect.height*0.02 and w>60 and h>50:
                infos.append({"bbox":[round(x0,2),round(y0,2),round(x1,2),round(y1,2)],"w":info.get("width"),"h":info.get("height"),"area":round(w*h,1)})
        infos=sorted(infos,key=lambda z:(z["bbox"][1],z["bbox"][0]))
        print("PAGE",page_num,"size",[round(p.rect.width,2),round(p.rect.height,2)],"items",[x["uid"]+":"+x["title"] for x in items],"images",json.dumps(infos))
