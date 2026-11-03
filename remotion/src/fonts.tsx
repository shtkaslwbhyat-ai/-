import { useEffect, useState } from "react";
import { continueRender, delayRender, staticFile } from "remotion";

const WEIGHTS = [400, 700, 900];

// Loads the Cairo font files from public/fonts and holds rendering until they are ready.
export const FontFaces: React.FC = () => {
  const [handle] = useState(() => delayRender("Loading Cairo font"));
  useEffect(() => {
    Promise.all(
      WEIGHTS.map((w) => {
        const face = new FontFace("Cairo", `url(${staticFile(`fonts/cairo${w}.ttf`)})`, { weight: String(w) });
        document.fonts.add(face);
        return face.load();
      })
    ).then(() => continueRender(handle));
  }, [handle]);
  return null;
};
