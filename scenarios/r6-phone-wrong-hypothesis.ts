import type { Scenario } from '../synth/format/scenario.ts';
import type { Lang } from '../synth/i18n.ts';
import { tr } from '../synth/i18n.ts';
import { contoso, files, people, voice } from './common.ts';

export const r6 = (lang: Lang): Scenario => {
  const t = tr(lang);
  const p = people(lang);
  const [, budget, , shot] = files(lang);
  return {
    id: 'r6-phone-wrong-hypothesis',
    lang,
    kind: 'bug-repro',
    title: t(
      'Phone, live speech: "the file must be too big", but the one that went through is the bigger one',
      'Телефон, живая речь: «наверное, файл большой», а ушёл как раз больший',
    ),
    screen: { w: 1080, h: 1920 },
    device: 'phone',
    wallpaper: '#fff',
    cast: [{ id: 'artem', name: p.artemShort, voice: voice(lang, 'artem') }],
    windows: [{ id: 'a', app: 'relay', title: 'Relay', bbox: [0, 0, 1080, 1920], state: contoso(lang) }],
    steps: [
      { say: t("Ugh, it's not sending from the phone again.", 'Блин, с телефона опять не уходит.') },
      { act: { click: 'a/attach' } },
      { act: { click: 'a/file:budget' } },
      { act: { click: 'a/send' }, name: 'send1' },
      { sys: 'a', op: { progress: { msg: 's1', value: 20 } }, at: 'send1', delay: 0.4 },
      { sys: 'a', op: { progress: { msg: 's1', value: 55 } }, at: 'send1', delay: 1.2 },
      { sys: 'a', op: { status: { msg: 's1', to: 'failed' } }, at: 'send1', delay: 2.1, name: 'fail1' },
      { wait: 2.3 },
      { say: t('There. Not sent.', 'Вот. Не отправлено.') },
      { say: t("Maybe the file's too big? Let me try a small one.", 'Может, файл большой? Щас маленький попробую.'), name: 'hypothesis' },
      { act: { click: 'a/attach' } },
      { act: { click: 'a/file:shot' } },
      { act: { click: 'a/send' }, name: 'send2' },
      { sys: 'a', op: { progress: { msg: 's2', value: 60 } }, at: 'send2', delay: 0.4 },
      { sys: 'a', op: { progress: { msg: 's2', value: 100 } }, at: 'send2', delay: 0.9 },
      { sys: 'a', op: { status: { msg: 's2', to: 'delivered' } }, at: 'send2', delay: 1.3, name: 'ok2' },
      { wait: 1.5 },
      { say: t('Oh. The picture went through. So it was too big, I guess.', 'О. Картинка ушла. Значит, большой был, видимо.'), name: 'conclusion' },
    ],
    bug: {
      class: 'error-shown',
      title: t(
        `Mobile Relay: "${budget.name}" is not sent to an external chat, the picture goes through`,
        `Мобильный Relay: «${budget.name}» во внешний чат не отправляется, картинка уходит`,
      ),
      expected: { text: t('The file is sent to the external chat.', 'Файл отправляется во внешний чат.'), source: 'implied' },
      actual: t(
        `"${budget.name}" (${budget.size}) reaches 55% and turns into "Not sent". "${shot.name}" (${shot.size}) is sent and delivered.`,
        `«${budget.name}» (${budget.size}) доходит до 55% и становится «Не отправлено». «${shot.name}» (${shot.size}) отправляется и доставляется.`,
      ),
      critical: ['send1', 'fail1', 'send2', 'ok2'],
      traps: [
        t(
          `The author's conclusion "the file was too big" is contradicted by the screen: the picture that went through (${shot.size}) is bigger than the file that failed (${budget.size})`,
          `вывод автора «файл был большой» опровергается экраном: ушедшая картинка (${shot.size}) больше упавшего файла (${budget.size})`,
        ),
        t('The difference may be the file type (xlsx and png), this is a hypothesis, not a fact', 'различие может быть в типе файла (xlsx и png), это гипотеза, не факт'),
      ],
    },
    difficulty: { speech: 'vague', signal: { kind: 'inline' }, windows: 1, occluded: false, distractors: [], attempts: 'wrong-path-first' },
    variants: [{ id: 'clean', height: 1920, fps: 30, crf: 18, audio: 'clean' }],
  };
};
