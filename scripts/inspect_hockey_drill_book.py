import fitz, requests, collections
url="https://cdn2.sportngin.com/attachments/document/c4b8-3131914/The-Hockey-Drill-Book-1st-Edition-2007.pdf"
r=requests.get(url,timeout=120);r.raise_for_status();doc=fitz.open(stream=r.content,filetype="pdf")
p=doc[8]
words=p.get_text("words")
# group left-column words by rounded vertical center
groups=collections.defaultdict(list)
for w in words:
    x0,y0,x1,y1,t,*_=w
    if x0<252:
        groups[round((y0+y1)/2,1)].append((x0,t))
for y,vals in sorted(groups.items()):
    vals=sorted(vals)
    if vals and vals[0][1].isdigit() and int(vals[0][1])<=10:
        print("Y",y,[(round(x,1),t) for x,t in vals])
