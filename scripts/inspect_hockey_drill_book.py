import fitz, requests, json
url="https://cdn2.sportngin.com/attachments/document/c4b8-3131914/The-Hockey-Drill-Book-1st-Edition-2007.pdf"
r=requests.get(url,timeout=120);r.raise_for_status();doc=fitz.open(stream=r.content,filetype="pdf")
for pno in [29,30,31,243,244,259,308,336,374,391]:
    p=doc[pno]
    draws=[]
    for d in p.get_drawings():
      r=d["rect"]; area=r.width*r.height
      if area>20:
        draws.append([round(r.x0,1),round(r.y0,1),round(r.x1,1),round(r.y1,1),round(area,1),d.get("type")])
    print("PAGE",pno+1,"DRAWINGS",len(draws),json.dumps(draws[:80]))
