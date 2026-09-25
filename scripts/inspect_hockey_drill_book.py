import fitz, requests, json
url="https://cdn2.sportngin.com/attachments/document/c4b8-3131914/The-Hockey-Drill-Book-1st-Edition-2007.pdf"
r=requests.get(url,timeout=120);r.raise_for_status();doc=fitz.open(stream=r.content,filetype="pdf")
for pno in [8,9,10,11,12,13]:
    p=doc[pno]
    print("===PAGE",pno+1,"===")
    words=p.get_text("words")
    # group by rounded baseline/block-line
    rows={}
    for w in words:
        x0,y0,x1,y1,txt,block,line,word=w
        key=(block,line)
        rows.setdefault(key,[]).append((x0,txt))
    for key,vals in rows.items():
        vals=sorted(vals)
        line=" ".join(t for x,t in vals)
        if any(ch.isdigit() for ch in line):
            print("ROW",key,[(round(x,1),t) for x,t in vals])
