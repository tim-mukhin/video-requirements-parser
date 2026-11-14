import type { Scenario, Step } from '../synth/format/scenario.ts';
import type { Lang } from '../synth/i18n.ts';
import { tr } from '../synth/i18n.ts';
import { deck, m1 } from './m1-meeting-requirements.ts';
import { people, WALLPAPER } from './common.ts';

// the same meeting as M1, but the whole screen with the editor is shared: slides change by clicking thumbnails
export const m4 = (lang: Lang): Scenario => {
  const t = tr(lang);
  const p = people(lang);
  const base = m1(lang);
  const d = deck(lang);

  let slide = 0;
  const steps: Step[] = base.steps.map((st) => {
    if ('act' in st && 'key' in st.act) {
      slide += st.act.key === 'next' ? 1 : -1;
      return { act: { click: `d/thumb:${slide}` } };
    }
    if ('say' in st) return { ...st, say: st.say.replaceAll('m/slide/', 'd/slide/') };
    return st;
  });

  const notes: Record<string, string> = {
    screen: t(
      'The retention decision has already been made: 1 year. Do not mention it until it is agreed with Security.',
      'Решение по хранению уже принято: 1 год. Не озвучивать до согласования с безопасностью.',
    ),
    filters: t('The time period filter defaults to the last 30 days.', 'Фильтр по периоду - по умолчанию последние 30 дней.'),
  };

  return {
    ...base,
    id: 'm4-meeting-editor-share',
    title: t('The M1 meeting, sharing the whole screen with the presentation editor', 'Встреча M1, показ всего экрана с редактором презентаций'),
    voiceFrom: base.id,
    wallpaper: WALLPAPER,
    recording: {
      layout: 'gallery-right',
      title: t('Requirements review: external access log', 'Ревью требований: журнал внешнего доступа'),
      elapsed: 754,
      frame: { w: 1920, h: 1080 },
      tiles: [
        { id: 'artem', name: p.artem, kind: 'person', color: '#4f46e5' },
        { id: 'denis', name: p.denis, kind: 'person', color: '#0f766e' },
        { id: 'irina', name: p.irina, kind: 'person', color: '#b45309', muted: true },
        { id: 'lena', name: p.lena, kind: 'person', color: '#be185d', muted: true },
      ],
    },
    decks: [{ ...d, slides: d.slides.map((s) => (notes[s.id] ? { ...s, notes: notes[s.id] } : s)) }],
    windows: [{ id: 'd', app: 'slides', title: `${d.file} - Deck`, bbox: [0, 30, 1920, 1050], state: { deck: 'deck', slide: 0, mode: 'editor' } }],
    steps,
    traps: [
      ...(base.traps ?? []),
      t(
        'the notes for slide 3 are visible on screen: "The retention decision has already been made: 1 year", but in the meeting retention stays an open question',
        'заметки к слайду 3 видны на экране: «решение по хранению уже принято: 1 год», но на встрече хранение остаётся открытым вопросом',
      ),
      t(
        'the thumbnails on the left show all slides at once: that does not mean they were shown',
        'миниатюры слева показывают все слайды сразу: это не значит, что их показывали',
      ),
    ],
  };
};
