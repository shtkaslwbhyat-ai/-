import json,base64,os,sys
S=sys.argv[1]; out=sys.argv[2]
m=json.load(open(f"{S}/tools/manifest.json",encoding="utf8"))
d={}
for k,t in m.items():
    p=f"{S}/clips/{k}.mp3"
    if os.path.exists(p): d[t]="data:audio/mpeg;base64,"+base64.b64encode(open(p,"rb").read()).decode()
open(out,"w",encoding="utf8").write("window.SARA_AUDIO="+json.dumps(d,ensure_ascii=False)+";\n")
print(len(d),"clips",os.path.getsize(out),"bytes")
