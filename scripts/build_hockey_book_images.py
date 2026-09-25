import fitz, requests, json, os, pathlib
PDF="https://cdn2.sportngin.com/attachments/document/c4b8-3131914/The-Hockey-Drill-Book-1st-Edition-2007.pdf"
META="data/hockey-drill-book/hockey-drill-book.json"
OUT="data/hockey-drill-book/images"
r=requests.get(PDF,timeout=180)
r.raise_for_status()
doc=fitz.open(stream=r.content,filetype="pdf")
rows=json.load(open(META))
os.makedirs(OUT,exist_ok=True)
for i,d in enumerate(rows,1):
    p=doc[int(d["source_page"])-1]
    rect=fitz.Rect(*map(float,d["diagram_rect"]))
    pix=p.get_pixmap(matrix=fitz.Matrix(1.45,1.45),clip=rect,alpha=False)
    path=f'{OUT}/{d["uid"]}.png'
    pix.save(path)
    d["diagram_image"]=path
    if i%50==0: print("RENDERED",i)
json.dump(rows,open(META,"w"),indent=2,ensure_ascii=False)
print("DONE",len(rows))

# trigger image build
