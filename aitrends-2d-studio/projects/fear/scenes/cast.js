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
// episode 2 cast
export const KARIM = { top: 'hoodie', color: '#1fa38a', head: 'none' };                                    // كريم (you), teal hoodie
export const MARYAM = { top: 'dress', color: '#e8735a', head: 'hood', headColor: '#e8735a' };              // مريم, coral dress + headscarf
export const YOUNES = { top: 'tshirt', color: '#f2c21a', head: 'cap', headColor: '#f2c21a', kid: true };   // يونس, yellow cap
export const SAMER = { top: 'tshirt', color: '#8a5ad6', head: 'spiky' };                                    // سامر, purple tee
export const DOC = { top: 'labcoat', face: 'glasses', head: 'none' };
Object.assign(CAST, { KARIM, MARYAM, YOUNES, SAMER, DOC });
// episode 3 cast
export const SALIM = { top: 'hoodie', color: '#2f7fd6', head: 'none', face: 'glasses' };                  // سليم (you), blue hoodie + glasses
export const NOUR = { top: 'dress', color: '#f29ac0', head: 'ponytail', headColor: '#f29ac0', kid: true }; // نور, pink
export const HADI = { top: 'tshirt', color: '#3fb950', head: 'capBack', headColor: '#3fb950' };           // هادي, green
export const ANCHOR = { top: 'suit', color: '#30304a', head: 'none' };
Object.assign(CAST, { SALIM, NOUR, HADI, ANCHOR });
// episode 4 cast
export const YAZAN = { top: 'hoodie', color: '#e8a020', head: 'spiky' };                                   // يزن (you), amber hoodie
export const HUDA = { top: 'dress', color: '#2fa08a', head: 'hood', headColor: '#2fa08a' };               // هدى (mother), teal dress + headscarf
export const TAREQ = { top: 'tshirt', color: '#e04a3a', head: 'capBack', headColor: '#e04a3a' };          // طارق, red
export const COACH = { top: 'suit', color: '#1e3a6a', head: 'cap', headColor: '#1e3a6a' };
export const YAZANKID = { ...YAZAN, kid: true };
Object.assign(CAST, { YAZAN, HUDA, TAREQ, COACH, YAZANKID });
export const YAZANJ = { top: 'jersey', color: '#e8a020', color2: '#1a1a1a', number: '10', head: 'spiky' };  // يزن in team kit
export const TAREQJ = { top: 'jersey', color: '#e8a020', color2: '#1a1a1a', number: '7', head: 'capBack', headColor: '#e04a3a' };
export const RIVAL = { top: 'jersey', color: '#2f5fd6', color2: '#ffffff', number: '4', head: 'none' };
Object.assign(CAST, { YAZANJ, TAREQJ, RIVAL });
CAST.COACH = { top: 'tracksuit', color: '#1e3a6a', color2: '#ffffff', head: 'cap', headColor: '#1e3a6a' };
// episode 5 cast
export const OMAR = { top: 'hoodie', color: '#c8326e', head: 'curly' };                                   // عمر (you), magenta hoodie
export const OMARKID = { ...OMAR, kid: true };
export const SAWSAN = { top: 'dress', color: '#8a9a3a', head: 'hood', headColor: '#8a9a3a' };             // سوسن (mother), olive
export const YOUSEF = { top: 'suit', color: '#4a3a2a', head: 'fedora', headColor: '#3a2a1a', face: 'glasses' }; // جد يوسف
export const MEDIC = { top: 'suit', color: '#c83a3a', head: 'cap', headColor: '#c83a3a' };
Object.assign(CAST, { OMAR, OMARKID, SAWSAN, YOUSEF, MEDIC });
// episode 6 cast
export const ZAID = { top: 'hoodie', color: '#c8692a', head: 'spiky' };                                     // زيد (you), copper hoodie
export const LINA = { top: 'dress', color: '#f2c21a', head: 'ponytail', headColor: '#f2c21a', kid: true };  // لينا, yellow
export const NURSE = { top: 'dress', color: '#7ac8e0', head: 'bun', headColor: '#e8f4f8' };
export const SALEH = { top: 'tshirt', color: '#e8e0d0', head: 'cap', headColor: '#e8e0d0' };               // العم صالح (baker)
Object.assign(CAST, { ZAID, LINA, NURSE, SALEH });
// episode 7 cast
export const FARIS = { top: 'hoodie', color: '#8a2a3a', head: 'spiky' };                                   // فارس (you), maroon hoodie
export const FARISKID = { ...FARIS, kid: true };
export const RAMI = { top: 'tshirt', color: '#5ab0e8', head: 'capBack', headColor: '#5ab0e8' };            // رامي, sky blue
export const RAMIKID = { ...RAMI, kid: true };
export const FIRE = { top: 'suit', color: '#c8a020', head: 'cap', headColor: '#c83a3a' };                   // firefighter
Object.assign(CAST, { FARIS, FARISKID, RAMI, RAMIKID, FIRE });
// episode 8 cast (documentary: stylised stand-ins for real people)
export const SCIENTIST = { top: 'labcoat', face: 'glasses', head: 'bun', headColor: '#2a2026' };
export const DRWOMAN = { top: 'dress', color: '#5a7ad6', head: 'bun', headColor: '#3a2a2a' };
export const PAINTER = { top: 'dress', color: '#e05a8a', head: 'curly', headColor: '#3a2a2a' };
export const ZARQA = { top: 'dress', color: '#2f5fd6', head: 'hood', headColor: '#2f5fd6' };
export const MOKEN = { top: 'tshirt', color: '#2fa08a', head: 'none', kid: true };
export const OLDMAN = { top: 'suit', color: '#5a5a66', head: 'none' };
Object.assign(CAST, { SCIENTIST, DRWOMAN, PAINTER, ZARQA, MOKEN, OLDMAN });
// episode 9 cast (stand-ins for real people)
export const JOY = { top: 'dress', color: '#3a9a8a', head: 'bun', headColor: '#d8d0c0', face: 'glasses' };
export const LES = { top: 'suit', color: '#3a4a6a', head: 'none' };
export const LAB = { top: 'labcoat', face: 'glasses', head: 'none' };
Object.assign(CAST, { JOY, LES, LAB });
export const DIVER = { top: 'tshirt', color: '#1c2430', head: 'none' };                 // Maričić (reenactment), black wetsuit
export const SOBAT = { top: 'tshirt', color: '#2a3a52', head: 'none', face: 'glasses' }; // Šobat (reenactment)
export const NATALIA = { top: 'tshirt', color: '#1c2430', head: 'ponytail', headColor: '#e9d8a0' }; // Molchanova (reenactment)
export const BLAINE = { top: 'suit', color: '#24242c', head: 'none' };                 // Blaine (reenactment)
export const BAJAU = { top: 'tshirt', color: '#2fa08a', head: 'none' };
export const AMA = { top: 'dress', color: '#f0f0f0', head: 'bun', headColor: '#f0f0f0' };
Object.assign(CAST, { DIVER, SOBAT, NATALIA, BLAINE, BAJAU, AMA });
export const SAM = { top: 'tshirt', color: '#3a6ea5', head: 'none', face: 'glasses', kid: true };   // Sam Berns (reenactment)
export const LESLIE = { top: 'labcoat', head: 'bun', face: 'glasses' };                           // his mother, doctor
export const SCOTT = { top: 'labcoat', head: 'none' };                                            // his father, doctor
export const CALMENT = { top: 'dress', color: '#8a5ad6', head: 'bun', headColor: '#f0f0f0', face: 'glasses' };
export const BUTTON = { top: 'suit', color: '#5a4a3a', head: 'none' };
Object.assign(CAST, { SAM, LESLIE, SCOTT, CALMENT, BUTTON });
export const BOLT = { top: 'tshirt', color: '#f2d21a', head: 'none' };       // Bolt (reenactment), yellow Jamaica vest
export const BLAKE = { top: 'tshirt', color: '#2fa050', head: 'none' };      // Blake (reenactment)
export const GAY = { top: 'tshirt', color: '#2a4aa0', head: 'none' };
export const POWELL = { top: 'tshirt', color: '#e8e030', head: 'capBack', headColor: '#2a7a3a' };
export const HEALY = { top: 'labcoat', head: 'none' };
export const PATEK = { top: 'labcoat', head: 'ponytail' };
export const WELLS = { top: 'suit', color: '#3a3a44', head: 'none' };
export const EAGLEMAN = { top: 'tshirt', color: '#5a4a8a', head: 'none', face: 'glasses' };
Object.assign(CAST, { BOLT, BLAKE, GAY, POWELL, HEALY, PATEK, WELLS, EAGLEMAN });
export const SALINAS = { top: 'labcoat', head: 'none', face: 'glasses' };    // Joel Salinas (reenactment)
export const SINGER = { top: 'suit', color: '#5a3a6a', head: 'bun' };         // Tania Singer (reenactment)
export const KRAMER = { top: 'tshirt', color: '#3a5a9a', head: 'none' };
export const RIZZO = { top: 'labcoat', head: 'none' };
export const HICKOK = { top: 'suit', color: '#2a3a4a', head: 'none', face: 'glasses' };
export const PKD = { top: 'suit', color: '#4a3a2a', head: 'none', face: 'glasses' };
Object.assign(CAST, { SALINAS, SINGER, KRAMER, RIZZO, HICKOK, PKD });
export const COLLINS = { top: 'suit', color: '#1e2a52', head: 'cap', headColor: '#1e2a52' };  // PC Gary Collins (reenactment), police uniform
export const NEVILLE = { top: 'suit', color: '#3a3a44', head: 'none' };
export const RUSSELL = { top: 'labcoat', head: 'none', face: 'glasses' };
export const SACKS = { top: 'suit', color: '#5a4a3a', head: 'none', face: 'glasses' };
export const KANWISHER = { top: 'labcoat', head: 'bun' };
export const GAUTHIER = { top: 'labcoat', head: 'ponytail', face: 'glasses' };
export const KID2 = { top: 'tshirt', color: '#3fb950', head: 'none', kid: true };
Object.assign(CAST, { COLLINS, NEVILLE, RUSSELL, SACKS, KANWISHER, GAUTHIER, KID2 });
export const HARBISSON = { top: 'tshirt', color: '#2a2a30', head: 'none' };     // Neil Harbisson (reenactment)
export const NABOKOV = { top: 'suit', color: '#4a4a3a', head: 'none' };
export const NABOMOM = { top: 'dress', color: '#6a4a8a', head: 'bun' };
export const SIMNER = { top: 'labcoat', head: 'ponytail' };
export const RAMA = { top: 'suit', color: '#2a3a5a', head: 'none', face: 'glasses' };
export const MAURER = { top: 'labcoat', head: 'bun', face: 'glasses' };
Object.assign(CAST, { HARBISSON, NABOKOV, NABOMOM, SIMNER, RAMA, MAURER });
export const SM = { top: 'dress', color: '#3a7ab0', head: 'ponytail', headColor: '#2a1a10' };   // patient S.M. (reenactment, anonymous)
export const FEINSTEIN = { top: 'labcoat', head: 'none', face: 'glasses' };
export const HONNOLD = { top: 'tshirt', color: '#d0402a', head: 'none' };
export const JOSEPH = { top: 'labcoat', head: 'bun' };
export const BELYAEV = { top: 'suit', color: '#3a3a3a', head: 'none', face: 'glasses' };
export const GRIMMBOY = { top: 'tshirt', color: '#5a7a3a', head: 'none' };
Object.assign(CAST, { SM, FEINSTEIN, HONNOLD, JOSEPH, BELYAEV, GRIMMBOY });
