import type { Deck, Scenario, Slide } from '../synth/format/scenario.ts';
import type { Lang } from '../synth/i18n.ts';
import { tr } from '../synth/i18n.ts';
import { people, voice, WALLPAPER } from './common.ts';

const screen = (lang: Lang): Slide => {
  const t = tr(lang);
  const p = people(lang);
  const delivered = t('Delivered', 'Доставлен');
  return {
    id: 'screen',
    title: t('Log screen (draft)', 'Экран журнала (черновик)'),
    table: {
      columns: [
        { id: 'file', label: t('File', 'Файл') },
        { id: 'recipient', label: t('Recipient', 'Получатель') },
        { id: 'org', label: t('Organization', 'Организация') },
        { id: 'status', label: t('Status', 'Статус') },
      ],
      rows: [
        [t('Q3_Report.pdf', 'Отчёт_Q3.pdf'), p.marko, 'Fabrikam', t('Blocked by policy', 'Заблокирован политикой')],
        [t('Budget_2027.xlsx', 'Бюджет_2027.xlsx'), p.marko, 'Fabrikam', delivered],
        [t('Supply_Agreement.docx', 'Договор_поставки.docx'), p.ana, 'Northwind', t('Not delivered', 'Не доставлен')],
        [t('Screenshot.png', 'Скриншот.png'), p.lenaK, 'Fabrikam', delivered],
      ],
    },
  };
};

// the slide in the old version of the deck: no "Status" column yet
export const screenOld = (lang: Lang): Slide => {
  const s = screen(lang);
  return { ...s, table: { columns: s.table!.columns.slice(0, 3), rows: s.table!.rows.map((r) => r.slice(0, 3)) } };
};

export const deck = (lang: Lang): Deck => {
  const t = tr(lang);
  return {
    id: 'deck',
    file: t('External_Access_Log.pptx', 'Журнал_внешнего_доступа.pptx'),
    slides: [
      { id: 'cover', title: t('External Access Log', 'Журнал внешнего доступа'), subtitle: t('Requirements review · November 14', 'Ревью требований · 14 ноября') },
      {
        id: 'why',
        title: t('Why', 'Зачем'),
        bullets: [
          t("Admins can't see which files went to other organizations", 'Администраторы не видят, какие файлы ушли в другие организации'),
          t('Complaints: a file is “sent”, but the recipient doesn’t see it', 'Жалобы: файл «отправлен», но получатель его не видит'),
          t('We need one screen instead of digging through logs', 'Нужен один экран вместо поиска по логам'),
        ],
      },
      screen(lang),
      {
        id: 'filters',
        title: t('Filters', 'Фильтры'),
        bullets: [t('By recipient organization', 'По организации-получателю'), t('By delivery status', 'По статусу доставки'), t('By time period', 'По периоду')],
      },
      {
        id: 'open',
        title: t('Open questions', 'Открытые вопросы'),
        bullets: [
          t('How long do we keep the log: 90 days or a year?', 'Сколько хранить журнал: 90 дней или год?'),
          t('Should the admin see the file contents?', 'Показывать ли администратору содержимое файла?'),
        ],
      },
      {
        id: 'next',
        title: t('Next steps', 'Следующие шаги'),
        bullets: [
          t('Update the screen mockup', 'Обновить макет экрана'),
          t('Agree on retention with Security', 'Согласовать хранение с безопасностью'),
          t('Next review on November 21', 'Следующее ревью 21 ноября'),
        ],
      },
    ],
  };
};

const next = { act: { key: 'next', win: 'm' } } as const;
const prev = { act: { key: 'prev', win: 'm' } } as const;

export const m1 = (lang: Lang): Scenario => {
  const t = tr(lang);
  const p = people(lang);
  return {
    id: 'm1-meeting-requirements',
    lang,
    kind: 'meeting',
    title: t('Meeting: requirements for the external access log', 'Встреча: требования к журналу внешнего доступа'),
    screen: { w: 1920, h: 1080 },
    wallpaper: WALLPAPER,
    cast: [
      { id: 'artem', name: p.artem, voice: voice(lang, 'artem') },
      { id: 'denis', name: p.denis, voice: voice(lang, 'denis') },
    ],
    windows: [
      {
        id: 'm',
        app: 'meet',
        title: t('Relay Meet - Requirements review', 'Relay Meet - Ревью требований'),
        bbox: [0, 30, 1920, 1050],
        state: {
          title: t('Requirements review: external access log', 'Ревью требований: журнал внешнего доступа'),
          org: 'Contoso',
          deck: 'deck',
          slide: 0,
          presenter: 'artem',
          elapsed: 754,
          people: [
            { id: 'artem', name: p.artem, initials: t('A', 'АМ'), color: '#4f46e5' },
            { id: 'denis', name: p.denis, initials: t('R', 'ДО'), color: '#0f766e' },
            { id: 'irina', name: p.irina, initials: t('M', 'ИС'), color: '#b45309', muted: true },
            { id: 'lena', name: p.lena, initials: t('S', 'ЛК'), color: '#be185d', muted: true },
          ],
        },
      },
    ],
    decks: [deck(lang)],
    attachments: [
      { deck: 'deck', format: 'pptx' },
      { deck: 'deck', format: 'pdf' },
    ],
    steps: [
      { say: t("Hi everyone. Today we're going over the requirements for the external access log.", 'Коллеги, привет. Сегодня смотрим требования к журналу внешнего доступа.'), name: 'intro' },
      next,
      { say: t("The problem is simple: admins can't see which files went out to other organizations.", 'Проблема простая: администраторы не видят, какие файлы ушли в другие организации.'), name: 'problem' },
      { say: t("And there are complaints: a file was sent, but the recipient can't see it or can't open it.", 'И есть жалобы: файл отправлен, а получатель его не видит или не может открыть.') },
      { say: t('Yeah, we had three tickets like that last week.', 'Да, у нас на прошлой неделе было три таких обращения.'), who: 'denis', name: 'tickets' },
      next,
      { say: t("Here's a draft of the screen. Each row is one file that went outside.", 'Вот черновик экрана. Каждая строка - один файл, который ушёл наружу.'), name: 'screen' },
      {
        say: t(
          '[In this column](point:m/slide/col:status) we show the status: delivered, blocked by policy, or not delivered.',
          '[Вот в этом столбце](point:m/slide/col:status) показываем статус: доставлен, заблокирован политикой или не доставлен.',
        ),
        name: 'status',
      },
      {
        say: t('Can we add the date [here as well](ref:m/slide/col:status)? When the status changed.', 'А можно [сюда же](ref:m/slide/col:status) добавить дату? Когда статус поменялся.'),
        who: 'denis',
        name: 'date-ask',
      },
      { say: t("Yeah, makes sense. But as a separate column, next to the status. I'm writing it down.", 'Да, логично. Только отдельным столбцом, рядом со статусом. Записываю.'), name: 'date-ok' },
      {
        say: t(
          "And one more thing. Maybe [here](point:m/slide/col:recipient) we show only the organization, without the recipient's name?",
          'И ещё. Может, [здесь](point:m/slide/col:recipient) показывать только организацию, без имени получателя?',
        ),
        who: 'denis',
        name: 'hide-ask',
      },
      { say: t("Not sure. Security might push back, let's discuss that separately.", 'Не уверен. Безопасники могут быть против, давай это отдельно обсудим.'), name: 'hide-defer' },
      next,
      { say: t('Filters: by organization, by status, and by time period.', 'Фильтры: по организации, по статусу и по периоду.'), name: 'filters' },
      { say: t("The period is a must. Otherwise a year's worth of log just won't open.", 'Период обязательно. Иначе журнал за год просто не откроется.'), who: 'denis', name: 'period' },
      prev,
      prev,
      {
        say: t(
          'Let me go back for a second. [This complaint here](point:m/slide/b:1) is exactly the bug we went through yesterday.',
          'Вернусь на секунду назад. [Вот эта](point:m/slide/b:1) жалоба - ровно тот баг, который мы вчера разбирали.',
        ),
        name: 'back',
      },
      next,
      next,
      next,
      {
        say: t('Open questions: how long to keep the log, and whether to show the admin the file contents.', 'Открытые вопросы: сколько хранить журнал и показывать ли администратору содержимое файла.'),
        name: 'open',
      },
      { say: t('On retention: ninety days is too little, the auditors are asking for a year.', 'По хранению: девяносто дней мало, аудиторы просят год.'), who: 'denis', name: 'retention' },
      {
        say: t("OK, I'm writing that down as an open question too, we'll settle it with Security.", 'Хорошо, это тоже записываю как открытый вопрос, решим с безопасниками.'),
        name: 'retention-open',
      },
      next,
      {
        say: t("So: we're adding the date column, everything else we'll discuss separately. Thanks, everyone.", 'Итого: столбец с датой добавляем, остальное обсудим отдельно. Спасибо всем.'),
        name: 'summary',
      },
    ],
    requirements: [
      {
        id: 'REQ-01',
        text: t(
          'The log shows one row per file sent to an external organization: file, recipient, organization.',
          'Журнал показывает по строке на каждый файл, отправленный во внешнюю организацию: файл, получатель, организация.',
        ),
        status: 'stated',
        evidence: ['screen'],
      },
      { id: 'REQ-02', text: t('A "Status" column: delivered, blocked by policy, or not delivered.', 'Столбец «Статус»: доставлен, заблокирован политикой или не доставлен.'), status: 'stated', evidence: ['status'] },
      {
        id: 'REQ-03',
        text: t('A separate column with the date of the status change, next to the "Status" column.', 'Отдельный столбец с датой смены статуса рядом со столбцом «Статус».'),
        status: 'decided',
        proposed_by: 'denis',
        decided_by: 'artem',
        evidence: ['date-ask', 'date-ok', 'summary'],
      },
      {
        id: 'REQ-04',
        text: t("Show only the recipient's organization, without the name.", 'Показывать только организацию получателя, без имени.'),
        status: 'proposed',
        proposed_by: 'denis',
        evidence: ['hide-ask', 'hide-defer'],
      },
      {
        id: 'REQ-05',
        text: t(
          'Filters by recipient organization, delivery status, and time period; the time period filter is mandatory.',
          'Фильтры по организации-получателю, статусу доставки и периоду; фильтр по периоду обязателен.',
        ),
        status: 'stated',
        evidence: ['filters', 'period'],
      },
      {
        id: 'REQ-06',
        text: t('Log retention period: 90 days or a year.', 'Срок хранения журнала: 90 дней или год.'),
        status: 'open_question',
        proposed_by: 'denis',
        evidence: ['open', 'retention', 'retention-open'],
      },
      { id: 'REQ-07', text: t('Whether to show the admin the file contents.', 'Показывать ли администратору содержимое файла.'), status: 'open_question', evidence: ['open'] },
    ],
    traps: [
      t(
        'going back to the second slide: the slide was already shown, it must be recognized, not counted as new',
        'возврат ко второму слайду: слайд уже был показан, его надо узнать, а не считать новым',
      ),
      t(
        '"here as well" in Rahul\'s line is the "Status" column Alex pointed at before; the cursor does not move at that moment',
        '«сюда же» в реплике Дениса - столбец «Статус», на который до этого указал Артём; курсор в этот момент не двигается',
      ),
      t('Mei and Sara are in the meeting but stay silent', 'Ирина и Лена на встрече, но молчат'),
      t(
        'REQ-04 is a proposal without a decision, REQ-03 is a decision: "I\'m writing it down" and the summary',
        'REQ-04 - предложение без решения, REQ-03 - решение: «записываю» и итог',
      ),
    ],
    difficulty: { speech: 'deictic', signal: { kind: 'none' }, windows: 1, occluded: false, distractors: [], attempts: 'once' },
    variants: [
      { id: 'clean', height: 1080, fps: 30, crf: 18, audio: 'clean' },
      { id: 'low', height: 720, fps: 15, crf: 32, audio: 'noise' },
    ],
  };
};
