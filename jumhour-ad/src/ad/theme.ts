import { loadFont } from "@remotion/fonts";
import { Easing, interpolate, staticFile } from "remotion";

export const display = "Lalezar";
export const body = "Tajawal";
loadFont({ family: display, url: staticFile("fonts/Lalezar-Regular.ttf") });
loadFont({ family: body, url: staticFile("fonts/Tajawal-Medium.ttf"), weight: "500" });
loadFont({ family: body, url: staticFile("fonts/Tajawal-ExtraBold.ttf"), weight: "800" });

export const C = {
  espresso: "#1E110A",
  roast: "#3A2214",
  coffee: "#6B3E22",
  caramel: "#C27C3E",
  gold: "#E8B04B",
  cream: "#F6EBDD",
  milk: "#FFF8EE",
  ice: "#BFE3F0",
  ember: "#E0592A",
};

export const ease = (
  f: number,
  input: [number, number],
  output: [number, number],
  e: (t: number) => number = Easing.bezier(0.16, 1, 0.3, 1),
) =>
  interpolate(f, input, output, {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: e,
  });

export const pop = (f: number, start: number, dur = 18) =>
  interpolate(f, [start, start + dur], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.spring({ damping: 11, mass: 0.8 }),
  });
