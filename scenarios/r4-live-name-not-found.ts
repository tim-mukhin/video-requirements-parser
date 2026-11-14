import type { RelayState } from '../synth/apps/relay/model.ts';
import type { Scenario } from '../synth/format/scenario.ts';
import type { Lang } from '../synth/i18n.ts';
import { tr } from '../synth/i18n.ts';
import { contoso, fabrikam, files, mojibake, people, voice, WALLPAPER } from './common.ts';

const ask = (lang: Lang) => tr(lang)("Can't find your report in my downloads, what's it called?", 'Не могу найти твой отчёт в загрузках, как он называется?');
const a = (lang: Lang): RelayState => {
  const s = contoso(lang);
  const p = people(lang);
  return {
    ...s,
    threads: {
      ...s.threads,
      marko: [
        ...s.threads.marko,
        { id: 's1', mine: true, author: p.artem, time: '10:43', file: files(lang)[0], status: 'delivered' },
        { id: 'q1', mine: false, author: p.marko, time: '10:51', text: ask(lang) },
      ],
    },
  };
};
const b = (lang: Lang): RelayState => {
  const s = fabrikam(lang);
  const p = people(lang);
  const f = files(lang)[0];
  return {
    ...s,
    threads: {
      ...s.threads,
      artem: [
        ...s.threads.artem,
        { id: 'r1', mine: false, author: p.artem, time: '10:43', file: { ...f, name: mojibake(f.name) } },
        { id: 'q1', mine: true, author: p.marko, time: '10:51', text: ask(lang), status: 'delivered' },
      ],
    },
  };
};

export const r4 = (lang: Lang): Scenario => {
  const t = tr(lang);
  const p = people(lang);
  const name = files(lang)[0].name;
  return {
    id: 'r4-live-name-not-found',
    lang,
    kind: 'bug-repro',
    title: t(
      `Live speech: "he can't find the file", but the file name on his side is broken - the author does not see it`,
      'Живая речь: «он не может найти файл», а имя файла у него битое - автор этого не видит',
    ),
    screen: { w: 1920, h: 1080 },
    wallpaper: WALLPAPER,
    cast: [{ id: 'artem', name: p.artemShort, voice: voice(lang, 'artem') }],
    windows: [
      { id: 'b', app: 'relay', title: 'Relay - Fabrikam', bbox: [966, 44, 934, 1016], state: b(lang) },
      { id: 'a', app: 'relay', title: 'Relay - Contoso', bbox: [20, 44, 934, 1016], state: a(lang) },
    ],
    steps: [
      { say: t("Okay, Diego writes that he can't find the file.", 'Так, Марко пишет, что не может найти файл.'), name: 'claim' },
      { say: t("It's right here, I sent it. [Here](point:a/msg:s1).", 'Вот же он, я отправил. [Вот](point:a/msg:s1).') },
      { say: t("And on his side it's [here](point:b/msg:r1#theirs), it came.", 'И у него [вот](point:b/msg:r1#theirs) он есть, пришёл.') },
      { say: t("I mean, it's right there. Dunno why he can't see it.", 'Ну вот же он. Не знаю, чего он не видит.') },
      { act: { point: 'b/msg:r1', ms: 1200 } },
      { say: t('Maybe his downloads are, uh, saving somewhere wrong.', 'Может, у него загрузки куда-то не туда сохраняются.'), name: 'guess' },
    ],
    bug: {
      class: 'wrong-data',
      title: t(
        'For an external recipient a file name with non-ASCII characters arrives in the wrong encoding, so the file cannot be found by name',
        'У внешнего получателя имя файла с кириллицей приходит в неверной кодировке, поэтому файл не находится по имени',
      ),
      expected: { text: t('The recipient sees the file under the same name as the sender.', 'У получателя файл называется так же, как у отправителя.'), source: 'implied' },
      actual: t(
        `The sender has "${name}", the recipient has the same file named "${mojibake(name)}". The recipient asks what the file is called because he cannot find it in his downloads.`,
        `У отправителя «${name}», у получателя тот же файл называется «${mojibake(name)}». Получатель спрашивает, как называется файл, потому что не находит его в загрузках.`,
      ),
      critical: ['claim', 'theirs'],
      traps: [
        t(
          'The author does not notice the broken name and does not say it aloud: the cause has to be seen by comparing the text in the two windows',
          'автор не замечает битое имя и голосом его не называет: причину надо увидеть, сравнив текст двух окон',
        ),
        t('"Maybe the downloads are saving somewhere wrong" is a wrong guess by the author', '«может, загрузки не туда сохраняются» - неверная догадка автора'),
      ],
    },
    difficulty: { speech: 'vague', signal: { kind: 'inline' }, windows: 2, occluded: false, distractors: [], attempts: 'once' },
    variants: [
      { id: 'clean', height: 1080, fps: 30, crf: 18, audio: 'clean' },
      { id: 'small', height: 480, fps: 30, crf: 28, audio: 'clean' },
    ],
  };
};
