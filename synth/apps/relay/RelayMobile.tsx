import React from 'react';
import type { RelayMsg, RelayState } from './model.ts';
import { thread } from './model.ts';
import { UI } from '../../i18n.ts';
import type { Lang } from '../../i18n.ts';

const C = { brand: '#4f46e5', ink: '#111827', muted: '#6b7280', line: '#e5e7eb', bg: '#f3f4f6', red: '#dc2626', ext: '#c2410c' };
const KIND: Record<string, string> = { pdf: '#dc2626', xlsx: '#16a34a', docx: '#2563eb', png: '#9333ea' };
const P = (d: string, size = 40, color = 'currentColor', fill = false) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill={fill ? color : 'none'} stroke={fill ? 'none' : color} strokeWidth={2} strokeLinecap="round" strokeLinejoin="round"><path d={d} /></svg>
);
const I = {
  back: 'M15 18l-6-6 6-6',
  plus: 'M12 5v14M5 12h14',
  send: 'M2 21l21-9L2 3v7l15 2-15 2z',
  lock: 'M6 11h12v10H6zM8 11V7a4 4 0 018 0v4',
  alert: 'M12 8v5M12 16.5v.5M12 21a9 9 0 100-18 9 9 0 000 18z',
  retry: 'M4 4v6h6M20 20v-6h-6M5.5 15a8 8 0 0013.1 3M18.5 9A8 8 0 005.4 6',
};

const Status: React.FC<{ m: RelayMsg; T: (typeof UI)['en']['relay'] }> = ({ m, T }) => {
  if (m.status === 'failed')
    return <span style={{ color: '#fecaca', display: 'inline-flex', alignItems: 'center', gap: 6 }}>{P(I.alert, 26, '#fecaca')} {T.failed}</span>;
  if (m.status === 'uploading') return <span>{T.uploading(m.progress!)}</span>;
  if (m.status === 'sending') return <span>{T.sending}</span>;
  if (m.status === 'scheduled') return <span>{T.scheduledAt(m.scheduledFor!)}</span>;
  return <span>{m.status === 'delivered' ? '✓✓' : '✓'}</span>;
};

export const RelayMobile: React.FC<{ s: RelayState; win: string; box: [number, number]; lang: Lang }> = ({ s, win, box, lang }) => {
  const T = UI[lang].relay;
  const E = (id: string, role: string, label?: string) => ({ 'data-el': `${win}/${id}`, 'data-role': role, 'data-label': label });
  const chat = s.chats.find((c) => c.id === s.active)!;
  return (
    <div style={{ width: box[0], height: box[1], background: C.bg, color: C.ink, position: 'relative', display: 'flex', flexDirection: 'column', fontSize: 34 }}>
      <div {...E('chat-header', 'header')} style={{ background: '#fff', borderBottom: `2px solid ${C.line}`, padding: '24px 28px', display: 'flex', alignItems: 'center', gap: 20 }}>
        <span style={{ color: C.brand }}>{P(I.back, 52, C.brand)}</span>
        <div style={{ width: 88, height: 88, borderRadius: 44, background: chat.external ? '#ea580c' : '#6366f1', color: '#fff', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 600, fontSize: 34 }}>{chat.initials}</div>
        <div>
          <div style={{ fontWeight: 600, fontSize: 38 }}>{chat.title}</div>
          <div style={{ fontSize: 26, color: chat.external ? C.ext : C.muted }}>{chat.external ? T.externalOrg(chat.external) : T.online}</div>
        </div>
      </div>
      <div {...E('messages', 'list')} style={{ flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'flex-end', gap: 22, padding: '28px 28px' }}>
        {thread(s).map((m) => (
          <div key={m.id} style={{ display: 'flex', justifyContent: m.mine ? 'flex-end' : 'flex-start' }}>
            <div {...E(`msg:${m.id}`, m.file ? 'file' : 'message')} style={{ maxWidth: '80%', background: m.mine ? (m.status === 'failed' ? '#991b1b' : C.brand) : '#fff', color: m.mine ? '#fff' : C.ink, borderRadius: 34, padding: m.file ? 22 : '20px 28px', boxShadow: '0 2px 4px rgba(0,0,0,.06)' }}>
              {!m.mine && <div style={{ fontSize: 26, fontWeight: 600, color: '#ea580c', marginBottom: 8 }}>{m.author}</div>}
              {m.text && <div>{m.text}</div>}
              {m.file && (
                <div style={{ display: 'flex', gap: 20, alignItems: 'center', minWidth: 520 }}>
                  <div style={{ width: 84, height: 100, borderRadius: 14, background: m.blocked ? '#9ca3af' : KIND[m.file.kind], color: '#fff', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 24, fontWeight: 700 }}>
                    {m.blocked ? P(I.lock, 40, '#fff') : m.file.kind.toUpperCase()}
                  </div>
                  <div>
                    <div style={{ fontWeight: 600, fontSize: 32 }}>{m.file.name}</div>
                    <div style={{ fontSize: 26, opacity: 0.75 }}>{m.blocked ? T.unavailable : m.file.size}</div>
                    {m.status === 'uploading' && (
                      <div style={{ width: 340, height: 8, borderRadius: 4, background: 'rgba(255,255,255,.3)', marginTop: 12 }}>
                        <div style={{ width: `${m.progress}%`, height: 8, borderRadius: 4, background: '#fff' }} />
                      </div>
                    )}
                  </div>
                </div>
              )}
              <div style={{ display: 'flex', justifyContent: 'flex-end', gap: 10, fontSize: 24, opacity: 0.8, marginTop: 8 }}>
                {m.time} {m.mine && <Status m={m} T={T} />}
              </div>
              {m.status === 'failed' && (
                <div {...E(`retry:${m.id}`, 'button', T.retry)} style={{ marginTop: 12, display: 'inline-flex', alignItems: 'center', gap: 10, fontSize: 28, background: 'rgba(255,255,255,.18)', borderRadius: 20, padding: '8px 18px' }}>
                  {P(I.retry, 28, '#fff')} {T.retry}
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
      <div style={{ background: '#fff', borderTop: `2px solid ${C.line}`, padding: '18px 24px 40px' }}>
        {s.staged && (
          <div {...E('staged', 'attachment')} style={{ display: 'inline-flex', gap: 14, alignItems: 'center', background: '#eef2ff', borderRadius: 18, padding: '12px 20px', marginBottom: 16, fontSize: 28 }}>
            {s.staged.name} · {s.staged.size}
          </div>
        )}
        <div style={{ display: 'flex', alignItems: 'center', gap: 18 }}>
          <div {...E('attach', 'button', T.attachShort)} style={{ width: 80, height: 80, borderRadius: 40, background: C.bg, display: 'flex', alignItems: 'center', justifyContent: 'center', color: C.brand }}>{P(I.plus, 48, C.brand)}</div>
          <div {...E('composer', 'textbox', T.message)} style={{ flex: 1, height: 80, borderRadius: 40, background: C.bg, display: 'flex', alignItems: 'center', padding: '0 30px', color: C.muted, fontSize: 32 }}>{T.message}</div>
          <div {...E('send', 'button', T.send)} style={{ width: 80, height: 80, borderRadius: 40, background: s.staged ? C.brand : '#c7d2fe', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>{P(I.send, 38, '#fff', true)}</div>
        </div>
      </div>

      {s.toast && (
        <div {...E('toast', 'alert')} style={{ position: 'absolute', left: 30, right: 30, top: 180, background: s.toast.tone === 'error' ? C.red : '#111827', color: '#fff', padding: '24px 28px', borderRadius: 24, fontSize: 30, zIndex: 4 }}>
          {s.toast.text}
        </div>
      )}

      {s.picker && (
        <div style={{ position: 'absolute', inset: 0, background: 'rgba(0,0,0,.35)', zIndex: 3, pointerEvents: 'none' }}>
          <div {...E('picker', 'menu')} style={{ pointerEvents: 'auto', position: 'absolute', left: 0, right: 0, bottom: 0, background: '#fff', borderRadius: '40px 40px 0 0', padding: '20px 30px 60px' }}>
            <div style={{ width: 90, height: 10, borderRadius: 5, background: '#d1d5db', margin: '0 auto 24px' }} />
            <div style={{ fontSize: 30, color: C.muted, marginBottom: 14 }}>{T.recentFiles}</div>
            {s.files.map((f) => (
              <div key={f.id} {...E(`file:${f.id}`, 'menuitem')} style={{ display: 'flex', gap: 22, alignItems: 'center', padding: '18px 0', borderBottom: `2px solid ${C.line}` }}>
                <div style={{ width: 64, height: 76, borderRadius: 10, background: KIND[f.kind], color: '#fff', fontSize: 18, fontWeight: 700, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>{f.kind.toUpperCase()}</div>
                <div>
                  <div style={{ fontSize: 32 }}>{f.name}</div>
                  <div style={{ fontSize: 26, color: C.muted }}>{f.size}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {s.dialog && (
        <div style={{ position: 'absolute', inset: 0, background: 'rgba(0,0,0,.35)', zIndex: 5, display: 'flex', alignItems: 'center', justifyContent: 'center', pointerEvents: 'none' }}>
          <div {...E('dialog', 'dialog')} style={{ pointerEvents: 'auto', width: 760, background: 'rgba(250,250,250,.98)', borderRadius: 40, overflow: 'hidden', textAlign: 'center' }}>
            <div style={{ padding: '40px 40px 30px' }}>
              <div style={{ fontWeight: 700, fontSize: 36, marginBottom: 14 }}>{T.unavailable}</div>
              <div style={{ fontSize: 28, color: '#374151', lineHeight: 1.4 }}>{s.dialog.text}</div>
            </div>
            <div {...E('dialog-ok', 'button')} style={{ borderTop: `2px solid ${C.line}`, padding: '26px 0', color: '#2563eb', fontSize: 34, fontWeight: 600 }}>OK</div>
          </div>
        </div>
      )}
    </div>
  );
};
