import type { Deck, Scenario, Step } from '../synth/format/scenario.ts';
import type { Lang } from '../synth/i18n.ts';
import { tr } from '../synth/i18n.ts';
import { people, voice, WALLPAPER } from './common.ts';

const policyDeck = (lang: Lang): Deck => {
  const t = tr(lang);
  return {
    id: 'policy',
    file: t('External_Access_2027.pptx', 'Внешний_доступ_2027.pptx'),
    slides: [
      { id: 'cover', title: t('External access in 2027', 'Внешний доступ в 2027'), subtitle: t('What we change in the policy · working group', 'Что меняем в политике · рабочая группа') },
      {
        id: 'now',
        title: t('Where we are now', 'Как сейчас'),
        bullets: [
          t('Any employee can share a file with any organization', 'Любой сотрудник делится файлом с любой организацией'),
          t('Blocking only by a list of banned domains', 'Блокировка только по списку запрещённых доменов'),
          t('No log of external sends', 'Журнала внешних отправок нет'),
        ],
      },
      {
        id: 'incidents',
        title: t('Incidents this quarter', 'Инциденты за квартал'),
        table: {
          columns: [
            { id: 'month', label: t('Month', 'Месяц') },
            { id: 'sent', label: t('External sends', 'Внешних отправок') },
            { id: 'blocked', label: t('Blocked', 'Заблокировано') },
            { id: 'leaks', label: t('Leaks', 'Утечки') },
          ],
          rows: [
            [t('July', 'Июль'), t('1,240', '1 240'), '32', '1'],
            [t('August', 'Август'), t('1,385', '1 385'), '41', '0'],
            [t('September', 'Сентябрь'), t('1,502', '1 502'), '57', '2'],
          ],
        },
      },
      {
        id: 'options',
        title: t('Policy options', 'Варианты политики'),
        bullets: [
          t('A. An allowlist of organizations, sending to everyone else is closed', 'А. Список разрешённых организаций, остальным отправка закрыта'),
          t('B. A manager approves every external send', 'Б. Каждую внешнюю отправку подтверждает руководитель'),
          t('C. Sensitivity labels, rules decide automatically', 'В. Метки конфиденциальности, правила решают автоматически'),
        ],
      },
      {
        id: 'labels',
        title: t('Sensitivity labels', 'Метки конфиденциальности'),
        table: {
          columns: [
            { id: 'label', label: t('Label', 'Метка') },
            { id: 'who', label: t('Who can see it', 'Кто видит') },
            { id: 'external', label: t('Outside', 'Наружу') },
          ],
          rows: [
            [t('Public', 'Публичный'), t('everyone', 'все'), t('allowed', 'можно')],
            [t('Internal', 'Внутренний'), t('employees', 'сотрудники'), t('with approval', 'с подтверждением')],
            [t('Confidential', 'Конфиденциальный'), t('working group', 'рабочая группа'), t('not allowed', 'нельзя')],
          ],
        },
      },
      {
        id: 'rollout',
        title: t('Rollout plan', 'План внедрения'),
        bullets: [
          t('December: pilot in Finance', 'Декабрь: пилот в финансах'),
          t('January: external access log', 'Январь: журнал внешнего доступа'),
          t('February: all departments', 'Февраль: все подразделения'),
        ],
      },
      {
        id: 'open',
        title: t('Open questions', 'Открытые вопросы'),
        bullets: [
          t('Who maintains the allowlist of organizations?', 'Кто ведёт список разрешённых организаций?'),
          t('What do we do with files that were already sent?', 'Что делать с уже отправленными файлами?'),
        ],
      },
      { id: 'end', title: t('Thank you', 'Спасибо'), subtitle: t('Questions and decisions go into the minutes', 'Вопросы и решения - в протокол') },
    ],
  };
};

const next: Step = { act: { key: 'next', win: 'd' } };
const A = (say: string, name?: string): Step => ({ say, name });
const D = (say: string, name?: string): Step => ({ say, who: 'denis', name });
const O = (say: string, name?: string): Step => ({ say, who: 'oleg', name });
const R = (say: string, name?: string): Step => ({ say, who: 'roomb', name });

export const m3 = (lang: Lang): Scenario => {
  const t = tr(lang);
  const p = people(lang);
  const deck = policyDeck(lang);
  return {
    id: 'm3-meeting-long-room',
    lang,
    kind: 'meeting',
    title: t('A long meeting with a meeting room: choosing an external access policy', 'Длинная встреча с переговоркой: выбор политики внешнего доступа'),
    screen: { w: 1920, h: 1080 },
    wallpaper: WALLPAPER,
    recording: {
      layout: 'strip-top',
      title: t('Working group: external access', 'Рабочая группа: внешний доступ'),
      elapsed: 120,
      frame: { w: 1920, h: 1080 },
      tiles: [
        { id: 'artem', name: p.artem, kind: 'person', color: '#4f46e5' },
        { id: 'denis', name: p.denis, kind: 'person', color: '#0f766e' },
        { id: 'room4', name: t('Room 4', 'Переговорная 4'), kind: 'room', color: '#64748b', figures: 3 },
        { id: 'irina', name: p.irina, kind: 'person', color: '#b45309', muted: true },
        { id: 'lena', name: p.lena, kind: 'person', color: '#be185d', muted: true },
      ],
    },
    cast: [
      { id: 'artem', name: p.artem, voice: voice(lang, 'artem') },
      { id: 'denis', name: p.denis, voice: voice(lang, 'denis') },
      { id: 'oleg', name: p.oleg, voice: voice(lang, 'oleg'), tile: 'room4', introduced: true },
      { id: 'roomb', name: t('second person in the room', 'второй участник в переговорке'), voice: voice(lang, 'roomb'), tile: 'room4' },
    ],
    windows: [{ id: 'd', app: 'slides', title: `${deck.file} - Deck`, bbox: [0, 30, 1920, 1050], state: { deck: 'policy', slide: 0, mode: 'show' } }],
    decks: [deck],
    attachments: [
      { deck: 'policy', format: 'pptx' },
      { deck: 'policy', format: 'pdf' },
    ],
    steps: [
      A(
        t(
          'Hi everyone. Today is the external access working group, we need to pick a policy for next year.',
          'Всем привет. Сегодня рабочая группа по внешнему доступу, надо выбрать политику на следующий год.',
        ),
        'intro',
      ),
      A(t('Lukas, are you in the meeting room? Can we hear you?', 'Олег, вы в переговорке? Вас слышно?')),
      O(t("Yes, I can hear you, I'm here. This is Lukas from Security.", 'Да, слышу, я тут. Это Олег из безопасности.'), 'oleg-intro'),
      A(t("Great, let's get started.", 'Отлично, тогда начнём.')),
      next,
      A(t('Where we are now: any employee can share a file with any organization.', 'Как сейчас: любой сотрудник может поделиться файлом с любой организацией.'), 'now'),
      A(t('We only block by a list of banned domains, and we have no log of external sends.', 'Блокируем только по списку запрещённых доменов, и журнала внешних отправок у нас нет.')),
      D(t('By the way, nobody has updated that domain list since spring.', 'Список доменов, кстати, никто не обновлял с весны.'), 'stale-list'),
      next,
      A(t('Incidents this quarter. Sends keep growing, in September it was already fifteen hundred.', 'Инциденты за квартал. Отправок всё больше, в сентябре уже полторы тысячи.')),
      A(t('[In this column](point:d/slide/col:leaks) are the leaks: two in September.', '[Вот в этом столбце](point:d/slide/col:leaks) утечки: в сентябре две.'), 'leaks'),
      O(t('Both were confidential files, sent to a contractor by mistake.', 'Обе - конфиденциальные файлы, ушли подрядчику по ошибке.'), 'leaks-detail'),
      R(t("And the blocked ones, how much is that out of the total, about three percent?", 'А заблокированные - это сколько от всех, процента три?')),
      A(t('About three to four percent, yeah.', 'Примерно три-четыре процента, да.')),
      next,
      A(t("The main thing today: three policy options. Let's go one by one.", 'Главное на сегодня: три варианта политики. Давайте по очереди.'), 'options'),
      A(
        t(
          '[Option A](point:d/slide/b:0): an allowlist of organizations, sending to everyone else is closed.',
          '[Вариант А](point:d/slide/b:0): список разрешённых организаций, всем остальным отправка закрыта.',
        ),
      ),
      D(t("I like this one. It's clear, simple, and it shuts out contractors right away.", 'Мне этот нравится. Понятно, просто, и сразу закрывает подрядчиков.'), 'a-for'),
      O(
        t(
          "It won't fly. We have over three hundred partners, and new ones every week. The list will always be out of date.",
          'Не взлетит. У нас больше трёхсот партнёров, и каждую неделю новые. Список будет вечно устаревшим.',
        ),
        'a-against',
      ),
      D(t('Well, we could just put someone in charge of that list.', 'Ну, можно же поручить кому-то вести этот список.')),
      O(t("Who? Security can't handle it, and the business has no time.", 'Кому? Безопасность не потянет, у бизнеса нет времени.')),
      D(t("Is that three hundred including the ones we haven't worked with in a year?", 'Триста - это вместе с теми, с кем мы год не работали?')),
      O(t("Yes. Active ones are about a hundred and twenty. But that's still a lot.", 'Да. Активных где-то сто двадцать. Но всё равно много.'), 'active-partners'),
      R(t("Could we build the list automatically from contracts? There's a registry, right?", 'А можно собирать список автоматически из договоров? Есть же реестр.'), 'registry-ask'),
      O(t("The registry is incomplete, half the contracts are sitting in the lawyers' email.", 'Реестр неполный, половина договоров у юристов в почте.'), 'registry-no'),
      A(t("OK, that's a separate topic.", 'Ладно, это уже отдельная тема.')),
      A(
        t(
          "OK, let's put it aside. [Option B](point:d/slide/b:1): a manager approves every external send.",
          'Ладно, отложим. [Вариант Б](point:d/slide/b:1): каждую внешнюю отправку подтверждает руководитель.',
        ),
        'a-postpone',
      ),
      R(t("That's fifteen hundred approvals a month. Managers will scream.", 'Это же полторы тысячи подтверждений в месяц. Руководители взвоют.'), 'b-against'),
      D(t('What if they approve not every send, but once a day, in a batch?', 'А если подтверждать не каждую отправку, а раз в день, пачкой?'), 'batch-ask'),
      R(t("Then people will wait until the evening. That's bad too.", 'Тогда люди будут ждать до вечера. Тоже плохо.'), 'batch-no'),
      A(t('Agreed. We reject B, it would kill the speed of work.', 'Согласен. Б отклоняем, он убьёт скорость работы.'), 'b-reject'),
      D(t('I second that.', 'Поддерживаю.')),
      A(
        t(
          '[Option C](point:d/slide/b:2): sensitivity labels, and the system decides on its own what can be sent outside.',
          '[Вариант В](point:d/slide/b:2): метки конфиденциальности, и система сама решает, что можно отправлять наружу.',
        ),
      ),
      O(
        t(
          "We're for C. The labels are already in the office suite, we just need to turn them on and set up the rules.",
          'Мы за В. Метки и так есть в офисном пакете, их надо просто включить и настроить правила.',
        ),
        'c-for',
      ),
      R(
        t(
          "But will people set the labels correctly? Usually everyone just sets public so it doesn't get in the way.",
          'А люди будут правильно ставить метки? Обычно всё ставят «публичный», чтобы не мешало.',
        ),
        'c-concern',
      ),
      O(t("That's why the default label is internal, and you can only remove it with a comment.", 'Поэтому по умолчанию метка «внутренний», а снять её можно только с комментарием.'), 'default-internal'),
      A(t('Lukas, how long will it take to set up the labels?', 'Олег, а сколько времени уйдёт на настройку меток?')),
      O(t("About a month for the rules, plus training. Without training nobody will set the labels.", 'Где-то месяц на правила, плюс обучение. Без обучения метки никто ставить не будет.'), 'setup-time'),
      D(t('The training could be short videos, we did that with phishing.', 'Обучение можно короткими видео, мы так делали с фишингом.'), 'training'),
      A(t("OK, we'll discuss that later.", 'Хорошо, это потом обсудим.'), 'training-later'),
      A(t('OK. Then we decide: we go with option C, and the default label is internal.', 'Хорошо. Тогда решаем: берём вариант В, по умолчанию метка «внутренний».'), 'c-decide'),
      D(t('So we throw out the allowlist completely?', 'А список разрешённых организаций совсем выкидываем?')),
      O(t('We could keep it as an exception. For confidential files, for example, only vetted partners.', 'Можно оставить его как исключение. Для конфиденциальных файлов, например, только проверенные партнёры.'), 'a-exception'),
      A(t("That's interesting, but we're not deciding it yet. I'll write it down as a proposal.", 'Это интересно, но пока не решаем. Запишу как предложение.'), 'a-exception-defer'),
      D(t('Hey, go back to the incidents for a second. I want to look at July.', 'Слушай, вернись на секунду к инцидентам. Хочу посмотреть июль.'), 'back-ask'),
      { act: { key: 'prev', win: 'd' } },
      D(t('Right, one leak in July. What happened there?', 'Ага, в июле одна утечка. А что там было?')),
      O(t('That was a price list sent to the wrong partner. We revoked it afterwards.', 'Это прайс-лист, который отправили не тому партнёру. Мы его потом отозвали.'), 'july'),
      A(t('OK, going back.', 'Ладно, возвращаюсь.')),
      { act: { key: 'next', win: 'd' } },
      { wait: 1.2 },
      A(t("Anything else on the options? No? Let's move on.", 'Ещё что-то по вариантам? Нет? Идём дальше.')),
      next,
      A(
        t(
          'Labels. Public, allowed to everyone. Internal, outside with approval. Confidential, not allowed outside.',
          'Метки. Публичный - можно всем. Внутренний - наружу с подтверждением. Конфиденциальный - наружу нельзя.',
        ),
        'labels',
      ),
      R(t('Hold on, with approval is option B, the one we just rejected.', 'Подождите, «с подтверждением» - это же вариант Б, который мы только что отклонили.'), 'labels-conflict'),
      A(
        t(
          'Fair point. Then internal files go outside without approval, but every send goes into the log.',
          'Справедливо. Тогда для внутренних наружу без подтверждения, но каждая отправка попадает в журнал.',
        ),
        'internal-decide',
      ),
      O(
        t(
          "Yes, that's better. And for confidential, a ban with no exceptions until we decide on the partner list.",
          'Да, так лучше. И для конфиденциальных запрет без исключений, пока не решим со списком партнёров.',
        ),
        'conf-ok',
      ),
      next,
      A(
        t(
          'The plan: in December a pilot in Finance, in January the log, in February all departments.',
          'План: в декабре пилот в финансах, в январе журнал, в феврале все подразделения.',
        ),
        'rollout',
      ),
      D(t("We won't make December. Finance is closing the year, they have no time for pilots right now.", 'Декабрь не успеем. У финансов закрытие года, им сейчас не до пилотов.'), 'december-no'),
      A(t('Then we move the pilot to January, and launch the log together with it.', 'Тогда переносим пилот на январь, и журнал запускаем вместе с ним.'), 'pilot-move'),
      O(t('Agreed, the log is useless without the pilot anyway.', 'Согласен, журнал без пилота всё равно не нужен.')),
      R(t('Is the pilot just Finance, or Legal too?', 'А пилот только финансы или ещё юристы?')),
      A(t('Just Finance. Legal is in the second wave, in February.', 'Только финансы. Юристы во второй волне, в феврале.'), 'pilot-scope'),
      next,
      A(t('Open questions. Who maintains the allowlist of organizations, if we have one at all?', 'Открытые вопросы. Кто ведёт список разрешённых организаций, если он вообще будет?'), 'owner-q'),
      O(
        t(
          'I suggest the owner of the contract with the partner maintains it. But that has to be agreed with Legal.',
          'Предлагаю, чтобы вёл владелец договора с партнёром. Но это надо согласовать с юристами.',
        ),
        'owner-proposal',
      ),
      A(t('OK, that stays open.', 'Хорошо, это остаётся открытым.')),
      A(t('And the second one: what to do with files that have already gone outside.', 'И второй: что делать с файлами, которые уже ушли наружу.'), 'sent-q'),
      R(t('Maybe revoke access to everything confidential from the last ninety days?', 'Может, отозвать доступ ко всему конфиденциальному за последние девяносто дней?'), 'revoke-ask'),
      O(t("Technically we can, but we'll break work with contractors in the middle of projects.", 'Технически можно, но сломаем работу с подрядчиками посреди проектов.'), 'revoke-risk'),
      A(t("I'm writing it down as a proposal, we'll decide at the next meeting.", 'Записываю как предложение, решим на следующей встрече.'), 'revoke-defer'),
      next,
      A(
        t(
          'To sum up: option C with internal as the default label, we rejected B, the pilot is in January together with the log.',
          'Итого: вариант В с меткой «внутренний» по умолчанию, Б отклонили, пилот в январе вместе с журналом.',
        ),
        'summary',
      ),
      A(t("I'll send the minutes today. Thanks, everyone.", 'Протокол пришлю сегодня. Всем спасибо.')),
      D(t('Thanks, bye.', 'Спасибо, пока.')),
    ],
    requirements: [
      {
        id: 'REQ-01',
        text: t('The external access policy is built on sensitivity labels (option C).', 'Политика внешнего доступа строится на метках конфиденциальности (вариант В).'),
        status: 'decided',
        proposed_by: 'oleg',
        decided_by: 'artem',
        evidence: ['c-for', 'c-decide', 'summary'],
      },
      {
        id: 'REQ-02',
        text: t('The default label is "Internal".', 'Метка по умолчанию - «Внутренний».'),
        status: 'decided',
        proposed_by: 'oleg',
        decided_by: 'artem',
        evidence: ['default-internal', 'c-decide', 'summary'],
      },
      {
        id: 'REQ-03',
        text: t('The "Internal" label can only be removed with a comment.', 'Снять метку «Внутренний» можно только с комментарием.'),
        status: 'proposed',
        proposed_by: 'oleg',
        evidence: ['default-internal'],
      },
      {
        id: 'REQ-04',
        text: t('A manager approves every external send (option B).', 'Каждую внешнюю отправку подтверждает руководитель (вариант Б).'),
        status: 'rejected',
        decided_by: 'artem',
        evidence: ['b-against', 'b-reject', 'summary'],
      },
      {
        id: 'REQ-05',
        text: t('An allowlist of organizations as an exception for confidential files.', 'Список разрешённых организаций как исключение для конфиденциальных файлов.'),
        status: 'proposed',
        proposed_by: 'oleg',
        evidence: ['a-exception', 'a-exception-defer'],
      },
      {
        id: 'REQ-06',
        text: t(
          '"Internal" label: sent outside without approval, every send is written to the log (instead of "with approval" on the slide).',
          'Метка «Внутренний»: наружу без подтверждения, каждая отправка пишется в журнал (вместо «с подтверждением» на слайде).',
        ),
        status: 'decided',
        proposed_by: 'roomb',
        decided_by: 'artem',
        evidence: ['labels-conflict', 'internal-decide'],
      },
      { id: 'REQ-07', text: t('"Public" label: sending outside is allowed to everyone.', 'Метка «Публичный»: отправка наружу разрешена всем.'), status: 'stated', evidence: ['labels'] },
      {
        id: 'REQ-08',
        text: t(
          '"Confidential" label: sending outside is forbidden with no exceptions until there is a decision on the partner list.',
          'Метка «Конфиденциальный»: отправка наружу запрещена без исключений, пока нет решения по списку партнёров.',
        ),
        status: 'stated',
        evidence: ['labels', 'conf-ok'],
      },
      {
        id: 'REQ-09',
        text: t(
          'The Finance pilot moves from December to January, and the external access log launches together with the pilot.',
          'Пилот в финансах переносится с декабря на январь, журнал внешнего доступа запускается вместе с пилотом.',
        ),
        status: 'decided',
        proposed_by: 'denis',
        decided_by: 'artem',
        evidence: ['december-no', 'pilot-move', 'summary'],
      },
      {
        id: 'REQ-10',
        text: t(
          'Who maintains the allowlist of organizations (proposal: the contract owner, needs to be agreed with Legal).',
          'Кто ведёт список разрешённых организаций (предложение: владелец договора, нужно согласовать с юристами).',
        ),
        status: 'open_question',
        evidence: ['owner-q', 'owner-proposal'],
      },
      {
        id: 'REQ-11',
        text: t('Revoke access to all confidential files sent outside in the last 90 days.', 'Отозвать доступ ко всем конфиденциальным файлам, отправленным наружу за последние 90 дней.'),
        status: 'proposed',
        proposed_by: 'roomb',
        evidence: ['revoke-ask', 'revoke-risk', 'revoke-defer'],
      },
      {
        id: 'REQ-12',
        text: t('The pilot is Finance only, Legal is in the second wave in February.', 'Пилот только в финансах, юристы - во второй волне в феврале.'),
        status: 'stated',
        evidence: ['pilot-scope'],
      },
      {
        id: 'REQ-13',
        text: t('Approve external sends once a day in a batch.', 'Подтверждение внешних отправок раз в день пачкой.'),
        status: 'proposed',
        proposed_by: 'denis',
        evidence: ['batch-ask', 'batch-no'],
      },
      {
        id: 'REQ-14',
        text: t('Train users on labels with short videos.', 'Обучение пользователей меткам короткими видео.'),
        status: 'proposed',
        proposed_by: 'denis',
        evidence: ['setup-time', 'training', 'training-later'],
      },
    ],
    traps: [
      t(
        'Rahul asks to go back to the "Incidents this quarter" slide: it is shown a second time in the middle of the options discussion',
        'Денис просит вернуться к слайду «Инциденты»: он показан второй раз посреди обсуждения вариантов',
      ),
      t(
        'the contract registry as a source for the partner list is proposed and immediately rejected by Lukas, no decision',
        'реестр договоров как источник списка партнёров предложен и сразу отвергнут Олегом, решения нет',
      ),
      t(
        'two people speak from the meeting room (the tile shows three): Lukas introduced himself, the second did not - the reference has Person1, do not guess the name',
        'из переговорки говорят двое (на плитке трое): Олег представился, второй нет - в эталоне Person1, имя не угадывать',
      ),
      t('the "Room 4" tile lights up for both voices from the meeting room', 'плитка «Переговорная 4» подсвечивается для обоих голосов из переговорки'),
      t('the "Policy options" slide stays on screen for about two minutes without changes', 'слайд «Варианты политики» стоит на экране около двух минут без изменений'),
      t(
        'on the "Sensitivity labels" slide "Internal" says "with approval", the meeting decision is without approval, with the log',
        'на слайде «Метки» у «Внутреннего» написано «с подтверждением», решение встречи - без подтверждения, с журналом',
      ),
      t('on the "Rollout plan" slide the pilot is in December, the meeting decision is January', 'на слайде «План внедрения» пилот в декабре, решение встречи - январь'),
      t('option A is not explicitly rejected: "let\'s put it aside", then C is chosen', 'вариант А явно не отклонён: «отложим», потом выбран В'),
      t('Mei and Sara are in the meeting but stay silent', 'Ирина и Лена на встрече, но молчат'),
      t(
        'people in the recording do not need to be analyzed: the screen is a separate area of the frame',
        'людей в записи разбирать не нужно: экран - отдельная область кадра',
      ),
    ],
    difficulty: { speech: 'deictic', signal: { kind: 'none' }, windows: 1, occluded: false, distractors: [], attempts: 'once' },
    variants: [
      { id: 'clean', height: 1080, fps: 30, crf: 18, audio: 'clean' },
      { id: 'low', height: 720, fps: 15, crf: 32, audio: 'noise' },
    ],
  };
};
