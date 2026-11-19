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
b("مطبخ بيتكم صباح", dict(tpl="title", lines=["ماذا لو", "كان رد فعلك أسرع بمئة مرة؟"]), bars="scope", cap=False, sfx=[SFX("riser", 0, -12)])
b("ينزلق كوب الشاي", ins("cupfreeze", fall=True))
b("وفجاه يتوقف في الهواء", ins("cupfreeze"), sfx=[SFX("shimmer", 0.1, -10)])
b("انت وحدك تتحرك", ins("cupfreeze", hand=True, cam=IN))
b("ماذا لو كان رد فعلك", bl("ماذا لو كان رد فعلك أسرع بمئة مرة؟", "archive", size=70), cap=False, sfx=[SFX("stinger", 0.1, -10)])
b("العالم لم يتوقف", st("home", [C("YOU", 0.4, "stand", "awe", 1, s=1.5), C("SALMA", 0.62, "stand", "surprised", -1, s=1.5)], cam=PUSH))
b("كل ثانيه عند الناس", da(value="1 ث = 1:40", label="ثانيتهم… ودقيقتك ونصف", size=150))
b("تناول اختك الكوب", st("home", [C("SALMA", 0.55, "talk", "smile", -1, s=1.7)], cam=PUSH, labels=[L("شُكْ…رًا", y=0.18, box=True)]))
b("تضحك ثم تذهب", st("classroom", [C("YOU", 0.5, "sit", "neutral", 1, chair=True, s=1.4)], cam=PUSH))
b("خمس واربعون دقيقه", da(value="45 دقيقة = 3 أيام", label="الحصة الأولى… عندك", size=130, color="coral"))
b("لا تضحك هذه المره", fc("YOU", "classroom", "sad", side=0.0))
b("هذا خيال لكن هناك", ins("track", who=["BOLT", "PLAIN", "PLAIN", "PLAIN"], go=99))
b("وفي اخر هذه الحلقه ستعرف", bl("في آخر الحلقة: هل الأسرع هو الأقوى؟", "archive", coral=True, size=70), cap=False)
b("برلين السادس عشر", da(value="16 أغسطس 2009", label="برلين — نهائي 100 متر", size=130), in_=DIP, music_cut="tension")
b("ثمانيه عدائين على خط", ins("track", who=["GAY", "BOLT", "POWELL", "PLAIN"], go=99, label="يوسين بولت"))
b("ينطلق المسدس", ins("track", who=["GAY", "BOLT", "POWELL", "PLAIN"], go=0.3, lead=1), sfx=[SFX("hit", 0.2, -8)])
b("رقم قياسي عالمي ما زال", da(value="9.58", label="رقم عالمي ما زال صامدا", size=200), sfx=[SFX("shimmer", 0.2, -10)])
b("لكن في النتائج الرسميه", ins("blocks", ms=146, label="رد فعل بولت"))
b("اما منافساه تايسون", da(value="0.134 · 0.144 · 0.146", label="باول · غاي · بولت", size=110))
b("ووصفت مراجعه الاتحاد", da(value="السادس", label="أسرع انطلاقة… فقط", size=170))
b("اسرع رجل في التاريخ لم", sc("pitch", [C("BOLT", 0.5, "cheer", "smile", 1, s=1.6)], cam=PULL))
b("وفي نصف النهائي قبلها", ins("blocks", ms=135, label="نصف النهائي"))
b("وهنا المفاجاه الاولى", bl("المفاجأة الأولى", "archive"), cap=False, in_=DIP, music_cut="calm")
b("لو حسبت زمن رد الفعل", da(value="1.5%", label="من زمن السباق فقط", size=190))
b("بولت لم يفز لانه سمع", ins("track", who=["GAY", "BOLT", "POWELL", "PLAIN"], go=0.0, lead=1))
b("فلو كان رد فعلك اسرع", ins("track", who=["PLAIN", "YOU", "PLAIN", "PLAIN"], go=0.0, lead=1, label="تربح البداية فقط"))
b("رد الفعل يحدد متى", bl("رد الفعل = متى تبدأ… لا من يصل", "archive", size=68), cap=False)
b("اما المفاجاه الثانيه", bl("المفاجأة الثانية", "archive"), cap=False, music_cut="tension")
b("بعد عامين في الثامن", da(value="28 أغسطس 2011", label="دايغو — كوريا", size=130))
b("ومنذ موسم الفين وعشره", da(value="خطأ واحد = إقصاء", label="القانون منذ 2010", size=130, color="coral"))
b("وقبل صوت المسدس تحرك", ins("track", who=["BLAKE", "BOLT", "PLAIN", "PLAIN"], go=1.0, lead=1))
b("اقصي في الحال", ins("blocks", ms=0, bad=True, badText="إقصاء!"), sfx=[SFX("impact", 0.1, -8)])
b("وتقول التقارير انه خلع", sc("pitch", [C("BOLT", 0.4, "handsOnHead", "angry", 1, s=1.5), C("BLAKE", 0.65, "cheer", "smile", -1, s=1.4)], cam=PUSH))
b("وقال بولت في بيانه", fc("BOLT", "pitch", "sad", side=0.3, rimSide=1), music_cut="sad")
b("وهنا السؤال المخيف", st("studio", [C("PLAIN", 0.5, "think", "thinking", 1, s=1.5)], cam=PUSH))
b("القانون يعد كل عداء", ins("blocks", ms=99, bad=True, label="قبل 0.100 = مخالف"))
b("لكن هذا الحد قام على", da(value="8 عدائين", label="دراسة التسعينيات — فنلندا", size=160))
b("وفي عام الفين وتسعه اوصت", da(value="0.080–0.085", label="توصية 2009", size=140))
b("وانتقدت مراجعات علميه", ar(hero=True, heroC="PLAIN", pose="think", expr="thinking", n=40, cards=["0.080؟", "0.100؟", "0.115؟"], cardsX=[0.2, 0.5, 0.8], cardsY=[0.25, 0.18, 0.25], gap=0.6))
b("فالعلماء انفسهم", da(icon="brain", value="؟", label="أسرع رد فعل ممكن للإنسان", size=180))
b("فلو كان رد فعلك اسرع بمئه مره لاقصيت", ins("blocks", ms=2, bad=True, badText="إقصاء… دائما"))
b("وفي الطبيعه مخلوقات", ins("fly"), in_=DIP, music_cut="calm")
b("في عام الفين وثلاثه عشر قارن", st("clinic", [C("HEALY", 0.5, "holdFront", "thinking", 1, prop="paper", s=1.5)], cam=PUSH, labels=[L("كيفن هيلي — دبلن 2013", y=0.18, box=True)]))
b("فوجدوا ان عيون عده", da(value="×4+", label="عين الذبابة أسرع من عينك", size=180))
b("يدك التي تهوي عليها", ins("fly", label="يدك… بالحركة البطيئة"))
b("ويرى الباحثون ان الحيوانات", da(value="جسم صغير = زمن أبطأ", label="معلومات أكثر في كل ثانية", size=110))
b("وعلى الطرف الاخر وجدوا", da(value="4 ومضات/ث", label="قشريات أعماق البحر", size=150))
b("اما روبيان السرعوف", ins("mantis", label="روبيان السرعوف"))
b("فوجدت ان ذراعه", da(value="23 م/ث", label="في أقل من 0.003 ثانية", size=170))
b("ضربه سريعه جدا", ins("mantis", cam=IN))
b("والادب سبق العلم", sc("archive", [C("WELLS", 0.5, "holdFront", "smile", 1, prop="paper", s=1.6)], cam=PUSH, labels=[L("هـ. ج. ويلز — 1901", y=0.18, box=True)]))
b("عن دواء يسرع", st("city", [C("YOU", 0.5, "stand", "awe", 1, s=1.3), C("PLAIN", 0.3, "stand", "neutral", 1), C("PLAIN", 0.72, "stand", "neutral", -1)], so=dict(mood="day"), cam=DRIFT, labels=[L("المسرّع الجديد", y=0.18, box=True)]))
b("والان الى العلم", bl("العلم", "archive"), cap=False, music_cut="calm", in_=DIP)
b("يلتقط المشهد عينك", da(value="عين ← دماغ ← عضلة", label="رحلة رد الفعل", size=130))
b("وتقول الدراسات الكلاسيكيه", da(value="0.18–0.20", label="رد الفعل على الضوء", size=160))
b("اما على الصوت فاسرع", da(value="0.14–0.16", label="على الصوت… أسرع", size=160))
b("ولهذا تبدا السباقات", ins("blocks", ms=150, label="لهذا: مسدس لا ضوء"))
b("والاعصاب نفسها لها", da(value="120 م/ث", label="أسرع الألياف العصبية", size=170))
b("اما الالياف الرقيقه", da(value="0.5–2 م/ث", label="الألياف الرقيقة", size=160, color="coral"))
b("اي ان رد الفعل الاسرع", st("home", [C("YOU", 0.5, "shrug", "confused", 1, s=1.6)], cam=PUSH))
b("وفي رياضه البيسبول", ins("baseball", label="الكرة السريعة"))
b("فكيف يضربونها", ins("baseball", label="الضارب يتوقع قبل أن يرى", cam=IN))
b("وهنا خلاف علمي ممتع", bl("خلاف علمي: هل يتباطأ الزمن في الخطر؟", "archive", coral=True, size=66), cap=False)
b("في عام الفين وسبعه اختبر", st("studio", [C("EAGLEMAN", 0.5, "explain", "smile", 1, s=1.6)], cam=PUSH, labels=[L("ديفيد إيغلمان — 2007", y=0.18, box=True)]))
b("سقوط حر من ارتفاع", ins("freefall"))
b("لو تسارع الدماغ في الخوف", ins("freefall", label="لم يقرأ أحد الأرقام", cam=IN))
b("ومع ذلك قدروا مده", da(value="+36%", label="شعروا أن السقوط أطول", size=180))
b("واستنتج الفريق ان الخوف", da(icon="brain", value="الذاكرة", label="لا الإدراك: تفاصيل أكثر = لحظة أطول", size=120, count=2))
b("والان الى ما وعدتك به", bl("الجواب الموعود", "archive"), cap=False, in_=DIP, sfx=[SFX("stinger", 0.1, -10)], music_cut="hopeful")
b("هل كان رد الفعل الاسرع", st("home", [C("YOU", 0.5, "think", "thinking", 1, s=1.6)], cam=PUSH))
b("غالبا لا", bl("غالبًا… لا", "archive", coral=True), cap=False)
b("فاعصابك وعضلاتك لها", da(value="يوم = شهر", label="والحافلة = يوم كامل", size=150))
b("اما السر الذي يعتمد", bl("السر: التوقع والتدريب", "archive"), cap=False, sfx=[SFX("impact", 0.2, -10)])
b("بولت فاز برقمه", ins("track", who=["GAY", "BOLT", "POWELL", "PLAIN"], go=0.0, lead=1))
b("والضارب المحترف يضرب", ins("baseball"))
b("والمره الوحيده التي حاول", ins("blocks", ms=0, bad=True, badText="خسر اللقب"))
b("فالسرعه الحقيقيه ليست", fc("YOU", "home", "smile", side=0.0))
b("وفي الحلقه القادمه", bl("ماذا لو شعرت بمشاعر كل من حولك؟", "archive", str2="الحلقة القادمة", at2=0.8), cap=False, sfx=[SFX("riser", 0, -12)])
b("والان سؤال الحلقه", dict(tpl="endscreen", q="لو خُيّرت: رد فعل أسرع بمئة مرة… وكل يوم كأنه مئة يوم؟", cast=["BOLT", "BLAKE", "YOU", "SALMA", "EAGLEMAN", "WELLS"]), in_=FADE, cap=False)

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
story = {"title": "ماذا لو كان رد فعلك أسرع بمئة مرة؟", "duration": DUR, "shots": shots, "music": music, "sfx": []}
json.dump(story, open(f"{PROJ}/story/shots.json", "w"), ensure_ascii=False, indent=1)
d = [s["end"] - s["start"] for s in shots]; d.sort()
print(len(shots), "shots; median", round(d[len(d) // 2], 2), "min", round(d[0], 2), "max", round(d[-1], 2))
print("music:", [(m["mood"], round(m["start"]), round(m["end"])) for m in music])
