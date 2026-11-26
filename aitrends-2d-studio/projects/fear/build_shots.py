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
b("سطح بنايه من خمسين", dict(tpl="title", lines=["ماذا لو", "لم تشعر بالخوف أبدًا؟"]), bars="scope", cap=False, sfx=[SFX("riser", 0, -12)])
b("تمشي الى الحافه", ins("rooftop"))
b("السيارات صغيره كالنمل", ins("rooftop", cam=IN, label="50 طابقًا… ولا شيء"))
b("خلفك صديقك يرتجف", ins("rooftop", cam=dict(z0=1.2, z1=1.3, x0=300, x1=320)))
b("ماذا لو لم تشعر بالخوف", bl("ماذا لو لم تشعر بالخوف أبدًا؟", "archive", size=70), cap=False, sfx=[SFX("stinger", 0.1, -10)])
b("لا رهبه ولا قلق", da(value="0%", label="رهبة · قلق · خفقان", size=200))
b("في يوم الامتحان تدخل", st("classroom", [C("YOU", 0.5, "sit", "smile", 1, chair=True, s=1.4)], cam=PUSH))
b("وفي حفل المدرسه تقف", st("studio", [C("YOU", 0.5, "explain", "smile", 1, s=1.5)], cam=PUSH, labels=[L("أمام 1000 شخص", y=0.18, box=True)]))
b("وفي مدينه الالعاب", st("city", [C("YOU", 0.5, "stand", "sleepy", 1, s=1.4)], so=dict(mood="day"), cam=PUSH, labels=[L("🎢 … 🥱", y=0.18, box=True)]))
b("يسالك اخوك الم تخف", st("home", [C("YOU", 0.4, "shrug", "smile", 1, s=1.5), C("ADAM", 0.62, "stand", "shocked", -1, s=1.5)], cam=PUSH, labels=[L("«ممّ أخاف؟»", y=0.18, box=True)]))
b("لكن في طريق العوده تعبر", st("city", [C("YOU", 0.45, "stand", "neutral", 1, s=1.3)], so=dict(mood="dusk"), cam=PUSH, labels=[L("🚗💨", x=0.82, y=0.6, size=120)]), music_cut="tension")
b("هذا خيال لكن هناك", ins("amygdala", off=True))
b("وفي اخر هذه الحلقه ستعرف", bl("في آخر الحلقة: سر أشجع الناس", "archive", coral=True, size=70), cap=False)
b("يسميها العلماء بالحرفين", sc("home", [C("SM", 0.5, "stand", "smile", 1, s=1.7)], cam=PUSH, labels=[L("المريضة S.M.", y=0.18, box=True)]), in_=DIP, music_cut="calm")
b("دمر في دماغها منطقتين", ins("amygdala", off=True, label="مرض أورباخ-فيث"))
b("وهذه المنطقه يعدها العلماء", ins("amygdala", off=False, cap="مركز الخوف"))
b("وفي نهايه عام الفين وعشره", sc("clinic", [C("FEINSTEIN", 0.5, "holdFront", "thinking", 1, prop="paper", s=1.5)], cam=PUSH, labels=[L("جاستن فاينشتاين — 2010", y=0.18, box=True)]))
b("حاولوا ان يخيفوها", ins("snakes", label="أفاعٍ وعناكب وبيت رعب"))
b("لم تشعر بالخوف ابدا", fc("SM", "home", "smile", side=0.3, rimSide=1))
b("واخر مره تتذكر", da(value="10 سنوات", label="آخر مرة خافت فيها", size=170))
b("والمدهش ان بقيه مشاعرها", da(value="😠 😢 😊 🤢", label="كل المشاعر… إلا الخوف", size=120))
b("واذا اعجبتك القصه حتى الان", ins("likesub", label="أعجبتك القصة؟"), sfx=[SFX("pop", 0.3, -10)])
b("وهنا تبدا المشكله", bl("وهنا تبدأ المشكلة", "archive", coral=True), cap=False, music_cut="tension")
b("في متجر الافاعي لم", ins("snakes", label="أرادت أن تلمسها!", cam=IN))
b("وفي حياتها الحقيقيه كان", da(value="🔪 🔫", label="هُدّدت… ولم تخف", size=170, color="coral"))
b("وكتب الباحثون جمله", bl("مناعتها ضد الخوف تزيد تعرضها للخطر", "archive", size=62), cap=False)
b("ومع ذلك حذرت عالمه", da(value="حالة واحدة", label="تحذير إليزابيث فيلبس", size=150))
b("فالخوف ليس شعورا مزعجا", st("city", [C("YOU", 0.5, "stand", "neutral", 1, s=1.3)], so=dict(mood="dusk"), cam=DRIFT, labels=[L("إنذار", y=0.18, box=True)]))
b("هناك طفيلي صغير اسمه", ins("ratcat"))
b("وفي عام الفين نشر باحثون", da(value="أكسفورد 2000", label="«الانجذاب القاتل»", size=150))
b("وتقول الابحاث ان الجرذان", ins("ratcat", label="نحو القط… لا بعيدًا عنه"))
b("ووجدت دراسه لاحقه", da(value="رائحة القط فقط", label="الخوف الوحيد الذي يحميه", size=130))
b("جرذ فقد خوفه", ins("ratcat", cam=IN))
b("وتعود انت الى قصتك", st("home", [C("YOU", 0.4, "stand", "neutral", 1, s=1.5), C("PLAIN", 0.66, "stand", "smirk", -1, s=1.5)], cam=PUSH))
b("فالخطر لا يصير اصغر", bl("الخطر لا يصغر… بل يقترب", "archive", coral=True), cap=False)
b("والان الى المفاجاه", bl("المفاجأة", "archive"), cap=False, in_=DIP, music_cut="hopeful")
b("في الثالث من يونيو", ins("climb", label="أليكس هونولد — 3 يونيو 2017"))
b("خطا واحد كان يعني", ins("climb", cam=IN))
b("وفاز الفيلم الوثائقي", ins("medal"), sfx=[SFX("shimmer", 0.2, -10)])
b("وقبلها بسنوات فحصت", sc("clinic", [C("JOSEPH", 0.5, "explain", "thinking", 1, s=1.6)], cam=PUSH, labels=[L("جين جوزيف", y=0.18, box=True)]))
b("فبدت اللوزه الدماغيه", ins("amygdala", off=True, cap="لوزة هادئة"))
b("لكنها لم تقل انه", da(value="تنظيم؟", label="لا انعدام خوف", size=180))
b("فهونولد لم يولد", sc("studio", [C("HONNOLD", 0.5, "stand", "determined", 1, s=1.6)], cam=PULL, labels=[L("يسمع الخوف… ولا يطيعه", y=0.18, box=True)]))
b("والمفاجاه الثانيه جاءت", ins("co2", label="35% ثاني أكسيد الكربون"))
b("فاصيب الثلاثه بنوبه", da(value="3 من 3", label="مقابل 3 من 12 سليمًا", size=180, color="coral"))
b("واستنتج الباحثون ان", ins("amygdala", off=True, cap="خوف من الداخل"))
b("وفي دراسه لاحقه على", da(value="توأمان", label="قلق… وهلع عند أحدهما", size=170))
b("لم يتركها جسدها بلا", fc("SM", "home", "shocked", side=0.3, rimSide=1))
b("وللخوف اثر اعمق", sc("archive", [C("BELYAEV", 0.5, "holdFront", "thinking", 1, prop="paper", s=1.6)], cam=PUSH, labels=[L("دميتري بيلياييف — 1959", y=0.18, box=True)]), music_cut="calm")
b("كان يختار من كل جيل", ins("foxes", label="الأقل خوفًا فقط"))
b("وبعد اجيال لم تصر", ins("foxes", cam=IN))
b("وما زالت تلميذته", da(value="لودميلا تروت", label="تواصل التجربة", size=140))
b("ومع ذلك شكك فريق", da(value="2019", label="تشكيك في الاستنتاجات", size=170, color="coral"))
b("والحكايات الشعبيه عرفت", sc("archive", [C("GRIMMBOY", 0.5, "stand", "smile", 1, s=1.6)], cam=PUSH, labels=[L("الأخوان غريم — 1819", y=0.18, box=True)]))
b("يبيت في قلعه مسكونه", st("bedroom", [C("GRIMMBOY", 0.5, "sit", "smile", 1, s=1.4)], so=dict(mood="night"), cam=PUSH))
b("وفي النهايه تسكب عليه", da(value="🪣💦🐟", label="دلو ماء بارد… فيرتجف", size=150))
b("والان الى ما وعدتك به", bl("الجواب الموعود", "archive"), cap=False, in_=DIP, sfx=[SFX("stinger", 0.1, -10)], music_cut="hopeful")
b("لانه الحارس الذي يقف", ins("rooftop"))
b("اس ام فقدته فصارت", ins("snakes"))
b("اما السر عند اشجع الناس", bl("أن تسمع الخوف… ثم تقرر أنت", "archive"), cap=False, sfx=[SFX("impact", 0.2, -10)])
b("هونولد لم يطفئ الانذار", ins("climb"))
b("والخوف الذي يزعجك", st("classroom", [C("YOU", 0.5, "sit", "worried", 1, chair=True, s=1.4)], cam=PUSH))
b("وفي اخر قصتنا تسمع", ins("rooftop", youPose="stand", youExpr="smile", label="خطوة إلى الوراء"))
b("انه الصديق الذي يصرخ", fc("YOU", "home", "smile", side=0.0))
b("واذا استمتعت بهذه القصه", ins("likesub", label="لا تنسَ: إعجاب + اشتراك + 🔔"), sfx=[SFX("pop", 0.3, -10)])
b("وفي الحلقه القادمه", bl("ماذا لو قدرت تعرف كم مرة باقي لك تشوف كل شخص تحبه؟", "archive", str2="الحلقة القادمة", at2=0.8, size=56), cap=False, sfx=[SFX("riser", 0, -12)])
b("والان سؤال الحلقه", dict(tpl="endscreen", q="لو خُيّرت: لا تخاف أبدًا… ولا تعرف متى تهرب؟", cast=["SM", "HONNOLD", "YOU", "FEINSTEIN", "JOSEPH", "BELYAEV"]), in_=FADE, cap=False)

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
    if d > 4.0 and tpl in ("stage", "insert", "archive", "data"):
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
story = {"title": "ماذا لو لم تشعر بالخوف أبدًا؟", "duration": DUR, "shots": shots, "music": music, "sfx": []}
json.dump(story, open(f"{PROJ}/story/shots.json", "w"), ensure_ascii=False, indent=1)
d = [s["end"] - s["start"] for s in shots]; d.sort()
print(len(shots), "shots; median", round(d[len(d) // 2], 2), "min", round(d[0], 2), "max", round(d[-1], 2))
print("music:", [(m["mood"], round(m["start"]), round(m["end"])) for m in music])
