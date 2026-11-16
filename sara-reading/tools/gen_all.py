import asyncio, os, sys, json, hashlib, subprocess, unicodedata
import edge_tts
items_file, OUT = sys.argv[1], sys.argv[2]; PROXY=os.environ.get("HTTPS_PROXY")
N=lambda s: unicodedata.normalize("NFC", s)
items=[N(x) for x in json.load(open(items_file, encoding="utf8"))]
extra=["ليست هذه الصورة، جربي مرة ثانية","أحسنتِ يا سارة! أنهيتِ اللعبة وربحتِ نجومًا","ليس هذا الحرف","نحتاج","صحيح!","وهو من حروف القلقلة","اختاري الكلمة أولًا"]
for e in extra:
    if N(e) not in items: items.append(N(e))
SPOKEN={"ألف":"أَلِف","همزة":"هَمْزَة","فتحة":"فَتْحَة","كسرة":"كَسْرَة","ضمة":"ضَمَّة","سكون":"سُكُون","شدة":"شَدَّة",
 "تنوين ضم":"تَنْوِينُ ضَمّ","تنوين فتح":"تَنْوِينُ فَتْح","تنوين كسر":"تَنْوِينُ كَسْر","نحتاج":"نَحْتَاجُ",
 "ألف مقصورة":"أَلِفٌ مَقْصُورَة","تاء مربوطة":"تَاءٌ مَرْبُوطَة"}
sem=asyncio.Semaphore(5); manifest={}; fails=[]
async def one(key):
    h=hashlib.md5(key.encode()).hexdigest()[:10]; raw=f"{OUT}/{h}.raw.mp3"; fin=f"{OUT}/{h}.mp3"
    manifest[h]=key
    if os.path.exists(fin): return
    text=SPOKEN.get(key,key)
    async with sem:
        for a in range(5):
            try:
                await edge_tts.Communicate(text,"ar-SA-HamedNeural",rate="-15%",proxy=PROXY).save(raw)
                if os.path.getsize(raw)>500: break
            except Exception as e:
                if a==4: fails.append(key); return
            await asyncio.sleep(1.5*(a+1))
    subprocess.run(["ffmpeg","-y","-v","error","-i",raw,"-af","silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,apad=pad_dur=0.08","-ac","1","-ar","22050","-b:a","40k",fin],check=True)
    os.remove(raw)
async def main():
    await asyncio.gather(*(one(k) for k in items))
    json.dump(manifest,open(f"{OUT}/manifest.json","w",encoding="utf8"),ensure_ascii=False)
    print(len(items),"items; fails:",fails)
asyncio.run(main())
