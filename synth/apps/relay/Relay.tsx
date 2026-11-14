import React from 'react';
import type { RelayFile, RelayMsg, RelayState } from './model.ts';
import { UI } from '../../i18n.ts';
import type { Lang } from '../../i18n.ts';
import { thread } from './model.ts';

const C = {
  brand: '#4f46e5',
  brandSoft: '#eef2ff',
  ink: '#111827',
  muted: '#6b7280',
  line: '#e5e7eb',
  side: '#f8fafc',
  bg: '#f3f4f6',
  red: '#dc2626',
  ext: '#c2410c',
};
const KIND: Record<RelayFile['kind'], string> = { pdf: '#dc2626', xlsx: '#16a34a', docx: '#2563eb', png: '#9333ea' };

const Icon: React.FC<{ d: string; size?: number; color?: string; fill?: boolean }> = ({ d, size = 20, color = 'currentColor', fill }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill={fill ? color : 'none'} stroke={fill ? 'none' : color} strokeWidth={2} strokeLinecap="round" strokeLinejoin="round">
    <path d={d} />
  </svg>
);
const I = {
  clip: 'M21.4 11.1l-9.2 9.2a6 6 0 01-8.5-8.5l9.2-9.2a4 4 0 015.7 5.7l-9.2 9.2a2 2 0 01-2.8-2.8l8.5-8.5',
  send: 'M2 21l21-9L2 3v7l15 2-15 2z',
  lock: 'M6 11h12v10H6zM8 11V7a4 4 0 018 0v4',
  check: 'M4 12l5 5L20 6',
  search: 'M11 18a7 7 0 100-14 7 7 0 000 14zM21 21l-4.3-4.3',
  alert: 'M12 8v5M12 16.5v.5M10.3 3.9L1.8 18a2 2 0 001.7 3h17a2 2 0 001.7-3L13.7 3.9a2 2 0 00-3.4 0z',
  smile: 'M12 21a9 9 0 100-18 9 9 0 000 18zM8 14s1.5 2 4 2 4-2 4-2M9 9h.01M15 9h.01',
  clock: 'M12 21a9 9 0 100-18 9 9 0 000 18zM12 7v5l3 2',
};

const Avatar: React.FC<{ text: string; size?: number; color?: string }> = ({ text, size = 40, color = '#6366f1' }) => (
  <div style={{ width: size, height: size, borderRadius: size / 2, background: color, color: '#fff', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 600, fontSize: size * 0.38, flexShrink: 0 }}>
    {text}
  </div>
);

const FileBox: React.FC<{ f: RelayFile; locked?: boolean }> = ({ f, locked }) => (
  <div style={{ width: 40, height: 46, borderRadius: 6, background: locked ? '#9ca3af' : KIND[f.kind], color: '#fff', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 11, fontWeight: 700, flexShrink: 0 }}>
    {locked ? <Icon d={I.lock} size={20} color="#fff" /> : f.kind.toUpperCase()}
  </div>
);

const Ticks: React.FC<{ m: RelayMsg; T: (typeof UI)['en']['relay'] }> = ({ m, T }) => {
  if (m.status === 'sending') return <span style={{ fontSize: 12 }}>{T.sending}</span>;
  if (m.status === 'uploading') return <span style={{ fontSize: 12 }}>{T.uploading(m.progress!)}</span>;
  if (m.status === 'scheduled')
    return (
      <span style={{ display: 'inline-flex', alignItems: 'center', gap: 3, fontSize: 12 }}>
        <Icon d={I.clock} size={13} /> {T.scheduledAt(m.scheduledFor!)}
      </span>
    );
  if (m.status === 'failed') return <span style={{ color: '#fecaca', fontSize: 12 }}>{T.failed}</span>;
  return (
    <span style={{ display: 'inline-flex' }}>
      <Icon d={I.check} size={15} />
      {m.status === 'delivered' && <span style={{ marginLeft: -9 }}><Icon d={I.check} size={15} /></span>}
    </span>
  );
};

export const Relay: React.FC<{ s: RelayState; win: string; lang: Lang }> = ({ s, win, lang }) => {
  const T = UI[lang].relay;
  const E = (id: string, role: string, label?: string) => ({ 'data-el': `${win}/${id}`, 'data-role': role, 'data-label': label });
  const chat = s.chats.find((c) => c.id === s.active)!;
  return (
    <div style={{ display: 'flex', height: '100%', color: C.ink, fontSize: 15, position: 'relative', background: '#fff' }}>
      <div style={{ width: 260, background: C.side, borderRight: `1px solid ${C.line}`, display: 'flex', flexDirection: 'column' }}>
        <div {...E('org', 'header')} style={{ display: 'flex', alignItems: 'center', gap: 10, padding: '16px 16px 12px' }}>
          <div style={{ width: 34, height: 34, borderRadius: 8, background: C.brand, color: '#fff', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 700 }}>{s.org[0]}</div>
          <div>
            <div style={{ fontWeight: 600 }}>{s.org}</div>
            <div style={{ fontSize: 12, color: C.muted }}>{s.me}</div>
          </div>
        </div>
        <div style={{ margin: '0 12px 10px', padding: '8px 10px', borderRadius: 8, background: '#fff', border: `1px solid ${C.line}`, display: 'flex', gap: 8, alignItems: 'center', color: C.muted, fontSize: 14 }}>
          <Icon d={I.search} size={16} /> {T.search}
        </div>
        {s.chats.map((c) => (
          <div key={c.id} {...E(`chat:${c.id}`, 'listitem')} style={{ display: 'flex', gap: 10, padding: '10px 14px', alignItems: 'center', background: c.id === s.active ? C.brandSoft : undefined }}>
            <Avatar text={c.initials} size={38} color={c.external ? '#ea580c' : '#6366f1'} />
            <div style={{ minWidth: 0, flex: 1 }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                <span style={{ fontWeight: 600, fontSize: 14, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>{c.title}</span>
                {c.external && <span style={{ fontSize: 10, color: C.ext, border: `1px solid ${C.ext}`, borderRadius: 4, padding: '0 4px' }}>{T.external}</span>}
              </div>
              <div style={{ fontSize: 13, color: C.muted, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>{c.preview}</div>
            </div>
            {c.unread ? <div style={{ minWidth: 20, height: 20, borderRadius: 10, background: C.brand, color: '#fff', fontSize: 12, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>{c.unread}</div> : null}
          </div>
        ))}
      </div>

      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', minWidth: 0, background: C.bg, position: 'relative' }}>
        <div {...E('chat-header', 'header')} style={{ height: 64, background: '#fff', borderBottom: `1px solid ${C.line}`, display: 'flex', alignItems: 'center', gap: 12, padding: '0 18px' }}>
          <Avatar text={chat.initials} size={38} color={chat.external ? '#ea580c' : '#6366f1'} />
          <div>
            <div style={{ fontWeight: 600 }}>{chat.title}</div>
            <div style={{ fontSize: 13, color: C.muted }}>{chat.external ? T.externalOrg(chat.external) : T.online}</div>
          </div>
        </div>
        {chat.external && (
          <div {...E('external-banner', 'banner')} style={{ background: '#fff7ed', color: C.ext, fontSize: 13, padding: '7px 18px', borderBottom: '1px solid #fed7aa' }}>
            {T.banner(chat.external)}
          </div>
        )}

        <div {...E('messages', 'list')} style={{ flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'flex-end', gap: 10, padding: '16px 18px' }}>
          {thread(s).map((m) => (
            <div key={m.id} style={{ display: 'flex', justifyContent: m.mine ? 'flex-end' : 'flex-start' }}>
              <div {...E(`msg:${m.id}`, m.file ? 'file' : 'message')} style={{ maxWidth: '72%', background: m.mine ? C.brand : '#fff', color: m.mine ? '#fff' : C.ink, borderRadius: 14, padding: m.file ? 10 : '9px 13px', boxShadow: '0 1px 2px rgba(0,0,0,.06)' }}>
                {!m.mine && <div style={{ fontSize: 12, fontWeight: 600, color: '#ea580c', marginBottom: 4 }}>{m.author}</div>}
                {m.text && <div>{m.text}</div>}
                {m.file && (
                  <div style={{ display: 'flex', gap: 10, alignItems: 'center', minWidth: 240, opacity: m.blocked ? 0.85 : 1 }}>
                    <FileBox f={m.file} locked={!!m.blocked} />
                    <div>
                      <div style={{ fontWeight: 600, fontSize: 14 }}>{m.file.name}</div>
                      <div style={{ fontSize: 12, opacity: 0.75 }}>{m.blocked ? T.unavailable : m.file.size}</div>
                      {m.status === 'uploading' && (
                        <div style={{ width: 170, height: 4, borderRadius: 2, background: 'rgba(255,255,255,.3)', marginTop: 6 }}>
                          <div style={{ width: `${m.progress}%`, height: 4, borderRadius: 2, background: '#fff' }} />
                        </div>
                      )}
                    </div>
                  </div>
                )}
                <div style={{ display: 'flex', justifyContent: 'flex-end', alignItems: 'center', gap: 4, fontSize: 11, opacity: 0.7, marginTop: 4 }}>
                  {m.time} {m.mine && <Ticks m={m} T={T} />}
                </div>
              </div>
            </div>
          ))}
        </div>

        {s.picker && (
          <div {...E('picker', 'menu')} style={{ position: 'absolute', left: 14, bottom: 76, width: 300, background: '#fff', borderRadius: 12, boxShadow: '0 10px 30px rgba(0,0,0,.18)', padding: 8, zIndex: 3 }}>
            <div style={{ fontSize: 12, color: C.muted, padding: '4px 8px 6px' }}>{T.recentFiles}</div>
            {s.files.map((f) => (
              <div key={f.id} {...E(`file:${f.id}`, 'menuitem')} style={{ display: 'flex', gap: 10, alignItems: 'center', padding: '6px 8px', borderRadius: 8 }}>
                <div style={{ transform: 'scale(.75)', margin: -5 }}><FileBox f={f} /></div>
                <div>
                  <div style={{ fontSize: 14 }}>{f.name}</div>
                  <div style={{ fontSize: 12, color: C.muted }}>{f.size}</div>
                </div>
              </div>
            ))}
          </div>
        )}

        {s.toast && (
          <div {...E('toast', 'alert')} style={{ position: 'absolute', left: '50%', bottom: 86, transform: 'translateX(-50%)', background: s.toast.tone === 'error' ? C.red : '#111827', color: '#fff', padding: '10px 16px', borderRadius: 10, display: 'flex', gap: 8, alignItems: 'center', fontSize: 14, whiteSpace: 'nowrap', boxShadow: '0 6px 18px rgba(0,0,0,.2)', zIndex: 4 }}>
            <Icon d={I.alert} size={17} /> {s.toast.text}
          </div>
        )}

        <div style={{ background: '#fff', borderTop: `1px solid ${C.line}`, padding: '10px 14px' }}>
          {s.staged && (
            <div {...E('staged', 'attachment')} style={{ display: 'inline-flex', gap: 8, alignItems: 'center', background: C.brandSoft, borderRadius: 8, padding: '5px 10px', marginBottom: 8, fontSize: 13 }}>
              <div style={{ transform: 'scale(.6)', margin: -9 }}><FileBox f={s.staged} /></div>
              {s.staged.name} · {s.staged.size}
            </div>
          )}
          <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
            <div {...E('attach', 'button', T.attach)} style={{ width: 38, height: 38, borderRadius: 19, display: 'flex', alignItems: 'center', justifyContent: 'center', color: C.muted, background: s.picker ? C.brandSoft : undefined }}>
              <Icon d={I.clip} />
            </div>
            <div {...E('composer', 'textbox')} style={{ flex: 1, height: 40, borderRadius: 20, background: C.bg, display: 'flex', alignItems: 'center', padding: '0 16px', color: C.muted, fontSize: 14 }}>
              {T.message}
            </div>
            <div style={{ color: C.muted }}><Icon d={I.smile} /></div>
            <div {...E('schedule', 'button', T.schedule)} style={{ width: 38, height: 38, borderRadius: 19, display: 'flex', alignItems: 'center', justifyContent: 'center', color: s.staged ? C.brand : C.muted }}>
              <Icon d={I.clock} />
            </div>
            <div {...E('send', 'button', T.send)} style={{ width: 40, height: 40, borderRadius: 20, background: s.staged ? C.brand : '#c7d2fe', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <Icon d={I.send} size={18} color="#fff" fill />
            </div>
          </div>
        </div>
      </div>

      {s.dialog && (
        <div style={{ position: 'absolute', inset: 0, background: 'rgba(17,24,39,.35)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 5, pointerEvents: 'none' }}>
          <div {...E('dialog', 'dialog')} style={{ pointerEvents: 'auto', width: 400, background: '#fff', borderRadius: 14, padding: 22, boxShadow: '0 20px 50px rgba(0,0,0,.3)' }}>
            <div style={{ display: 'flex', gap: 10, alignItems: 'center', fontWeight: 600, fontSize: 17 }}>
              <Icon d={I.lock} color={C.red} /> {T.unavailable}
            </div>
            <div style={{ color: '#374151', fontSize: 14, lineHeight: 1.5, margin: '10px 0 18px' }}>{s.dialog.text}</div>
            <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
              <div {...E('dialog-ok', 'button')} style={{ background: C.brand, color: '#fff', borderRadius: 8, padding: '8px 18px', fontWeight: 600, fontSize: 14 }}>{T.ok}</div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
