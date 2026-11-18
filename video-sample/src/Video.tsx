import React from 'react';
import {
  AbsoluteFill,
  Img,
  Sequence,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import {continueRender, delayRender, Audio} from 'remotion';
import DURS from '../public/audio/durations.json';

const HEAD = 'Lalezar';
const BODY = 'Cairo';

// fonts are served locally from public/fonts (downloaded from Google Fonts)
if (typeof document !== 'undefined' && !document.getElementById('local-fonts')) {
  const handle = delayRender('Loading local Arabic fonts');
  const link = document.createElement('link');
  link.id = 'local-fonts';
  link.rel = 'stylesheet';
  link.href = staticFile('fonts/fonts.css');
  link.onload = () => {
    Promise.all([
      document.fonts.load('100px Lalezar', 'القرفة'),
      document.fonts.load('900 60px Cairo', 'القرفة'),
      document.fonts.load('700 60px Cairo', 'القرفة'),
    ]).then(() => continueRender(handle));
  };
  document.head.appendChild(link);
}

const C = {
  yellow: '#FFD21F',
  orange: '#F28C28',
  dark: '#1B1410',
  cream: '#FFF6E5',
  brown: '#7A3E12',
  red: '#E5402A',
  green: '#3BA55C',
};

const FPS = 30;
const s = (sec: number) => Math.round(sec * FPS);

// ---------- helpers ----------
const usePop = (delay = 0, damping = 12) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  return spring({frame: frame - delay, fps, config: {damping}});
};

const Banner: React.FC<{
  children: React.ReactNode;
  bg: string;
  color: string;
  delay?: number;
  rotate?: number;
  size?: number;
  font?: string;
}> = ({children, bg, color, delay = 0, rotate = -2, size = 110, font = HEAD}) => {
  const p = usePop(delay);
  return (
    <div
      style={{
        background: bg,
        color,
        fontFamily: font,
        fontSize: size,
        lineHeight: 1.25,
        padding: '10px 48px 18px',
        borderRadius: 18,
        transform: `rotate(${rotate}deg) scale(${p})`,
        opacity: p,
        boxShadow: '0 18px 40px rgba(0,0,0,.35)',
        direction: 'rtl',
        display: 'inline-block',
      }}
    >
      {children}
    </div>
  );
};

const KenBurns: React.FC<{src: string; from?: number; to?: number}> = ({src, from = 1.05, to = 1.18}) => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const scale = interpolate(frame, [0, durationInFrames], [from, to]);
  return (
    <AbsoluteFill style={{overflow: 'hidden'}}>
      <Img src={staticFile(src)} style={{width: '100%', height: '100%', objectFit: 'cover', transform: `scale(${scale})`}} />
    </AbsoluteFill>
  );
};

const FadeIn: React.FC<{children: React.ReactNode}> = ({children}) => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const o = interpolate(frame, [0, 8, durationInFrames - 8, durationInFrames], [0, 1, 1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  return <AbsoluteFill style={{opacity: o}}>{children}</AbsoluteFill>;
};

// warm animated background with floating spice particles
const WarmBg: React.FC<{tint?: string}> = ({tint = C.orange}) => {
  const frame = useCurrentFrame();
  const dots = Array.from({length: 28}, (_, i) => {
    const x = (i * 137.5) % 100;
    const speed = 0.15 + (i % 5) * 0.07;
    const y = (100 + ((i * 53) % 100) - frame * speed) % 110;
    const r = 6 + (i % 4) * 5;
    return (
      <div
        key={i}
        style={{
          position: 'absolute',
          left: `${x}%`,
          top: `${y}%`,
          width: r,
          height: r,
          borderRadius: '50%',
          background: i % 3 === 0 ? C.yellow : '#C8641E',
          opacity: 0.35,
          filter: 'blur(1px)',
        }}
      />
    );
  });
  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(circle at 70% 30%, ${tint} 0%, #8A3A10 45%, ${C.dark} 100%)`,
      }}
    >
      {dots}
    </AbsoluteFill>
  );
};

const NumberBadge: React.FC<{n: string}> = ({n}) => {
  const p = usePop(0, 9);
  return (
    <div
      style={{
        width: 260,
        height: 260,
        borderRadius: '50%',
        background: C.yellow,
        color: C.dark,
        fontFamily: HEAD,
        fontSize: 120,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        transform: `scale(${p}) rotate(${(1 - p) * -90}deg)`,
        boxShadow: '0 0 0 14px rgba(255,210,31,.25), 0 25px 50px rgba(0,0,0,.4)',
      }}
    >
      {n}
    </div>
  );
};

const PointScene: React.FC<{n: string; title: string; sub: string; note?: string}> = ({n, title, sub, note}) => {
  const p2 = usePop(14);
  const p3 = usePop(30);
  return (
    <FadeIn>
      <WarmBg />
      <AbsoluteFill style={{flexDirection: 'row-reverse', alignItems: 'center', justifyContent: 'center', gap: 90, padding: 120}}>
        <NumberBadge n={n} />
        <div style={{direction: 'rtl', maxWidth: 1150, display: 'flex', flexDirection: 'column', gap: 34}}>
          <div style={{opacity: p2, transform: `translateX(${(1 - p2) * 120}px)`}}>
            <Banner bg={C.cream} color={C.dark} delay={10} rotate={-1.5} size={120}>
              {title}
            </Banner>
          </div>
          <div
            style={{
              fontFamily: BODY,
              fontWeight: 900,
              fontSize: 64,
              color: '#fff',
              lineHeight: 1.5,
              opacity: p3,
              transform: `translateY(${(1 - p3) * 40}px)`,
              textShadow: '0 4px 14px rgba(0,0,0,.5)',
            }}
          >
            {sub}
          </div>
          {note && (
            <div style={{fontFamily: BODY, fontWeight: 700, fontSize: 40, color: C.yellow, opacity: p3}}>{note}</div>
          )}
        </div>
      </AbsoluteFill>
    </FadeIn>
  );
};

// ---------- scenes ----------
const Hook = () => {
  const frame = useCurrentFrame();
  const warn = frame >= s(5.3);
  return (
    <FadeIn>
      <KenBurns src="hook.png" />
      <AbsoluteFill style={{background: 'linear-gradient(90deg, rgba(0,0,0,.05) 30%, rgba(0,0,0,.75) 100%)'}} />
      <AbsoluteFill style={{alignItems: 'flex-end', justifyContent: 'center', padding: '0 110px', gap: 30, flexDirection: 'column'}}>
        <Banner bg="#fff" color={C.dark} delay={4} rotate={-3}>
          ملعقة صغيرة من القرفة
        </Banner>
        <Banner bg={C.orange} color="#fff" delay={22} rotate={-3} size={130}>
          قد تغيّر يومك!
        </Banner>
        {warn && (
          <Sequence from={s(5.3)} layout="none">
            <Banner bg={C.red} color="#fff" delay={0} rotate={2} size={70} font={BODY}>
              <span style={{fontWeight: 900}}>⚠ لكن انتبه… نوع منها قد يضرّك</span>
            </Banner>
          </Sequence>
        )}
      </AbsoluteFill>
    </FadeIn>
  );
};

const TitleCard = () => {
  const frame = useCurrentFrame();
  const shine = interpolate(frame, [10, 50], [-30, 130], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const p = usePop(0, 10);
  return (
    <FadeIn>
      <AbsoluteFill style={{background: C.dark}}>
        <KenBurns src="hook.png" from={1.2} to={1.3} />
        <AbsoluteFill style={{background: 'rgba(20,10,5,.72)'}} />
      </AbsoluteFill>
      <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', flexDirection: 'column', gap: 10}}>
        <div
          style={{
            fontFamily: HEAD,
            fontSize: 230,
            color: C.yellow,
            transform: `scale(${p})`,
            textShadow: '0 10px 0 #9A5A00, 0 20px 40px rgba(0,0,0,.6)',
            backgroundImage: `linear-gradient(100deg, ${C.yellow} ${shine - 15}%, #fff ${shine}%, ${C.yellow} ${shine + 15}%)`,
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
          }}
        >
          القرفة
        </div>
        <Banner bg={C.orange} color="#fff" delay={12} rotate={-2} size={100}>
          فوائد وأسرار
        </Banner>
      </AbsoluteFill>
    </FadeIn>
  );
};

const Secret = () => {
  const frame = useCurrentFrame();
  const showLabels = frame > s(5);
  const lp = usePop(s(5));
  const rp = usePop(s(13.5));
  return (
    <FadeIn>
      <KenBurns src="compare.png" from={1.02} to={1.08} />
      <AbsoluteFill style={{background: 'linear-gradient(180deg, rgba(0,0,0,.65) 0%, rgba(0,0,0,0) 30%, rgba(0,0,0,0) 65%, rgba(0,0,0,.7) 100%)'}} />
      <AbsoluteFill style={{alignItems: 'center', paddingTop: 50}}>
        <Banner bg={C.yellow} color={C.dark} rotate={-1} size={100}>
          السر الذي لا يعرفه كثيرون
        </Banner>
      </AbsoluteFill>
      {showLabels && (
        <AbsoluteFill style={{flexDirection: 'row', justifyContent: 'space-around', alignItems: 'flex-end', paddingBottom: 70}}>
          {/* image: cassia on the left, Ceylon on the right */}
          <div style={{transform: `scale(${lp})`, textAlign: 'center', direction: 'rtl'}}>
            <div style={{fontFamily: HEAD, fontSize: 84, color: '#fff', background: C.red, padding: '4px 40px 12px', borderRadius: 16}}>
              الصينية (كاسيا)
            </div>
            <div style={{fontFamily: BODY, fontWeight: 900, fontSize: 46, color: '#fff', marginTop: 14, textShadow: '0 3px 10px #000'}}>
              كومارين مرتفع ✗
            </div>
          </div>
          <div style={{transform: `scale(${rp})`, textAlign: 'center', direction: 'rtl'}}>
            <div style={{fontFamily: HEAD, fontSize: 84, color: '#fff', background: C.green, padding: '4px 40px 12px', borderRadius: 16}}>
              السيلانية
            </div>
            <div style={{fontFamily: BODY, fontWeight: 900, fontSize: 46, color: '#fff', marginTop: 14, textShadow: '0 3px 10px #000'}}>
              كومارين أقل بكثير ✓
            </div>
          </div>
        </AbsoluteFill>
      )}
    </FadeIn>
  );
};

const Tip: React.FC<{text: string; icon: string; color: string; delay: number}> = ({text, icon, color, delay}) => {
  const p = usePop(delay);
  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'row-reverse',
        alignItems: 'center',
        gap: 30,
        background: 'rgba(255,246,229,.96)',
        borderRadius: 24,
        padding: '22px 40px',
        opacity: p,
        transform: `translateX(${(1 - p) * 200}px)`,
        boxShadow: '0 14px 30px rgba(0,0,0,.3)',
      }}
    >
      <div
        style={{
          minWidth: 90,
          height: 90,
          borderRadius: '50%',
          background: color,
          color: '#fff',
          fontSize: 56,
          fontWeight: 900,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontFamily: 'DejaVu Sans',
        }}
      >
        {icon}
      </div>
      <div style={{fontFamily: BODY, fontWeight: 900, fontSize: 54, color: C.dark, direction: 'rtl', lineHeight: 1.4}}>{text}</div>
    </div>
  );
};

const Advice = () => (
  <FadeIn>
    <WarmBg tint="#D9782A" />
    <AbsoluteFill style={{alignItems: 'flex-end', justifyContent: 'center', padding: '0 140px', gap: 34, flexDirection: 'column'}}>
      <Banner bg={C.yellow} color={C.dark} rotate={-2} size={110}>
        نصيحتنا لك
      </Banner>
      <Tip icon="✓" color={C.green} delay={s(1.8)} text="اختر القرفة السيلانية" />
      <Tip icon="½" color={C.orange} delay={s(4)} text="لا تتجاوز نصف ملعقة صغيرة يومياً من الصينية" />
      <Tip icon="!" color={C.red} delay={s(9.5)} text="تتناول أدوية السكر أو مميّعات الدم؟ استشر طبيبك أولاً" />
    </AbsoluteFill>
  </FadeIn>
);

const CTA = () => {
  const frame = useCurrentFrame();
  const pulse = 1 + Math.sin(frame / 6) * 0.04;
  return (
    <FadeIn>
      <KenBurns src="hook.png" from={1.15} to={1.05} />
      <AbsoluteFill style={{background: 'rgba(20,10,5,.7)'}} />
      <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', flexDirection: 'column', gap: 40}}>
        <Banner bg="#fff" color={C.dark} rotate={-2} size={120}>
          كيف تحب أن تتناول القرفة؟
        </Banner>
        <Banner bg={C.orange} color="#fff" delay={15} rotate={1.5} size={80} font={BODY}>
          <span style={{fontWeight: 900}}>اكتب لنا في التعليقات</span>
        </Banner>
        <div
          style={{
            marginTop: 30,
            transform: `scale(${pulse})`,
            background: '#E62117',
            color: '#fff',
            fontFamily: BODY,
            fontWeight: 900,
            fontSize: 60,
            padding: '14px 60px 20px',
            borderRadius: 14,
          }}
        >
          اشترك ▶
        </div>
      </AbsoluteFill>
    </FadeIn>
  );
};

// ---------- timeline ----------
const PAD = 0.7; // seconds of breathing room after each line
const SCENES: {dur: number; el: React.ReactNode}[] = [
  {dur: DURS[0] + PAD, el: <Hook />},
  {dur: DURS[1] + PAD, el: <TitleCard />},
  {dur: DURS[2] + PAD, el: <PointScene n="1" title="مضادات الأكسدة" sub="من أغنى التوابل بها… تساعد جسمك على مقاومة الالتهابات" />},
  {
    dur: DURS[3] + PAD,
    el: (
      <PointScene
        n="2"
        title="حساسية الإنسولين"
        sub="قد تساعد على تخفيف ارتفاع السكر بعد الوجبات"
        note="بحسب بعض الدراسات"
      />
    ),
  },
  {dur: DURS[4] + PAD, el: <PointScene n="3" title="سكر أقل بدون ما تحس" sub="طعمها الحلو يغنيك عن جزء من السكر في قهوتك وشايك" />},
  {dur: DURS[5] + PAD, el: <Secret />},
  {dur: DURS[6] + PAD, el: <Advice />},
  {dur: DURS[7] + PAD, el: <CTA />},
];

export const TOTAL = SCENES.reduce((a, b) => a + s(b.dur), 0);

export const CinnamonVideo: React.FC = () => {
  let from = 0;
  return (
    <AbsoluteFill style={{background: C.dark}}>
      {SCENES.map((sc, i) => {
        const el = (
          <Sequence key={i} from={from} durationInFrames={s(sc.dur)}>
            {sc.el}
            <Sequence from={s(0.25)} layout="none">
              <Audio src={staticFile(`audio/scene${i}.mp3`)} />
            </Sequence>
          </Sequence>
        );
        from += s(sc.dur);
        return el;
      })}
    </AbsoluteFill>
  );
};
