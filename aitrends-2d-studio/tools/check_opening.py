"""tools/check_opening.py — verify the story cold-open timing before rendering.

  python3 tools/check_opening.py --project projects/<p> --question "ماذا لو ..." [--bridge "هذا خيال"]

Channel rules (bible, 2026-11-18/21): the title question is spoken before 0:15 and the bridge
to the first real case ("هذا خيال…") starts before 0:55. Ep14 shipped a first cut with the
question at 0:24 because lines were added to the opening; this catches it from words.json.
Exit 1 when a rule is broken or a phrase is not found.
"""
import argparse, json, re, sys
ap = argparse.ArgumentParser(); ap.add_argument("--project", required=True); ap.add_argument("--question", required=True)
ap.add_argument("--bridge", default="هذا خيال"); ap.add_argument("--qmax", type=float, default=15.0); ap.add_argument("--bmax", type=float, default=55.0)
a = ap.parse_args()
W = json.load(open(f"{a.project}/timeline/words.json")); W = W.get("words", W)
def n(w):
    w = re.sub(r"[ً-ْٰـ]", "", w); w = re.sub(r"[آأإ]", "ا", w).replace("ة", "ه").replace("ى", "ي"); return re.sub(r"[^\w]+", "", w)
T = [n(w["word"]) for w in W]
def find(ph):
    p = [n(x) for x in ph.split() if n(x)][:4]
    for i in range(len(T) - len(p) + 1):
        if T[i:i + len(p)] == p: return W[i]["start"]
ok = True
for name, ph, lim in (("question", a.question, a.qmax), ("bridge", a.bridge, a.bmax)):
    t = find(ph)
    if t is None: print(f"❌ {name}: phrase not found"); ok = False
    elif t > lim: print(f"❌ {name} at {t:.1f}s (rule: before {lim:.0f}s) — shorten the opening, don't add to it"); ok = False
    else: print(f"✅ {name} at {t:.1f}s (< {lim:.0f}s)")
sys.exit(0 if ok else 1)
