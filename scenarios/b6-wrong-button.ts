import type { Scenario } from '../synth/format/scenario.ts';
import type { Lang } from '../synth/i18n.ts';
import { tr } from '../synth/i18n.ts';
import { contoso, fabrikam, people, voice, WALLPAPER } from './common.ts';

export const b6 = (lang: Lang): Scenario => {
  const t = tr(lang);
  const p = people(lang);
  return {
    id: 'b6-wrong-button',
    lang,
    kind: 'bug-repro',
    title: t(
      'Complaint "the file won\'t send", but the video shows "Schedule send" being clicked',
      'Жалоба «файл не уходит», а на видео нажата «Запланировать отправку»',
    ),
    screen: { w: 1920, h: 1080 },
    wallpaper: WALLPAPER,
    cast: [{ id: 'artem', name: p.artemShort, voice: voice(lang, 'artem') }],
    windows: [
      { id: 'b', app: 'relay', title: 'Relay - Fabrikam', bbox: [966, 44, 934, 1016], state: fabrikam(lang) },
      { id: 'a', app: 'relay', title: 'Relay - Contoso', bbox: [20, 44, 934, 1016], state: contoso(lang) },
    ],
    steps: [
      { say: t("Files aren't going out again. I'm attaching the report.", 'Файлы опять не уходят. Прикрепляю отчёт.') },
      { act: { click: 'a/attach' } },
      { act: { click: 'a/file:q3' } },
      { say: t('I click [Send](click:a/schedule#press).', 'Нажимаю [Отправить](click:a/schedule#press).'), name: 'claim' },
      { wait: 1 },
      {
        say: t(
          "And it's just [hanging there](ref:a/msg:s1), not going out. Diego's side is [empty](focus:b#peer).",
          'И он [висит](ref:a/msg:s1), не уходит. У Марко [пусто](focus:b#peer).',
        ),
      },
      { say: t('Some kind of bug, it used to send right away.', 'Баг какой-то, раньше сразу отправлялось.'), name: 'complaint' },
    ],
    bug: {
      class: 'not-a-bug',
      title: t('Not a bug: "Schedule send" was clicked instead of "Send"', 'Не баг: вместо «Отправить» нажата «Запланировать отправку»'),
      expected: {
        text: t('The file goes to the recipient right after clicking "Send".', 'Файл уходит получателю сразу после нажатия «Отправить».'),
        source: 'speech',
      },
      actual: t(
        'The cursor clicked the neighboring "Schedule send" button (the clock), the message is scheduled for 18:00 and shown with an "at 18:00" label. This is expected behavior.',
        'Курсор нажал соседнюю кнопку «Запланировать отправку» (часы), сообщение запланировано на 18:00 и показано с отметкой «в 18:00». Это ожидаемое поведение.',
      ),
      critical: ['press', 'claim'],
      traps: [
        t(
          'the speech says "Send", the click is on "Schedule send": the correct conclusion is user error, not a bug',
          'речь говорит «Отправить», клик по «Запланировать отправку»: правильный вывод - ошибка пользователя, не баг',
        ),
      ],
    },
    difficulty: { speech: 'contradicts', signal: { kind: 'inline' }, windows: 2, occluded: false, distractors: [], attempts: 'once' },
    variants: [{ id: 'clean', height: 1080, fps: 30, crf: 18, audio: 'clean' }],
  };
};
