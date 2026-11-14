import type { RelayFile, RelayMsg, RelayState } from '../synth/apps/relay/model.ts';
import type { VaultState } from '../synth/apps/vault/model.ts';
import type { Lang } from '../synth/i18n.ts';
import { tr } from '../synth/i18n.ts';

export const WALLPAPER = 'linear-gradient(135deg, #1e3a8a 0%, #6d28d9 55%, #db2777 100%)';

// voice ids in voices.local.json per language; the Russian set uses the author's own voice clone
const VOICES: Record<string, Record<Lang, string>> = {
  artem: { en: 'en_alex', ru: 'artem' },
  denis: { en: 'en_rahul', ru: 'denis' },
  oleg: { en: 'en_lukas', ru: 'oleg' },
  roomb: { en: 'en_roomb', ru: 'roomb' },
};
export const voice = (lang: Lang, who: keyof typeof VOICES) => VOICES[who][lang];

// people and names that appear on screen
export const people = (lang: Lang) => {
  const t = tr(lang);
  return {
    artem: t('Alex', 'Артём Мухин'),
    artemShort: t('Alex', 'Артём'),
    marko: t('Diego', 'Марко Петрович'),
    denis: t('Rahul', 'Денис Орлов'),
    irina: t('Mei', 'Ирина Сокол'),
    lena: t('Sara', 'Лена Ким'),
    lenaK: t('Nina', 'Лена Ковач'),
    oleg: t('Lukas', 'Олег'),
    ana: t('Aisha', 'Ана Йович'),
  };
};

// the English Q3 report has a non-ASCII name too, so the encoding bug (B3, R4) shows in both languages
export const files = (lang: Lang): RelayFile[] => {
  const t = tr(lang);
  return [
    { id: 'q3', name: t('Q3_Report_Zürich.pdf', 'Отчёт_Q3.pdf'), size: t('2.4 MB', '2,4 МБ'), kind: 'pdf' },
    { id: 'budget', name: t('Budget_2027.xlsx', 'Бюджет_2027.xlsx'), size: t('310 KB', '310 КБ'), kind: 'xlsx' },
    { id: 'contract', name: t('Supply_Agreement.docx', 'Договор_поставки.docx'), size: t('88 KB', '88 КБ'), kind: 'docx' },
    { id: 'shot', name: t('Screenshot 2026-11-14.png', 'Скриншот 2026-11-14.png'), size: t('1.1 MB', '1,1 МБ'), kind: 'png' },
  ];
};

const history = (lang: Lang, mineIsArtem: boolean): RelayMsg[] => {
  const t = tr(lang);
  const p = people(lang);
  return [
    { id: 'h1', mine: !mineIsArtem, author: p.marko, time: '10:38', text: t('Hi! Can you send me the Q3 report?', 'Привет! Скинешь отчёт по третьему кварталу?') },
    { id: 'h2', mine: mineIsArtem, author: p.artem, time: '10:40', text: t('Hi, sure, sending it now', 'Привет, да, сейчас пришлю') },
  ];
};

export const contoso = (lang: Lang): RelayState => {
  const t = tr(lang);
  const p = people(lang);
  return {
    org: 'Contoso',
    me: p.artem,
    active: 'marko',
    home: 'marko',
    chats: [
      { id: 'marko', title: p.marko, preview: t('Hi, sure, sending it now', 'Привет, да, сейчас пришлю'), initials: t('D', 'МП'), external: 'Fabrikam' },
      { id: 'dx', title: t('DX Team', 'Команда DX'), preview: t('Mei: release on Thursday', 'Ирина: релиз в четверг'), initials: 'DX', unread: 3 },
      { id: 'design', title: t('Design review', 'Дизайн-ревью'), preview: t('New mockups are in the folder', 'Новые макеты в папке'), initials: t('DR', 'ДР') },
      { id: 'all', title: t('Contoso: everyone', 'Contoso: все'), preview: t('Office closed on December 4', 'Офис закрыт 4 декабря'), initials: 'C' },
    ],
    threads: {
      marko: history(lang, true),
      dx: [
        { id: 'd1', mine: false, author: p.irina, time: '09:12', text: t("Release on Thursday, don't forget the checklist", 'Релиз в четверг, не забудьте про чеклист') },
        { id: 'd2', mine: false, author: p.denis, time: '09:40', text: t("OK, I'll take the test accounts", 'Ок, я за тестовые аккаунты') },
      ],
      design: [{ id: 'g1', mine: false, author: p.lena, time: t('yesterday', 'вчера'), text: t('New mockups are in the folder', 'Новые макеты в папке') }],
      all: [{ id: 'c1', mine: false, author: t('Office', 'Офис'), time: t('Mon', 'пн'), text: t('Office closed on December 4', 'Офис закрыт 4 декабря') }],
    },
    files: files(lang),
    picker: false,
    clock: '10:43',
  };
};

export const fabrikam = (lang: Lang): RelayState => {
  const t = tr(lang);
  const p = people(lang);
  return {
    org: 'Fabrikam',
    me: p.marko,
    active: 'artem',
    home: 'artem',
    chats: [
      { id: 'artem', title: p.artem, preview: t('Hi, sure, sending it now', 'Привет, да, сейчас пришлю'), initials: t('A', 'АМ'), external: 'Contoso' },
      { id: 'ops', title: 'Fabrikam Ops', preview: t('On-call rota for the week', 'Дежурство на неделю'), initials: 'FO' },
      { id: 'lena', title: p.lenaK, preview: t("OK, let's call", 'Ок, созвонимся'), initials: t('N', 'ЛК') },
    ],
    threads: { artem: history(lang, false), ops: [], lena: [] },
    files: [],
    picker: false,
    clock: '10:43',
  };
};

// UTF-8 bytes read as Windows-1252: this is how a broken non-ASCII file name looks
const CP1252: Record<number, string> = {
  0x80: '€', 0x82: '‚', 0x83: 'ƒ', 0x84: '„', 0x85: '…', 0x86: '†', 0x87: '‡', 0x88: 'ˆ', 0x89: '‰', 0x8a: 'Š', 0x8b: '‹', 0x8c: 'Œ', 0x8e: 'Ž',
  0x91: '‘', 0x92: '’', 0x93: '“', 0x94: '”', 0x95: '•', 0x96: '–', 0x97: '—', 0x98: '˜', 0x99: '™', 0x9a: 'š', 0x9b: '›', 0x9c: 'œ', 0x9e: 'ž', 0x9f: 'Ÿ',
};
export const mojibake = (s: string) => [...new TextEncoder().encode(s)].map((b) => (b < 0x80 || b > 0x9f ? String.fromCharCode(b) : CP1252[b] ?? '?')).join('');

export const vaultContoso = (lang: Lang): VaultState => {
  const t = tr(lang);
  const p = people(lang);
  const f = files(lang);
  return {
    org: 'Contoso',
    me: p.artem,
    path: [t('My Drive', 'Мой диск'), t('Finance', 'Финансы')],
    files: [
      { id: 'archive', name: t('Archive 2025', 'Архив 2025'), kind: 'folder', owner: t('me', 'я'), modified: t('Oct 3', '3 окт.'), size: '-' },
      { id: 'q3', name: f[0].name, kind: 'pdf', owner: t('me', 'я'), modified: '10:21', size: f[0].size },
      { id: 'budget', name: f[1].name, kind: 'xlsx', owner: p.irina, modified: t('yesterday', 'вчера'), size: f[1].size },
      { id: 'contract', name: f[2].name, kind: 'docx', owner: t('me', 'я'), modified: t('Nov 11', '11 нояб.'), size: f[2].size },
      { id: 'shot', name: f[3].name, kind: 'png', owner: t('me', 'я'), modified: '09:58', size: f[3].size },
    ],
    links: { budget: 'org' },
    people: {
      q3: [{ name: p.artem, email: t('alex@contoso.com', 'artem@contoso.com'), role: 'owner' }],
      budget: [
        { name: p.irina, email: t('mei@contoso.com', 'irina@contoso.com'), role: 'owner' },
        { name: p.artem, email: t('alex@contoso.com', 'artem@contoso.com'), role: 'editor' },
      ],
    },
    clock: '10:43',
  };
};
