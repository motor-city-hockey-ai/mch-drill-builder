import requests
urls=[
"https://cdn1.sportngin.com/attachments/document/c4b8-3131914/The-Hockey-Drill-Book-1st-Edition-2007.pdf",
"https://cdn2.sportngin.com/attachments/document/c4b8-3131914/The-Hockey-Drill-Book-1st-Edition-2007.pdf"]
for u in urls:
 r=requests.get(u,headers={"Origin":"https://motor-city-hockey-ai.github.io"},stream=True,timeout=60)
 print("URL",u,"STATUS",r.status_code)
 for k,v in r.headers.items():
  if k.lower() in ["access-control-allow-origin","access-control-allow-credentials","content-type","content-length","accept-ranges"]:
   print(k,":",v)
