import type { Scenario } from '../synth/format/scenario.ts';
import type { Lang } from '../synth/i18n.ts';
import { tr } from '../synth/i18n.ts';
import { m1, screenOld } from './m1-meeting-requirements.ts';

export const m2 = (lang: Lang): Scenario => {
  const t = tr(lang);
  const base = m1(lang);
  return {
    ...base,
    id: 'm2-meeting-stale-pdf',
    title: t('The M1 meeting, but the attached pdf is an old version of the deck', 'Встреча из M1, но приложенный pdf - старая версия презентации'),
    voiceFrom: base.id,
    attachments: [
      { deck: 'deck', format: 'pptx' },
      { deck: 'deck', format: 'pdf', overrides: { screen: screenOld(lang) } },
    ],
    traps: [
      ...(base.traps ?? []),
      t(
        'in the attached pdf slide 3 is old: there is no "Status" column, although that is exactly the column shown and discussed in the meeting',
        'в приложенном pdf слайд 3 старый: нет столбца «Статус», хотя на встрече показан и обсуждается именно он',
      ),
    ],
    variants: [{ id: 'clean', height: 1080, fps: 30, crf: 18, audio: 'clean' }],
  };
};
