# usage: split.py in.mp3 outdir name1 name2 ...  -> cuts at the N-1 longest silences
import sys, subprocess, re
src, out, names = sys.argv[1], sys.argv[2], sys.argv[3:]
n = len(names)
def silences(db):
    r = subprocess.run(["ffmpeg","-hide_banner","-i",src,"-af",f"silencedetect=noise={db}dB:d=0.15","-f","null","-"],capture_output=True,text=True).stderr
    st=[float(x) for x in re.findall(r"silence_start: ([\d.]+)",r)]; en=[float(x) for x in re.findall(r"silence_end: ([\d.]+)",r)]
    return list(zip(st,en))
dur=float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",src],capture_output=True,text=True).stdout)
for db in (-38,-35,-32,-42,-30):
    sil=[(a,b) for a,b in silences(db) if a>0.05 and b<dur-0.05]
    if len(sil)>=n-1: break
if len(sil)<n-1: sys.exit(f"FAIL {src}: found {len(sil)} gaps, need {n-1}")
gaps=sorted(sorted(sil,key=lambda g:g[1]-g[0],reverse=True)[:n-1])
cuts=[0]+[ (a+b)/2 for a,b in gaps ]+[dur]
for i,name in enumerate(names):
    s,e=cuts[i],cuts[i+1]
    subprocess.run(["ffmpeg","-y","-v","error","-ss",f"{s:.3f}","-to",f"{e:.3f}","-i",src,
      "-af","silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,apad=pad_dur=0.08",
      "-ac","1","-ar","22050","-b:a","40k",f"{out}/{name}.mp3"],check=True)
print("OK",src,[round(b-a,2) for a,b in gaps])
