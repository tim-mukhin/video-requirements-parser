export type MeetPerson = { id: string; name: string; initials: string; color: string; muted?: boolean };
export type MeetState = {
  title: string;
  org: string;
  deck: string;
  slide: number;
  presenter: string;
  people: MeetPerson[];
  // meeting clock seconds at video t=0
  elapsed: number;
};

export type MeetOp = { slide: number } | { mute: { id: string; muted: boolean } };

export function meetKey(s: MeetState, key: string, slides: number): MeetState {
  if (key === 'next') return { ...s, slide: Math.min(slides - 1, s.slide + 1) };
  if (key === 'prev') return { ...s, slide: Math.max(0, s.slide - 1) };
  return s;
}

export function meetOp(s: MeetState, op: MeetOp): MeetState {
  if ('slide' in op) return { ...s, slide: op.slide };
  if ('mute' in op) return { ...s, people: s.people.map((p) => (p.id === op.mute.id ? { ...p, muted: op.mute.muted } : p)) };
  return s;
}

export const meetWho = (s: MeetState) => ({ org: s.org, user: s.presenter });
