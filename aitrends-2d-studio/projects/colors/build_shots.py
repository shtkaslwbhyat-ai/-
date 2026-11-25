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
b("الحافله صباح الاحد", dict(tpl="title", lines=["ماذا لو", "سمعت الألوان؟"]), bars="scope", cap=False, sfx=[SFX("riser", 0, -12)])
b("تضع السماعتين في اذنيك", ins("busmusic", on=99))
b("ومع اول نغمه", ins("busmusic", on=0.3), sfx=[SFX("shimmer", 0.2, -10)])
b("لا احد غيرك يراها", ins("busmusic", on=0, cam=IN))
b("ماذا لو سمعت الالوان", bl("ماذا لو سمعت الألوان؟", "archive", size=76), cap=False, sfx=[SFX("stinger", 0.1, -10)])
b("كل صوت يصل الى اذنك", da(value="🥁 🎻 😂", label="برتقالي · أزرق · ذهبي", size=130))
b("في الفصل تقول المعلمه", st("classroom", [C("YOU", 0.4, "sit", "smile", 1, chair=True, s=1.4), C("TEACHER", 0.65, "explain", "neutral", -1, s=1.4)], cam=PUSH, labels=[L("7 ألوان = رقم", y=0.18, box=True)]))
b("يسالك زميلك كيف", st("classroom", [C("YOU", 0.4, "talk", "smile", 1, s=1.5), C("ADAM", 0.62, "stand", "confused", -1, s=1.5)], cam=PUSH, labels=[L("«أخضر وأحمر… سهل!»", y=0.18, box=True)]))
b("لكن في طريق العوده", ins("sirenred", label="صفارة واحدة… والطريق أحمر"), music_cut="tension")
b("هذا خيال لكن هناك", ins("antenna"))
b("وفي اخر هذه الحلقه ستعرف", bl("في آخر الحلقة: شيء نسي الدماغ أن يحذفه", "archive", coral=True, size=66), cap=False)
b("اسمه نيل هاربيسون", sc("studio", [C("HARBISSON", 0.5, "stand", "smile", 1, s=1.7)], cam=PUSH, labels=[L("نيل هاربيسون", y=0.18, ap="نيل", box=True)]), in_=DIP, music_cut="calm")
b("العالم كله عنده رمادي", da(value="⚫ ⚪", label="اللالونية: عالم رمادي", size=170))
b("وفي عام الفين وثلاثه طور", da(value="2003 · 2004", label="الفكرة · زرع الهوائي", size=150))
b("تلتقط هذه العين لون", ins("antenna", label="كل لون = نغمة"))
b("صار هاربيسون يسمع ما لا يراه", ins("antenna", cam=IN))
b("وتقول التقارير ان الهوائي", da(value="تحت الأحمر · فوق البنفسجي", label="ألوان لا تراها أعيننا", size=110))
b("الرجل الذي لا يرى", fc("HARBISSON", "studio", "smile", side=0.3, rimSide=1))
b("وحين جاء وقت تجديد", ins("news", head="الهوائي في صورة الجواز", who="HARBISSON"))
b("وتسجله موسوعه غينيس", ins("medal"), sfx=[SFX("shimmer", 0.2, -10)])
b("وفي عام الفين وعشره اسس", da(value="برشلونة 2010", label="مؤسسة السايبورغ — مع مون ريباس", size=130))
b("واذا اعجبتك هذه القصه", ins("likesub", label="أعجبتك القصة؟"), sfx=[SFX("pop", 0.3, -10)])
b("لكن هاربيسون اختار", st("home", [C("YOU", 0.5, "think", "thinking", 1, s=1.6)], cam=PUSH))
b("في عام الفين وسته فحصت", sc("clinic", [C("SIMNER", 0.5, "holdFront", "thinking", 1, prop="paper", s=1.5)], cam=PUSH, labels=[L("جوليا سيمنر — 2006", y=0.18, box=True)]))
b("فوجدوا ان نحو اربعه", da(value="4.4%", label="عندهم تداخل حواس", size=190))
b("والمفاجئ ان اشهر نوع", ins("weekcolors", label="أيام الأسبوع ملونة"))
b("اما رؤيه الحروف والارقام", da(value="≈ 1%", label="يرون الحروف والأرقام ملونة", size=180))
b("اي ان واحدا من كل ثلاثين", st("city", [C("PLAIN", 0.3, "stand", "neutral", 1), C("PLAIN", 0.5, "stand", "awe", 1), C("PLAIN", 0.7, "stand", "neutral", -1)], so=dict(mood="day"), cam=DRIFT, labels=[L("1 من 30", y=0.18, box=True)]))
b("وهنا تبدا المشكله", bl("وهنا تبدأ المشكلة", "archive", coral=True), cap=False, music_cut="tension")
b("كان الروائي الشهير", sc("archive", [C("NABOKOV", 0.5, "stand", "neutral", 1, s=1.7)], cam=PUSH, labels=[L("فلاديمير نابوكوف", y=0.18, box=True)]))
b("ويروي في سيرته الذاتيه", ins("letterblocks", label="«ألوانها كلها خطأ!»"))
b("واكتشف يومها ان امه", sc("home", [C("YOUKID", 0.4, "stand", "surprised", 1, s=1.4), C("NABOMOM", 0.62, "stand", "smile", -1, s=1.5)], cam=PUSH))
b("ثم اكتشف لاحقا ان ابنه", da(value="3 أجيال", label="الجدة · الأب · الابن", size=170))
b("لكن العجيب ان الوانهم", ins("letterblocks", at=0.3))
b("واللون الخطا ليس مزعجا", st("studio", [C("LAB", 0.5, "holdFront", "thinking", 1, prop="paper", s=1.5)], cam=PUSH, labels=[L("ديكسون وزملاؤه — 2000", y=0.18, box=True)]))
b("درسوا امراه يظهر لها", ins("fiveplustwo", red=False, label="7 عندها أصفر"))
b("حين كانت البقعه صفراء", ins("fiveplustwo", red=False))
b("وحين كانت حمراء", ins("fiveplustwo", red=True, slow="⏱ +236 جزءًا من الألف"))
b("فالجواب في راسها كان", fc("PLAIN", "studio", "confused", side=0.3, rimSide=1))
b("والان تخيل هذا في كل", ins("sirenred"))
b("والان الى العلم والى", bl("العلم… والمفاجأة الكبرى", "archive"), cap=False, music_cut="calm", in_=DIP)
b("في عام الفين وواحد اقترح", sc("clinic", [C("RAMA", 0.5, "explain", "smile", 1, s=1.6)], cam=PUSH, labels=[L("راماتشاندران وهبارد — 2001", y=0.18, box=True)]))
b("في الدماغ منطقه تعالج", ins("ffa", icons=["🎨", "5"], label="منطقتان متجاورتان"))
b("وصمما اختبارا ذكيا", ins("popout", at=99, label="أين المثلث؟"))
b("اما صاحب الحواس المتداخله", ins("popout", at=0.3, label="يراه فورًا تقريبًا"))
b("ولكن هذا التفسير ما زال", da(value="فرضية", label="والجدل مستمر", size=180, color="coral"))
b("وهنا تاتي الفكره الاغرب", sc("clinic", [C("MAURER", 0.5, "explain", "thinking", 1, s=1.6)], cam=PUSH, labels=[L("دافني ماورر", y=0.18, box=True)]), music_cut="tension")
b("ثم يبدا الدماغ مع الخبره", ins("pruning", pruned=True, label="تقليم الوصلات"))
b("وفي عام الفين وعشرين نشر", da(value="2020", label="تقليم لم يكتمل؟", size=180))
b("لكن مراجعات علميه اخرى", da(value="خلاف علمي", label="هل الرضّع متداخلو الحواس؟", size=140, color="coral"))
b("وفي عام الفين وثلاثه عشر وجد", da(value="19% · 7%", label="مع التوحد · دونه (استبيان عبر الإنترنت)", size=150))
b("فان صحت الفكره", bl("ليست إضافة… بل شيء لم يُحذف", "archive"), cap=False, sfx=[SFX("impact", 0.2, -10)])
b("وحواسك المرتبه الهادئه", ins("pruning", pruned=True))
b("والان الى ما وعدتك به", bl("الجواب الموعود", "archive"), cap=False, in_=DIP, sfx=[SFX("stinger", 0.1, -10)], music_cut="hopeful")
b("هاربيسون وجد فيها", ins("antenna"))
b("لكن الدماغ الذي يخلط", ins("sirenred"))
b("والسر الذي وعدتك به", ins("pruning", pruned=False, label="بقية مما كنا عليه جميعًا"))
b("وفي اخر قصتنا تخفض", ins("busmusic", on=99))
b("وتعرف ان اجمل القدرات", fc("YOU", "home", "smile", side=0.0))
b("فالدماغ العادي ليس", da(icon="brain", value="أن يختار", label="الدماغ العادي ليس فقيرًا", size=150, count=2))
b("واذا استمتعت بهذه القصه", ins("likesub", label="لا تنسَ: إعجاب + اشتراك + 🔔"), sfx=[SFX("pop", 0.3, -10)])
b("وفي الحلقه القادمه", bl("ماذا لو لم تشعر بالخوف أبدًا؟", "archive", str2="الحلقة القادمة", at2=0.8), cap=False, sfx=[SFX("riser", 0, -12)])
b("والان سؤال الحلقه", dict(tpl="endscreen", q="لو خُيّرت: تسمع الألوان… وكل صوت يرسم فوق عينيك؟", cast=["HARBISSON", "NABOKOV", "YOU", "RAMA", "MAURER", "SIMNER"]), in_=FADE, cap=False)

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
story = {"title": "ماذا لو سمعت الألوان؟", "duration": DUR, "shots": shots, "music": music, "sfx": []}
json.dump(story, open(f"{PROJ}/story/shots.json", "w"), ensure_ascii=False, indent=1)
d = [s["end"] - s["start"] for s in shots]; d.sort()
print(len(shots), "shots; median", round(d[len(d) // 2], 2), "min", round(d[0], 2), "max", round(d[-1], 2))
print("music:", [(m["mood"], round(m["start"]), round(m["end"])) for m in music])
