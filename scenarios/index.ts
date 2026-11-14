import type { Scenario } from '../synth/format/scenario.ts';
import type { Lang } from '../synth/i18n.ts';
import { LANGS } from '../synth/i18n.ts';
import { b1 } from './b1-xtenant-file.ts';
import { b2 } from './b2-xtenant-toast.ts';
import { b3 } from './b3-xtenant-mojibake.ts';
import { b4 } from './b4-upload-stuck.ts';
import { b5 } from './b5-share-revert.ts';
import { b6 } from './b6-wrong-button.ts';
import { b7 } from './b7-hidden-error.ts';
import { w1 } from './w1-web-share-403.ts';
import { w2 } from './w2-web-tabs-duplicate.ts';
import { p1 } from './p1-phone-blocked-file.ts';
import { p2 } from './p2-phone-send-retry.ts';
import { r1 } from './r1-live-no-access.ts';
import { r2 } from './r2-live-resend.ts';
import { r3 } from './r3-live-share-fumble.ts';
import { r4 } from './r4-live-name-not-found.ts';
import { r5 } from './r5-live-wrong-chat.ts';
import { r6 } from './r6-phone-wrong-hypothesis.ts';
import { m1 } from './m1-meeting-requirements.ts';
import { m2 } from './m2-meeting-stale-pdf.ts';
import { m3 } from './m3-meeting-long-room.ts';
import { m4 } from './m4-meeting-editor-share.ts';

const FACTORIES: ((lang: Lang) => Scenario)[] = [b1, b2, b3, b4, b5, b6, b7, w1, w2, p1, p2, r1, r2, r3, r4, r5, r6, m1, m2, m3, m4];

// every scenario in every language; a scenario is addressed by key = <lang>/<id>, which is also its path under out/
export const SCENARIOS: Scenario[] = LANGS.flatMap((lang) => FACTORIES.map((f) => f(lang)));
export const keyOf = (sc: Scenario) => `${sc.lang}/${sc.id}`;
export const byKey = (key: string) => {
  const sc = SCENARIOS.find((s) => keyOf(s) === key);
  if (!sc) throw new Error(`unknown scenario ${key}; known: ${SCENARIOS.map(keyOf).join(', ')}`);
  return sc;
};
// Remotion composition ids cannot contain '/'
export const compId = (key: string) => key.replace('/', '-');
