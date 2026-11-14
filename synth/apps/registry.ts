import type { AppKind, Scenario } from '../format/scenario.ts';
import { relayClick, relayExpire, relayOp, relayWho } from './relay/model.ts';
import { vaultClick, vaultExpire, vaultOp, vaultType, vaultWho } from './vault/model.ts';
import { meetKey, meetOp, meetWho } from './meet/model.ts';
import type { MeetState } from './meet/model.ts';
import { slidesClick, slidesKey, slidesWho } from './slides/model.ts';
import type { SlidesState } from './slides/model.ts';

/* eslint-disable @typescript-eslint/no-explicit-any */
type App = {
  click: (s: any, el: string) => any;
  op: (s: any, op: any) => any;
  expire: (op: any) => object | null;
  key: (s: any, key: string, sc: Scenario) => any;
  type: (s: any, el: string, text: string) => any;
  who: (s: any) => { org?: string; user?: string };
  name: string;
};

const same = (s: unknown) => s;

export const APPS: Record<AppKind, App> = {
  relay: { name: 'Relay', click: relayClick, op: relayOp, expire: relayExpire, key: same, type: same, who: relayWho },
  vault: { name: 'Vault', click: vaultClick, op: vaultOp, expire: vaultExpire, key: same, type: vaultType, who: vaultWho },
  meet: {
    name: 'Relay Meet',
    click: same,
    op: meetOp,
    expire: () => null,
    key: (s: MeetState, k, sc) => meetKey(s, k, sc.decks!.find((d) => d.id === s.deck)!.slides.length),
    type: same,
    who: meetWho,
  },
  slides: {
    name: 'Deck',
    click: slidesClick,
    op: same,
    expire: () => null,
    key: (s: SlidesState, k, sc) => slidesKey(s, k, sc.decks!.find((d) => d.id === s.deck)!.slides.length),
    type: same,
    who: slidesWho,
  },
};
