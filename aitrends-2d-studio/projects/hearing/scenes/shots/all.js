// shots/all.js — registers every shot in story/shots.json from its params.tpl template.
import { E, registerShot } from '/engine/core.js';
import { TPL } from './_tpl.js';

for (const sh of E.shots) {
  const fn = TPL[sh.params?.tpl];
  if (fn) registerShot(sh.id, { draw: (g, t, info) => fn(g, t, info) });
}
