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
F = lambda x, pose="stand", expr="neutral", f=1, **kw: C("FARIS", x, pose, expr, f, **kw)
R = lambda x, pose="stand", expr="neutral", f=-1, **kw: C("RAMI", x, pose, expr, f, **kw)
NIGHT = dict(night=True, sky="night")

b("جرحت يدك بسكين المطبخ", ins("palm", cut=True), sfx=[SFX("swish", 0.1, -10), SFX("shimmer", 1.8, -12)], amb={"name": "roomtone", "gain": -28})
b("لا ندبه لا اثر", st("home", [C("MOM", 0.62, "handsOnHead", "shocked", -1), F(0.4, "holdFront", "smirk")], cam=PUSH, labels=[L("لا ندبة", y=0.18, ap="ندبه", box=True)]))
b("تسقط عن دراجتك", st("city", [F(0.45, "fall", "surprised")], so=dict(mood="day"), cam=dict(z0=1.05, z1=1.12, shake=5)), sfx=[SFX("hit", 0.3, -8)])
b("وحين كسرت ذراعك", ins("bone"), sfx=[SFX("hit", 0.2, -10), SFX("ding", 2.4, -12)])
b("جسمك يشفى اسرع بمئه مره", da(value="×100", label="أسرع من أي إنسان", size=200), sfx=[SFX("shimmer", 0.2, -10)])
b("الا جرحا واحدا", ins("palm"), music_cut="tension")
b("لان لهذه القوه قاعده", bl("قاعدة واحدة", "home", str2="جسدك يشفي كل جرح… إلا الذي تهرب منه", at2=1.6), cap=False, sfx=[SFX("stinger", 0.1, -10)])
b("اسمك فارس", st("city", [F(0.5, "relaxed", "smile", s=1.8)], so=dict(mood="day"), cam=PUSH, labels=[L("فارس", y=0.2, ap="فارس", size=90), L("18 عاما", y=0.32, ap="ثمانيه", cream=True)]))
b("وستتعلم يوما ان الشفاء", fc("FARIS", "city", "thinking", side=0.0, labels=[L("الشفاء السريع… ليس هو الشفاء", y=0.18, ap="الشفاء")]))
b("فماذا لو التامت جروحك", dict(tpl="title", lines=["ماذا لو", "التأمت جروحك أسرع بمئة مرة؟"]), in_=FADE, bars="scope", cap=False, sfx=[SFX("riser", 0, -12)])
b("في البدايه يبدو الامر لعبه", st("city", [F(0.3, "jump", "joy", s=1.3)], so=dict(mood="golden"), cam=DRIFT), in_=DIP)
b("مقاطعك على الانترنت", ins("views"), sfx=[POP(0.3), POP(0.8)])
b("والناس يسمونك", bl("الفتى الذي لا يُكسر", "city"), cap=False, sfx=[SFX("impact", 0.2, -10)])
b("اصدقاؤك الجدد يتحدونك", st("seacafe", [F(0.5, "dive", "joy", y=0.55), C("PLAIN", 0.2, "cheer", "joy", 1, s=1.2), C("PLAIN", 0.8, "phone", "joy", -1, s=1.2)], so=dict(outside=True), cam=DRIFT), sfx=[SFX("whoosh", 1.2, -12)])
b("وترتطم بالماء بقوه", fc("FARIS", "seacafe", "shocked", side=0.0, tilt=0.06), sfx=[SFX("impact", 0.1, -8)])
b("وقبل ان تصل الى الشاطئ", st("seacafe", [F(0.5, "cheer", "joy"), C("PLAIN", 0.3, "phone", "joy", 1), C("PLAIN", 0.7, "cheer", "joy", -1)], so=dict(outside=True), cam=PULL), sfx=[SFX("cheer", 0.2, -18)])
b("الاطباء يدرسون صور الاشعه", st("clinic", [C("DOC", 0.6, "point", "shocked", -1), F(0.38, "sit", "smirk", chair=True)], cam=PUSH, labels=[L("أسابيع… في ليلة واحدة", y=0.18, ap="الكسر", box=True)]))
b("وفي ليله شتويه تشتعل", ins("fire"), music_cut="tension", sfx=[SFX("whoosh", 0.1, -10)])
b("تدخل قبل ان يصل", fc("FARIS", "home", "determined", side=0.0), in_=FLASH)
b("وتخرج والطفل بين يديك", st("city", [F(0.45, "holdFront", "determined", s=1.4), C("FIRE", 0.75, "point", "surprised", -1)], so=dict(mood="night"), cam=PUSH), sfx=[SFX("cheer", 0.6, -18)])
b("ام الطفل تبكي", st("city", [C("PLAIN", 0.6, "reach", "cry", -1, s=1.6), F(0.4, "stand", "smile", s=1.6)], so=dict(mood="night"), cam=PUSH))
b("لان الخط الاحمر بدا", ins("palm"))
b("يفحصه الاطباء ولا يفهمون", st("clinic", [C("DOC", 0.6, "shrug", "confused", -1), F(0.38, "sit", "worried", chair=True)], cam=PUSH, labels=[L("خُيّط مرتين… وانفتح", y=0.18, ap="خيطوه", box=True, coral=True)]))
b("لكنك تعرف من اين جاء", fc("FARIS", "bedroom", "sad", side=0.0), music_cut="sad")
b("قبل سنتين كان رامي", ar(hero=True, heroC="RAMIKID", expr="joy", hs=1.2, labels=[L("رامي", y=0.2, ap="رامي", box=True)]))
b("بنيتما كوخا خشبيا", ins("treehouse"), sfx=[SFX("shimmer", 0.3, -14)])
b("وفي ذلك اليوم تحديته", st("city", [C("FARISKID", 0.4, "point", "smirk", 1), C("RAMIKID", 0.6, "stand", "worried", -1)], so=dict(mood="golden"), cam=PUSH, labels=[L("بلا مكابح", y=0.18, ap="مكابح", box=True, coral=True)]))
b("فضحكت وقلت جبان", fc("FARIS", "city", "smirk", side=0.0, labels=[L("جبان", y=0.18, ap="جبان", size=100, coral=True)]))
b("نزل رامي", ins("hill"), sfx=[SFX("whoosh", 1.6, -10), SFX("hit", 2.1, -6)])
b("ومددت يدك لتمسكه", ins("palm", cut=False), in_=FLASH)
b("كسرت ساق رامي", da(value="3 كسور", label="وما زال يعرج", size=170, color="coral"))
b("وانت لم تزره في المستشفى", fc("FARIS", "bedroom", "sad", side=0.0))
b("فصرت تغير طريقك", st("city", [F(0.3, walk=[0.45, 0.1]), R(0.8, "stand", "sad")], so=dict(mood="day"), cam=DRIFT))
b("وفي المدرسه تراه يصعد", st("classroom", [R(0.5, "stand", "sad", s=1.3), C("PLAIN", 0.25, "cheer", "smirk", 1, s=1.2), C("PLAIN", 0.75, "point", "smirk", -1, s=1.2)], cam=PUSH))
b("وانت تقف بينهم", fc("FARIS", "classroom", "sad", side=0.0))
b("وتلك الليله تستيقظ", st("bedroom", [F(0.45, "sit", "shocked", chair=True, s=1.5)], cam=PUSH, labels=[L("دم على الوسادة", y=0.18, ap="والدم", box=True, coral=True)]))
b("ومع الوقت صارت قوتك تغيرك", st("city", [F(0.5, "jump", "smirk", s=1.3)], so=dict(mood="dusk"), cam=DRIFT))
b("امك تراك تقفز", st("home", [C("MOM", 0.58, "handsOnHead", "worried", -1), F(0.4, "stand", "smirk")], cam=PUSH))
b("وتقول لك ليله جسمك يشفى", fc("MOM", "home", "sad", side=0.3, rimSide=1, talkp="لكن قلبي انا لا يشفى", labels=[L("قلبي أنا لا يشفى", y=0.18, ap="لكن", box=True)]))
b("واصدقاؤك الجدد يحبون", st("city", [C("PLAIN", 0.3, "phone", "joy", 1), C("PLAIN", 0.5, "phone", "joy", 1), F(0.75, "stand", "sad", -1)], so=dict(mood="night"), cam=PUSH, labels=[L("رباط أسود", x=0.75, y=0.3, ap="برباط", box=True)]))
b("ثم ياتي ذلك المساء", ins("chat", msgs=["أنا والد رامي", "عملية غدا", "يحتاج متبرعا بالدم", "فصيلته نادرة"]), music_cut="tension", in_=DIP)
b("فصيله دم رامي", da(value="نفس الفصيلة", label="إخوة بالدم", size=130))
b("تقضي الليل والهاتف", ins("chat", msgs=["رامي… أنا آسف", "⌫", "رامي أنا", "⌫"]))
b("وتنام قرب الفجر", st("bedroom", [F(0.45, "sitBack", "sad", chair=True, s=1.5)], cam=PULL, clock=[5, 0]))
b("في الصباح تذهب الى المستشفى", st("clinic", [F(0.42, "sitBack", "neutral", chair=True), C("NURSE", 0.64, "holdFront", "neutral", -1)], cam=PUSH))
b("الابره في ذراعك", ins("bloodbag"))
b("وتقول للممرضه", fc("FARIS", "clinic", "sad", side=0.0, labels=[L("لا تذكري اسمي", y=0.18, ap="لا", box=True)]))
b("ثم تقف امام باب غرفته", st("clinic", [F(0.25, "stand", "worried"), R(0.68, "sitBack", "sad", chair=True)], cam=PUSH))
b("والجرح في يدك ينزف", ins("palm"))
b("وهنا تفهم امامك طريقان", bl("أمامك طريقان", "clinic"), cap=False)
b("اما ان تمشي بعيدا", ar(hero=True, heroC="FARIS", pose="think", expr="thinking", n=50, cards=["تمشي بعيدا", "تدخل"], cardsX=[0.25, 0.75], gap=1.2))
b("تطرق الباب", st("clinic", [F(0.35, "stand", "worried", s=1.6), R(0.62, "sitBack", "surprised", chair=True, s=1.6)], cam=PUSH), sfx=[SFX("hit", 0.2, -14), SFX("hit", 0.5, -14)])
b("ثم تقول الكلمه التي تاخرت", fc("FARIS", "clinic", "sad", side=0.0, talkp="اسف يا رامي", labels=[L("آسف يا رامي", y=0.18, ap="اسف", size=90)]), music_cut="calm")
b("ينظر رامي الى يدك", fc("RAMI", "clinic", "sad", side=0.3, rimSide=1, talkp="لم اكن غاضبا من السقوط يا فارس"))
b("كنت احتاج صديقي", fc("RAMI", "clinic", "smile", side=0.3, rimSide=1, tear=0.3, labels=[L("كنت أحتاج صديقي… أكثر من ساقي", y=0.18, ap="كنت", box=True)]))
b("ثم يمد يده", st("clinic", [F(0.45, "reach", "smile", s=1.8), R(0.58, "reach", "smile", chair=True, pose="sitBack") if False else R(0.58, "reach", "smile", s=1.8)], cam=dict(z0=1.1, z1=1.2, x0=0, x1=-20)), music_cut="hopeful")
b("تفك الرباط بعد ان تخرج", ins("palm", healed=False))
b("وبعد العمليه يعرف والد رامي", st("clinic", [C("DAD", 0.55, "reach", "cry", -1, s=1.6), F(0.42, "stand", "sad", s=1.6)], cam=PUSH))
b("وتشعر لاول مره منذ سنتين", fc("FARIS", "clinic", "smile", side=0.0))
b("وفي الايام التاليه يلتئم", ins("palm", healed=True))
b("بعد شهر يخرج رامي", st("city", [F(0.4, walk=[0.2, 0.55]), R(0.5, walk=[0.3, 0.65])], so=dict(mood="golden"), cam=DRIFT))
b("وتجلسان على القمه", st("city", [F(0.45, "sit", "joy", y=0.82, s=1.4), R(0.58, "sit", "joy", y=0.82, s=1.4)], so=dict(mood="golden"), cam=PULL))
b("لم يبق من الجرح الا ندبه", ins("palm", healed=True))
b("لانك تعلمت اخيرا ان بعض", fc("FARIS", "city", "smile", side=0.0, labels=[L("بعض الجروح تُشفى بالشجاعة", y=0.18, ap="بعض")]))
b("فما الحقيقي في هذه القصه", bl("ما الحقيقي في هذه القصة؟", "archive"), in_=DIP, cap=False, music_cut="calm")
b("يمر شفاء الجروح", ins("phases"))
b("والندبه ليست جلدا عاديا", da(value="80%", label="أقصى قوة للندبة مقارنة بالجلد", size=180))
b("والكسر العادي يحتاج غالبا", da(value="6–8 أسابيع", label="لالتئام كسر عادي", size=140))
b("لكن في الطبيعه ابطالا", ins("axolotl"))
b("وفي عام الف وتسعمئه وثمانيه", da(value="1998", label="فئران تشفى بلا ندبة", size=160))
b("وحتى الانسان يملك", da(value="الكبد", label="ينمو من جديد بعد استئصال أكثر من نصفه", size=150))
b("واطراف اصابع الاطفال", da(value="أطراف الأصابع", label="عند الأطفال الصغار… أحيانا", size=120))
b("اما الجلد في الاشهر الاولى", da(value="بلا ندبة", label="جلد الجنين في الأشهر الأولى", size=150))
b("وهناك رابط حقيقي بين القلب", da(icon="brain", value="القلب والجسد", label="رابط حقيقي", size=110, count=2))
b("في عام الف وتسعمئه وخمسه", da(value="+24%", label="وقت أطول للشفاء مع الضغط النفسي (1995)", size=170, color="coral"))
b("وفي عام الفين وثلاثه اظهرت", da(icon="brain", value="ألم الرفض", label="ينشط مناطق من الألم الجسدي (2003)", size=110, count=2))
b("لكن العلماء ما زالوا يختلفون", da(value="محل خلاف", label="هل يؤلم القلب المكسور كالعظم؟", size=130))
b("فالجسد يشفى بالوقت", bl("الجسد يُشفى بالوقت… والقلب بكلمة", "archive"), cap=False)
b("وفي الحلقه القادمه", bl("ماذا لو كان بصرك أحد بمئة مرة؟", "archive", str2="الحلقة القادمة", at2=0.8), cap=False, sfx=[SFX("riser", 0, -12)])
b("ما رايك اخبرنا", dict(tpl="endscreen", q="هل هناك اعتذار تأخرت فيه؟", cast=["MOM", "FARIS", "RAMI", "DAD", "NURSE", "DOC"]), in_=FADE, cap=False)

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
story = {"title": "ماذا لو التأمت جروحك أسرع بمئة مرة؟", "duration": DUR, "shots": shots, "music": music, "sfx": []}
json.dump(story, open(f"{PROJ}/story/shots.json", "w"), ensure_ascii=False, indent=1)
d = [s["end"] - s["start"] for s in shots]; d.sort()
print(len(shots), "shots; median", round(d[len(d) // 2], 2), "min", round(d[0], 2), "max", round(d[-1], 2))
print("music:", [(m["mood"], round(m["start"]), round(m["end"])) for m in music])
