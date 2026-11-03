// Generates all 7 scene voiceovers with ElevenLabs into public/vo/.
// Usage: ELEVENLABS_API_KEY=... node generate-voiceover.mjs
import { writeFileSync, mkdirSync, existsSync } from "node:fs";

const VOICE_ID = "cFUFIbKkO2iZFwS8cRnY"; // Nasser AlJubaily - Authentic Saudi Pro
const MODEL = "eleven_v3";
const LINES = [
  "[excited] تخيّل إنك تسوّي فيديو احترافي كامل... بدون ما تفتح أي برنامج مونتاج. ولا ثانية!",
  "هذا الفيديو اللي تشوفه الحين؟ انصنع بالكامل عن طريق كلود كود. والصوت اللي تسمعه؟ من إليفن لابز.",
  "الخطوة الأولى: افتح كلود كود، واكتب له فكرتك بكلام بسيط. مثلاً: سوّ لي فيديو يشرح كذا، وابدأ بهوك قوي.",
  "الخطوة الثانية: كلود يكتب السكربت، ويختار الصوت المناسب من إليفن لابز، ويولّد التعليق الصوتي تلقائياً.",
  "الخطوة الثالثة: يبني المشاهد بالكود باستخدام ريموشن. حركات، ألوان، ونصوص متزامنة مع الصوت.",
  "وأخيراً: يرندر الفيديو، ويطلع لك ملف جاهز للنشر على أي منصة.",
  "يعني أنت عليك الفكرة... والباقي على كلود. جرّبها اليوم، وتابعني لأفكار أكثر!",
];

mkdirSync("public/vo", { recursive: true });
for (const [i, text] of LINES.entries()) {
  const file = `public/vo/s${i + 1}.mp3`;
  if (existsSync(file) && !process.argv.includes("--force")) { console.log("skip", file); continue; }
  const res = await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${VOICE_ID}`, {
    method: "POST",
    headers: { "xi-api-key": process.env.ELEVENLABS_API_KEY, "Content-Type": "application/json", Accept: "audio/mpeg" },
    body: JSON.stringify({ text, model_id: MODEL }),
  });
  if (!res.ok) throw new Error(`${file}: ${res.status} ${await res.text()}`);
  writeFileSync(file, Buffer.from(await res.arrayBuffer()));
  console.log("wrote", file);
}
