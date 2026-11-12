"""tools/make_voice.py — the channel voiceover in one command.

  python3 tools/make_voice.py <script.txt> <out_dir> [--min 480] [--max 600]

Splits the vowelized script at sentence ends (~2800 chars per chunk), voices each chunk with
Edge TTS (Bassel, ar-IQ-BasselNeural, --rate=+15% --pitch=-4Hz) through the session proxy,
pads 0.3 s, concatenates, trims long silences with tools/tighten_voice.sh and writes
<out_dir>/voiceover.mp3. Prints words, duration and pace; exits 2 when the duration is
outside [--min, --max] seconds (channel rule: 8–10 minutes), so the writer adds/cuts a scene first.
"""
import argparse, os, re, subprocess, sys
VOICE, RATE, PITCH = "ar-IQ-BasselNeural", "+15%", "-4Hz"
ap = argparse.ArgumentParser(); ap.add_argument("script"); ap.add_argument("out")
ap.add_argument("--min", type=float, default=480); ap.add_argument("--max", type=float, default=600)
a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
t = open(a.script).read().strip()
sents = re.findall(r".+?(?:\.\.\.|[.؟?:!])(?:\s+|$)", t, flags=re.S) or [t]
if "".join(sents).replace(" ", "").replace("\n", "") != t.replace(" ", "").replace("\n", ""): sents.append(t[len("".join(sents)):])
chunks, cur = [], ""
for s in sents:
    if len(cur) + len(s) > 2800 and cur: chunks.append(cur.strip()); cur = ""
    cur += s
chunks.append(cur.strip())
env = dict(os.environ, SSL_CERT_FILE=os.environ.get("SSL_CERT_FILE", "/root/.ccr/ca-bundle.crt"))
proxy = ["--proxy", os.environ["HTTPS_PROXY"]] if os.environ.get("HTTPS_PROXY") else []
wavs = []
for i, c in enumerate(chunks, 1):
    txt, mp3, wav = (os.path.join(a.out, f"c{i}.{e}") for e in ("txt", "mp3", "wav"))
    open(txt, "w").write(c)
    for attempt in range(3):
        r = subprocess.run(["edge-tts", *proxy, "--voice", VOICE, f"--rate={RATE}", f"--pitch={PITCH}", "-f", txt, "--write-media", mp3], env=env, capture_output=True, text=True, timeout=300)
        if r.returncode == 0 and os.path.getsize(mp3) > 1000: break
    else: sys.exit(f"edge-tts failed on chunk {i}: {r.stderr[-300:]}")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", mp3, "-af", "apad=pad_dur=0.3", "-ar", "44100", "-ac", "1", wav], check=True)
    wavs.append(wav)
lst = os.path.join(a.out, "list.txt"); open(lst, "w").write("".join(f"file '{os.path.abspath(w)}'\n" for w in wavs))
joined, final = os.path.join(a.out, "joined.mp3"), os.path.join(a.out, "voiceover.mp3")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c:a", "libmp3lame", "-b:a", "192k", joined], check=True)
subprocess.run(["bash", os.path.join(os.path.dirname(os.path.abspath(__file__)), "tighten_voice.sh"), joined, final], check=True, capture_output=True)
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", final], capture_output=True, text=True).stdout)
words = len(t.split())
print(f"{final}\n  words {words} | chunks {len(chunks)} | duration {int(dur//60)}:{dur%60:04.1f} | pace {words/dur*60:.0f} wpm")
if dur < a.min: print(f"  TOO SHORT: need about {int((a.min-dur)/60*words/dur*60)+20} more words (rule: >= {a.min/60:.0f} min)"); sys.exit(2)
if dur > a.max: print(f"  TOO LONG: cut about {int((dur-a.max)/60*words/dur*60)+20} words (rule: <= {a.max/60:.0f} min)"); sys.exit(2)
print("  OK: within the channel's 8–10 minute rule")
