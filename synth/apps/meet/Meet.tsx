import React from 'react';
import type { Deck } from '../../format/scenario.ts';
import type { MeetState } from './model.ts';
import { SLIDE_H, SLIDE_W, SlideView } from './SlideView.tsx';
import { UI } from '../../i18n.ts';
import type { Lang } from '../../i18n.ts';

const RAIL = 300;
const TOP = 52;
const BAR = 76;

const Mic: React.FC<{ off?: boolean }> = ({ off }) => (
  <svg width={18} height={18} viewBox="0 0 24 24" fill="none" stroke={off ? '#f87171' : '#e5e7eb'} strokeWidth={2} strokeLinecap="round">
    <path d="M12 3a3 3 0 00-3 3v6a3 3 0 006 0V6a3 3 0 00-3-3zM5 11a7 7 0 0014 0M12 18v3" />
    {off && <path d="M3 3l18 18" />}
  </svg>
);

const mmss = (sec: number) => `${String(Math.floor(sec / 60)).padStart(2, '0')}:${String(Math.floor(sec % 60)).padStart(2, '0')}`;

export const Meet: React.FC<{ s: MeetState; win: string; t: number; deck: Deck; speaking: string[]; box: [number, number]; lang: Lang }> = ({ s, win, t, deck, speaking, box, lang }) => {
  const T = UI[lang].meet;
  const [w, h] = box;
  const stageW = w - RAIL - 32;
  const stageH = h - TOP - BAR - 56;
  const k = Math.min(stageW / SLIDE_W, stageH / SLIDE_H);
  const presenter = s.people.find((p) => p.id === s.presenter)!;
  return (
    <div style={{ width: w, height: h, background: '#111827', color: '#f9fafb', position: 'relative' }}>
      <div {...{ 'data-el': `${win}/header`, 'data-role': 'header' }} style={{ height: TOP, display: 'flex', alignItems: 'center', gap: 14, padding: '0 20px', borderBottom: '1px solid #1f2937', fontSize: 16 }}>
        <span style={{ display: 'inline-flex', alignItems: 'center', gap: 6, color: '#f87171', fontWeight: 600, fontSize: 13 }}>
          <span style={{ width: 9, height: 9, borderRadius: 5, background: '#ef4444' }} /> {T.rec}
        </span>
        <span style={{ fontWeight: 600 }}>{s.title}</span>
        <span style={{ color: '#9ca3af', fontVariantNumeric: 'tabular-nums' }}>{mmss(s.elapsed + t)}</span>
      </div>
      <div style={{ position: 'absolute', left: 16, top: TOP + 12, width: stageW, height: stageH + 32 }}>
        <div style={{ fontSize: 14, color: '#9ca3af', marginBottom: 10 }}>{T.presenting(presenter.name)}</div>
        <div style={{ width: SLIDE_W * k, height: SLIDE_H * k, boxShadow: '0 8px 30px rgba(0,0,0,.5)', borderRadius: 6, overflow: 'hidden' }}>
          <div style={{ transform: `scale(${k})`, transformOrigin: '0 0' }}>
            <SlideView slide={deck.slides[s.slide]} n={s.slide + 1} total={deck.slides.length} deck={deck.file.replace(/\.\w+$/, '')} prefix={`${win}/slide`} />
          </div>
        </div>
      </div>
      <div style={{ position: 'absolute', right: 16, top: TOP + 16, width: RAIL - 16, display: 'flex', flexDirection: 'column', gap: 12 }}>
        {s.people.map((p) => {
          const on = speaking.includes(p.id);
          return (
            <div key={p.id} {...{ 'data-el': `${win}/tile:${p.id}`, 'data-role': 'participant' }} style={{ height: 150, borderRadius: 12, background: '#1f2937', position: 'relative', display: 'flex', alignItems: 'center', justifyContent: 'center', outline: on ? '3px solid #22c55e' : '1px solid #374151' }}>
              <div style={{ width: 64, height: 64, borderRadius: 32, background: p.color, display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 600, fontSize: 24 }}>{p.initials}</div>
              <div style={{ position: 'absolute', left: 10, bottom: 8, display: 'flex', alignItems: 'center', gap: 6, fontSize: 13, background: 'rgba(0,0,0,.45)', padding: '3px 8px', borderRadius: 6 }}>
                <Mic off={p.muted} /> {p.name}
              </div>
            </div>
          );
        })}
      </div>
      <div style={{ position: 'absolute', left: 0, right: 0, bottom: 0, height: BAR, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 14, borderTop: '1px solid #1f2937' }}>
        {Object.entries(T.buttons).map(([k, l]) => (
          <div key={k} {...{ 'data-el': `${win}/btn:${k}`, 'data-role': 'button' }} style={{ padding: '10px 16px', borderRadius: 10, background: '#1f2937', fontSize: 14, color: '#d1d5db' }}>{l}</div>
        ))}
        <div {...{ 'data-el': `${win}/leave`, 'data-role': 'button' }} style={{ padding: '10px 18px', borderRadius: 10, background: '#dc2626', fontSize: 14, fontWeight: 600 }}>{T.leave}</div>
      </div>
    </div>
  );
};
