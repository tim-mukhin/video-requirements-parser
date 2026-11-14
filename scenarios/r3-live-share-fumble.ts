import type { Scenario } from '../synth/format/scenario.ts';
import type { Lang } from '../synth/i18n.ts';
import { tr } from '../synth/i18n.ts';
import { people, vaultContoso, voice, WALLPAPER } from './common.ts';

export const r3 = (lang: Lang): Scenario => {
  const t = tr(lang);
  const p = people(lang);
  return {
    id: 'r3-live-share-fumble',
    lang,
    kind: 'bug-repro',
    title: t('Live speech: fumbles with files and menus, the access setting reverts', 'Живая речь: путается в файлах и меню, настройка доступа откатывается'),
    screen: { w: 1920, h: 1080 },
    wallpaper: WALLPAPER,
    cast: [{ id: 'artem', name: p.artemShort, voice: voice(lang, 'artem') }],
    windows: [{ id: 'v', app: 'vault', title: t('Vault - My Drive', 'Vault - Мой диск'), bbox: [60, 48, 1800, 1010], state: vaultContoso(lang) }],
    steps: [
      { say: t('Okay, I need this file to open by link.', 'Так, мне надо, чтобы этот файл открывался по ссылке.') },
      { act: { click: 'v/row:budget' }, name: 'wrong-row' },
      { say: t('No, not this one.', 'Не, не этот.') },
      { act: { click: 'v/row:q3' } },
      { act: { click: 'v/share' } },
      { act: { point: 'v/mode', ms: 900 } },
      { say: t("Here... I'm setting [this thing](click:v/mode).", 'Вот тут... [вот это](click:v/mode) ставлю.') },
      { act: { point: 'v/mode:org', ms: 700 } },
      { act: { click: 'v/mode:anyone' }, name: 'pick' },
      { say: t('Well, by link. [Save](click:v/save#save).', 'Ну, по ссылке. [Сохранить](click:v/save#save).') },
      { sys: 'v', op: { toast: { text: t('Access settings saved', 'Настройки доступа сохранены'), tone: 'info' } }, at: 'save', delay: 0.4, ms: 2500, name: 'saved' },
      { sys: 'v', op: { link: { file: 'q3', mode: 'restricted' } }, at: 'save', delay: 1.3, name: 'revert' },
      { wait: 2 },
      { say: t('Okay. Checking.', 'Так. Проверяю.') },
      { act: { click: 'v/share' }, name: 'reopen' },
      { say: t("There you go. It's [this thing](ref:v/mode) again.", 'Ну вот. Опять [вот это](ref:v/mode) стоит.'), name: 'seen' },
      { say: t("But I changed it. So that's the bug.", 'Я же поменял. Вот такая бага.') },
    ],
    bug: {
      class: 'state-revert',
      title: t('The "Anyone with the link" mode is not saved', 'Режим «Все, у кого есть ссылка» не сохраняется'),
      expected: { text: t('After saving, the file keeps link access.', 'После сохранения у файла остаётся доступ по ссылке.'), source: 'speech' },
      actual: t(
        'For "Q3_Report_Zürich.pdf" the "Anyone with the link" mode is selected, then "Save", toast "Access settings saved"; a second later the icon in the list goes back to "private", and on reopening the mode is "Restricted".',
        'Для «Отчёт_Q3.pdf» выбран режим «Все, у кого есть ссылка», «Сохранить», тост «Настройки доступа сохранены»; через секунду значок в списке возвращается на «личный», при повторном открытии режим «Только приглашённые».',
      ),
      critical: ['pick', 'save', 'revert', 'reopen'],
      traps: [
        t('The wrong file (Budget_2027.xlsx) is selected first, this is not part of the repro', 'сначала выбран не тот файл (Бюджет_2027.xlsx), это не часть репро'),
        t('Hovering over "Anyone at Contoso" without a click is not a selection', 'наведение на «Все в Contoso» без клика - не выбор'),
        t('"This thing" at the end is the "Restricted" mode, it is not named aloud', '«вот это» в конце - режим «Только приглашённые», вслух не назван'),
      ],
    },
    difficulty: { speech: 'vague', signal: { kind: 'none' }, windows: 1, occluded: false, distractors: ['cursor-wander'], attempts: 'wrong-path-first' },
    variants: [{ id: 'clean', height: 1080, fps: 30, crf: 18, audio: 'clean' }],
  };
};
