import asyncio, os, sys, json, hashlib, subprocess
import edge_tts
OUT=sys.argv[1]; PROXY=os.environ.get("HTTPS_PROXY")
SYL="أَأْ أَبْ أَتْ أَثْ أَجْ أَحْ أَخْ أَدْ أَذْ أَرْ أَزْ أَسْ إِشْ حَصْ حَضْ سِطْ فَظْ فَعْ فَغْ فِفْ حَقْ بَكْ سَلْ إِمْ قَنْ بَهْ بِوْ أُيْ بُكْ فُرْ بُرْ تُضْ أُطْ حُرْ صُمْ فُغْ".split()
WORDS="فَخْرٌ طَعْمٌ عَبْدٌ فَزْعٌ فَجْرٌ عَيْنٌ حَرْفٌ حَرْثٌ صَبْرٌ رَصْدٌ رَسْمٌ صَدْرٌ أَنْوَرُ أَذْهَبُ أَسْعَدُ أَحْمَدُ دَمْعٌ زَرْعٌ اِقْرَأْ اِسْمَحْ اِفْتَحْ اِلْعَبْ اِطْمَحْ اِشْبَعْ فَرْحَانُ اِشْرَبْ اِحْفَظْ اِبْدَأْ اِفْرَحْ اِمْرَحْ يُحْزِنُ يُنْصِفُ يُبْصِرُ فُنْدُقٌ بُنْدُقٌ يَسْمَعُ يَمْرَحُونَ يَرْكُضُونَ يَكْتُمُونَ يَلْعَبُونَ يَجْلِسُونَ يَدْخُلُونَ".split()
NAMES="ألف همزة باء تاء ثاء جيم حاء خاء دال ذال راء زاي سين شين صاد ضاد طاء ظاء عين غين فاء قاف كاف لام ميم نون هاء واو ياء".split()
MARKS=["فتحة","كسرة","ضمة","سكون","تنوين ضم"]
PH=["أحسنتِ يا سارة!","ممتاز يا سارة!","رائعة يا سارة!","برافو يا بطلة!","شاطرة يا سارة!","أحسنتِ يا سارة! أنهيتِ اللعبة وربحتِ نجومًا","الحرف صحيح، لكن انتبهي للحركة","ليس هذا الحرف","نحتاج","صحيح!","وهو من حروف القلقلة","هذا الحرف ليس ساكنًا","ليست هذه، اسمعي مرة ثانية","اسمعي جيدًا، وجربي مرة ثانية","ليست هذه الصورة، جربي مرة ثانية"]
# spoken form can differ from key (vocalized names help pronunciation)
SPOKEN={"ألف":"أَلِف","همزة":"هَمْزَة","فتحة":"فَتْحَة","كسرة":"كَسْرَة","ضمة":"ضَمَّة","سكون":"سُكُون","تنوين ضم":"تَنْوِينُ ضَمّ","نحتاج":"نَحْتَاجُ"}
items=[(t,t) for t in SYL+WORDS]+[(t,SPOKEN.get(t,t)) for t in NAMES+MARKS]+[(t,SPOKEN.get(t,t)) for t in PH]
sem=asyncio.Semaphore(4); manifest={}
async def one(key,text):
    h=hashlib.md5(key.encode()).hexdigest()[:10]; raw=f"{OUT}/{h}.raw.mp3"; fin=f"{OUT}/{h}.mp3"
    manifest[h]=key
    if os.path.exists(fin): return
    async with sem:
        for a in range(4):
            try:
                await edge_tts.Communicate(text,"ar-SA-HamedNeural",rate="-15%",proxy=PROXY).save(raw); break
            except Exception as e:
                if a==3: print("FAIL",key,e); return
                await asyncio.sleep(2)
    subprocess.run(["ffmpeg","-y","-v","error","-i",raw,"-af","silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,apad=pad_dur=0.08","-ac","1","-ar","22050","-b:a","40k",fin],check=True)
    os.remove(raw)
async def main():
    await asyncio.gather(*(one(k,t) for k,t in items))
    json.dump(manifest,open(f"{OUT}/manifest.json","w",encoding="utf8"),ensure_ascii=False)
    print(len(items),"items")
asyncio.run(main())
