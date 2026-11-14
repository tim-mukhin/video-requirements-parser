import type { Scenario } from '../format/scenario.ts';

export function recordingRegions(sc: Scenario) {
  const r = sc.recording!;
  const { w: FW, h: FH } = r.frame;
  const strip = r.layout === 'strip-top' ? { x: 0, y: 0, w: FW, h: 176 } : { x: FW - 300, y: 0, w: 300, h: FH };
  const area = r.layout === 'strip-top' ? { x: 0, y: strip.h, w: FW, h: FH - strip.h } : { x: 0, y: 0, w: FW - strip.w, h: FH };
  const k = Math.min(area.w / sc.screen.w, area.h / sc.screen.h);
  const screen = { x: area.x + (area.w - sc.screen.w * k) / 2, y: area.y + (area.h - sc.screen.h * k) / 2, w: sc.screen.w * k, h: sc.screen.h * k };
  return { strip, screen, k };
}
