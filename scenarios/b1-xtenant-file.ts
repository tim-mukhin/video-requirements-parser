import type { Scenario } from '../synth/format/scenario.ts';
import type { Lang } from '../synth/i18n.ts';
import { tr } from '../synth/i18n.ts';
import { contoso, fabrikam, files, people, voice, WALLPAPER } from './common.ts';

export const b1 = (lang: Lang): Scenario => {
  const t = tr(lang);
  const p = people(lang);
  const blocked = t(
    'Contoso policy does not allow access to this file for people outside the organization.',
    'Политика организации Contoso запрещает доступ к этому файлу для пользователей из других организаций.',
  );
  return {
    id: 'b1-xtenant-file',
    lang,
    kind: 'bug-repro',
    title: t('A file from Contoso does not open for the recipient at Fabrikam', 'Файл из Contoso не открывается у получателя из Fabrikam'),
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
          "Let me show a bug with sending files between organizations. On the left I'm in Contoso, on the right is my colleague Diego from Fabrikam.",
          'Покажу баг с передачей файлов между организациями. Слева я в Contoso, справа мой коллега Марко из Fabrikam.',
        ),
      },
      { say: t('Diego asked for the report. I click the [paperclip](click:a/attach) and pick the file.', 'Марко просит отчёт. Нажимаю [скрепку](click:a/attach) и выбираю файл.') },
      { act: { click: 'a/file:q3' }, name: 'pick' },
      { say: t("The file is attached, I'm [sending](click:a/send#send) it.", 'Файл прикреплён, [отправляю](click:a/send#send).') },
      { sys: 'a', op: { status: { msg: 's1', to: 'sent' } }, at: 'send', delay: 0.9, name: 'sent' },
      {
        sys: 'b',
        op: { incoming: { id: 'r1', mine: false, author: p.artem, time: '10:43', file: files(lang)[0], blocked } },
        at: 'send',
        delay: 1.6,
        name: 'arrive',
      },
      {
        say: t(
          "On my side there's a check mark, the file went out. Diego got it too, but with a lock. I try to [open](click:b/msg:r1#open) it.",
          'У меня стоит галочка, файл ушёл. У Марко он тоже появился, но с замком. Пробую [открыть](click:b/msg:r1#open).',
        ),
      },
      {
        say: t(
          'It says [file unavailable](ref:b/dialog), the organization policy blocks access for outside people.',
          'Пишет: [файл недоступен](ref:b/dialog), политика организации запрещает доступ внешним пользователям.',
        ),
      },
      {
        say: t(
          'But Diego is a member of this chat. I expect him to be able to open a file that was sent to him.',
          'Но Марко - участник этого чата. Ожидаю, что он сможет открыть файл, который ему отправили.',
        ),
      },
      { act: { click: 'b/dialog-ok' } },
    ],
    bug: {
      class: 'error-shown',
      title: t('A recipient from another organization cannot open a file sent to the chat', 'Получатель из другой организации не может открыть файл, отправленный в чат'),
      expected: { text: t('An external chat member opens the file sent to them.', 'Внешний участник чата открывает файл, который ему отправили.'), source: 'speech' },
      actual: t(
        'The sender sees the file as sent; the recipient gets the file with a lock, and opening it shows a "File unavailable" dialog that cites the Contoso policy.',
        'У отправителя файл отмечен отправленным; у получателя файл пришёл с замком, при открытии - диалог «Файл недоступен» со ссылкой на политику Contoso.',
      ),
      critical: ['send', 'arrive', 'open'],
    },
    difficulty: { speech: 'explicit', signal: { kind: 'modal' }, windows: 2, occluded: false, distractors: [], attempts: 'once' },
    variants: [{ id: 'clean', height: 1080, fps: 30, crf: 18, audio: 'clean' }],
  };
};
