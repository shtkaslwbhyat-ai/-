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
FAM = lambda bro="neutral", you="surprised", mom="sad": [C("DAD", 0.2, "stand", "neutral", 1, s=1.3), C("YOU", 0.38, "stand", you, 1, s=1.4), C("MOM", 0.62, "sit", mom, -1, chair=True, s=1.35), C("BRO", 0.8, "sit", bro, -1, chair=True, s=1.35)]
b("تعود الى البيت في المساء", dict(tpl="title", lines=["ماذا لو أصرّ أهلك", "أن شخصًا غريبًا هو أخوك الحقيقي؟"]), bars="scope", cap=False, sfx=[SFX("riser", 0, -12)])
b("فتجد في الصاله شابا", st("home", FAM(), cam=PUSH))
b("امك تبكي وتمسك يده", st("home", [C("MOM", 0.45, "sit", "sad", 1, chair=True, s=1.7), C("BRO", 0.62, "sit", "neutral", -1, chair=True, s=1.7)], cam=IN))
b("وابوك يقول بصوت هادئ", st("home", [C("DAD", 0.5, "talk", "neutral", 1, s=1.8)], cam=PUSH, labels=[L("«هذا أخوك الحقيقي»", y=0.18, box=True, at=1.2)]))
b("ماذا لو اصر اهلك", bl("ماذا لو أصرّ أهلك أن شخصًا غريبًا هو أخوك الحقيقي؟", "archive", size=56), cap=False, sfx=[SFX("stinger", 0.1, -10)])
b("تنظر اليه فترى عينيك", fc("BRO", "home", "neutral", side=0.0))
b("الضحكه نفسها", st("home", [C("YOU", 0.4, "laugh", "laugh", 1, s=1.6), C("BRO", 0.6, "laugh", "laugh", -1, s=1.6)], cam=DRIFT))
b("ثم يرفع ابوك ورقه", ins("dnapaper"), sfx=[SFX("whoosh", 0.1, -12)])
b("وتوامك سامي الذي كبرت", st("bedroom", [C("YOUKID", 0.4, "stand", "laugh", 1, s=1.3), C("SAMI", 0.6, "stand", "laugh", -1, kid=True, s=1.3)], so=dict(mood="day"), cam=PULL, labels=[L("سامي", x=0.6, y=0.22, box=True)]))
b("ليس اخاك بالدم", ins("dnapaper", result="ليس أخاك بالدم ✗", bad=True), sfx=[SFX("impact", 1.0, -10)], music_cut="tension")
b("في المستشفي يوم ولدت", ins("wristbands"))
b("في البدايه يبدو الامر", st("city", [C("YOU", 0.42, "walk", "smile", 1, s=1.5), C("BRO", 0.58, "walk", "smile", 1, s=1.5)], so=dict(mood="day"), cam=PUSH), music_cut="hopeful")
b("اخ جديد يشبهك كانه", fc("YOU", "home", "smile", side=0.3, rimSide=1))
b("هذا خيال", bl("هذا خيال… لكنه حدث فعلًا", "archive", coral=True), cap=False)
b("وفي اخر هذه الحلقه ستعرف", bl("في آخر الحلقة: الدم أم السنون؟", "archive", size=62), cap=False)
b("في شهر ديسمبر من عام", da(value="ديسمبر 1988", label="كولومبيا", size=170), in_=DIP, music_cut="calm")
b("ولد في مستشفي بالعاصمه", sc("clinic", [C("JORGE", 0.42, "stand", "neutral", 1, kid=True, s=1.2), C("WILLIAM", 0.58, "stand", "neutral", -1, kid=True, s=1.2)], cam=PUSH, labels=[L("بوغوتا: خورخي وويليام", y=0.18, box=True)]))
b("وفي اليوم التالي في اقليم", sc("clinic", [C("CARLOS", 0.42, "stand", "neutral", 1, kid=True, s=1.2), C("WILBER", 0.58, "stand", "neutral", -1, kid=True, s=1.2)], cam=DRIFT, labels=[L("سانتاندير: كارلوس وويلبر", y=0.18, box=True)]))
b("كان كارلوس مريضا", sc("clinic", [C("CARLOS", 0.5, "lie", "sad", 1, kid=True, s=1.3)], cam=PUSH, labels=[L("نُقل إلى بوغوتا", y=0.18, box=True)]))
b("وهناك اختلط الطفلان", ins("wristbands", label="هنا اختلط الطفلان"), sfx=[SFX("whoosh", 1.2, -12)])
b("وتقول احدي الروايات", ins("wristbands", label="إحدى الروايات: الأساور سقطت", cam=IN))
b("فعاد ويليام مع ويلبر", ins("twinmap", names={"JORGE": "خورخي", "CARLOS": "كارلوس", "WILLIAM": "ويليام", "WILBER": "ويلبر"}))
b("وكبرت كل عائله", ins("twinmap", names={"JORGE": "خورخي", "CARLOS": "كارلوس", "WILLIAM": "ويليام", "WILBER": "ويلبر"}, cam=IN))
b("وهذا ليس غريبا", ins("eggsplit"))
b("اما التوامان غير المتطابقين", ins("eggsplit", cam=IN))
b("فلم يستغرب احد", st("home", [C("MOM", 0.5, "stand", "smile", 1, s=1.5), C("JORGE", 0.35, "stand", "smile", 1, kid=True, s=1.1), C("CARLOS", 0.65, "stand", "smile", -1, kid=True, s=1.1)], cam=PUSH))
b("كبر ويليام وويلبر في الريف", sc("city", [C("WILLIAM", 0.42, "walk", "smile", 1, s=1.4), C("WILBER", 0.58, "walk", "smile", 1, s=1.4)], so=dict(mood="dusk"), cam=DRIFT, labels=[L("الريف", y=0.18, box=True)]))
b("وكبر خورخي وكارلوس في العاصمه", sc("city", [C("JORGE", 0.42, "walk", "smile", 1, s=1.4), C("CARLOS", 0.58, "walk", "smile", 1, s=1.4)], so=dict(mood="day"), cam=PUSH, labels=[L("العاصمة", y=0.18, box=True)]))
b("حياتان مختلفتان", da(value="25 عامًا", label="ولا أحد يعرف", size=170))
b("وكل واحد منهم لا يعرف", fc("JORGE", "studio", "neutral", side=0.0))
b("ومرت خمسه وعشرون عاما", bl("بعد 25 عامًا…", "archive"), cap=False, in_=DIP, music_cut="calm")
b("ثم دخلت امراه تعمل", sc("bakery", [C("COWORKER", 0.35, "walk", "neutral", 1, s=1.5)], cam=PUSH, labels=[L("محل لحوم — بوغوتا", y=0.18, box=True)]))
b("فرات خلف المنضده رجلا", sc("bakery", [C("COWORKER", 0.32, "stand", "surprised", 1, s=1.5), C("WILLIAM", 0.66, "stand", "neutral", -1, s=1.6)], cam=IN))
b("لكنه لم يعرفها", fc("COWORKER", "bakery", "surprised", side=0.3, rimSide=1))
b("كان اسمه ويليام", sc("bakery", [C("WILLIAM", 0.5, "talk", "smile", 1, s=1.7)], cam=PUSH, labels=[L("ويليام", y=0.18, box=True)]))
b("وحين اخبرت خورخي", sc("studio", [C("COWORKER", 0.38, "talk", "surprised", 1, s=1.5), C("JORGE", 0.62, "laugh", "smile", -1, s=1.5)], cam=PUSH))
b("لكنهما لا يتشابهان ابدا", sc("studio", [C("JORGE", 0.5, "explain", "smile", 1, s=1.7)], cam=IN, labels=[L("«عندي توأم… لكننا لا نتشابه»", y=0.18, box=True)]))
b("ففتح خورخي صور ويليام", ins("phonepics", who=["WILLIAM", "WILLIAM", "WILLIAM", "WILLIAM"], hl=0, label="صور ويليام"), sfx=[SFX("pop", 0.3, -12)])
b("ثم راي في الصور شابا", ins("phonepics", who=["WILLIAM", "WILBER", "WILLIAM", "WILBER"], hl=1, label="ومن هذا؟!"))
b("وكان نسخه من كارلوس", ins("twinmap", names={"JORGE": "خورخي", "CARLOS": "كارلوس", "WILLIAM": "ويليام", "WILBER": "ويلبر"}, links=True), sfx=[SFX("shimmer", 0.6, -10)])
b("واكدت فحوص الحمض النووي", ins("dnapaper", result="توأمان متطابقان ✓", head="فحص الحمض النووي"))
b("والتقي الاربعه اخيرا", ins("twinmap", truth=True, expr="surprised", names={"JORGE": "خورخي", "CARLOS": "كارلوس", "WILLIAM": "ويليام", "WILBER": "ويلبر"}), music_cut="hopeful")
b("اربعه رجال ينظر كل", st("archive", [C("JORGE", 0.2, "stand", "surprised", 1, s=1.25), C("WILLIAM", 0.4, "stand", "surprised", -1, s=1.25), C("CARLOS", 0.6, "stand", "surprised", 1, s=1.25), C("WILBER", 0.8, "stand", "surprised", -1, s=1.25)], cam=PUSH))
b("ودرست قصتهم عالمه النفس", sc("studio", [C("SEGAL", 0.5, "explain", "smile", 1, s=1.6)], cam=PUSH, labels=[L("نانسي سيغال", y=0.18, box=True)]))
b("عنوانه اخوه بالصدفه", ins("news", head="إخوة بالصدفة — 2018", who="SEGAL"))
b("ورات فيها تجربه طبيعيه", da(value="جينات ⇄ حياة", label="تجربة طبيعية نادرة", size=140))
b("ثم صارت فيلما وثائقيا", da(value="2024", label="فيلم وثائقي على نتفليكس", size=200))
b("واذا اعجبتك القصه حتي الان", ins("likesub", label="أعجبتك القصة؟"), sfx=[SFX("pop", 0.3, -10)])
b("وهنا تبدا المشكله", bl("وهنا تبدأ المشكلة", "archive", coral=True), cap=False, music_cut="tension")
b("في الليله الاولي يجلس سامي", st("bedroom", [C("SAMI", 0.5, "sit", "sad", 1, s=1.5)], so=dict(mood="night"), cam=PULL))
b("ثم يسالك بصوت خافت", st("bedroom", [C("YOU", 0.38, "stand", "worried", 1, s=1.5), C("SAMI", 0.6, "sit", "sad", -1, s=1.5)], so=dict(mood="night"), cam=PUSH, labels=[L("«هل ما زلت أخاك؟»", y=0.18, box=True, at=0.6)]))
b("وانت لا تعرف الجواب", fc("YOU", "bedroom", "worried", side=0.0))
b("وفي الصباح يحكي لك", st("home", [C("YOU", 0.4, "sit", "neutral", 1, chair=True, s=1.5), C("BRO", 0.6, "talk", "sad", -1, chair=True, s=1.5)], so=dict(mood="day"), cam=PUSH))
b("كبر في قريه فقيره", st("city", [C("BRO", 0.5, "walk", "sad", 1, kid=True, s=1.2)], so=dict(mood="dusk"), cam=DRIFT, labels=[L("ترك المدرسة ليعمل", y=0.18, box=True)]))
b("وانت تعرف ان المقعد", st("classroom", [C("SAMI", 0.5, "sit", "smile", 1, chair=True, kid=True, s=1.3)], cam=PUSH))
b("كان مقعده هو", fc("BRO", "classroom", "sad", side=0.3, rimSide=1))
b("وهذا الثمن ليس خيالا", bl("وهذا الثمن ليس خيالًا", "archive", coral=True), cap=False, in_=DIP, music_cut="sad")
b("في عام الف وتسعمئه وثلاثه وخمسين", da(value="طوكيو 1953", label="طفلان… بفارق 13 دقيقة تقريبًا", size=150))
b("وبحسب حكم المحكمه", ins("wristbands", label="خطأ بعد الولادة مباشرة"))
b("ذهب احدهما الي عائله غنيه", da(value="غنية ⇄ فقيرة", label="حياتان تبدّلتا", size=140, color="coral"))
b("وفي العائله الفقيره مات", sc("home", [C("MOM", 0.5, "stand", "sad", 1, s=1.5), C("YOUKID", 0.35, "stand", "sad", 1, s=1.0), C("SALMA", 0.65, "stand", "sad", -1, s=1.0)], so=dict(mood="night"), cam=PUSH, labels=[L("ثلاثة أطفال ومساعدات الدولة", y=0.18, box=True)]))
b("كبر الطفل وصار سائق", sc("city", [C("TRUCKER", 0.5, "walk", "neutral", 1, s=1.6)], so=dict(mood="dusk"), cam=DRIFT, labels=[L("سائق شاحنة", y=0.18, box=True)]))
b("اما الطفل الاخر فكبر", sc("studio", [C("RICHMAN", 0.5, "stand", "smile", 1, s=1.6)], cam=PUSH, labels=[L("رئيس شركة عقارات", y=0.18, box=True)]))
b("وبعد عقود لاحظ الاخوه", sc("home", [C("RICHMAN", 0.25, "stand", "neutral", 1, s=1.3), C("DAD", 0.5, "stand", "thinking", -1, s=1.3), C("ADAM", 0.65, "stand", "thinking", -1, s=1.3), C("KARIM", 0.8, "stand", "thinking", -1, s=1.3)], cam=PUSH, labels=[L("«لا يشبهنا»", y=0.18, box=True)]))
b("فطلبوا فحصا للحمض النووي", ins("dnapaper", result="2009: ليس أخاهم ✗", bad=True))
b("وفي نوفمبر من عام الفين وثلاثه عشر", ins("yencourt"), sfx=[SFX("impact", 0.6, -8)])
b("لان الخطا حرمه من فرصه", da(value="التعليم العالي", label="الفرصة التي ضاعت", size=140, color="coral"))
b("كان عمره ستين عاما", fc("TRUCKER", "home", "sad", side=0.0))
b("وكان الاخوه الثلاثه قد رفعوا", ins("yencourt", sub="طلبوا أكثر… وحكمت المحكمة بأقل", cam=IN))
b("فالمال يصل", bl("المال يصل… لكن السنين لا تعود", "archive", coral=True), cap=False)
b("وفي قصتنا تزداد الامور", st("home", [C("MOM", 0.4, "stand", "smile", 1, s=1.5), C("BRO", 0.55, "stand", "neutral", -1, s=1.5), C("SAMI", 0.85, "stand", "sad", -1, s=1.3)], cam=PUSH), music_cut="tension")
b("علي العشاء يضحك الجميع", st("home", [C("DAD", 0.2, "sit", "laugh", 1, chair=True, s=1.25), C("MOM", 0.38, "sit", "laugh", 1, chair=True, s=1.25), C("YOU", 0.56, "sit", "laugh", -1, chair=True, s=1.25), C("BRO", 0.76, "sit", "neutral", -1, chair=True, s=1.25)], cam=DRIFT))
b("وحين تنادي امك يا سامي", fc("SAMI", "home", "sad", side=0.3, rimSide=1))
b("وفي الجامعه يسالك اصدقاؤك", st("classroom", [C("ADAM", 0.25, "talk", "surprised", 1, s=1.3), C("YOU", 0.45, "stand", "worried", -1, s=1.3), C("BRO", 0.6, "stand", "neutral", -1, s=1.3), C("SAMI", 0.78, "stand", "sad", -1, s=1.3)], cam=PUSH))
b("وانت تجلس بين اخوين", st("home", [C("SAMI", 0.3, "sit", "sad", 1, chair=True, s=1.4), C("YOU", 0.5, "sit", "worried", 1, chair=True, s=1.4), C("BRO", 0.7, "sit", "neutral", -1, chair=True, s=1.4)], cam=PULL, labels=[L("يشبهك", x=0.7, y=0.2, box=True, at=1.5), L("يعرفك", x=0.3, y=0.2, box=True, at=2.4)]))
b("ثم تكتشف شيئا يخيفك", fc("YOU", "home", "surprised", side=0.0))
b("ولا تشعر بشيء", fc("BRO", "home", "neutral", side=0.3, rimSide=1))
b("وجه تعرف انه قريبك", da(icon="heart", value="لا شيء", label="القلب لا يتحرك", size=140, color="coral"))
b("والان الي المفاجاه", bl("المفاجأة", "archive"), cap=False, in_=DIP, music_cut="calm")
b("في عام الف وتسعمئه وثلاثه وعشرين", sc("clinic", [C("CAPGRAS", 0.5, "explain", "thinking", 1, s=1.6)], cam=PUSH, labels=[L("جوزيف كابغرا — 1923", y=0.18, box=True)]))
b("كانت مقتنعه بان زوجها", sc("home", [C("CAPWOMAN", 0.3, "stand", "scared", 1, s=1.5), C("DAD", 0.55, "stand", "neutral", -1, s=1.4), C("SALMA", 0.72, "stand", "neutral", -1, s=1.1)], cam=PUSH, labels=[L("«ليسوا هم!»", y=0.18, box=True, at=0.8)]))
b("تراهم وتعرف وجوههم", fc("CAPWOMAN", "home", "scared", side=0.0))
b("وصارت هذه الحاله تسمي", da(icon="brain", value="متلازمة كابغرا", label="الأهل… محتالون", size=130))
b("وهي ليست شائعه", da(value="نادرة", label="أمراض نفسية · الخرف · إصابات الرأس", size=170))
b("انها عكس قصتنا تماما", bl("عكس قصتنا تمامًا", "archive", coral=True), cap=False)
b("وفي عام الف وتسعمئه وسبعه وتسعين", sc("clinic", [C("HIRSTEIN", 0.38, "explain", "neutral", 1, s=1.5), C("RAMA", 0.62, "explain", "thinking", -1, s=1.5)], cam=PUSH, labels=[L("هيرستين وراماتشاندران — 1997", y=0.18, box=True)]))
b("بعد حادث سياره صار يعتقد", sc("home", [C("DSPAT", 0.35, "stand", "scared", 1, s=1.5), C("DAD", 0.6, "stand", "neutral", -1, s=1.4), C("MOM", 0.75, "stand", "neutral", -1, s=1.4)], cam=PUSH, labels=[L("المريض DS", y=0.18, box=True)]))
b("فعرضا عليه صورا لوجوه", ins("facegrid"))
b("عند اغلب الناس ترتفع", ins("skinresp"))
b("اما عنده فلم تكن", ins("skinresp", cam=IN), sfx=[SFX("impact", 0.3, -12)])
b("واقترح الباحثان تفسيرا", da(icon="brain", value="أعرف الوجه ≠ أشعر به", label="تفسير مقترح", size=120))
b("فيستنتج الدماغ هذا ليس", fc("DSPAT", "home", "scared", side=0.0))
b("اي ان العين تقول", da(value="العين: أبي ✓", label="القلب: لا شيء ✗", size=140, color="coral"))
b("وما زال العلماء يدرسون", da(value="قيد الدراسة", label="تفسير لم يُحسم", size=150))
b("وهنا المفاجاه الكبري", bl("الأخ في دماغك… إحساس لا ورقة", "archive"), cap=False, sfx=[SFX("stinger", 0.1, -10)])
b("انه احساس دافئ يبنيه", ar(hero=True, heroC="YOU", pose="stand", expr="smile", n=40, cards=["ضحك", "شجار", "ذكريات", "سنوات"], cardsX=[0.15, 0.38, 0.62, 0.85], cardsY=[0.25, 0.18, 0.18, 0.25], gap=0.5))
b("ولهذا يمكن لاخوين", st("bedroom", [C("YOU", 0.42, "laugh", "laugh", 1, s=1.5), C("SAMI", 0.58, "laugh", "laugh", -1, s=1.5)], so=dict(mood="day"), cam=PUSH))
b("ولهذا لا يتحرك قلبك", fc("YOU", "home", "sad", side=0.3, rimSide=1))
b("اما الثمن غير المتوقع", bl("الثمن: سنين لا تعود", "archive", coral=True), cap=False, sfx=[SFX("impact", 0.2, -10)], music_cut="sad")
b("انه ياخذ سنين لا تعود", ar(hero=True, heroC="BRO", pose="stand", expr="sad", n=40, cards=["طفولة", "مدرسة", "ذكريات"], cardsX=[0.2, 0.5, 0.8], gap=0.8))
b("والان الي ما وعدتك به", bl("الجواب الموعود", "archive"), cap=False, in_=DIP, sfx=[SFX("stinger", 0.1, -10)], music_cut="hopeful")
b("من هو اخوك الحقيقي فعلا الدم", da(value="الدم أم السنون؟", label="", size=150))
b("الجواب الدم يخبرك", da(value="الدم ← من أين جئت", label="السنون ← من أنت", size=110))
b("وليس عليك ان تختار", fc("YOU", "home", "smile", side=0.0))
b("فالاخوه لا تسحب بورقه", ins("dnapaper", result="الأخوّة لا تُسحب بورقة", cam=IN))
b("فالدماغ الذي صنع دفء", st("home", [C("YOU", 0.3, "sit", "laugh", 1, chair=True, s=1.35), C("BRO", 0.5, "sit", "laugh", -1, chair=True, s=1.35), C("SAMI", 0.7, "sit", "laugh", -1, chair=True, s=1.35)], cam=DRIFT))
b("وفي اخر قصتنا تدخل غرفه", st("bedroom", [C("YOU", 0.4, "walk", "smile", 1, s=1.4), C("BRO", 0.25, "walk", "neutral", 1, s=1.4), C("SAMI", 0.72, "sit", "sad", -1, s=1.4)], so=dict(mood="dusk"), cam=PUSH))
b("تجلس بينهما علي السرير", st("bedroom", [C("BRO", 0.32, "sit", "neutral", 1, s=1.4), C("YOU", 0.5, "sit", "smile", -1, s=1.4), C("SAMI", 0.68, "sit", "sad", -1, s=1.4)], so=dict(mood="dusk"), cam=IN, labels=[L("«أنت أخي»", y=0.18, box=True, at=1.4)]))
b("ثم تلتفت الي الاخر", st("bedroom", [C("BRO", 0.32, "sit", "smile", 1, s=1.4), C("YOU", 0.5, "sit", "smile", 1, s=1.4), C("SAMI", 0.68, "sit", "smile", -1, s=1.4)], so=dict(mood="dusk"), cam=DRIFT, labels=[L("«سنبدأ من اليوم»", y=0.18, box=True, at=1.4)]))
b("فيبتسم سامي لاول مره", st("bedroom", [C("BRO", 0.32, "sit", "laugh", 1, s=1.4), C("YOU", 0.5, "sit", "laugh", 1, s=1.4), C("SAMI", 0.68, "sit", "laugh", -1, s=1.4)], so=dict(mood="dusk"), cam=PUSH))
b("فقد كان عندك اخ واحد", da(value="1 ← 2", label="صار عندك أخوان", size=200))
b("واذا استمتعت بهذه القصه", ins("likesub", label="إعجاب + اشتراك + شاركها مع أخيك"), sfx=[SFX("pop", 0.3, -10)])
b("وفي الحلقه القادمه", bl("ماذا لو بدأت أمك تكبر بالعكس… وأنت تكبر؟", "archive", str2="الحلقة القادمة", at2=0.8, size=56), cap=False, sfx=[SFX("riser", 0, -12)])
b("والان سؤال الحلقه", dict(tpl="endscreen", q="لو خُيّرت: تعرف الحقيقة… حتى لو غيّرت عائلتك كلها؟", cast=["JORGE", "WILLIAM", "YOU", "BRO", "SAMI", "MOM"]), in_=FADE, cap=False)


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
story = {"title": "ماذا لو أصرّ أهلك أن شخصًا غريبًا هو أخوك الحقيقي؟", "duration": DUR, "shots": shots, "music": music, "sfx": []}
json.dump(story, open(f"{PROJ}/story/shots.json", "w"), ensure_ascii=False, indent=1)
d = [s["end"] - s["start"] for s in shots]; d.sort()
print(len(shots), "shots; median", round(d[len(d) // 2], 2), "min", round(d[0], 2), "max", round(d[-1], 2))
print("music:", [(m["mood"], round(m["start"]), round(m["end"])) for m in music])
