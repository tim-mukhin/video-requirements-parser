import type { Scenario } from '../synth/format/scenario.ts';
import type { Lang } from '../synth/i18n.ts';
import { tr } from '../synth/i18n.ts';
import { people, vaultContoso, voice, WALLPAPER } from './common.ts';

export const b5 = (lang: Lang): Scenario => {
  const t = tr(lang);
  const p = people(lang);
  return {
    id: 'b5-share-revert',
    lang,
    kind: 'bug-repro',
    title: t('"Anyone with the link" access reverts after saving', 'Доступ «Все, у кого есть ссылка» после сохранения откатывается'),
    screen: { w: 1920, h: 1080 },
    wallpaper: WALLPAPER,
    cast: [{ id: 'artem', name: p.artemShort, voice: voice(lang, 'artem') }],
    windows: [
      { id: 'v', app: 'vault', title: t('Vault - My Drive', 'Vault - Мой диск'), bbox: [60, 48, 1800, 1010], state: vaultContoso(lang) },
    ],
    steps: [
      {
        say: t(
          'Let me show a bug with link sharing. I want to open the report to anyone who has the link.',
          'Покажу баг с доступом по ссылке. Хочу открыть отчёт для всех, у кого есть ссылка.',
        ),
      },
      { act: { click: 'v/row:q3' } },
      { say: t('I selected the file, now I click [Share](click:v/share).', 'Выбрал файл, нажимаю [Поделиться](click:v/share).') },
      {
        say: t(
          "Right now it's set to [restricted](ref:v/mode). I change it [right here](click:v/mode).",
          'Сейчас стоит [только для приглашённых](ref:v/mode). Меняю [вот здесь](click:v/mode).',
        ),
      },
      { act: { click: 'v/mode:anyone' }, name: 'pick' },
      { say: t("Anyone with the link. [Saving](click:v/save#save) it.", 'Все, у кого есть ссылка. [Сохраняю](click:v/save#save).') },
      { sys: 'v', op: { toast: { text: t('Sharing settings saved', 'Настройки доступа сохранены'), tone: 'info' } }, at: 'save', delay: 0.4, ms: 2500, name: 'saved' },
      { sys: 'v', op: { link: { file: 'q3', mode: 'restricted' } }, at: 'save', delay: 1.4, name: 'revert' },
      { wait: 1.5 },
      {
        say: t("It says it's saved. I open it [again](click:v/share#reopen) to check.", 'Написано, что сохранено. Открываю [ещё раз](click:v/share#reopen) проверить.'),
      },
      {
        say: t("And it's [restricted](ref:v/mode) again. The setting didn't stick.", 'И снова [только приглашённые](ref:v/mode). Настройка не сохранилась.'),
        name: 'seen',
      },
      { say: t('I expect link access to stay after saving.', 'Ожидаю, что после сохранения останется доступ по ссылке.'), name: 'expect' },
      { act: { click: 'v/cancel' } },
    ],
    bug: {
      class: 'state-revert',
      title: t(
        'The "Anyone with the link" access mode is not saved, even though "saved" is shown',
        'Режим доступа «Все, у кого есть ссылка» не сохраняется, хотя показано «сохранено»',
      ),
      expected: {
        text: t('After "Save", the file keeps "Anyone with the link" access.', 'После «Сохранить» у файла остаётся доступ «Все, у кого есть ссылка».'),
        source: 'speech',
      },
      actual: t(
        'After "Save", a "Sharing settings saved" toast appears, the file in the list shows "link" for a second, then "private"; when the dialog is reopened the mode is "Restricted".',
        'После «Сохранить» тост «Настройки доступа сохранены», в списке у файла на секунду «по ссылке», затем «личный»; при повторном открытии диалога режим «Только приглашённые».',
      ),
      critical: ['pick', 'save', 'saved', 'revert', 'reopen'],
      traps: [
        t(
          'the access badge in the file list shows "link" for about a second and silently reverts: a change with no words',
          'значок доступа в списке файлов показывает «по ссылке» около секунды и молча возвращается: изменение без слов',
        ),
      ],
    },
    difficulty: { speech: 'deictic', signal: { kind: 'none' }, windows: 1, occluded: false, distractors: [], attempts: 'once' },
    variants: [
      { id: 'clean', height: 1080, fps: 30, crf: 18, audio: 'clean' },
      { id: 'low', height: 720, fps: 15, crf: 32, audio: 'noise' },
    ],
  };
};
