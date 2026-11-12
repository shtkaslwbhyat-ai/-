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
O = lambda x, pose="stand", expr="neutral", f=1, **kw: C("OMAR", x, pose, expr, f, **kw)
G = lambda x, pose="sit", expr="smile", f=-1, **kw: C("YOUSEF", x, pose, expr, f, **kw)
NIGHT = dict(night=True, sky="night")

b("الساعه الثالثه فجرا", st("bedroom", [O(0.45, "sit", "sleepy", chair=True)], cam=PUSH, clock=[3, 0]), amb={"name": "roomtone", "gain": -28})
b("تسمع قلب جارك", ins("heart", mode="calm", label="خلف الجدار"), sfx=[SFX("heartbeat", 0.0, -10)])
b("تسمع نمله تمشي", fc("OMAR", "bedroom", "surprised", side=0.0, labels=[L("نملة على الزجاج", y=0.18, ap="نمله", box=True)]))
b("والثلاجه في المطبخ", st("home", [], so=NIGHT, cam=PULL, labels=[L("هدير قطار!", y=0.3, ap="قطار", size=90, coral=True)]), sfx=[SFX("hum", 0, -12)])
b("ثم تسمع امك", st("home", [C("SAWSAN", 0.55, "phone", "sad", -1)], so=NIGHT, cam=PUSH, labels=[L("الطابق الأرضي", y=0.18, ap="الطابق", box=True)]))
b("وانت تسمع كل كلمه", fc("OMAR", "bedroom", "worried", side=0.0))
b("في الصباح تعرف ان الحافله", dict(tpl="places", pins=[["البيت", 0.25, 0.65], ["الحافلة عالقة", 0.78, 0.32, 1.4]], home=0))
b("سمعك اقوى من سمع", da(value="×1,000,000", label="أقوى من سمع أي إنسان", size=150), sfx=[SFX("shimmer", 0.2, -10)])
b("تسمع كل سر في المدينه", ins("waves", src=["كل سر", "كل همسة", "كل كذبة"]))
b("الا شيئا واحدا", fc("OMAR", "city", "confused", side=0.0, labels=[L("إلا الصوت الذي يكلمك", y=0.18, ap="الصوت")]))
b("لان لهذه القوه قاعده", bl("قاعدة واحدة", "home", str2="الأذن تسمع… والدماغ ينصت", at2=1.6), cap=False, sfx=[SFX("stinger", 0.1, -10)])
b("وحين يصل اليه كل صوت", ins("bubbles", n=44))
b("اسمك عمر", st("city", [O(0.5, "relaxed", "smile", s=1.8)], so=dict(mood="day"), cam=PUSH, labels=[L("عمر", y=0.2, ap="عمر", size=90), L("17 عاما", y=0.32, ap="سبعه", cream=True)]))
b("وستتعلم يوما ان اصعب", fc("OMAR", "city", "thinking", side=0.0, labels=[L("أن تختار ما تسمعه", y=0.18, ap="تختار")]))
b("فماذا لو كان سمعك", dict(tpl="title", lines=["ماذا لو", "كان سمعك أقوى بمليون مرة؟"]), in_=FADE, bars="scope", cap=False, sfx=[SFX("riser", 0, -12)])
b("في البدايه تبدو الحياه", st("studio", [O(0.5, "sit", "smile", chair=True, s=1.3)], crowd=0.2, cam=PUSH), in_=DIP, amb={"name": "murmur", "gain": -26})
b("تعرف ان عازف الكمان", fc("OMAR", "studio", "smirk", side=0.0, labels=[L("الكمان الثالث متوتر", y=0.18, ap="الكمان", box=True)]))
b("وتعرف ان سياره ابيك", st("city", [C("DAD", 0.6, "shrug", "confused", -1), O(0.4, "point", "determined")], props=[dict(k="taxi", x=0.75)], so=dict(mood="day"), cam=PUSH, labels=[L("بعد أسبوع", y=0.18, ap="اسبوع", box=True)]))
b("لا يسمعه الميكانيكي", fc("DAD", "city", "surprised", side=0.2, rimSide=1))
b("وفي الصف لا يستطيع", st("classroom", [O(0.38, "crossArms", "smirk"), C("PLAIN", 0.62, "explain", "nervous", -1)], cam=PUSH))
b("حين يكذب زميلك", ins("heart", mode="fast", label="يكذب…"), sfx=[SFX("heartbeat", 0, -10)])
b("وخلف الحي تسمع", ins("cat"), music_cut="hopeful")
b("تحفر بيديك ساعه", st("city", [O(0.45, "kneel", "determined")], so=dict(mood="golden"), cam=PUSH))
b("تسميها همسه", ins("cat", out=True), sfx=[SFX("shimmer", 0.2, -12)])
b("لكن الليله التي غيرت", st("city", [O(0.45, "stand", "shocked")], so=dict(mood="night"), cam=PUSH), music_cut="tension", in_=DIP)
b("فحيح رفيع", ins("gas"), sfx=[SFX("wind", 0, -14)])
b("الجميع نائمون", ins("building", hiss=True))
b("تطرق الابواب", st("home", [O(0.5, "point", "shocked", s=1.4)], so=NIGHT, cam=dict(z0=1.05, z1=1.12, shake=4)), sfx=[SFX("hit", 0.2, -10), SFX("hit", 0.6, -10), SFX("hit", 1.0, -10)])
b("وينزل السكان الى الشارع", st("city", [C("PLAIN", 0.25, "crossArms", "angry", 1, s=1.2), C("PLAIN", 0.4, "crossArms", "angry", 1, s=1.2), O(0.6, "explain", "worried", -1, s=1.2), C("PLAIN", 0.78, "crossArms", "angry", -1, s=1.2)], so=dict(mood="night"), cam=PULL))
b("ثم يصل رجال الطوارئ", st("city", [C("MEDIC", 0.4, "point", "determined", 1), C("MEDIC", 0.6, "stand", "surprised", -1)], so=dict(mood="night"), cam=PUSH), sfx=[SFX("whistle", 0.1, -16)])
b("في الصباح تكتب الصحف", ins("news"), music_cut="hopeful")
b("ويسميك اصدقاؤك", bl("الرادار", "city"), cap=False, sfx=[SFX("impact", 0.2, -10)])
b("لكن الرادار لا يعرف", fc("OMAR", "city", "worried", side=0.0), music_cut="sad")
b("المدينه عندك لا تنام", st("city", [O(0.5, "handsOnHead", "worried", s=1.3)], so=dict(mood="night"), cam=dict(z0=1.05, z1=1.12, x0=0, x1=-20, shake=3), labels=[L("بيب!", x=0.2, y=0.3, ap="ابواق", coral=True), L("ززززز", x=0.8, y=0.3, ap="اجهزه", coral=True)]), sfx=[SFX("carpass", 0.2, -12)])
b("شخير عماره كامله", ins("building", snore=True))
b("صرت تنام وعلى اذنيك", ins("headphones"))
b("وفي الامتحان تسمع", ins("exam", noTimer=True, labels=[L("30 قلما… في وقت واحد", y=0.12, ap="اقلام", box=True, coral=True)]), sfx=[SFX("tick", 0.2, -14)])
b("ودرجاتك تهبط", da(value="↓", label="الدرجات تهبط شهرا بعد شهر", size=200, color="coral"))
b("ياخذك ابوك الى طبيب", st("clinic", [C("DOC", 0.62, "think", "thinking", -1), O(0.4, "sit", "neutral", chair=True), C("DAD", 0.2, "stand", "worried", 1)], cam=PUSH))
b("المشكله ليست في ما تسمعه", fc("DOC", "clinic", "neutral", side=0.2, rimSide=1, labels=[L("دماغك لا يعرف ماذا يترك", y=0.18, ap="دماغك", box=True)]))
b("والاسرار ليست ممتعه", st("city", [C("PLAIN", 0.3, "cheer", "joy", 1, s=1.2), C("PLAIN", 0.48, "talk", "smirk", -1, s=1.2), O(0.85, "stand", "sad", -1, s=1.2)], so=dict(mood="dusk"), cam=PUSH))
b("وتسمع امك تبكي ليلا", st("home", [C("SAWSAN", 0.5, "sit", "cry", -1, chair=True)], props=[dict(k="table", x=0.6)], so=NIGHT, cam=PUSH, labels=[L("ديون", y=0.2, ap="ديون", box=True, coral=True)]))
b("صرت تعرف كل شيء عن", fc("OMAR", "bedroom", "sad", side=0.0))
b("لكن اصعب ما في الامر", st("home", [O(0.4, "sit", "neutral", chair=True), G(0.62, chair=True)], cam=PUSH, labels=[L("جدك يوسف", x=0.62, y=0.2, ap="يوسف", box=True)]), music_cut="calm")
b("وكل مساء يجلس بجانبك", fc("YOUSEF", "home", "smile", side=0.3, rimSide=1, talkp="ليحكي لك حكايه"))
b("حكايات عن البحر", st("seacafe", [C("YOUSEF", 0.5, "explain", "happy", 1, s=1.4)], so=dict(outside=True), cam=DRIFT))
b("يضيع بين دقات ساعه", ins("bubbles", n=34))
b("فتقول له ماذا يا جدي", fc("OMAR", "home", "confused", side=0.0, labels=[L("ماذا؟", y=0.18, ap="ماذا", size=100)]))
b("فيبتسم ويسكت", fc("YOUSEF", "home", "sad", side=0.3, rimSide=1))
b("والغريب ان جدك نفسه", st("home", [G(0.5, "stand", "smile", 1, s=1.8)], cam=PUSH, labels=[L("سماعة طبية", y=0.18, ap="سماعه", box=True)]))
b("هو الذي يفهمك دائما", st("home", [O(0.42, "sit", "smile", chair=True, s=1.5), G(0.6, "sit", "smile", chair=True, s=1.5)], cam=PULL))
b("ثم ياتي ذلك المساء", st("home", [C("YOUSEF", 0.55, "kneel", "scared", -1), O(0.35, "stand", "shocked")], so=NIGHT, cam=PUSH), music_cut="tension", in_=DIP)
b("وانت تسمع قلبه", ins("heart", mode="stumble"), sfx=[SFX("heartbeat", 0, -8)])
b("سياره الاسعاف تصل", st("city", [C("MEDIC", 0.4, walk=[0.2, 0.6], run=True), C("MEDIC", 0.25, walk=[0.05, 0.45], run=True)], so=dict(mood="night"), cam=DRIFT))
b("وفي المستشفى يبدا الجحيم", ar(hero=True, heroC="OMAR", pose="handsOnHead", expr="scared", n=70, speed=3, cards=["أجهزة", "قلوب", "أبواب", "صراخ"], cardsX=[0.2, 0.8, 0.22, 0.78], cardsY=[0.22, 0.22, 0.45, 0.45], gap=0.7), sfx=[SFX("buzz", 0.3, -14), SFX("blip", 1.0, -12)])
b("تضع يديك على اذنيك", fc("OMAR", "clinic", "scared", side=0.0, tilt=0.06))
b("ثم يسمح لك بالدخول", st("clinic", [C("YOUSEF", 0.55, "sitBack", "sleepy", -1, chair=True), O(0.35, "stand", "worried")], cam=PUSH))
b("يحرك شفتيه", fc("YOUSEF", "clinic", "sleepy", side=0.3, rimSide=1, talkp="يهمس لك بشيء"))
b("الصوت الوحيد الذي تريده", bl("الصوت الوحيد الذي لا تسمعه", "clinic", coral=True), cap=False)
b("وهنا تفهم امامك طريقان", bl("أمامك طريقان", "clinic"), cap=False)
b("اما ان تحاول ان تسمع", ins("bubbles", n=44))
b("واما ان تفعل شيئا", ar(hero=True, heroC="OMAR", pose="think", expr="thinking", n=40))
b("تغمض عينيك", fc("OMAR", "clinic", "sleepy", side=0.0), in_=FLASH, sfx=[SFX("shimmer", 0, -10)], music_cut="calm")
b("القلب الذي كنت تنام عليه", st("home", [C("YOUSEF", 0.5, "sitBack", "smile", 1, chair=True, s=1.6), C("OMARKID", 0.56, "sit", "sleepy", -1, y=0.62, s=1.2)], so=NIGHT, cam=PUSH), bars="scope")
b("تجده دقه", ins("heart", mode="calm"), sfx=[SFX("heartbeat", 0, -8)])
b("وشيئا فشيئا يبتعد", ins("bubbles", n=44, pick=True, label="قلب جدك"))
b("لاول مره في حياتك يصير", fc("OMAR", "clinic", "awe", side=0.0), bars="scope", music_cut="hopeful")
b("وتسمعه يقول لك", fc("YOUSEF", "clinic", "smile", side=0.3, rimSide=1, talkp="لا تحتاج ان تسمع كل شيء يا عمر", labels=[L("اسمع من تحب", y=0.18, ap="اسمع")]))
b("بعد اسبوع يعود جدك", st("home", [O(0.4, "sit", "smile", chair=True), G(0.62, "sit", "happy", -1, chair=True)], cam=PUSH))
b("تغمض عينيك وتختار صوته", fc("OMAR", "home", "smile", side=0.0))
b("وفي اليوم التالي تذهب", st("home", [O(0.4, "talk", "determined", tp="اعرف عن الديون"), C("SAWSAN", 0.6, "stand", "surprised", -1)], cam=PUSH, labels=[L("سنحلها معا", y=0.18, ap="وسنحلها", box=True)]))
b("وحين يضحك اصدقاؤك", st("city", [O(0.5, "relaxed", "smile", s=1.4)], so=dict(mood="golden"), cam=PULL))
b("وفي الليل تنام همسه", st("bedroom", [O(0.45, "sitBack", "smile", chair=True, s=1.6)], cam=PUSH, labels=[L("همسة", y=0.2, ap="همسه", box=True)]))
b("ما زلت تسمع اقوى", fc("OMAR", "bedroom", "smile", side=0.0, labels=[L("السمع شيء… والإنصات شيء آخر", y=0.18, ap="السمع")]))
b("فما الحقيقي في هذه القصه", bl("ما الحقيقي في هذه القصة؟", "archive"), in_=DIP, cap=False, music_cut="calm")
b("اذن الانسان تسمع الاصوات", da(value="20 – 20,000", label="هرتز: مدى سمع الإنسان", size=140))
b("ويقل الحد الاعلى", da(value="↓ مع العمر", label="يقل الحد الأعلى", size=130))
b("اما قوه الصوت فتقاس", da(value="+10 dB = ×10", label="مقياس الديسيبل", size=130))
b("لذلك فالصوت الاقوى بمليون", da(value="+60 dB", label="= أقوى بمليون مرة", size=170, color="coral"))
b("واذنك حساسه اصلا", ins("waves", src=["جزيئات الهواء؟"]))
b("وفي اهدا الغرف التي", ins("heart", mode="calm", label="أهدأ غرفة في العالم"))
b("اما اقوى سمع عرف", ins("moth"))
b("ويرجح العلماء ان ذلك", da(value="🦇", label="تسمع الخفافيش التي تصطادها", size=160))
b("ومعاناه عمر لها اصل", da(value="فرط السمع", label="أصوات عادية… مؤلمة", size=140))
b("اما قدره عمر الاخيره", da(value="تأثير حفلة الكوكتيل", label="يملكه كل إنسان", size=100))
b("في غرفه مزدحمه يتكلم", ins("bubbles", n=44, pick=True, label="صوت واحد"))
b("واذا نطق احد اسمك", ins("bubbles", n=44, pick=True, label="اسمك!"))
b("وما زال العلماء يدرسون", da(value="البحث مستمر", label="كيف يختار الدماغ؟", size=130))
b("فاذنك تسمع", bl("أذنك تسمع… ودماغك يختار", "archive"), cap=False)
b("وفي الحلقه القادمه", bl("ماذا لو احتجت إلى ساعة نوم واحدة فقط؟", "archive", str2="الحلقة القادمة", at2=0.8), cap=False, sfx=[SFX("riser", 0, -12)])
b("ما رايك اخبرنا", dict(tpl="endscreen", q="لو سمعت كل الأسرار… هل كنت ستخبرهم؟", cast=["SAWSAN", "OMAR", "YOUSEF", "DAD", "DOC", "MEDIC"]), in_=FADE, cap=False)

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
story = {"title": "ماذا لو كان سمعك أقوى بمليون مرة؟", "duration": DUR, "shots": shots, "music": music, "sfx": []}
json.dump(story, open(f"{PROJ}/story/shots.json", "w"), ensure_ascii=False, indent=1)
d = [s["end"] - s["start"] for s in shots]; d.sort()
print(len(shots), "shots; median", round(d[len(d) // 2], 2), "min", round(d[0], 2), "max", round(d[-1], 2))
print("music:", [(m["mood"], round(m["start"]), round(m["end"])) for m in music])
