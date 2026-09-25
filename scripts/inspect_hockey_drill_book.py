import fitz, requests, json
url="https://cdn2.sportngin.com/attachments/document/c4b8-3131914/The-Hockey-Drill-Book-1st-Edition-2007.pdf"
r=requests.get(url,timeout=120);r.raise_for_status();doc=fitz.open(stream=r.content,filetype="pdf")
for pno in [29,30,31,243,244,392]:
    p=doc[pno]
    print("===PAGE",pno+1,"===")
    d=p.get_text("dict")
    for b in d["blocks"]:
      for line in b.get("lines",[]):
        spans=line.get("spans",[])
        txt=" ".join(s["text"] for s in spans).strip()
        if txt:
          print("LINE",round(line["bbox"][0],1),round(line["bbox"][1],1),[(s["text"],round(s["size"],1),s["font"],s["flags"]) for s in spans])
