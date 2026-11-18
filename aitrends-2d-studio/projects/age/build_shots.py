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

IN = dict(z0=1.12, z1=1.22, x0=0, x1=-20)
b("ماذا لو كان كل يوم", dict(tpl="title", lines=["ماذا لو", "كان كل يوم من عمرك يساوي عامًا؟"]), bars="scope", cap=False, sfx=[SFX("riser", 0, -12)])
b("تستيقظ صباح السبت", st("bedroom", [C("YOUKID", 0.5, "stand", "awe", 1, s=1.4)], cam=PUSH))
b("وفي نهايه الاسبوع", ins("calendar", d0=5, d1=13, head="السبت ← الجمعة"))
b("بعد شهر واحد تبلغ", ins("calendar", d0=13, d1=30))
b("ثمانون عاما في اقل", ins("calendar", d0=30, d1=80, label="أقل من 3 أشهر"), sfx=[SFX("stinger", 0.1, -10)])
b("يبدو هذا خيالا", bl("ليس خيالًا", "archive", coral=True), cap=False)
b("لكن هناك اطفالا حقيقيين", st("home", [C("SAM", 0.5, "stand", "smile", 1, s=1.6)], cam=PUSH, labels=[REP()]))
b("وفي اخر هذه الحلقه ستعرف", bl("في آخر الحلقة: هل الحياة القصيرة ناقصة؟", "archive", coral=True, size=70), cap=False)
b("ولماذا تشعر ان ايامك", da(value="أسرع؟", label="لماذا تمر أيامك أسرع كلما كبرت", size=170, color="coral"))
b("اسمه سام بيرنز", sc("home", [C("SAM", 0.5, "stand", "smile", 1, s=1.8)], cam=PUSH, labels=[L("سام بيرنز — أمريكا", y=0.18, ap="سام", box=True)]), in_=DIP, music_cut="calm")
b("يولد الطفل المصاب به", da(value="البروجيريا", label="الشيخوخة المبكرة — مرض نادر جدا", size=140))
b("ثم يتباطا نموه", sc("home", [C("SAM", 0.45, "stand", "neutral", 1, s=1.5), C("PLAIN", 0.65, "stand", "neutral", -1, s=1.5)], cam=PUSH))
b("والاخطر ما لا يرى", ins("heart"))
b("والداه طبيبان", sc("clinic", [C("LESLIE", 0.4, "explain", "determined", 1, s=1.5), C("SCOTT", 0.6, "crossArms", "determined", -1, s=1.5)], cam=PUSH, labels=[L("والداه: طبيبان", y=0.18, box=True)]))
b("اسسا عام الف وتسعمئه", da(value="1999", label="مؤسسة أبحاث البروجيريا", size=170))
b("وبعد اربع سنوات فقط", da(value="2003", label="اكتشاف الجين: LMNA", size=170), sfx=[SFX("hit", 0.3, -10)])
b("يجعل الخلايا تصنع", ins("cells", max=1, stop=False) if False else ins("bodymap", spots=[[0, -150, "بروتين مشوّه: البروجيرين", 0.3]]))
b("وكانت المؤسسه التي", sc("clinic", [C("LESLIE", 0.5, "holdFront", "smile", 1, prop="paper", s=1.6)], cam=PUSH))
b("اما سام نفسه فلم", sc("home", [C("SAM", 0.5, "sit", "smile", 1, s=1.5)], cam=PUSH, labels=[L("🧱 ليغو", x=0.7, y=0.55, size=80)]))
b("ويعزف في فرقه", sc("pitch", [C("SAM", 0.5, "stand", "smile", 1, s=1.4)], cam=PUSH, labels=[L("🥁", x=0.62, y=0.5, size=110)]))
b("وكان يحلم بالدراسه", da(value="MIT", label="حلمه: معهد ماساتشوستس للتكنولوجيا", size=180))
b("وفي عام الفين وثلاثه عشر عرض", ins("news", head="الحياة كما يراها سام", who="SAM"))
b("وفي العام نفسه وقف", sc("studio", [C("SAM", 0.5, "explain", "smile", 1, s=1.6)], cam=PUSH, labels=[L("TEDx — 2013", y=0.18, box=True)]), music_cut="hopeful")
b("ومن افكاره فيها", bl("تقبّل ما لا تستطيع… فهناك الكثير مما تستطيع", "archive", size=66), cap=False)
b("شاهد المحاضره عشرات", da(value="+50 مليون", label="مشاهدة حول العالم", size=160))
b("وبعد اسابيع قليله", da(value="10 يناير 2014", label="رحل في السابعة عشرة", size=130, color="coral"), music_cut="sad")
b("وهنا المفاجاه الاولى", bl("المفاجأة الأولى", "archive"), cap=False, in_=DIP, music_cut="calm")
b("قد تظن ان هذا المرض", st("home", [C("YOU", 0.5, "think", "thinking", 1, s=1.6)], cam=PUSH))
b("فالاطباء يقولون ان ذكاء", da(icon="brain", value="ذكاء طبيعي", label="وتطور حركي طبيعي", size=130, count=2))
b("جسد يشيخ بسرعه", sc("home", [C("SAM", 0.5, "relaxed", "smile", 1, s=1.7)], cam=PULL))
b("وفي عام الفين وثلاثه عشر نشر", st("clinic", [C("LAB", 0.5, "holdFront", "thinking", 1, prop="paper", s=1.5)], cam=PUSH, labels=[L("ستيف هورفاث — 2013", y=0.18, box=True)]))
b("اي ان المرض لا يدير", da(value="جسد ≠ عقل", label="الشيخوخة لا تصيب كل شيء", size=140))
b("فلو صار كل يوم من عمرك", fc("YOU", "home", "sad", side=0.0))
b("بل ان يبقى قلبك", st("home", [C("YOU", 0.5, "stand", "sad", 1, s=1.5)], cam=PULL))
b("اما المفاجاه الثانيه", bl("المفاجأة الثانية", "archive"), cap=False, music_cut="sad")
b("يقدر الباحثون ان عدد", da(value="≈ 400", label="طفل فقط في العالم كله", size=180))
b("ودون علاج يموت", da(value="14.5", label="متوسط العمر دون علاج", size=180, color="coral"))
b("طفل في العاشره", ins("heart", mode="fast"))
b("ولسنوات طويله لم يكن", sc("clinic", [C("DOC", 0.5, "shrug", "sad", 1, s=1.5)], cam=PUSH))
b("فقد شارك سام نفسه", sc("clinic", [C("SAM", 0.4, "stand", "determined", 1), C("LESLIE", 0.6, "explain", "smile", -1)], cam=PUSH), music_cut="hopeful")
b("وفي العشرين من نوفمبر", da(value="20 نوفمبر 2020", label="أول علاج للبروجيريا في التاريخ", size=120), sfx=[SFX("shimmer", 0.2, -10)])
b("ليس شفاء لكنه", da(value="−60% · +2.5", label="الوفيات · سنوات إضافية", size=130))
b("وقامت الموافقه على", da(value="62 طفلا", label="مستشفى بوسطن للأطفال — ثم أوروبا 2022", size=150))
b("سنتان ونصف قد تبدوان", ins("cake", n=14, label="سدس حياته تقريبا"))
b("سدس حياه اضافي", sc("home", [C("LESLIE", 0.38, "stand", "smile", 1), C("SAM", 0.55, "stand", "smile", -1), C("SCOTT", 0.7, "stand", "smile", -1)], cam=PULL))
b("وفي الطبيعه مخلوقات", ins("mayfly", label="ذبابة مايو"), in_=DIP, music_cut="calm")
b("وفي نوع امريكي منها", ins("mayfly", timer=True, label="دولانيا: أقل من 5 دقائق"))
b("ويعتقد انه اقصر", da(value="5 دقائق", label="أقصر عمر بالغ لحشرة", size=170))
b("وعلى الطرف الاخر", ins("shark", to=272, pre="≥ ", label="قرش غرينلاند"))
b("درسوا ثمانيا", ins("eye") if False else ins("shark", to=392, label="أكبرها ± 120 عامًا", cam=IN))
b("ولا يبلغ هذا القرش", da(value="156 عامًا", label="حتى يبلغ سن التكاثر", size=160))
b("اي ان قرشا يسبح", bl("وُلد قبل المصباح الكهربائي", "archive"), cap=False)
b("اما اطول عمر انساني", sc("home", [C("CALMENT", 0.5, "stand", "smile", 1, s=1.6)], cam=PUSH, labels=[L("جان كالمان — فرنسا", y=0.18, ap="جان", box=True)]))
b("مئه واثنين وعشرين عاما", da(value="122 عامًا", label="و164 يومًا — 1875 إلى 1997", size=160))
b("وهي الانسان الوحيد", da(value="120+", label="الوحيدة الموثقة", size=180))
b("والادب قلب الزمن", da(value="1922", label="فيتزجيرالد: الحالة الغريبة لبنجامين باتون", size=170))
b("وتحولت عام الفين وثمانيه", sc("archive", [C("BUTTON", 0.5, "stand", "neutral", 1, s=1.6)], cam=PULL, labels=[L("بنجامين باتون", y=0.18, box=True)]))
b("والان الى العلم", bl("لماذا نشيخ؟", "archive"), cap=False, music_cut="calm", in_=DIP)
b("في عام الف وتسعمئه وواحد وستين", ins("cells", max=50, stop=True))
b("وصار هذا يسمى حد", da(value="40–60", label="حد هايفليك — 1961", size=170))
b("ثم اكتشف العلماء جزءا", ins("telomere", shrink=False))
b("وتقصر هذه الاغطيه قليلا", ins("telomere", label="تقصر مع كل انقسام"))
b("وفي عام الف وتسعمئه واربعه وثمانين", da(value="1984", label="بلاكبيرن وغرايدر: التيلوميراز", size=170))
b("وفي عام الفين وتسعه نالت", ins("medal"), sfx=[SFX("shimmer", 0.2, -10)])
b("ودراسه هورفاث التي", da(value="353", label="علامة على الحمض النووي = ساعة الجسد", size=180))
b("فلجسدك عمر مكتوب", st("home", [C("YOU", 0.5, "holdFront", "surprised", 1, prop="paper", s=1.5)], cam=PUSH))
b("وفي الدراسه نفسها مفاجاتان", da(value="+36 عامًا", label="عمر أنسجة الأورام", size=160, color="coral"))
b("اما الخلايا التي اعاد", da(value="0", label="عادت ساعتها إلى الصفر", size=200))
b("لكن هناك سؤال اخر", bl("خلاف علمي", "archive", coral=True), cap=False)
b("في عام الف وثمانمئه وسبعه", da(value="1 / 5  ·  1 / 50", label="بول جانيه — 1877", size=130))
b("وبعد ثلاثه عشر عاما", sc("archive", [C("OLDMAN", 0.5, "explain", "thinking", 1, s=1.5)], cam=PUSH, labels=[L("وليام جيمس — 1890", y=0.18, box=True)]))
b("لكن دراسات حديثه وجدت", da(value="ساعة ✗ · سنوات ✓", label="ما يتسارع مع العمر: السنوات الطويلة فقط", size=110))
b("ويرى باحثون اخرون", ar(hero=True, heroC="YOU", pose="stand", expr="worried", n=40, cards=["مسؤوليات", "روتين", "تجارب جديدة؟"], cardsX=[0.2, 0.5, 0.8], cardsY=[0.25, 0.18, 0.25], gap=0.6))
b("وما زال الجواب الكامل", da(icon="brain", value="؟", label="ما زال موضع بحث", size=180))
b("والان الى ما وعدتك به", bl("الجواب الموعود", "archive"), cap=False, in_=DIP, sfx=[SFX("stinger", 0.1, -10)], music_cut="hopeful")
b("لو صار كل يوم من عمرك عاما", ins("calendar", d0=1, d1=80))
b("ستحتفل بعيد ميلادك", ins("cake", n=10, label="كل صباح!"))
b("هل تكون حياتك ناقصه", st("home", [C("YOU", 0.5, "think", "thinking", 1, s=1.6)], cam=PUSH))
b("ذبابه مايو تعيش دقائق", ins("mayfly"))
b("وقرش غرينلاند يعيش", ins("shark", to=300, unit=" عام"))
b("وسام بيرنز عاش", sc("studio", [C("SAM", 0.5, "explain", "smile", 1, s=1.7)], cam=PULL))
b("اما سؤال لماذا تمر", st("city", [C("YOU", 0.5, "relaxed", "smile", 1, s=1.3)], so=dict(mood="day"), cam=DRIFT))
b("فربما لا يكون السؤال", bl("كم يومًا تتذكر أنك عشته؟", "archive"), cap=False)
b("فعمرك ليس عدد الايام", fc("YOU", "home", "smile", side=0.0))
b("وفي الحلقه القادمه", bl("ماذا لو كان رد فعلك أسرع بمئة مرة؟", "archive", str2="الحلقة القادمة", at2=0.8), cap=False, sfx=[SFX("riser", 0, -12)])
b("والان سؤال الحلقه", dict(tpl="endscreen", q="لو خُيّرت: عمر كامل في 3 أشهر… أم عمر طويل يمر كيوم واحد؟", cast=["SAM", "LESLIE", "CALMENT", "YOU", "BUTTON", "SCOTT"]), in_=FADE, cap=False)

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
story = {"title": "ماذا لو كان كل يوم من عمرك يساوي عامًا؟", "duration": DUR, "shots": shots, "music": music, "sfx": []}
json.dump(story, open(f"{PROJ}/story/shots.json", "w"), ensure_ascii=False, indent=1)
d = [s["end"] - s["start"] for s in shots]; d.sort()
print(len(shots), "shots; median", round(d[len(d) // 2], 2), "min", round(d[0], 2), "max", round(d[-1], 2))
print("music:", [(m["mood"], round(m["start"]), round(m["end"])) for m in music])
