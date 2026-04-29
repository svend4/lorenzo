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

> **Ограничения**: Экономически жизнеспособно только для клиентов с достаточно высоким заработком, чтобы 10-20% комиссии стоили того для агента. Авторы литературной фантастики, например, часто не могут …

> **Почему работает**: Позволяет высокоталантливым, но наивным в бизнесе создателям сосредоточиться на творчестве, по-прежнему получая справедливое вознаграждение. Стимул агента (комиссия) совпадает с и…

> **Механика**: Смешанная — некоторые финансируются государством (юридическая помощь, омбудсмены), некоторые коммерческие (иммиграционные консультанты, налоговые подготовители), некоторые добровольчески…

---

### 82% — `docs/02-anthropic-vacancies/173-4-ten-domains-of-application.md` vs `docs/nautilus/representative-agent-layer-en/04-ten-domains.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **What's different**: Retired professional doesn't have to  "job hunt" for volunteer work. Agent finds the right matches  proactively. Particularly valuable for those experiencing  post-retirement ide…

> **Agent function**: Monitor opportunities (scholarships,  research programs, internships). Decode institutional  communications. Track deadlines. Identify entitlements.  Connect with relevant advisors…

> **Personal note from author**: This is the domain where the  author currently engages, navigating Sozialgericht proceedings  with disability status. The need is intensely felt. Existing  infrastructur…

---

### 82% — `docs/02-anthropic-vacancies/261-8-seven-domains-of-application.md` vs `docs/nautilus/composite-skills-agents/08-seven-domains.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Typical configurations**: A lawyer specializing in disability  rights for migrants speaks both German and the migrant's  language and has medical understanding for assessing claims —  a combination …

> **Typical configurations**: A primary care physician working  in a rural clinic with elderly patients faces different  challenges from a specialist working in tertiary care. Even  within specialties, …

> **Sub-agent specializations might include**: Therapeutic  modalities (CBT, somatic experiencing, narrative therapy,  gestalt), specific conditions (trauma, addiction, eating  disorders, mood disorders…

---

### 81% — `docs/02-anthropic-vacancies/194-4-десять-областей-применения.md` vs `docs/nautilus/representative-agent-layer-ru/04-desyat-oblastey.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Функция агента**: Отслеживать состояние. Предупреждать о предстоящих приёмах, продлениях рецептов, результатах лабораторных исследований. Переводить медицинские коммуникации. Мониторить новые методы…

> **Функция агента**: Координировать членов сообщества. Поддерживать последовательную позицию во всех коммуникациях. Исследовать соответствующее право и прецедент. Составлять формальные документы. Выявл…

> **Функция агента**: Артикулировать вероятные интересы непредставленных заинтересованных сторон. Выводить на поверхность соображения, иначе пропущенные. Обеспечивать структурированный вход в делиберати…

---

### 79% — `docs/02-anthropic-vacancies/256-3-what-makes-a-composite-skills-agent.md` vs `docs/nautilus/composite-skills-agents/03-what-makes-csa.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Not act externally.** Like Professional Colleague Agents, the  composite agent works inside the principal's professional  practice. External representation is the role of Representative  Agents (Typ…

> **Function 2 — Synthesis.** When multiple sub-agents contribute  to a response, the composite agent integrates their outputs  into a coherent whole — without obscuring which sub-agent  contributed wha…

> **Function 3 — Disagreement Management.** When sub-agents  provide conflicting recommendations, the composite agent  presents the disagreement clearly to the principal: "Sub-agent  A recommends X for …

---

### 79% — `docs/02-anthropic-vacancies/263-10-risks-specific-to-composite-architectures.md` vs `docs/nautilus/composite-skills-agents/10-risks.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Scenario**: As composite configurations diversify, professional  practice fragments. Practitioners working on similar problems  develop incompatible approaches because they used different  sub-agent…

> **Mitigations**: - Strong starting templates for common professional patterns - AI-assisted recommendation as default (with override) - Limit on initial configuration size (start with 5-10, grow    ov…

> **Scenario**: Principals discover that specific configurations  are particularly effective. They keep these configurations  secret as competitive advantage. Configuration knowledge becomes  hoarded ra…

---

### 78% — `docs/02-anthropic-vacancies/237-6-риски-специфичные-для-этой-категории.md` vs `docs/nautilus/professional-colleague-agents-ru/06-riski.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Меры противодействия 4 — Приемлемые компромиссы.** Некоторая атрофия навыков приемлема. Мы не сожалеем о потере навыков ментальной арифметики из-за калькуляторов. Вопрос в том, какие навыки существе…

> **Конкретный пример**: Терапевт использует Профессионального Коллегу-Агента для синтеза заметок. Конфиденциальность пациента скомпрометирована, когда у провайдера агента происходит инцидент безопаснос…

> - [6. Риски, специфичные для этой категории](#6-риски-специфичные-для-этой-категории)   - [6.1. Риск: Коллапс Опосредования](#61-риск-коллапс-опосредования)   - [6.2. Риск: Атрофия Навыков у Новых Пра…

---

### 78% — `docs/02-anthropic-vacancies/255-2-the-twenty-one-teachers-pattern.md` vs `docs/nautilus/composite-skills-agents/02-twenty-one-teachers-pattern.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> - [2. The Twenty-One Teachers Pattern](#2-the-twenty-one-teachers-pattern)   - [2.1. The Story](#21-the-story)   - [2.2. What This Pattern Reveals](#22-what-this-pattern-reveals)   - [2.3. Why This Pa…

> **Law.** Lawyers who combine practice areas. A lawyer with  expertise in technology law plus disability rights plus  international human rights occupies a niche shaped by her  specific combination, ev…

> **The pattern is repeatable but not duplicable.** Other students  could similarly study with twenty teachers and develop their  own composite mastery. But each composite would be different.  The patte…

---

### 77% — `docs/02-anthropic-vacancies/158-4-proposed-infrastructure.md` vs `docs/nautilus/okwf-concept/04-proposed-infrastructure.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Proposed initial guilds**: - **Legal Writing Guild** — German/EU social and disability    law documentation - **Science Communication Guild** — arxiv paper translation    and summarization - **Medic…

> **Proposed structure**: - **Base stipend**: €500-1500/month for active contributors    (depending on region cost-of-living) - **Project bonuses**: €500-5000/project for specific deliverables - **Reven…

> OKWF infrastructure consists of six interlocking layers. Each  layer has reference implementation (open source), operational  component (foundation-staffed), and community component  (contributor-gove…

---

### 76% — `docs/02-anthropic-vacancies/156-2-target-populations.md` vs `docs/nautilus/okwf-concept/02-target-populations.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> - [2. Target Populations](#2-target-populations)   - [2.1. Retired Experts with Remaining Intellectual Capacity](#21-retired-experts-with-remaining-intellectual-capacity)   - [2.2. Disabled Specialist…

> **Example use cases**: - Blind contributor working on screen reader AI improvements - Chronic fatigue patient contributing health AI research    during good hours - Person with Sozialgericht experienc…

> **Example use cases**: - Retired German law professor contributing to legal pattern    library and junior legal writer mentorship - Former medical researcher reviewing bioinformatics code - Retired jo…

---

### 76% — `docs/02-anthropic-vacancies/235-4-архитектура-профессиональных-коллег-агентов.md` vs `docs/nautilus/professional-colleague-agents-ru/04-arkhitektura.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Принцип Осведомлённости об Обновлениях.** Существенные обновления базы знаний выводятся на поверхность практикующему. «Соответствующий статут был изменён на прошлой неделе. Ваше текущее обращение мо…

> **Слой A — База Профессиональных Знаний.** Закодированное знание профессии: стандарты, регуляции, методологии, шаблоны, словари, общие паттерны. Курируется и поддерживается профессиональными экспертам…

> Эта работа по интеграции значительна. Это также то, где многие проекты «AI для X профессии» проваливаются — построив прекрасного агента, которого ни один практикующий не может вписать в свой существую…

---

### 75% — `docs/02-anthropic-vacancies/161-7-phased-rollout-plan.md` vs `docs/nautilus/okwf-concept/07-phased-rollout.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> OKWF evolves into trusted infrastructure for distributed  expert work globally. Multiple foundations and corporate  partners sustain operations. Contributors span every continent.  Specialization exte…

> **Risk mitigations**: - If anchor commitment fails: pivot to foundation-only funding    with delayed, smaller pilot - If core team assembly slow: partner with established entity    (e.g., Mozilla Foun…

> **Key activities**: - Establish legal entity (non-profit foundation in Germany or    similar jurisdiction) - Secure anchor corporate funding commitment - Assemble core team (Executive Director, Techni…

---

### 75% — `docs/02-anthropic-vacancies/234-3-эмпирический-кейс-обучай.md` vs `docs/nautilus/professional-colleague-agents-ru/03-keys-obuchay.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> Более широкое общественное влияние сервиса не доказано. Действительно ли он улучшает образование или просто ускоряет бюрократический процесс, оставляя качество образования неизменным, ещё предстоит из…

> Это согласуется с общими паттернами принятия технологий: рекомендованные коллегами инструменты распространяются быстрее, чем самопродвигаемые инструменты. Как только органические первопроходцы создали…

> Сервис генерирует: - Планы уроков для конкретных предметов, классов,   уровней сложности - Задания для учеников, откалиброванные под   конкретные уровни обучения - Изображения и презентации для уроков…

---

### 73% — `docs/02-anthropic-vacancies/162-8-risk-analysis.md` vs `docs/nautilus/okwf-concept/08-risk-analysis.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Mitigations**: - Anchor partner committed before launch - Multiple partnership types explored in parallel - Hybrid funding model (corporate + foundation + grants) - Strong pipeline of grants submiss…

> **Evidence of demand**: - Substantial LinkedIn/professional network discussions about    underemployment of elder professionals - Active disability advocacy groups seeking employment    infrastructure…

> **Mitigations**: - Realistic hiring of core team (5-8 people, not 3) - Co-leadership model (Executive Director supported by    technical, community leads) - Clear succession planning from launch - Exp…

---

### 73% — `docs/02-anthropic-vacancies/144-7-open-questions.md` vs `docs/nautilus/double-triangle-architecture/07-open-questions.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Who decides what the meta-agent can see?** Node's team context  is defined as "what Node makes visible to team level". But in  practice, many decisions about visibility are unclear. A draft  documen…

> Participants may game the system: - Nodes may present inflated deliverables to meta-agent - Meta-agents may favor some Nodes over others - Assistants may develop unauthorized private goals - Bad actor…

> Possible mitigations: explicit completion criteria before  starting new work, formal time limits on parallel projects,  regular retrospectives with honest burnout assessment,  co-founder or collaborat…

---

### 73% — `docs/02-anthropic-vacancies/171-2-historical-precedents-agents-as-civilizational-i.md` vs `docs/nautilus/representative-agent-layer-en/02-historical-precedents.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Mechanics**: Similar commission structure (3-10% in sports,  typically lower because contracts are larger). Major agents  become institutional powers (e.g., Scott Boras in baseball,  who has fundame…

> - **Economic viability** drops dramatically — AI agent costs    $10-100/month vs. human agent's $50K+ annual cost - **Entry-level access** becomes universal — even small    contributors can have repre…

> **Mechanics**: Commission-based (10% standard). Agencies  (CAA, WME, UTA) have hundreds of agents, structured as  sophisticated organizations with specialized departments  (film, TV, music, publishing…

---

### 73% — `docs/02-anthropic-vacancies/195-5-архитектурная-спецификация.md` vs `docs/nautilus/representative-agent-layer-ru/05-arkhitekturnaya-spetsifikatsiya.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Компонент 6 — Монитор Защиты**: Выявляет риски, несоответствия, мошенничество, эксплуатацию. Предупреждает принципала о тревожных знаках. Поддерживает скептическую позицию по отношению к контрагента…

> **Компонент 5 — Менеджер Коммуникаций**: Обрабатывает текущую переписку с контрагентами. Начальное обращение, уточнение, планирование. Выводит сложные решения принципалу. Работает в рамках, установлен…

> **Компонент 1 — Профиль Принципала**: Всестороннее представление экспертизы, способностей, предпочтений, истории, целей, ограничений принципала. Создаётся через интервью на стадии онбординга, уточняет…

---

### 72% — `docs/02-anthropic-vacancies/145-8-call-to-action.md` vs `docs/nautilus/double-triangle-architecture/08-call-to-action.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Grant applications.** EU funding programs (EIC Pathfinder,  Horizon Europe) increasingly support AI-for-good research.  Double-Triangle deployments in humanities domains (access to  justice, disabil…

> **Product opportunities.** Existing AI tools implement single  triangles. Double-Triangle implementations represent differentiated  product opportunities across many domains. First-movers will  define…

> **Public infrastructure.** Pattern libraries in domains like  legal knowledge, medical protocols, educational curricula have  public good properties. Government funding for public pattern  libraries (…

---

### 72% — `docs/02-anthropic-vacancies/215-4-architecture-of-professional-colleague-agents.md` vs `docs/nautilus/professional-colleague-agents-en/04-architecture.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Layer B — Generation and Reasoning Engine.** The active component: an LLM (or ensemble of LLMs) configured to operate within Layer A. Receives practitioner input, applies professional knowledge, gen…

> **QA Mechanism 3 — Practitioner Review Required.** Outputs are drafts requiring practitioner review and acceptance, not final products. The agent's interface should make review natural rather than bur…

> **Authority systems** the profession is bound to. Legal filings to court systems. Tax submissions to government. Educational certifications. The agent should facilitate authority interactions, not cre…

---

### 71% — `docs/02-anthropic-vacancies/262-9-integration-with-okwf-infrastructure.md` vs `docs/nautilus/composite-skills-agents/09-okwf-integration.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> This is a better proposal for foundation funders even at higher  cost, because it demonstrates a more sophisticated understanding  of how skilled practice works and produces infrastructure with  broad…

> The Nautilus pattern library architecture (public patterns,  private instances, anonymization pipeline) provides foundational  support for the sub-agent registry. Patterns become source  material for …

> Composite Skills Agents and Representative Agents work together  naturally: - The composite agent supports the practitioner's work - The representative agent supports the practitioner's external    po…

---

### 71% — `docs/02-anthropic-vacancies/233-2-что-делает-агента-профессиональным-коллегой.md` vs `docs/nautilus/professional-colleague-agents-ru/02-chto-delaet-pka.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **«Коллега»** предполагает равного в профессии, общий контекст, взаимное уважение, параллельную работу. Коллега-врач, проверяющий ваш случай. Старший учитель, дающий совет. Коллеги привносят профессио…

> **Свойство 1 — Встроенный профессиональный контекст.** Агент имеет глубокое, постоянное знание профессиональных норм, методологий, регуляций, словаря и шаблонов. Практикующему не нужно заново объяснят…

> **Свойство 2 — Специализация на единственной профессии.** Агент обслуживает одну определённую профессию (или один определённый подвид). Не «несколько профессий». Не «общая профессиональная работа». Эт…

---

### 71% — `docs/02-anthropic-vacancies/191-1-синдром-золушки-почему-качество-остаётся-невидим.md` vs `docs/nautilus/representative-agent-layer-ru/01-sindrom-zolushki.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> - [1. Синдром Золушки: Почему качество остаётся невидимым](#1-синдром-золушки-почему-качество-остаётся-невидимым)   - [1.1. Паттерн](#11-паттерн)   - [1.2. Анекдотическая иллюстрация](#12-анекдотическ…

> **Причина 5 — Асимметрия внимания на современных рынках.** Как заметил Герберт Саймон в 1971 году, информационное изобилие создаёт бедность внимания. Способность **захватывать внимание** стала отдельн…

> **Причина 1 — Когнитивные ограничения пропускной способности.** Человеческая когнитивная способность ограничена. Глубокая техническая работа, научные исследования, художественное творчество или уход з…

---

### 69% — `docs/02-anthropic-vacancies/258-5-configuration-how-principals-build-their-ensembl.md` vs `docs/nautilus/composite-skills-agents/05-configuration-ensembles.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> A principal entering an ecosystem with hundreds of available  sub-agents faces a configuration problem. They do not yet know: - Which specializations are most relevant to their work - Which combinatio…

> A principal's configuration is not static. Specializations  change over time: - New specializations enter their work as careers evolve - Old specializations become less relevant as priorities shift - …

> The composite agent should help the principal monitor  configuration health: - Which sub-agents are most used? - Which are rarely consulted? - Are there new sub-agents that match the principal's recen…

---

### 69% — `docs/02-anthropic-vacancies/143-6-four-deployment-domains.md` vs `docs/nautilus/double-triangle-architecture/06-four-deployment-domains.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Concrete deployment.** An individual (the first author,  svend4) currently engages with Sozialgericht Dresden on cases  S 6 SO 58/26 ER and S 7 SO 99/25. Personal workflow already  exhibits lower tr…

> **Lower triangle contents.** Assistants specialized for: - Legal research (case law, statute lookup) - Document drafting (Widerspruch, Klage, petitions) - Compliance checking (GDPR, medical confidenti…

> - [6. Four Deployment Domains](#6-four-deployment-domains)   - [6.1. Humanities Domain (Legal, Medical, Social)](#61-humanities-domain-legal-medical-social)   - [6.2. Project Management Domain](#62-pr…

---

### 69% — `docs/02-anthropic-vacancies/254-1-why-the-binary-view-is-incomplete.md` vs `docs/nautilus/composite-skills-agents/01-why-binary-incomplete.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> This mirrors a common pattern in technology architecture: the  extremes get attention because they are conceptually clean;  the middle gets neglected because it is messier. Yet the middle  is where mo…

> Professional Colleague Agents (PCA) v1.0 introduced five types  of principal-side agents. Of these, Type 1 (Professional  Colleague Agent) and Type 4 (Representative Agent) anchor the  extremes of spe…

> **They are differentiated within the profession.** No two  musicians are identical. No two lawyers practice exactly the  same way. Each combines particular specializations, particular  influences, par…

---

### 69% — `docs/02-anthropic-vacancies/142-5-pattern-library-as-bridge-between-triangles.md` vs `docs/nautilus/double-triangle-architecture/05-pattern-library-bridge.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> Double-Triangle systems face a fundamental question: how do  assistants in different Nodes' lower triangles share knowledge  about best practices, conventions, and reusable patterns, without  each Nod…

> Without pattern library architecture: - Assistants in N_1's lower triangle and N_2's lower triangle    cannot share knowledge - Cross-Node learning requires explicit human coordination - Team knowledg…

> **Tier 2 — Private Instances.** Concrete applications of patterns  within specific contexts: a team's actual sprint, a lawyer's  actual case, a developer's actual deployment. These are  Node-specific …

---

### 69% — `docs/02-anthropic-vacancies/213-2-what-makes-a-professional-colleague-agent.md` vs `docs/nautilus/professional-colleague-agents-en/02-what-makes-pca.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Function 1 — Generation in Professional Format.** Produce drafts, materials, plans, analyses in formats specific to the profession. A teaching agent generates lesson plans in educational formats. A …

> **Property 2 — Single-Profession Specialization.** The agent serves one defined profession (or one defined sub-specialty). Not "multiple professions". Not "general professional work." This focus enabl…

> **Function 3 — Routine Task Automation.** Handle the repetitive components of professional work that consume disproportionate time relative to value. Grade entry. Form filling. Standard correspondence…

---

### 67% — `docs/02-anthropic-vacancies/292-что-отсутствует-слой-b.md` vs `docs/nautilus/infrastructure-layer-b-ru/03-otsutstvuet-sloy-b.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Версионирование без кодо-ориентации.** Документы могли бы версионироваться, с показанными диффами, но без культурных накладных расходов на pull requests и процессы ревью кода. Правки могли бы быть с…

> **Двунаправленный поток.** Продвижение не односторонне. Материал в Слое C мог бы быть возвращён в Слой B для дальнейшей разработки, затем перепродвинут. Материал в Слое B мог бы быть извлечён в чат дл…

> **Аннотация на документах.** Конкретные разделы документов могли бы быть аннотированы комментариями. Комментарии могли бы быть тредированы. Другие AI-агенты (или человек-сотрудник) могли бы отвечать н…

---

### 67% — `docs/02-anthropic-vacancies/277-what-s-missing-layer-b.md` vs `docs/nautilus/infrastructure-layer-b-en/04-whats-missing-layer-b.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **AI collaboration as primary operation.** Each thread, each  document, each annotation could be developed in collaboration  with AI. The AI would have access to the full context of the  project — not…

> **Annotation on documents.** Specific sections of documents  could be annotated with comments. Comments could be threaded.  Other AI agents (or human collaborators) could respond to  comments. Annotat…

> **Bidirectional flow.** Promotion is not one-way. Material  in Layer C could be brought back to Layer B for further  development, then re-promoted. Material in Layer B could be  extracted to chat for …

---

_...и ещё 145 пар._

> Файлы не удалялись автоматически. Проверьте вручную и удалите ненужные.

<!-- see-also -->

---

**Смотрите также:**
- [01-response-en](docs/nautilus/community-discussions/agent-changes-reality/01-response-en.md)
- [SOURCE_MAP](docs/SOURCE_MAP.md)
- [READING_TIME](docs/READING_TIME.md)
- [READABILITY](docs/READABILITY.md)

