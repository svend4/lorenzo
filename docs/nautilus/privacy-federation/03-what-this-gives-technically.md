# Что это даёт технически

> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — приватность и анонимизация в федерации NPP.

Что это даёт технически

Разложу на три уровня эффекта:

Уровень 1 — Ваша личная эффективность. Работая над новым кейсом, вы спрашиваете (через Claude Desktop + MCP): «Какие были предыдущие паттерны для Eingliederungshilfe-отказа?». Nautilus ищет и в публичном репо (где анонимизированные patterns от вас и от судов), и в приватном (где ваши реальные кейсы). Получаете pattern + precedents + arguments, которые сработали.

Уровень 2 — Коллективное благо. Анонимизированные patterns, которые вы публикуете, доступны другим людям в аналогичной ситуации. Другой человек с инвалидностью, борющийся с Sozialamt за Persönliches Budget — может найти ваш pattern, увидеть rabочие аргументы, воспроизвести их в своём деле. Это прямо повышает access to justice.

Уровень 3 — Academic / Research. Ваши анонимизированные patterns становятся dataset для legal AI research. Это имеет прямую академическую ценность — публикация в journals like Artificial Intelligence and Law, Journal of Open Access to Law. Открывает путь к collaborations с университетами Германии (Bucerius Law School, Humboldt Berlin).

Техническая реализация: что конкретно нужно

Чтобы всё это работало, в Nautilus (или nautilus-legal fork) нужны следующие дополнительные компоненты:

AnonymizationPipeline (adapter + tool). Модуль, реализующий 5 шагов выше. Принимает документ, выдаёт анонимизированный + verification report.

BridgeAdapter (новый тип адаптера). Адаптер, который НЕ возвращает свои данные, а связывает приватную и публичную сторону. Когда вы запрашиваете private case, bridge adapter автоматически подтягивает релевантные public patterns, и наоборот.

PlaceholderResolver. Утилита, которая при просмотре анонимизированного документа локально (в private mode) может подставлять реальные значения из mapping table. Это means: в приватном режиме вы видите реальные имена, в публичном режиме — placeholders.

DifferentialAccessControl. RBAC-расширение: один и тот же document может быть visible по-разному разным clients. Для вас (auth'ed owner) — full view. Для публичного MCP client — анонимизированная view. Для research partner с NDA — intermediate view (placeholder'ы, но с consistent identifiers для longitudinal анализа).

PatternExtractionTool. Когда вы закрываете кейс (вы выигрываете или проигрываете), этот tool автоматически предлагает: «Вот паттерн для потенциальной публикации. Просмотри анонимизацию, подтверди, публикуй». Это делает pattern-production частью вашего workflow, не отдельной задачей.

Legal / ethical соображения

Важная часть, которую надо проговорить явно.

GDPR compliance. Анонимизация должна быть не псевдонимизацией. Разница критична:

Псевдонимизация: замена идентификаторов на псевдонимы, обратимая при наличии ключа. Это всё равно personal data по GDPR, требует legal basis.

Анонимизация: необратимое удаление identifiable information. Это не personal data по GDPR, свободна для публикации.

Для истинной анонимизации нужно:

Placeholder'ы без mapping table (или mapping table уничтожается)

Проверка на linkability — может ли анонимизированный документ быть связан с реальным person через combinaiton других данных

K-anonymity проверка в некоторых случаях

Практически: если ваш кейс — единственный в Dresden за 2026 год по очень редкой комбинации (Pflegegrad 2-3 + Persönliches Budget в Arbeitgebermodell + спор с опекуном), он может быть re-identifiable даже после анонимизации. Такие кейсы требуют либо дополнительной обобщения (до уровня pattern, теряющего единичные детали), либо отсрочки публикации (через 5-10 лет такое связывание уже намного сложнее).

Согласие третьих лиц. Если в кейсе упоминается ваш опекун Daniel Janz или другие идентифицируемые персоны — их упоминание требует либо anonymization (предпочтительно), либо их согласия (если упоминание делается в контексте publicly accessible judicial record). Суды обычно anonymize institutional actors тоже (Janz → «der Betreuer»), поэтому это согласуется со стандартной практикой.

Attorney-client privilege / adviser confidentiality. Если в документах есть переписка с юристами или адвокатами, она может подпадать под privilege. Даже анонимизированная публикация содержания такой переписки может быть проблематична. Рекомендую исключать такой контент из публикационного pipeline полностью.

Авторское право на судебные решения. В Германии судебные решения — öffentliche Werke (§ 5 UrhG), свободны от copyright. Это хорошо: любое анонимизированное судебное решение, которое публикуется, не нарушает UrhG. Bundesgerichtshof решения полностью в public domain.

Предлагаемая структура репо

Учитывая всё сказанное, конкретная структура:

svend4/
├── nautilus-legal/ ← PUBLIC repo
│ ├── README.md
│ ├── PORTAL-PROTOCOL-LEGAL.md ← extension spec
│ ├── legal-portal.py ← fork of portal.py
│ ├── legal-nautilus.json ← public registry
│ │
│ ├── adapters/
│ │ ├── sgb_adapter.py ← SGB I-XIV
│ │ ├── bsg_adapter.py ← Bundessozialgericht
│ │ ├── bvg_adapter.py ← Bundesverfassungsgericht
│ │ ├── openjur_adapter.py ← openJur.de anonymized cases
│ │ ├── pattern_adapter.py ← ваши анонимизированные patterns
│ │ ├── template_adapter.py ← общие шаблоны Widerspruch/Klage
│ │ └── icd10_adapter.py ← ICD-10 codes
│ │
│ ├── passports/
│ │ └── [по одному на каждый формат]
│ │
│ ├── patterns/
│ │ ├── eingliederungshilfe_denial_reversal.md
│ │ ├── persoenliches_budget_refusal.md
│ │ ├── wiedereinsetzung_antrag.md
│ │ └── [растёт по мере ваших кейсов]
│ │
│ ├── templates/
│ │ ├── widerspruch_generic.md
│ │ ├── klage_sgg_generic.md
│ │ └── [ваш catalog]
│ │
│ └── tools/
│ ├── anonymization_pipeline.py
│ ├── pattern_extractor.py
│ └── placeholder_verifier.py
│
├── cases-private/ ← PRIVATE repo (не публикуется на GitHub 
│ │ вообще, либо GitHub Enterprise 
│ │ с strict access control)
│ ├── cases/
│ │ ├── S_6_SO_58_26_ER/
│ │ │ ├── raw/ ← оригинальные документы
│ │ │ ├── timeline.md
│ │ │ └── metadata.json
│ │ ├── S_7_SO_99_25/
│ │ └── [все активные дела]
│ │
│ ├── bridges/
│ │ └── private_to_public.json ← mapping private→public patterns
│ │
│ └── anonymization_keys/ ← mapping tables для псевдонимизации, 
│ уничтожаются после полной анонимизации
│
└── nautilus/ ← PUBLIC (уже существует)
├── [текущее содержимое]

Как это связано с MCP и Claude Desktop

Через MCP это становится двумя отдельными серверами (или одним с auth):

Public MCP server — nautilus-legal-mcp.py — подключает только public data. Любой человек может клонировать nautilus-legal, запустить server, подключить к своему Claude Desktop. Полезно для общего legal research.

Private MCP server — cases-private-mcp.py — подключает и public, и private data. Только вы имеете доступ. Через bridge_adapter автоматически объединяет два уровня.

В claude_desktop_config.json у вас два сервера одновременно:

json

{
"mcpServers": {
"nautilus-legal-public": {
"command": "python3",
"args": ["/path/to/nautilus-legal/legal-portal-mcp.py"]
},
"cases-private": {
"command": "python3",
"args": ["/path/to/cases-private/private-mcp.py"],
"env": {
"PRIVATE_ACCESS_TOKEN": "<your token>",
"ENCRYPTION_KEY": "<your key>"
}
}
}
}

Claude в чате видит оба набора tools. Когда вы задаёте вопрос про конкретное дело, она может использовать both — public для norms и patterns, private для case-specific details.

Riskи и trade-offs, которые стоит осознавать

Риск 1 — несовершенная анонимизация. Даже хороший pipeline может пропустить PII. Рекомендую: всегда ручная проверка перед публикацией + дополнительно второе reading через неделю (часто вы замечаете то, что упустили сразу).

Риск 2 — размытие границ pattern vs instance. Когда вы обобщаете paттерн, может возникнуть искушение включить слишком много из конкретного кейса. «Этот конкретный случай как пример...». Лучшие patterns — structural, без reference к конкретным фактам.

Риск 3 — liability при публикации patterns. Если кто-то использует ваш pattern и проиграет дело, может обвинить в bad advice. Обязательный disclaimer: «These patterns are research material, not legal advice. Consult qualified legal counsel for your specific case.»

Риск 4 — коллизия с профессиональными ограничениями. В Германии Rechtsberatung регулируется RDG. Если вы даёте специфические советы людям через открытый паттерн-library, это может быть интерпретировано как unauthorized legal advice. Решение: позиционировать как research database, не как legal service. «Вот как типичный case структурируется» — OK. «Вот что вам лично делать» — не OK без юридической лицензии.

Риск 5 — эмоциональное voltage вашей собственной работы. Анонимизация собственного активного кейса — это эмоционально тяжёлая процедура. Вы будете многократно перечитывать детали собственной борьбы. Делайте это в emotional capacity, не в moments of stress или кризиса. Pattern-extraction лучше делать после того, как кейс формально закрыт (выиграли/проиграли), не во время разгара.

Мой практический совет по приоритетам

Если вы решите двигаться в этом направлении, предлагаю следующую последовательность:

Первое — paper-based design (1 неделя). Не пишите код. Напишите дизайн-документ PORTAL-PROTOCOL-HUMANITIES-EXTENSION.md, где формализуется всё обсуждённое: humanity-specific format_types, temporal metadata, anonymization pipeline spec, two-level architecture, GDPR considerations. 15-20 страниц. Это становится reference для всей будущей работы + материал для grant application.

Второе — public demo без private (2 недели). Создайте nautilus-legal репо. Напишите один адаптер — SGBAdapter для одной книги (предлагаю SGB IX — ваша core-область). Используйте публичные тексты с gesetze-im-internet.de. Напишите pattern_adapter.py с одним-двумя generic patterns (НЕ ваши реальные кейсы пока). Проверьте через MCP, что Claude Desktop может работать с этим.

Третье — first anonymized pattern (1 неделя). Возьмите ОДИН из ваших кейсов, который уже достаточно старый или закрытый. Пропустите через anonymization pipeline. Получите clean pattern. Опубликуйте в nautilus-legal/patterns/. Это первый пример two-level architecture в действии.

Четвёртое — private layer (2 недели). Создайте приватный cases-private репо. Перенесите туда ваши активные кейсы (S 6 SO 58/26 ER, S 7 SO 99/25). Настройте auth layer. Настройте bridges к nautilus-legal patterns.

Пятое — daily use (ongoing). Начните реально использовать для работы. Через 2-3 месяца практики станет ясно, какие paттерны и инструменты действительно нужны, что можно упростить, что надо расширить. Это единственный способ узнать, работает ли система.
