"""tools/chapters.py — YouTube chapters from a project's shots, by anchor phrase.

  python3 tools/chapters.py --project projects/<slug> chapters.txt

chapters.txt: one chapter per line, "anchor words | chapter title" (anchor = first words of the
spoken line where the chapter starts; Arabic diacritics/hamza forms ignored). The first chapter is
forced to 0:00. Warns when a chapter is shorter than 10 s (YouTube ignores chapters then).
"""
import argparse, json, re, sys
def norm(w):
    w = re.sub(r"[ً-ْٰـ]", "", w); w = re.sub(r"[آأإ]", "ا", w).replace("ة", "ه").replace("ى", "ي")
    return re.sub(r"[^\w\s]+", "", w)
ap = argparse.ArgumentParser(); ap.add_argument("--project", required=True); ap.add_argument("spec"); a = ap.parse_args()
W = json.load(open(f"{a.project}/timeline/words.json")); W = W.get("words", W); tok = [norm(w["word"]).strip() for w in W]
out, pos = [], 0
for line in open(a.spec):
    if "|" not in line: continue
    anc, title = (x.strip() for x in line.split("|", 1)); p = [norm(x) for x in anc.split() if norm(x)]
    for i in range(pos, len(tok) - len(p) + 1):
        if tok[i:i + len(p)] == p: break
    else: sys.exit(f"anchor not found: {anc}")
    t = 0.0 if not out else W[i]["start"]; pos = i + 1; out.append((t, title))
for k, (t, title) in enumerate(out):
    nxt = out[k + 1][0] if k + 1 < len(out) else W[-1]["end"]
    print(f"{int(t // 60)}:{int(t % 60):02d} {title}" + ("   ⚠ أقل من 10 ثوان" if nxt - t < 10 else ""))
