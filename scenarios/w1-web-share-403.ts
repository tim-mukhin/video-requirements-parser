import type { Scenario } from '../synth/format/scenario.ts';
import type { Lang } from '../synth/i18n.ts';
import { tr } from '../synth/i18n.ts';
import { people, vaultContoso, voice, WALLPAPER } from './common.ts';

export const w1 = (lang: Lang): Scenario => {
  const t = tr(lang);
  const p = people(lang);
  const tab = t('Finance - Vault', 'Финансы - Vault');
  return {
    id: 'w1-web-share-403',
    lang,
    kind: 'bug-repro',
    title: t(
      'Vault in the browser: "saved", but DevTools shows a 403 on saving access',
      'Vault в браузере: «сохранено», а в DevTools 403 на сохранение доступа',
    ),
    screen: { w: 1920, h: 1080 },
    wallpaper: WALLPAPER,
    cast: [{ id: 'artem', name: p.artemShort, voice: voice(lang, 'artem') }],
    windows: [
      {
        id: 'v',
        app: 'vault',
        title: tab,
        bbox: [40, 44, 1840, 1020],
        browser: { url: 'vault.contoso.com/drive/finance', tab, group: 'g' },
        state: vaultContoso(lang),
      },
    ],
    steps: [
      { sys: 'v', op: { console: { level: 'info', text: 'Vault web 4.12.0 (build 2026.11.13)' } }, delay: 0 },
      { sys: 'v', op: { console: { level: 'warn', text: '[Deprecation] Listener added for a synchronous DOMNodeInserted event' } }, delay: 0 },
      { sys: 'v', op: { network: { method: 'GET', url: '/api/drive/finance/files', status: 200, ms: 84 } }, delay: 0 },
      { sys: 'v', op: { devtools: 'console' }, delay: 0 },
      {
        say: t(
          "Link sharing doesn't save in the web version either. I'll show it on the report.",
          'Доступ по ссылке в веб-версии тоже не сохраняется. Показываю на отчёте.',
        ),
      },
      { act: { click: 'v/row:q3' } },
      { say: t('[Share](click:v/share), [access mode](click:v/mode).', '[Поделиться](click:v/share), [режим](click:v/mode).') },
      { act: { click: 'v/mode:anyone' }, name: 'pick' },
      { say: t('Anyone with the link, and I [save](click:v/save#save).', 'Все, у кого есть ссылка, и [сохраняю](click:v/save#save).') },
      { sys: 'v', op: { network: { method: 'PATCH', url: '/api/files/q3/sharing', status: 403, ms: 212 } }, at: 'save', delay: 0.3, name: 'patch-403' },
      {
        sys: 'v',
        op: { console: { level: 'error', text: 'PATCH https://vault.contoso.com/api/files/q3/sharing 403 (Forbidden): tenant policy blocks anonymous links' } },
        at: 'save',
        delay: 0.35,
        name: 'console-403',
      },
      { sys: 'v', op: { toast: { text: t('Sharing settings saved', 'Настройки доступа сохранены'), tone: 'info' } }, at: 'save', delay: 0.5, ms: 2500, name: 'saved' },
      { sys: 'v', op: { link: { file: 'q3', mode: 'restricted' } }, at: 'save', delay: 1.2, name: 'revert' },
      { wait: 1.5 },
      { say: t('It says "saved". I open it [again](click:v/share#reopen).', 'Пишет «сохранено». Открываю [снова](click:v/share#reopen).') },
      { say: t("And it's back to restricted again.", 'А там опять только приглашённые.'), name: 'seen' },
      { act: { click: 'v/cancel' } },
    ],
    bug: {
      class: 'state-revert',
      title: t(
        'Web Vault shows "saved" even though the request to save access returned 403',
        'Веб-Vault показывает «сохранено», хотя запрос сохранения доступа вернул 403',
      ),
      expected: {
        text: t(
          'The "Anyone with the link" mode is saved, or the interface shows an error.',
          'Режим «Все, у кого есть ссылка» сохраняется, либо интерфейс показывает ошибку.',
        ),
        source: 'implied',
      },
      actual: t(
        'PATCH /api/files/q3/sharing returns 403 (tenant policy blocks anonymous links), with an error in the console. Meanwhile the interface shows a "Sharing settings saved" toast, and the mode goes back to "Restricted".',
        'PATCH /api/files/q3/sharing возвращает 403 (tenant policy blocks anonymous links), в консоли ошибка. Интерфейс при этом показывает тост «Настройки доступа сохранены», режим возвращается на «Только приглашённые».',
      ),
      critical: ['save', 'patch-403', 'console-403', 'saved', 'reopen'],
      traps: [
        t(
          'the cause is visible only in the open DevTools panel at the bottom of the window, the speech never mentions it',
          'причина видна только в открытой панели DevTools внизу окна, голосом о ней не говорится',
        ),
        t('the Deprecation warning in the console is unrelated to the bug', 'предупреждение Deprecation в консоли к багу не относится'),
      ],
    },
    difficulty: { speech: 'deictic', signal: { kind: 'inline' }, windows: 1, occluded: false, distractors: [], attempts: 'once' },
    variants: [
      { id: 'clean', height: 1080, fps: 30, crf: 18, audio: 'clean' },
      { id: 'low', height: 720, fps: 15, crf: 32, audio: 'clean' },
    ],
  };
};
