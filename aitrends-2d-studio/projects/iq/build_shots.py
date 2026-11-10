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
Y = lambda x, pose="stand", expr="neutral", f=1, **kw: C("SALIM", x, pose, expr, f, **kw)

b("الفطور لم يبدا بعد", st("home", [Y(0.4, "sit", "smirk", chair=True), C("MOM", 0.65, "stand", "neutral", -1)], props=[dict(k="table", x=0.52, plate=True)], cam=PUSH), amb={"name": "roomtone", "gain": -26})
b("وانت حللت مكعب روبيك", ins("cube"), sfx=[SFX("swish", 0.4, -10), SFX("ding", 1.6, -10)])
b("امك تسالك عن واجب", st("home", [C("MOM", 0.62, "talk", "neutral", -1), Y(0.38, "explain", "smirk")], cam=PUSH, labels=[L("انتهيت منه أمس", y=0.18, ap="انتهيت", box=True)]))
b("المذيع في التلفاز يخطئ", st("home", [Y(0.35, "point", "determined"), C("DAD", 0.55, "sitBack", "sad", 1, chair=True)], props=[dict(k="tv", x=0.82)], cam=PUSH))
b("تنظر من النافذه تحسب", st("city", [Y(0.5, "think", "thinking", s=1.2)], so=dict(mood="day"), cam=DRIFT, labels=[L("62 كم/س", x=0.25, y=0.3, at=0.5, cream=True), L("48 كم/س", x=0.75, y=0.35, at=1.0, cream=True)]))
b("ثم تدخل اختك الصغيره نور", st("home", [C("NOUR", 0.6, "crossArms", "angry", -1, s=1.7), Y(0.38, "stand", "confused", s=1.7)], cam=PUSH), sfx=[SFX("hit", 1.5, -10)])
b("وانت اذكى انسان في المدينه", fc("SALIM", "home", "confused", side=0.0))
b("معظم الناس تقع درجاتهم", ins("iqcurve"), in_=DIP, sfx=[POP(0.3)])
b("وانت عقلك اسرع من", da(icon="brain", value="10×", label="أسرع من الجميع", size=170, count=2), sfx=[SFX("shimmer", 0.2, -10)])
b("تقرا الكتاب في ساعه", st("home", [Y(0.45, "holdFront", "smirk", prop="paper", s=1.6)], cam=PUSH, labels=[L("ساعة واحدة", y=0.18, ap="ساعه", box=True)]))
b("لكن لهذه القوه قاعده", bl("قاعدة واحدة", "home", str2="الذكاء يسرّع التفكير… ولا يسرّع المشاعر", at2=2.0), cap=False, sfx=[SFX("stinger", 0.1, -10)])
b("الحزن يحتاج وقته", ar(hero=True, heroC="SALIM", expr="thinking", labels=[L("الحزن يحتاج وقته", x=0.3, y=0.25, ap="الحزن"), L("الفرح يحتاج وقته", x=0.7, y=0.25, ap="والفرح")]))
b("اسمك سليم", st("home", [Y(0.5, "relaxed", "smile", s=1.8)], cam=PUSH, labels=[L("سليم", y=0.2, ap="سليم", size=90), L("14 عاما", y=0.32, ap="عمرك", cream=True)]))
b("وستتعلم يوما ان اذكى", fc("SALIM", "home", "neutral", side=0.0, labels=[L("أذكى إجابة… أحيانا أن تصمت", y=0.2, ap="اذكى")]))
b("فماذا لو كان ذكاؤك", dict(tpl="title", lines=["ماذا لو", "كان ذكاؤك أعلى بعشرة أضعاف؟"]), in_=FADE, bars="scope", cap=False, sfx=[SFX("riser", 0, -12)])
b("تبدا بالمدرسه امتحان", st("classroom", [Y(0.6, "holdFront", "smirk", f=-1, prop="paper"), C("TEACHER", 0.3, "stand", "neutral", 1)], cam=PUSH), in_=DIP, amb={"name": "roomtone", "gain": -26})
b("تسلم الورقه بعد سبع", ins("exam"), sfx=[SFX("tick", 0.3, -16)])
b("هو لم يحله حتى الان", fc("TEACHER", "classroom", "confused", side=-0.2))
b("في الشهر الثالث تنتقل", st("classroom", [Y(0.5, "stand", "smile", s=1.2), C("PLAIN", 0.3, "stand", "surprised", 1, s=1.4), C("PLAIN", 0.72, "stand", "surprised", -1, s=1.4)], cam=PUSH, labels=[L("أصغر طالب جامعي", y=0.18, ap="اصغر", box=True)]))
b("ياخذك ابوك الى مركز", st("clinic", [C("DOC", 0.62, "think", "shocked", -1), Y(0.38, "sit", "neutral", chair=True)], cam=PUSH))
b("الرقم خارج المقياس", da(value="خارج المقياس", label="الجهاز ليس معطلا", size=130, color="coral"))
b("ثم تدعوك بطوله الشطرنج", st("studio", [Y(0.5, "stand", "determined")], crowd=0.3, cam=PUSH), amb={"name": "murmur", "gain": -26})
b("تلعب عشرين مباراه", ins("chess"))
b("تتعلم لغه جديده كل شهر", da(value="6 لغات", label="ولا أحد تكلمه", size=150))
b("ثم تقرا عن قرى بعيده", st("city", [C("PLAIN", 0.4, "sad", "sad", 1, s=1.2), C("PLAIN", 0.6, "sad", "sad", -1, s=1.2)], so=dict(mood="golden"), cam=DRIFT))
b("في عطله نهايه الاسبوع", ins("filter"), sfx=[POP(0.2), POP(0.6), POP(1.0)])
b("بعد شهر تستعمله عشرات", st("city", [C("PLAIN", 0.35, "cheer", "joy", 1, s=1.2), C("PLAIN", 0.55, "cheer", "joy", 1, s=1.2), C("PLAIN", 0.75, "cheer", "joy", -1, s=1.2)], so=dict(mood="golden"), cam=PULL), sfx=[SFX("cheer", 0.2, -18)])
b("الصحف تكتب عنك", bl("العبقري الصغير", "city"), cap=False, sfx=[SFX("impact", 0.2, -10)])
b("والعلماء يرسلون لك", st("home", [Y(0.45, "holdFront", "smirk", prop="phone")], props=[dict(k="table", x=0.6, cups=[[0, False]])], cam=PUSH))
b("لكن شيئا اخر يحدث", st("city", [Y(0.4, "stand", "neutral"), C("HADI", 0.6, "explain", "happy", -1)], so=dict(mood="dusk"), cam=PUSH), music_cut="sad", in_=DIP)
b("وانت تعرف نهايتها من", fc("SALIM", "city", "smirk", side=-0.2))
b("ثم يتوقف عن الحكايه", fc("HADI", "city", "sad", side=0.3, rimSide=1))
b("وحين يحكي الناس نكته", st("classroom", [Y(0.5, "think", "thinking"), C("PLAIN", 0.3, "cheer", "joy", 1, s=1.2), C("PLAIN", 0.7, "cheer", "joy", -1, s=1.2)], cam=PUSH))
b("في الفصل لم يعد احد", st("classroom", [Y(0.5, "sit", "sad", chair=True)], cam=PULL))
b("وفي حفله عيد ميلاد", st("home", [Y(0.15, "stand", "thinking", s=1.3), C("HADI", 0.55, "cheer", "joy", 1, s=1.3), C("PLAIN", 0.7, "cheer", "joy", -1, s=1.3), C("PLAIN", 0.85, "cheer", "joy", -1, s=1.3)], so=dict(night=True, sky="night"), cam=DRIFT), amb={"name": "murmur", "gain": -26})
b("وهناك ثمن اخر دماغ", da(icon="brain", value="20%", label="من طاقة الجسم", size=150, count=2))
b("ودماغك لا يتوقف تاكل", st("bedroom", [Y(0.45, "sit", "sleepy", chair=True)], cam=PUSH, clock=[2, 0]))
b("وحين تسالك امك كيف", st("home", [C("MOM", 0.62, "stand", "sad", -1), Y(0.38, "explain", "neutral", prop="paper")], cam=PUSH, labels=[L("تقرير من 3 صفحات", y=0.18, ap="تقريرا", box=True)]))
b("صرت تعرف كل شيء", bl("تعرف كل شيء… إلا كيف تكون قريبا", "home", coral=True), cap=False)
b("في البيت اختك نور", st("home", [C("NOUR", 0.58, "cheer", "happy", -1), Y(0.42, "stand", "smile")], cam=PUSH, labels=[L("نور 7 سنوات", x=0.58, y=0.2, ap="نور", box=True)]), music_cut="hopeful", in_=FADE)
b("تعلمك لعبه سخيفه", st("home", [C("NOUR", 0.6, "cheer", "joy", -1, s=1.7), Y(0.4, "shrug", "confused", s=1.7)], cam=PUSH))
b("كل مساء ترسم لك", ins("drawings", n=1))
b("وكل مساء تسالك السؤال", fc("NOUR", "home", "smile", side=0.3, rimSide=1, talkp="هل انت سعيد"))
b("وانت تجيبها بدقه", st("home", [Y(0.4, "explain", "thinking", s=1.7), C("NOUR", 0.6, "stand", "neutral", -1, s=1.7)], cam=PUSH))
b("فتنظر اليك طويلا", fc("NOUR", "home", "sad", side=0.3, rimSide=1))
b("عندك الان مئه وعشرون", ins("drawings", n=12, labels=[L("120 رسمة", y=0.08, ap="مئه", box=True)]))
b("ثم ياتي ذلك الصباح", ins("fishbowl", dead=True), in_=DIP, music_cut="tension")
b("نور تبكي وانت تعرف", fc("NOUR", "home", "cry", side=0.3, rimSide=1, tear=0.3))
b("هذا النوع من السمك", st("home", [Y(0.4, "explain", "neutral", s=1.7), C("NOUR", 0.6, "sad", "cry", -1, s=1.7)], cam=PUSH, labels=[L("2 إلى 3 سنوات", y=0.18, ap="عامين", box=True)]))
b("تنظر اليك نور ثم تبكي", st("home", [C("NOUR", 0.6, walk=[0.6, 0.95], run=True), Y(0.4, "stand", "shocked")], cam=PUSH), sfx=[SFX("hit", 2.0, -8)])
b("تقف وحدك في الممر", st("home", [Y(0.5, "stand", "worried", still=True, s=1.2)], cam=PULL))
b("مئه حل في ثانيه", ar(hero=True, heroC="SALIM", pose="handsOnHead", expr="worried", n=70, speed=3, cards=["سمكة جديدة", "كتاب عن الأسماك", "خطة من 10 خطوات"], cardsX=[0.2, 0.5, 0.8], cardsY=[0.25, 0.18, 0.25], gap=0.6))
b("وتتذكر ان هاديا اتصل", fc("SALIM", "home", "sad", side=0.0))
b("لان القاعده لا ترحم", bl("الحزن لا يُحلّ… الحزن يُرافَق", "home"), cap=False)
b("وهنا تفهم امامك طريقان", bl("أمامك طريقان", "home"), cap=False)
b("اما ان تطرق الباب", ar(hero=True, heroC="SALIM", pose="think", expr="thinking", n=40))
b("ان تجلس وتصمت", fc("SALIM", "home", "determined", side=0.0), in_=FLASH, sfx=[SFX("shimmer", 0, -10)])
b("تجلس على الارض امام", st("home", [Y(0.45, "sit", "sad", still=True, y=0.86)], cam=PUSH, bars="scope"))
b("تسمع بكاءها يخف", fc("SALIM", "home", "neutral", side=0.0))
b("ثم تاخذ ورقه وقلما", ins("drawings", n=1, fish=True), sfx=[SFX("shimmer", 1.0, -14)])
b("تدخلها من تحت الباب", st("home", [Y(0.45, "sit", "neutral", still=True, y=0.86)], cam=PUSH))
b("ثم يفتح الباب نور تجلس", st("home", [Y(0.45, "sit", "smile", still=True, y=0.86, s=1.8), C("NOUR", 0.55, "sit", "sad", -1, y=0.86, s=1.8)], cam=dict(z0=1.1, z1=1.18, x0=0, x1=-20)), music_cut="hopeful", bars="scope")
b("وبعد قليل تسالك بصوت", fc("NOUR", "home", "smile", side=0.3, rimSide=1, tear=0.2, talkp="هل انت سعيد"))
b("ولاول مره لا تحسب", fc("SALIM", "home", "smile", side=0.0, labels=[L("نعم", y=0.2, ap="نعم", size=110)]), bars="scope")
b("وفي المساء تتصل بهادي", st("city", [Y(0.4, "relaxed", "smile"), C("HADI", 0.6, "talk", "happy", -1)], so=dict(mood="night"), cam=PUSH))
b("وتضع رسمه نور الجديده", ins("drawings", n=1, fish=True))
b("ذكاؤك ما زال اعلى", fc("SALIM", "bedroom", "smile", side=0.0, labels=[L("أذكى إجابة… أحيانا أن تصمت", y=0.2, ap="اذكى")]))
b("فما الحقيقي في هذه القصه", bl("ما الحقيقي في هذه القصة؟", "archive"), in_=DIP, cap=False, music_cut="calm")
b("اختبارات الذكاء تقارنك", ins("iqcurve"))
b("لذلك فذكاء اعلى", da(value="1000 IQ؟", label="لا يمكن قياسه أصلا", size=140, color="coral"))
b("والدماغ يستهلك فعلا", da(icon="brain", value="20%", label="من طاقة الجسم", size=150, count=2))
b("ومن الحقائق الغريبه ان", da(value="+3 نقاط", label="كل 10 سنوات: أثر فلين", size=140))
b("ويختلف العلماء في سببه", da(value="تعليم؟ تغذية؟", label="السبب ما زال محل خلاف", size=110))
b("وفي عام 1921 بدا", da(value="1921", label="دراسة ترمان: أكثر من 1500 طفل", size=150))
b("ومن المفارقات ان طفلين", da(value="نوبل", label="لطفلين لم يُختارا للدراسة", size=150))
b("اما الذكاء العاطفي", da(value="الذكاء العاطفي", label="1990… وانتشر عام 1995", size=110))
b("يراه بعض العلماء قدره", da(value="النقاش مستمر", label="قدرة مستقلة؟ أم سمات شخصية؟", size=110))
b("وفي الحلقه القادمه", bl("ماذا لو لم تشعر بالألم أبدا؟", "archive", str2="الحلقة القادمة", at2=0.8), cap=False, sfx=[SFX("riser", 0, -12)])
b("ما رايك اخبرنا", dict(tpl="endscreen", q="ما رأيك؟ أخبرنا في التعليقات", cast=["NOUR", "SALIM", "HADI", "MOM", "DAD", "TEACHER"]), in_=FADE, cap=False)

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
story = {"title": "ماذا لو كان ذكاؤك أعلى بعشرة أضعاف؟", "duration": DUR, "shots": shots, "music": music, "sfx": []}
json.dump(story, open(f"{PROJ}/story/shots.json", "w"), ensure_ascii=False, indent=1)
d = [s["end"] - s["start"] for s in shots]; d.sort()
print(len(shots), "shots; median", round(d[len(d) // 2], 2), "min", round(d[0], 2), "max", round(d[-1], 2))
print("music:", [(m["mood"], round(m["start"]), round(m["end"])) for m in music])
