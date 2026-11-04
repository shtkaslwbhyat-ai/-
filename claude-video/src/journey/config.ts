// Video 2 — "رحلتي في إنشاء فيديو عبر Claude Code". One ElevenLabs clip per scene in public/vo2/.
export type JourneySceneId = "hook" | "try1" | "search" | "try2" | "connect" | "result" | "outro";

export const JOURNEY_SCENES: { id: JourneySceneId; audio: string; fallbackSeconds: number; text: string }[] = [
  { id: "hook", audio: "vo2/s1.mp3", fallbackSeconds: 4, text: "جرّبت أسوّي فيديو عن طريق كلود كود... وهذا اللي صار!" },
  { id: "try1", audio: "vo2/s2.mp3", fallbackSeconds: 7, text: "في المرة الأولى، بدون ما أضيف أي سكل، طلع لي فيديو... بس صراحة، ما كانت النتيجة اللي أبيها." },
  { id: "search", audio: "vo2/s3.mp3", fallbackSeconds: 5, text: "بعدها بحثت... ولقيت إني لازم أفعّل إضافة اسمها ريموشن." },
  { id: "try2", audio: "vo2/s4.mp3", fallbackSeconds: 5, text: "جرّبت مرة ثانية، وهالمرة الفيديو طلع حلو! بس... بدون صوت." },
  { id: "connect", audio: "vo2/s5.mp3", fallbackSeconds: 3.5, text: "رجعت، وربطت كلود كود بإليفن لابز..." },
  { id: "result", audio: "vo2/s6.mp3", fallbackSeconds: 4, text: "والنتيجة؟ زي ما أنت شايف... فيديو رائع!" },
  { id: "outro", audio: "vo2/s7.mp3", fallbackSeconds: 10, text: "الدرس اللي تعلمته؟ الأداة لحالها ما تكفي... السر في الإضافات الصح. وكل محاولة فاشلة، كانت خطوة للنتيجة اللي تبيها. جرّبها بنفسك، وقلّي وش بتسوّي!" },
];
