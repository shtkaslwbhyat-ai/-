"""tools/schedule.py — print the publishing calendar with episode and short TITLES (not folder numbers).

  python3 tools/schedule.py [--from 2026-11-26] [--to 2026-12-31]

Reads docs/publishing-plan.md, deliverables/*/upload.md (episode title) and
deliverables/*/shorts/shorts.md (short titles). The owner asked for the schedule by name (2026-11-26).
"""
import argparse, glob, re, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ap = argparse.ArgumentParser(); ap.add_argument("--from", dest="frm", default="0000"); ap.add_argument("--to", default="9999"); a = ap.parse_args()
T, E = {}, {}
for f in glob.glob(f"{ROOT}/deliverables/*/shorts/shorts.md"):
    ep = f.split("/")[-3]
    for m in re.finditer(r"^###\s+(\S+)\s+·\s+(.+)$", open(f).read(), re.M):
        T.setdefault(f"{ep[:2]}/{m.group(1)}", m.group(2).replace("#shorts", "").strip())
for f in glob.glob(f"{ROOT}/deliverables/*/upload.md"):
    m = re.search(r"## العنوان\n(.+)", open(f).read())
    if m: E[f.split("/")[-2]] = m.group(1).strip()
print("| التاريخ | شورت 15:00 | حلقة 20:00 |\n|---|---|---|")
for l in open(f"{ROOT}/docs/publishing-plan.md").read().split("\n"):
    if not l.startswith("| 20"): continue
    c = [x.strip() for x in l.strip("|").split("|")]
    if not (a.frm <= c[0] <= a.to): continue
    s = c[2].replace("✅ ", "").split(" ")[0]; k = s[:2] + "/" + s.split("/", 1)[1] if "/" in s else s
    m = re.search(r"\((\d\d-[a-z]+)\)", c[3])
    print(f"| {c[0]} {c[1]} | {T.get(k, s)} | {E.get(m.group(1)) if m else c[3]} |")
