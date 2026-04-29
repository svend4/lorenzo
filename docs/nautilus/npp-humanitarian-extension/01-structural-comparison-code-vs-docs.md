# Структурное сравнение: код vs гуманитарные документы

<!-- summary -->
> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — применение NPP к гуманитарным документам (юридические, социальные).

---
<!-- tags: rag, ingestion, architecture, roadmap, anthropic, collaboration -->




> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — применение NPP к гуманитарным документам (юридические, социальные).

Структурное сравнение: код vs гуманитарные документы

Чтобы понять, что менять и что оставить, полезно сопоставить оба домена:

| Аспект | Код/Research (текущий Nautilus) | Юридические/Социальные документы
| Единица данных | Концепт/функция/теорема | Статья закона/параграф решения/кейс
| Native format | .py, .md, .info1, .pro2 | .pdf, .docx, .odt, .md, .rtf
| Язык | En/Ru, технический | De (SGB, SGG), En (EU law), Ru
| Связи | Import, reference, bridge | Статья→статья, прецедент→прецедент, учреждение→процедура
| Авторство | Автор-разработчик | Законодатель, суд, учреждение
| Консенсус | Концепт в N репо | Факт подтверждён N источниками
| Q6-координата | Семантическая вершина | Категория права/социальной сферы
| Стабильность | Меняется часто (коммиты) | Стабильна (Geltungsbereich), но с поправками
| Timestamp-критичность | Умеренная | Критическая (Fristwahrung, Inkrafttreten)
| Regulatory | Open-source lics | Urheberrecht, Amtliche Werke, GDPR

Главные отличия, влияющие на протокол:

Критичность дат и версий. Юридический документ — это статья N версии закона M по состоянию на дату D. Nautilus v1.1 умеет timeline.py, но не формально валидирует «действует ли эта норма на дату запроса». Это нужно расширять.

Много native форматов. PDF, DOCX, ODT — не только текст. Нужны адаптеры, которые умеют извлекать текст из PDF-решений суда, OCR'ить сканы, работать с таблицами из Excel-ведомостей.

Легальная семантика ссылок. В коде ссылка pro2:q6:010011 — указание на концепт. В законе ссылка § 90 Abs. 4 SGB XII — legally binding reference с нормативной силой. Разница в том, что неточная ссылка в коде — баг, неточная ссылка в правовом документе — ошибка, которая может повлиять на суд.

Теперь конкретно, что добавить.

1. Новые format_type значения

В PORTAL-PROTOCOL v1.1 §7.1 я определил format_type: document, concept, rule, theory, schema, archetype. Добавляем категорию для гуманитарных доменов:

python

FORMAT_TYPES_HUMANITIES = [
# Законодательные
"law_section", # статья закона (§ 90 SGB XII)
"law_paragraph", # абзац (Absatz)
"law_regulation", # постановление (Verordnung)
"eu_directive", # EU Richtlinie

# Судебные
"court_decision", # судебное решение
"court_order", # определение
"precedent", # прецедент (обязывающий)
"legal_commentary", # комментарий юриста

# Административные
"bescheid", # административное решение (DE)
"administrative_act", # administrative act (EN)
"circular_letter", # Rundschreiben

# Процессуальные
"widerspruch", # возражение
"klage", # исковое заявление
"antrag", # заявление
"urteil", # окончательное решение

# Социальные/медицинские
"benefit_entitlement", # право на льготу
"care_plan", # план ухода
"disability_assessment", # оценка инвалидности
"medical_report", # медицинское заключение

# Контрактные
"contract_clause", # условие договора
"service_agreement", # соглашение об услугах

# Метаданные
"case_file", # дело (группа документов)
"institutional_profile", # учреждение
"legal_entity", # юр.лицо / чиновник
]

Это не breaking change — существующие адаптеры продолжают использовать старые значения. Новые появляются по мере появления новых адаптеров.

2. Новые адаптеры для гуманитарных источников

Требуется разработка следующих адаптеров:

PDFLegalAdapter — читает PDF-документы (решения судов, Bescheide, законы в PDF), извлекает структуру (параграфы, пункты), возвращает как PortalEntry с format_type="law_section" или "court_decision". Требует pdfplumber или pypdf2 — первая внешняя зависимость, отход от stdlib-only. Или альтернативно — вызов внешнего сервиса OCR.

DocxLegalAdapter — читает .docx шаблоны и реальные документы. В ваших soz* репо, по userMemories, много Word-документов (Stellungnahme, Widerspruch, Antrag). Адаптер извлекает структуру (разделы, подписи), мапит на format_type.

SGBLawAdapter — специализированный под Sozialgesetzbuch. Знает структуру: SGB I–XIV, каждая книга → параграфы → абзацы → пункты. Может построить уникальный ID: sgb:XII:90:4 (SGB XII, § 90, Abs. 4). Q6-координата может кодировать область права (Arbeitsförderung / Rentenversicherung / Krankenversicherung / Pflegeversicherung / etc).

CourtDecisionAdapter — для решений судов. Уникальный ID по Aktenzeichen (dresden_sg:S_6_SO_58_26_ER). Метаданные: суд, дата, судья, стороны. Ссылки: на применённые статьи закона (sgb:IX:102, sgg:86b:2), на прецеденты.

BescheidAdapter — административные решения (от Sozialamt, Jobcenter, Krankenkasse). Уникальный ID: sozialamt_dresden:bescheid:2025-11-12:SO-123. Содержит: issuer, addressee, дата, срок Widerspruch, применённые нормы.

CaseFileAdapter — мета-адаптер для целого дела. Группирует все документы кейса: Antrag → Bescheid → Widerspruch → Widerspruchsbescheid → Klage → Urteil. Возвращает timeline целого процесса как единую PortalEntry.

InstitutionalAdapter — для информации об учреждениях (Sozialamt Dresden, KSV Sachsen, SG Dresden). Метаданные: адрес, контакты, компетенции, Aktenzeichen-схема, ответственные персоны.

Каждый адаптер — отдельный Python-файл в adapters/, наследуется от BaseAdapter, реализует fetch() + describe().

3. Расширение PortalEntry для гуманитарных доменов

В PORTAL-PROTOCOL v1.1 §7.1 PortalEntry имеет metadata как свободный dict. Для гуманитарных документов рекомендую conventional metadata keys:

python

@dataclass
class LegalPortalEntry(PortalEntry):
# Всё из PortalEntry (id, title, source, format_type, content, links, is_fallback)
# плюс рекомендуемые keys в metadata:
metadata: dict = {
# Темпоральные
"effective_from": "2024-01-01", # ISO date, Inkrafttreten
"effective_until": None, # ISO date or None (still valid)
"version": "2024-01", # версия документа

# Юридические
"jurisdiction": "DE/SN", # ISO country / state
"legal_area": "social_law", # см. таксономию ниже
"binding": True, # обязательно к применению
"normative_rank": "statute", # constitution/statute/regulation/directive

# Источник
"issuer": "Bundestag", # кто издал
"official_journal": "BGBl. I S. 3234", # официальная публикация
"aktenzeichen": "S 6 SO 58/26 ER", # номер дела (для судов)

# Классификация 
"q6": "010011", # как у всех
"topic_tags": ["Eingliederungshilfe", "Persönliches Budget"],

# Процессуальные
"deadline": "2025-12-15", # если документ содержит срок
"deadline_type": "widerspruchsfrist", # тип срока

# Ссылки (перекрёстные)
"supersedes": ["sgb:XII:90:3"], # что заменил
"superseded_by": [], # что заменило это
"cited_by": ["dresden_sg:S_6_SO_58_26_ER"], # кто ссылается
}

Эти поля — convention, не требование протокола. Адаптер может заполнять или не заполнять их. Но если заполняет — все адаптеры делают это одинаково, что enables cross-repo queries типа «найди все нормы, действовавшие на дату X».

4. Q6-маппинг для гуманитарного домена

В PORTAL-PROTOCOL v1.1 §8.3 каждый format определяет свой Q6-маппинг. Для юридических/социальных документов предлагаю следующую схему — пример, не нормативная спецификация:

6 бит Q6 распределены так:

Биты 5-4 (старшие) — уровень нормы:

00 — конституционный (Grundgesetz, Menschenrechte)

01 — федеральный закон (Bundesgesetz, SGB)

10 — постановление (Verordnung, Durchführungsverordnung)

11 — административный акт (Bescheid, Rundschreiben)

Биты 3-2 — область права:

00 — социальное (Sozialrecht: SGB II, XII, IX)

01 — трудовое/налоговое (Arbeits-/Steuerrecht)

10 — гражданское/семейное (BGB, FamFG)

11 — публичное/процессуальное (VwVfG, SGG, StPO)

Биты 1-0 — статус/временность:

00 — действующий (gültig, rechtskräftig)

01 — устаревший (aufgehoben)

10 — спорный/обжалуемый (strittig, angefochten)

11 — планируемый/будущий (geplant, in Beratung)

Пример: статья SGB XII § 90 (социальная, действующая, федеральный закон) → биты 01 00 00 = 010000.

Это конкретный маппинг для гуманитарного под-домена. Другие domains (юридические системы других стран, медицинские документы) будут иметь свой Q6-маппинг — это и есть гибкость протокола. Nautilus не навязывает одну онтологию, каждый домен выбирает свою.

5. Новые bridges для гуманитарного домена

В PORTAL-PROTOCOL v1.1 §3.2 bridges — это словарь repo_name → description. Для гуманитарных репо типичные bridges:

json

"bridges": {
"sgb_laws": "цитаты в решениях ↔ статьи закона, через § номер",
"court_decisions": "прецеденты ↔ кейсы по Aktenzeichen",
"sozialamt_cases": "Bescheide ↔ конкретные административные решения",
"medical_reports": "диагнозы ↔ медицинские заключения по ICD-10"
}

Уникальная особенность гуманитарных bridges — они часто прямые и формальные, не текстовые интерпретации. Ссылка "§ 90 SGB XII" в тексте решения — это machine-parseable citation, не свободное описание. Это означает, что Level 3 адаптеры для юриспруденции могут реализовать translate_to() как алгоритмический lookup, не как эвристическое отображение.

6. Что это меняет в PORTAL-PROTOCOL

Для поддержки гуманитарного домена нужно PORTAL-PROTOCOL v1.2 со следующими дополнениями:

Новый раздел — "Humanities Extension". Описывает conventional format_type values, metadata keys, Q6 mapping patterns для законодательных/судебных/административных документов. Это informative, не нормативная часть — позволяет разным юрисдикциям адаптировать под себя.

Новое ADR — "ADR-004: Temporal Metadata as First-Class Concept". Фиксирует, что effective_from/effective_until — mandatory для юридических адаптеров, желательны для всех остальных. Это решает критичную проблему юридических документов: «действует ли эта норма сейчас».

Расширение раздела 15 Security Considerations. Гуманитарные документы часто содержат персональные данные (имена, адреса, диагнозы, Aktenzeichen). Добавляется подраздел "15.6. Personal Data and GDPR Compliance" с требованиями: отдельные private vs public registries, pseudonymization, opt-in для MCP exposure.

7. Application к вашим реальным кейсам

Теперь — практика. Из userMemories я знаю, что у вас есть:

Активные кейсы в Sozialgericht Dresden (S 6 SO 58/26 ER, S 7 SO 99/25)

Множество soz* репозиториев (по userMemories — 11 штук)

Writing OS — React-система с 300+ специализированными юридическими инструментами

Мегашаблон для 24/7 психиатрической помощи через Persönliches Budget

База документов по SGB IX, XII, SGG

Шаблоны Widerspruch, Klage, Eingliederungshilfe-Antrag

Анализ корреспонденции опекуна Daniel Janz

Всё это — идеальный кандидат для гуманитарной версии Nautilus. Конкретное применение:

Legal-Nautilus — параллельный portal для юридического домена. Это не подмножество svend4/nautilus, а отдельная instance с собственным legal-nautilus.json и адаптерами для юридических форматов. Причина отдельной instance — приватность: ваши soz* репо содержат детали конкретных людей и конкретных дел, не должны смешиваться с публичной Q6-федерацией.

Структура Legal-Nautilus мне видится так:

legal-nautilus/ ← отдельный приватный репо
├── legal-nautilus.json ← приватный registry
├── legal-portal.py ← fork svend4/nautilus/portal.py
├── legal-portal-mcp.py ← fork portal-mcp.py, с auth
├── adapters/
│ ├── base.py ← тот же BaseAdapter
│ ├── sgb_adapter.py ← SGB I-XIV (legal texts)
│ ├── dresden_sg_adapter.py ← решения SG Dresden
│ ├── bescheid_adapter.py ← Bescheide Sozialamt/KSV
│ ├── case_file_adapter.py ← ваши текущие дела
│ ├── widerspruch_template_adapter.py
│ ├── medical_report_adapter.py ← медицинские заключения
│ └── institutional_adapter.py ← учреждения Sachsen
├── passports/
│ ├── sgb.md
│ ├── dresden_sg.md
│ ├── case_files.md
│ └── ...
├── auth/
│ ├── jwt_config.json ← API keys
│ └── access_control.yml
└── README-LEGAL.md ← инструкция для вашего use case

<!-- see-also -->

---

**Смотрите также:**
- [133-обратная-связь](docs/02-anthropic-vacancies/133-обратная-связь.md)
- [03-what-this-gives-technically](docs/nautilus/privacy-federation/03-what-this-gives-technically.md)
- [01-strategic-significance](docs/nautilus/multi-tier-architecture/01-strategic-significance.md)
- [02-two-tier-publication](docs/nautilus/privacy-federation/02-two-tier-publication.md)


<!-- similar-docs -->

---

**Похожие документы:**
- [133-обратная-связь](docs/obsidian/02-anthropic-vacancies/133-обратная-связь.md) (сходство 0.20)
- [133-обратная-связь](docs/02-anthropic-vacancies/133-обратная-связь.md) (сходство 0.20)
- [03-what-this-gives-technically](docs/nautilus/privacy-federation/03-what-this-gives-technically.md) (сходство 0.14)

