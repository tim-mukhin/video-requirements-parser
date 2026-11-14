import type { Scenario } from '../format/scenario.ts';
import type { TEvent, Timeline } from './timeline.ts';
import { stateAt } from './timeline.ts';
import type { Layout, ProbeItem } from '../render/cursor.ts';
import { APPS } from '../apps/registry.ts';
import type { MeetState } from '../apps/meet/model.ts';
import type { SlidesState } from '../apps/slides/model.ts';
import { recordingRegions } from '../render/regions.ts';

const ms = (s: number) => Math.round(s * 1000);

export function truth(sc: Scenario, tl: Timeline, layout: Layout) {
  const end = ms(tl.duration);
  const title = (win: string) => sc.windows.find((w) => w.id === win)?.title ?? win;
  const evId = new Map<TEvent, string>();
  tl.events.forEach((e, i) => evId.set(e, `evt_${String(i + 1).padStart(3, '0')}`));
  const segAt = (t: number) => {
    let i = 0;
    while (i + 1 < tl.segments.length && tl.segments[i + 1] <= t) i++;
    return i;
  };
  const elText = (el: string, at: number) => {
    const it = layout[segAt(at - 0.001)].items.find((i) => i.el === el) ?? layout[segAt(at)].items.find((i) => i.el === el);
    return it ? it.text || `${it.role} ${el.split('/').slice(1).join('/')}` : el;
  };
  // intermediate typing chars: ground truth has one type_text action, not one event per letter
  const midTyping = (e: TEvent) => !!e.typing && e.typing.k > 0;

  // speakers: the tile is visible on video; the name is known if the tile is personal or the person introduced themselves
  const tileName = (id: string) => sc.recording?.tiles.find((t) => t.id === id)?.name ?? null;
  let unnamed = 0;
  const firstSpoke = [...new Set(tl.lines.map((l) => l.who))];
  const speakers = firstSpoke.map((id) => {
    const c = sc.cast.find((x) => x.id === id)!;
    const tile = c.tile ?? c.id;
    const room = sc.recording?.tiles.find((t) => t.id === tile)?.kind === 'room';
    const known = !room || !!c.introduced;
    return {
      id,
      tile,
      tile_name: tileName(tile),
      name_on_video: known ? c.name : null,
      label: known ? c.name : `Person${++unnamed}`,
      shares_tile_with: sc.cast.filter((x) => x.id !== id && (x.tile ?? x.id) === tile).map((x) => x.id),
    };
  });
  const label = (id: string) => speakers.find((x) => x.id === id)!.label;

  const transcript = tl.lines.map((l) => ({
    id: l.id,
    speaker_id: l.who,
    speaker_label: label(l.who),
    tile: speakers.find((x) => x.id === l.who)!.tile,
    start_ms: ms(l.start),
    end_ms: ms(l.end),
    text: l.text,
    words: l.words.map((w) => ({ w: w.w, start_ms: ms(w.start), end_ms: ms(w.end) })),
    timing: tl.voiced ? 'tts+whisper' : 'estimated',
  }));

  const states = layout.map((seg, i) => ({
    state_id: `state_${String(i + 1).padStart(3, '0')}`,
    start_ms: ms(seg.t),
    end_ms: i + 1 < layout.length ? ms(layout[i + 1].t) : end,
    screen: { width: sc.screen.w, height: sc.screen.h },
    windows: seg.wins.map((w) => ({ id: w.id, title: w.title, bbox: w.bbox, z_index: w.z })),
    elements: seg.items.map((it) => ({ id: it.el, window: it.win, role: it.role, text: it.text, bbox: it.bbox, visibility: it.vis })),
  }));

  const actions = tl.events
    .filter((e) => !midTyping(e))
    .map((e) => {
      const base = { event_id: evId.get(e)!, t_ms: ms(e.t), name: e.name ?? null };
      if (e.src === 'user' && e.action) {
        const a = e.action;
        const common = { ...base, actor: 'user', window: e.win, window_title: title(e.win), utterance: e.line ?? null };
        if ('key' in a) return { ...common, type: 'key', key: a.key, target: null, target_text: null, observed: 'none' };
        if ('type' in a) {
          const full = tl.events.filter((x) => x.typing && x.action && 'type' in x.action && x.action.type === a.type && x.typing.end === e.typing!.end);
          const text = (full[full.length - 1].action as { text: string }).text;
          return { ...common, type: 'type_text', target: a.type, target_text: elText(a.type, e.t), text, duration_ms: ms(e.typing!.end - e.t), observed: 'screen_only' };
        }
        const target = 'click' in a ? a.click : 'focus' in a ? `${a.focus}/__title` : 'point' in a ? a.point : null;
        return {
          ...common,
          type: 'click' in a ? 'click' : 'focus' in a ? 'focus_window' : 'point' in a ? 'point' : 'cursor_move',
          target,
          target_text: target ? elText(target, e.t) : null,
          duration_ms: 'point' in a ? a.ms : null,
          observed: 'cursor',
        };
      }
      return { ...base, type: e.expires ? 'system_effect_end' : 'system_effect', actor: 'system', window: e.win, op: e.op, observed: 'screen_only', ends: e.expires ?? null };
    });

  const diffs: ({ t_ms: number } & Record<string, unknown>)[] = [];
  for (let i = 1; i < layout.length; i++) {
    const prev = new Map(layout[i - 1].items.map((it: ProbeItem) => [it.el, it]));
    const next = new Map(layout[i].items.map((it: ProbeItem) => [it.el, it]));
    const t = layout[i].t;
    const causes = tl.events.filter((e) => e.t === t);
    if (causes.length && causes.every(midTyping) && !causes.some((e) => e.typing!.k === e.typing!.n - 1)) continue;
    const cause = causes.map((e) => {
      const first = e.typing ? tl.events.find((x) => x.typing?.k === 0 && x.typing.end === e.typing!.end) : e;
      return evId.get(first ?? e);
    });
    const lifetime = (el: string) => {
      let j = i;
      while (j + 1 < layout.length && layout[j + 1].items.some((x) => x.el === el)) j++;
      return (j + 1 < layout.length ? ms(layout[j + 1].t) : end) - ms(t);
    };
    const push = (type: string, el: string, extra: object) => diffs.push({ type, t_ms: ms(t), target: el, caused_by: [...new Set(cause)], ...extra });
    for (const [el, it] of next) {
      const p = prev.get(el);
      if (!p) push('element_added', el, { role: it.role, text: it.text, bbox: it.bbox, visibility: it.vis, visible_for_ms: lifetime(el) });
      else {
        if (p.text !== it.text && !['list', 'slide', 'column'].includes(it.role)) push('text_changed', el, { before: p.text, after: it.text });
        if (p.vis !== it.vis) push('visibility_changed', el, { before: p.vis, after: it.vis });
      }
    }
    for (const [el, p] of prev) if (!next.has(el)) push('element_removed', el, { role: p.role, text: p.text });
    const z = (k: number) => layout[k].wins.toSorted((a, b) => a.z - b.z).map((w) => w.id);
    if (z(i - 1).join() !== z(i).join()) push('z_order_changed', 'screen', { before: z(i - 1), after: z(i) });
  }

  const timeline = [
    ...actions.map((a) => ({ kind: 'action', ...a })),
    ...diffs.map((d) => ({ kind: 'ui_change', ...d })),
    ...transcript.map((u) => ({ kind: 'speech', t_ms: u.start_ms, end_ms: u.end_ms, utterance: u.id, speaker_id: u.speaker_id, text: u.text })),
  ].sort((a, b) => a.t_ms - b.t_ms);

  const links = tl.lines.flatMap((l) =>
    l.anchors.map((a) => {
      const target = a.kind === 'focus' ? `${a.target}/__title` : a.target;
      const resolved = target !== '?';
      return {
        utterance: l.id,
        speaker_id: l.who,
        phrase: a.phrase,
        start_ms: ms(a.start),
        end_ms: ms(a.end),
        relation: a.kind === 'ref' ? 'mentions' : a.kind,
        target: resolved ? target : 'unresolved',
        target_text: resolved ? elText(target, a.kind === 'ref' ? a.end : a.start) : null,
      };
    }),
  );

  // step name -> event or line
  const ref = (n: string) => {
    const e = tl.events.find((x) => x.name === n);
    if (e) {
      const endEv = tl.events.find((x) => x.expires === n);
      return { name: n, event_id: evId.get(e)!, t_ms: ms(e.t), duration_ms: endEv ? ms(endEv.t - e.t) : null };
    }
    const l = tl.lines.find((x) => x.name === n);
    if (l) return { name: n, utterance: l.id, speaker_id: l.who, t_ms: ms(l.start), end_ms: ms(l.end), text: l.text };
    if (n.includes('/')) return { element: n };
    throw new Error(`${sc.id}: ${n} not found among events, lines or elements`);
  };

  const environment = sc.windows.map((w) => ({ window: w.id, title: w.title, app: APPS[w.app].name, ...APPS[w.app].who(w.state) }));

  const report = sc.bug && {
    title: sc.bug.title,
    class: sc.bug.class,
    environment,
    steps: actions
      .filter((a) => a.actor === 'user')
      .map((a, i) => ({
        n: i + 1,
        t_ms: a.t_ms,
        event_id: a.event_id,
        action: a.type,
        target: 'target' in a ? a.target : null,
        target_text: 'target_text' in a ? a.target_text : null,
        text: 'text' in a ? a.text : undefined,
        key: 'key' in a ? a.key : undefined,
        window_title: 'window_title' in a ? a.window_title : null,
      })),
    expected: sc.bug.expected,
    actual: sc.bug.actual,
    critical: sc.bug.critical.map(ref),
    traps: sc.bug.traps ?? [],
  };

  const requirements = sc.requirements?.map((r) => ({ ...r, evidence: r.evidence.map(ref) }));

  const show = sc.windows.find((w) => w.app === 'meet' || w.app === 'slides');
  let slides = null;
  if (show && sc.decks) {
    const deck = sc.decks.find((d) => d.id === (show.state as MeetState | SlidesState).deck)!;
    const shown: { slide_id: string; index: number; mode: string; start_ms: number; end_ms: number }[] = [];
    for (const [i, seg] of layout.entries()) {
      const st = stateAt(sc, tl, seg.t).apps[show.id] as MeetState | SlidesState;
      const mode = show.app === 'meet' ? 'meeting_stage' : (st as SlidesState).mode;
      const last = shown[shown.length - 1];
      const segEnd = i + 1 < layout.length ? ms(layout[i + 1].t) : end;
      if (last && last.index === st.slide + 1 && last.mode === mode) last.end_ms = segEnd;
      else shown.push({ slide_id: deck.slides[st.slide].id, index: st.slide + 1, mode, start_ms: ms(seg.t), end_ms: segEnd });
    }
    slides = {
      deck: deck.file,
      shown,
      attachments: (sc.attachments ?? []).map((a) => {
        const d = sc.decks!.find((x) => x.id === a.deck)!;
        return {
          file: d.file.replace(/\.\w+$/, `.${a.format}`),
          format: a.format,
          differs_from_screen: Object.keys(a.overrides ?? {}).map((id) => ({ slide_id: id, index: d.slides.findIndex((s) => s.id === id) + 1 })),
        };
      }),
    };
  }

  // in a meeting recording only the screen is parsed: people are in a separate strip
  const regions = sc.recording
    ? (() => {
        const r = recordingRegions(sc);
        const b = (x: { x: number; y: number; w: number; h: number }) => [x.x, x.y, x.w, x.h].map(Math.round);
        return { screen: b(r.screen), people: b(r.strip), screen_scale: +r.k.toFixed(4) };
      })()
    : { screen: [0, 0, sc.screen.w, sc.screen.h], people: null, screen_scale: 1 };

  return { transcript, speakers, states, timeline, links, report, requirements, slides, environment, regions, traps: sc.traps ?? [] };
}
