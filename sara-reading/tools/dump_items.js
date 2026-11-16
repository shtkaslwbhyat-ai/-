global.window={}; require(process.argv[2]);
const src=require('fs').readFileSync(process.argv[3],'utf8');
const L=window.SARA_LESSONS, out=new Set();
for(const l of L){ out.add(l.rule); l.examples.forEach(x=>out.add(x)); l.grids.forEach(g=>g.items.forEach(([w])=>out.add(w))); }
const grab=re=>{const m=src.match(re); return m?JSON.parse(m[1]):null};
const names=Object.values(eval("("+src.match(/const NAMES = (\{[^}]*\})/)[1]+")"));
const marks=Object.values(eval("("+src.match(/const MARKS = (\{[^}]*\})/)[1]+")"));
names.forEach(x=>out.add(x)); marks.forEach(x=>out.add(x)); out.add("شدة");
eval(src.match(/const PRAISE=(\[[^\]]*\])/)[0].replace("const PRAISE","global.PR")); PR.forEach(x=>out.add(x));
// every literal passed to say()/sayParts()
for(const m of src.matchAll(/say(?:Parts)?\((?:\[)?([^)]*)\)/g)) for(const s of m[1].matchAll(/"([^"]*[؀-ۿ][^"]*)"/g)) out.add(s[1]);
console.log(JSON.stringify([...out].map(s=>s.normalize("NFC"))));
