// Video 3 — "3 دروس": my own script on the same journey idea. Clips in public/vo3/.
export type LessonSceneId = "hook" | "l1" | "l2" | "l3" | "result" | "outro";

export const LESSON_SCENES: { id: LessonSceneId; audio: string; fallbackSeconds: number; text: string }[] = [
  { id: "hook", audio: "vo3/s1.mp3", fallbackSeconds: 6.3, text: "أول فيديو سويته بالذكاء الاصطناعي... كان كارثة. والثالث؟ شوفه بنفسك." },
  { id: "l1", audio: "vo3/s2.mp3", fallbackSeconds: 6.1, text: "الدرس الأول: كلود كود ذكي، بس بدون أدوات... يطلّع لك فيديو بدائي." },
  { id: "l2", audio: "vo3/s3.mp3", fallbackSeconds: 7, text: "الدرس الثاني: أضف سكل ريموشن... وفجأة صار يفهم الحركة، والتوقيت، والتصميم." },
  { id: "l3", audio: "vo3/s4.mp3", fallbackSeconds: 7, text: "الدرس الثالث: الصورة نص القصة. اربطه بإليفن لابز، وخلّه يعطي الفيديو صوت... وروح." },
  { id: "result", audio: "vo3/s5.mp3", fallbackSeconds: 6, text: "من فكرة... لفيديو جاهز للنشر. وأنا ما لمست برنامج مونتاج." },
  { id: "outro", audio: "vo3/s6.mp3", fallbackSeconds: 10, text: "الخلاصة؟ ما تحتاج تكون مونتير... تحتاج تعرف وش تطلب، ومن وين تجيب الأدوات. احفظ الفيديو، وسوّ أول فيديو لك اليوم." },
];
