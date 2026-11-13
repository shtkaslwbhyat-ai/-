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
Z = lambda x, pose="stand", expr="neutral", f=1, **kw: C("ZAID", x, pose, expr, f, **kw)
LI = lambda x, pose="stand", expr="happy", f=-1, **kw: C("LINA", x, pose, expr, f, **kw)
NIGHT = dict(night=True, sky="night")

b("نمت ساعه واحده فقط", fc("ZAID", "bedroom", "smirk", side=0.0, labels=[L("ساعة واحدة… منذ 3 سنوات", y=0.18, ap="نمت", box=True)]), amb={"name": "roomtone", "gain": -28}, sfx=[SFX("stinger", 0.1, -10)])
b("ولم تشعر بالتعب", st("bedroom", [Z(0.45, "relaxed", "smile", s=1.6)], cam=PUSH, clock=[3, 0]))
b("المدينه كلها نائمه", st("city", [], so=dict(mood="night"), cam=DRIFT, labels=[L("3:00 فجرا", y=0.2, ap="المدينه", box=True)]))
b("وانت انهيت روايه كامله", ins("mural"), sfx=[SFX("swish", 0.3, -12)])
b("وما زال امامك ثلاث ساعات", st("bedroom", [Z(0.45, "holdFront", "smile", prop="paper")], cam=PUSH, clock=[3, 0]))
b("الناس ينامون ثلث اعمارهم", da(value="⅓", label="من أعمارنا… نوم", size=200))
b("فتعيش ثلاثا وعشرين ساعه", ins("clock24"), sfx=[SFX("tick", 0.2, -14)])
b("سبع ساعات اضافيه", da(value="+100 يوم", label="إضافي كل سنة", size=170), sfx=[SFX("shimmer", 0.2, -10)])
b("لكن لهذه القوه قاعده", bl("قاعدة واحدة", "bedroom", str2="الوقت الذي تعيشه وحدك… لا يساوي شيئا", at2=1.6), cap=False)
b("اسمك زيد", st("city", [Z(0.5, "relaxed", "smile", s=1.8)], so=dict(mood="day"), cam=PUSH, labels=[L("زيد", y=0.2, ap="زيد", size=90), L("20 عاما", y=0.32, ap="عشرون", cream=True)]))
b("وستتعلم يوما ان اجمل", fc("ZAID", "city", "thinking", side=0.0, labels=[L("أجمل ساعاتك… التي تعطيها", y=0.18, ap="اجمل")]))
b("فماذا لو احتجت الى ساعه", dict(tpl="title", lines=["ماذا لو", "احتجت إلى ساعة نوم واحدة فقط؟"]), in_=FADE, bars="scope", cap=False, sfx=[SFX("riser", 0, -12)])
b("في البدايه يبدو الامر", st("classroom", [Z(0.5, "explain", "smirk")], cam=PUSH, labels=[L("طب + هندسة", y=0.18, ap="تخصصين", box=True)]), in_=DIP)
b("تتعلم العزف على العود", st("bedroom", [Z(0.45, "sit", "smile", chair=True)], cam=PUSH, labels=[L("العود في شهرين", y=0.18, ap="العود", box=True)]), sfx=[SFX("ding", 0.6, -14)])
b("وتقرا ثلاثمئه كتاب", da(value="300", label="كتاب في سنة", size=200))
b("وفي الثانيه فجرا تعمل", st("bakery", [Z(0.42, "holdFront", "smile"), C("SALEH", 0.62, "explain", "happy", -1)], cam=PUSH), amb={"name": "roomtone", "gain": -26})
b("العجين والفرن", ins("bread", noQ=True))
b("العم صالح يعمل في الليل", st("bakery", [C("SALEH", 0.55, "holdFront", "smile", -1, s=1.7)], cam=PUSH, labels=[L("40 عاما في الليل", y=0.18, ap="اربعين", box=True)]))
b("يقول لك انت اول شاب", fc("SALEH", "bakery", "smile", side=0.25, rimSide=1, talkp="انت اول شاب لا يتثاءب"))
b("وفي الخامسه تركض", st("seacafe", [Z(0.3, walk=[0.15, 0.85], run=True)], so=dict(outside=True), cam=DRIFT))
b("ثم تفتح مشروعك الصغير", st("city", [Z(0.35, walk=[0.2, 0.7]), C("PLAIN", 0.8, "wave", "happy", -1)], so=dict(mood="golden"), cam=DRIFT))
b("بعد سته اشهر يعمل معك", st("bakery", [Z(0.5, "cheer", "joy", s=1.3), C("PLAIN", 0.3, "cheer", "joy", 1, s=1.2), C("PLAIN", 0.72, "cheer", "joy", -1, s=1.2)], cam=PULL, labels=[L("10 شبان", y=0.18, ap="عشره", box=True)]))
b("وتدفع ديون ابيك", st("home", [Z(0.4, "holdFront", "smile", prop="paper"), C("DAD", 0.6, "handsOnHead", "joy", -1), C("MOM", 0.78, "cheer", "joy", -1)], cam=PUSH))
b("الصحف تسميك", ins("news", head="الشاب الذي لا ينام", who="ZAID"), sfx=[SFX("impact", 0.2, -10)])
b("والاطباء يطلبون فحصك", st("clinic", [Z(0.42, "sitBack", "neutral", chair=True), C("DOC", 0.64, "think", "thinking", -1)], cam=PUSH))
b("يقول الطبيب ان دماغك", ins("eeg"), sfx=[SFX("blip", 0.4, -14)])
b("ويسالك سؤالا غريبا", fc("DOC", "clinic", "thinking", side=0.2, rimSide=1, labels=[L("متى حلمت آخر مرة؟", y=0.18, ap="متي", box=True)]))
b("وانت لا تتذكر", fc("ZAID", "clinic", "confused", side=0.0), music_cut="sad")
b("لكن الليل طويل", st("city", [Z(0.5, "stand", "sad", s=1.2)], so=dict(mood="night"), cam=PULL))
b("في البدايه كنت ترسل الرسائل", ins("chat"))
b("وحين يضحكون في الصباح", st("classroom", [C("PLAIN", 0.3, "cheer", "joy", 1), C("PLAIN", 0.48, "cheer", "joy", -1), Z(0.78, "stand", "sad", -1)], cam=PUSH))
b("صرت تسبق الجميع", fc("ZAID", "classroom", "sad", side=0.0))
b("في عرس صديقك احمد", st("studio", [C("PLAIN", 0.35, "cheer", "joy", 1), C("PLAIN", 0.5, "cheer", "joy", 1), Z(0.65, "cheer", "smile", -1)], crowd=0.6, cam=DRIFT), sfx=[SFX("cheer", 0.2, -18)])
b("وانت تبقى في الشارع الفارغ", st("city", [Z(0.5, "stand", "sad", still=True)], so=dict(mood="night"), cam=PULL, labels=[L("6 ساعات أخرى", y=0.18, ap="ست", box=True)]))
b("تعرف المدينه في الليل", st("city", [C("PLAIN", 0.3, walk=[0.1, 0.4]), C("NURSE", 0.7, walk=[0.9, 0.6]), Z(0.5, "stand", "neutral")], so=dict(mood="night"), cam=DRIFT))
b("فتجلس في المخبز", st("bakery", [Z(0.4, "sit", "sad", chair=True), C("SALEH", 0.62, "holdFront", "neutral", -1)], cam=PUSH))
b("ويقول لك يوما وهو يعجن", fc("SALEH", "bakery", "smile", side=0.25, rimSide=1, labels=[L("لمن ينتظره أحد في الصباح", y=0.18, ap="لمن", box=True)]))
b("وفي البيت اختك الصغيره", st("home", [LI(0.58, "holdFront", "happy", prop="book"), Z(0.38, "sit", "neutral", chair=True)], cam=PUSH, labels=[L("لينا 6 سنوات", x=0.58, y=0.2, ap="لينا", box=True)]), music_cut="calm")
b("وانت تقول غدا يا لينا", fc("LINA", "home", "sad", side=0.3, rimSide=1))
b("وكل صباح تجلس بجانبك", st("home", [LI(0.58, "explain", "joy", chair=True, pose="sit") if False else LI(0.58, "explain", "joy"), Z(0.38, "sit", "neutral", chair=True)], props=[dict(k="table", x=0.48, plate=True)], cam=PUSH))
b("حلمت اني اطير فوق البحر", ins("dreamsea"))
b("ثم تسالك وانت بماذا حلمت", fc("LINA", "home", "smile", side=0.3, rimSide=1, talkp="بماذا حلمت"))
b("وانت لا تعرف بماذا تجيب", fc("ZAID", "home", "sad", side=0.0, labels=[L("لا أحلام منذ 3 سنوات", y=0.18, ap="تحلم", box=True, coral=True)]))
b("وبدات اشياء صغيره تتغير", fc("ZAID", "bedroom", "angry", side=0.0))
b("وتنسى وجوه الناس", st("city", [Z(0.5, "think", "confused"), C("PLAIN", 0.7, "wave", "happy", -1)], so=dict(mood="day"), cam=PUSH))
b("والالوان في جداريتك", ins("mural", gray=True))
b("امك تلاحظ", st("home", [C("MOM", 0.58, "reach", "sad", -1), Z(0.4, "stand", "neutral")], cam=PUSH, labels=[L("هنا معنا… ولست معنا", y=0.18, ap="هنا", box=True)]))
b("ثم تاتي تلك الليله", bl("ليلة المسابقة", "bedroom"), cap=False, in_=DIP, music_cut="tension", sfx=[SFX("impact", 0.2, -10)])
b("مشروع عملت عليه ثمانيه", st("bedroom", [Z(0.45, "sit", "determined", chair=True)], props=[dict(k="desk", x=0.6)], cam=PUSH, labels=[L("التسليم 6:00 صباحا", y=0.18, ap="والتسليم", box=True, coral=True)]))
b("ابوك وامك مسافران", st("home", [Z(0.45, "stand", "neutral"), LI(0.6, "stand", "sleepy")], so=NIGHT, cam=PULL))
b("في الثالثه فجرا تسمع", fc("ZAID", "bedroom", "shocked", side=0.0), sfx=[SFX("heartbeat", 0, -10)])
b("صفير في صدرها", ins("breath"), sfx=[SFX("wind", 0, -18)])
b("تحملها الى السياره", st("city", [Z(0.4, walk=[0.3, 0.7], run=True)], so=dict(mood="night"), cam=DRIFT))
b("وتعد انفاسها كما علمك", ins("breath"))
b("الشوارع فارغه", st("city", [], props=[dict(k="taxi", x=0.5, move=True)], so=dict(mood="night"), cam=DRIFT))
b("تشكر الله انك لا تنام", fc("ZAID", "city", "determined", side=0.0))
b("في الطوارئ يقول الطبيب", st("clinic", [C("DOC", 0.62, "explain", "neutral", -1), Z(0.38, "stand", "worried"), C("NURSE", 0.82, "stand", "neutral", -1)], cam=PUSH))
b("الساعه الان الرابعه والنصف", st("clinic", [Z(0.45, "sit", "worried", chair=True)], cam=PUSH, clock=[4, 30], labels=[L("1:30 على التسليم", y=0.18, ap="ساعه", box=True, coral=True)]), sfx=[SFX("tick", 0.2, -14)])
b("ثم تمسك لينا يدك", st("clinic", [Z(0.42, "sit", "worried", chair=True, s=1.7), LI(0.6, "reach", "scared", s=1.5)], cam=PUSH))
b("وتقول بصوت ضعيف", fc("LINA", "clinic", "scared", side=0.3, rimSide=1, talkp="لا تذهب"))
b("وهنا تفهم امامك طريقان", bl("أمامك طريقان", "clinic"), cap=False)
b("اما ان تاخذ الساعه", ar(hero=True, heroC="ZAID", pose="think", expr="thinking", n=50, cards=["المشروع", "المسابقة", "السنوات"], cardsX=[0.2, 0.5, 0.8], cardsY=[0.25, 0.18, 0.25], gap=0.6))
b("واما ان تعطيها لها", fc("ZAID", "clinic", "determined", side=0.0), in_=FLASH, sfx=[SFX("shimmer", 0, -10)], music_cut="calm")
b("تطفئ الهاتف تجلس", st("clinic", [Z(0.45, "sit", "smile", chair=True, s=1.6), LI(0.62, "sitBack", "sleepy", chair=True, s=1.4)], cam=PUSH), bars="scope")
b("كان يا ما كان", ins("storybook"), sfx=[SFX("shimmer", 0.3, -14)])
b("تضحك لينا تحت القناع", fc("LINA", "clinic", "joy", side=0.3, rimSide=1))
b("وتكمل القصه حتى بعد", st("clinic", [Z(0.45, "sit", "smile", chair=True, s=1.7), LI(0.62, "sitBack", "sleepy", chair=True, s=1.5)], cam=dict(z0=1.1, z1=1.2, x0=0, x1=-20)), bars="scope")
b("وفي مكان ما بين البحر", ins("dreamsea"), music_cut="hopeful")
b("تستيقظ في السابعه", st("clinic", [Z(0.45, "sitBack", "sleepy", chair=True)], cam=PUSH, clock=[7, 0]))
b("ولينا تنظر اليك وتبتسم", fc("LINA", "clinic", "smile", side=0.3, rimSide=1, talkp="بماذا حلمت"))
b("ولاول مره عندك جواب", fc("ZAID", "clinic", "joy", side=0.0))
b("وحين تصل امك ظهرا", st("clinic", [C("MOM", 0.62, "handsOnHead", "joy", -1), Z(0.4, "sitBack", "sleepy", chair=True)], cam=PUSH))
b("بعد اسبوع ترسل مشروعك", da(value="مجانا", label="للمستشفى", size=170))
b("وصرت تقضي ليلتين", st("clinic", [Z(0.5, "holdFront", "smile", prop="book", s=1.3), C("PLAIN", 0.3, "sit", "smile", 1, chair=True, s=1.0), C("PLAIN", 0.7, "sit", "joy", -1, chair=True, s=1.0)], cam=PUSH))
b("وصارت الممرضات", st("clinic", [C("NURSE", 0.35, "wave", "happy", 1), Z(0.6, "wave", "smile", -1)], cam=PULL))
b("وفي كل مساء تاتيك لينا", st("home", [LI(0.58, "holdFront", "happy", prop="book"), Z(0.38, "sit", "smile", chair=True)], cam=PUSH))
b("ما زلت تنام ساعه واحده", st("bedroom", [Z(0.45, "relaxed", "smile", s=1.6)], cam=PULL, clock=[23, 0]))
b("لكنك تعلمت اخيرا ان", fc("ZAID", "home", "smile", side=0.0, labels=[L("أجمل ساعة… التي تعطيها", y=0.18, ap="اجملها")]))
b("فما الحقيقي في هذه القصه", bl("ما الحقيقي في هذه القصة؟", "archive"), in_=DIP, cap=False, music_cut="calm")
b("توصي جمعيات طب النوم", da(value="7+ ساعات", label="توصية النوم للبالغين", size=160))
b("لكن هناك اشخاصا نادرين", da(value="قصيرو النوم", label="الطبيعيون: نادرون جدا", size=130))
b("في عام الفين وتسعه وجد", da(value="2009", label="أم وابنتها: نحو 6 ساعات", size=160))
b("والسبب تغير نادر", da(icon="brain", value="جين واحد", label="تغير نادر", size=130, count=2))
b("اما ساعه واحده فقط", da(value="ساعة واحدة؟", label="لم يوثقها العلم", size=140, color="coral"))
b("وفي عام الف وتسعمئه", da(value="11 يوما", label="بلا نوم — 1964", size=170, color="coral"))
b("وبسبب خطوره مثل", da(value="غينيس", label="توقفت عن تسجيل هذا الرقم", size=150))
b("ولماذا لم يحلم زيد", ins("hypno"))
b("وفي النوم ايضا يثبت", da(icon="brain", value="تثبيت الذاكرة", label="أثناء النوم", size=110, count=2))
b("وفي عام الفين وثلاثه عشر", da(value="2013", label="الدماغ يغسل فضلاته أثناء النوم (في الفئران)", size=150))
b("اما عند الانسان فما زال", da(value="محل نقاش", label="عند الإنسان", size=140))
b("ومن اغرب اسرار النوم", ins("dolphin"))
b("ويبقى سؤال يختلف فيه", da(value="لماذا نحلم؟", label="سؤال بلا جواب نهائي", size=140))
b("فالنوم ليس وقتا ضائعا", bl("النوم… وقت يصلح فيه الدماغ نفسه", "archive"), cap=False)
b("وفي الحلقه القادمه", bl("ماذا لو التأمت جروحك أسرع بمئة مرة… إلا جرحا واحدا؟", "archive", str2="الحلقة القادمة", at2=0.8, size=64), cap=False, sfx=[SFX("riser", 0, -12)])
b("ما رايك اخبرنا", dict(tpl="endscreen", q="7 ساعات إضافية كل يوم… ماذا ستفعل بها؟", cast=["MOM", "ZAID", "LINA", "SALEH", "NURSE", "DOC"]), in_=FADE, cap=False)

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
story = {"title": "ماذا لو احتجت إلى ساعة نوم واحدة فقط؟", "duration": DUR, "shots": shots, "music": music, "sfx": []}
json.dump(story, open(f"{PROJ}/story/shots.json", "w"), ensure_ascii=False, indent=1)
d = [s["end"] - s["start"] for s in shots]; d.sort()
print(len(shots), "shots; median", round(d[len(d) // 2], 2), "min", round(d[0], 2), "max", round(d[-1], 2))
print("music:", [(m["mood"], round(m["start"]), round(m["end"])) for m in music])
