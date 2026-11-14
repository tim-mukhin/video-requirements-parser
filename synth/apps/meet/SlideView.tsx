import React from 'react';
import type { Slide } from '../../format/scenario.ts';

export const SLIDE_W = 1600;
export const SLIDE_H = 900;
const ACCENT = '#0f766e';

export const SlideView: React.FC<{ slide: Slide; n: number; total: number; deck: string; prefix?: string }> = ({ slide, n, total, deck, prefix }) => {
  const E = (id?: string, role = 'text') => (prefix ? { 'data-el': id ? `${prefix}/${id}` : prefix, 'data-role': role } : {});
  const cover = !slide.bullets && !slide.table;
  return (
    <div {...E(undefined, 'slide')} style={{ width: SLIDE_W, height: SLIDE_H, background: '#fff', color: '#0f172a', position: 'relative', overflow: 'hidden', fontFamily: 'inherit' }}>
      <div style={{ position: 'absolute', left: 0, top: 0, bottom: 0, width: 18, background: ACCENT }} />
      {cover ? (
        <div style={{ position: 'absolute', left: 140, right: 140, top: 300 }}>
          <div {...E('title', 'heading')} style={{ fontSize: 88, fontWeight: 700, letterSpacing: -1.5, lineHeight: 1.05 }}>{slide.title}</div>
          {slide.subtitle && <div {...E('subtitle')} style={{ fontSize: 40, color: '#475569', marginTop: 28 }}>{slide.subtitle}</div>}
        </div>
      ) : (
        <div style={{ position: 'absolute', left: 110, right: 110, top: 80 }}>
          <div {...E('title', 'heading')} style={{ fontSize: 64, fontWeight: 700, letterSpacing: -1, marginBottom: 48 }}>{slide.title}</div>
          {slide.bullets?.map((b, i) => (
            <div key={i} {...E(`b:${i}`, 'listitem')} style={{ display: 'flex', gap: 24, alignItems: 'baseline', fontSize: 40, lineHeight: 1.35, marginBottom: 26 }}>
              <div style={{ width: 14, height: 14, borderRadius: 7, background: ACCENT, flexShrink: 0, transform: 'translateY(-6px)' }} />
              {b}
            </div>
          ))}
          {slide.table && (
            <div style={{ display: 'flex', border: '2px solid #cbd5e1', borderRadius: 12, overflow: 'hidden' }}>
              {slide.table.columns.map((c, ci) => (
                <div key={c.id} {...E(`col:${c.id}`, 'column')} style={{ flex: 1, borderLeft: ci ? '2px solid #e2e8f0' : undefined }}>
                  <div style={{ background: '#f1f5f9', fontWeight: 700, fontSize: 30, padding: '18px 22px', borderBottom: '2px solid #cbd5e1' }}>{c.label}</div>
                  {slide.table!.rows.map((r, ri) => (
                    <div key={ri} style={{ fontSize: 28, padding: '18px 22px', borderTop: ri ? '1px solid #e2e8f0' : undefined, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>{r[ci]}</div>
                  ))}
                </div>
              ))}
            </div>
          )}
        </div>
      )}
      <div style={{ position: 'absolute', left: 110, right: 70, bottom: 36, display: 'flex', justifyContent: 'space-between', fontSize: 22, color: '#94a3b8' }}>
        <span>{deck}</span>
        <span {...E('page')}>{n} / {total}</span>
      </div>
    </div>
  );
};
