import type { Scenario } from '../synth/format/scenario.ts';
import type { Lang } from '../synth/i18n.ts';
import { tr } from '../synth/i18n.ts';
import { contoso, fabrikam, people, vaultContoso, voice, WALLPAPER } from './common.ts';

const withBot = (lang: Lang) => {
  const t = tr(lang);
  const s = contoso(lang);
  return { ...s, chats: [...s.chats, { id: 'bot', title: 'Relay Bot', preview: t('Welcome to Relay', 'Добро пожаловать в Relay'), initials: 'RB' }] };
};

export const b7 = (lang: Lang): Scenario => {
  const t = tr(lang);
  const p = people(lang);
  return {
    id: 'b7-hidden-error',
    lang,
    kind: 'bug-repro',
    title: t(
      'An invitation to an external user is not sent, the error is in a covered window',
      'Приглашение внешнему пользователю не уходит, ошибка в перекрытом окне',
    ),
    screen: { w: 1920, h: 1080 },
    wallpaper: WALLPAPER,
    cast: [{ id: 'artem', name: p.artemShort, voice: voice(lang, 'artem') }],
    windows: [
      { id: 'a', app: 'relay', title: 'Relay - Contoso', bbox: [20, 40, 900, 1010], state: withBot(lang) },
      { id: 'b', app: 'relay', title: 'Relay - Fabrikam', bbox: [1000, 90, 900, 960], state: fabrikam(lang) },
      { id: 'v', app: 'vault', title: t('Vault - My Drive', 'Vault - Мой диск'), bbox: [330, 64, 1240, 960], state: vaultContoso(lang) },
    ],
    steps: [
      { say: t('I want to give Diego access to the report right from Vault.', 'Хочу дать Марко доступ к отчёту прямо из Vault.') },
      { act: { click: 'v/row:q3' } },
      { act: { click: 'v/share' } },
      { act: { type: 'v/invite', text: t('diego@fabrikam.com', 'marko@fabrikam.com') }, name: 'invite' },
      { say: t("Added Diego, and I'm [saving](click:v/save#save).", 'Добавил Марко и [сохраняю](click:v/save#save).') },
      { sys: 'v', op: { toast: { text: t('Invitation sent', 'Приглашение отправлено'), tone: 'info' } }, at: 'save', delay: 0.5, ms: 2500, name: 'sent' },
      {
        sys: 'a',
        op: {
          chat: {
            id: 'bot',
            preview: t(
              "Couldn't send the invitation to diego@fabrikam.com: external invitations are turned off",
              'Не удалось отправить приглашение marko@fabrikam.com: внешние приглашения отключены',
            ),
            unread: 1,
          },
        },
        at: 'save',
        delay: 1.2,
        name: 'bot-error',
      },
      { wait: 2 },
      { say: t("Done. Now I'm checking [whether Diego got it](focus:b#peer).", 'Готово. Теперь смотрю, [пришло ли у Марко](focus:b#peer).') },
      { say: t('Nothing there. No message, no invitation to the file.', 'Ничего нет. Ни сообщения, ни приглашения к файлу.') },
      { say: t('I expect Diego to get the invitation.', 'Ожидаю, что Марко получит приглашение.'), name: 'expect' },
    ],
    bug: {
      class: 'silent-fail',
      title: t(
        'A file invitation to an external address is not delivered, even though Vault says "Invitation sent"',
        'Приглашение к файлу для внешнего адреса не доставляется, хотя Vault пишет «Приглашение отправлено»',
      ),
      expected: { text: t('Diego from Fabrikam gets the invitation to the file.', 'Марко из Fabrikam получает приглашение к файлу.'), source: 'speech' },
      actual: t(
        'Vault shows "Invitation sent" and adds diego@fabrikam.com to the list. At the same time, in the covered Relay - Contoso window, the Relay Bot chat jumps to the top with an unread message: "Couldn\'t send the invitation to diego@fabrikam.com: external invitations are turned off". The video author does not notice it; Diego has nothing.',
        'Vault показывает «Приглашение отправлено» и добавляет marko@fabrikam.com в список. Одновременно в перекрытом окне Relay - Contoso чат Relay Bot поднимается наверх с непрочитанным: «Не удалось отправить приглашение marko@fabrikam.com: внешние приглашения отключены». Автор видео это не замечает; у Марко ничего нет.',
      ),
      critical: ['invite', 'save', 'sent', 'bot-error', 'peer'],
      checks: [{ kind: 'unmentioned', at: 'bot-error' }, { kind: 'covered', at: 'bot-error' }],
      traps: [
        t(
          'the error is visible only in the sidebar of a window covered by the Vault window, and it is cut off with an ellipsis',
          'ошибка видна только в боковой панели окна, которое закрыто окном Vault, и обрезана многоточием',
        ),
        t('the "Invitation sent" toast contradicts the bot error', 'тост «Приглашение отправлено» противоречит ошибке бота'),
      ],
    },
    difficulty: { speech: 'explicit', signal: { kind: 'inline' }, windows: 3, occluded: true, distractors: [], attempts: 'once' },
    variants: [
      { id: 'clean', height: 1080, fps: 30, crf: 18, audio: 'clean' },
      { id: 'low', height: 720, fps: 15, crf: 32, audio: 'clean' },
    ],
  };
};
