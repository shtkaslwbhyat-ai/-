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
b("ماذا لو استطعت حبس انفاسك", dict(tpl="title", lines=["ماذا لو", "استطعت حبس أنفاسك ساعة كاملة؟"]), bars="scope", cap=False, sfx=[SFX("riser", 0, -12)])
b("تنزل الى قاع البحر", ins("underwater"))
b("وتصعد بعد ستين دقيقه", ins("pool", who="YOU", from_=0, to=3600, label="60 دقيقة… بلا نفس"))
b("اغلب البالغين يصمدون", st("home", [C("YOU", 0.5, "stand", "shocked", 1, s=1.6)], cam=PUSH, labels=[L("30–90 ثانية", y=0.18, box=True)]))
b("لكن رجلا حقيقيا بقي", ins("pool", who="DIVER", from_=0, to=1743, red=1500, label="رجل حقيقي"), sfx=[SFX("stinger", 0.1, -10)])
b("وحيوان اخر في المحيط", ins("whale", to=3, unit=" ساعات+", label="حيوان حقيقي"))
b("وفي اخر هذه الحلقه ستعرف", bl("في آخر الحلقة: هل يصل إنسان إلى الساعة؟", "archive", coral=True, size=70), cap=False)
b("ولماذا يكون الاحساس", ins("co2", label="الإحساس الذي تكرهه"))
b("اسمه فيتومير", sc("studio", [C("DIVER", 0.5, "stand", "determined", 1, s=1.7)], cam=PUSH, labels=[L("فيتومير ماريتشيتش — كرواتيا", y=0.18, ap="فيتومير", box=True)]), in_=DIP, music_cut="tension")
b("في الرابع عشر من يونيو", da(value="14 يونيو 2025", label="أوباتيا — حوض بعمق 3 أمتار", size=130))
b("امامه خمسه حكام", sc("audience", [C("DIVER", 0.5, "stand", "determined", 1)], cam=PULL) if False else sc("studio", [C("DIVER", 0.3, "stand", "determined", 1), C("PLAIN", 0.55, "sit", "neutral", -1, chair=True), C("PLAIN", 0.7, "sit", "neutral", -1, chair=True), C("PLAIN", 0.85, "sit", "neutral", -1, chair=True)], cam=PUSH, labels=[L("5 حكام · 100 متفرج", y=0.18, box=True)]))
b("تنفس اكسجينا نقيا", ins("tank", label="10 دقائق من الأكسجين النقي"))
b("ثم نزل الى القاع", ins("pool", who="DIVER", from_=0, to=300))
b("مرت خمس دقائق", ins("pool", who="DIVER", from_=300, to=900, cam=IN))
b("الجمهور ينظر الى الساعه", st("studio", [C("PLAIN", 0.35, "stand", "shocked", 1), C("PLAIN", 0.6, "handsOnHead", "awe", -1)], cam=PUSH))
b("عشرون دقيقه", ins("pool", who="DIVER", from_=1200, to=1500, red=1500))
b("وحين خرج اخيرا", ins("pool", who="DIVER", from_=1730, to=1743, red=1500, label="29:03"), sfx=[SFX("impact", 0.3, -10)])
b("رقم قياسي جديد", ins("medal"), sfx=[SFX("shimmer", 0.2, -10)])
b("وكان الرقم السابق", sc("studio", [C("SOBAT", 0.5, "stand", "smile", 1, s=1.7)], cam=PUSH, labels=[L("بوديمير شوبات — 2021", y=0.18, ap="بوديمير", box=True)]))
b("ووصفته موسوعه غينيس", da(value="24:37", label="في السادسة والخمسين", size=170))
b("اي ان البشر قطعوا", ins("clock24") if False else da(value="نصف الطريق", label="إلى الساعة الكاملة", size=130))
b("وقبله بسنوات", da(value="29:03", label="بعد أن كان 16:32 عام 2008", size=130))
b("هنا المفاجاه الاولى", bl("المفاجأة الأولى", "archive"), cap=False, in_=DIP, music_cut="calm")
b("هذه الارقام لم تصنع", bl("ليس بالهواء العادي", "archive", coral=True), cap=False)
b("قواعد هذا الرقم تسمح", ins("tank", label="قواعد غينيس تسمح بالأكسجين"))
b("اما بنفس عادي", da(value="11:35", label="بالهواء فقط — ستيفان ميفسود", size=170))
b("وحتى ماريتشيتش نفسه", sc("studio", [C("DIVER", 0.5, "shrug", "neutral", 1, s=1.6)], cam=PUSH, labels=[L("بالهواء وحده: نحو 10 دقائق", y=0.18, ap="تقول", box=True)]))
b("يعني ان اعظم الغواصين", da(value="خُمس الساعة", label="أقصى ما بلغه البشر بالهواء", size=130, color="coral"))
b("والسبب ليس ضعف الاراده", da(value="لا مخزن", label="الجسم لا يخزّن الأكسجين", size=160))
b("وفي احدى الدراسات", da(value="≈ 300 مل", label="أكسجين كل دقيقة… حتى وأنت تحبس نفسك", size=150))
b("وحتى الاكسجين النقي", sc("clinic", [C("DOC", 0.5, "explain", "worried", 1, s=1.5)], cam=PUSH, labels=[L("تحت إشراف صارم", y=0.18, box=True)]))
b("اما المفاجاه الثانيه", bl("المفاجأة الثانية", "archive"), cap=False, music_cut="tension")
b("هل تعرف لماذا تشعر", st("home", [C("YOU", 0.5, "handsOnHead", "worried", 1, s=1.6)], cam=PUSH))
b("لكن التفسير المعتمد", ins("co2", label="ثاني أكسيد الكربون"))
b("وبعض الناس يتنفسون", st("seacafe", [C("YOU", 0.5, "stand", "determined", 1, s=1.4)], cam=PUSH, labels=[L("تنفّس سريع قبل الغوص", y=0.18, box=True)]))
b("هذا يخرج ثاني اكسيد", ins("co2", quiet=True, label="لا تحذير"))
b("فيفقد الغواص وعيه", ins("blackout", label="إغماء بلا تحذير"), sfx=[SFX("hit", 0.3, -10)])
b("فقط ظلام مفاجئ", ins("blackout", cam=IN))
b("ولهذا يحذر الصليب الاحمر", da(value="⚠️", label="لا تغُص بعد تنفّس سريع", size=170, color="coral"))
b("ولهذه الرياضه ثمن", bl("الثمن الإنساني", "archive"), cap=False, music_cut="sad")
b("ناتاليا مولتشانوفا", sc("seacafe", [C("NATALIA", 0.5, "stand", "smile", 1, s=1.7)], cam=PUSH, labels=[L("ناتاليا مولتشانوفا", y=0.18, ap="ناتاليا", box=True)]))
b("حطمت اكثر من اربعين", da(value="+40", label="رقما قياسيا عالميا", size=180))
b("وفي الثاني من اغسطس", da(value="2 أغسطس 2015", label="قرب فورمنتيرا — إسبانيا", size=130))
b("ولم تصعد", ins("underwater", fade=True) if False else bl("…ولم تصعد", "archive", coral=True), cap=False, sfx=[SFX("impact", 0.2, -12)])
b("بحثوا عنها اياما", st("seacafe", [C("PLAIN", 0.4, "stand", "sad", 1), C("PLAIN", 0.6, "stand", "worried", -1)], so=dict(mood="dusk"), cam=PULL, labels=[L("ابنها أليكسي شارك في البحث", y=0.18, ap="ابنها", box=True)]))
b("وبعد ثلاثه ايام", da(value="لم يُعثر عليها", label="حتى اليوم", size=140, color="coral"))
b("اعظم رئتين عرفتهما", fc("NATALIA", "seacafe", "sad", side=0.3, rimSide=1))
b("وقبل ماريتشيتش بسنوات", ins("news", head="ساحر يحبس أنفاسه على الهواء", who="BLAINE"), music_cut="hopeful", in_=DIP)
b("في الثلاثين من ابريل", ins("sphere", label="ديفيد بلين — 2008"))
b("تنفس الاكسجين النقي ثلاثا", da(value="17:04", label="بعد 23 دقيقة من الأكسجين", size=170))
b("وبعد اربع سنوات", da(value="22 دقيقة", label="ستيغ سيفيرينسن — ماء شديد البرودة", size=150))
b("ولكن اغرب القصص", ins("underwater"))
b("في جنوب شرق اسيا", st("seacafe", [C("BAJAU", 0.5, "stand", "smile", 1, s=1.6)], cam=PUSH, labels=[L("الباجاو — بدو البحر", y=0.18, box=True)]))
b("وفي عام الفين وثمانيه عشر", sc("clinic", [C("LAB", 0.5, "holdFront", "determined", 1, prop="paper", s=1.5)], cam=PUSH, labels=[L("دراسة Cell — 2018", y=0.18, box=True)]) if False else st("clinic", [C("DRWOMAN", 0.5, "holdFront", "determined", 1, prop="paper", s=1.5)], cam=PUSH, labels=[L("ميليسا إيلاردو — Cell 2018", y=0.18, box=True)]))
b("فحصوا الباجاو بالموجات", ins("bodymap", spots=[[120, -40, "طحال أكبر 50%", 0.3]]))
b("والاغرب ان هذا الفرق", da(value="PDE10A", label="جين مرتبط بالطحال الكبير", size=150))
b("فالطحال يعمل مثل", ins("bloodbag"))
b("ومع ذلك يقول علماء", da(value="عينة صغيرة", label="تحتاج دراسات أوسع", size=140, color="coral"))
b("وفي اليابان تعيش", st("seacafe", [C("AMA", 0.5, "stand", "determined", 1, s=1.6)], cam=PUSH, labels=[L("الأما — اليابان", y=0.18, box=True)]))
b("ولم يكن يطلبن", ins("underwater", cam=IN))
b("وتشير المصادر الى انه", da(value="17 ألفًا … ألفان", label="غواصات الأما عام 1956… واليوم", size=130))
b("مهنه عاشت الاف", fc("AMA", "seacafe", "sad", side=0.3, rimSide=1))
b("والان الى العلم", bl("العلم", "archive"), cap=False, music_cut="calm", in_=DIP)
b("اغمس وجهك في ماء", ins("icewater"))
b("سيتباطا قلبك", ins("heart"))
b("يبطؤ قلب الانسان", da(value="−10 إلى −25%", label="نبض القلب", size=140))
b("ليذهب الاكسجين الى", ins("bodymap", spots=[[0, -260, "الدماغ", 0.3], [0, -120, "القلب", 0.8]]) if False else ins("bodymap", spots=[[0, -200, "القلب والدماغ أولا", 0.3]]))
b("ويبلغ هذا الاثر", st("home", [C("YOU", 0.5, "stand", "surprised", 1, s=1.6)], cam=PUSH, labels=[L("الوجه… لا اليدين", y=0.18, box=True)]))
b("انه اثر قديم", ins("whale", to=80, unit="%", label="أقوى بكثير عند الحيتان والفقمات"))
b("فقلب الثدييات البحريه", da(value="−80%", label="نبض الثدييات البحرية", size=170))
b("والفقمه لا تعتمد", da(value="5%", label="فقط من أكسجين فقمة ويدل في رئتيها", size=170))
b("اما بطل العالم الحقيقي", ins("whale", to=222, label="حوت كوفييه ذو المنقار"), music_cut="hopeful")
b("اكثر من ثلاث ساعات", bl("أكثر من 3 ساعات ونصف… بنفس واحد", "archive"), cap=False, sfx=[SFX("shimmer", 0.2, -10)])
b("واستمرت الدراسه خمس", da(value="23 حوتا", label="5 سنوات · آلاف الغوصات", size=150))
b("وكان نصف غوصات", ins("whale", to=59, label="نصف غوصاتها أطول من هذا"))
b("وهنا يختلف العلماء", bl("خلاف علمي", "archive", coral=True), cap=False)
b("التفسير الشائع يقول", ins("co2"))
b("لكن بعض الابحاث", ins("bodymap", spots=[[0, -60, "الحجاب الحاجز", 0.3]]))
b("والجواب الدقيق", da(icon="brain", value="؟", label="ما زال موضع بحث", size=180))
b("والان الى ما وعدتك به", bl("الجواب الموعود", "archive"), cap=False, in_=DIP, sfx=[SFX("stinger", 0.1, -10)])
b("هل يستطيع انسان ان يحبس", st("home", [C("YOU", 0.5, "think", "thinking", 1, s=1.6)], cam=PUSH))
b("الجواب الصادق", bl("لم يفعلها أحد قط", "archive", coral=True), cap=False)
b("حتى بالاكسجين النقي اطول", da(value="29:03 / 11:35", label="بالأكسجين / بالهواء", size=130))
b("فالدماغ عضو جائع", da(icon="brain", value="الدماغ", label="عضو جائع للأكسجين", size=130, count=2))
b("ويذكر مرجع طبي", da(value="10–30 ثانية", label="ويختفي نشاط سطح الدماغ دون دم", size=150, color="coral"))
b("والغواصون الكبار لا", ins("pool", who="DIVER", from_=600, to=640, expr="neutral"))
b("الساعه الكامله تنتمي", ins("whale", to=60, label="الساعة للحيتان… لا لنا"))
b("لكن تذكر ذلك الاحساس", ins("co2", label="الحريق في صدرك"), music_cut="hopeful")
b("هذا الاحساس ليس عدوك", bl("إنه حارسك", "archive"), cap=False, sfx=[SFX("impact", 0.2, -10)])
b("والغواصون الذين اسكتوه", ins("blackout"))
b("فلو اعطاك احد", st("home", [C("YOU", 0.5, "stand", "determined", 1, s=1.6)], cam=PULL))
b("فاحيانا يكون اكثر", fc("YOU", "home", "smile", side=0.0))
b("وفي الحلقه القادمه", bl("ماذا لو كان كل يوم من عمرك يساوي عاما؟", "archive", str2="الحلقة القادمة", at2=0.8), cap=False, sfx=[SFX("riser", 0, -12)])
b("والان سؤال الحلقه", dict(tpl="endscreen", q="لو خُيّرت: ساعة بلا نفس… مقابل أن يسكت جسدك عن تحذيرك؟", cast=["DIVER", "NATALIA", "BLAINE", "YOU", "BAJAU", "AMA"]), in_=FADE, cap=False)

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
story = {"title": "ماذا لو استطعت حبس أنفاسك ساعة كاملة؟", "duration": DUR, "shots": shots, "music": music, "sfx": []}
json.dump(story, open(f"{PROJ}/story/shots.json", "w"), ensure_ascii=False, indent=1)
d = [s["end"] - s["start"] for s in shots]; d.sort()
print(len(shots), "shots; median", round(d[len(d) // 2], 2), "min", round(d[0], 2), "max", round(d[-1], 2))
print("music:", [(m["mood"], round(m["start"]), round(m["end"])) for m in music])
