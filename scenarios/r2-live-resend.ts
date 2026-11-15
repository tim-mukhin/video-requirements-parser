import type { Scenario } from '../synth/format/scenario.ts';
import type { Lang } from '../synth/i18n.ts';
import { tr } from '../synth/i18n.ts';
import { contoso, people, voice, WALLPAPER } from './common.ts';

export const r2 = (lang: Lang): Scenario => {
  const t = tr(lang);
  const p = people(lang);
  const toast = {
    toast: { text: t('Could not deliver: the recipient is in an external organization', 'Не удалось доставить: получатель во внешней организации'), tone: 'error' as const },
  };
  return {
    id: 'r2-live-resend',
    lang,
    kind: 'bug-repro',
    title: t(
      'Live speech: "it went through on my end", an error flashes twice and the author does not notice it',
      'Живая речь: «у меня ушло», дважды мелькает ошибка, которую автор не замечает',
    ),
    screen: { w: 1920, h: 1080 },
    wallpaper: WALLPAPER,
    cast: [{ id: 'artem', name: p.artemShort, voice: voice(lang, 'artem') }],
    windows: [{ id: 'a', app: 'relay', title: 'Relay - Contoso', bbox: [200, 44, 1500, 1016], state: contoso(lang) }],
    steps: [
      { say: t("Okay, so, look. I'm sending Diego the file.", 'Ну вот, смотрите. Отправляю файл Марко.') },
      { act: { click: 'a/attach' } },
      { act: { click: 'a/file:q3' } },
      { act: { click: 'a/send' }, name: 'send1' },
      { sys: 'a', op: { status: { msg: 's1', to: 'sent' } }, at: 'send1', delay: 0.6 },
      { sys: 'a', op: toast, at: 'send1', delay: 0.9, ms: 300, name: 'toast1' },
      { act: { move: [1200, 480] } },
      { say: t("Went through, I think. There's a check mark.", 'Ушло вроде. Галочка есть.'), name: 'think' },
      { wait: 1.5 },
      { say: t('But he says nothing came. Hang on, once more.', 'А он говорит, ничего не пришло. Щас ещё раз.'), name: 'claim' },
      { act: { click: 'a/attach' } },
      { act: { click: 'a/file:q3' } },
      { act: { click: 'a/send' }, name: 'send2' },
      { sys: 'a', op: { status: { msg: 's2', to: 'sent' } }, at: 'send2', delay: 0.6 },
      { sys: 'a', op: toast, at: 'send2', delay: 1.0, ms: 300, name: 'toast2' },
      {
        sys: 'os',
        op: { notify: { app: t('Calendar', 'Календарь'), title: t('Standup in 5 minutes', 'Стендап через 5 минут'), text: t('Meeting room 4, Relay Meet', 'Переговорная 4, Relay Meet') } },
        at: 'send2',
        delay: 1.7,
        ms: 3500,
        name: 'notify',
      },
      { wait: 0.6 },
      { say: t('There. Went through again. Well, on my end it went through.', 'Вот. Опять ушло. Ну, у меня ушло.') },
      { act: { move: [700, 380] } },
      { say: t("Dunno what's wrong. Maybe something on their end.", 'Не знаю, что не так. Может, у них там что-то.'), name: 'guess' },
    ],
    bug: {
      class: 'silent-fail',
      title: t(
        'A file to an external organization is not delivered, the sender sees "sent", the error flashes for 0.3 s',
        'Файл во внешнюю организацию не доставляется, отправитель видит «отправлено», ошибка мелькает на 0,3 с',
      ),
      expected: { text: t('The file is delivered to the recipient.', 'Файл доставляется получателю.'), source: 'implied' },
      actual: t(
        'Both sends of "Q3_Report_Zürich.pdf" get the "sent" mark, and after each one the toast "Could not deliver: the recipient is in an external organization" appears for 0.3 s. The author does not notice the toast and does not mention it.',
        'Обе отправки «Отчёт_Q3.pdf» получают отметку «отправлено», после каждой на 0,3 с появляется тост «Не удалось доставить: получатель во внешней организации». Автор тост не замечает и о нём не говорит.',
      ),
      critical: ['send1', 'toast1', 'send2', 'toast2'],
      checks: [{ kind: 'unmentioned', at: 'toast1' }, { kind: 'unmentioned', at: 'toast2' }, { kind: 'claim', at: 'think' }, { kind: 'claim', at: 'claim' }, { kind: 'claim', at: 'guess' }],
      traps: [
        t('Neither toast is mentioned aloud', 'оба тоста голосом не упомянуты'),
        t('The calendar notification is unrelated to the bug', 'уведомление календаря не связано с багом'),
        t(`"Maybe something on their end" is the author's guess, not a fact`, '«может, у них там что-то» - догадка автора, не факт'),
      ],
    },
    difficulty: { speech: 'vague', signal: { kind: 'toast', ms: 300 }, windows: 1, occluded: false, distractors: ['notifications', 'cursor-wander'], attempts: 'intermittent' },
    variants: [
      { id: 'clean', height: 1080, fps: 30, crf: 18, audio: 'clean' },
      { id: 'low', height: 720, fps: 15, crf: 32, audio: 'noise' },
    ],
  };
};
