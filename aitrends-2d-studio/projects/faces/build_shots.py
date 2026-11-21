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
b("محطه القطار مساء", dict(tpl="title", lines=["ماذا لو", "لم تنسَ وجهًا رأيته أبدًا؟"]), bars="scope", cap=False, sfx=[SFX("riser", 0, -12)])
b("فجاه تتوقف عند وجه", ins("facegrid", hi=22, at=1.2))
b("تعرفه فورا انه", st("city", [C("YOU", 0.35, "stand", "awe", 1, s=1.4), C("PLAIN", 0.65, "stand", "neutral", -1, s=1.4)], so=dict(mood="dusk"), cam=PUSH))
b("انه الطفل الذي كان", st("classroom", [C("YOUKID", 0.4, "sit", "smile", 1, chair=True, s=1.4), C("KID2", 0.6, "sit", "smile", 1, chair=True, s=1.4)], cam=PUSH, labels=[L("قبل 20 عامًا", y=0.18, box=True)]))
b("لكنه لا يعرفك", st("city", [C("YOU", 0.35, "wave", "smile", 1, s=1.4), C("PLAIN", 0.65, "stand", "confused", -1, s=1.4)], so=dict(mood="dusk"), cam=PUSH))
b("ماذا لو لم تنس وجها", bl("ماذا لو لم تنسَ وجهًا رأيته أبدًا؟", "archive", size=68), cap=False, sfx=[SFX("stinger", 0.1, -10)])
b("كل وجه تراه ولو", da(value="ثانية = إلى الأبد", label="كل وجه تراه", size=130))
b("انت تتذكر لون حقيبته", fc("YOU", "city", "sad", side=0.0))
b("تقول للبائعه", st("bakery", [C("YOU", 0.38, "talk", "smile", 1, s=1.5), C("MOM", 0.62, "stand", "confused", -1, s=1.5)], cam=PUSH, labels=[L("«هل أعرفك؟»", y=0.18, box=True)]))
b("لكن في طريق العوده", st("city", [C("YOU", 0.3, "stand", "worried", 1, s=1.3), C("PLAIN", 0.75, "crossArms", "neutral", -1, s=1.1)], so=dict(mood="dusk"), cam=PUSH), music_cut="tension")
b("رايت وجهه امس", ins("facegrid", hi=13, at=0.3, label="الوجه نفسه… للمرة الرابعة"))
b("انت وحدك تعرف", fc("YOU", "city", "shocked", side=0.0))
b("هذا خيال لكن هناك", ins("cctv"))
b("وفي اخر هذه الحلقه ستعرف", bl("في آخر الحلقة: لماذا يُخفون أنهم تعرّفوا عليك؟", "archive", coral=True, size=64), cap=False)
b("لندن صيف عام", da(value="لندن 2011", label="أعمال شغب لعدة ليالٍ", size=170, color="coral"), in_=DIP)
b("وبعد ان هدات الشوارع", ins("cctv", label="آلاف الصور الضبابية"))
b("وجربت الشرطه برامج", sc("studio", [C("NEVILLE", 0.5, "shrug", "neutral", 1, s=1.6)], cam=PUSH, labels=[L("ميك نيفيل", y=0.18, box=True)]))
b("فقال المحقق ميك", da(value="1", label="مشتبه به واحد… تعرّف عليه البرنامج", size=200))
b("ثم جاء دور مجموعه", sc("studio", [C("COLLINS", 0.5, "stand", "determined", 1, s=1.7)], cam=PUSH, labels=[L("غاري كولينز — هاكني", y=0.18, ap="غاري", box=True)]), music_cut="calm")
b("جلس كولينز امام الصور", ins("cctv", count=180, label="تعرّف وحده"))
b("ومن بينهم رجل ملثم", ins("facegrid", hi=4, at=0.5, label="حتى الملثّمون"))
b("وتقول التقارير ان هذه", da(value="+600", label="مشتبه به — وصل ثلثاهم إلى المحاكم", size=180))
b("اي ان عيون بضعه رجال", da(value="1 ← 600", label="الآلة ← العيون", size=150))
b("ويقال ان كولينز تعرف", sc("city", [C("COLLINS", 0.5, "stand", "smile", 1, s=1.4)], so=dict(mood="day"), cam=DRIFT, labels=[L("+800 في مسيرته", y=0.18, box=True)]))
b("وفي مايو عام الفين وخمسه عشر", da(value="2015", label="وحدة فائقي التعرف — سكوتلاند يارد", size=170))
b("وفي عام الفين وثمانيه عشر بعد", ins("cctv", label="سالزبري 2018 — آلاف الساعات"))
b("وهنا المفاجاه الاولى", bl("المفاجأة الأولى", "archive"), cap=False, in_=DIP)
b("ففي جامعه هارفارد", sc("clinic", [C("LAB", 0.4, "explain", "thinking", 1), C("RUSSELL", 0.6, "holdFront", "thinking", -1, prop="paper")], cam=PUSH, labels=[L("هارفارد — عمى الوجوه", y=0.18, box=True)]))
b("وبعد ان نشرت الصحف", ins("news", head="نحن العكس… لا ننسى وجهًا", who="PLAIN"))
b("فاختبروا اربعه منهم", da(value="4 من 4", label="تفوقوا على الجميع — 2009", size=170))
b("ولاحظ الباحثون شيئا", da(value="اختبار سهل جدًا", label="صُمم لكشف الضعف لا التفوق", size=130))
b("وخلصوا الى ان قدره", ins("spectrum", mark=0.5))
b("اما المفاجاه الثانيه", bl("المفاجأة الثانية", "archive"), cap=False, music_cut="sad")
b("يقول فائقو التعرف انهم", ins("spectrum", mark=0.05, label="يعرفونك… ولا تعرفهم"))
b("وقال الباحث ريتشارد", sc("clinic", [C("RUSSELL", 0.5, "explain", "neutral", 1, s=1.6)], cam=PUSH))
b("تخيل ان تعرف كل من حولك", st("city", [C("YOU", 0.5, "stand", "sad", 1, s=1.3), C("PLAIN", 0.3, "stand", "neutral", 1), C("PLAIN", 0.72, "stand", "neutral", -1)], so=dict(mood="dusk"), cam=PULL))
b("وعلى الطرف الاخر من الطيف", ins("spectrum", mark=0.95, label="الطرف الآخر"))
b("طبيب الاعصاب الشهير اوليفر", sc("archive", [C("SACKS", 0.5, "stand", "smile", 1, s=1.7)], cam=PUSH, labels=[L("أوليفر ساكس — عين العقل 2010", y=0.18, box=True)]))
b("وتروي مراجعات الكتاب", ins("window"))
b("اشهر من كتب عن الدماغ", fc("SACKS", "archive", "confused", side=0.3, rimSide=1))
b("وكم عدد هؤلاء", da(value="2%؟  أم  <1%؟", label="عمى الوجوه — الرقم غير محسوم", size=130))
b("ولسنا وحدنا من يتذكر", ins("sheep", label="كندريك — 2001"), in_=DIP, music_cut="calm")
b("فوجدوا ان الخراف تتعرف", da(value="50 وجهًا", label="لمدة تصل إلى عامين", size=170))
b("وفي عام الفين وسبعه عشر ذهب", ins("sheep", label="كامبريدج — 2017"))
b("فاختارت الخراف الصوره", da(value="8 من 10", label="اختيار صحيح في المتوسط", size=180))
b("وكان هدف الفريق", da(value="هنتنغتون", label="متابعة مرض يصيب الدماغ", size=150))
b("ومع ذلك انتقد باحثون", da(value="ادعاء أكبر من البيانات؟", label="نقد 2019", size=110, color="coral"))
b("وفي الادب العلمي كتب", ins("news", head="الرجل الذي حسب زوجته قبعة", who="SACKS"))
b("والان الى العلم", bl("أين يتعرّف الدماغ على الوجوه؟", "archive"), cap=False, music_cut="calm", in_=DIP)
b("في عام الف وتسعمئه وسبعه وتسعين اطلقت", sc("clinic", [C("KANWISHER", 0.5, "explain", "smile", 1, s=1.6)], cam=PUSH, labels=[L("نانسي كانويشر — 1997", y=0.18, box=True)]))
b("منطقه الوجوه المغزليه", ins("ffa", label="منطقة الوجوه المغزلية"))
b("لكن عالمه اخرى هي", sc("clinic", [C("GAUTHIER", 0.5, "explain", "thinking", 1, s=1.6)], cam=PUSH, labels=[L("إيزابيل غوتييه", y=0.18, box=True)]))
b("ففي تجاربها نشطت", ins("ffa", icons=["🚗", "🐦"], label="خبراء السيارات والطيور"))
b("بل صممت مع زميلها", ins("ffa", icons=["👾"], label="الغريبلز"))
b("فردت كانويشر وزملاؤها", st("studio", [C("KANWISHER", 0.35, "explain", "determined", 1), C("GAUTHIER", 0.65, "explain", "determined", -1)], cam=PUSH, labels=[L("خلاف علمي مفتوح", y=0.18, box=True)]))
b("والان الى ما وعدتك به", bl("الجواب الموعود", "archive"), cap=False, in_=DIP, sfx=[SFX("stinger", 0.1, -10)], music_cut="hopeful")
b("في يد غاري كولينز", sc("city", [C("COLLINS", 0.5, "stand", "smile", 1, s=1.5)], so=dict(mood="day"), cam=PULL))
b("لكن فائقي التعرف انفسهم", ins("spectrum", mark=0.05))
b("فان تتذكر وجه انسان", bl("أن تتذكره… غير أن يتذكرك", "archive"), cap=False, sfx=[SFX("impact", 0.2, -10)])
b("وربما يكون هذا هو الدرس", ins("spectrum", mark=0.5, label="كلنا على الطيف"))
b("واذا تذكرت انت وجه", st("city", [C("YOU", 0.38, "wave", "smile", 1, s=1.4), C("PLAIN", 0.62, "stand", "smile", -1, s=1.4)], so=dict(mood="dusk"), cam=PULL))
b("فالذاكره الخارقه لا تصنع", fc("YOU", "city", "smile", side=0.0))
b("وفي الحلقه القادمه", bl("ماذا لو سمعت الألوان؟", "archive", str2="الحلقة القادمة", at2=0.8), cap=False, sfx=[SFX("riser", 0, -12)])
b("والان سؤال الحلقه", dict(tpl="endscreen", q="لو خُيّرت: لا تنسى وجهًا… حتى من تتمنى نسيانهم؟", cast=["COLLINS", "SACKS", "YOU", "RUSSELL", "KANWISHER", "GAUTHIER"]), in_=FADE, cap=False)

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
story = {"title": "ماذا لو لم تنسَ وجهًا رأيته أبدًا؟", "duration": DUR, "shots": shots, "music": music, "sfx": []}
json.dump(story, open(f"{PROJ}/story/shots.json", "w"), ensure_ascii=False, indent=1)
d = [s["end"] - s["start"] for s in shots]; d.sort()
print(len(shots), "shots; median", round(d[len(d) // 2], 2), "min", round(d[0], 2), "max", round(d[-1], 2))
print("music:", [(m["mood"], round(m["start"]), round(m["end"])) for m in music])
