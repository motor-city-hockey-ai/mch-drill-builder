import fitz, requests, os, json, statistics

PDFS={
 "tcs2020":"https://members.thecoachessite.com/videos/video_230619070227_v1340/video_230619070227_v1340.pdf",
 "tcs2021":"https://members.thecoachessite.com/videos/video_230619071227_v28c4/video_230619071227_v28c4.pdf",
 "katy":"https://members.thecoachessite.com/videos/v_251001123919_v6b01/v_251001123919_v6b01.pdf",
 "gameday":"https://members.thecoachessite.com/videos/v_250422110050_v4831/v_250422110050_v4831.pdf",
}
os.makedirs("probe",exist_ok=True)
for name,url in PDFS.items():
    r=requests.get(url,timeout=90)
    print("DOWNLOAD",name,r.status_code,len(r.content),r.headers.get("content-type"))
    path=f"probe/{name}.pdf"; open(path,"wb").write(r.content)
    doc=fitz.open(path)
    print("PDF",name,"pages",doc.page_count)
    for pno in range(min(doc.page_count,8)):
        p=doc[pno]
        imgs=p.get_images(full=True)
        sizes=[]
        for img in imgs:
            xref=img[0]
            try:
                pm=fitz.Pixmap(doc,xref)
                sizes.append((pm.width,pm.height,pm.n))
            except Exception as e:
                sizes.append(("err",str(e)))
        print("PAGE",name,pno,"rect",tuple(round(x,1) for x in p.rect),"images",len(imgs),"sizes",sizes[:12])
