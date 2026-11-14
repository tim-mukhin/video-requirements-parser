import type { Scenario } from '../synth/format/scenario.ts';
import type { Lang } from '../synth/i18n.ts';
import { tr } from '../synth/i18n.ts';
import { contoso, fabrikam, files, mojibake, people, voice, WALLPAPER } from './common.ts';

export const b3 = (lang: Lang): Scenario => {
  const t = tr(lang);
  const p = people(lang);
  const q3 = files(lang)[0];
  return {
    id: 'b3-xtenant-mojibake',
    lang,
    kind: 'bug-repro',
    title: t(
      'For a recipient in another organization, non-ASCII letters in the file name turn into garbage',
      'У получателя из другой организации кириллица в имени файла превращается в кашу',
    ),
    screen: { w: 1920, h: 1080 },
    wallpaper: WALLPAPER,
    cast: [{ id: 'artem', name: p.artemShort, voice: voice(lang, 'artem') }],
    windows: [
      { id: 'b', app: 'relay', title: 'Relay - Fabrikam', bbox: [966, 44, 934, 1016], state: fabrikam(lang) },
      { id: 'a', app: 'relay', title: 'Relay - Contoso', bbox: [20, 44, 934, 1016], state: contoso(lang) },
    ],
    steps: [
      {
        say: t(
          "One more weird thing with files between organizations. I'm sending Diego the report.",
          'Ещё одна странность с файлами между организациями. Отправляю Марко отчёт.',
        ),
      },
      { act: { click: 'a/attach' } },
      { act: { click: 'a/file:q3' } },
      { act: { click: 'a/send' }, name: 'send' },
      { sys: 'a', op: { status: { msg: 's1', to: 'sent' } }, at: 'send', delay: 0.6 },
      {
        sys: 'b',
        op: { incoming: { id: 'r1', mine: false, author: p.artem, time: '10:43', file: { ...q3, name: mojibake(q3.name) } } },
        at: 'send',
        delay: 1.3,
        name: 'arrive',
      },
      { sys: 'a', op: { status: { msg: 's1', to: 'delivered' } }, at: 'send', delay: 1.6 },
      { wait: 1.2 },
      {
        say: t(
          "Delivered, two check marks. Now look at [the file name on Diego's side](point:b/msg:r1#look).",
          'Доставлено, две галочки. А теперь посмотрите на [имя файла у Марко](point:b/msg:r1#look).',
        ),
        name: 'look-line',
      },
      {
        say: t(
          "Instead of the u with the two dots there's some garbled mess. No error, the file opens, but the name is broken.",
          'Вместо русских букв какая-то каша. Ошибки нет, файл открывается, но имя сломано.',
        ),
      },
      {
        say: t(
          'I expect the recipient to see the same file name as I do: Q3 Report Zürich.',
          'Ожидаю, что у получателя файл называется так же, как у меня: отчёт Q3.',
        ),
        name: 'expect',
      },
    ],
    bug: {
      class: 'wrong-data',
      title: t(
        'A file name with non-ASCII letters reaches an external recipient in the wrong encoding',
        'Имя файла с кириллицей приходит внешнему получателю в неверной кодировке',
      ),
      expected: {
        text: t(`The recipient sees the original file name: "${q3.name}".`, 'У получателя имя файла совпадает с исходным: «Отчёт_Q3.pdf».'),
        source: 'speech',
      },
      actual: t(
        `The sender sees "${q3.name}", the Fabrikam recipient sees "${mojibake(q3.name)}": UTF-8 read as Windows-1252. No errors on screen, the status is "delivered".`,
        `У отправителя «Отчёт_Q3.pdf», у получателя из Fabrikam «${mojibake('Отчёт_Q3.pdf')}»: UTF-8, прочитанный как Windows-1252. Ошибок на экране нет, статус «доставлено».`,
      ),
      critical: ['send', 'arrive', 'look'],
      traps: [
        t(
          'no errors on screen: the bug is only visible by comparing the text in the two windows',
          'ошибок на экране нет: баг виден только при сравнении текста двух окон',
        ),
      ],
    },
    difficulty: { speech: 'explicit', signal: { kind: 'inline' }, windows: 2, occluded: false, distractors: [], attempts: 'once' },
    variants: [
      { id: 'clean', height: 1080, fps: 30, crf: 18, audio: 'clean' },
      { id: 'small', height: 480, fps: 30, crf: 28, audio: 'clean' },
    ],
  };
};
