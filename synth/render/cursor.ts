import { segmentAt } from '../compile/timeline.ts';
import type { Timeline } from '../compile/timeline.ts';

export type Vis = 'visible' | 'occluded' | 'out_of_view';
export type ProbeItem = { el: string; win: string; role: string; text: string; bbox: [number, number, number, number]; vis: Vis };
export type ProbeWin = { id: string; title: string; bbox: [number, number, number, number]; z: number };
export type Layout = { t: number; wins: ProbeWin[]; items: ProbeItem[] }[];

const ease = (x: number) => (x < 0.5 ? 2 * x * x : 1 - (-2 * x + 2) ** 2 / 2);

export function cursorAt(tl: Timeline, layout: Layout, t: number) {
  const box = (el: string, at: number) => {
    const it = layout[segmentAt(tl, at)].items.find((i) => i.el === el);
    if (!it) throw new Error(`cursor: no element ${el} in segment ${segmentAt(tl, at)}`);
    return it.bbox;
  };
  const center = (el: string, at: number) => {
    const b = box(el, at);
    return [b[0] + b[2] * 0.5, b[1] + b[3] * 0.5] as const;
  };
  const target = (i: number) => {
    const m = tl.moves[i];
    return m.point ?? center(m.el!, m.t1 - 0.001);
  };
  let pos: readonly [number, number] = [tl.w * 0.55, tl.h * 0.62];
  let ring = -1;
  for (let i = 0; i < tl.moves.length; i++) {
    const m = tl.moves[i];
    if (t < m.t0) break;
    const to = target(i);
    if (t >= m.t1) {
      pos = to;
      // pointing at an element: cursor moves along it while the phrase lasts
      if (m.hold && m.el && t < m.t1 + m.hold) {
        const b = box(m.el, m.t1 - 0.001);
        const k = Math.sin(((t - m.t1) / m.hold) * Math.PI);
        pos = [to[0] + Math.sin((t - m.t1) * 5.3) * Math.min(14, b[2] * 0.2) * k, to[1] + Math.sin((t - m.t1) * 2.4) * b[3] * 0.3 * k];
      }
      if (m.click && t - m.t1 < 0.3) ring = (t - m.t1) / 0.3;
      continue;
    }
    const k = ease((t - m.t0) / (m.t1 - m.t0));
    pos = [pos[0] + (to[0] - pos[0]) * k, pos[1] + (to[1] - pos[1]) * k];
  }
  return { pos, ring };
}


// phone: tap markers around the press moment instead of a cursor
export function touchesAt(tl: Timeline, layout: Layout, t: number) {
  const out: { x: number; y: number; a: number }[] = [];
  for (const m of tl.moves) {
    if (!m.el || t < m.t1 - 0.12 || t > m.t1 + m.hold + 0.35) continue;
    const it = layout[segmentAt(tl, m.t1 - 0.001)].items.find((i) => i.el === m.el);
    if (!it) continue;
    const a = t < m.t1 ? (t - m.t1 + 0.12) / 0.12 : t > m.t1 + m.hold ? 1 - (t - m.t1 - m.hold) / 0.35 : 1;
    out.push({ x: it.bbox[0] + it.bbox[2] / 2, y: it.bbox[1] + it.bbox[3] / 2, a });
  }
  return out;
}
