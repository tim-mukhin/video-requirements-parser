import type { Scenario } from '../synth/format/scenario.ts';
import type { Lang } from '../synth/i18n.ts';
import { tr } from '../synth/i18n.ts';
import { contoso, people, voice, WALLPAPER } from './common.ts';

export const r5 = (lang: Lang): Scenario => {
  const t = tr(lang);
  const p = people(lang);
  return {
    id: 'r5-live-wrong-chat',
    lang,
    kind: 'bug-repro',
    title: t(`Live speech: "Diego didn't get it", but the file went to another chat`, 'Живая речь: «Марко не получил», а файл ушёл в другой чат'),
    screen: { w: 1920, h: 1080 },
    wallpaper: WALLPAPER,
    cast: [{ id: 'artem', name: p.artemShort, voice: voice(lang, 'artem') }],
    windows: [{ id: 'a', app: 'relay', title: 'Relay - Contoso', bbox: [200, 44, 1500, 1016], state: { ...contoso(lang), active: 'dx' } }],
    steps: [
      { say: t('Gonna send Diego the budget real quick.', 'Щас скину Марко бюджет.') },
      { act: { click: 'a/attach' } },
      { act: { click: 'a/file:budget' } },
      { act: { click: 'a/send' }, name: 'send' },
      { sys: 'a', op: { status: { msg: 's1', to: 'delivered' } }, at: 'send', delay: 0.7 },
      { say: t('There, sent.', 'Всё, ушло.') },
      { wait: 2.5 },
      { say: t("He says it didn't come. Hang on, let me look.", 'Он говорит, не пришло. Щас посмотрю.'), name: 'claim' },
      { say: t("[Here's](click:a/chat:marko#open-marko) our chat... and there's nothing here.", '[Вот](click:a/chat:marko#open-marko) наш чат... и тут ничего нет.') },
      { say: t("Weird. I did send it. So that's the problem.", 'Странно. Я же отправлял. Это вот такая проблема.'), name: 'complaint' },
    ],
    bug: {
      class: 'not-a-bug',
      title: t('Not a bug: the file was sent to the "DX Team" chat, not to Diego', 'Не баг: файл отправлен в чат «Команда DX», а не Марко'),
      expected: { text: t('The file reaches Diego.', 'Файл приходит Марко.'), source: 'speech' },
      actual: t(
        'Before sending, the "DX Team" chat is open (the team header and feed); "Budget_2027.xlsx" went there and was delivered. The chat with Diego has no file because it was never sent there.',
        'Перед отправкой открыт чат «Команда DX» (заголовок и лента команды); «Бюджет_2027.xlsx» ушёл туда и доставлен. В чате с Марко Петровичем файла нет, потому что туда его не отправляли.',
      ),
      critical: ['send', 'open-marko'],
      traps: [
        t('User error: at the moment of sending the chat header said "DX Team"', 'ошибка пользователя: в заголовке чата при отправке было «Команда DX»'),
        t(
          'Side fact: the budget went to the team chat - this may be a separate problem, but not an app bug',
          'побочный факт: бюджет ушёл в командный чат - это может быть отдельной проблемой, но не багом приложения',
        ),
      ],
    },
    difficulty: { speech: 'vague', signal: { kind: 'none' }, windows: 1, occluded: false, distractors: [], attempts: 'once' },
    variants: [{ id: 'clean', height: 1080, fps: 30, crf: 18, audio: 'clean' }],
  };
};
