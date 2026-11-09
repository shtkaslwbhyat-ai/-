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

# ================= COLD OPEN =================
b("تسألك أختك سلمى", st("home", [C("YOU", 0.38, f=1, expr="neutral", **CH()), C("SALMA", 0.62, f=-1, expr="smirk", **CH())], props=[dict(k="table", x=0.5, plate=True)], cam=PUSH, s=1.45), amb={"name": "roomtone", "gain": -26})
b("ماذا اكلنا يوم الثلاثاء", fc("SALMA", "home", "smirk", side=0.4, rimSide=1, talkp="ماذا اكلنا يوم الثلاثاء قبل اربع سنوات"), bars="scope")
b("تجيب فورا", fc("YOU", "home", "smile", side=-0.3, memories=True))
b("ارزا وملوخيه", ins("plate"), sfx=[POP(0.2, -14)])
b("في الثانيه وسبع دقائق", ar(hero=True, expr="smile", cards=["الثلاثاء", "2:07"], cardsX=[0.25, 0.75], cardsY=[0.28, 0.28], gap=0.4), sfx=[SFX("shimmer", 0, -14)])
b("وكانت الملوخيه مالحه", ins("plate", labels=[L("مالحة قليلا", y=0.16, cream=True, at=0.6, box=True)]))
b("تفتح سلمى فمها", fc("SALMA", "home", [[0, "surprised"], [1.1, "neutral"]], side=0.3, rimSide=1))
b("يسالك المعلم", st("classroom", [C("TEACHER", 0.28, "point", "neutral", f=1), C("YOU", 0.7, "stand", "neutral", f=-1), C("PLAIN", 0.85, "sit", "neutral", f=-1, s=1.2, chair=True)], cam=PUSH, s=1.4), in_=DIP, amb={"name": "roomtone", "gain": -24})
b("تعيده كلمه كلمه", st("classroom", [C("YOU", 0.55, "explain", "determined", f=-1, s=1.8)], cam=dict(z0=1.1, z1=1.18, x0=0, x1=-30), labels=[L("كح كح", x=0.3, y=0.3, ap="وبالسعال", cream=True)]))
b("يضحك الفصل كله", st("classroom", [C("PLAIN", 0.15, "cheer", "joy", f=1, s=1.1), C("PLAIN", 0.3, "cheer", "joy", f=1, s=1.1), C("PLAIN", 0.62, "cheer", "joy", f=-1, s=1.1), C("YOU", 0.47, "stand", "smile", f=1, s=1.2), C("PLAIN", 0.8, "cheer", "joy", f=-1, s=1.1)], cam=DRIFT), sfx=[SFX("cheer", 0, -20)])
b("المعلم لا يضحك", fc("TEACHER", "classroom", "neutral", side=-0.2, tilt=-0.05))
b("تبحث امك عن مفاتيحها", st("home", [C("MOM", 0.38, [[0, "think"], [1.2, "handsOnHead"]], "worried", f=1), C("YOU", 0.72, "relaxed", "neutral", f=-1)], cam=PUSH))
b("تقول لها", st("home", [C("YOU", 0.62, [[0, "relaxed"], [0.8, "point"]], "smile", f=-1, s=1.7, tp="في جيب المعطف الرمادي يا امي"), C("MOM", 0.32, "stand", [[0, "worried"], [1.5, "surprised"]], f=1, s=1.7)], cam=dict(z0=1.05, z1=1.12, x0=20, x1=-20)))
b("وضعتها هناك مساء الخميس", ar(hero=True, expr="smile", cards=["الخميس", "8:10 مساء"], cardsX=[0.25, 0.75], cardsY=[0.28, 0.28], gap=1.0), sfx=[SFX("shimmer", 0, -14)])
b("تجدها", ins("keys"), sfx=[SFX("ding", 0.9, -12)])
b("ثم تنظر اليك نظره غريبه", fc("MOM", "home", "confused", side=0.3, rimSide=1))
b("في المخبز يعطيك", st("bakery", [C("BAKER", 0.62, "holdFront", "smile", f=-1), C("YOU", 0.38, "stand", "neutral", f=1)], cam=PUSH), in_=WHIP, amb={"name": "city", "gain": -26}, sfx=[SFX("whoosh", 0, -14)])
b("فتذكره بلطف", ins("coin", labels=[L("قبل 3 سنوات", y=0.15, at=1.5, box=True)]))
b("يضحك ثم يعطيك الجنيه", st("bakery", [C("BAKER", 0.6, "shrug", "joy", f=-1, s=1.7), C("YOU", 0.38, "stand", "smirk", f=1, s=1.7)], cam=dict(z0=1.08, z1=1.14, x0=0, x1=-30)))
b("وجوربك الازرق", ins("sock", labels=[L("قبل 43 يوما", y=0.15, ap="ثلاثه واربعين", box=True)]))
b("وهو ليس هناك", fc("YOU", "bedroom", "confused", side=0.0), sfx=[SFX("blip", 0.3, -16)])
# ================= BASELINE / RULE =================
b("معظم الناس لا يتذكرون", st("city", [C("PLAIN", 0.2, walk=[0.1, 0.35], s=1.1), C("PLAIN", 0.5, "think", "confused", f=-1, s=1.2), C("PLAIN", 0.85, walk=[0.9, 0.65], s=1.1)], so=dict(mood="golden"), cam=DRIFT, labels=[L("قبل 5 سنوات؟", y=0.2, ap="قبل خمس سنوات", box=True)]), in_=DIP, amb={"name": "city", "gain": -26})
b("في عام 1885", dict(tpl="curve", label="منحنى النسيان"), sfx=[POP(0.2)])
b("نحن نفقد جزءا كبيرا", dict(tpl="curve", label="ننسى بسرعة"))
b("وانت لا تفقد شيئا", dict(tpl="curve", you=0.3), sfx=[SFX("shimmer", 0.3, -12)])
b("ثمانون عاما من العمر", da(icon="life", to=2500000000, label="ثانية", count=2.6, size=120), sfx=[SFX("counter", 0.3, -16)])
b("وانت تحفظ كل ثانيه", ar(hero=True, expr="awe", cards=["التاريخ", "الساعة", "الإحساس"], cardsX=[0.2, 0.5, 0.8], cardsY=[0.25, 0.18, 0.25], gap=0.9))
b("لكن لهذه القدره قاعده", bl("قاعدة واحدة", "archive"), sfx=[SFX("stinger", 0.2, -10)], cap=False)
b("انت لا تستطيع ان تنسى", bl("لا تستطيع أن تنسى", "home", str2="ولا أن تختار ما تتذكر", at2=2.2, coral=True), cap=False)
b("وكل ذكرى تفتحها تعود بمشاعرها", dict(tpl="freeze", set="home", expr=[[0, "neutral"], [1.4, "awe"]]), in_=FLASH, bars="scope", sfx=[SFX("freeze", 0, -6)])
b("وستتعلم يوما", ar(hero=True, pose="think", expr="thinking", labels=[L("عقلك يحفظ كل شيء", y=0.2, ap="عقلك يحفظ كل شيء"), L("لكن قلبك يختار ما يبقى", y=0.32, ap="لكن قلبك", cream=True)], cam=PUSH))
b("اسمك يوسف", st("home", [C("YOU", 0.5, "relaxed", "smile", f=1, s=1.8)], cam=PUSH, labels=[L("يوسف", y=0.2, ap="يوسف", size=90), L("17 عاما", y=0.32, ap="عمرك", cream=True)]))
b("فماذا لو تذكرت كل ثانيه", dict(tpl="title"), in_=FADE, bars="scope", cap=False, sfx=[SFX("riser", 0, -12)])
# ================= MONTAGE =================
b("تبدا بالمدرسه", st("classroom", [C("YOU", 0.45, "holdFront", "neutral", f=1, prop="paper", s=1.6), C("PLAIN", 0.75, "sit", "sleepy", f=-1, chair=True, s=1.3)], cam=PUSH, labels=[L("سبتمبر", y=0.2, ap="سبتمبر", box=True)]), in_=DIP, amb={"name": "roomtone", "gain": -26})
b("وفي الامتحان ترى الصفحه", ins("book"))
b("الدرجه مئه من مئه", da(value="100 / 100", label="الدرجة", at=0.6), sfx=[SFX("ding", 0.6, -10)])
b("زملاؤك يسهرون", st("bedroom", [C("YOU", 0.5, [[0, "relaxed"], [2.4, "facepalm"]], [[0, "sleepy"], [2.4, "worried"]], f=1, s=1.6)], cam=PUSH, labels=[L("أسبوع كامل", y=0.2, ap="اسبوعا كاملا", cream=True, out=1.8)]), amb={"name": "roomtone", "gain": -28})
b("ثم يختبرك اصدقاؤك", st("city", [C("ADAM", 0.62, [[0, "stand"], [1.6, "point"]], "smirk", f=-1, tp="الخامس عشر من مارس"), C("PLAIN", 0.78, "crossArms", "smirk", f=-1, s=1.3), C("YOU", 0.36, "stand", "neutral", f=1)], so=dict(mood="golden"), cam=PUSH, labels=[L("15 مارس 2019", y=0.18, ap="الخامس عشر", box=True)]), amb={"name": "city", "gain": -26})
b("تجيب كان يوم جمعه", ar(hero=True, expr="smile", cards=["الجمعة", "غائمة", "قميص أخضر"], cardsX=[0.2, 0.5, 0.8], cardsY=[0.25, 0.18, 0.25], gap=0.9), sfx=[SFX("shimmer", 0, -14)])
b("يفتح هاتفه ليتاكد", ins("phone"), sfx=[SFX("ding", 1.0, -12)])
b("يغلق هاتفه ببطء", fc("ADAM", "city", "shocked", side=0.3, rimSide=1))
b("ابوك يراهنك", st("home", [C("DAD", 0.32, "sitBack", "smirk", f=1, chair=True), C("YOU", 0.55, "crossArms", "smirk", f=-1)], props=[dict(k="tv", x=0.82)], cam=PUSH, labels=[L("قبل 6 سنوات", y=0.18, ap="قبل ست سنوات", box=True)]))
b("تصف له الاهداف الثلاثه", ins("tvscore"), sfx=[SFX("whistle", 0.2, -16)])
b("وماذا صرخ هو", st("home", [C("DAD", 0.55, [[0, "stand"], [0.6, "cheer"]], "angry", f=1, s=1.7)], props=[dict(k="tv", x=0.82)], cam=dict(z0=1.05, z1=1.12, x0=0, x1=-60, shake=4), badge="85'"), sfx=[SFX("cheer", 0.6, -18)])
b("يدفع ابوك ثمن العشاء", st("home", [C("DAD", 0.35, "shrug", "sad", f=1), C("YOU", 0.6, "relaxed", "smirk", f=-1)], props=[dict(k="table", x=0.48, plate=True)], cam=PUSH))
b("في كل خلاف عائلي", st("home", [C("YOU", 0.2, "stand", "neutral", f=1), C("MOM", 0.5, "point", "angry", f=-1), C("DAD", 0.68, "crossArms", "angry", f=-1), C("SALMA", 0.84, "handsOnHead", "worried", f=-1)], cam=DRIFT, labels=[L("من قال ماذا؟", y=0.2, ap="من قال ماذا", cream=True)]))
b("تعيد الكلام حرفا حرفا", st("home", [C("YOU", 0.3, "explain", "determined", f=1, s=1.6), C("MOM", 0.6, "crossArms", "surprised", f=-1, s=1.6), C("DAD", 0.78, "shrug", "confused", f=-1, s=1.6)], cam=PUSH, labels=[L("دقيقتان", y=0.18, ap="في دقيقتين", box=True)]))
b("وبعد شهر", st("home", [C("YOU", 0.14, "stand", "confused", f=1, s=1.3), C("MOM", 0.6, "talk", "joy", f=1, s=1.3), C("DAD", 0.76, "talk", "joy", f=-1, s=1.3), C("SALMA", 0.68, "cheer", "happy", f=-1, s=1.3)], cam=PULL))
b("تشاهد فيلما يابانيا", ins("film", labels=[L("90 دقيقة", y=0.1, ap="تسعون", box=True)]), in_=WHIP)
b("ثم تعيد حواره كله", st("home", [C("YOU", 0.32, "sit", "determined", f=1, chair=True), C("MOM", 0.6, "sit", "confused", f=-1, chair=True), C("SALMA", 0.74, "sit", "shocked", f=-1, chair=True)], props=[dict(k="table", x=0.47, w=420, plate=True)], cam=PUSH, labels=[L("؟؟؟", x=0.6, y=0.25, at=0.8, cream=True)]))
b("هل فهمت كلمه واحده", fc("YOU", "home", [[0, "thinking"], [1.7, "smirk"]], side=-0.2))
b("ثم تاخذك امك الى عياده", st("clinic", [C("MOM", 0.22, "stand", "worried", f=1), C("YOU", 0.36, "stand", "neutral", f=1), C("MAYA", 0.72, "explain", "smile", f=-1)], cam=PUSH, labels=[L("د. مايا", x=0.72, y=0.18, ap="الدكتوره", box=True)]), in_=DIP, amb={"name": "hum", "gain": -28})
b("تخبرك ان في الدماغ", da(icon="brain", to=86, suffix=" مليار", label="خلية عصبية", count=1.8, size=120), sfx=[SFX("counter", 0.3, -16)])
b("وان حالات تشبه حالتك", st("clinic", [C("MAYA", 0.22, "point", "smile", f=1), C("YOU", 0.8, "stand", "surprised", f=-1)], cam=DRIFT, labels=[L("2006", x=0.5, y=0.12, ap="2006", size=80)]))
b("لامراه امريكيه", da(value="جيل برايس", label="أول حالة موثقة", size=120, at=0.2))
b("وعدد الحالات المؤكده", da(value="بضع عشرات", label="حالة مؤكدة في العالم", size=120))
b("ثم تنظر الى نتائجك", st("clinic", [C("MAYA", 0.36, [[0, "think"], [1.5, "explain"]], [[0, "thinking"], [1.5, "awe"]], f=1, s=1.7), C("YOU", 0.66, "stand", "neutral", f=-1, s=1.7)], cam=PUSH))
b("انت ابعد من كل هؤلاء", fc("MAYA", "clinic", "awe", side=0.3, rimSide=1, talkp="انت ابعد من كل هؤلاء"), bars="scope")
b("ثم ياتي يوم مختلف", st("city", [C("PLAIN", 0.42, "handsOnHead", "shocked", f=1, s=1.5)], so=dict(mood="night"), cam=PUSH, labels=[L("سُرقت!", x=0.42, y=0.22, ap="تسرق", coral=True)]), in_=DIP, amb={"name": "city", "gain": -28})
b("الشرطه لا تملك", st("city", [C("POLICE", 0.3, "shrug", "confused", f=1), C("PLAIN", 0.45, "sad", "sad", f=-1), C("YOU", 0.72, "think", "thinking", f=-1)], so=dict(mood="night"), cam=DRIFT, labels=[L("قبل 3 أشهر", y=0.16, ap="قبل ثلاثه اشهر", box=True), L("ثانيتان فقط", y=0.28, ap="لثانيتين", cream=True)]))
b("وتتذكر رقم لوحتها", ins("plate_number"), sfx=[SFX("ding", 0.4, -10)])
b("بعد يومين تعود الدراجه", st("city", [C("PLAIN", 0.45, "cheer", "joy", f=1), C("YOU", 0.66, "relaxed", "smile", f=-1)], so=dict(mood="golden"), cam=PUSH, labels=[L("بعد يومين", y=0.18, at=0.2, box=True)]))
b("ثم تدعوك بطوله دوليه", st("studio", [C("YOU", 0.5, "stand", "determined", f=1, s=1.5)], crowd=0.2, cam=PUSH, labels=[L("1000 رقم", x=0.3, y=0.15, ap="الف رقم", box=True), L("10 دقائق", x=0.7, y=0.15, ap="عشر دقائق", box=True)]), in_=WHIP, amb={"name": "murmur", "gain": -26})
b("تحفظها كلها", ins("digits"), sfx=[SFX("counter", 0.2, -16)])
b("الحكام مذهولون", st("studio", [C("PLAIN", 0.32, "sitBack", "shocked", f=1, chair=True), C("PLAIN", 0.5, "sitBack", "shocked", f=1, chair=True), C("PLAIN", 0.68, "sitBack", "awe", f=1, chair=True)], cam=PUSH), sfx=[SFX("stinger", 0.1, -12)])
b("وانت تتساءل في سرك", fc("YOU", "studio", "thinking", side=-0.2, look=[0.4, -0.3]))
b("وبعدها العالم كله", st("studio", [C("YOU", 0.42, "wave", "smile", f=1), C("WAITER", 0.62, "explain", "happy", f=-1)], crowd=1, cam=PULL), sfx=[SFX("applause", 0.2, -16)], amb={"name": "murmur", "gain": -24})
b("ثلاثمئه تاريخ", da(to=300, label="تاريخ في ساعة واحدة", count=2.0), sfx=[SFX("counter", 0.3, -16)])
b("المقطع يصل الى", da(to=20000000, label="مشاهدة في أسبوع", count=2.0, size=130), sfx=[SFX("counter", 0.3, -16)])
b("الصحف تسميك", bl("الفتى الذي لا ينسى", "city"), cap=False, sfx=[SFX("impact", 0.2, -10)])
b("وانت تبتسم للكاميرا", fc("YOU", "studio", [[0, "smile"], [1.8, "sleepy"]], side=0.1))
# ================= HIDDEN COST =================
b("لان هناك شيئا لا يعرفه", st("bedroom", [C("YOU", 0.19, "lie", "sleepy", f=1, y=0.815, still=True, s=1.3, rot=-1.5708)], cam=PUSH), in_=DIP, amb={"name": "roomtone", "gain": -30}, music_cut="sad")
b("كل وجه كل صوت", fc("YOU", "bedroom", "worried", side=0.0, memories=True), sfx=[SFX("whoosh", 0, -16)])
b("تنام في الثالثه فجرا", st("bedroom", [C("YOU", 0.42, "sit", "sleepy", f=1, chair=True)], cam=PUSH, clock=[3, 0]))
b("وتستيقظ في السابعه", st("bedroom", [C("YOU", 0.5, "stand", "sleepy", f=1, s=1.6)], so=dict(), cam=PUSH, clock=[7, 0]), sfx=[SFX("clock", 0, -14)])
b("وهناك اشياء صغيره تختفي", st("home", [C("YOU", 0.4, "sitBack", "sleepy", f=1, chair=True)], props=[dict(k="tv", x=0.75)], cam=PUSH))
b("وحين سقطت عن الدراجه", st("city", [C("YOUKID", 0.48, "fall", "cry", f=1, rot=0.5)], so=dict(mood="golden"), cam=dict(z0=1.06, z1=1.12, x0=0, x1=-30), labels=[L("في الخامسة", y=0.18, ap="في الخامسه", box=True)]), in_=FADE)
b("وهناك ما هو اسوا", st("classroom", [C("ADAM", 0.36, "point", "smirk", f=1), C("PLAIN", 0.18, "cheer", "joy", f=1, s=1.2), C("PLAIN", 0.26, "cheer", "joy", f=1, s=1.2), C("YOU", 0.7, "sad", "sad", f=-1)], cam=PUSH, labels=[L("قبل عامين", y=0.16, ap="قبل عامين", box=True)]), in_=DIP)
b("اعتذر في اليوم نفسه", st("city", [C("ADAM", 0.4, "shrug", "sad", f=1), C("YOU", 0.62, "crossArms", "sad", f=-1)], so=dict(mood="golden"), cam=PUSH))
b("الناس نسوا", st("city", [C("ADAM", 0.4, walk=[0.3, 0.6]), C("PLAIN", 0.5, walk=[0.4, 0.7]), C("PLAIN", 0.3, walk=[0.2, 0.5])], so=dict(mood="golden"), cam=DRIFT))
b("وانت تسمعها الان", dict(tpl="freeze", set="classroom", expr=[[0, "sad"], [2, "cry"]]), in_=FLASH, bars="scope", sfx=[SFX("freeze", 0, -6)])
b("فكيف تسامح على جرح", fc("YOU", "bedroom", "sad", side=0.0, tear=1.0), bars="scope")
b("تشرح لك الدكتوره مايا", st("clinic", [C("MAYA", 0.32, "explain", "smile", f=1, s=1.6), C("YOU", 0.66, "stand", "neutral", f=-1, s=1.6)], cam=PUSH, labels=[L("النسيان ليس عطلا", y=0.15, ap="النسيان ليس", box=True)]), amb={"name": "hum", "gain": -28})
b("انه يساعد الدماغ", da(icon="brain", value="الصورة الكبيرة", label="ذكريات أخف ألما", size=100, at=0.4, count=4))
b("وتخبرك عن عالم نفس", da(value="ألكسندر لوريا", label="30 عاما من الدراسة", size=110))
b("كان يحفظ كل شيء تقريبا", ar(hero=True, heroC="PLAIN", expr="confused", cards=["يحفظ كل شيء", "لا يستطيع النسيان"], cardsX=[0.25, 0.75], cardsY=[0.25, 0.25], gap=1.6))
b("نشر لوريا كتابه", da(value="1968", label="كتاب لوريا عنه", size=150))
b("ثم تقول لك بهدوء", fc("MAYA", "clinic", "smile", side=0.3, rimSide=1, talkp="التفاصيل الكثيره قد تخفي عنك الطريق يا يوسف"))
b("وانت لا تعرف بعد", fc("YOU", "clinic", "thinking", side=-0.2))
b("ومع الوقت صرت الشخص", st("city", [C("YOU", 0.36, "point", "smirk", f=1), C("ADAM", 0.6, "crossArms", "neutral", f=-1), C("PLAIN", 0.74, "crossArms", "neutral", f=-1, s=1.3)], so=dict(mood="dusk"), cam=PUSH))
b("وصار اصدقاؤك يختارون", st("city", [C("YOU", 0.3, "sad", "sad", f=1), C("ADAM", 0.65, walk=[0.6, 0.85]), C("PLAIN", 0.75, walk=[0.7, 0.95], s=1.3)], so=dict(mood="dusk"), cam=PULL))
# ================= THE HEART =================
b("في البيت جدتك ليلى", st("home", [C("LAYLA", 0.56, "relaxed", "joy", f=-1), C("YOU", 0.36, "relaxed", "smile", f=1)], cam=PUSH, labels=[L("جدتك ليلى", x=0.56, y=0.18, ap="جدتك ليلى", box=True)]), in_=FADE, music_cut="hopeful")
b("لكن الطبيب قال", fc("LAYLA", "home", "confused", side=0.3, rimSide=1, look=[0.4, -0.2]))
b("تسالك اليوم ثلاث مرات", st("home", [C("LAYLA", 0.6, "talk", "smile", f=-1, tp="هل اكلت يا حبيبي"), C("YOU", 0.38, "sit", "smile", f=1, chair=True)], props=[dict(k="table", x=0.5)], cam=PUSH, badge="×3"))
b("وتجيبها في كل مره", fc("YOU", "home", "smile", side=-0.2))
b("هي التي علمتك صنع الشاي", st("home", [C("LAYLA", 0.58, "holdFront", "joy", f=-1, s=1.6), C("YOUKID", 0.44, "stand", "happy", f=1, s=1.6)], cam=PUSH, labels=[L("في السادسة", y=0.16, ap="في السادسه", box=True)]), in_=FADE)
b("ملعقتان من السكر", ins("teacups", labels=[L("ملعقتان سكر", x=0.3, y=0.16, at=0.3, box=True), L("ورقة نعناع", x=0.7, y=0.16, ap="وورقه نعناع", box=True)]))
b("والاسبوع الماضي", st("home", [C("LAYLA", 0.58, "talk", "joy", f=-1, s=1.6), C("YOU", 0.38, "stand", [[0, "smile"], [2, "sad"]], f=1, s=1.6)], cam=PUSH))
b("انت لم تضحك", fc("YOU", "home", "sad", side=-0.1))
b("هي تنسى كل يوم اكثر", dict(tpl="split"), bars="scope")
b("عندما تطبخ تدندن", st("home", [C("LAYLA", 0.6, "holdFront", "happy", f=1, s=1.6)], cam=PUSH, labels=[L("♪", x=0.66, y=0.25, at=0.4), L("♫", x=0.72, y=0.18, at=1.0)]))
b("تسالها عن اسمها", fc("LAYLA", "home", "joy", side=0.3, rimSide=1, talkp="نسيته"))
b("لكن اللحن لا يذهب", ins("song"))
b("وتحكي لك عن مقهى صغير", st("seacafe", [C("GRANDPA", 0.4, "sit", "smile", f=1, chair=True), C("LAYLA", 0.6, "sit", "joy", f=-1, chair=True)], props=[dict(k="table", x=0.5, cups=[[-50, False], [50, False]])], cam=PUSH), in_=FADE, amb={"name": "wind", "gain": -28})
b("حكتها لك مئه وسبع", da(to=117, label="مرة", count=1.6))
b("وانت تتذكر كل مره", ar(hero=True, expr="smile", n=60))
b("تضع يدها على صدرك", st("home", [C("LAYLA", 0.55, [[0, "stand"], [0.6, "reach"]], "smile", f=-1, s=1.9, tp="الذاكره صندوق يا يوسف والقلب مفتاحه"), C("YOU", 0.4, "stand", "smile", f=1, s=1.9)], cam=dict(z0=1.1, z1=1.18, x0=0, x1=-30)), bars="scope")
b("تبتسم لها ولا تفهم", fc("YOU", "home", [[0, "smile"], [1.2, "thinking"]], side=-0.2))
b("وحين تنام في المساء", st("home", [C("LAYLA", 0.4, "sitBack", "sleepy", f=1, chair=True), C("YOU", 0.58, "sit", "sad", f=-1, chair=True)], so=dict(night=True, sky="night"), cam=PUSH), in_=DIP)
# ================= CRISIS =================
b("ثم ياتي يوم الجمعه", st("home", [C("YOU", 0.5, "relaxed", "neutral", f=1)], cam=PUSH, clock=[4, 0]), in_=DIP, music_cut="tension")
b("يرن هاتفك", ins("phonering"), sfx=[SFX("phonering", 0, -10)])
b("جدتك خرجت من البيت", st("home", [C("MOM", 0.62, "phone", "scared", f=-1, prop="phone")], props=[dict(k="chairEmpty", x=0.35)], cam=PUSH, labels=[L("قبل ساعتين", y=0.16, ap="قبل ساعتين", coral=True, box=True)]))
b("هاتفها على الطاوله", st("home", [], props=[dict(k="table", x=0.5, phone=True)], cam=dict(z0=1.6, z1=1.7, x0=0, x1=-20, y0=170, y1=175)))
b("الشمس تغيب بعد", st("city", [], so=dict(mood="dusk"), cam=PULL, labels=[L("40 دقيقة", y=0.2, ap="اربعين", coral=True, box=True)]), amb={"name": "wind", "gain": -22})
b("انت تعرف كل مكان", fc("YOU", "home", "determined", side=0.0))
b("تغمض عينيك وينفتح", ar(hero=True, expr="determined", speed=2.5, cam=dict(z0=1.0, z1=1.15, x0=0, x1=0)), in_=ZOOM, sfx=[SFX("whoosh", 0, -10)])
b("سوق الخضار بيت", dict(tpl="places", pins=[["سوق الخضار", 0.2, 0.4, "سوق"], ["بيت خالتها", 0.45, 0.65, "بيت"], ["محطة القطار", 0.7, 0.35, "محطه"], ["المدرسة", 0.85, 0.7, "المدرسه"]]), sfx=[POP(0.2), POP(1.2), POP(2.2), POP(3.4)])
b("هل ذهبت الى المحطه", st("city", [], so=dict(mood="dusk", station=True), cam=PUSH, labels=[L("12 كم", y=0.3, ap="اثني عشر", coral=True, box=True)]))
b("الى السوق السوق يغلق", st("city", [C("PLAIN", 0.5, walk=[0.55, 0.45], s=1.1)], so=dict(mood="dusk", market=True), cam=DRIFT, clock=[5, 0]))
b("الى المدرسه لكنها", st("classroom", [], cam=PUSH, labels=[L("مغلقة", y=0.2, ap="اغلقت", coral=True, box=True)]))
b("ثلاثمئه مكان", dict(tpl="places", many=True, pins=[], labels=[L("300 مكان", x=0.3, y=0.15, at=0.2, box=True), L("40 عاما", x=0.7, y=0.15, ap="اربعون", box=True)]))
b("وكل ذكرى تفتحها تعود كامله", ar(hero=True, expr="worried", speed=3, cards=["رائحتها", "صوتها", "ضحكتها"], cardsX=[0.2, 0.5, 0.8], cardsY=[0.25, 0.18, 0.25], gap=0.8))
b("تمر دقيقه ثم خمس", da(value="", labels=[L("1 دقيقة", y=0.35, at=0.2, coral=True, size=90, out=0.9), L("5 دقائق", y=0.5, at=1.0, coral=True, size=90, out=1.8), L("10 دقائق", y=0.65, at=1.9, coral=True, size=100)]), sfx=[SFX("clock", 0, -12)])
b("وانت ما زلت واقفا", st("home", [C("YOU", 0.5, "stand", "worried", f=1, still=True, s=1.2)], cam=PULL))
b("تسالك امك على الهاتف", st("home", [C("YOU", 0.5, "phone", "worried", f=1, prop="phone", s=1.7)], cam=PUSH))
b("وانت صاحب الذاكره", fc("YOU", "home", [[0, "worried"], [2.5, "scared"]], side=0.0), bars="scope")
b("ثلاثون دقيقه على الغروب", dict(tpl="places", many=True, pins=[], timer=[30, 0.0]), sfx=[SFX("heartbeat", 0, -10)])
b("عقلك يحفظ كل شيء ولهذا", ar(hero=True, pose="handsOnHead", expr="scared", n=90, speed=4, cam=dict(z0=1.0, z1=1.1, x0=0, x1=0, shake=6)), sfx=[SFX("glitch", 0.3, -14)])
b("وهنا تفهم", bl("أمامك طريقان فقط", "home"), cap=False)
b("اما ان تغوص اعمق", ar(hero=True, pose="fall", expr="scared", n=80, speed=3, cam=dict(z0=1.0, z1=1.4, x0=0, x1=0)))
b("واما ان تفتح عينيك", fc("YOU", "home", "determined", side=0.0), in_=FLASH, sfx=[SFX("shimmer", 0, -10)])
b("تفتح عينيك تمسك الهاتف", st("home", [C("YOU", 0.5, [[0, "stand"], [1, "phone"]], "determined", f=1, prop="phone", s=1.7)], cam=PUSH, labels=[L("آدم", y=0.18, ap="بادم", box=True)]))
b("ادم نفسه", fc("ADAM", "city", "neutral", side=0.3, rimSide=1))
b("يرد من الرنه الاولى", st("city", [C("ADAM", 0.3, walk=[0.15, 0.8], run=True, tp="انا قادم")], so=dict(mood="dusk"), cam=DRIFT), sfx=[SFX("footstep", 0.6, -14), SFX("footstep", 1.2, -14)])
b("وسلمى تطبع صوره", ins("group"), sfx=[POP(0.4), POP(1.2, -16)])
b("يصل ادم بعد سبع", st("city", [C("ADAM", 0.62, [[0, "stand"], [1.5, "explain"]], "determined", f=-1), C("YOU", 0.38, "stand", "worried", f=1)], so=dict(mood="dusk"), cam=PUSH, labels=[L("7 دقائق", y=0.16, ap="سبع دقائق", box=True)]))
b("ما الشيء الذي لا تنساه", fc("ADAM", "city", "determined", side=0.3, rimSide=1, talkp="ما الشيء الذي لا تنساه جدتك ابدا"), bars="scope")
b("ليس الشوارع", bl("ليس الشوارع... وليس الأسماء", "city"), cap=False)
b("تتوقف ثم تسمعه", fc("YOU", "city", [[0, "thinking"], [1.6, "awe"]], side=0.0), sfx=[SFX("shimmer", 1.5, -10)])
b("اللحن الاغنيه التي", ins("song"), in_=FLASH, music_cut="hopeful")
b("والمكان الذي تعود اليه", st("seacafe", [], so=dict(outside=True), cam=PULL, labels=[L("المقهى قرب البحر", y=0.2, ap="المقهى", box=True)]))
b("توقفان سياره اجره", st("city", [C("ADAM", 0.36, "point", "determined", f=1), C("YOU", 0.26, "stand", "determined", f=1)], props=[dict(k="taxi", x=0.65, move=True)], so=dict(mood="dusk"), cam=DRIFT), sfx=[SFX("carpass", 0.5, -12)])
b("الريح بارده الشمس", st("seacafe", [], so=dict(outside=True, sunset=0.6), cam=PUSH), amb={"name": "wind", "gain": -22})
b("وهناك على كرسي خشبي", st("seacafe", [C("LAYLA", 0.6, "sit", "happy", f=-1, chair=True)], props=[dict(k="table", x=0.48, cups=[[-40, True], [40, True]]), dict(k="chairEmpty", x=0.38)], cam=PUSH, labels=[L("♪", x=0.62, y=0.3, at=1.5), L("♫", x=0.66, y=0.24, at=2.2)]), bars="scope", in_=FADE)
b("يقول النادل", st("seacafe", [C("WAITER", 0.32, "explain", "neutral", f=1), C("YOU", 0.5, "stand", "worried", f=-1)], cam=PUSH, labels=[L("منذ ساعة", y=0.16, ap="منذ ساعه", box=True)]))
b("واحدا لها", ins("teacups"))
b("تقترب منها", st("seacafe", [C("YOU", 0.3, walk=[0.25, 0.42]), C("LAYLA", 0.62, "sit", "confused", f=-1, chair=True)], props=[dict(k="table", x=0.5, cups=[[-40, True], [40, True]])], cam=PUSH))
b("كانها تبحث عن اسمك", fc("LAYLA", "seacafe", [[0, "confused"], [2.2, "smile"]], side=0.3, rimSide=1))
b("جئت يا حبيبي", fc("LAYLA", "seacafe", "joy", side=0.3, rimSide=1, talkp="جئت يا حبيبي جدك كان يجلس هنا"))
b("تسالها عن اسمه", st("seacafe", [C("YOU", 0.4, "sit", "neutral", f=1, chair=True), C("LAYLA", 0.6, "sit", [[0, "smile"], [1.2, "confused"]], f=-1, chair=True)], props=[dict(k="table", x=0.5, cups=[[-40, True], [40, True]])], cam=PUSH))
b("لكنها تدندن اللحن نفسه", fc("LAYLA", "seacafe", "joy", side=0.3, rimSide=1, labels=[L("♪", x=0.25, y=0.3, at=0.4), L("♫", x=0.8, y=0.25, at=1.0)]))
b("وفي طريق العوده", st("city", [C("YOU", 0.5, walk=[0.3, 0.55]), C("LAYLA", 0.4, walk=[0.2, 0.45]), C("ADAM", 0.6, walk=[0.4, 0.65])], so=dict(mood="night"), cam=DRIFT), in_=DIP, amb={"name": "city", "gain": -28})
b("لكنك تختار الا تحملها", st("city", [C("YOU", 0.4, [[0, "stand"], [2, "explain"]], "smile", f=1, s=1.8, tp="شكرا لنبدا من جديد"), C("ADAM", 0.6, "stand", [[0, "neutral"], [4, "smile"]], f=-1, s=1.8)], so=dict(mood="night"), cam=PUSH))
b("وفي البيت تعلق امك", ins("card"))
b("وسلمى تعانقها", st("home", [C("SALMA", 0.46, "reach", "happy", f=1), C("LAYLA", 0.55, "reach", "smile", f=-1)], so=dict(night=True, sky="night"), cam=PUSH))
b("وتلك الليله يعيد", fc("YOU", "bedroom", "neutral", side=0.0, memories=True), in_=DIP)
b("لكنك تتوقف عند لحظه", st("seacafe", [C("LAYLA", 0.6, "sit", "happy", f=-1, chair=True)], props=[dict(k="table", x=0.48, cups=[[-40, True], [40, True]])], cam=dict(z0=1.15, z1=1.25, x0=-100, x1=-140), labels=[L("♪", x=0.62, y=0.28, at=1.0)]), in_=FADE)
b("وتفهم اخيرا", fc("YOU", "bedroom", "smile", side=0.0, labels=[L("عقلك يحفظ كل شيء", y=0.22, ap="عقلك يحفظ"), L("لكن قلبك يختار ما يبقى", y=0.33, ap="لكن قلبك", cream=True)]), bars="scope")
# ================= REALITY CHECK =================
b("فما الحقيقي في هذه القصه", bl("ما الحقيقي في هذه القصة؟", "archive"), in_=DIP, cap=False, music_cut="calm")
b("الذاكره الذاتيه فائقه", da(value="حالة حقيقية", label="الذاكرة الذاتية فائقة القوة", size=120))
b("لكنهم لا يتذكرون كل ثانيه", da(value="لا يتذكرون كل ثانية", label="ولا يتفوقون في حفظ الأرقام", size=90))
b("بل ان دراسه عام 2013", da(value="2013", label="ذكريات زائفة أيضا", size=150))
b("وجيل برايس نفسها", da(value="بلا توقف", label="مرهقة أكثر منها موهبة", size=120, color="coral"))
b("اما ان تحفظ كل لحظه", da(value="2,500,000,000", label="خيال", size=120, color="coral"))
b("ويبقى سؤال مفتوح", bl("هل ننسى عن قصد؟", "archive"), cap=False)
b("بعض العلماء يرون", da(icon="brain", value="النوم", label="يضعف الروابط الأقل أهمية", size=110, count=3))
b("واخرون يرون ان الصوره", da(value="النقاش مستمر", label="الصورة أعقد", size=110))
b("ونصيحه حقيقيه اخيره", ins("card", labels=[L("بطاقة باسمه ورقم هاتف", y=0.12, ap="بطاقه", box=True)]))
b("واحتفظ بصوره حديثه", st("home", [C("LAYLA", 0.55, "relaxed", "joy", f=-1), C("YOU", 0.4, "phone", "smile", f=1, prop="phone")], cam=PUSH, labels=[L("صورة حديثة", y=0.18, at=0.3, box=True)]))
b("والان تخيل العكس", bl("ماذا لو كان كل يوم يمحى؟", "archive", str2="الحلقة القادمة", at2=3.5), cap=False, in_=DIP, sfx=[SFX("riser", 0, -12)])
b("ما رايك اخبرنا", dict(tpl="endscreen", q="ما رأيك؟ أخبرنا في التعليقات"), in_=FADE, cap=False)

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

# music sections from music_cut markers
music = []; cur = ("playful", 0.35, 0.0)
cuts = {"sad": ("sad", 0.35), "hopeful": ("hopeful", 0.35), "tension": ("tension", 0.6), "calm": ("calm", 0.3)}
for (anchor, params, meta), sh in zip(B, shots):
    if sh["params"]["tpl"] == "title": music.append({"start": cur[2], "end": sh["start"], "mood": cur[0], "intensity": cur[1]}); cur = ("wonder", 0.4, sh["start"])
    if sh["id"] == "s032": pass
    if "music_cut" in meta:
        music.append({"start": cur[2], "end": sh["start"], "mood": cur[0], "intensity": cur[1]}); m, it = cuts[meta["music_cut"]]; cur = (m, it, sh["start"])
music.append({"start": cur[2], "end": DUR, "mood": cur[0], "intensity": cur[1]})
# montage after title back to playful
for k, m in enumerate(music):
    if m["mood"] == "wonder":
        t_end = m["end"]; m["end"] = round(m["start"] + 8, 3); music.insert(k + 1, {"start": m["end"], "end": t_end, "mood": "playful", "intensity": 0.45}); break
story = {"title": "ماذا لو تذكرت كل ثانية من حياتك؟", "duration": DUR, "shots": shots, "music": music, "sfx": []}
json.dump(story, open(f"{PROJ}/story/shots.json", "w"), ensure_ascii=False, indent=1)
d = [s["end"] - s["start"] for s in shots]; d.sort()
print(len(shots), "shots; median", round(d[len(d) // 2], 2), "min", round(d[0], 2), "max", round(d[-1], 2))
print("music:", [(m["mood"], round(m["start"]), round(m["end"])) for m in music])
