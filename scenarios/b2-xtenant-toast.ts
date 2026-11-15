import type { Scenario } from '../synth/format/scenario.ts';
import type { Lang } from '../synth/i18n.ts';
import { tr } from '../synth/i18n.ts';
import { contoso, fabrikam, people, voice, WALLPAPER } from './common.ts';

export const b2 = (lang: Lang): Scenario => {
  const t = tr(lang);
  const p = people(lang);
  return {
    id: 'b2-xtenant-toast',
    lang,
    kind: 'bug-repro',
    title: t(
      'A file to an external organization silently fails to arrive, the error flashes for 0.3 s',
      'Файл во внешнюю организацию молча не доходит, ошибка мелькает на 0,3 с',
    ),
    screen: { w: 1920, h: 1080 },
    wallpaper: WALLPAPER,
    cast: [{ id: 'artem', name: p.artemShort, voice: voice(lang, 'artem') }],
    windows: [
      { id: 'b', app: 'relay', title: 'Relay - Fabrikam', bbox: [760, 96, 1120, 940], state: fabrikam(lang) },
      { id: 'a', app: 'relay', title: 'Relay - Contoso', bbox: [36, 52, 1180, 1000], state: contoso(lang) },
    ],
    steps: [
      { say: t("So, files aren't getting through again. Let me show you.", 'Короче, опять файлы не доходят. Сейчас покажу.') },
      { act: { click: 'a/attach' } },
      { act: { click: 'a/file:q3' } },
      { say: t('Here, [this one](ref:a/staged), [sending](click:a/send#send) it.', 'Вот, [вот это](ref:a/staged) [кидаю](click:a/send#send).') },
      { sys: 'a', op: { status: { msg: 's1', to: 'sent' } }, at: 'send', delay: 0.7, name: 'sent' },
      {
        sys: 'a',
        op: {
          toast: {
            text: t("Couldn't deliver: the recipient is in an external organization", 'Не удалось доставить: получатель во внешней организации'),
            tone: 'error',
          },
        },
        at: 'send',
        delay: 1.1,
        ms: 300,
        name: 'toast',
      },
      {
        sys: 'os',
        op: {
          notify: {
            app: t('Calendar', 'Календарь'),
            title: t('Standup in 5 minutes', 'Стендап через 5 минут'),
            text: t('Room 4, Relay Meet', 'Переговорная 4, Relay Meet'),
          },
        },
        at: 'send',
        delay: 2.0,
        ms: 4000,
        name: 'notify',
      },
      { say: t('Well, looks like it went out, [here](ref:a/msg:s1) is the check mark.', 'Ну, вроде ушло, [вот](ref:a/msg:s1) отметка стоит.') },
      { say: t("But [on his side](focus:b#peer) it's empty. Nothing came through.", 'А [у него](focus:b#peer) пусто. Ничего не пришло.') },
      { wait: 0.6 },
      { say: t('And [here](ref:?) there was nothing either, I already checked.', 'И [тут](ref:?) тоже ничего не было, я уже проверял.'), name: 'checked' },
      { say: t('It should just arrive, like it normally does.', 'Должно же приходить, как обычно.'), name: 'normally' },
    ],
    bug: {
      class: 'silent-fail',
      title: t(
        'A file to an external organization is not delivered, but the sender sees "sent"',
        'Файл во внешнюю организацию не доставляется, а отправитель видит «отправлено»',
      ),
      expected: {
        text: t(
          'The file is delivered to the recipient from another organization, the same as an internal one.',
          'Файл доставляется получателю из другой организации, как и внутренний.',
        ),
        source: 'implied',
      },
      actual: t(
        'On the sender side the message with the file is marked as sent; a toast "Couldn\'t deliver: the recipient is in an external organization" flashes for 0.3 s; the message never appears for the recipient.',
        'У отправителя сообщение с файлом отмечено отправленным; на 0,3 с мелькает тост «Не удалось доставить: получатель во внешней организации»; у получателя сообщение не появляется.',
      ),
      critical: ['send', 'toast', 'peer'],
      checks: [{ kind: 'unmentioned', at: 'toast' }, { kind: 'claim', at: 'checked' }, { kind: 'claim', at: 'normally' }],
      traps: [
        t('notify: the calendar notification is unrelated to the bug', 'notify: уведомление календаря не связано с багом'),
        t(
          '"here" in line l06 does not point to anything on screen: the correct answer is unresolved',
          '«тут» в реплике l06 не указывает ни на что на экране: правильный ответ unresolved',
        ),
        t('the "sent" check mark contradicts the error toast', 'галочка «отправлено» противоречит тосту об ошибке'),
      ],
    },
    difficulty: {
      speech: 'deictic',
      signal: { kind: 'toast', ms: 300 },
      windows: 2,
      occluded: true,
      distractors: ['notifications'],
      attempts: 'once',
    },
    variants: [
      { id: 'clean', height: 1080, fps: 30, crf: 18, audio: 'clean' },
      { id: 'low', height: 720, fps: 15, crf: 34, audio: 'noise' },
    ],
  };
};
