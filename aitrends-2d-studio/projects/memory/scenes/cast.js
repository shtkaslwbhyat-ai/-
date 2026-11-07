// cast.js — one signature colour per recurring character, identical in every shot.
export const YOU = { top: 'hoodie', color: '#d64a33', head: 'none' };                                        // يوسف (you), red-orange hoodie
export const SALMA = { top: 'tshirt', color: '#f29ac0', head: 'ponytail', headColor: '#f29ac0', kid: true };  // little sister, pink
export const MOM = { top: 'dress', color: '#8a5ad6', head: 'bun' };                                           // mother, purple dress
export const DAD = { top: 'tshirt', color: '#3fb950', head: 'none' };                                         // father, green tee
export const LAYLA = { top: 'dress', color: '#f2c21a', head: 'bun', headColor: '#e9e4da', face: 'glasses' };  // grandmother, yellow dress, white bun
export const ADAM = { top: 'tshirt', color: '#3a6ea5', head: 'capBack', headColor: '#3a6ea5' };               // friend, blue tee + cap
export const MAYA = { top: 'labcoat', face: 'glasses', head: 'ponytail' };                                    // neurologist (fictional)
export const TEACHER = { top: 'suit', color: '#2a2a34', head: 'none', face: 'glasses' };
export const PLAIN = { top: 'none', head: 'none' };
export const CAST = { YOU, SALMA, MOM, DAD, LAYLA, ADAM, MAYA, TEACHER, PLAIN };
export const YOUKID = { ...YOU, kid: true };
export const POLICE = { top: 'suit', color: '#1e2a52', head: 'cap', headColor: '#1e2a52' };
export const BAKER = { top: 'tshirt', color: '#e8e0d0', head: 'none' };
export const WAITER = { top: 'suit', color: '#1a1a1a', head: 'none' };
export const GRANDPA = { top: 'suit', color: '#4a3a2a', head: 'fedora', headColor: '#3a2a1a' };
Object.assign(CAST, { YOUKID, POLICE, BAKER, WAITER, GRANDPA });
