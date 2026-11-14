import type { Scenario } from '../synth/format/scenario.ts';
import type { Lang } from '../synth/i18n.ts';
import { tr } from '../synth/i18n.ts';
import { contoso, fabrikam, files, people, voice, WALLPAPER } from './common.ts';

const box: [number, number, number, number] = [60, 44, 1800, 1016];

export const w2 = (lang: Lang): Scenario => {
  const t = tr(lang);
  const p = people(lang);
  const contract = files(lang)[2];
  return {
    id: 'w2-web-tabs-duplicate',
    lang,
    kind: 'bug-repro',
    title: t(
      'Relay in the browser, two tabs: the external recipient gets the file twice',
      'Relay в браузере, две вкладки: внешний получатель получает файл дважды',
    ),
    screen: { w: 1920, h: 1080 },
    wallpaper: WALLPAPER,
    cast: [{ id: 'artem', name: p.artemShort, voice: voice(lang, 'artem') }],
    windows: [
      {
        id: 'b',
        app: 'relay',
        title: 'Relay - Fabrikam',
        bbox: box,
        browser: { url: 'relay.fabrikam.com/chat/artem', tab: t('Relay - Fabrikam (test)', 'Relay - Fabrikam (тест)'), group: 'g' },
        state: fabrikam(lang),
      },
      { id: 'a', app: 'relay', title: 'Relay - Contoso', bbox: box, browser: { url: 'relay.contoso.com/chat/marko', tab: 'Relay - Contoso', group: 'g' }, state: contoso(lang) },
    ],
    steps: [
      {
        say: t(
          "This is the Relay web version. I'm in one tab, and Diego's test account is in the other.",
          'Веб-версия Relay. В одной вкладке я, во второй тестовый аккаунт Марко.',
        ),
      },
      { act: { click: 'a/attach' } },
      { act: { click: 'a/file:contract' } },
      { say: t('I send the agreement [once](click:a/send#send).', 'Отправляю договор [один раз](click:a/send#send).') },
      { sys: 'a', op: { status: { msg: 's1', to: 'sent' } }, at: 'send', delay: 0.6 },
      { sys: 'b', op: { incoming: { id: 'r1', mine: false, author: p.artem, time: '10:43', file: contract } }, at: 'send', delay: 1.2, name: 'arrive1' },
      { sys: 'b', op: { incoming: { id: 'r2', mine: false, author: p.artem, time: '10:43', file: contract } }, at: 'send', delay: 2.1, name: 'arrive2' },
      { sys: 'a', op: { status: { msg: 's1', to: 'delivered' } }, at: 'send', delay: 2.4 },
      { wait: 1 },
      {
        say: t("I have one message. Switching to [Diego's tab](click:b/__tab#tab).", 'У меня одно сообщение. Переключаюсь на [вкладку Марко](click:b/__tab#tab).'),
      },
      {
        say: t('But on his side the agreement came in [twice](point:b/messages#twice).', 'А у него договор пришёл [два раза](point:b/messages#twice).'),
        name: 'claim',
      },
      { say: t('I expect one copy per send.', 'Ожидаю одну копию на одну отправку.'), name: 'expect' },
    ],
    bug: {
      class: 'wrong-data',
      title: t(
        'One sent message with a file is delivered to the external recipient twice',
        'Одно отправленное сообщение с файлом доставляется внешнему получателю дважды',
      ),
      expected: { text: t('One send, one message for the recipient.', 'Одна отправка - одно сообщение у получателя.'), source: 'speech' },
      actual: t(
        `The Contoso tab has one "${contract.name}" message, the Fabrikam tab has two identical messages with this file, about a second apart.`,
        'Во вкладке Contoso одно сообщение «Договор_поставки.docx», во вкладке Fabrikam два одинаковых сообщения с этим файлом с разницей около секунды.',
      ),
      critical: ['send', 'arrive1', 'arrive2', 'tab'],
      traps: [
        t(
          'both organizations are in one browser window: the window content changes when switching tabs',
          'обе организации в одном окне браузера: содержимое окна меняется при переключении вкладки',
        ),
        t(
          'the second copy arrived while the other tab was open: it is not visible at the moment it arrives',
          'вторая копия пришла, пока была открыта другая вкладка: в момент прихода её не видно',
        ),
      ],
    },
    difficulty: { speech: 'explicit', signal: { kind: 'inline' }, windows: 1, occluded: true, distractors: [], attempts: 'once' },
    variants: [{ id: 'clean', height: 1080, fps: 30, crf: 18, audio: 'clean' }],
  };
};
