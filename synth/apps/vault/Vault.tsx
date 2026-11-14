import React from 'react';
import type { LinkMode, VaultFile, VaultState } from './model.ts';
import { UI } from '../../i18n.ts';
import type { Lang } from '../../i18n.ts';

const C = { brand: '#0f766e', soft: '#ecfdf5', ink: '#0f172a', muted: '#64748b', line: '#e2e8f0', side: '#f8fafc' };
const KIND: Record<VaultFile['kind'], string> = { pdf: '#dc2626', xlsx: '#16a34a', docx: '#2563eb', png: '#9333ea', folder: '#f59e0b' };
const P = (d: string, size = 18, color = 'currentColor') => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={2} strokeLinecap="round" strokeLinejoin="round"><path d={d} /></svg>
);
const I = {
  share: 'M16 8a3 3 0 100-6 3 3 0 000 6zM6 15a3 3 0 100-6 3 3 0 000 6zM16 22a3 3 0 100-6 3 3 0 000 6zM8.6 13.5l4.8 2.8M13.4 6.7L8.6 9.5',
  upload: 'M12 16V4M7 9l5-5 5 5M4 20h16',
  folder: 'M3 7a2 2 0 012-2h4l2 2h8a2 2 0 012 2v8a2 2 0 01-2 2H5a2 2 0 01-2-2z',
  globe: 'M12 21a9 9 0 100-18 9 9 0 000 18zM3 12h18M12 3a14 14 0 010 18M12 3a14 14 0 000 18',
  lock: 'M6 11h12v10H6zM8 11V7a4 4 0 018 0v4',
  building: 'M4 21V5l8-3v19M12 9h8v12M7 8h2M7 12h2M7 16h2M15 13h2M15 17h2',
  chev: 'M6 9l6 6 6-6',
  check: 'M4 12l5 5L20 6',
  search: 'M11 18a7 7 0 100-14 7 7 0 000 14zM21 21l-4.3-4.3',
};
const MODE_ICON: Record<LinkMode, string> = { restricted: I.lock, org: I.building, anyone: I.globe };

export const Vault: React.FC<{ s: VaultState; win: string; lang: Lang }> = ({ s, win, lang }) => {
  const T = UI[lang].vault;
  const linkLabel = (m: LinkMode) => (m === 'restricted' ? T.restricted : m === 'org' ? T.orgMode(s.org) : T.anyone);
  const E = (id: string, role: string, label?: string) => ({ 'data-el': `${win}/${id}`, 'data-role': role, 'data-label': label });
  const sel = s.files.find((f) => f.id === s.selected);
  const shareFile = s.share && s.files.find((f) => f.id === s.share!.file)!;
  const modes: LinkMode[] = ['restricted', 'org', 'anyone'];
  return (
    <div style={{ display: 'flex', height: '100%', color: C.ink, fontSize: 15, position: 'relative', background: '#fff' }}>
      <div style={{ width: 230, background: C.side, borderRight: `1px solid ${C.line}`, padding: '18px 12px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 10, fontWeight: 700, fontSize: 19, padding: '0 8px 18px' }}>
          <div style={{ width: 30, height: 30, borderRadius: 8, background: C.brand, color: '#fff', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 16 }}>V</div>
          Vault
        </div>
        {T.nav.map((n, i) => (
          <div key={n} style={{ padding: '9px 12px', borderRadius: 8, background: i === 0 ? C.soft : undefined, color: i === 0 ? C.brand : C.ink, fontWeight: i === 0 ? 600 : 400, fontSize: 14 }}>{n}</div>
        ))}
        <div style={{ position: 'absolute', bottom: 22, left: 20, width: 190, fontSize: 12, color: C.muted }}>
          <div style={{ height: 6, borderRadius: 3, background: C.line, marginBottom: 6 }}><div style={{ width: '38%', height: 6, borderRadius: 3, background: C.brand }} /></div>
          {T.storage}
        </div>
      </div>
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', minWidth: 0 }}>
        <div style={{ height: 60, display: 'flex', alignItems: 'center', padding: '0 22px', borderBottom: `1px solid ${C.line}` }}>
          <div style={{ flex: 1, maxWidth: 520, height: 38, borderRadius: 19, background: '#f1f5f9', display: 'flex', alignItems: 'center', gap: 8, padding: '0 14px', color: C.muted, fontSize: 14 }}>{P(I.search, 16)} {T.search}</div>
          <div style={{ marginLeft: 'auto', fontSize: 13, color: C.muted }}>{s.me} · {s.org}</div>
        </div>
        <div {...E('path', 'breadcrumb')} style={{ padding: '16px 22px 8px', fontSize: 20, fontWeight: 600 }}>{s.path.join('  ›  ')}</div>
        <div style={{ display: 'flex', gap: 10, padding: '6px 22px 14px' }}>
          <div {...E('upload', 'button')} style={{ display: 'flex', gap: 6, alignItems: 'center', padding: '8px 14px', borderRadius: 8, border: `1px solid ${C.line}`, fontSize: 14 }}>{P(I.upload, 16)} {T.upload}</div>
          <div {...E('share', 'button')} style={{ display: 'flex', gap: 6, alignItems: 'center', padding: '8px 14px', borderRadius: 8, fontSize: 14, background: sel ? C.brand : '#e2e8f0', color: sel ? '#fff' : C.muted }}>{P(I.share, 16)} {T.share}</div>
        </div>
        <div style={{ display: 'flex', padding: '10px 22px', fontSize: 13, color: C.muted, borderBottom: `1px solid ${C.line}` }}>
          <span style={{ flex: 3 }}>{T.cols[0]}</span><span style={{ flex: 1.4 }}>{T.cols[1]}</span><span style={{ flex: 1.4 }}>{T.cols[2]}</span><span style={{ flex: 0.8 }}>{T.cols[3]}</span><span style={{ width: 120 }}>{T.cols[4]}</span>
        </div>
        {s.files.map((f) => {
          const mode = s.links[f.id] ?? 'restricted';
          return (
            <div key={f.id} {...E(`row:${f.id}`, 'row')} style={{ display: 'flex', alignItems: 'center', padding: '11px 22px', fontSize: 14, borderBottom: `1px solid ${C.line}`, background: f.id === s.selected ? '#ccfbf1' : undefined }}>
              <span style={{ flex: 3, display: 'flex', alignItems: 'center', gap: 10 }}>
                {f.kind === 'folder' ? P(I.folder, 20, KIND.folder) : <span style={{ width: 22, height: 26, borderRadius: 4, background: KIND[f.kind], color: '#fff', fontSize: 8, fontWeight: 700, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>{f.kind.toUpperCase()}</span>}
                {f.name}
              </span>
              <span style={{ flex: 1.4, color: C.muted }}>{f.owner}</span>
              <span style={{ flex: 1.4, color: C.muted }}>{f.modified}</span>
              <span style={{ flex: 0.8, color: C.muted }}>{f.size}</span>
              <span {...E(`access:${f.id}`, 'status')} style={{ width: 120, display: 'flex', alignItems: 'center', gap: 5, color: mode === 'anyone' ? C.brand : C.muted, fontSize: 13 }}>
                {f.kind !== 'folder' && <>{P(MODE_ICON[mode], 14)} {mode === 'anyone' ? T.accessLink : mode === 'org' ? s.org : T.accessPrivate}</>}
              </span>
            </div>
          );
        })}
      </div>

      {s.toast && (
        <div {...E('toast', 'alert')} style={{ position: 'absolute', left: 24, bottom: 24, background: '#0f172a', color: '#fff', padding: '12px 18px', borderRadius: 10, fontSize: 14, display: 'flex', gap: 8, alignItems: 'center', zIndex: 6 }}>
          {P(I.check, 16)} {s.toast.text}
        </div>
      )}

      {s.share && shareFile && (
        <div style={{ position: 'absolute', inset: 0, background: 'rgba(15,23,42,.4)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 5, pointerEvents: 'none' }}>
          <div {...E('share-dialog', 'dialog')} style={{ pointerEvents: 'auto', width: 560, background: '#fff', borderRadius: 16, padding: 26, boxShadow: '0 24px 60px rgba(0,0,0,.35)', position: 'relative' }}>
            <div style={{ fontSize: 21, fontWeight: 600, marginBottom: 16 }}>{T.dialogTitle(shareFile.name)}</div>
            <div {...E('invite', 'textbox', T.invite)} style={{ height: 46, borderRadius: 10, border: `2px solid ${s.share.invite ? C.brand : C.line}`, display: 'flex', alignItems: 'center', padding: '0 14px', fontSize: 15, color: s.share.invite ? C.ink : C.muted }}>
              {s.share.invite || T.invite}
            </div>
            <div style={{ fontSize: 15, fontWeight: 600, margin: '20px 0 10px' }}>{T.people}</div>
            {(s.people[shareFile.id] ?? []).map((p) => (
              <div key={p.email} style={{ display: 'flex', alignItems: 'center', gap: 12, padding: '6px 0' }}>
                <div style={{ width: 34, height: 34, borderRadius: 17, background: '#6366f1', color: '#fff', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 13, fontWeight: 600 }}>{p.name.split(' ').map((x) => x[0]).join('')}</div>
                <div style={{ flex: 1 }}>
                  <div style={{ fontSize: 14 }}>{p.name}</div>
                  <div style={{ fontSize: 12, color: C.muted }}>{p.email}</div>
                </div>
                <div style={{ fontSize: 13, color: C.muted }}>{T.roles[p.role] ?? p.role}</div>
              </div>
            ))}
            <div style={{ fontSize: 15, fontWeight: 600, margin: '18px 0 10px' }}>{T.general}</div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
              <div style={{ width: 38, height: 38, borderRadius: 19, background: '#f1f5f9', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>{P(MODE_ICON[s.share.mode], 18)}</div>
              <div {...E('mode', 'combobox')} style={{ display: 'inline-flex', alignItems: 'center', gap: 6, padding: '6px 10px', borderRadius: 8, background: s.share.menu ? '#f1f5f9' : undefined, fontWeight: 600, fontSize: 15 }}>
                {linkLabel(s.share.mode)} {P(I.chev, 16)}
              </div>
            </div>
            {s.share.menu && (
              <div {...E('mode-menu', 'listbox')} style={{ position: 'absolute', left: 76, top: 330, width: 320, background: '#fff', borderRadius: 12, boxShadow: '0 12px 30px rgba(0,0,0,.2)', padding: 6, zIndex: 2 }}>
                {modes.map((m) => (
                  <div key={m} {...E(`mode:${m}`, 'option')} style={{ display: 'flex', alignItems: 'center', gap: 10, padding: '10px 12px', borderRadius: 8, fontSize: 15, background: m === s.share!.mode ? C.soft : undefined }}>
                    {P(MODE_ICON[m], 16)} {linkLabel(m)}
                  </div>
                ))}
              </div>
            )}
            <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 26 }}>
              <div {...E('copy-link', 'button')} style={{ padding: '9px 16px', borderRadius: 20, border: `1px solid ${C.brand}`, color: C.brand, fontSize: 14, fontWeight: 600 }}>{T.copy}</div>
              <div style={{ display: 'flex', gap: 10 }}>
                <div {...E('cancel', 'button')} style={{ padding: '9px 16px', borderRadius: 20, fontSize: 14, color: C.muted }}>{T.cancel}</div>
                <div {...E('save', 'button')} style={{ padding: '9px 20px', borderRadius: 20, background: C.brand, color: '#fff', fontSize: 14, fontWeight: 600 }}>{T.save}</div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
