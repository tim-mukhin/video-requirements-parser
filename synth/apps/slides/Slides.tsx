import React from 'react';
import type { Deck } from '../../format/scenario.ts';
import type { SlidesState } from './model.ts';
import { SLIDE_H, SLIDE_W, SlideView } from '../meet/SlideView.tsx';
import { UI } from '../../i18n.ts';
import type { Lang } from '../../i18n.ts';


const Scaled: React.FC<{ k: number; children: React.ReactNode }> = ({ k, children }) => (
  <div style={{ width: SLIDE_W * k, height: SLIDE_H * k, overflow: 'hidden', position: 'relative' }}>
    <div style={{ transform: `scale(${k})`, transformOrigin: '0 0', position: 'absolute' }}>{children}</div>
  </div>
);

export const SlideShow: React.FC<{ s: SlidesState; win: string; deck: Deck; box: [number, number] }> = ({ s, win, deck, box }) => {
  const k = Math.min(box[0] / SLIDE_W, box[1] / SLIDE_H);
  const name = deck.file.replace(/\.\w+$/, '');
  return (
    <div style={{ width: box[0], height: box[1], background: '#000', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      <Scaled k={k}>
        <SlideView slide={deck.slides[s.slide]} n={s.slide + 1} total={deck.slides.length} deck={name} prefix={`${win}/slide`} />
      </Scaled>
    </div>
  );
};

export const Slides: React.FC<{ s: SlidesState; win: string; deck: Deck; box: [number, number]; lang: Lang }> = ({ s, win, deck, box, lang }) => {
  const T = UI[lang].slides;
  const [w, h] = box;
  const E = (id: string, role: string, label?: string) => ({ 'data-el': `${win}/${id}`, 'data-role': role, 'data-label': label });
  const name = deck.file.replace(/\.\w+$/, '');
  const THUMBS = 230;
  const NOTES = 120;
  const TOP = 104;
  const STATUS = 28;
  const canvasW = w - THUMBS - 60;
  const canvasH = h - TOP - NOTES - STATUS - 40;
  const k = Math.min(canvasW / SLIDE_W, canvasH / SLIDE_H);
  const slide = deck.slides[s.slide];
  return (
    <div style={{ width: w, height: h, background: '#f3f4f6', color: '#111827', position: 'relative', fontSize: 13 }}>
      <div style={{ height: 34, background: '#b91c1c', color: '#fff', display: 'flex', alignItems: 'center', gap: 20, padding: '0 16px' }}>
        {T.ribbon.map((r, i) => (
          <span key={r} {...E(`tab:${r}`, 'tab')} style={{ fontWeight: i === 1 ? 700 : 400, borderBottom: i === 1 ? '2px solid #fff' : undefined, paddingBottom: 2 }}>{r}</span>
        ))}
        <span {...E('present', 'button', T.start)} style={{ marginLeft: 'auto', background: 'rgba(255,255,255,.18)', borderRadius: 6, padding: '3px 10px' }}>{T.present}</span>
      </div>
      <div style={{ height: 70, background: '#fff', borderBottom: '1px solid #e5e7eb', display: 'flex', alignItems: 'center', gap: 10, padding: '0 14px' }}>
        {T.tools.map((t) => (
          <div key={t} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 4, padding: '0 10px', borderRight: '1px solid #f1f5f9', color: '#374151' }}>
            <div style={{ width: 26, height: 22, borderRadius: 4, background: '#e5e7eb' }} />
            <span style={{ fontSize: 11 }}>{t}</span>
          </div>
        ))}
      </div>
      <div style={{ position: 'absolute', left: 0, top: TOP, width: THUMBS, bottom: STATUS, background: '#e5e7eb', overflow: 'hidden', padding: '10px 12px' }}>
        {deck.slides.map((sl, i) => (
          <div key={sl.id} {...E(`thumb:${i}`, 'thumbnail', T.thumb(i + 1))} style={{ display: 'flex', gap: 6, marginBottom: 10 }}>
            <span style={{ width: 16, color: '#6b7280', fontSize: 12 }}>{i + 1}</span>
            <div style={{ outline: i === s.slide ? '3px solid #b91c1c' : '1px solid #d1d5db', borderRadius: 2 }}>
              <Scaled k={180 / SLIDE_W}>
                <SlideView slide={sl} n={i + 1} total={deck.slides.length} deck={name} />
              </Scaled>
            </div>
          </div>
        ))}
      </div>
      <div style={{ position: 'absolute', left: THUMBS + 30, top: TOP + 18, boxShadow: '0 2px 10px rgba(0,0,0,.15)' }}>
        <Scaled k={k}>
          <SlideView slide={slide} n={s.slide + 1} total={deck.slides.length} deck={name} prefix={`${win}/slide`} />
        </Scaled>
      </div>
      <div {...E('notes', 'textbox')} style={{ position: 'absolute', left: THUMBS, right: 0, bottom: STATUS, height: NOTES, background: '#fff', borderTop: '1px solid #d1d5db', padding: '10px 30px', fontSize: 14, color: slide.notes ? '#111827' : '#9ca3af' }}>
        {slide.notes ?? T.notes}
      </div>
      <div style={{ position: 'absolute', left: 0, right: 0, bottom: 0, height: STATUS, background: '#f3f4f6', borderTop: '1px solid #d1d5db', display: 'flex', alignItems: 'center', padding: '0 14px', gap: 20, color: '#4b5563', fontSize: 12 }}>
        <span {...E('status', 'status')}>{T.status(s.slide + 1, deck.slides.length)}</span>
        <span>{T.lang}</span>
        <span style={{ marginLeft: 'auto' }}>{T.zoom}</span>
      </div>
    </div>
  );
};
