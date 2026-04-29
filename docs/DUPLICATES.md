# Отчёт о дублировании

> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

Порог сходства: **0.5**  
Точных дублей: **0**  
Похожих пар: **175**

## Похожие файлы (Jaccard ≥ 0.5)

### 100% — `docs/02-anthropic-vacancies/16-history.md` vs `docs/nautilus/npp-v1-0/04-passport.md`

**Общих абзацев:** 1  
**Примеры совпадений:**

> Passports MAY быть на любом языке. Для международной видимости  RECOMMENDED иметь минимум две секции: primary language автора +  English. Рекомендуется формат с параллельными разделами, а не  отдельны…

---

### 88% — `docs/02-anthropic-vacancies/192-2-исторические-прецеденты-агенты-как-цивилизационн.md` vs `docs/nautilus/representative-agent-layer-ru/02-istoricheskie-pretsedenty.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> - [2. Исторические прецеденты: Агенты как цивилизационная инновация](#2-исторические-прецеденты-агенты-как-цивилизационная-инновация)   - [2.1. Литературные и исполнительские агенты](#21-литературные-…

> **Почему работает**: Голливуд — индустрия, интенсивная отношениями. Агенты приносят институциональную память, межпроектную видимость и переговорную экспертизу, которую отдельные исполнители не могут о…

> **Механика**: Аналогичная структура комиссий (3-10% в спорте, обычно ниже, потому что контракты больше). Крупные агенты становятся институциональными силами (например, Скотт Борас в бейсболе, который …

---

### 82% — `docs/02-anthropic-vacancies/173-4-ten-domains-of-application.md` vs `docs/nautilus/representative-agent-layer-en/04-ten-domains.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Agent function**: Monitor customer inquiries across channels.  Draft responses. Track regulatory deadlines. Identify  opportunities (grants for small business, new market trends).  Manage routine co…

> **What's different**: Proactive advocacy. Agent surfaces  opportunities for clients without requiring worker's manual  search. Reduces caseload-fatigue. Helps social workers serve  more clients more e…

> **Agent function**: Track each client's status across  multiple service systems. Alert worker to deadlines,  opportunities, complications. Draft routine communications.  Prepare client-specific resour…

---

### 82% — `docs/02-anthropic-vacancies/261-8-seven-domains-of-application.md` vs `docs/nautilus/composite-skills-agents/08-seven-domains.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> What unites these domains: - Practice is deeply specialized, but specialization combines    rather than replaces general profession competency - Practitioners typically span 10-30 distinct specializat…

> **Sub-agent specializations might include**: Classical  composition, jazz improvisation, electronic music production,  specific instruments (piano, violin, voice, etc.), genres  (folk traditions, cont…

> **Typical configurations**: A primary care physician working  in a rural clinic with elderly patients faces different  challenges from a specialist working in tertiary care. Even  within specialties, …

---

### 81% — `docs/02-anthropic-vacancies/194-4-десять-областей-применения.md` vs `docs/nautilus/representative-agent-layer-ru/04-desyat-oblastey.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Готовность к развёртыванию**: Средняя-Низкая. Требует тщательного управления для предотвращения захвата агента подгруппами в сообществе. Но потенциально трансформирующая для баланса гражданского общ…

> **Функция агента**: Отслеживать статус каждого клиента в нескольких системах услуг. Предупреждать работника о сроках, возможностях, осложнениях. Составлять рутинные коммуникации. Готовить клиент-специ…

> **Что отличается**: Владелец может сосредоточиться на ремесле (своём ресторане, своём консалтинге, своей маленькой мастерской), пока агент занимается накладными расходами развития бизнеса. Особенно це…

---

### 79% — `docs/02-anthropic-vacancies/256-3-what-makes-a-composite-skills-agent.md` vs `docs/nautilus/composite-skills-agents/03-what-makes-csa.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Function 1 — Routing.** When the principal poses a question  or task, the composite agent determines which sub-agents are  relevant. Some questions need only one sub-agent. Others need  several in c…

> **Property 1 — Configurable Sub-Agent Set.** The composite  agent draws on a specified set of narrow-specialist sub-agents,  selected by the principal (with possible AI assistance) from a  larger regi…

> **Not act externally.** Like Professional Colleague Agents, the  composite agent works inside the principal's professional  practice. External representation is the role of Representative  Agents (Typ…

---

### 79% — `docs/02-anthropic-vacancies/263-10-risks-specific-to-composite-architectures.md` vs `docs/nautilus/composite-skills-agents/10-risks.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Scenario**: The coordinator (general infrastructure managing  configurations) develops biases in routing or synthesis that  systematically favor some sub-agents over others. Practice  patterns shift…

> **Mitigations**: - Sub-agents share common foundational knowledge (so    configurations diverge from a common base) - Guild structure maintains profession-level community across    diverse configurati…

> **Scenario**: A configuration appears to work well, but its  output depends on subtle interactions between specific sub-agents.  When one sub-agent updates, the configuration's output changes  in ways…

---

### 78% — `docs/02-anthropic-vacancies/237-6-риски-специфичные-для-этой-категории.md` vs `docs/nautilus/professional-colleague-agents-ru/06-riski.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Сценарий**: Широкое развёртывание одного агента в профессии гомогенизирует профессиональную практику. Инновации извне обучающих данных агента становится труднее вводить. Профессиональное творчество …

> **Конкретный пример**: Юрист подаёт обращение с цитатой, сгенерированной параюридическим AI. Цитата оказывается галлюцинацией. Суд наказывает юриста. Был ли юрист небрежен? Был ли небрежен AI-провайде…

> - [6. Риски, специфичные для этой категории](#6-риски-специфичные-для-этой-категории)   - [6.1. Риск: Коллапс Опосредования](#61-риск-коллапс-опосредования)   - [6.2. Риск: Атрофия Навыков у Новых Пра…

---

### 78% — `docs/02-anthropic-vacancies/255-2-the-twenty-one-teachers-pattern.md` vs `docs/nautilus/composite-skills-agents/02-twenty-one-teachers-pattern.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> - [2. The Twenty-One Teachers Pattern](#2-the-twenty-one-teachers-pattern)   - [2.1. The Story](#21-the-story)   - [2.2. What This Pattern Reveals](#22-what-this-pattern-reveals)   - [2.3. Why This Pa…

> **Academic research.** Scholars whose work bridges fields.  Computational biology, environmental humanities, science and  technology studies — these fields exist because individuals  combined speciali…

> A journalist interviewing an Indian yoga master asked how he  became a teacher. The master replied that before he became a  teacher in his own right, he had studied with twenty different  teachers. Ea…

---

### 77% — `docs/02-anthropic-vacancies/158-4-proposed-infrastructure.md` vs `docs/nautilus/okwf-concept/04-proposed-infrastructure.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Extensions required for OKWF**: - Agent registry (AI assistants and meta-agents as first-class    participants) - Task protocol (formal task objects with lifecycle) - Role protocol (first-class role…

> **What it provides**: - Formal model for human-AI collaboration preserving human    agency - Three inter-layer protocols (Human↔Assistants,    Meta-agent↔Human, Assistant↔Meta-agent negotiation) - Fra…

> **Why Nautilus over alternatives**: - Already exists and demonstrably works - Zero external dependencies (auditable, portable) - Federation-over-merging principle aligns with foundation values - Human…

---

### 76% — `docs/02-anthropic-vacancies/156-2-target-populations.md` vs `docs/nautilus/okwf-concept/02-target-populations.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Example use cases**: - Blind contributor working on screen reader AI improvements - Chronic fatigue patient contributing health AI research    during good hours - Person with Sozialgericht experienc…

> **Example use cases**: - Retired German law professor contributing to legal pattern    library and junior legal writer mentorship - Former medical researcher reviewing bioinformatics code - Retired jo…

> **Unique value proposition from OKWF**: - Asynchronous work accommodating variable capacity - No discrimination in selection (AI-assisted blind matching) - Bringing disability-informed perspective to …

---

### 76% — `docs/02-anthropic-vacancies/235-4-архитектура-профессиональных-коллег-агентов.md` vs `docs/nautilus/professional-colleague-agents-ru/04-arkhitektura.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Слой B — Движок Генерации и Рассуждений.** Активный компонент: LLM (или ансамбль LLM), сконфигурированный для работы в Слое A. Принимает ввод практикующего, применяет профессиональные знания, генери…

> **Стратегия 2 — Федерация практикующих.** Многие практикующие вносят фрагменты знаний через механизм библиотеки паттернов. Качество варьируется, масштаб большой. Требует кураторского надзора. Это связ…

> Это самый дорогой слой для построения и наиболее ценный конкурентный ров. Высококачественная база профессиональных знаний для немецкого социального права, например, представляет собой тысячи часов экс…

---

### 75% — `docs/02-anthropic-vacancies/161-7-phased-rollout-plan.md` vs `docs/nautilus/okwf-concept/07-phased-rollout.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Key activities**: - Build production-ready technical infrastructure    (Nautilus-based) - Recruit first 50 contributors, primarily in legal writing    guild - Execute 5-10 pilot projects (mix of int…

> **Key activities**: - Expand to 500+ contributors across 3-5 guilds - Launch commercial project revenue stream - Establish second guild (potentially science communication or    medical documentation) …

> **Success criteria**: - 5000+ active contributors globally - Self-sustaining core operations (non-grant funding covers    baseline) - 10+ active research partnerships - Policy impact measurable - Repl…

---

### 75% — `docs/02-anthropic-vacancies/234-3-эмпирический-кейс-обучай.md` vs `docs/nautilus/professional-colleague-agents-ru/03-keys-obuchay.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> «Обучай» — российский AI-сервис для школьных учителей, запущенный осенью 2025 года Константином Чукавиным (тогда 25 лет, учителем и образовательным предпринимателем в Петербурге) вместе с разработчико…

> 1. **Встроенный профессиональный контекст**: Да    (ФГОС, методологии) 2. **Специализация на единственной профессии**:    Да (только учителя) 3. **Дополнение, не замена**: Да (учитель остаётся    отве…

> Намеренный эффект — **не** уменьшение учительского труда в смысле игры с нулевой суммой. Это **перераспределение** учительского труда от рутины к отношениям. Агент автоматизирует бюрократическую работ…

---

### 73% — `docs/02-anthropic-vacancies/162-8-risk-analysis.md` vs `docs/nautilus/okwf-concept/08-risk-analysis.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Mitigations**: - Realistic hiring of core team (5-8 people, not 3) - Co-leadership model (Executive Director supported by    technical, community leads) - Clear succession planning from launch - Exp…

> **Mitigations**: - Anchor partner committed before launch - Multiple partnership types explored in parallel - Hybrid funding model (corporate + foundation + grants) - Strong pipeline of grants submiss…

> **Risk sources**: - Employment law reclassifying contributors as employees - GDPR enforcement challenges with anonymization pipeline - AI Act regulatory requirements - Tax law differences across juris…

---

### 73% — `docs/02-anthropic-vacancies/144-7-open-questions.md` vs `docs/nautilus/double-triangle-architecture/07-open-questions.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Who decides what the meta-agent can see?** Node's team context  is defined as "what Node makes visible to team level". But in  practice, many decisions about visibility are unclear. A draft  documen…

> **Who decides who meta-agent coordinates?** Node's participation  in a team means meta-agent has authority over Node's task  assignment. But what if Node disagrees with an assignment? What  is the "ex…

> Possible mitigations: explicit completion criteria before  starting new work, formal time limits on parallel projects,  regular retrospectives with honest burnout assessment,  co-founder or collaborat…

---

### 73% — `docs/02-anthropic-vacancies/171-2-historical-precedents-agents-as-civilizational-i.md` vs `docs/nautilus/representative-agent-layer-en/02-historical-precedents.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Limitations**: Only economically viable for clients with  sufficiently high earnings to make 10-20% commission worth  it for the agent. Authors of literary fiction, for example,  often cannot afford…

> **Mechanics**: Agents typically take 10-20% commission of  client earnings. They: - Develop client portfolio over years - Maintain relationships with potential buyers (publishers,    studios, networks…

> **Why it works**: Allows highly-talented but business-naive  creators to focus on creation while still receiving fair  compensation. The agent's incentive (commission) aligns with  client's interest (…

---

### 73% — `docs/02-anthropic-vacancies/195-5-архитектурная-спецификация.md` vs `docs/nautilus/representative-agent-layer-ru/05-arkhitekturnaya-spetsifikatsiya.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> - [5. Архитектурная спецификация](#5-архитектурная-спецификация)   - [5.1. Основные компоненты](#51-основные-компоненты)   - [5.2. Принципы работы](#52-принципы-работы)   - [5.3. Технический стек](#53…

> **Компонент 6 — Монитор Защиты**: Выявляет риски, несоответствия, мошенничество, эксплуатацию. Предупреждает принципала о тревожных знаках. Поддерживает скептическую позицию по отношению к контрагента…

> **Компонент 1 — Профиль Принципала**: Всестороннее представление экспертизы, способностей, предпочтений, истории, целей, ограничений принципала. Создаётся через интервью на стадии онбординга, уточняет…

---

### 72% — `docs/02-anthropic-vacancies/145-8-call-to-action.md` vs `docs/nautilus/double-triangle-architecture/08-call-to-action.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Pattern library construction.** Begin contributing to domain  pattern libraries. Anonymize your successful workflows and  publish them. Early contributors gain first-mover advantage in  shaping conv…

> The next phase of my work is to formalize this recognition,  deploy it in the specific humanities domain that motivates my  daily effort (German social law, disability rights, access to  justice), and…

> **Comparative analysis.** Compare Double-Triangle deployments  against single-triangle baselines (centralized AI assistants vs.  centralized multi-agent systems). Quantify productivity,  coordination …

---

### 72% — `docs/02-anthropic-vacancies/215-4-architecture-of-professional-colleague-agents.md` vs `docs/nautilus/professional-colleague-agents-en/04-architecture.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> This is the most expensive layer to build and the most valuable competitive moat. A high-quality professional knowledge base for German social law, for example, represents thousands of hours of expert…

> **Authority systems** the profession is bound to. Legal filings to court systems. Tax submissions to government. Educational certifications. The agent should facilitate authority interactions, not cre…

> **Layer B — Generation and Reasoning Engine.** The active component: an LLM (or ensemble of LLMs) configured to operate within Layer A. Receives practitioner input, applies professional knowledge, gen…

---

### 71% — `docs/02-anthropic-vacancies/262-9-integration-with-okwf-infrastructure.md` vs `docs/nautilus/composite-skills-agents/09-okwf-integration.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Phase 0** (Months 1-12): Foundation establishment, initial  sub-agent set for one profession (perhaps SGB social law). Build  20-30 narrow sub-agents plus coordinator. Pilot with 5-10  practitioners…

> A mature practitioner has both: composite for daily work,  representative for opportunity navigation. They share underlying  profile information about the practitioner but operate in  different layers…

> In the Double-Triangle Architecture, each Node (human  practitioner) has lower-triangle assistants supporting their  work. Composite Skills Agents formalize what lower-triangle  assistants typically c…

---

### 71% — `docs/02-anthropic-vacancies/233-2-что-делает-агента-профессиональным-коллегой.md` vs `docs/nautilus/professional-colleague-agents-ru/02-chto-delaet-pka.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Функция 3 — Автоматизация рутинных задач.** Заниматься повторяющимися компонентами профессиональной работы, которые потребляют непропорционально много времени относительно ценности. Ввод оценок. Зап…

> **Свойство 6 — Признание нагрузки.** Агент адресует работу, которую сами практикующие признают обременительной или малоценной. Это существенно для принятия — агенты, которые «помогают» с работой, кото…

> - [2. Что делает агента Профессиональным Коллегой](#2-что-делает-агента-профессиональным-коллегой)   - [2.1. Определяющие свойства](#21-определяющие-свойства)   - [2.2. Что делает Профессиональный Кол…

---

### 71% — `docs/02-anthropic-vacancies/191-1-синдром-золушки-почему-качество-остаётся-невидим.md` vs `docs/nautilus/representative-agent-layer-ru/01-sindrom-zolushki.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Причина 3 — Личностная предрасположенность.** Многие высококачественные эксперты по природе **интроверты**, находят самопродвижение **психологически затратным** или имеют **моральное сопротивление к…

> **Причина 5 — Асимметрия внимания на современных рынках.** Как заметил Герберт Саймон в 1971 году, информационное изобилие создаёт бедность внимания. Способность **захватывать внимание** стала отдельн…

> **Причина 1 — Когнитивные ограничения пропускной способности.** Человеческая когнитивная способность ограничена. Глубокая техническая работа, научные исследования, художественное творчество или уход з…

---

### 69% — `docs/02-anthropic-vacancies/258-5-configuration-how-principals-build-their-ensembl.md` vs `docs/nautilus/composite-skills-agents/05-configuration-ensembles.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> The composite agent should help the principal monitor  configuration health: - Which sub-agents are most used? - Which are rarely consulted? - Are there new sub-agents that match the principal's recen…

> **Approach 2 — AI-assisted recommendation.** The composite  agent (or a separate recommendation system) analyzes the  principal's stated goals, work history, and preferences, then  suggests an initial…

> For many professions, common configurations exist. A new social  law lawyer might benefit from a starting template: - General SGB IX sub-agent - General SGB XII sub-agent   - Procedural law sub-agent …

---

### 69% — `docs/02-anthropic-vacancies/143-6-four-deployment-domains.md` vs `docs/nautilus/double-triangle-architecture/06-four-deployment-domains.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Lower triangle contents.** Assistants specialized for: - Legal research (case law, statute lookup) - Document drafting (Widerspruch, Klage, petitions) - Compliance checking (GDPR, medical confidenti…

> - [6. Four Deployment Domains](#6-four-deployment-domains)   - [6.1. Humanities Domain (Legal, Medical, Social)](#61-humanities-domain-legal-medical-social)   - [6.2. Project Management Domain](#62-pr…

> **Concrete deployment.** An individual (the first author,  svend4) currently engages with Sozialgericht Dresden on cases  S 6 SO 58/26 ER and S 7 SO 99/25. Personal workflow already  exhibits lower tr…

---

### 69% — `docs/02-anthropic-vacancies/254-1-why-the-binary-view-is-incomplete.md` vs `docs/nautilus/composite-skills-agents/01-why-binary-incomplete.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> This mirrors a common pattern in technology architecture: the  extremes get attention because they are conceptually clean;  the middle gets neglected because it is messier. Yet the middle  is where mo…

> Professional Colleague Agents (PCA) v1.0 introduced five types  of principal-side agents. Of these, Type 1 (Professional  Colleague Agent) and Type 4 (Representative Agent) anchor the  extremes of spe…

> What matches is an architecture where: - Many narrow-specialist sub-agents exist, each built once - Sub-agents are shared across all practitioners who need that    specialization - Each principal conf…

---

### 69% — `docs/02-anthropic-vacancies/142-5-pattern-library-as-bridge-between-triangles.md` vs `docs/nautilus/double-triangle-architecture/05-pattern-library-bridge.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> - **Start** of work: instance inherits from patterns (use existing    knowledge) - **During** work: instance cites authorities (ground work in    source material) - **After** work: instance contribute…

> Without pattern library architecture: - Assistants in N_1's lower triangle and N_2's lower triangle    cannot share knowledge - Cross-Node learning requires explicit human coordination - Team knowledg…

> 1. PII detection (names, dates, addresses, identifiers) 2. Replacement with type-consistent placeholders 3. Manual verification (automated anonymization is insufficient) 4. Structural metadata additio…

---

### 69% — `docs/02-anthropic-vacancies/213-2-what-makes-a-professional-colleague-agent.md` vs `docs/nautilus/professional-colleague-agents-en/02-what-makes-pca.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Property 6 — Recognition of Burden.** The agent addresses work that practitioners themselves recognize as burdensome or low-value. This is essential to adoption — agents that "help" with work practi…

> **Function 1 — Generation in Professional Format.** Produce drafts, materials, plans, analyses in formats specific to the profession. A teaching agent generates lesson plans in educational formats. A …

> **Property 5 — Mass Replication.** The same agent design serves all practitioners of the profession. Per-user customization is limited to user preferences and work-in-progress. The professional contex…

---

### 67% — `docs/02-anthropic-vacancies/292-что-отсутствует-слой-b.md` vs `docs/nautilus/infrastructure-layer-b-ru/03-otsutstvuet-sloy-b.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Рабочий процесс продвижения.** Содержание, разработанное в Слое B, могло бы быть продвинуто в Слой C (закоммичено в репозиторий), когда оно достаточно стабильно. Содержание из Слоя A (чата) могло бы…

> Он бы поддерживал **текучую креативность** чата, добавляя **структурную стабильность** репозитория. Он бы позволял **ветвящееся исследование** без потери контекста. Он бы сохранял **конкретные точки**…

> **Перекрёстные ссылки.** Документы и треды обсуждений могли бы ссылаться друг на друга явно. Ссылка из Документа 7 на Документ 6 была бы реальной ссылкой, не просто текстом. Переход по ссылке показыва…

---

### 67% — `docs/02-anthropic-vacancies/277-what-s-missing-layer-b.md` vs `docs/nautilus/infrastructure-layer-b-en/04-whats-missing-layer-b.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Annotation on documents.** Specific sections of documents  could be annotated with comments. Comments could be threaded.  Other AI agents (or human collaborators) could respond to  comments. Annotat…

> It would maintain the **fluid creativity** of chat while adding  the **structural stability** of repository. It would allow  **branching exploration** without losing context. It would  preserve **spec…

> **Bidirectional flow.** Promotion is not one-way. Material  in Layer C could be brought back to Layer B for further  development, then re-promoted. Material in Layer B could be  extracted to chat for …

---

_...и ещё 145 пар._

> Файлы не удалялись автоматически. Проверьте вручную и удалите ненужные.

<!-- see-also -->

---

**Смотрите также:**
- [01-response-en](docs/nautilus/community-discussions/agent-changes-reality/01-response-en.md)
- [SOURCE_MAP](docs/SOURCE_MAP.md)
- [READABILITY](docs/READABILITY.md)
- [READING_TIME](docs/READING_TIME.md)

