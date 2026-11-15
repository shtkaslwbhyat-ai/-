"""Build story/shots.json for the memory video from a storyboard of anchor phrases -> templates."""
import json, re, sys
PROJ = sys.argv[1]
W = json.load(open(f"{PROJ}/timeline/words.json")); W = W.get("words", W)
import subprocess
VO = float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f"{PROJ}/input/voiceover.mp3"],capture_output=True,text=True).stdout); DUR = round(VO + 1.5, 3)

def norm(w):
    w = re.sub(r"[ً-ْٰـ]", "", w)
    w = re.sub(r"[آأإ]", "ا", w).replace("ة", "ه").replace("ى", "ي")
    return re.sub(r"[^\w']+", "", w.lower())
TOK = [norm(w["word"]) for w in W]
def find(phrase, frm=0):
    p = [norm(x) for x in phrase.split()]; p = [x for x in p if x]
    for i in range(frm, len(TOK) - len(p) + 1):
        if TOK[i:i + len(p)] == p: return i
    raise SystemExit(f"anchor not found after {frm}: {phrase}")

# ---- helpers ----
def C(c, x, pose="stand", expr="neutral", f=1, **kw): d = dict(c=c, x=x, pose=pose, expr=expr, f=f); d.update(kw); return d
def L(s, x=0.5, y=0.2, **kw): d = dict(s=s, x=x, y=y); d.update(kw); return d
def st(set_, chars, **kw): d = dict(tpl="stage", set=set_, chars=chars); d.update(kw); return d
def fc(who, set_, expr="neutral", **kw): d = dict(tpl="face", who=who, set=set_, expr=expr); d.update(kw); return d
def ins(kind, **kw): d = dict(tpl="insert", kind=kind); d.update(kw); return d
def da(**kw): d = dict(tpl="data"); d.update(kw); return d
def ar(**kw): d = dict(tpl="archive"); d.update(kw); return d
def bl(s, set_="home", **kw): d = dict(tpl="bigline", str=s, set=set_); d.update(kw); return d
CH = lambda **kw: dict(chair=True, pose="sit", **kw)
PUSH = dict(z0=1.0, z1=1.08, x0=0, x1=-40); PULL = dict(z0=1.12, z1=1.0, x0=-30, x1=20); DRIFT = dict(z0=1.04, z1=1.06, x0=40, x1=-60)
FLASH = {"type": "flash", "dur": 0.4}; DIP = {"type": "dip", "dur": 0.6}; FADE = {"type": "fade", "dur": 0.6}; WHIP = {"type": "whip", "dur": 0.35}; ZOOM = {"type": "zoom", "dur": 0.5}
POP = lambda at=0.3, g=-12: {"at": at, "name": "pop", "gain": g}
SFX = lambda name, at=0.0, g=-10: {"at": at, "name": name, "gain": g}

B = []
def b(anchor, params, **meta): B.append((anchor, params, meta))
REP = lambda: L("تمثيل", x=0.93, y=0.08, size=34, cream=True, at=0.1)
def sc(set_, chars, labels=None, **kw): return st(set_, chars, labels=[REP()] + (labels or []), **kw)

b("ماذا لو كان بصرك احد", dict(tpl="title", lines=["ماذا لو", "كان بصرك أحدّ بمئة مرة؟"]), bars="scope", cap=False, sfx=[SFX("riser", 0, -12)])
b("تقرا لوحه سياره", ins("plate_number"), sfx=[SFX("whoosh", 0.1, -12)])
b("تري نمله تمشي", st("city", [], so=dict(mood="day"), cam=dict(z0=1.0, z1=1.5, x0=0, x1=-200), labels=[L("1 كم", y=0.2, ap="نمله", box=True)]))
b("وتعد ريش صقر", ins("eagle"))
b("يبدو هذا حلما", fc("YOU", "city", "awe", side=0.0))
b("لكن الطبيعه جربت", bl("الطبيعة جرّبت…", "archive", str2="والنتائج لم تكن كما نتوقع", at2=1.4), cap=False)
b("وفي اخر هذه الحلقه ستعرف", bl("في آخر الحلقة: لماذا لا يمكن؟", "archive", coral=True), cap=False, sfx=[SFX("stinger", 0.1, -10)])
b("لنبدا بامراه حقيقيه", ins("colors", n=3), in_=DIP, music_cut="calm")
b("في عام الفين وعشره نشرت", sc("clinic", [C("SCIENTIST", 0.5, "explain", "determined", 1, s=1.5)], cam=PUSH, labels=[L("غابرييلا جوردان — 2010", y=0.18, ap="غابرييلا", box=True)]))
b("كانت تبحث عن انسان", da(value="4 بدل 3", label="قنوات للألوان", size=170))
b("فمعظمنا يملك في شبكيه", ins("colors", n=3))
b("لكن بعض النساء يحملن", ins("colors", n=4, count="~12%؟"), sfx=[SFX("shimmer", 0.2, -10)])
b("ولهذا سبب عجيب", ins("xchrom"))
b("اما الرجل فيملك نسخه", ins("xchrom", cam=dict(z0=1.2, z1=1.3, x0=-300, x1=-320)))
b("ولهذا يكثر عمى الالوان", da(value="عمى الألوان", label="أكثر بكثير عند الرجال", size=130))
b("فاختبرت جوردان عشرات", sc("clinic", [C("SCIENTIST", 0.62, "point", "thinking", -1), C("PLAIN", 0.38, "sit", "neutral", 1, chair=True)], cam=PUSH))
b("ينظر المشارك الى ضوءين", ins("matchtest"))
b("وواحده فقط نجحت", sc("clinic", [C("DRWOMAN", 0.5, "stand", "smile", 1, s=1.6)], cam=PUSH, labels=[L("طبيبة في شمال إنجلترا", y=0.18, ap="طبيبه", box=True)]))
b("وهناك ايضا الرسامه", sc("studio", [C("PAINTER", 0.45, "holdFront", "joy", 1, prop="paper", s=1.5)], cam=PUSH, labels=[L("كونشيتا أنتيكو", y=0.18, ap="كونشيتا", box=True)]))
b("وهي تصف في مقابلاتها", ins("mural"))
b("يقدر بعض العلماء ان هذه", da(value="عشرات الملايين", label="مقابل نحو مليون لون لنا", size=130))
b("فهل هذه قوه خارقه", bl("المفاجأة الأولى", "archive"), cap=False, in_=DIP, music_cut="tension")
b("لم تكتشف اي من هاتين", sc("home", [C("PAINTER", 0.4, "shrug", "confused", 1), C("PLAIN", 0.62, "shrug", "confused", -1)], cam=PUSH))
b("كل انسان يظن ان العالم", fc("YOU", "home", "thinking", side=0.0))
b("والاغرب ان كثيرا من النساء", ins("colors", n=4))
b("فالعين قد تلتقط المعلومه", da(icon="brain", value="الدماغ", label="لا يتعلم دائما", size=130, count=2))
b("وحتى من تري الالوان الاضافيه", ins("screen"))
b("والمثال الاكثر ادهاشا", ins("shrimp"), sfx=[SFX("whoosh", 0.2, -14)])
b("ثم في عام الفين واربعه عشر", da(value="2014", label="اختبروه… فكان أسوأ منا!", size=170, color="coral"))
b("يبدو انه لا يقارن", bl("أدوات أكثر… لا تعني رؤية أفضل", "archive"), cap=False)
b("والمفاجاه الثانيه اقسى", bl("المفاجأة الثانية", "archive"), cap=False, music_cut="sad")
b("في التراث العربي حكايه", ins("desert"))
b("وفي يوم صعدت الى مكان", ins("desert", cam=dict(z0=1.1, z1=1.25, x0=-200, x1=-260)), sfx=[SFX("wind", 0, -16)])
b("ضحك قومها", st("city", [C("PLAIN", 0.35, "cheer", "smirk", 1), C("PLAIN", 0.55, "cheer", "smirk", -1), C("ZARQA", 0.8, "sad", "sad", -1)], so=dict(mood="golden"), cam=PUSH, labels=[L("أسطورة", x=0.93, y=0.08, size=34, cream=True)]))
b("الحكايه اسطوره لكن", bl("أن ترى أكثر… يعني أن ترى وحدك", "archive", coral=True), cap=False)
b("وهذه هي العزله نفسها", ins("colors", n=4))
b("وهناك قصه حقيقيه اقسي", sc("home", [C("OLDMAN", 0.5, "stand", "neutral", 1, s=1.6)], cam=PUSH, labels=[L("سيدني برادفورد", y=0.18, ap="سيدني", box=True)]))
b("وفي عام الف وتسعمئه وثمانيه", da(value="1958", label="استعاد بصره في الثانية والخمسين", size=160))
b("ودرس حالته عالم النفس", sc("bedroom", [C("OLDMAN", 0.5, "sit", "sad", 1, chair=True, s=1.5)], so=dict(night=True), cam=PULL))
b("ومات بعد اقل من عامين", bl("أن ترى… لا يعني أن تفهم", "archive"), cap=False)
b("لكن هل يمكن ان نحسن بصرنا", ins("underwater"), music_cut="hopeful", in_=DIP)
b("وفي عام الفين وثلاثه قاست", sc("seacafe", [C("SCIENTIST", 0.4, "explain", "smile", 1), C("MOKEN", 0.62, "cheer", "joy", -1)], so=dict(outside=True), cam=PUSH, labels=[L("آنا جيسلين — 2003", y=0.18, ap="انا", box=True)]))
b("فوجدت انهم يرون بوضوح", da(value="×2", label="وضوح تحت الماء", size=200))
b("والسر انهم تعلموا", ins("underwater", cam=dict(z0=1.2, z1=1.35, x0=0, x1=-40)))
b("والاجمل ان اطفالا اوروبيين", da(value="أسابيع", label="من التدريب… فتحسنوا", size=160))
b("وفي الهند بدا عالم الاعصاب", sc("clinic", [C("DOC", 0.6, "explain", "smile", -1), C("PLAIN", 0.4, "sit", "neutral", 1, chair=True, s=1.0)], cam=PUSH, labels=[L("مشروع براكاش — 2005", y=0.18, ap="براكاش", box=True)]))
b("بعد العمليه لا يعرف", sc("home", [C("PLAIN", 0.42, "stand", "confused", 1, s=1.1), C("MOM", 0.6, "reach", "smile", -1)], cam=PUSH))
b("لكن ادمغتهم تتعلم", da(icon="brain", value="الدماغ يتعلم", label="حتى بعد سنوات", size=120, count=2))
b("والعرب قديما كانوا يختبرون", ins("stars"))
b("من راي السها كان", ins("stars", cam=dict(z0=1.3, z1=1.5, x0=200, x1=180)))
b("ومن هنا جاء المثل العربي", bl("أُريها السُّها… وتُريني القمر", "archive"), cap=False)
b("اما اليوم فنقيس البصر", ins("snellen"))
b("والان الى العلم", bl("كيف نرى أصلا؟", "archive"), cap=False, music_cut="calm")
b("يدخل الضوء من القرنيه", ins("eye"))
b("وفي الشبكيه نحو سته ملايين", da(value="6 + 120 مليون", label="مخروط + عُصيّة", size=130))
b("وادق تفاصيل رؤيتك", ins("eye", cam=dict(z0=1.2, z1=1.4, x0=-300, x1=-340)))
b("اما الصوره التي تراها", da(icon="brain", value="دماغك", label="هو الذي يصنع الصورة", size=130, count=2))
b("ويقدر العلماء ان نحو ثلث", da(value="⅓", label="من قشرة الدماغ للبصر", size=200))
b("والنسور تملك في كل عين", ins("eagle"))
b("وهنا سؤال يختلف فيه", ins("photon"))
b("لكن النتيجه كانت اعلى", da(value="محل نقاش", label="أعلى من الصدفة بقليل", size=130))
b("والان الى الجواب الذي", bl("الجواب الموعود", "archive"), cap=False, in_=DIP, sfx=[SFX("stinger", 0.1, -10)])
b("لان الضوء نفسه لا يسمح", da(value="حد الضوء", label="الضوء يتشتت عند الفتحات الصغيرة", size=130))
b("فلكي ترى ادق بمئه مره", ins("eyesize"))
b("ولهذا يبني الفلكيون", da(value="تلسكوب", label="عدسات بعرض أمتار", size=150))
b("وحتى لو امتلكت تلك العين", da(icon="brain", value="حمل هائل", label="على الدماغ", size=130, count=2))
b("فعينك ليست ضعيفه", ar(hero=True, heroC="YOU", pose="relaxed", expr="smile", n=40, cards=["حل ذكي", "الدماغ يتعلم", "الموكن", "زرقاء اليمامة"], cardsX=[0.2, 0.8, 0.22, 0.78], cardsY=[0.22, 0.22, 0.45, 0.45], gap=1.4), music_cut="hopeful")
b("وفي الحلقه القادمه", bl("ماذا لو كانت كل رائحة أقوى بألف مرة؟", "archive", str2="الحلقة القادمة", at2=0.8), cap=False, sfx=[SFX("riser", 0, -12)])
b("والان سؤال الحلقه", dict(tpl="endscreen", q="لو خُيّرت: بصر النسر… أم ألوان لا يراها غيرك؟", cast=["SCIENTIST", "PAINTER", "ZARQA", "MOKEN", "OLDMAN", "DOC"]), in_=FADE, cap=False)

# ---- resolve anchors -> contiguous shots ----
shots = []; pos = 0; idxs = []
for anchor, params, meta in B:
    i = find(anchor, pos); idxs.append(i); pos = i + 1
starts = [0.0] + [max(0.0, W[i]["start"] - 0.15) for i in idxs[1:]]
for k in range(1, len(starts)):
    if starts[k] < starts[k - 1] + 0.6: starts[k] = starts[k - 1] + 0.6
for k, ((anchor, params, meta), i) in enumerate(zip(B, idxs)):
    s0 = round(starts[k], 3); s1 = round(starts[k + 1], 3) if k + 1 < len(B) else DUR
    j1 = idxs[k + 1] if k + 1 < len(B) else len(W)
    line = " ".join(re.sub(r"[ً-ْٰ]", "", w["word"]) for w in W[i:j1])
    p = json.loads(json.dumps(params))
    def rel(phrase, end=False):
        a = find(phrase, max(0, i - 3)); n = len([x for x in phrase.split() if norm(x)])
        return round((W[a + n - 1]["end"] if end else W[a]["start"]) - s0, 2)
    for ch in p.get("chars", []):
        if "tp" in ch: ch["talk"] = [rel(ch["tp"]), rel(ch["tp"], True)]; del ch["tp"]
    if "talkp" in p: p["talk"] = [rel(p["talkp"]), rel(p["talkp"], True)]; del p["talkp"]
    for Lb in p.get("labels", []):
        if "ap" in Lb: Lb["at"] = max(0.1, rel(Lb["ap"]) - 0.1); del Lb["ap"]
    for pin in p.get("pins", []):
        if len(pin) > 3 and isinstance(pin[3], str): pin[3] = max(0.1, rel(pin[3]) - 0.1)
    sh = {"id": f"s{k + 1:03d}", "start": s0, "end": s1, "line": line, "scene": f"{p['tpl']} {p.get('set', p.get('kind', ''))}",
          "set": p.get("set", ""), "bars": meta.get("bars"), "in": meta.get("in_", {"type": "cut"}), "sfx": meta.get("sfx", []), "params": p, "notes": ""}
    if "amb" in meta: sh["amb"] = meta["amb"]
    if meta.get("cap") is False: sh["captions"] = False
    shots.append(sh)
base_shots = list(shots)


# ---- auto-split long shots (> 6 s) at a word boundary for a livelier pace ----
VAR = [dict(z0=1.12, z1=1.2, x0=40, x1=-20), dict(z0=1.0, z1=1.06, x0=-60, x1=30)]
out = []
for sh in shots:
    d = sh["end"] - sh["start"]; tpl = sh["params"]["tpl"]
    if d > 5.0 and tpl in ("stage", "insert", "archive", "data"):
        n = 2 if d < 11 else 3; cuts = [sh["start"] + d * k / n for k in range(1, n)]
        cut_t = []
        for c in cuts:
            ws = [w["start"] - 0.12 for w in W if sh["start"] + 1.5 < w["start"] - 0.12 < sh["end"] - 1.5]
            cut_t.append(min(ws, key=lambda x: abs(x - c)) if ws else c)
        bounds = [sh["start"]] + sorted(set(round(x, 3) for x in cut_t)) + [sh["end"]]
        for k in range(len(bounds) - 1):
            p2 = json.loads(json.dumps(sh["params"]))
            if k > 0:
                p2["cam"] = VAR[(k - 1) % 2]
                for Lb in p2.get("labels", []): Lb["at"] = max(0.05, Lb.get("at", 0.3) - (bounds[k] - bounds[0]))
            s2 = dict(sh, start=bounds[k], end=bounds[k + 1], params=p2)
            if k > 0: s2["in"] = {"type": "cut"}; s2["sfx"] = []
            out.append(s2)
    else: out.append(sh)
for i, sh in enumerate(out): sh["id"] = f"s{i + 1:03d}"
shots = out

# music sections from music_cut markers
music = []; cur = ("playful", 0.35, 0.0)
cuts = {"sad": ("sad", 0.35), "hopeful": ("hopeful", 0.35), "tension": ("tension", 0.6), "calm": ("calm", 0.3)}
for (anchor, params, meta), sh in zip(B, base_shots):
    if sh["params"]["tpl"] == "title": music.append({"start": cur[2], "end": sh["start"], "mood": cur[0], "intensity": cur[1]}); cur = ("wonder", 0.4, sh["start"])
    if sh["id"] == "s032": pass
    if "music_cut" in meta:
        music.append({"start": cur[2], "end": sh["start"], "mood": cur[0], "intensity": cur[1]}); m, it = cuts[meta["music_cut"]]; cur = (m, it, sh["start"])
music.append({"start": cur[2], "end": DUR, "mood": cur[0], "intensity": cur[1]})
# montage after title back to playful
for k, m in enumerate(music):
    if m["mood"] == "wonder":
        t_end = m["end"]; m["end"] = round(m["start"] + 8, 3); music.insert(k + 1, {"start": m["end"], "end": t_end, "mood": "playful", "intensity": 0.45}); break
story = {"title": "ماذا لو كان بصرك أحد بمئة مرة؟", "duration": DUR, "shots": shots, "music": music, "sfx": []}
json.dump(story, open(f"{PROJ}/story/shots.json", "w"), ensure_ascii=False, indent=1)
d = [s["end"] - s["start"] for s in shots]; d.sort()
print(len(shots), "shots; median", round(d[len(d) // 2], 2), "min", round(d[0], 2), "max", round(d[-1], 2))
print("music:", [(m["mood"], round(m["start"]), round(m["end"])) for m in music])
