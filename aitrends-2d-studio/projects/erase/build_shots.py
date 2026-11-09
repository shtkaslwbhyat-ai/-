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
K = lambda x, pose="stand", expr="neutral", f=1, **kw: C("KARIM", x, pose, expr, f, **kw)
OUT = dict(outside=True)

b("تفتح عينيك السقف ابيض", st("bedroom", [K(0.19, "lie", [[0, "sleepy"], [1.2, "surprised"]], y=0.815, still=True, s=1.3, rot=-1.5708)], cam=PUSH), amb={"name": "roomtone", "gain": -28})
b("لكن على المراه ورقه", ins("notes", notes=["لا تخف", "اقرأ هذا أولا"]), sfx=[POP(0.3, -14)])
b("تقترب تحتها ورقه ثانيه", ins("notes", notes=["لا تخف", "اقرأ هذا أولا", "اسمك كريم", "26 عاما"]), sfx=[POP(0.9, -16)])
b("واليوم هو اليوم المئه", fc("KARIM", "bedroom", [[0, "confused"], [1.4, "smirk"]], labels=[L("اليوم 100", y=0.2, at=0.2, box=True)]))
b("ثم ترى الدفتر الازرق", ins("notebook", pages=100, head="لا تخف"), sfx=[SFX("counter", 0.3, -16)])
b("في الليل لا ينام دماغك", da(icon="brain", value="الدماغ لا ينام", label="يثبّت ذكريات اليوم", size=100, at=0.3, count=3), in_=DIP)
b("ولجزء صغير في عمق", da(icon="brain", value="الحُصين", label="ذكريات اليوم تمر من هنا", size=120, count=2))
b("هكذا يصير يومك ذكرى", ar(hero=True, heroC="KARIM", expr="thinking", labels=[L("اسمك", x=0.22, y=0.25, ap="اسمك"), L("أهلك", x=0.5, y=0.18, ap="اهلك"), L("طفولتك", x=0.78, y=0.25, ap="طفولتك")]))
b("لكن كل يوم جديد يمحى", dict(tpl="freeze", set="bedroom", who="KARIM", expr=[[0, "neutral"], [1.0, "sad"]]), in_=FLASH, bars="scope", sfx=[SFX("freeze", 0, -6)])
b("وهناك قاعده واحده", bl("قاعدة واحدة", "bedroom", str2="ما تتعلمه يداك وقدماك… يبقى", at2=2.0), cap=False, sfx=[SFX("stinger", 0.1, -10)])
b("فالذاكره ليست في الراس", bl("الذاكرة ليست في الرأس وحده", "bedroom"), cap=False)
b("فماذا لو كان كل يوم يمحى", dict(tpl="title", lines=["ماذا لو", "كان كل يوم يُمحى من ذاكرتك؟"]), in_=FADE, bars="scope", cap=False, sfx=[SFX("riser", 0, -12)])
b("تبدا كل صباح بالدفتر", st("bedroom", [K(0.45, "holdFront", "thinking", prop="paper", s=1.6)], cam=PUSH, clock=[7, 0], labels=[L("30 دقيقة", y=0.2, ap="ثلاثون", box=True)]), in_=DIP)
b("صديقك سامر يحكي لك", st("city", [C("SAMER", 0.6, "explain", "happy", -1), K(0.38, "stand", "neutral")], so=dict(mood="golden"), cam=PUSH, labels=[L("منذ شهرين", y=0.18, ap="منذ شهرين", box=True)]), amb={"name": "city", "gain": -26})
b("وانت تضحك كل مره", fc("KARIM", "city", "joy", side=-0.2))
b("هو اسعد صديق في العالم", fc("SAMER", "city", "joy", side=0.3, rimSide=1))
b("تذهب الى السوق بقائمه", st("city", [K(0.4, walk=[0.3, 0.6])], so=dict(mood="golden", market=True), cam=DRIFT))
b("ثم تجد في المطبخ ثلاثه", ins("bread"), sfx=[POP(0.3), POP(0.65), POP(1.0)])
b("فتضيف الى الدفتر قاعده", ins("notebook", pages=40, head="لا تشتر الخبز!"))
b("فيلمك المفضل شاهدته", st("home", [K(0.4, "sitBack", "happy", chair=True)], props=[dict(k="tv", x=0.75)], cam=PUSH, labels=[L("27 مرة", y=0.18, ap="سبعا", box=True)]))
b("وفي كل مره تفاجئك النهايه", fc("KARIM", "home", [[0, "surprised"], [1.0, "awe"]], side=0.0))
b("وهناك ما هو اغرب امك تضع", st("home", [C("MOM", 0.6, "point", "smile", -1), K(0.38, "stand", "confused")], cam=PUSH))
b("في اليوم الاول لا تعرف", fc("KARIM", "home", "confused", side=-0.2, labels=[L("اليوم 1", y=0.2, at=0.1, box=True)]))
b("في اليوم الستين تعزف", ins("piano", labels=[L("اليوم 60", y=0.12, at=0.1, box=True)]), sfx=[SFX("shimmer", 0.3, -14)])
b("يداك تتذكران عنك", bl("يداك تتذكران عنك", "home"), cap=False)
b("والاجمل انت لا تحمل", st("city", [K(0.4, "wave", "smile"), C("SAMER", 0.6, "wave", "happy", -1)], so=dict(mood="golden"), cam=PUSH))
b("الخلاف الذي حدث امس", fc("KARIM", "city", "smile", side=-0.1))
b("كل صباح صفحه بيضاء", ins("notebook", pages=1, head="صفحة بيضاء"))
b("وفي العياده يعطيك طبيبك", st("clinic", [C("DOC", 0.62, "explain", "smile", -1), K(0.38, "sit", "neutral", chair=True)], cam=PUSH), amb={"name": "hum", "gain": -28})
b("ترسم نجمه وانت لا ترى", ins("star", messy=True, timeLabel="6 دقائق"))
b("في اليوم العاشر في دقيقه", ins("star", messy=False, timeLabel="دقيقة واحدة"), sfx=[SFX("ding", 2.4, -12)])
b("وانت تقسم انك ترى", fc("KARIM", "clinic", "confused", side=0.0))
b("يقول لك طبيبك ان حالتك", st("clinic", [C("DOC", 0.3, "point", "neutral", 1), K(0.7, "stand", "thinking", f=-1)], cam=DRIFT))
b("اشخاص فقدوا القدره", da(value="حالات حقيقية", label="فقدوا القدرة على صنع ذكريات جديدة", size=100))
b("ويريك رقما ثلاثه الاف", da(to=3200, label="سطر في دفترك", count=1.6), sfx=[SFX("counter", 0.3, -16)])
b("كلها لرجل لا تتذكره", fc("KARIM", "clinic", "sad", side=0.0), bars="scope")
b("لكن للصفحه البيضاء ثمنا", ar(hero=True, heroC="KARIM", expr="worried", cards=["مريم"], cardsX=[0.72], cardsY=[0.3], gap=1.0), music_cut="sad", in_=DIP)
b("كل صباح تطرق الباب", st("home", [C("MARYAM", 0.6, [[0, "stand"], [0.8, "wave"]], "smile", -1), K(0.38, "stand", "confused")], cam=PUSH, labels=[L("خطيبتك", x=0.6, y=0.2, ap="خطيبتك", box=True)]))
b("تبتسم لك كان الامر", fc("MARYAM", "home", "smile", side=0.3, rimSide=1))
b("وفي الصفحه السبعين كتبت", ins("notebook", pages=70, head="رأيتها تبكي"))
b("انت لا تكبر معها", st("home", [C("MARYAM", 0.66, "sad", "sad", -1), K(0.3, "stand", "sad")], so=dict(night=True, sky="night"), cam=PULL))
b("صرت تسجل لنفسك مقطعا", ins("selfvideo"))
b("لكنك في الصباح تنظر", fc("KARIM", "bedroom", "confused", side=0.0))
b("فكيف تعد امراه بالغد", bl("كيف تعد بالغد… وأنت لا تملك أمس؟", "home", coral=True), cap=False)
b("لكن مريم لا تستسلم", st("city", [C("MARYAM", 0.45, walk=[0.3, 0.55]), K(0.35, walk=[0.2, 0.45])], so=dict(mood="dusk"), cam=DRIFT), music_cut="hopeful", amb={"name": "city", "gain": -28})
b("شارع المخبز ثم الجسر", st("bakery", [C("MARYAM", 0.5, walk=[0.35, 0.6]), K(0.4, walk=[0.25, 0.5])], cam=DRIFT, labels=[L("شارع المخبز", y=0.2, at=0.1, box=True)]))
b("ثم الدرج الحجري", st("seacafe", [C("MARYAM", 0.55, "stand", "smile", 1), K(0.42)], so=OUT, props=[dict(k="sand"), dict(k="stairs", x=0.3)], cam=PUSH))
b("ثم الصخره الكبيره عند", st("seacafe", [C("MARYAM", 0.62, "stand", "happy", -1), K(0.38, "stand", "smile")], so=OUT, props=[dict(k="sand"), dict(k="rock", x=0.5)], cam=PUSH, bars="scope"), amb={"name": "wind", "gain": -26})
b("هناك تجلسان وتحكي لك", fc("MARYAM", "seacafe", "happy", side=0.3, rimSide=1))
b("في محطه الحافلات تحت", st("city", [C("MARYAM", 0.58, "stand", "smile", -1), K(0.42, "stand", "awe")], so=dict(mood="storm"), rain=True, cam=PUSH), in_=FADE)
b("وانت تسمع القصه كانها", fc("KARIM", "seacafe", "awe", side=-0.2))
b("وهناك تقول لك كل مره", fc("MARYAM", "seacafe", "smile", side=0.3, rimSide=1, talkp="انت لا تتذكرني لكنك تجدني دائما"), bars="scope")
b("مئه مساء على الطريق", da(value="100 مساء", label="على الطريق نفسه", size=130))
b("لكن قدميك تمشيانه", st("bakery", [K(0.4, walk=[0.3, 0.6])], cam=dict(z0=1.3, z1=1.38, x0=0, x1=-30, y0=180, y1=185)))
b("ثم ياتي اليوم الواحد بعد", st("home", [K(0.5, "relaxed", "neutral")], cam=PUSH, labels=[L("اليوم 101", y=0.18, at=0.2, box=True)]), in_=DIP, music_cut="tension")
b("يرن هاتفك صوت مريم", ins("phonering", caller="مريم", callerColor="#e8735a"), sfx=[SFX("phonering", 0, -10)])
b("اخوها يونس ثماني سنوات", fc("YOUNES", "seacafe", "scared", side=0.2, rimSide=1, labels=[L("8 سنوات", y=0.18, ap="ثماني", box=True)]))
b("وهي عالقه في المستشفى", st("clinic", [C("MARYAM", 0.5, "phone", "scared", 1, prop="phone", s=1.7)], cam=PUSH))
b("انت الاقرب الى البحر", st("seacafe", [], so=dict(outside=True, sunset=0.4), props=[dict(k="sand")], cam=PULL, labels=[L("20 دقيقة", y=0.2, ap="عشرين", coral=True, box=True)]), amb={"name": "wind", "gain": -22})
b("ثم ينطفئ الهاتف", fc("KARIM", "home", [[0, "worried"], [0.8, "shocked"]], side=0.0), sfx=[SFX("glitch", 0.3, -14)])
b("والشاطئ طويل كيلومتران", da(value="2 كم", label="من الرمل والصخور", size=150, color="coral"))
b("تفتح الدفتر الطريق مكتوب", ins("notebook", pages=3200, head="أين الطريق؟"), sfx=[SFX("heartbeat", 0, -12)])
b("صفحه اليوم الثالث", ins("notebook", pages=60, head="لا شيء عن الطريق"), sfx=[SFX("clock", 0, -12)])
b("وهنا تفهم امامك طريقان", bl("أمامك طريقان", "home"), cap=False)
b("اما ان تبحث في ذاكره", ar(hero=True, heroC="KARIM", pose="handsOnHead", expr="scared", n=80, speed=3, cam=dict(z0=1.0, z1=1.25, x0=0, x1=0, shake=4)))
b("واما ان تغلق الدفتر", fc("KARIM", "home", "determined", side=0.0), in_=FLASH, sfx=[SFX("shimmer", 0, -10)])
b("تغلق الدفتر تخرج", st("city", [K(0.3, walk=[0.15, 0.8], run=True)], so=dict(mood="dusk"), cam=DRIFT), sfx=[SFX("footstep", 0.4, -14), SFX("footstep", 0.9, -14)])
b("شارع المخبز قدماك", st("bakery", [K(0.4, walk=[0.2, 0.7], run=True)], cam=DRIFT, labels=[L("شارع المخبز", y=0.2, at=0.1, box=True)]))
b("الجسر الصغير لا تعرف", st("city", [K(0.4, walk=[0.25, 0.7])], so=dict(mood="dusk"), props=[dict(k="bridge", x=0.5)], cam=PUSH))
b("الدرج الحجري تعد", st("seacafe", [K(0.35, walk=[0.2, 0.5])], so=OUT, props=[dict(k="sand"), dict(k="stairs", x=0.35)], cam=PUSH))
b("وهناك عند الصخره الكبيره", st("seacafe", [C("YOUNES", 0.56, "sad", "cry", -1)], so=dict(outside=True, sunset=0.6), props=[dict(k="sand"), dict(k="rock", x=0.62)], cam=PUSH, bars="scope"), music_cut="hopeful")
b("يرفع راسه ويقول", fc("YOUNES", "seacafe", "sad", side=0.2, rimSide=1, talkp="اختي تاتي الى هنا كل يوم فانتظرتها"))
b("تجلس بجانبه يضع يده", st("seacafe", [K(0.44, "kneel", "smile"), C("YOUNES", 0.54, "stand", "smile", -1)], so=dict(outside=True, sunset=0.8), props=[dict(k="sand"), dict(k="rock", x=0.7)], cam=PUSH))
b("وبعد نصف ساعه تركض", st("seacafe", [C("MARYAM", 0.6, walk=[0.85, 0.6], run=True), K(0.3, "stand", "neutral"), C("YOUNES", 0.38, "cheer", "joy", 1)], so=dict(outside=True, sunset=0.9), props=[dict(k="sand")], cam=DRIFT))
b("لكن يدك تمتد الى يدها", st("seacafe", [K(0.43, "reach", "smile", s=1.9), C("MARYAM", 0.57, "reach", "joy", -1, s=1.9)], so=dict(outside=True, sunset=1.0), props=[dict(k="sand")], cam=dict(z0=1.08, z1=1.16, x0=0, x1=-20)), bars="scope")
b("تبتسم مريم والدموع", fc("MARYAM", "seacafe", "joy", side=0.3, rimSide=1, tear=0.4, talkp="انت لا تتذكرني لكنك تجدني دائما"), bars="scope")
b("وفي تلك الليله تكتب", ins("notes", notes=["لا تخف", "أنت لست وحدك"]), in_=DIP)
b("فالذاكره ليست في الراس وحده فما", fc("KARIM", "bedroom", "smile", side=0.0, labels=[L("الذاكرة ليست في الرأس وحده", y=0.22, at=0.2)]))
b("الحقيقي في هذه القصه", bl("ما الحقيقي في هذه القصة؟", "archive"), in_=DIP, cap=False, music_cut="calm")
b("فقدان القدره على صنع", da(value="حالة حقيقية", label="فقدان القدرة على صنع ذكريات جديدة", size=110))
b("اشهر مثال عليها رجل", da(value="هنري موليسون", label="جراحة في الدماغ عام 1953", size=110))
b("ومع ذلك تعلم مهاره رسم", ins("star", messy=False, timeLabel="يتحسن كل يوم"))
b("والعازف البريطاني كلايف", da(value="كلايف ويرينغ", label="فقد ذاكرته عام 1985", size=110))
b("لكنه ظل يعزف", ins("piano"))
b("اما ان تمحى الذاكره بالضبط", da(value="خيال", label="المحو لحظة النوم", size=150, color="coral"))
b("لكن دور النوم في تثبيت", da(icon="brain", value="النوم", label="يثبّت الذكريات… والبحث مستمر", size=110, count=3))
b("وفي الحلقه القادمه", bl("ماذا لو كان ذكاؤك أعلى بعشرة أضعاف؟", "archive", str2="الحلقة القادمة", at2=0.8), cap=False, sfx=[SFX("riser", 0, -12)])
b("ما رايك اخبرنا", dict(tpl="endscreen", q="ما رأيك؟ أخبرنا في التعليقات", cast=["YOUNES", "MARYAM", "KARIM", "SAMER", "MOM", "DOC"]), in_=FADE, cap=False)

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
    if d > 6.0 and tpl in ("stage", "insert", "archive", "data"):
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
story = {"title": "ماذا لو كان كل يوم يُمحى من ذاكرتك لحظة تنام؟", "duration": DUR, "shots": shots, "music": music, "sfx": []}
json.dump(story, open(f"{PROJ}/story/shots.json", "w"), ensure_ascii=False, indent=1)
d = [s["end"] - s["start"] for s in shots]; d.sort()
print(len(shots), "shots; median", round(d[len(d) // 2], 2), "min", round(d[0], 2), "max", round(d[-1], 2))
print("music:", [(m["mood"], round(m["start"]), round(m["end"])) for m in music])
