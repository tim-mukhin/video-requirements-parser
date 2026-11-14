import React from 'react';
import type { Scenario, Win } from '../format/scenario.ts';
import { Relay } from './relay/Relay.tsx';
import { RelayMobile } from './relay/RelayMobile.tsx';
import { Vault } from './vault/Vault.tsx';
import { Meet } from './meet/Meet.tsx';
import { Slides, SlideShow } from './slides/Slides.tsx';
import type { RelayState } from './relay/model.ts';
import type { VaultState } from './vault/model.ts';
import type { MeetState } from './meet/model.ts';
import type { SlidesState } from './slides/model.ts';

export const AppView: React.FC<{ w: Win; s: unknown; sc: Scenario; t: number; speaking: string[]; box: [number, number] }> = ({ w, s, sc, t, speaking, box }) => {
  if (w.app === 'relay') return sc.device === 'phone' ? <RelayMobile s={s as RelayState} win={w.id} box={box} lang={sc.lang} /> : <Relay s={s as RelayState} win={w.id} lang={sc.lang} />;
  if (w.app === 'vault') return <Vault s={s as VaultState} win={w.id} lang={sc.lang} />;
  const deckOf = (id: string) => sc.decks!.find((d) => d.id === id)!;
  if (w.app === 'slides') {
    const st = s as SlidesState;
    return st.mode === 'show' ? <SlideShow s={st} win={w.id} deck={deckOf(st.deck)} box={box} /> : <Slides s={st} win={w.id} deck={deckOf(st.deck)} box={box} lang={sc.lang} />;
  }
  const m = s as MeetState;
  return <Meet s={m} win={w.id} t={t} deck={deckOf(m.deck)} speaking={speaking} box={box} lang={sc.lang} />;
};
