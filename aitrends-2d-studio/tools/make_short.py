"""tools/make_short.py — cut a vertical 9:16 Short from a finished episode.

  python3 tools/make_short.py --project projects/<slug> --video <episode.mp4> \
      --start "<first words of the clip>" --end "<last words of the clip>" \
      --hook "<hook line, <b>highlight</b> allowed>" --out <short.mp4> [--cta "..."]

Finds the phrases in timeline/words.json (Arabic diacritics ignored), snaps the cut to word boundaries,
and builds 1080x1920: blurred full-frame background, the episode frame (center 4:3 crop) in the middle,
hook text on top and a call-to-action pill at the bottom. Refuses clips longer than 59 s.
"""
import argparse, json, os, re, subprocess, sys

def norm(w):
    w = re.sub(r"[ً-ْٰـ]", "", w)
    w = re.sub(r"[آأإ]", "ا", w).replace("ة", "ه").replace("ى", "ي")
    return re.sub(r"[^\w']+", "", w.lower())

def find(tok, phrase, frm=0):
    p = [x for x in (norm(t) for t in phrase.split()) if x]
    for i in range(frm, len(tok) - len(p) + 1):
        if tok[i:i + len(p)] == p: return i, len(p)
    sys.exit(f"phrase not found: {phrase}")

ap = argparse.ArgumentParser()
ap.add_argument("--project", required=True); ap.add_argument("--video", required=True)
ap.add_argument("--start", required=True); ap.add_argument("--end", required=True)
ap.add_argument("--hook", required=True); ap.add_argument("--out", required=True)
ap.add_argument("--cta", default="الحلقة كاملة على قناة عالم لو")
a = ap.parse_args()
W = json.load(open(os.path.join(a.project, "timeline/words.json"))); W = W.get("words", W)
tok = [norm(w["word"]) for w in W]
i, _ = find(tok, a.start); j, n = find(tok, a.end, i)
t0 = max(0.0, W[i]["start"] - 0.12); t1 = W[j + n - 1]["end"] + 0.45
dur = t1 - t0
if dur > 59: sys.exit(f"clip is {dur:.1f}s — too long for a Short (max 59 s)")
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ov = a.out.rsplit(".", 1)[0] + "_overlay.png"
env = dict(os.environ, CHROME_PATH=os.environ.get("CHROME_PATH", "/opt/pw-browsers/chromium"))
subprocess.run(["node", os.path.join(root, "tools/short_overlay.mjs"), a.hook, a.cta, ov], check=True, env=env, cwd=root)
fade = max(0.0, dur - 0.4)
fc = ("[0:v]split[a][b];"
      "[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:3,eq=brightness=-0.12[bg];"
      "[b]crop=1200:1080:360:0,scale=1080:972[fg];"
      "[bg][fg]overlay=0:474[v1];[v1][1:v]overlay=0:0,"
      f"fade=t=in:st=0:d=0.25,fade=t=out:st={fade:.2f}:d=0.4[v]")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t0:.3f}", "-t", f"{dur:.3f}", "-i", a.video, "-i", ov,
                "-filter_complex", fc, "-map", "[v]", "-map", "0:a:0",
                "-af", f"afade=t=in:st=0:d=0.2,afade=t=out:st={fade:.2f}:d=0.4",
                "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-pix_fmt", "yuv420p", "-r", "30",
                "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", a.out], check=True)
os.remove(ov)
print(f"{a.out}  {dur:.1f}s  ({t0:.1f} → {t1:.1f})")
