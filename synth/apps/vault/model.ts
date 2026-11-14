export type LinkMode = 'restricted' | 'org' | 'anyone';
export type VaultFile = { id: string; name: string; kind: 'pdf' | 'xlsx' | 'docx' | 'png' | 'folder'; owner: string; modified: string; size: string };
// role: owner | editor | viewer, the label comes from the UI dictionary
export type VaultPerson = { name: string; email: string; role: string };
export type VaultState = {
  org: string;
  me: string;
  path: string[];
  files: VaultFile[];
  selected?: string;
  links: Record<string, LinkMode>;
  people: Record<string, VaultPerson[]>;
  share?: { file: string; mode: LinkMode; menu: boolean; invite: string };
  toast?: { text: string; tone: 'error' | 'info' };
  clock: string;
};

export type VaultOp =
  | { link: { file: string; mode: LinkMode } }
  | { toast: VaultState['toast'] | null }
  | { share: null };


export function vaultClick(s: VaultState, el: string): VaultState {
  if (el.startsWith('row:')) return { ...s, selected: el.slice(4) };
  if (el === 'share' && s.selected) {
    return { ...s, share: { file: s.selected, mode: s.links[s.selected] ?? 'restricted', menu: false, invite: '' } };
  }
  if (!s.share) return s;
  if (el === 'mode') return { ...s, share: { ...s.share, menu: !s.share.menu } };
  if (el.startsWith('mode:')) return { ...s, share: { ...s.share, mode: el.slice(5) as LinkMode, menu: false } };
  if (el === 'save') {
    const f = s.share.file;
    const invited = s.share.invite ? [...(s.people[f] ?? []), { name: s.share.invite, email: s.share.invite, role: 'viewer' }] : s.people[f];
    return { ...s, links: { ...s.links, [f]: s.share.mode }, people: { ...s.people, [f]: invited ?? [] }, share: undefined };
  }
  if (el === 'cancel') return { ...s, share: undefined };
  return s;
}

export function vaultType(s: VaultState, el: string, text: string): VaultState {
  if (el === 'invite' && s.share) return { ...s, share: { ...s.share, invite: text } };
  return s;
}

export function vaultOp(s: VaultState, op: VaultOp): VaultState {
  if ('link' in op) return { ...s, links: { ...s.links, [op.link.file]: op.link.mode } };
  if ('toast' in op) return { ...s, toast: op.toast ?? undefined };
  if ('share' in op) return { ...s, share: undefined };
  return s;
}

export function vaultExpire(op: VaultOp): VaultOp | null {
  if ('toast' in op) return { toast: null };
  return null;
}

export const vaultWho = (s: VaultState) => ({ org: s.org, user: s.me });
