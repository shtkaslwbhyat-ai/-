"""tools/check_inserts.py — warn about reused inserts that carry text from an older episode.

  python3 tools/check_inserts.py --project projects/<name>

Some inserts in shots/_tpl.js were written for one episode and draw fixed Arabic words
(e.g. clock24 = "23 ساعة يقظة / 1 نوم" from the sleep episode). Reusing them silently put the
wrong words on screen in Ep11/Ep12. This tool lists every shot that uses one of them so the
storyboard can swap it before rendering. Exit code 1 when anything is found.
"""
import argparse, json, sys
STALE = {
    "clock24": "23 ساعة يقظة / 1 نوم (حلقة النوم)",
    "nerve": "كلمة البوابة (حلقة الألم)",
    "breath": "نفسًا / دقيقة (حلقة النوم)",
    "dolphin": "نائم / مستيقظ مع القمر (حلقة النوم)",
    "eeg": "نوم عميق / استيقاظ (حلقة النوم)",
    "novel": "رواية العطر 1985 (حلقة الشم)",
    "madeleine": "بروست والكعكة (حلقة الشم)",
    "sniffbars": "أعداد خلايا الشم (حلقة الشم)",
    "shirts": "اختبار القمصان (حلقة الشم)",
    "xray": "أشعة الكسور (حلقة الألم)",
    "scoreboard": "لوحة نتيجة كرة القدم",
    "phases": "مراحل النوم",
    "snellen": "لوحة فحص النظر (حلقة البصر)",
}
ap = argparse.ArgumentParser(); ap.add_argument("--project", required=True); a = ap.parse_args()
shots = json.load(open(f"{a.project}/story/shots.json"))["shots"]
hits = [(s["id"], round(s["start"], 1), s["params"]["kind"]) for s in shots
        if s["params"].get("tpl") == "insert" and s["params"].get("kind") in STALE]
for sid, t0, k in hits: print(f"⚠️  {sid} @{t0}s insert '{k}': {STALE[k]}")
print(f"{len(hits)} reused insert(s) with episode-specific text" if hits else "OK: no stale inserts")
sys.exit(1 if hits else 0)
