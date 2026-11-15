import type { Scenario } from '../synth/format/scenario.ts';
import type { Lang } from '../synth/i18n.ts';
import { tr } from '../synth/i18n.ts';
import { fabrikam, files, people, voice } from './common.ts';

export const p1 = (lang: Lang): Scenario => {
  const t = tr(lang);
  const p = people(lang);
  const f = files(lang);
  const blocked = t(
    'Contoso policy does not allow access to this file for people outside the organization.',
    'Политика организации Contoso запрещает доступ к этому файлу для пользователей из других организаций.',
  );
  return {
    id: 'p1-phone-blocked-file',
    lang,
    kind: 'bug-repro',
    title: t('Phone: an external recipient cannot open a file sent to them', 'Телефон: внешний получатель не может открыть присланный файл'),
    screen: { w: 1080, h: 1920 },
    device: 'phone',
    wallpaper: '#fff',
    cast: [{ id: 'artem', name: p.artemShort, voice: voice(lang, 'artem') }],
    windows: [{ id: 'm', app: 'relay', title: 'Relay', bbox: [0, 0, 1080, 1920], state: fabrikam(lang) }],
    steps: [
      { say: t("This is a test phone signed in as Diego from Fabrikam. I'm waiting for a file from myself.", 'Это тестовый телефон с аккаунтом Марко из Fabrikam. Жду файл от себя.') },
      { sys: 'os', op: { notify: { app: 'Relay', title: p.artem, text: f[0].name } }, delay: 0.4, ms: 2500, name: 'banner' },
      { sys: 'm', op: { incoming: { id: 'r1', mine: false, author: p.artem, time: '10:43', file: f[0], blocked } }, delay: 0.2, name: 'arrive' },
      { wait: 1.5 },
      { say: t('It arrived, but with a lock. I tap [the file](click:m/msg:r1#open).', 'Пришёл, но с замком. Нажимаю [на файл](click:m/msg:r1#open).') },
      { say: t('File unavailable, organization policy. Same thing on the computer.', 'Файл недоступен, политика организации. С компьютера то же самое.'), name: 'seen' },
      { act: { click: 'm/dialog-ok' } },
      { say: t('I expect a chat member to be able to open a file that was sent to them.', 'Ожидаю, что участник чата может открыть файл, который ему прислали.'), name: 'expect' },
    ],
    bug: {
      class: 'error-shown',
      title: t('Mobile Relay: a file from an external organization does not open for the recipient', 'Мобильный Relay: файл от внешней организации не открывается у получателя'),
      expected: { text: t('A chat member opens the file sent to them.', 'Участник чата открывает присланный файл.'), source: 'speech' },
      actual: t(
        'The file arrives with a lock and the caption "File unavailable"; tapping it shows a system dialog "File unavailable" that cites the Contoso policy.',
        'Файл приходит с замком и подписью «Файл недоступен»; при нажатии - системное окно «Файл недоступен» со ссылкой на политику Contoso.',
      ),
      critical: ['banner', 'arrive', 'open'],
      checks: [{ kind: 'claim', at: 'seen' }],
      traps: [t('"Same thing on the computer" is a claim that is not shown; the video shows only the phone', '«с компьютера то же самое» - утверждение без показа, на видео только телефон')],
    },
    difficulty: { speech: 'explicit', signal: { kind: 'modal' }, windows: 1, occluded: false, distractors: [], attempts: 'once' },
    variants: [
      { id: 'clean', height: 1920, fps: 30, crf: 18, audio: 'clean' },
      { id: 'low', height: 1280, fps: 30, crf: 30, audio: 'noise' },
    ],
  };
};
