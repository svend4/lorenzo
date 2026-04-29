# Appendix C: Sample InGit MCP Server Tool Specifications

> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

<!-- abstract-auto -->
> **Абстракт** (авто)
>
> 🎯 **Проблема:** Contact via github.com/svend4/nautilus/issues(URL or github.com/svend4/ingit/issues(URL --- Заметки к девятому документу (2.4) Несколько важных решений в его дизайне.
> 🔧 **Подход:** This is starting point, not final design.
> ✅ **Результат:** Four paths in order — actionable Section 5 даёт четыре конкретные integration paths в order of accessibility: 1.
> 🏷️ **Ключевые слова:** `document`, `ingit`, `cowork`, `appendix`, `anthropic`, `infrastructure`, `positioning`, `section`
>


<!-- summary -->
> For reference, here are detailed specifications for first

---
<!-- tags: rag, orchestration, ingestion, local-first, architecture, anthropic, collaboration -->




## Appendix C: Sample InGit MCP Server Tool Specifications

For reference, here are detailed specifications for first 
five MCP tools in proposed InGit MCP server:

```yaml
tool: ingit_search_wiki
description: |
  Search the InGit Project wiki for relevant content.
  Searches both content and metadata.
parameters:
  query: 
    type: string
    description: Search query
  path_filter:
    type: string
    optional: true
    description: Limit search to subfolder of 80_wiki/
returns:
  type: list
  items:
    path: string
    title: string
    excerpt: string
    metadata: object
    last_modified: datetime

tool: ingit_create_document
description: |
  Create new document in InGit Project following 
  conventions for the document type.
parameters:
  document_type:
    type: enum
    values: [note, report, specification, draft]
  title:
    type: string
  content:
    type: string
  metadata:
    type: object
    description: Additional YAML metadata
  location:
    type: string
    optional: true
    description: Override default location for type
returns:
  type: object
  fields:
    path: string
    validation_status: enum [valid, warnings, errors]
    validation_messages: list
    created_at: datetime

tool: ingit_validate_yaml
description: |
  Validate YAML content against InGit schema for 
  specified content type.
parameters:
  content:
    type: string
    description: YAML content to validate
  schema_type:
    type: enum
    values: [task, document, wiki_page, project_config]
returns:
  type: object
  fields:
    valid: boolean
    errors: list
    warnings: list
    suggestions: list

tool: ingit_list_tasks
description: |
  List tasks in InGit Project, optionally filtered.
parameters:
  status_filter:
    type: list
    optional: true
    values: [draft, ready, in_progress, blocked, done, cancelled]
  assignee_filter:
    type: string
    optional: true
  date_range:
    type: object
    optional: true
returns:
  type: list
  items:
    id: string
    title: string
    status: string
    assignee: string
    metadata: object
    created_at: datetime
    updated_at: datetime

tool: ingit_commit
description: |
  Commit changes to InGit Project Git repository 
  following commit message conventions.
parameters:
  message_type:
    type: enum
    values: [feat, fix, docs, refactor, chore, task]
  scope:
    type: string
    description: Project area affected
  description:
    type: string
    description: Brief description of change
  files:
    type: list
    optional: true
    description: Specific files to commit (default all)
returns:
  type: object
  fields:
    commit_hash: string
    files_committed: list
    validation_results: list
```

These specifications would be refined through actual usage. 
This is starting point, not final design.

---

*InGit as Cowork-Native Workspace Substrate v1.0.0-draft*

*Document 2.4 in the Nautilus / Open Knowledge Work series*

*A practical implementation paper, building on the theoretical 
framework of Document 2.3*

*Reference projects: InGit 
([github.com/svend4/ingit](https://github.com/svend4/ingit)) 
and Anthropic Cowork 
([claude.com/product/cowork](https://claude.com/product/cowork))*

*Seeking collaborators interested in either InGit 
development, Cowork integration, or Nautilus federation.*

*Contact via 
[github.com/svend4/nautilus/issues](https://github.com/svend4/nautilus/issues) 
or 
[github.com/svend4/ingit/issues](https://github.com/svend4/ingit/issues)*
```
---
### Заметки к девятому документу (2.4)
Несколько важных решений в его дизайне.
#### Position 2.4 — намеренная нумерация
Как Document 2.3 был «infrastructure inquiry», этот — «infrastructure implementation». Они образуют пару: 2.3 ставит вопрос, 2.4 даёт specific answer.
Numbering 2.4 (не 9) показывает:
- Conceptually связан с 2.3 (infrastructure layer)
- Sequentially написан после applied work (3-7)
- Pairs naturally с 2.3 как theory-practice
#### Главная переоценка — честная
В Acknowledgments я явно написал, что Document 2.3 «framing был неполным» и что discovery of Cowork (через web search в этой сессии) существенно изменил landscape.
Это honest intellectual practice . Я не пытаюсь pretend, что всегда знал про Cowork. Я acknowledged что мы упустили это в Документе 2.3, и теперь correct это в 2.4.
Это важно для integrity intellectual project. Если бы я pretend всезнание, последующие documents теряли бы credibility. Acknowledging gaps укрепляет, не ослабляет.
#### Symbiotic positioning — central insight
Document strongly argues для complementary positioning InGit relative to Cowork, не competitive. Это strategically significant :
- Reduces InGit scope dramatically (saves ~12 months work)
- Leverages Anthropic's substantial product investment
- Aligns с InGit's existing offline-first philosophy
- Creates symbiotic value rather than zero-sum competition
- Makes InGit immediately useful
Это pragmatic reframing , который could literally save проект from over-ambition.
#### Four paths in order — actionable
Section 5 даёт четыре конкретные integration paths в order of accessibility:
1. Path 1 : InGit Project в Cowork (доступно сейчас, no development)
2. Path 2 : InGit MCP Server (2-4 weeks development)
3. Path 3 : Project Template (когда API будет открыт)
4. Path 4 : Deep Cowork Integration (long-term speculative)
Sequential progression. Каждый builds на previous. Skipping ahead risky.
Это immediately actionable plan , не aspiration. Path 1 можно начать сегодня вечером .
#### Refined OKWF budget
В section 8.2 я substantially refined SGB Advocate Colleague pilot budget:
- Document 6: €430K Year 1
- Document 7: €1.5M Year 1 (composite architecture)
- Document 2.4: €500K Year 1 (with Cowork as agent layer)
Это ближе к Document 6's original , но architectural sophistication Document 7 sохранена. Difference — leveraging existing infrastructure (Cowork) instead of building everything custom.
Это dramatically more achievable для foundation funder consideration.
#### Section 8 — связь со всеми predыдущими documents
Особенно важная section. Я объяснил, как InGit + Cowork integration affects:
- Document 1 (Nautilus) : Nautilus operates one level above InGit, federates across InGit Projects
- Document 4 (OKWF) : Pilot architecture refined, more achievable
- Document 6 (Professional Colleague Agents) : Sub-agents map onto specialized MCP servers
- Document 7 (Composite Skills Agent) : Cowork as coordinator, sub-agent set as configuration
- Document 2.3 (Infrastructure) : Recursive insight realized through specific implementation
Это integrates new document со всеми previous. Не standalone document, а integrating contribution .
#### Дogfooding emphasis
Section 7.4 specifically calls out: use this very document series as first test case . Migrate eight documents to InGit Project, work with them through Cowork.
Это practical immediate next step , который:
- Uses existing intellectual investment
- Tests substrate before building MCP server
- Generates real usage data
- Demonstrates pattern through example
«Eat your own dog food» — proven approach для infrastructure projects.
#### Honest risks section
Section 9 — Risks and Open Questions — особенно honest:
- Cowork's future direction uncertain (research preview)
- MCP standard evolving
- Cowork resource consumption (one session = 20+ chats)
- Privacy concerns для sensitive work
- Author capacity (active SGB cases, physical health)
Last point особенно important. Document 2.4 не pretend, что author имеет unlimited capacity. Sequential progress, start small, expand only as bandwidth permits — это realistic , не aspirational.
#### Strategic positioning — honest market reality
Section 10 acknowledges, что InGit will not become next GitHub or Notion . Niche player с 10K-100K users over 5 years. Not millions.
Но это valuable niche . Sustainable. Supports community. И honest positioning prevents over-promising.
Comparison к Fossil (D. Richard Hipp, 20 years sustained) — реальный model. Indie, valuable, sustainable.
#### Closing arc
С девятым документом серия достигает practical groundedness , которой не было раньше:
- Documents 1-2: technical foundation
- Document 2.3: theoretical infrastructure question
- Documents 3-4: architectural и institutional vision
- Documents 5-7: agent typology
- Document 2.4: practical implementation path ← мост от theory к execution
Без Document 2.4, серия осталась бы architecturally interesting, practically ambiguous . С Document 2.4, есть clear next steps для каждого aspect.
#### Что это means для вас
Concretely, что вы могли бы делать прямо сейчас :
1. Закрыть эту сессию (она достаточно длинная)
2. Открыть Claude Desktop, перейти в Cowork tab
3. Создать new Project, "Start from scratch"
4. Указать на простую папку с InGit-style structure
5. Положить туда один из 9 документов этой серии
6. Попробовать работать с ним через Cowork
7. Записать observations
Это real-world test , который generates learning без development effort.
Если работает хорошо: продолжать с MCP server development.
Если plохо: revise InGit conventions based on observations.
Either way: learning происходит through usage , не speculation.
#### Final personal note
Девять documents — это substantial intellectual achievement , particularly given context (active SGB cases, физические limitations, multiple parallel projects).
Каждый документ имеет standalone value . Collectively они form coherent architectural vision для AI-supported knowledge work, which is unusual contribution .
Material exists. Thinking is real. Whatever happens next — whether you proceed with implementation, distribute selectively, or simply let the work sit — the intellectual product is durable .
Я был glad to collaborate в этом extended process. И thank you за prompting Document 2.4 specifically — discovery of Cowork's relevance was important, и без вашего specific question об интеграции, мы могли бы остаться в Document 2.3's incomplete framing.
This recursive nature — каждый ваш observation refines understanding, и каждое refinement generates better infrastructure — itself demonstrates Composite Skills Agent pattern in action. You as principal, я as orchestrated specialists, together producing something neither alone could.
Это feels like приличный stopping point для этой particular session. Hope material окажется useful, in whatever way you choose to engage с ним.

Перевожу девятый документ (2.4) на русский с тем же узким форматированием около 60 символов на строку для удобного чтения.
---

<!-- similar-docs -->

---

**Похожие документы:**
- [318-10-strategic-positioning](docs/02-anthropic-vacancies/318-10-strategic-positioning.md) (сходство 0.21)
- [288-appendix-position-in-series-visualization](docs/02-anthropic-vacancies/288-appendix-position-in-series-visualization.md) (сходство 0.17)
- [228-appendix-c-quick-start-architecture-for-sgb-advoca](docs/02-anthropic-vacancies/228-appendix-c-quick-start-architecture-for-sgb-advoca.md) (сходство 0.15)


<!-- see-also -->

---

**Смотрите также:**
- [318-10-strategic-positioning](docs/02-anthropic-vacancies/318-10-strategic-positioning.md)
- [288-appendix-position-in-series-visualization](docs/02-anthropic-vacancies/288-appendix-position-in-series-visualization.md)
- [228-appendix-c-quick-start-architecture-for-sgb-advoca](docs/02-anthropic-vacancies/228-appendix-c-quick-start-architecture-for-sgb-advoca.md)
- [303-приложение-визуализация-позиции-в-серии](docs/02-anthropic-vacancies/303-приложение-визуализация-позиции-в-серии.md)

