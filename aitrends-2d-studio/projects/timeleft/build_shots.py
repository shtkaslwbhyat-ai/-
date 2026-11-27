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
b("عشاء الجمعه في بيت", dict(tpl="title", lines=["ماذا لو قدرت تعرف", "كم مرة باقي لك تشوف كل شخص تحبه؟"]), bars="scope", cap=False, sfx=[SFX("riser", 0, -12)])
b("امك تضع الاطباق", ins("dinnercount", ppl=[["MOM", None], ["YOU", None], ["GRANDPA", None], ["ADAM", None]], youExpr="smile"))
b("وفجاه يظهر فوق راس امك", ins("dinnercount", ppl=[["MOM", 312], ["YOU", None], ["GRANDPA", None], ["ADAM", None]]), sfx=[SFX("shimmer", 0.2, -10)])
b("ثم فوق راس جدك", ins("dinnercount", ppl=[["MOM", 312], ["YOU", None], ["GRANDPA", 7], ["ADAM", None]], cam=IN))
b("ماذا لو قدرت تعرف", bl("ماذا لو قدرت تعرف كم مرة باقي لك تشوف كل شخص تحبه؟", "archive", size=56), cap=False, sfx=[SFX("stinger", 0.1, -10)])
b("كل رقم يقول لك", da(value="312", label="مرة… وجهًا لوجه، قبل النهاية", size=190))
b("صديقك المقرب فوقه", st("city", [C("YOU", 0.4, "talk", "smile", 1, s=1.5), C("ADAM", 0.62, "laugh", "laugh", -1, s=1.5)], so=dict(mood="day"), cam=PUSH, labels=[L("4000", x=0.62, y=0.2, box=True)]))
b("لكن حين تعود الى البيت", st("bedroom", [C("YOU", 0.5, "sit", "sad", 1, s=1.4)], so=dict(mood="night"), cam=PULL), music_cut="sad")
b("جدك سبع مرات فقط", da(value="7", label="مرات فقط", size=220, color="coral"))
b("هذا خيال لكن هناك", ins("lifegrid", used=0.0))
b("وفي اخر هذه الحلقه ستعرف", bl("في آخر الحلقة: الشيء الوحيد الذي يغيّر الرقم", "archive", coral=True, size=62), cap=False)
b("اسمه تيم اوربان", sc("studio", [C("URBAN", 0.5, "explain", "smile", 1, s=1.7)], cam=PUSH, labels=[L("تيم أوربان", y=0.18, ap="تيم", box=True)]), in_=DIP, music_cut="calm")
b("في عام الفين وخمسه عشر وهو", ins("lifegrid", used=0.34, label="حياته مربعات صغيرة"))
b("فوجد انه حين تخرج", ins("lifegrid", used=0.93, label="الوقت مع الوالدين"))
b("اي انه يعيش الان", da(value="آخر 5%", label="من وقته مع والديه", size=170, color="coral"))
b("والسبب بسيط وقاس", st("home", [C("YOUKID", 0.4, "stand", "smile", 1, s=1.3), C("MOM", 0.62, "stand", "smile", -1, s=1.5)], cam=PUSH, labels=[L("كل يوم… ثم بضع مرات في السنة", y=0.18, box=True)]))
b("سمى اوربان مقالته", ins("news", head="الذيل الأخير", who="URBAN"))
b("واذا اعجبتك القصه حتى الان", ins("likesub", label="أعجبتك القصة؟"), sfx=[SFX("pop", 0.3, -10)])
b("وهنا تبدا المشكله", bl("وهنا تبدأ المشكلة", "archive", coral=True), cap=False, music_cut="tension")
b("في الاسبوع التالي تزور", st("home", [C("YOU", 0.4, "sit", "smile", 1, chair=True, s=1.4), C("GRANDPA", 0.62, "sit", "smile", -1, chair=True, s=1.4)], cam=PUSH))
b("وحين تقوم لتخرج", ins("dinnercount", ppl=[["YOU", None], ["GRANDPA", 7]], dec=True, label="7 ← 6"))
b("ثم ترى في الجامعه زميلا", st("classroom", [C("YOU", 0.38, "stand", "worried", 1, s=1.4), C("PLAIN", 0.66, "stand", "neutral", -1, s=1.4)], cam=PUSH, labels=[L("1", x=0.66, y=0.22, box=True)]))
b("فتمر بجانبه وتبتسم", fc("YOU", "classroom", "sad", side=0.0))
b("وفي الليل لا تنام", st("bedroom", [C("YOU", 0.5, "lie", "sad", 1, s=1.3)], so=dict(mood="night"), cam=PULL))
b("والارقام الحقيقيه ليست", ins("alonechart", label="مسح استخدام الوقت الأمريكي"))
b("والاغرب ان الشباب", da(value="+45%", label="وقت الشباب وحدهم (2010 ← 2023)", size=180, color="coral"))
b("ووجد الموقع ايضا", ins("alonechart", cam=IN))
b("وهي بيانات من اشخاص", da(value="وحدك ≠ وحيد", label="تنبيه الباحثين", size=150))
b("لكن الرقم فوق رؤوس", ins("dinnercount", ppl=[["MOM", 311], ["YOU", None], ["GRANDPA", 6], ["ADAM", 3998]]))
b("والان الى المفاجاه", bl("المفاجأة", "archive"), cap=False, in_=DIP, music_cut="hopeful")
b("درست عالمه النفس لورا", sc("clinic", [C("CARSTENSEN", 0.5, "explain", "thinking", 1, s=1.6)], cam=PUSH, labels=[L("لورا كارستنسن — ستانفورد", y=0.18, box=True)]))
b("حين نشعر ان الوقت مفتوح", da(value="وقت مفتوح ← الجديد", label="معارف · أشخاص · معلومات", size=110))
b("اما حين نشعر انه محدود", da(value="وقت محدود ← من نحب", label="المشاعر قبل كل شيء", size=110, color="coral"))
b("وفي تجاربها حين خير", ar(hero=True, heroC="OLDMAN", pose="stand", expr="smile", n=40, cards=["من تحب ❤", "شخص جديد ✨"], cardsX=[0.25, 0.75], gap=1.0))
b("والمفاجئ ان السبب", da(icon="brain", value="الإحساس بالوقت", label="لا العمر", size=130, count=2))
b("ومع ذلك ما زال باحثون", da(value="مراجعة مستمرة", label="خلاف علمي", size=140, color="coral"))
b("اي ان الرقم فوق راس جدك", st("home", [C("YOU", 0.4, "stand", "smile", 1, s=1.5), C("GRANDPA", 0.62, "talk", "smile", -1, s=1.5)], cam=PUSH))
b("وهناك قصه حقيقيه", sc("studio", [C("MITCH", 0.5, "stand", "neutral", 1, s=1.6)], cam=PUSH, labels=[L("ميتش ألبوم — 1995", y=0.18, box=True)]))
b("كان موري يحتضر", sc("home", [C("MORRIE", 0.5, "sit", "smile", 1, chair=True, s=1.6)], cam=PUSH, labels=[L("موري شوارتز", y=0.18, box=True)]))
b("وكان موري يدرس في جامعه", ins("tuesdays", label="كل يوم ثلاثاء"))
b("اربع عشره زياره فقط", ins("tuesdays", cam=IN))
b("وصار من اكثر كتب السير", ins("news", head="أيام الثلاثاء مع موري", who="MORRIE"))
b("ميتش عرف الرقم تقريبا", fc("MITCH", "home", "smile", side=0.3, rimSide=1))
b("ولكن للامر وجها اخر", sc("clinic", [C("WARE", 0.5, "explain", "sad", 1, s=1.6)], cam=PUSH, labels=[L("بروني وير — ممرضة", y=0.18, box=True)]), music_cut="calm")
b("ومنه ليتني عشت حياه", ar(hero=True, heroC="OLDMAN", pose="sit", expr="sad", n=40, cards=["حياة صادقة", "عمل أقل", "الأصدقاء", "سعادة"], cardsX=[0.15, 0.38, 0.62, 0.85], cardsY=[0.25, 0.18, 0.18, 0.25], gap=0.5))
b("وصار كتابها مشهورا", da(value="27 لغة", label="ملاحظات… لا دراسة علمية", size=170))
b("اما العلم فعنده دراسه", da(value="1938 ← اليوم", label="دراسة هارفارد — 268 طالبًا", size=130))
b("ويقول مديرها روبرت", sc("studio", [C("WALDINGER", 0.5, "explain", "smile", 1, s=1.6)], cam=PUSH, labels=[L("روبرت والدينغر", y=0.18, box=True)]))
b("كانوا الاكثر صحه في الثمانين", da(value="50 → 80", label="رضا العلاقات → الصحة", size=170))
b("لكن هنا يظهر الثمن", bl("الثمن: أن تعدّ بدل أن تعيش", "archive", coral=True), cap=False, sfx=[SFX("impact", 0.2, -10)])
b("يجلس مع جده وعيناه", ins("dinnercount", ppl=[["YOU", None], ["GRANDPA", 5]], youExpr="sad"))
b("والان الى ما وعدتك به", bl("الجواب الموعود", "archive"), cap=False, in_=DIP, sfx=[SFX("stinger", 0.1, -10)], music_cut="hopeful")
b("الجواب الاثنان معا", da(value="ينقذك + يتعبك", label="الاثنان معًا", size=150))
b("اما الشيء الوحيد الذي", bl("الشيء الوحيد الذي يغيّره: أنت", "archive"), cap=False)
b("فالرقم في الحقيقه ليس", st("home", [C("YOU", 0.5, "phone", "smile", 1, s=1.6)], cam=PUSH))
b("وفي اخر قصتنا تمسك", st("home", [C("YOU", 0.5, "phone", "smile", 1, s=1.6)], cam=PULL, labels=[L("«سآتي غدًا… وبعد غد»", y=0.18, box=True)]))
b("فالمهم ليس كم مره", fc("YOU", "home", "smile", side=0.0))
b("واذا استمتعت بهذه القصه", ins("likesub", label="إعجاب + اشتراك + شاركها مع من تحب"), sfx=[SFX("pop", 0.3, -10)])
b("وفي الحلقه القادمه", bl("ماذا لو أصرّ أهلك أن شخصًا غريبًا هو أخوك الحقيقي؟", "archive", str2="الحلقة القادمة", at2=0.8, size=56), cap=False, sfx=[SFX("riser", 0, -12)])
b("والان سؤال الحلقه", dict(tpl="endscreen", q="لو خُيّرت: ترى الرقم فوق رؤوس من تحب… حتى لو كان صغيرًا؟", cast=["URBAN", "MORRIE", "YOU", "GRANDPA", "MOM", "CARSTENSEN"]), in_=FADE, cap=False)

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
    if d > 3.6 and tpl in ("stage", "insert", "archive", "data"):
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
story = {"title": "ماذا لو قدرت تعرف كم مرة باقي لك تشوف كل شخص تحبه؟", "duration": DUR, "shots": shots, "music": music, "sfx": []}
json.dump(story, open(f"{PROJ}/story/shots.json", "w"), ensure_ascii=False, indent=1)
d = [s["end"] - s["start"] for s in shots]; d.sort()
print(len(shots), "shots; median", round(d[len(d) // 2], 2), "min", round(d[0], 2), "max", round(d[-1], 2))
print("music:", [(m["mood"], round(m["start"]), round(m["end"])) for m in music])
