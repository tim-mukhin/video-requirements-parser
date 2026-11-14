import type { Scenario } from '../synth/format/scenario.ts';
import type { Lang } from '../synth/i18n.ts';
import { tr } from '../synth/i18n.ts';
import { contoso, people, voice, WALLPAPER } from './common.ts';

export const r1 = (lang: Lang): Scenario => {
  const t = tr(lang);
  const p = people(lang);
  return {
    id: 'r1-live-no-access',
    lang,
    kind: 'bug-repro',
    title: t(`Live speech: "he says it won't open", the context is only on screen`, 'Живая речь: «он пишет, не открывается», контекст только на экране'),
    screen: { w: 1920, h: 1080 },
    wallpaper: WALLPAPER,
    cast: [{ id: 'artem', name: p.artemShort, voice: voice(lang, 'artem') }],
    windows: [{ id: 'a', app: 'relay', title: 'Relay - Contoso', bbox: [260, 44, 1400, 1016], state: contoso(lang) }],
    steps: [
      { say: t('Okay. Hang on.', 'Так. Щас.') },
      { act: { move: [900, 520] } },
      { say: t('So, uh, Diego asked for the report.', 'Вот, короче, Марко просил отчёт.') },
      { act: { click: 'a/attach' } },
      { act: { point: 'a/file:budget', ms: 600 } },
      { act: { click: 'a/file:q3' } },
      { say: t('There. [Sending](click:a/send#send).', 'Вот. [Отправляю](click:a/send#send).') },
      { sys: 'a', op: { status: { msg: 's1', to: 'sent' } }, at: 'send', delay: 0.7 },
      { wait: 2.5 },
      {
        sys: 'a',
        op: { incoming: { id: 'r1', mine: false, author: p.marko, time: '10:44', text: t("Won't open, says no access", 'Не открывается, пишет нет доступа') } },
        delay: 0.2,
        name: 'reply',
      },
      { wait: 0.8 },
      { say: t("Oh, [here](ref:a/msg:r1). He says it won't open.", 'О, [вот](ref:a/msg:r1). Пишет, не открывается.') },
      { say: t('No access, he says. What access, I sent it to him.', 'Нет доступа, говорит. А какой доступ, я же ему отправил.') },
      { wait: 1 },
      { say: t("It was fine before, I think. So yeah, that's the bug.", 'Раньше вроде нормально было. Ну вот, такая вот бага.'), name: 'end' },
    ],
    bug: {
      class: 'silent-fail',
      title: t('A recipient from another organization cannot open the sent file: "no access"', 'Получатель из другой организации не может открыть отправленный файл: «нет доступа»'),
      expected: { text: t('The recipient opens the file sent to them.', 'Получатель открывает отправленный ему файл.'), source: 'implied' },
      actual: t(
        `On the sender side the file "Q3_Report_Zürich.pdf" is marked "sent". The recipient Diego replies with the text "Won't open, says no access". The recipient's window is not in the video.`,
        'У отправителя файл «Отчёт_Q3.pdf» с отметкой «отправлено». Получатель Марко Петрович отвечает текстом «Не открывается, пишет нет доступа». Окна получателя на видео нет.',
      ),
      critical: ['send', 'reply'],
      traps: [
        t(
          'That Diego is from another organization is visible only from the "external" label and the banner "This chat includes people from another organization (Fabrikam)"; it is not said aloud',
          'что Марко из другой организации, видно только по метке «внешний» и плашке «В чате есть участники из другой организации (Fabrikam)»; голосом не сказано',
        ),
        t('The error was seen by the recipient: in the video it exists only as his text message', 'ошибку видел получатель: на видео она есть только как его текстовое сообщение'),
        t('"It was fine before" is a claim that is not shown', '«раньше нормально было» - утверждение без показа'),
      ],
    },
    difficulty: { speech: 'vague', signal: { kind: 'none' }, windows: 1, occluded: false, distractors: ['cursor-wander'], attempts: 'once' },
    variants: [
      { id: 'clean', height: 1080, fps: 30, crf: 18, audio: 'clean' },
      { id: 'low', height: 720, fps: 15, crf: 32, audio: 'noise' },
    ],
  };
};
