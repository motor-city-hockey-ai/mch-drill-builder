import fitz, requests, re, json
url="https://cdn2.sportngin.com/attachments/document/c4b8-3131914/The-Hockey-Drill-Book-1st-Edition-2007.pdf"
r=requests.get(url,timeout=120)
print("DOWNLOAD",r.status_code,len(r.content),r.headers.get("content-type"),r.headers.get("access-control-allow-origin"))
r.raise_for_status()
doc=fitz.open(stream=r.content,filetype="pdf")
print("PAGES",doc.page_count)
print("TOC",json.dumps(doc.get_toc()[:200]))
for i,p in enumerate(doc):
    text=" ".join(p.get_text("text").split())
    imgs=[]
    for info in p.get_image_info(xrefs=True):
        x0,y0,x1,y1=map(float,info["bbox"])
        if (x1-x0)*(y1-y0)>20000:
            imgs.append([round(x0,1),round(y0,1),round(x1,1),round(y1,1),info.get("width"),info.get("height")])
    if i<40 or "drill" in text.lower() or imgs:
        print("PAGE",i+1,"SIZE",[round(p.rect.width,1),round(p.rect.height,1)],"IMGS",json.dumps(imgs[:8]),"TEXT",text[:700])
