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
b("صباح الاثنين في ساحه", dict(tpl="title", lines=["ماذا لو", "شعرت بمشاعر كل من حولك؟"]), bars="scope", cap=False, sfx=[SFX("riser", 0, -12)])
b("يقترب منك صديقك ادم", st("classroom", [C("YOU", 0.4, "stand", "neutral", 1, s=1.5), C("ADAM", 0.62, "wave", "smile", -1, s=1.5)], cam=PUSH, labels=[L("«أنا بخير»", y=0.18, box=True)]))
b("لكنك في اللحظه نفسها", ins("emoaura"), sfx=[SFX("shimmer", 0.2, -10)])
b("انه حزن ادم", ins("emoaura", cam=IN, label="حزنٌ ليس حزنك"))
b("ماذا لو شعرت بمشاعر", bl("ماذا لو شعرت بمشاعر كل من حولك؟", "archive", size=70), cap=False, sfx=[SFX("stinger", 0.1, -10)])
b("القاعده بسيطه", da(value="شعورهم = شعورك", label="كل من يقترب منك", size=140))
b("في المقهى يقرا رجل", ins("emoaura", warm=True, other="PLAIN", otherExpr="laugh", youExpr="laugh"))
b("تسالك اختك لماذا", st("seacafe", [C("YOU", 0.42, "laugh", "laugh", 1, s=1.5), C("SALMA", 0.62, "stand", "confused", -1, s=1.5)], cam=PUSH, labels=[L("«هو فرحان»", y=0.18, box=True)]))
b("ثم تزور جدتك في المستشفى", st("clinic", [C("YOU", 0.5, "stand", "worried", 1, s=1.4)], cam=PUSH), music_cut="tension")
b("خوفهم كله يدخل صدرك", ins("crowdwave", label="خمسون خوفًا… في صدرك"))
b("تخرج مسرعا الى الشارع", st("city", [C("YOU", 0.5, "handsOnHead", "shocked", 1, s=1.3)], so=dict(mood="dusk"), cam=DRIFT))
b("هذا خيال لكن هناك طبيبا", ins("mirrortouch"))
b("وفي اخر هذه الحلقه ستعرف", bl("في آخر الحلقة: نعمة أم لعنة؟", "archive", coral=True, size=70), cap=False)
b("اسمه جويل ساليناس", sc("clinic", [C("SALINAS", 0.5, "stand", "smile", 1, s=1.7)], cam=PUSH, labels=[L("جويل ساليناس — طبيب أعصاب", y=0.18, ap="جويل", box=True)]), in_=DIP, music_cut="calm")
b("حين يرى انسانا يلمس", ins("mirrortouch", label="يرى اللمسة… فيشعر بها"))
b("وتقول نبذه كتابه", da(value="جسديًا + عاطفيًا", label="يشعر بتجارب الآخرين", size=130))
b("وعنده انواع اخرى", da(value="🎵 = 🎨", label="يرى الموسيقى ألوانًا", size=170))
b("تخيل طبيبا يقف بجانب", ins("mirrortouch", cam=IN))
b("هذا ما وصفه ساليناس", fc("SALINAS", "clinic", "worried", side=0.3, rimSide=1))
b("وفي عام الفين وسبعه عشر نشر", ins("news", head="طبيب يشعر بألمك", who="SALINAS"))
b("وكان يعمل يومها", da(value="بوسطن", label="مستشفى ماساتشوستس العام", size=170))
b("وقارن احد نقاد", da(value="أوليفر ساكس", label="مقارنة النقاد", size=150))
b("وهنا المفاجاه الاولى", bl("المفاجأة الأولى", "archive"), cap=False, in_=DIP)
b("فقد روي ان ما شعر به", sc("clinic", [C("SALINAS", 0.38, "explain", "determined", 1), C("PLAIN", 0.62, "sit", "worried", -1, chair=True)], cam=PUSH))
b("جسده صار اداه تشخيص", ins("bodymap", spots=[[0, -170, "جلطة في الرئتين", 0.3]]))
b("وهذه الحاله ليست نادره", st("studio", [C("LAB", 0.5, "holdFront", "thinking", 1, prop="paper", s=1.5)], cam=PUSH, labels=[L("بانيسي ووارد — 2007", y=0.18, box=True)]))
b("فوجدوا انهم سجلوا", da(value="تعاطف أعلى", label="عند عشرة أشخاص بهذه الحالة", size=140))
b("ثم قدرت دراسه لاحقه", da(value="1 من 60", label="نحو 1.6% من الناس", size=180))
b("ربما يجلس احدهم", st("classroom", [C("PLAIN", 0.3, "sit", "neutral", 1, chair=True), C("PLAIN", 0.5, "sit", "smile", 1, chair=True), C("YOU", 0.7, "sit", "surprised", -1, chair=True)], cam=PUSH))
b("اما المفاجاه الثانيه", bl("المفاجأة الثانية", "archive"), cap=False, music_cut="sad")
b("في عام الفين واربعه عشر نشرت", sc("studio", [C("SINGER", 0.5, "explain", "thinking", 1, s=1.6)], cam=PUSH, labels=[L("تانيا سينغر وأولغا كليميكي", y=0.18, box=True)]))
b("دربوا متطوعين يوما", da(value="يوم واحد", label="تدريب على التعاطف مع الألم", size=160))
b("زادت مشاعر مجموعه التعاطف", ins("bodymap", spots=[[0, -250, "مناطق ألم التعاطف", 0.3]]))
b("كان ادمغتهم صارت", ins("crowdwave", color="#7aa0ff", expr="sad"))
b("وكتب الباحثون ان المشاركه", da(value="احتراق نفسي", label="ثمن المشاركة المفرطة", size=150, color="coral"))
b("تخيل ممرضه في قسم", ar(hero=True, heroC="NURSE", pose="stand", expr="sad", n=40, cards=["ممرضة", "معلّم", "أم"], cardsX=[0.2, 0.5, 0.8], cardsY=[0.25, 0.18, 0.25], gap=0.6))
b("لن يستطيعوا المساعده", fc("YOU", "clinic", "cry", side=0.0, tear=0.6))
b("فالقدره التي تبدو", bl("قد تُطفئ إنسانيتك", "archive", coral=True), cap=False)
b("والمشاعر تنتقل بيننا", ins("feed"), in_=DIP, music_cut="calm")
b("بعضهم راى منشورات ايجابيه", ins("feed", mood="sad", big="😊 ↓", sub="منشورات إيجابية أقل"))
b("والنتيجه ان من قلت", da(value="😊 ↓  😢 ↑", label="ما كتبوه بعدها", size=150))
b("وكان الاثر صغيرا جدا", da(value="أثر صغير", label="لكن فكرة مرعبة", size=160, color="coral"))
b("وانتقد كثيرون التجربه", sc("studio", [C("KRAMER", 0.5, "sad", "sad", 1, s=1.6)], cam=PUSH, labels=[L("آدم كرامر — اعتذار", y=0.18, box=True)]))
b("ولسنا وحدنا من يقرا", ins("dogfaces", label="17 كلبًا — 2016"))
b("فكانت الكلاب تنظر", ins("dogfaces", voice="angry", cam=IN))
b("ولكن حساسيتها لوجوه", da(value="🐕 > 🧑", label="أدق مع وجوه الكلاب", size=170))
b("والادب جعل التعاطف", sc("archive", [C("PKD", 0.5, "holdFront", "thinking", 1, prop="paper", s=1.6)], cam=PUSH, labels=[L("فيليب ك. ديك — 1968", y=0.18, box=True)]))
b("لان الروبوتات تستطيع", da(value="اختبار التعاطف", label="يكشف الروبوت المتنكر", size=140))
b("ويملك البشر فيها صندوقا", ins("empathybox", label="صندوق التعاطف"))
b("في تلك الروايه الانسان", bl("الإنسان هو من يشعر بغيره", "archive"), cap=False)
b("والان الى العلم", bl("كيف يشعر الدماغ بغيره؟", "archive"), cap=False, music_cut="calm", in_=DIP)
b("في اوائل التسعينيات", sc("clinic", [C("RIZZO", 0.5, "explain", "smile", 1, s=1.6)], cam=PUSH, labels=[L("ريتسولاتي — بارما", y=0.18, box=True)]))
b("فلاحظوا خلايا عصبيه", ins("monkeymirror"))
b("ونشر وصفها الاول", da(value="1992 · 1996", label="الوصف الأول · التسمية", size=150))
b("وانتشرت الفكره بسرعه", da(value="+300", label="بحث في عام 2013 وحده", size=180))
b("وفي عام الفين وعشره سجل", da(value="21 مريضًا", label="UCLA — خلايا مرآتية في الإنسان", size=150))
b("وهنا يبدا الخلاف العلمي", bl("خلاف علمي", "archive", coral=True), cap=False)
b("في عام الفين واربعه عشر نشر عالم", sc("studio", [C("HICKOK", 0.5, "crossArms", "thinking", 1, s=1.6)], cam=PUSH, labels=[L("غريغوري هيكوك — 2014", y=0.18, box=True)]))
b("وقال ان كثيرا من", ins("news", head="خرافة الخلايا المرآتية؟", who="HICKOK"))
b("ودافع عنها اخرون", st("studio", [C("HICKOK", 0.35, "explain", "angry", 1), C("RIZZO", 0.65, "explain", "determined", -1)], cam=PUSH, labels=[L("مناظرة نيويورك — 2015", y=0.18, box=True)]))
b("وحتى ريتسولاتي نفسه", fc("RIZZO", "clinic", "thinking", side=0.3, rimSide=1))
b("فالجواب الصادق اليوم", da(icon="brain", value="؟", label="آلية التعاطف لم تُحسم", size=180))
b("والان الى ما وعدتك به", bl("الجواب الموعود", "archive"), cap=False, in_=DIP, sfx=[SFX("stinger", 0.1, -10)], music_cut="hopeful")
b("الجواب مختبئ في التجربه", st("studio", [C("SINGER", 0.5, "explain", "smile", 1, s=1.6)], cam=PUSH))
b("فانعكست زياده المشاعر", ins("emoaura", warm=True, youExpr="smile", otherExpr="smile"))
b("واقترح الباحثون ان الرحمه", da(value="الرحمة", label="تحمي من ضيق التعاطف", size=170))
b("هذا هو الفرق الصغير", bl("التعاطف: أن تشعر… الرحمة: أن تمدّ يدك", "archive", size=64), cap=False, sfx=[SFX("impact", 0.2, -10)])
b("ساليناس لم يهرب", sc("clinic", [C("SALINAS", 0.4, "explain", "smile", 1), C("PLAIN", 0.6, "sit", "smile", -1, chair=True)], cam=PULL))
b("فربما لا يكون السؤال", fc("YOU", "home", "thinking", side=0.0))
b("فصديقك ادم لا يحتاج", st("classroom", [C("YOU", 0.4, "stand", "smile", 1, s=1.5), C("ADAM", 0.62, "stand", "sad", -1, s=1.5)], cam=PULL, labels=[L("«هل أنت بخير فعلًا؟»", y=0.18, box=True)]))
b("وفي الحلقه القادمه", bl("ماذا لو لم تنسَ وجهًا رأيته أبدًا؟", "archive", str2="الحلقة القادمة", at2=0.8), cap=False, sfx=[SFX("riser", 0, -12)])
b("والان سؤال الحلقه", dict(tpl="endscreen", q="لو خُيّرت: تشعر بكل من حولك… حتى أحزانهم المخفية؟", cast=["SALINAS", "SINGER", "YOU", "ADAM", "HICKOK", "PKD"]), in_=FADE, cap=False)

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
    if d > 4.5 and tpl in ("stage", "insert", "archive", "data"):
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
story = {"title": "ماذا لو شعرت بمشاعر كل من حولك؟", "duration": DUR, "shots": shots, "music": music, "sfx": []}
json.dump(story, open(f"{PROJ}/story/shots.json", "w"), ensure_ascii=False, indent=1)
d = [s["end"] - s["start"] for s in shots]; d.sort()
print(len(shots), "shots; median", round(d[len(d) // 2], 2), "min", round(d[0], 2), "max", round(d[-1], 2))
print("music:", [(m["mood"], round(m["start"]), round(m["end"])) for m in music])
