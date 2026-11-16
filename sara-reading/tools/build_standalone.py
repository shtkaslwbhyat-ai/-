# Builds one self-contained HTML file (opens in any browser, no login needed)
import sys,os
here=os.path.dirname(os.path.abspath(__file__)); root=os.path.dirname(here)
r=lambda f: open(os.path.join(root,f),encoding="utf8").read()
page=r("index.html")
page=page.replace('<script src="lessons.js"></script>','<script>'+r("lessons.js")+'</script>')
page=page.replace('<script src="audio.js"></script>','<script>'+r("audio.js")+'</script>')
doc='<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{margin:0}[hidden]{display:none!important}img{max-width:100%}</style></head><body>'+page+'</body></html>'
out=os.path.join(root,"sara-game.html"); open(out,"w",encoding="utf8").write(doc); print(out,os.path.getsize(out))
