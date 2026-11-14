import React, { useLayoutEffect, useRef } from 'react';
import { AbsoluteFill, continueRender, delayRender, useCurrentFrame } from 'remotion';
import { loadFont } from '@remotion/google-fonts/Inter';
import type { Scenario, Tile, Win } from '../format/scenario.ts';
import { speakingAt, stateAt } from '../compile/timeline.ts';
import type { DeskState, Devtools, Timeline } from '../compile/timeline.ts';
import { cursorAt, touchesAt } from './cursor.ts';
import type { Layout, Vis } from './cursor.ts';
import { AppView } from '../apps/views.tsx';
import { recordingRegions } from './regions.ts';
import { APPS } from '../apps/registry.ts';
import type { SlidesState } from '../apps/slides/model.ts';
import { UI } from '../i18n.ts';
import type { Lang } from '../i18n.ts';

export type { Layout, ProbeItem, ProbeWin, Vis } from './cursor.ts';

const { fontFamily } = loadFont('normal', { weights: ['400', '500', '600', '700'], subsets: ['latin', 'cyrillic'] });

const TITLE = 38;
const MENU = 30;
const BROWSER = 82;
const DEVTOOLS = 290;
const PHONE_BAR = 110;

// --- cursor and touches ---

const Cursor: React.FC<{ x: number; y: number; ring: number; k: number }> = ({ x, y, ring, k }) => (
  <div style={{ position: 'absolute', left: 0, top: 0, transform: `translate(${x}px, ${y}px) scale(${k})`, transformOrigin: '0 0', pointerEvents: 'none', zIndex: 1000 }}>
    {ring >= 0 && (
      <div style={{ position: 'absolute', left: -18, top: -18, width: 36, height: 36, borderRadius: 18, border: '3px solid rgba(79,70,229,.8)', transform: `scale(${0.4 + ring})`, opacity: 1 - ring }} />
    )}
    <svg width={26} height={30} viewBox="0 0 26 30" style={{ position: 'absolute', left: -3, top: -2, filter: 'drop-shadow(0 2px 2px rgba(0,0,0,.35))' }}>
      <path d="M3 2 L3 24 L9 18.5 L13 27 L17 25 L13 17 L21 17 Z" fill="#fff" stroke="#000" strokeWidth={1.6} strokeLinejoin="round" />
    </svg>
  </div>
);

const Touch: React.FC<{ x: number; y: number; a: number }> = ({ x, y, a }) => (
  <div style={{ position: 'absolute', left: x - 44, top: y - 44, width: 88, height: 88, borderRadius: 44, background: `rgba(120,120,120,${0.45 * a})`, border: `3px solid rgba(255,255,255,${0.7 * a})`, pointerEvents: 'none', zIndex: 1000 }} />
);

// --- DOM snapshot for ground truth ---

function probe(root: HTMLElement, w: number, h: number): Omit<Layout[number], 't'> {
  const r0 = root.getBoundingClientRect();
  const k = r0.width / w;
  const box = (n: Element): [number, number, number, number] => {
    const r = n.getBoundingClientRect();
    return [(r.left - r0.left) / k, (r.top - r0.top) / k, r.width / k, r.height / k].map((v) => Math.round(v)) as [number, number, number, number];
  };
  const wins = [...root.querySelectorAll<HTMLElement>('[data-win]')].map((n) => ({
    id: n.dataset.win!,
    title: n.dataset.title!,
    bbox: box(n),
    z: Number(n.style.zIndex),
  }));
  const items = [...root.querySelectorAll<HTMLElement>('[data-el]')].map((n) => {
    const b = box(n);
    const pts = [[0.5, 0.5], [0.2, 0.2], [0.8, 0.2], [0.2, 0.8], [0.8, 0.8]];
    const inside = pts.filter(([fx, fy]) => {
      const x = b[0] + b[2] * fx;
      const y = b[1] + b[3] * fy;
      return x >= 0 && y >= 0 && x < w && y < h;
    });
    const seen = inside.some(([fx, fy]) => {
      const hit = document.elementFromPoint(r0.left + (b[0] + b[2] * fx) * k, r0.top + (b[1] + b[3] * fy) * k);
      return !!hit && n.contains(hit);
    });
    const vis: Vis = seen ? 'visible' : inside.length ? 'occluded' : 'out_of_view';
    return { el: n.dataset.el!, win: n.dataset.el!.split('/')[0], role: n.dataset.role ?? '', text: ((n.innerText ?? '').replace(/\s+/g, ' ').trim() || n.dataset.label || '').slice(0, 240), bbox: b, vis };
  });
  return { wins, items };
}

// --- browser ---

const DevToolsPanel: React.FC<{ d: Devtools; win: string; lang: Lang }> = ({ d, win, lang }) => {
  const T = UI[lang].desktop;
  const E = (id: string, role: string) => ({ 'data-el': `${win}/devtools/${id}`, 'data-role': role });
  return (
    <div {...E('panel', 'panel')} style={{ position: 'absolute', left: 0, right: 0, bottom: 0, height: DEVTOOLS, background: '#fff', borderTop: '2px solid #cbd5e1', fontFamily: 'Menlo, monospace', fontSize: 13, color: '#1f2937', zIndex: 20 }}>
      <div style={{ display: 'flex', gap: 18, padding: '6px 12px', background: '#f1f5f9', borderBottom: '1px solid #e2e8f0', fontFamily: 'inherit' }}>
        {(['elements', 'console', 'network'] as const).map((t) => (
          <span key={t} {...E(`tab:${t}`, 'tab')} style={{ color: d.tab === t ? '#1d4ed8' : '#475569', borderBottom: d.tab === t ? '2px solid #1d4ed8' : undefined }}>
            {T.devtools[t]}
          </span>
        ))}
        {d.console.some((c) => c.level === 'error') && <span style={{ marginLeft: 'auto', color: '#dc2626' }}>✖ {d.console.filter((c) => c.level === 'error').length}</span>}
      </div>
      {d.tab === 'console' &&
        d.console.map((c, i) => (
          <div key={i} {...E(`console:${i}`, c.level === 'error' ? 'alert' : 'logline')} style={{ padding: '5px 12px', borderBottom: '1px solid #f1f5f9', background: c.level === 'error' ? '#fef2f2' : c.level === 'warn' ? '#fffbeb' : undefined, color: c.level === 'error' ? '#b91c1c' : c.level === 'warn' ? '#92400e' : '#334155', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
            {c.level === 'error' ? '✖ ' : c.level === 'warn' ? '⚠ ' : ''}
            {c.text}
          </div>
        ))}
      {d.tab === 'network' && (
        <>
          <div style={{ display: 'flex', padding: '4px 12px', color: '#64748b', borderBottom: '1px solid #e2e8f0' }}>
            <span style={{ width: 70 }}>{T.netCols[0]}</span><span style={{ flex: 1 }}>{T.netCols[1]}</span><span style={{ width: 70 }}>{T.netCols[2]}</span><span style={{ width: 70 }}>{T.netCols[3]}</span>
          </div>
          {d.network.map((r, i) => (
            <div key={i} {...E(`network:${i}`, 'row')} style={{ display: 'flex', padding: '4px 12px', borderBottom: '1px solid #f1f5f9', color: r.status >= 400 ? '#b91c1c' : '#334155' }}>
              <span style={{ width: 70 }}>{r.method}</span><span style={{ flex: 1 }}>{r.url}</span><span style={{ width: 70 }}>{r.status}</span><span style={{ width: 70 }}>{r.ms} {T.ms}</span>
            </div>
          ))}
        </>
      )}
    </div>
  );
};

const BrowserChrome: React.FC<{ w: Win; tabs: Win[]; front: boolean }> = ({ w, tabs, front }) => (
  <div style={{ height: BROWSER, background: front ? '#dee1e6' : '#eceef1' }}>
    <div data-el={`${w.id}/__title`} data-role="titlebar" style={{ height: 40, display: 'flex', alignItems: 'flex-end', gap: 2, padding: '0 12px' }}>
      <div style={{ display: 'flex', gap: 8, padding: '0 14px 14px 2px' }}>
        {['#ef4444', '#f59e0b', '#22c55e'].map((c) => <div key={c} style={{ width: 12, height: 12, borderRadius: 6, background: front ? c : '#d1d5db' }} />)}
      </div>
      {tabs.map((t) => (
        <div key={t.id} data-el={`${t.id}/__tab`} data-role="tab" style={{ width: 230, height: 32, borderRadius: '9px 9px 0 0', background: t.id === w.id ? '#fff' : 'transparent', display: 'flex', alignItems: 'center', padding: '0 12px', fontSize: 13, color: '#374151', whiteSpace: 'nowrap', overflow: 'hidden' }}>
          {t.browser!.tab}
        </div>
      ))}
    </div>
    <div style={{ height: 42, background: '#fff', display: 'flex', alignItems: 'center', gap: 12, padding: '0 14px', borderBottom: '1px solid #e5e7eb' }}>
      <span style={{ color: '#9ca3af', fontSize: 18 }}>‹ › ↻</span>
      <div data-el={`${w.id}/__url`} data-role="textbox" style={{ flex: 1, height: 30, borderRadius: 15, background: '#f1f3f4', display: 'flex', alignItems: 'center', padding: '0 14px', fontSize: 14, color: '#202124' }}>
        🔒&nbsp;{w.browser!.url}
      </div>
    </div>
  </div>
);

// --- presenter's screen ---

const Screen: React.FC<{ sc: Scenario; s: DeskState; t: number; speaking: string[] }> = ({ sc, s, t, speaking }) => {
  const T = UI[sc.lang].desktop;
  const top = sc.windows.find((w) => w.id === s.z[s.z.length - 1])!;
  const clock = sc.windows.map((w) => (s.apps[w.id] as { clock?: string }).clock).find(Boolean) ?? '10:43';
  const { w: W, h: H } = sc.screen;

  if (sc.device === 'phone') {
    return (
      <div style={{ position: 'absolute', inset: 0, background: '#fff' }}>
        <div style={{ height: PHONE_BAR, display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '20px 60px 0', fontSize: 36, fontWeight: 600, color: '#111' }}>
          <span>{clock}</span>
          <span style={{ fontSize: 28 }}>▂▄▆ 5G ▭</span>
        </div>
        <div data-win={top.id} data-title={top.title} style={{ position: 'absolute', left: 0, top: PHONE_BAR, width: W, height: H - PHONE_BAR, zIndex: 1 }}>
          <AppView w={top} s={s.apps[top.id]} sc={sc} t={t} speaking={speaking} box={[W, H - PHONE_BAR - 30]} />
        </div>
        <div style={{ position: 'absolute', left: W / 2 - 140, bottom: 14, width: 280, height: 10, borderRadius: 5, background: '#111', zIndex: 2 }} />
        {s.notify && (
          <div data-el="os/notify" data-role="notification" style={{ position: 'absolute', left: 24, right: 24, top: 30, zIndex: 900, background: 'rgba(245,245,245,.97)', borderRadius: 36, padding: '26px 30px', boxShadow: '0 10px 30px rgba(0,0,0,.25)', fontSize: 30 }}>
            <div style={{ fontWeight: 600 }}>{s.notify.app}: {s.notify.title}</div>
            <div style={{ color: '#4b5563' }}>{s.notify.text}</div>
          </div>
        )}
      </div>
    );
  }

  const groupTop = (w: Win) => {
    if (!w.browser) return true;
    const mates = sc.windows.filter((x) => x.browser?.group === w.browser!.group);
    return mates.every((x) => s.z.indexOf(x.id) <= s.z.indexOf(w.id));
  };

  return (
    <div style={{ position: 'absolute', inset: 0, background: sc.wallpaper }}>
      <div style={{ height: MENU, background: 'rgba(255,255,255,.55)', display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0 18px', fontSize: 14, fontWeight: 500, color: '#111' }}>
        <span><b>{top.browser ? T.browser : APPS[top.app].name}</b>{T.menu.map((m) => <React.Fragment key={m}>&nbsp;&nbsp;&nbsp;{m}</React.Fragment>)}</span>
        <span>{T.date} {clock}</span>
      </div>
      {sc.windows.filter(groupTop).map((w) => {
        const z = s.z.indexOf(w.id) + 1;
        const front = z === s.z.length;
        if (w.app === 'slides' && (s.apps[w.id] as SlidesState).mode === 'show') {
          return (
            <div key={w.id} data-win={w.id} data-title={w.title} style={{ position: 'absolute', left: 0, top: 0, width: W, height: H, zIndex: 800 }}>
              <AppView w={w} s={s.apps[w.id]} sc={sc} t={t} speaking={speaking} box={[W, H]} />
            </div>
          );
        }
        const [x, y, ww, hh] = w.bbox;
        const chrome = w.browser ? BROWSER : TITLE;
        const dev = s.devtools[w.id]?.open ? s.devtools[w.id] : undefined;
        const content = hh - chrome - (dev ? DEVTOOLS : 0);
        return (
          <div key={w.id} data-win={w.id} data-title={w.title} style={{ position: 'absolute', left: x, top: y, width: ww, height: hh, zIndex: z, borderRadius: 12, overflow: 'hidden', boxShadow: front ? '0 24px 60px rgba(0,0,0,.45)' : '0 10px 30px rgba(0,0,0,.3)', border: '1px solid rgba(0,0,0,.25)', background: '#fff' }}>
            {w.browser ? (
              <BrowserChrome w={w} tabs={sc.windows.filter((x2) => x2.browser?.group === w.browser!.group)} front={front} />
            ) : (
              <div data-el={`${w.id}/__title`} data-role="titlebar" style={{ height: TITLE, background: front ? '#e5e7eb' : '#f3f4f6', borderBottom: '1px solid #d1d5db', display: 'flex', alignItems: 'center', position: 'relative' }}>
                <div style={{ display: 'flex', gap: 8, paddingLeft: 14 }}>
                  {['#ef4444', '#f59e0b', '#22c55e'].map((c) => <div key={c} style={{ width: 12, height: 12, borderRadius: 6, background: front ? c : '#d1d5db' }} />)}
                </div>
                <div style={{ position: 'absolute', left: 0, right: 0, textAlign: 'center', fontSize: 14, fontWeight: 600, color: front ? '#374151' : '#9ca3af', pointerEvents: 'none' }}>{w.title}</div>
              </div>
            )}
            <div style={{ height: content, position: 'relative', overflow: 'hidden' }}>
              <AppView w={w} s={s.apps[w.id]} sc={sc} t={t} speaking={speaking} box={[ww, content]} />
            </div>
            {dev && <DevToolsPanel d={dev} win={w.id} lang={sc.lang} />}
          </div>
        );
      })}
      {s.notify && (
        <div data-el="os/notify" data-role="notification" style={{ position: 'absolute', right: 18, top: MENU + 12, width: 360, zIndex: 900, background: 'rgba(250,250,250,.96)', borderRadius: 14, padding: '12px 14px', boxShadow: '0 10px 30px rgba(0,0,0,.25)', display: 'flex', gap: 12 }}>
          <div style={{ width: 36, height: 36, borderRadius: 8, background: '#ef4444', color: '#fff', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 700 }}>14</div>
          <div style={{ fontSize: 13 }}>
            <div style={{ fontWeight: 600 }}>{s.notify.app}: {s.notify.title}</div>
            <div style={{ color: '#4b5563' }}>{s.notify.text}</div>
          </div>
        </div>
      )}
    </div>
  );
};

// --- meeting recording: screen and people are separate regions ---

const SKIN = ['#f1c27d', '#e0ac69', '#c68642', '#ffdbac', '#8d5524'];
const Figure: React.FC<{ x: number; y: number; s: number; shirt: string; skin: string }> = ({ x, y, s, shirt, skin }) => (
  <g transform={`translate(${x} ${y}) scale(${s})`}>
    <path d="M-34 60 Q-34 20 0 20 Q34 20 34 60 Z" fill={shirt} />
    <circle cx={0} cy={0} r={17} fill={skin} />
    <path d="M-17 -4 Q-15 -20 0 -20 Q15 -20 17 -4 Q8 -12 -17 -4Z" fill="#3f2a1d" />
  </g>
);

const TileView: React.FC<{ tile: Tile; on: boolean; w: number; h: number; i: number }> = ({ tile, on, w, h, i }) => {
  const n = tile.kind === 'room' ? tile.figures ?? 3 : 1;
  return (
    <div data-el={`rec/tile:${tile.id}`} data-role="participant" data-label={tile.name} style={{ width: w, height: h, borderRadius: 10, background: '#2b2f36', position: 'relative', overflow: 'hidden', outline: on ? '3px solid #22c55e' : '1px solid #3b4049', outlineOffset: -1 }}>
      <svg width={w} height={h} viewBox={`0 0 ${w} ${h}`} style={{ position: 'absolute', inset: 0 }}>
        {tile.kind === 'room' ? (
          <>
            <rect x={0} y={0} width={w} height={h} fill="#3a3f47" />
            <rect x={w * 0.06} y={h * 0.18} width={w * 0.88} height={h * 0.12} fill="#4b515b" />
            {Array.from({ length: n }, (_, k) => (
              <Figure key={k} x={w * (0.2 + (0.6 * k) / Math.max(1, n - 1))} y={h * 0.5} s={h / 230} shirt={['#64748b', '#0f766e', '#7c3aed', '#b45309'][k % 4]} skin={SKIN[(k + i) % SKIN.length]} />
            ))}
            <rect x={w * 0.1} y={h * 0.66} width={w * 0.8} height={h * 0.14} rx={8} fill="#8b6b4a" />
          </>
        ) : (
          <Figure x={w / 2} y={h * 0.42} s={h / 150} shirt={tile.color} skin={SKIN[i % SKIN.length]} />
        )}
      </svg>
      <div style={{ position: 'absolute', left: 8, bottom: 6, fontSize: 13, color: '#f3f4f6', background: 'rgba(0,0,0,.5)', padding: '2px 8px', borderRadius: 5, display: 'flex', gap: 6 }}>
        {tile.muted ? '🔇' : ''}
        {tile.name}
      </div>
    </div>
  );
};

const People: React.FC<{ sc: Scenario; speaking: string[] }> = ({ sc, speaking }) => {
  const r = sc.recording!;
  const { strip } = recordingRegions(sc);
  const tileOf = (cast: string) => sc.cast.find((c) => c.id === cast)?.tile ?? cast;
  const lit = new Set(speaking.map(tileOf));
  const top = r.layout === 'strip-top';
  const tw = top ? 260 : strip.w - 24;
  const th = top ? strip.h - 24 : 160;
  return (
    <div style={{ position: 'absolute', left: strip.x, top: strip.y, width: strip.w, height: strip.h, display: 'flex', flexDirection: top ? 'row' : 'column', justifyContent: 'center', alignItems: 'center', gap: 12, background: '#16181d' }}>
      {r.tiles.map((t, i) => (
        <TileView key={t.id} tile={t} on={lit.has(t.id)} w={t.kind === 'room' && top ? tw * 1.5 : tw} h={th} i={i} />
      ))}
    </div>
  );
};

// --- whole frame ---

export const Desktop: React.FC<{ sc: Scenario; tl: Timeline; layout?: Layout; probeMode?: boolean }> = ({ sc, tl, layout, probeMode }) => {
  const frame = useCurrentFrame();
  const t = probeMode ? tl.segments[frame] : frame / tl.fps;
  const s = stateAt(sc, tl, t);
  const root = useRef<HTMLDivElement>(null);
  const F = sc.recording?.frame ?? sc.screen;

  useLayoutEffect(() => {
    if (!probeMode || !root.current) return;
    const node = root.current;
    const h = delayRender(`probe ${frame}`);
    const shot = () => {
      if (node.getBoundingClientRect().width === 0) return requestAnimationFrame(shot);
      console.debug('PROBE ' + JSON.stringify({ seg: frame, t, ...probe(node, F.w, F.h) }));
      continueRender(h);
    };
    document.fonts.ready.then(() => requestAnimationFrame(shot));
  }, [probeMode, frame, t, F.w, F.h]);

  const speaking = speakingAt(tl, t);
  const phone = sc.device === 'phone';
  const cur = !probeMode && layout && !phone ? cursorAt(tl, layout, t) : null;
  const touches = !probeMode && layout && phone ? touchesAt(tl, layout, t) : [];
  const rec = sc.recording ? recordingRegions(sc) : null;
  const screen = <Screen sc={sc} s={s} t={t} speaking={speaking} />;

  return (
    <AbsoluteFill ref={root} style={{ background: rec ? '#0b0c0f' : '#000', fontFamily }}>
      {rec ? (
        <>
          <People sc={sc} speaking={speaking} />
          <div data-region="screen" style={{ position: 'absolute', left: rec.screen.x, top: rec.screen.y, width: sc.screen.w, height: sc.screen.h, transform: `scale(${rec.k})`, transformOrigin: '0 0', overflow: 'hidden' }}>
            {screen}
          </div>
        </>
      ) : (
        screen
      )}
      {cur && <Cursor x={cur.pos[0]} y={cur.pos[1]} ring={cur.ring} k={rec?.k ?? 1} />}
      {touches.map((p, i) => <Touch key={i} x={p.x} y={p.y} a={p.a} />)}
    </AbsoluteFill>
  );
};
