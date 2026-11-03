// Voiceover config: one ElevenLabs clip per scene (voice: Nasser AlJubaily, model eleven_v4).
// Drop the MP3s into public/vo/ — scene lengths adapt automatically to each clip.
export const FPS = 30;
export const PAD_SECONDS = 0.5;

export type SceneId = "hook" | "reveal" | "step1" | "step2" | "step3" | "step4" | "cta";

export const SCENES: { id: SceneId; audio: string; fallbackSeconds: number; text: string }[] = [
  { id: "hook", audio: "vo/s1.mp3", fallbackSeconds: 6.56, text: "تخيّل إنك تسوّي فيديو احترافي كامل... بدون ما تفتح أي برنامج مونتاج. ولا ثانية!" },
  { id: "reveal", audio: "vo/s2.mp3", fallbackSeconds: 7, text: "هذا الفيديو اللي تشوفه الحين؟ انصنع بالكامل عن طريق كلود كود. والصوت اللي تسمعه؟ من إليفن لابز." },
  { id: "step1", audio: "vo/s3.mp3", fallbackSeconds: 8, text: "الخطوة الأولى: افتح كلود كود، واكتب له فكرتك بكلام بسيط. مثلاً: سوّ لي فيديو يشرح كذا، وابدأ بهوك قوي." },
  { id: "step2", audio: "vo/s4.mp3", fallbackSeconds: 8, text: "الخطوة الثانية: كلود يكتب السكربت، ويختار الصوت المناسب من إليفن لابز، ويولّد التعليق الصوتي تلقائياً." },
  { id: "step3", audio: "vo/s5.mp3", fallbackSeconds: 8.64, text: "الخطوة الثالثة: يبني المشاهد بالكود باستخدام ريموشن. حركات، ألوان، ونصوص متزامنة مع الصوت." },
  { id: "step4", audio: "vo/s6.mp3", fallbackSeconds: 5.68, text: "وأخيراً: يرندر الفيديو، ويطلع لك ملف جاهز للنشر على أي منصة." },
  { id: "cta", audio: "vo/s7.mp3", fallbackSeconds: 6, text: "يعني أنت عليك الفكرة... والباقي على كلود. جرّبها اليوم، وتابعني لأفكار أكثر!" },
];

export const COLORS = {
  bg: "#141210",
  bg2: "#26201b",
  orange: "#D97757",
  cream: "#F4EDE4",
  muted: "#A89F94",
  green: "#7BC47F",
};
