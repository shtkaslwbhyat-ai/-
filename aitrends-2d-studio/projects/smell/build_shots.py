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

b("ماذا لو كانت كل رائحه", dict(tpl="title", lines=["ماذا لو", "كانت كل رائحة أقوى بألف مرة؟"]), bars="scope", cap=False, sfx=[SFX("riser", 0, -12)])
b("تشم المطر قبل ان يسقط", st("city", [C("YOU", 0.5, "think", "awe", 1, s=1.3)], so=dict(mood="dusk"), rain=True, cam=PUSH))
b("تعرف ماذا طبخ جيرانك", ins("building"))
b("وتشم المرض في جسد", ins("nose"), sfx=[SFX("shimmer", 0.2, -12)])
b("هذا الاخير ليس خيالا", bl("هذا ليس خيالا", "archive", str2="امرأة حقيقية فعلته", at2=1.2), cap=False, sfx=[SFX("stinger", 0.1, -10)])
b("وفي اخر هذه الحلقه ستعرف", bl("في آخر الحلقة: لماذا يخفي دماغك الروائح؟", "archive", coral=True, size=70), cap=False)
b("اسمها جوي ميلن", sc("home", [C("JOY", 0.5, "stand", "smile", 1, s=1.7)], cam=PUSH, labels=[L("جوي ميلن — إسكتلندا", y=0.18, ap="جوي", box=True)]), in_=DIP, music_cut="calm")
b("ورثت عن جدتها حاسه", da(value="فرط الشم", label="موروث من جدتها", size=150))
b("وتروي انها لاحظت يوما", sc("home", [C("JOY", 0.62, "think", "thinking", -1), C("LES", 0.4, "stand", "neutral", 1)], cam=PUSH, labels=[L("رائحة جديدة", y=0.18, ap="رائحه", box=True)]))
b("لم يشمها احد غيرها", fc("JOY", "home", "worried", side=0.3, rimSide=1))
b("وتروي العائله ان ليس", sc("home", [C("LES", 0.45, "crossArms", "angry", 1, s=1.5), C("JOY", 0.65, "stand", "sad", -1, s=1.5)], cam=PUSH))
b("وظنت في البدايه ان السبب", fc("JOY", "home", "confused", side=0.3, rimSide=1))
b("وبعد نحو اثني عشر عاما", da(value="1986", label="تشخيص باركنسون — في الخامسة والأربعين", size=160))
b("سنوات طويله مرت", sc("home", [C("JOY", 0.5, "sit", "sad", 1, chair=True, s=1.5)], cam=PULL))
b("ثم ذهبت مع زوجها الى لقاء", sc("studio", [C("JOY", 0.3, "stand", "shocked", 1), C("LES", 0.42, "stand", "neutral", 1), C("PLAIN", 0.6, "sit", "neutral", -1, chair=True), C("PLAIN", 0.78, "sit", "neutral", -1, chair=True)], cam=PUSH), music_cut="tension")
b("وما ان دخلت القاعه", fc("JOY", "studio", "shocked", side=0.3, rimSide=1))
b("الرائحه نفسها", ins("nose", label="الرائحة نفسها!"))
b("حينها فهمت", bl("للمرض رائحة", "archive"), cap=False, sfx=[SFX("impact", 0.2, -10)])
b("وسمع بقصتها باحث", sc("clinic", [C("LAB", 0.6, "explain", "thinking", -1), C("JOY", 0.38, "stand", "neutral", 1)], cam=PUSH, labels=[L("تيلو كونات — إدنبرة", y=0.18, ap="تيلو", box=True)]))
b("اعطوها اثني عشر قميصا", ins("shirts"))
b("تعرفت على قمصان المرضى", ins("shirts", cam=dict(z0=1.1, z1=1.2, x0=0, x1=-20)))
b("لكن بعد نحو ثمانيه اشهر", da(value="8 أشهر", label="ثم شُخّص بالمرض", size=170, color="coral"), sfx=[SFX("hit", 0.3, -10)])
b("انف جوي سبق الطب", fc("JOY", "clinic", "determined", side=0.3, rimSide=1))
b("وصارت قصتها بعد ذلك", ins("news", head="امرأة تشم باركنسون", who="JOY"))
b("هل هذه قوه خارقه", bl("المفاجأة الأولى", "archive"), cap=False, in_=DIP)
b("جوي شمت المرض في زوجها", fc("JOY", "home", "sad", side=0.3, rimSide=1))
b("لم يكن احد في العالم يعرف", sc("clinic", [C("DOC", 0.5, "shrug", "confused", 1, s=1.5)], cam=PUSH))
b("فالرائحه وحدها لا تخبرك", da(icon="brain", value="الرائحة ≠ المعنى", label="الأنف يلتقط… والمعرفة تفسر", size=110, count=2))
b("تخيل ان تشم شيئا غريبا", ar(hero=True, heroC="YOU", pose="think", expr="confused", n=40, cards=["مرض؟", "طعام؟", "عطر؟"], cardsX=[0.2, 0.5, 0.8], cardsY=[0.25, 0.18, 0.25], gap=0.7))
b("ولهذا احتاج الامر", sc("clinic", [C("LAB", 0.5, "holdFront", "determined", 1, prop="paper", s=1.5)], cam=PUSH, labels=[L("بيرديتا باران — مانشستر", y=0.18, ap="بيرديتا", box=True)]))
b("وهو المكان نفسه الذي", ins("bodymap", spots=[[0, -200, "أعلى الظهر", 0.3]]))
b("ويعمل الفريق على اختبار", da(value="مسحة جلد", label="ما زالت في المختبر", size=150))
b("اما المفاجاه الثانيه", bl("المفاجأة الثانية", "archive"), cap=False, music_cut="sad")
b("في عام الفين وخمسه عشر", da(value="2015", label="رحيل لِيس", size=170, color="coral"))
b("انف جوي لم يستطع", fc("JOY", "home", "cry", side=0.3, rimSide=1, tear=0.6))
b("لكنه قد يساعد يوما", da(value="تشخيص مبكر", label="أملٌ لغيره", size=150))
b("وللرائحه وجه اخر", bl("الذاكرة", "archive"), cap=False)
b("فاشارات الشم تصل", ins("brainpath"))
b("ولهذا تستطيع رائحه واحده", ar(hero=True, heroC="YOU", pose="relaxed", expr="awe", n=50, cards=["بيت الجدة", "عطر من رحل"], cardsX=[0.25, 0.75], gap=1.0))
b("كتب الروائي الفرنسي", ins("madeleine"))
b("كان ذلك في الجزء الاول", da(value="ظاهرة بروست", label="ذكرى توقظها رائحة", size=120))
b("فتخيل انفا اقوى بالف", st("city", [C("YOU", 0.5, "handsOnHead", "worried", 1, s=1.3)], so=dict(mood="dusk"), cam=DRIFT))
b("والادب تخيل هذا الانف", ins("novel"))
b("الا شيئا واحدا", bl("يشم كل شيء… إلا نفسه", "archive", coral=True), cap=False)
b("وقد بيعت من هذه الروايه", da(value="+20 مليون", label="نسخة… بعشرات اللغات", size=150))
b("لكن هناك مخلوقات حقيقيه", ins("sniffbars"), music_cut="hopeful", in_=DIP)
b("ولهذا تبحث الكلاب", st("city", [C("PLAIN", 0.4, "stand", "determined", 1)], so=dict(mood="day"), cam=PUSH, labels=[L("🐕", x=0.6, y=0.55, size=120)]))
b("وحتى الجرذان صارت", ins("ratfield"))
b("شم ماغاوا تسعه وثلاثين", da(value="39 + 28", label="لغما + قذيفة لم تنفجر", size=170))
b("وفي عام الفين وعشرين", ins("medal"), sfx=[SFX("shimmer", 0.2, -10)])
b("ولانه خفيف الوزن", ins("ratfield", cam=dict(z0=1.2, z1=1.3, x0=-200, x1=-220)))
b("وتدرب المنظمه نفسها جرذانا", da(value="السل", label="جرذان تشم المرض أيضا", size=170))
b("والان الى العلم", bl("كيف نشمّ أصلا؟", "archive"), cap=False, music_cut="calm")
b("حين تتطاير جزيئات", ins("nose"))
b("وفي عام الفين واربعه نال", da(value="نوبل 2004", label="أكسل وبك: مستقبلات الشم", size=140))
b("وكل رائحه لا تشغل", ins("letters"))
b("وحتى ما تسميه طعما", da(value="النكهة", label="معظمها من الأنف", size=160))
b("ولهذا يفقد الطعام نكهته", st("home", [C("YOU", 0.5, "sit", "sleepy", 1, chair=True, s=1.5)], props=[dict(k="table", x=0.6, plate=True)], cam=PUSH))
b("في عام الفين وسبعه عشر نشر", da(value="2017", label="«ضعف الشم… خرافة»", size=160))
b("ويشرح ان هذه الفكره بدات", sc("archive", [C("OLDMAN", 0.5, "explain", "smirk", 1, s=1.5)], cam=PUSH, labels=[L("بروكا — 1879", y=0.18, ap="بروكا", box=True)]) if False else da(value="1879", label="بروكا: الإنسان لا يعتمد على الشم", size=160))
b("وتشير المراجعه الى ان", da(value="≈ الفئران", label="عدد خلايا البصلة الشمية", size=150))
b("وقبلها بسنوات اجرى فريق", ins("trail"))
b("ومع التدريب صاروا", da(value="أدق وأسرع", label="بالتدريب", size=150))
b("وهناك سؤال يختلف فيه", da(value="ترليون؟", label="دراسة 2014", size=170))
b("لكن في العام التالي انتقد", da(value="لا أحد يعرف", label="الرقم الحقيقي", size=140, color="coral"))
b("والان الى ما وعدتك به", bl("الجواب الموعود", "archive"), cap=False, in_=DIP, sfx=[SFX("stinger", 0.1, -10)])
b("لان دماغك يخفيها عمدا", ins("nose", fade=True, label="التكيف الشمي"))
b("ولهذا لا تشم عطرك", st("home", [C("YOU", 0.45, "stand", "smile", 1, s=1.5), C("PLAIN", 0.62, "stand", "surprised", -1, s=1.5)], cam=PUSH))
b("رائحه دخان", ar(hero=True, heroC="YOU", pose="stand", expr="shocked", n=40, cards=["دخان", "طعام فاسد", "غاز"], cardsX=[0.2, 0.5, 0.8], cardsY=[0.25, 0.18, 0.25], gap=0.6))
b("فانف اقوى بالف مره لن", ins("bubbles", n=44, pick=True, label="الرائحة التي تنقذك"))
b("وحتى حين يضعف الشم", da(value="فقد الشم", label="مرتبط بالقلق والاكتئاب", size=150, color="coral"))
b("فانفك ليس ضعيفا", bl("أنفك أقوى مما قيل لك", "archive"), cap=False, music_cut="hopeful")
b("وهو الحاسه الاقرب", fc("YOU", "home", "smile", side=0.0))
b("ودماغك هو الذي يقرر", da(icon="brain", value="الدماغ يقرر", label="ما تشمه", size=130, count=2))
b("جوي ميلن لم تملك", sc("home", [C("JOY", 0.5, "relaxed", "smile", 1, s=1.7)], cam=PULL))
b("والعبره ليست ان تشم", bl("انتبه للشيء الصغير الذي تغيّر", "archive"), cap=False)
b("فاحيانا يكون اهم ما في", fc("JOY", "home", "smile", side=0.3, rimSide=1))
b("وفي الحلقه القادمه", bl("ماذا لو استطعت حبس أنفاسك ساعة كاملة؟", "archive", str2="الحلقة القادمة", at2=0.8), cap=False, sfx=[SFX("riser", 0, -12)])
b("والان سؤال الحلقه", dict(tpl="endscreen", q="لو خُيّرت: أنف كلب… أم أنف عادي يحفظ ذكرياتك؟", cast=["JOY", "LES", "LAB", "YOU", "PLAIN", "DOC"]), in_=FADE, cap=False)

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
story = {"title": "ماذا لو كانت كل رائحة أقوى بألف مرة؟", "duration": DUR, "shots": shots, "music": music, "sfx": []}
json.dump(story, open(f"{PROJ}/story/shots.json", "w"), ensure_ascii=False, indent=1)
d = [s["end"] - s["start"] for s in shots]; d.sort()
print(len(shots), "shots; median", round(d[len(d) // 2], 2), "min", round(d[0], 2), "max", round(d[-1], 2))
print("music:", [(m["mood"], round(m["start"]), round(m["end"])) for m in music])
