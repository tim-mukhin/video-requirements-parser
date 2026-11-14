import type { Action, AnchorKind, El, Scenario, WinId } from '../format/scenario.ts';
import { APPS } from '../apps/registry.ts';

export type Anchor = { kind: AnchorKind; target: string; name?: string; phrase: string; w0: number; w1: number };
export type Line = { id: string; who: string; name?: string; text: string; words: string[]; anchors: Anchor[] };

const MARK = /\[([^\]]+)\]\((click|focus|point|ref):([^)#]*)(?:#([\w-]+))?\)/g;
const split = (s: string) => s.split(/\s+/).filter(Boolean);

export function parseSay(id: string, who: string, src: string, name?: string): Line {
  let text = '';
  let last = 0;
  const anchors: Anchor[] = [];
  for (const m of src.matchAll(MARK)) {
    text += src.slice(last, m.index);
    const w0 = split(text).length;
    text += m[1];
    anchors.push({ kind: m[2] as AnchorKind, target: m[3], name: m[4], phrase: m[1], w0, w1: w0 + split(m[1]).length - 1 });
    last = m.index + m[0].length;
  }
  text += src.slice(last);
  if (/\]\(/.test(text)) throw new Error(`${id}: unrecognized markup in line "${src}"`);
  return { id, who, name, text, words: split(text), anchors };
}

export function lines(sc: Scenario): Line[] {
  let n = 0;
  return sc.steps.flatMap((s) =>
    'say' in s ? [parseSay(`l${String(++n).padStart(2, '0')}`, s.who ?? sc.cast[0].id, s.say, s.name)] : [],
  );
}

// word times from line start; array length = number of words in the text
export type Voice = Record<string, { dur: number; words: { start: number; end: number }[] }>;

export type Word = { w: string; start: number; end: number };
export type TLine = Omit<Line, 'words' | 'anchors'> & {
  start: number;
  end: number;
  words: Word[];
  anchors: (Anchor & { start: number; end: number })[];
};
export type TEvent = {
  t: number;
  src: 'user' | 'sys';
  win: WinId | 'os';
  action?: Action;
  op?: object;
  name?: string;
  expires?: string;
  line?: string;
  // typing: one action split into characters, k of n
  typing?: { k: number; n: number; end: number };
};
export type Move = { t0: number; t1: number; el?: El; point?: [number, number]; click: boolean; hold: number };
export type Timeline = {
  id: string;
  fps: number;
  w: number;
  h: number;
  duration: number;
  voiced: boolean;
  lines: TLine[];
  events: TEvent[];
  segments: number[];
  moves: Move[];
};

const LEAD = 0.8;
const GAP = 0.45;
const MOVE = 0.55;
const AFTER = 0.5;
const SYS_DELAY = 0.3;
const KEY_DELAY = 0.3;
const CHAR = 0.07;
const TAIL = 1.5;
const CPS = 14;

function estimateWords(line: Line, t: number, dur: number): Word[] {
  let off = 0;
  return line.words.map((w) => {
    const i = line.text.indexOf(w, off);
    off = i + w.length;
    return { w, start: t + (dur * i) / line.text.length, end: t + (dur * off) / line.text.length };
  });
}

const winOf = (sc: Scenario, id: string) => sc.windows.find((w) => w.id === id)!;

export function actionWin(a: Action): WinId | 'os' {
  if ('click' in a) return a.click.split('/')[0];
  if ('focus' in a) return a.focus;
  if ('key' in a) return a.win;
  if ('type' in a) return a.type.split('/')[0];
  if ('point' in a) return a.point.split('/')[0];
  return 'os';
}

export function compile(sc: Scenario, voice?: Voice, fps = 30): Timeline {
  const parsed = lines(sc);
  const events: TEvent[] = [];
  const named: Record<string, number> = {};
  const out: TLine[] = [];
  let t = LEAD;
  let li = 0;
  const user = (at: number, action: Action, name?: string, line?: string) => {
    events.push({ t: at, src: 'user', win: actionWin(action), action, name, line });
    if (name) named[name] = at;
  };

  for (const step of sc.steps) {
    if ('say' in step) {
      const line = parsed[li++];
      const v = voice?.[line.id];
      const dur = v?.dur ?? line.text.length / CPS;
      const words = v
        ? v.words.map((x, i) => ({ w: line.words[i], start: t + x.start, end: t + x.end }))
        : estimateWords(line, t, dur);
      const anchors = line.anchors.map((a) => ({ ...a, start: words[a.w0].start, end: words[a.w1].end }));
      if (line.name) named[line.name] = t;
      for (const a of anchors) {
        if (a.name) named[a.name] = a.start;
        if (a.kind === 'click') user(a.start, { click: a.target }, a.name, line.id);
        if (a.kind === 'focus') user(a.start, { focus: a.target }, a.name, line.id);
        if (a.kind === 'point') user(a.start, { point: a.target, ms: Math.round((a.end - a.start) * 1000) }, a.name, line.id);
      }
      out.push({ id: line.id, who: line.who, name: line.name, text: line.text, start: t, end: t + dur, words, anchors });
      t += dur + GAP;
    } else if ('act' in step) {
      const a = step.act;
      if ('key' in a) {
        const at = t + KEY_DELAY;
        user(at, a, step.name);
        t = at + AFTER;
      } else if ('type' in a) {
        const at = t + MOVE;
        user(at, { click: a.type }, step.name);
        const n = a.text.length;
        const end = at + 0.2 + CHAR * (n - 1);
        for (let k = 0; k < n; k++) {
          events.push({ t: at + 0.2 + CHAR * k, src: 'user', win: actionWin(a), action: { type: a.type, text: a.text.slice(0, k + 1) }, typing: { k, n, end } });
        }
        t = end + AFTER;
      } else {
        const at = t + MOVE;
        user(at, a, step.name);
        t = at + ('point' in a ? a.ms / 1000 : 0) + AFTER;
      }
    } else if ('sys' in step) {
      const base = step.at ? named[step.at] : t;
      if (base === undefined) throw new Error(`${sc.id}: no anchor ${step.at}`);
      const at = base + (step.delay ?? SYS_DELAY);
      events.push({ t: at, src: 'sys', win: step.sys, op: step.op, name: step.name });
      if (step.name) named[step.name] = at;
      if (step.ms) {
        const undo = step.sys === 'os' ? { notify: null } : 'devtools' in step.op ? { devtools: null } : APPS[winOf(sc, step.sys).app].expire(step.op);
        if (undo) events.push({ t: at + step.ms / 1000, src: 'sys', win: step.sys, op: undo, expires: step.name });
      }
      if (!step.at) t = at;
    } else {
      t += step.wait;
    }
  }

  events.sort((a, b) => a.t - b.t);
  const segments = [0, ...new Set(events.map((e) => e.t))].sort((a, b) => a - b);
  const duration = Math.max(t, ...events.map((e) => e.t)) + TAIL;

  const moves: Move[] = [];
  let prev = 0;
  for (const e of events) {
    if (e.src !== 'user' || !e.action) continue;
    const a = e.action;
    const t0 = Math.max(prev + 0.05, e.t - MOVE);
    if ('click' in a) moves.push({ t0, t1: e.t, el: a.click, click: true, hold: 0 });
    else if ('focus' in a) moves.push({ t0, t1: e.t, el: `${a.focus}/__title`, click: true, hold: 0 });
    else if ('point' in a) moves.push({ t0, t1: e.t, el: a.point, click: false, hold: a.ms / 1000 });
    else if ('move' in a) moves.push({ t0, t1: e.t, point: a.move, click: false, hold: 0 });
    else continue;
    prev = e.t + moves[moves.length - 1].hold;
  }

  const F = sc.recording?.frame ?? sc.screen;
  return { id: sc.id, fps, w: F.w, h: F.h, duration, voiced: !!voice, lines: out, events, segments, moves };
}

export type OsNotify = { app: string; title: string; text: string };
export type Devtools = {
  open: boolean;
  tab: 'elements' | 'console' | 'network';
  console: { level: 'error' | 'warn' | 'info'; text: string }[];
  network: { method: string; url: string; status: number; ms: number }[];
};
export type DeskState = { z: WinId[]; apps: Record<WinId, unknown>; notify?: OsNotify; devtools: Record<WinId, Devtools | undefined> };

// browser system events live outside the app: open DevTools, console line, network request
type BrowserOp = { devtools: Devtools['tab'] | null } | { console: Devtools['console'][number] } | { network: Devtools['network'][number] };
const isBrowserOp = (op: object): op is BrowserOp => 'devtools' in op || 'console' in op || 'network' in op;

export function stateAt(sc: Scenario, tl: Timeline, t: number): DeskState {
  let s: DeskState = { z: sc.windows.map((w) => w.id), apps: Object.fromEntries(sc.windows.map((w) => [w.id, w.state])), devtools: {} };
  const front = (z: WinId[], w: WinId) => [...z.filter((x) => x !== w), w];
  const put = (win: WinId, st: unknown) => (s = { ...s, apps: { ...s.apps, [win]: st } });
  for (const e of tl.events) {
    if (e.t > t) break;
    if (e.src === 'user' && e.action) {
      const a = e.action;
      if ('focus' in a) s = { ...s, z: front(s.z, a.focus) };
      if ('click' in a) {
        const [win, ...rest] = a.click.split('/');
        const el = rest.join('/');
        s = { ...s, z: front(s.z, win) };
        if (!el.startsWith('__')) put(win, APPS[winOf(sc, win).app].click(s.apps[win], el));
      }
      if ('key' in a) put(a.win, APPS[winOf(sc, a.win).app].key(s.apps[a.win], a.key, sc));
      if ('type' in a) {
        const [win, ...rest] = a.type.split('/');
        put(win, APPS[winOf(sc, win).app].type(s.apps[win], rest.join('/'), a.text));
      }
    } else if (e.win === 'os') {
      s = { ...s, notify: (e.op as { notify: OsNotify | null }).notify ?? undefined };
    } else if (isBrowserOp(e.op!)) {
      const op = e.op;
      const d: Devtools = s.devtools[e.win] ?? { open: false, tab: 'console', console: [], network: [] };
      const next: Devtools =
        'devtools' in op ? { ...d, open: !!op.devtools, tab: op.devtools ?? d.tab }
        : 'console' in op ? { ...d, console: [...d.console, op.console] }
        : { ...d, network: [...d.network, op.network] };
      s = { ...s, devtools: { ...s.devtools, [e.win]: next } };
    } else {
      put(e.win, APPS[winOf(sc, e.win).app].op(s.apps[e.win], e.op));
    }
  }
  return s;
}

export const segmentAt = (tl: Timeline, t: number) => {
  let i = 0;
  while (i + 1 < tl.segments.length && tl.segments[i + 1] <= t) i++;
  return i;
};

export const speakingAt = (tl: Timeline, t: number) => tl.lines.filter((l) => l.start <= t && t <= l.end).map((l) => l.who);
