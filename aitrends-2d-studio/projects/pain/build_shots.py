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
Y = lambda x, pose="stand", expr="neutral", f=1, **kw: C("YAZAN", x, pose, expr, f, **kw)
J = lambda x, pose="stand", expr="neutral", f=1, **kw: C("YAZANJ", x, pose, expr, f, **kw)
PI = lambda **kw: dict(so=dict(mood=kw.pop("mood", "dusk"), night=kw.pop("night", False), cheer=kw.pop("cheer", 0.2)), **kw)

b("المقلاه على النار", ins("stove"), amb={"name": "roomtone", "gain": -26}, sfx=[SFX("whoosh", 0.1, -16)])
b("امك تصرخ", st("home", [C("HUDA", 0.62, "handsOnHead", "shocked", -1), Y(0.38, "stand", "confused")], cam=PUSH), sfx=[SFX("hit", 0.2, -12)])
b("وانت تنظر الى يدك", fc("YAZAN", "home", "confused", side=0.0))
b("الجلد يحمر", ins("stove", cam=dict(z0=1.25, z1=1.4, x0=300, x1=320)))
b("وانت لا تشعر بشيء", fc("YAZAN", "home", "neutral", side=0.0, labels=[L("لا لسع", x=0.25, y=0.25, ap="لسع", cream=True), L("لا وخز", x=0.75, y=0.25, ap="وخز", cream=True), L("لا شيء", y=0.15, ap="شيء", size=90)]))
b("في المدرسه تصطدم كره", st("classroom", [Y(0.45, "stand", "smile", prop="ball"), C("PLAIN", 0.25, "handsOnHead", "shocked", 1, s=1.3), C("PLAIN", 0.72, "handsOnHead", "shocked", -1, s=1.3)], cam=PUSH), sfx=[SFX("hit", 0.6, -8)])
b("وانت تضحك", fc("YAZAN", "classroom", "joy", side=0.0))
b("في عياده الاسنان يرفع", st("clinic", [C("DOC", 0.62, "holdFront", "neutral", -1), Y(0.38, "sitBack", "smirk", chair=True)], cam=PUSH, labels=[L("لا داعي", y=0.2, ap="داعي", box=True)]))
b("انت لا تشعر بالالم", bl("لا تشعر بالألم… أبدا", "home"), cap=False, sfx=[SFX("stinger", 0.1, -10)])
b("لا جرح يؤلمك", da(value="0", label="جرح • كسر • حرق", size=220, color="coral"))
b("فهل هذه اعظم قوه", ar(hero=True, heroC="YAZAN", expr="smirk", cards=["قوة خارقة؟", "أم لعنة؟"], cardsX=[0.25, 0.75], gap=1.6))
b("لكن لهذه القوه قاعده", bl("قاعدة واحدة", "home", str2="الألم جرس إنذار", at2=2.2), cap=False)
b("الالم جرس انذار", ins("bell"), sfx=[SFX("ding", 0.1, -8), SFX("ding", 0.6, -12)])
b("ومن لا يسمع الجرس", ins("bell", silent=True), music_cut="tension")
b("لا يعرف ان البيت يحترق", st("home", [Y(0.5, "relaxed", "neutral", s=1.3)], cam=PULL, labels=[L("🔥", x=0.85, y=0.35, size=110, at=0.6)]))
b("اسمك يزن", st("home", [Y(0.5, "relaxed", "smile", s=1.8)], cam=PUSH, labels=[L("يزن", y=0.2, ap="يزن", size=90), L("15 عاما", y=0.32, ap="خمسه", cream=True)]))
b("وستتعلم يوما ان اخطر", fc("YAZAN", "home", "thinking", side=0.0, labels=[L("أخطر جرح… الذي لا تشعر به", y=0.18, ap="اخطر")]))
b("فماذا لو لم تشعر", dict(tpl="title", lines=["ماذا لو", "لم تشعر بالألم أبدا؟"]), in_=FADE, bars="scope", cap=False, sfx=[SFX("riser", 0, -12)])
b("في الملعب انت اللاعب", st("pitch", [J(0.45, "ready", "determined"), C("RIVAL", 0.7, "ready", "angry", -1)], cam=PUSH, **PI()), in_=DIP, amb={"name": "murmur", "gain": -24})
b("يدفعونك يركلون ساقيك", st("pitch", [J(0.45, "fall", "surprised"), C("RIVAL", 0.62, "kick", "angry", -1)], cam=dict(z0=1.1, z1=1.15, shake=6), **PI()), sfx=[SFX("hit", 0.3, -8), SFX("hit", 1.2, -10)])
b("ثم تقوم في ثانيه", st("pitch", [J(0.3, walk=[0.3, 0.8], run=True)], cam=DRIFT, **PI(cheer=0.6)), sfx=[SFX("cheer", 0.3, -18)])
b("المدرب يبتسم لاول", fc("COACH", "pitch", "smile", side=0.2, rimSide=1))
b("وزملاؤك يسمونك", bl("الرجل الحديدي", "pitch"), cap=False, sfx=[SFX("impact", 0.2, -10)])
b("وحين يسقط زميل لك", st("pitch", [C("TAREQJ", 0.4, "lie", "cry", 1, y=0.86), J(0.62, "stand", "confused", -1)], cam=PUSH, **PI()))
b("لماذا كل هذا الصراخ", fc("YAZAN", "pitch", "confused", side=0.0))
b("صديقك طارق يصورك", st("city", [Y(0.4, "relaxed", "smirk"), C("TAREQ", 0.65, "phone", "joy", -1)], so=dict(mood="day"), cam=PUSH, labels=[L("حافيا • ظهرا", y=0.18, ap="حافيا", box=True)]))
b("المقطع ينتشر", ins("views"), sfx=[POP(0.3), POP(0.8), POP(1.3)])
b("والتعليقات تسال", da(value="هل هذا حقيقي؟", label="آلاف التعليقات", size=110))
b("في يوم التطعيم تقف", st("clinic", [Y(0.25, "stand", "smile", s=1.3), C("PLAIN", 0.45, "stand", "scared", 1, s=1.3), C("PLAIN", 0.6, "stand", "worried", 1, s=1.3), C("DOC", 0.8, "holdFront", "neutral", -1, s=1.3)], cam=PUSH))
b("وفي النادي ترفع اوزانا", st("studio", [Y(0.5, "pointUp", "determined", s=1.6)], cam=PUSH, labels=[L("150 كغ", y=0.18, ap="اوزانا", box=True)]))
b("ولا تتوقف حين تصرخ", fc("YAZAN", "studio", "determined", side=0.0))
b("وفي الصف يتحداك طارق", st("classroom", [C("TAREQ", 0.62, "point", "smirk", -1), Y(0.38, "stand", "smirk")], cam=PUSH, labels=[L("دقيقة كاملة", y=0.18, ap="دقيقه", box=True)]))
b("تضعها خمس دقائق", ins("icewater"), sfx=[SFX("tick", 0.3, -16)])
b("الجميع يصفقون", st("classroom", [Y(0.5, "cheer", "joy"), C("PLAIN", 0.25, "cheer", "joy", 1, s=1.3), C("PLAIN", 0.75, "cheer", "joy", -1, s=1.3)], cam=PULL), sfx=[SFX("cheer", 0.2, -18)])
b("ويدك تتحول الى لون", ins("icewater", cam=dict(z0=1.3, z1=1.45, x0=-40, x1=-60)))
b("لكن امك هدى لا تضحك", fc("HUDA", "home", "worried", side=0.3, rimSide=1), music_cut="sad", in_=DIP)
b("كل مساء تمسك ورقه", st("bedroom", [C("HUDA", 0.6, "holdFront", "worried", -1, prop="paper"), Y(0.38, "sit", "neutral", chair=True)], cam=PUSH, labels=[L("كطيار قبل الإقلاع", y=0.18, ap="الطيار", box=True)]))
b("القدمان الركبتان", ins("checklist", at=0.1, gap=0.6))
b("وفي احدى الليالي تسمعها", st("home", [C("HUDA", 0.6, "sit", "cry", -1, chair=True), C("DAD", 0.38, "stand", "sad", 1)], so=dict(night=True), cam=PUSH))
b("كل ام تعرف ان طفلها", fc("HUDA", "home", "cry", side=0.3, rimSide=1, tear=0.5))
b("هي تعرف ما لا يعرفه", st("bedroom", [Y(0.5, "sit", "sad", chair=True)], cam=PULL))
b("حين كنت رضيعا عضضت", ar(hero=True, heroC="YAZANKID", expr="neutral", hs=1.2, labels=[L("لم يبك", y=0.2, ap="تبك", box=True)]))
b("وحين بدات تمشي كسرت", ar(hero=True, heroC="YAZANKID", pose="relaxed", expr="smile", hs=1.2, n=50, labels=[L("أسبوع كامل", y=0.2, ap="اسبوعا", box=True, coral=True)]))
b("وذات مساء تتوقف امك", st("bedroom", [C("HUDA", 0.58, "crouch", "shocked", -1), Y(0.38, "sit", "neutral", chair=True)], cam=PUSH))
b("الكاحل منتفخ ولونه ازرق", ins("bodymap", spots=[[-70, 380, "الكاحل", 0.3]]))
b("تسالك منذ متى", fc("YAZAN", "bedroom", "worried", side=0.0, labels=[L("منذ متى؟", y=0.2, ap="متي", box=True)]))
b("في المستشفى يضع الطبيب", st("clinic", [C("DOC", 0.6, "point", "thinking", -1), Y(0.35, "sit", "worried", chair=True), C("HUDA", 0.18, "stand", "worried", 1)], cam=PUSH))
b("كسر جديد في الكاحل", ins("xray"), sfx=[SFX("hit", 0.5, -12), POP(1.4), POP(1.9), POP(2.4)])
b("يقول الطبيب جسمك يصرخ", fc("DOC", "clinic", "sad", side=0.2, rimSide=1, talkp="جسمك يصرخ يا يزن"))
b("ولا حتى انت", fc("YAZAN", "clinic", "sad", side=0.0))
b("سته اسابيع بلا كره", da(value="6 أسابيع", label="بلا كرة", size=170, color="coral"))
b("وانت ترى فريقك من المدرجات", st("pitch", [J(0.5, "sit", "sad", y=0.6, s=1.2)], cam=PULL, **PI(cheer=0.5)))
b("الرجل الحديدي يجلس وحده", fc("YAZAN", "pitch", "sad", side=0.0))
b("والمقاطع التي ضحك", ins("views", cam=dict(z0=1.0, z1=1.04, x0=0, x1=0)))
b("ماذا احترق يومها", fc("YAZAN", "bedroom", "worried", side=0.0))
b("ثم ياتي طارق ويجلس", st("pitch", [J(0.42, "sit", "sad", y=0.6, s=1.3), C("TAREQ", 0.58, "sit", "sad", -1, y=0.6, s=1.3, prop="phone")], cam=PUSH, **PI(cheer=0.3)))
b("من اليوم انا عينك", fc("TAREQ", "pitch", "determined", side=0.3, rimSide=1, talkp="من اليوم انا عينك في الملعب"), music_cut="hopeful")
b("ثم يعود الموسم", bl("يوم النهائي", "pitch"), cap=False, in_=DIP, sfx=[SFX("impact", 0.2, -10)])
b("في الصباح لا تاكل", st("home", [Y(0.4, "sit", "sleepy", chair=True), C("HUDA", 0.65, "stand", "worried", -1)], props=[dict(k="table", x=0.5, plate=True)], cam=PUSH), music_cut="tension")
b("امك تضع يدها على جبينك", st("home", [C("HUDA", 0.55, "reach", "worried", -1, s=1.8), Y(0.4, "sit", "sleepy", chair=True, s=1.8)], cam=PUSH))
b("ثم تحضر مقياس الحراره", ins("thermo"), sfx=[SFX("tick", 0.3, -16), SFX("ding", 2.2, -12)])
b("تقول لن تلعب اليوم", fc("HUDA", "home", "determined", side=0.3, rimSide=1, talkp="لن تلعب اليوم"))
b("وانت تقول انا بخير", fc("YAZAN", "home", "smile", side=0.0, talkp="انا بخير يا امي"))
b("فتنظر اليك وتقول", fc("HUDA", "home", "sad", side=0.3, rimSide=1, labels=[L("وهذه هي المشكلة", y=0.18, ap="وهذه", box=True, coral=True)]))
b("لكنك تذهب", st("city", [Y(0.3, walk=[0.3, 0.7])], so=dict(mood="day"), cam=DRIFT))
b("الشوط الاول جيد", st("pitch", [J(0.4, "kick", "determined"), C("RIVAL", 0.65, "dive", "surprised", -1)], cam=PUSH, **PI(cheer=0.4)), sfx=[SFX("whistle", 0.0, -14), SFX("hit", 0.9, -10)])
b("المدرجات تهتف باسمك", st("pitch", [J(0.5, "cheer", "joy", s=1.6), C("TAREQJ", 0.3, "cheer", "joy", 1, s=1.4)], cam=PULL, **PI(cheer=1.0)), sfx=[SFX("cheer", 0.1, -14)])
b("لكن العرق بارد", fc("YAZAN", "pitch", "nervous", side=0.0, tilt=0.05))
b("والملعب يميل قليلا", st("pitch", [J(0.5, "stand", "worried", s=1.4, rot=0.08)], cam=dict(z0=1.05, z1=1.15, x0=0, x1=-30, r=0.05), **PI()))
b("في الاستراحه ينظر اليك", st("pitch", [C("TAREQJ", 0.6, "explain", "worried", -1, s=1.7), J(0.4, "stand", "nervous", s=1.7)], cam=PUSH, **PI(night=True)))
b("وجهك اصفر يا يزن", fc("TAREQ", "pitch", "scared", side=0.3, rimSide=1, talkp="وجهك اصفر يا يزن"))
b("والمدرب ينظر الى لوحه", ins("scoreboard", score="1 - 1", min="45'"))
b("وترى في عينيه", fc("COACH", "pitch", "determined", side=0.2, rimSide=1))
b("وهنا تفهم امامك طريقان", bl("أمامك طريقان", "pitch"), cap=False)
b("اما ان تسمع الصمت", ar(hero=True, heroC="YAZANJ", pose="think", expr="thinking", n=40))
b("واما ان تسمع ما يقوله", ar(hero=True, heroC="YAZANJ", pose="handsOnHead", expr="worried", n=60, speed=2, cards=["الحرارة", "العرق البارد", "الدوار", "وجه صديقك"], cardsX=[0.2, 0.8, 0.22, 0.78], cardsY=[0.22, 0.22, 0.45, 0.45], gap=0.9))
b("ترفع يدك", st("pitch", [J(0.5, "pointUp", "determined", s=1.7)], cam=PUSH, **PI(night=True)), in_=FLASH, sfx=[SFX("shimmer", 0, -10)])
b("لاول مره في حياتك", st("pitch", [J(0.5, walk=[0.5, 0.1]), C("COACH", 0.12, "stand", "surprised", 1)], cam=PULL, **PI(night=True, cheer=0.1)), music_cut="sad")
b("بعد ساعه انت في غرفه", st("clinic", [C("DOC", 0.6, "stand", "determined", -1), C("HUDA", 0.35, "handsOnHead", "worried", 1)], cam=PUSH), in_=DIP)
b("الزائده الدوديه ملتهبه", ins("bodymap", spots=[[45, 10, "الزائدة الدودية", 0.3]]))
b("والجراح يقول لامك", st("clinic", [C("DOC", 0.6, "talk", "neutral", -1, tp="لو تاخر قليلا لانفجرت"), C("HUDA", 0.38, "handsOnHead", "worried", 1)], cam=PUSH))
b("اي انسان اخر كان", fc("DOC", "clinic", "smile", side=0.2, rimSide=1, labels=[L("أنقذه أنه أصغى", y=0.18, ap="فانقذه", box=True)]), music_cut="hopeful")
b("حين تفتح عينيك تجدها", st("clinic", [Y(0.42, "sitBack", "sleepy", chair=True, s=1.6), C("HUDA", 0.62, "stand", "smile", -1, s=1.6)], cam=PUSH))
b("تمسك يدك وتسال", fc("HUDA", "clinic", "smile", side=0.3, rimSide=1, tear=0.6, talkp="كيف عرفت يا يزن"))
b("فتجيبها لم اسمع", fc("YAZAN", "clinic", "smile", side=0.0, talkp="لم اسمع الالم يا امي"))
b("في المساء يدخل طارق", st("clinic", [Y(0.25, "sitBack", "joy", chair=True, s=1.3), C("TAREQJ", 0.45, "cheer", "joy", -1, s=1.3), C("COACH", 0.62, "stand", "smile", -1, s=1.3), C("PLAIN", 0.78, "cheer", "joy", -1, s=1.3)], cam=PUSH), sfx=[SFX("cheer", 0.6, -18)])
b("ويضعون الميداليه على صدرك", ins("medal"), sfx=[SFX("shimmer", 0.2, -10)])
b("يقول المدرب اشجع", fc("COACH", "clinic", "smile", side=0.2, rimSide=1, labels=[L("أشجع شيء… أن تخرج", y=0.18, ap="كان", box=True)]))
b("وفي تلك الليله تطلب", st("bedroom", [Y(0.4, "holdFront", "determined", prop="paper"), C("HUDA", 0.65, "stand", "smile", -1)], cam=PUSH))
b("تفحص نفسك بنفسك", ins("checklist", items=["القدمان", "الركبتان", "الحرارة"], at=0.6, gap=0.8))
b("ثم تخبرها بكل شيء", st("bedroom", [Y(0.4, "explain", "smile"), C("HUDA", 0.62, "stand", "joy", -1)], cam=PUSH))
b("انت لا تملك جرس", bl("صرت أنت الجرس", "bedroom"), cap=False, sfx=[SFX("ding", 0.3, -10)])
b("لم تشعر بالالم يوما", fc("YAZAN", "bedroom", "smile", side=0.0))
b("فما الحقيقي في هذه القصه", bl("ما الحقيقي في هذه القصة؟", "archive"), in_=DIP, cap=False, music_cut="calm")
b("عدم الاحساس بالالم حاله", da(value="نادرة جدا", label="عدم الإحساس الخلقي بالألم", size=140))
b("ومن اشهر اسبابها خلل", ins("nerve", gene="SCN9A"))
b("حين تتعطل البوابه", ins("nerve", broken=True, gene="SCN9A"))
b("وفي الجسم السليم", ins("nerve", reflex=True))
b("وفي عام الفين وسته", da(value="2006", label="دراسة عائلات في شمال باكستان", size=160))
b("بدات القصه بصبي", st("city", [C("PLAIN", 0.5, "cheer", "smile", 1, s=1.4), C("PLAIN", 0.25, "handsOnHead", "shocked", 1, s=1.2), C("PLAIN", 0.75, "handsOnHead", "shocked", -1, s=1.2)], so=dict(mood="golden"), cam=DRIFT))
b("ومات قبل ان يكمل", da(value="14", label="لم يكمل الرابعة عشرة", size=200, color="coral"))
b("وما تعيشه ام يزن", ins("bodymap", spots=[[0, -305, "اللسان", 0.4], [135, -60, "المفاصل", 1.2], [50, 230, "العظام", 2.0]]))
b("لذلك تتعلم العائلات", ins("checklist", at=0.2, gap=0.4))
b("وكثير منهم لا يشمون", da(value="👃 ✕", label="فقدان الشم أيضا", size=150))
b("وفي عام الفين وتسعه عشر", da(value="2019", label="جو كاميرون — إسكتلندا", size=160))
b("اكتشفت في الستينيات", st("clinic", [C("PLAIN", 0.4, "sitBack", "smile", 1, chair=True), C("DOC", 0.65, "shrug", "surprised", -1)], cam=PUSH, labels=[L("بلا مسكنات", y=0.18, ap="مسكنات", box=True)]))
b("وتبين ان عندها تغيرا", da(value="FAAH-OUT", label="تغير جيني نادر… وقلق أقل", size=130))
b("وهنا سؤال ما زال", da(value="مسكنات جديدة؟", label="لملايين المرضى بألم مزمن", size=120))
b("بعض الادويه التي جربت", da(value="البحث مستمر", label="نتائج أقل من المتوقع حتى الآن", size=120, color="coral"))
b("فالالم الذي نكرهه", bl("الألم… هو الحارس", "archive"), cap=False)
b("وفي الحلقه القادمه", bl("ماذا لو كان سمعك أقوى بمليون مرة؟", "archive", str2="الحلقة القادمة", at2=0.8), cap=False, sfx=[SFX("riser", 0, -12)])
b("ما رايك اخبرنا", dict(tpl="endscreen", q="لو كنت مكان يزن… هل كنت ستخرج؟", cast=["HUDA", "YAZAN", "TAREQ", "COACH", "DOC", "DAD"]), in_=FADE, cap=False)

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
story = {"title": "ماذا لو لم تشعر بالألم أبدًا؟", "duration": DUR, "shots": shots, "music": music, "sfx": []}
json.dump(story, open(f"{PROJ}/story/shots.json", "w"), ensure_ascii=False, indent=1)
d = [s["end"] - s["start"] for s in shots]; d.sort()
print(len(shots), "shots; median", round(d[len(d) // 2], 2), "min", round(d[0], 2), "max", round(d[-1], 2))
print("music:", [(m["mood"], round(m["start"]), round(m["end"])) for m in music])
