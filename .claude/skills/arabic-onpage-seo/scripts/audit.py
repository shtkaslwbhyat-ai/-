#!/usr/bin/env python3
"""فحص سيو داخلي لصفحة HTML عربية. الاستعمال: python3 -I audit.py page.html [page2.html ...]
مكتبة بايثون القياسية فقط. يطبع المشاكل مرتّبة بالخطورة ويخرج بـ1 إن وُجدت مشكلة حرجة."""
import sys, json, re
from html.parser import HTMLParser

class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.html_attrs = {}; self.title = ""; self._in = None
        self.metas = {}; self.links = []; self.anchors = []; self.imgs = []
        self.heads = []; self.jsonld = []; self._buf = ""; self._a = None
    def handle_starttag(self, t, a):
        a = dict(a)
        if t == "html": self.html_attrs = a
        elif t == "title": self._in = "title"
        elif t == "meta":
            k = a.get("name") or a.get("property")
            if k: self.metas[k.lower()] = (a.get("content") or "").strip()
        elif t == "link": self.links.append(a)
        elif t == "a": self._a = {"href": a.get("href"), "text": "", "aria": a.get("aria-label")}
        elif t == "img": self.imgs.append(a)
        elif re.fullmatch(r"h[1-6]", t): self._in = t; self._buf = ""
        elif t == "script" and a.get("type") == "application/ld+json": self._in = "ld"; self._buf = ""
    def handle_endtag(self, t):
        if t == "a" and self._a: self.anchors.append(self._a); self._a = None
        if self._in == t and re.fullmatch(r"h[1-6]", t): self.heads.append((int(t[1]), self._buf.strip()))
        if t == "script" and self._in == "ld": self.jsonld.append(self._buf)
        if t in ("title", "script") or re.fullmatch(r"h[1-6]", t): self._in = None
    def handle_data(self, d):
        if self._in == "title": self.title += d
        elif self._in: self._buf += d
        if self._a is not None: self._a["text"] += d

def audit(path):
    p = P(); p.feed(open(path, encoding="utf-8").read())
    out = []  # (level, message)
    add = lambda lvl, m: out.append((lvl, m))
    h = p.html_attrs
    if h.get("lang", "")[:2] != "ar": add("حرج", f'lang="{h.get("lang","")}" — يجب أن يبدأ بـ ar')
    if h.get("dir") != "rtl": add("مهم", 'dir="rtl" مفقود على <html>')
    t = p.title.strip()
    if not t: add("حرج", "لا يوجد <title>")
    elif not 15 <= len(t) <= 65: add("مهم", f"طول العنوان {len(t)} حرفًا (المستهدف 15–65)")
    d = p.metas.get("description", "")
    if not d: add("حرج", "لا يوجد meta description")
    elif not 70 <= len(d) <= 160: add("مهم", f"طول الوصف {len(d)} حرفًا (المستهدف 70–160)")
    if re.search(r"(أفضل|الأول|رقم 1|الأكبر)", d + t): add("تنبيه", "ادّعاء تفضيل (أفضل/الأول) في العنوان أو الوصف — جوجل كثيرًا ما يعيد كتابته، والقارئ لا يصدّقه")
    if "keywords" in p.metas: add("تنبيه", "meta keywords يتجاهلها جوجل؛ وجودها ليس خطأ لكنها ليست إنجازًا")
    canon = [l for l in p.links if "canonical" in (l.get("rel") or "")]
    if not canon: add("مهم", "لا يوجد canonical")
    for k in ("og:title", "og:description", "og:image", "og:url"):
        if k not in p.metas: add("تنبيه", f"{k} مفقود (المشاركة في واتساب/إكس ستظهر بلا صورة أو رابط صحيح)" if k in ("og:image","og:url") else f"{k} مفقود")
    h1 = [x for x in p.heads if x[0] == 1]
    if len(h1) != 1: add("حرج" if not h1 else "مهم", f"عدد H1 = {len(h1)} (المطلوب 1)")
    prev = 0
    for lvl, txt in p.heads:
        if prev and lvl > prev + 1: add("مهم", f"قفزة عناوين H{prev}→H{lvl}: «{txt[:40]}»"); 
        prev = lvl
    dead = [a for a in p.anchors if (a["href"] or "").strip() in ("", "#", "javascript:void(0)")]
    if dead: add("حرج", f"{len(dead)} رابط href فارغ أو «#» — جوجل لا يزحف إليها، فكل صفحات التصنيفات والمقالات يتيمة")
    empty = [a for a in p.anchors if not a["text"].strip() and not a["aria"]]
    if empty: add("مهم", f"{len(empty)} رابط بلا نصّ مرئي ولا aria-label")
    noalt = [i for i in p.imgs if not (i.get("alt") or "").strip()]
    if noalt: add("مهم", f"{len(noalt)} صورة بلا alt")
    nolazy = [i for i in p.imgs[2:] if i.get("loading") != "lazy"]
    if nolazy: add("تنبيه", f"{len(nolazy)} صورة أسفل الصفحة بلا loading=\"lazy\"")
    if not p.jsonld: add("مهم", "لا توجد بيانات منظّمة JSON-LD (Organization/WebSite على الأقل للرئيسية، Article للمقالات)")
    for blob in p.jsonld:
        try: json.loads(blob)
        except Exception as e: add("حرج", f"JSON-LD غير صالح: {e}")
    return out

ORDER = {"حرج": 0, "مهم": 1, "تنبيه": 2}
crit = False
for f in sys.argv[1:] or sys.exit(__doc__):
    res = sorted(audit(f), key=lambda x: ORDER[x[0]])
    print(f"\n== {f} — {len(res)} ملاحظة")
    for lvl, m in res:
        print(f"[{lvl}] {m}"); crit |= lvl == "حرج"
sys.exit(1 if crit else 0)
