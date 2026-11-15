import type { Scenario } from '../synth/format/scenario.ts';
import type { Lang } from '../synth/i18n.ts';
import { tr } from '../synth/i18n.ts';
import { contoso, fabrikam, files, people, voice, WALLPAPER } from './common.ts';

export const b4 = (lang: Lang): Scenario => {
  const t = tr(lang);
  const p = people(lang);
  const f = files(lang);
  return {
    id: 'b4-upload-stuck',
    lang,
    kind: 'bug-repro',
    title: t('The second file in a row gets stuck at 99% upload', 'Второй файл подряд зависает на 99% загрузки'),
    screen: { w: 1920, h: 1080 },
    wallpaper: WALLPAPER,
    cast: [{ id: 'artem', name: p.artemShort, voice: voice(lang, 'artem') }],
    windows: [
      { id: 'b', app: 'relay', title: 'Relay - Fabrikam', bbox: [966, 44, 934, 1016], state: fabrikam(lang) },
      { id: 'a', app: 'relay', title: 'Relay - Contoso', bbox: [20, 44, 934, 1016], state: contoso(lang) },
    ],
    steps: [
      { say: t("Let me show how sending gets stuck. First I'm sending the budget.", 'Покажу, как зависает отправка. Сначала отправляю бюджет.') },
      { act: { click: 'a/attach' } },
      { act: { click: 'a/file:budget' } },
      { act: { click: 'a/send' }, name: 'send1' },
      { sys: 'a', op: { progress: { msg: 's1', value: 45 } }, at: 'send1', delay: 0.3 },
      { sys: 'a', op: { progress: { msg: 's1', value: 100 } }, at: 'send1', delay: 0.8 },
      { sys: 'a', op: { status: { msg: 's1', to: 'sent' } }, at: 'send1', delay: 1.0 },
      { sys: 'b', op: { incoming: { id: 'r1', mine: false, author: p.artem, time: '10:43', file: f[1] } }, at: 'send1', delay: 1.5, name: 'arrive1' },
      { sys: 'a', op: { status: { msg: 's1', to: 'delivered' } }, at: 'send1', delay: 1.8 },
      { wait: 1.5 },
      { say: t('It went through, Diego has it. Now the report.', 'Дошёл, у Марко он есть. Теперь отчёт.') },
      { act: { click: 'a/attach' } },
      { act: { click: 'a/file:q3' } },
      { act: { click: 'a/send' }, name: 'send2' },
      { sys: 'a', op: { progress: { msg: 's2', value: 12 } }, at: 'send2', delay: 0.3 },
      { sys: 'a', op: { progress: { msg: 's2', value: 37 } }, at: 'send2', delay: 0.9 },
      { sys: 'a', op: { progress: { msg: 's2', value: 64 } }, at: 'send2', delay: 1.6 },
      { sys: 'a', op: { progress: { msg: 's2', value: 88 } }, at: 'send2', delay: 2.3 },
      { sys: 'a', op: { progress: { msg: 's2', value: 99 } }, at: 'send2', delay: 2.9, name: 'stuck' },
      { wait: 3.5 },
      {
        say: t(
          "The upload got to ninety-nine percent and it's [stuck](point:a/msg:s2).",
          'Загрузка дошла до девяноста девяти процентов и [стоит](point:a/msg:s2).',
        ),
        name: 'stuck-line',
      },
      { wait: 2 },
      {
        say: t(
          "I'm waiting, nothing changes. Diego [doesn't have the second file](ref:b/messages).",
          'Жду, ничего не меняется. У Марко [второго файла нет](ref:b/messages).',
        ),
      },
      {
        say: t(
          'And it happens every other time: the first file always goes through, the second one in a row gets stuck.',
          'И так через раз: первый файл всегда проходит, второй подряд зависает.',
        ),
        name: 'pattern',
      },
    ],
    bug: {
      class: 'stuck',
      title: t(
        'Uploading the second file in a row stops at 99% and never finishes',
        'Загрузка второго файла подряд останавливается на 99% и не завершается',
      ),
      expected: {
        text: t('The second file uploads and is delivered just like the first one.', 'Второй файл загружается и доставляется так же, как первый.'),
        source: 'implied',
      },
      actual: t(
        `The first file (${f[1].name}) is uploaded and delivered. The second one (${f[0].name}) reaches 99% and stays there; the recipient never gets it.`,
        'Первый файл (Бюджет_2027.xlsx) загружен и доставлен. Второй (Отчёт_Q3.pdf) дошёл до 99% и дальше не меняется; получателю не пришёл.',
      ),
      critical: ['send1', 'arrive1', 'send2', 'stuck'],
      checks: [{ kind: 'claim', at: 'pattern' }],
      traps: [
        t(
          '"every other time" is a claim from the speech, the video shows only one pair of attempts',
          '«через раз» - утверждение из речи, на видео показана только одна пара попыток',
        ),
      ],
    },
    difficulty: { speech: 'explicit', signal: { kind: 'inline' }, windows: 2, occluded: false, distractors: [], attempts: 'intermittent' },
    variants: [{ id: 'clean', height: 1080, fps: 30, crf: 18, audio: 'clean' }],
  };
};
