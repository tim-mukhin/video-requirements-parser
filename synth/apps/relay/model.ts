export type RelayFile = { id: string; name: string; size: string; kind: 'pdf' | 'xlsx' | 'docx' | 'png' };
export type RelayStatus = 'sending' | 'uploading' | 'sent' | 'delivered' | 'failed' | 'scheduled';
export type RelayMsg = {
  id: string;
  mine: boolean;
  author: string;
  time: string;
  text?: string;
  file?: RelayFile;
  status?: RelayStatus;
  progress?: number;
  scheduledFor?: string;
  blocked?: string;
};
export type RelayChat = { id: string; title: string; preview: string; initials: string; external?: string; unread?: number };
export type RelayState = {
  org: string;
  me: string;
  chats: RelayChat[];
  active: string;
  // chat that receives scenario incoming messages by default
  home: string;
  threads: Record<string, RelayMsg[]>;
  files: RelayFile[];
  picker: boolean;
  staged?: RelayFile;
  toast?: { text: string; tone: 'error' | 'info' };
  dialog?: { text: string };
  clock: string;
};

export type RelayOp =
  | { status: { msg: string; to: RelayStatus } }
  | { progress: { msg: string; value: number } }
  | { incoming: RelayMsg; chat?: string }
  | { chat: { id: string; preview: string; unread: number } }
  | { toast: RelayState['toast'] | null }
  | { dialog: RelayState['dialog'] | null };

export const thread = (s: RelayState) => s.threads[s.active] ?? [];
const all = (s: RelayState) => Object.values(s.threads).flat();
const nextId = (s: RelayState) => `s${all(s).filter((m) => m.id.startsWith('s')).length + 1}`;
const patchAll = (s: RelayState, id: string, p: Partial<RelayMsg>): RelayState => ({
  ...s,
  threads: Object.fromEntries(Object.entries(s.threads).map(([k, v]) => [k, v.map((m) => (m.id === id ? { ...m, ...p } : m))])),
});
const append = (s: RelayState, chat: string, m: RelayMsg): RelayState => ({ ...s, threads: { ...s.threads, [chat]: [...(s.threads[chat] ?? []), m] } });

export function relayClick(s: RelayState, el: string): RelayState {
  if (el === 'attach') return { ...s, picker: !s.picker };
  if (el.startsWith('file:')) {
    const f = s.files.find((x) => x.id === el.slice(5));
    return { ...s, picker: false, staged: f };
  }
  if ((el === 'send' || el === 'schedule') && s.staged) {
    const msg: RelayMsg =
      el === 'send'
        ? { id: nextId(s), mine: true, author: s.me, time: s.clock, file: s.staged, status: 'sending' }
        : { id: nextId(s), mine: true, author: s.me, time: s.clock, file: s.staged, status: 'scheduled', scheduledFor: '18:00' };
    return { ...append(s, s.active, msg), staged: undefined };
  }
  if (el.startsWith('msg:')) {
    const m = thread(s).find((x) => x.id === el.slice(4));
    if (m?.blocked) return { ...s, dialog: { text: m.blocked } };
    return s;
  }
  if (el === 'dialog-ok') return { ...s, dialog: undefined };
  if (el.startsWith('retry:')) return patchAll(s, el.slice(6), { status: 'sending' });
  if (el.startsWith('chat:')) {
    const id = el.slice(5);
    return { ...s, active: id, chats: s.chats.map((c) => (c.id === id ? { ...c, unread: 0 } : c)) };
  }
  return s;
}

export function relayOp(s: RelayState, op: RelayOp): RelayState {
  if ('status' in op) return patchAll(s, op.status.msg, { status: op.status.to });
  if ('progress' in op) return patchAll(s, op.progress.msg, { status: 'uploading', progress: op.progress.value });
  if ('incoming' in op) {
    const chat = op.chat ?? s.home;
    const m = op.incoming;
    const next = append(s, chat, m);
    const preview = m.text ?? m.file?.name ?? '';
    return { ...next, chats: next.chats.map((c) => (c.id === chat ? { ...c, preview, unread: chat === s.active ? c.unread : (c.unread ?? 0) + 1 } : c)) };
  }
  if ('chat' in op) {
    const c = op.chat;
    const chat = { ...s.chats.find((x) => x.id === c.id)!, preview: c.preview, unread: c.unread };
    return { ...s, chats: [chat, ...s.chats.filter((x) => x.id !== c.id)] };
  }
  if ('toast' in op) return { ...s, toast: op.toast ?? undefined };
  if ('dialog' in op) return { ...s, dialog: op.dialog ?? undefined };
  return s;
}

export function relayExpire(op: RelayOp): RelayOp | null {
  if ('toast' in op) return { toast: null };
  if ('dialog' in op) return { dialog: null };
  return null;
}

export const relayWho = (s: RelayState) => ({ org: s.org, user: s.me });
