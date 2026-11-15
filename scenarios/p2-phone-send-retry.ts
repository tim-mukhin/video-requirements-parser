import type { Scenario } from '../synth/format/scenario.ts';
import type { Lang } from '../synth/i18n.ts';
import { tr } from '../synth/i18n.ts';
import { contoso, people, voice } from './common.ts';

export const p2 = (lang: Lang): Scenario => {
  const t = tr(lang);
  const p = people(lang);
  return {
    id: 'p2-phone-send-retry',
    lang,
    kind: 'bug-repro',
    title: t('Phone: a file to an external chat is not sent, and retrying fails again', 'Телефон: файл во внешний чат не отправляется, повтор снова падает'),
    screen: { w: 1080, h: 1920 },
    device: 'phone',
    wallpaper: '#fff',
    cast: [{ id: 'artem', name: p.artemShort, voice: voice(lang, 'artem') }],
    windows: [{ id: 'a', app: 'relay', title: 'Relay', bbox: [0, 0, 1080, 1920], state: contoso(lang) }],
    steps: [
      { say: t("From the phone, files don't go through to the chat with Diego. Let me show you.", 'С телефона в чат с Марко файлы не уходят. Показываю.') },
      { act: { click: 'a/attach' } },
      { act: { click: 'a/file:budget' } },
      { say: t('The budget, [send](click:a/send#send).', 'Бюджет, [отправить](click:a/send#send).') },
      { sys: 'a', op: { progress: { msg: 's1', value: 30 } }, at: 'send', delay: 0.4 },
      { sys: 'a', op: { progress: { msg: 's1', value: 62 } }, at: 'send', delay: 1.1 },
      { sys: 'a', op: { status: { msg: 's1', to: 'failed' } }, at: 'send', delay: 2.0, name: 'fail1' },
      { wait: 2.2 },
      { say: t('Not sent. I tap [retry](click:a/retry:s1#retry).', 'Не отправлено. Нажимаю [повторить](click:a/retry:s1#retry).') },
      { sys: 'a', op: { progress: { msg: 's1', value: 41 } }, at: 'retry', delay: 0.5 },
      { sys: 'a', op: { status: { msg: 's1', to: 'failed' } }, at: 'retry', delay: 1.4, name: 'fail2' },
      { wait: 1.5 },
      { say: t('And again. The connection is fine, though, websites open.', 'И опять. Связь при этом нормальная, сайты открываются.'), name: 'network-claim' },
      { say: t('Inside Contoso everything goes through from the phone, the problem is only with external people.', 'Внутри Contoso с телефона всё уходит, проблема только с внешними.'), name: 'scope' },
    ],
    bug: {
      class: 'error-shown',
      title: t(
        'Mobile Relay: sending a file to an external chat fails halfway through the upload, retrying does not help',
        'Мобильный Relay: отправка файла во внешний чат падает на середине загрузки, повтор не помогает',
      ),
      expected: { text: t('The file is sent to an external chat the same way as to an internal one.', 'Файл отправляется во внешний чат так же, как во внутренний.'), source: 'implied' },
      actual: t(
        'The upload reaches 62%, the message turns into "Not sent" with a "Retry" button; after retrying, the upload reaches 41% and again "Not sent".',
        'Загрузка доходит до 62%, сообщение становится «Не отправлено» с кнопкой «Повторить»; после повтора загрузка до 41% и снова «Не отправлено».',
      ),
      critical: ['send', 'fail1', 'retry', 'fail2'],
      checks: [{ kind: 'claim', at: 'network-claim' }, { kind: 'claim', at: 'scope' }],
      traps: [t('"The connection is fine" and "inside Contoso everything goes through" are claims that are not shown', '«связь нормальная» и «внутри Contoso всё уходит» - утверждения без показа')],
    },
    difficulty: { speech: 'explicit', signal: { kind: 'inline' }, windows: 1, occluded: false, distractors: [], attempts: 'intermittent' },
    variants: [{ id: 'clean', height: 1920, fps: 30, crf: 18, audio: 'clean' }],
  };
};
