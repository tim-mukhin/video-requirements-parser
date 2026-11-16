# OmniParser v2 для кликов по значкам

> Автор: Claude

Задача из плана (пункт 5): парсер читает текст через OCR, поэтому клик по кнопке без текста выходит как
`CLICK at [x, y]`. Проверяли, может ли OmniParser v2 (детектор интерактивных элементов + Florence-2, который
подписывает значки) дать дешёвый факт вида «нажат значок: clock / schedule», в первую очередь для B6, где автор говорит
«I click Send», а нажимает часы (schedule send).

**Итог: детектор полезен, подписи нет.** Детектор находит рамку нажатого элемента в 25 из 25 кликов по значкам.
Подпись называет действие правильно в 4 из 25 (16%), и все 4 это «Link» для скрепки. Часы в B6 подписаны как
«Number 0». Как отдельный проход парсера для имён значков OmniParser не годится.

## Установка

Всё лежит в `experiments/omniparser/`, тяжёлое закрыто локальным `.gitignore` (`OmniParser/`, `weights/`, `.venv/`,
`runs/`).

```sh
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python torch torchvision "transformers==4.45.2" "ultralytics==8.3.70" \
  einops timm pillow numpy opencv-python-headless "huggingface_hub<1"
uvx --from huggingface_hub hf download microsoft/OmniParser-v2.0 --local-dir weights
git clone --depth 1 https://github.com/microsoft/OmniParser.git   # только для справки по коду, не импортируется
HF_HOME=$PWD/weights/hf /usr/bin/lockf /tmp/dad-render.lock .venv/bin/python run.py --device mps --detector v8
.venv/bin/python summarize.py runs/results_v8_mps_64.json
```

Версии: torch 2.15.0, transformers 4.45.2, ultralytics 8.3.70. Код OmniParser не импортируется (его `util/utils.py`
тянет paddleocr и easyocr). `run.py` повторяет настройки из `weights/handler.py` и `util/utils.py`: детектор с conf 0.05,
iou 0.7 и imgsz равным размеру кадра; подпись строится по кропу рамки, сжатому до 64x64 с `do_resize=False`, prompt
`<CAPTION>`, `max_new_tokens=20`, greedy. Процессор и remote code Florence скачиваются с `microsoft/Florence-2-base` и
`-base-ft` (`trust_remote_code`, ревизия не закреплена: перед переносом в парсер закрепить `revision`).

Веса:

- `icon_detect` (YOLOv8): 40 МБ, **AGPL-3.0** (ultralytics тоже AGPL);
- `icon_detect_v3` (YOLOv9-E, TorchScript, появился в том же HF-репо): 268 МБ, MIT;
- `icon_caption` (Florence-2-base-ft, ~0.27B параметров, fp32): 1.08 ГБ, MIT;
- `.venv` на macOS: 1.1 ГБ.

## Что мерили

`run.py` берёт все клики из `out/en/*/parsed/evidence.json`. Эталон берётся из `truth/ui-states.json`: самый маленький
видимый элемент под точкой клика в состоянии экрана на момент `t - 1 ms`. У кнопок-значков `text` в эталоне содержит
действие («Attach file», «Send», «Schedule send»). Кадры двух видов:

- **before**: кадр экрана из парсера (`screens[].frame`), действующий до клика; курсор где-то на экране, но обычно не
  на значке;
- **at**: кадр из mp4 в момент клика, курсор стоит на значке.

Режимы:

- `full`: детектор на всём кадре, рамка под точкой клика (самая маленькая из содержащих точку, иначе ближайшая в
  пределах 12 px), подпись этой рамки;
- `cropdet`: кроп 200x200 вокруг клика, детектор на кропе (imgsz 640), подпись рамки;
- `cropcap`: подпись всего кропа 200x200 без детектора (Florence с обычным resize до 768).

Судья мягкий, по ключевым словам: attach = paperclip/clip/attach/link, schedule = clock/schedule/time/timer/alarm,
send = send/arrow/plane/submit/forward. Верно, если совпало только нужное действие.

Клики без текста: 42. Из них 25 это кнопки-значки (11 attach, 13 send, 1 schedule в B6), остальные 17 это строки
списков, миниатюры слайдов в M4 и заголовок окна, которые OCR не прочитал. Контроль: 12 случайных кликов с текстом.

## Числа

YOLOv8 (`icon_detect`), MPS, все 54 клика (`runs/results_v8_mps_64.json`), 25 кликов по значкам:

| режим | рамка найдена | подпись верна | неверна |
|---|---|---|---|
| full, before | 25 | 4 | 21 |
| full, at | 25 | 0 | 25 |
| cropdet, before | 9 | 1 | 8 |
| cropdet, at | 5 | 0 | 5 |
| cropcap, before | - | 1 (+8 смешанных) | 16 |
| cropcap, at | - | 2 (+5 смешанных) | 18 |

По действиям (full, before): attach 4 из 11 (все 4 это «Link»), send 0 из 13, schedule 0 из 1.

YOLOv9-E (`icon_detect_v3`, MIT), MPS (`runs/results_v3_mps_64.json`): рамка в 25 из 25 (before) и 24 из 25 (at),
подпись верна в 1 из 25: часы в B6 подписаны «Time Field». Кроп с детектором почти не работает (1 из 25).

CPU и MPS дают одинаковые подписи (проверено на одних и тех же кропах), разница только во времени.

### Примеры подписей

Подписи стабильные, но не про то:

- скрепка (attach, 11 кликов): «Hotel» 7 раз, «Link» 4 раза; с v3: «Ticket or Fill function.», «A thermometer or
  thermometer tool.», «Pills»;
- стрелка отправки (send, 13 кликов): «Navigation» 12 раз, «Navigation or direction.» 1 раз;
- часы в B6 (schedule send): «Number 0»; кроп с детектором: «Slow»; на кадре at: «Sign Up»; с v3: «Time Field»;
- кадр at (курсор на значке): «Recycle Bin», «Sign Up», «Travel Guide», «Share»; курсор перекрывает половину значка
  (`runs/b6_schedule_at.png`), так что брать нужно кадр before;
- кроп 200x200 целиком: Florence описывает сцену и читает текст рядом: «Sending it now with a clock mark showing
  10:40.», «A cursor pointing to the message.». Обе «верные» send в этом режиме случайны: слово «sending» пришло из
  текста сообщения в кропе;
- контроль с текстом: «Save» и «Share» читаются верно, имена файлов нет («Video Player», «The Complete Worksheet»).

Детектор ошибается и в рамке: для часов в B6 рамка смещена и захватывает пустое место слева (`runs/b6_schedule_before.png`).

Проверка, что дело не в установке: на скриншотах из самого репо (`OmniParser/imgs/teams.png`, `word.png`) подписи
местами верные («Settings», «More options», «Send», «Search function.», «Minimize», «Close», «Justified»,
«Numbering»), а местами такие же случайные («Vitamin B», «Capitol», «Power transformer», «Chinese People People»).
Captioner обучен на значках Office/Windows и шумит даже на них; линейные значки Relay (в стиле Lucide) для него чужие.

### Время

**Все замеры сняты при параллельной нагрузке других сессий** (рендер Remotion с Chrome и ffmpeg, симуляция flip2d,
процесс парсера на ~600% CPU). Числа ниже являются верхней оценкой и не годятся для точного сравнения; особенно
завышен CPU (3.6 с на один кроп 64x64 при 4.6 с на пачку из 51 кропа).

| что | MPS | CPU |
|---|---|---|
| детектор v8, кадр 1920x1080 | ~55 мс | ~1.0 с |
| детектор v3, кадр | ~0.4 с | ~2.2 с |
| подпись одной рамки (64x64) | ~110 мс | до 3.6 с |
| подпись кропа 200x200 (resize 768) | ~210 мс | до 5.6 с |
| OmniParser целиком: детектор + подписи всех 35-57 рамок кадра (v8) | 0.9-3.5 с | 6-8 с |
| то же с v3 (62-86 рамок) | 3.2-4.1 с | 4.3-5.9 с |

Для одного клика достаточно детектора и одной подписи: ~0.2 с на MPS. Проход «весь кадр с подписями всех значков» в
5-20 раз дороже и ничего не добавляет для задачи «что под кликом».

Кроп как дешёвая замена не работает: детектор на увеличенном кропе 200x200 теряет рамку (9 из 25 на before, 5 из 25 на
at), а подпись кропа без детектора описывает сцену, а не значок, и выходит дороже подписи рамки (768 против 64).

## Рекомендация

1. **Подписи Florence в парсер не добавлять.** 16% верных при мягком судье, B6 не ловится. Хуже того, подпись звучит
   уверенно («Hotel», «Navigation»), и агент поверит ложному факту.
2. **Детектор можно взять как проход для кликов без текста**, но только ради рамки: «клик по значку 50x24 в
   [835, 1015]» точнее, чем голая точка, и даёт кроп для следующего шага. YOLOv8 быстрый (~55 мс на MPS), но AGPL;
   если лицензия важна, v3 (MIT) находит те же рамки, но в 7 раз медленнее.
3. **Имя значка лучше получать иначе** (не проверено здесь, кандидаты):
   - кроп рамки (или 200x200 вокруг клика с кадра before) отдать локальной VLM, которую основная сессия уже
     поднимает для агента (qwen3-vl 8B), с вопросом «какой значок под точкой: скрепка, часы, стрелка отправки, ...».
     Это всего один вызов на клик без текста, их мало (0-9 на видео);
   - zero-shot CLIP/SigLIP по короткому словарю значков (paperclip, clock, paper plane, smiley, phone): дешевле VLM и
     без генерации текста;
   - без модели: детектор даёт соседние рамки, поэтому факт «нажат не крайний правый значок строки ввода, а второй
     справа» можно вывести геометрией. Для B6 это уже противоречие со словом «Send».

## Windows

Работает тем же стеком: у torch есть Windows wheels для CPU и CUDA, ultralytics и transformers написаны на чистом
Python, remote code Florence не требует flash_attn на transformers 4.45.2 (на macOS не потребовал). paddleocr и easyocr
из `requirements.txt` OmniParser не нужны, если брать только детектор и подписи.

- Диск: веса 1.1 ГБ (+0.27 ГБ, если v3), torch CPU ~1 ГБ в venv, torch CUDA ~3 ГБ.
- RAM: Florence в fp32 ~1.2 ГБ, YOLOv8 ~0.1 ГБ.
- Без NVIDIA только CPU: по замерам выше это секунды на клик (детектор ~1 с, подпись до 3.6 с). Для 0-9 кликов на
  видео терпимо, для «подписать весь кадр» нет.
- С NVIDIA: fp16 и `do_resize=False`, как в оригинальном коде; Microsoft заявляет 0.6 с на кадр целиком на A100 и
  0.8 с на 4090.

## Файлы

- `run.py`: сбор кликов и эталона, детектор (v8 или v3), подпись, режимы full/cropdet/cropcap, замер времени.
- `summarize.py`: сводка по `runs/results_*.json`.
- `runs/results_v8_mps_64.json`, `runs/results_v8_cpu_64.json`, `runs/results_v3_mps_64.json`,
  `runs/results_v3_cpu_64_lim.json` (6 кликов, только время): сырые результаты по каждому клику.
