# 5. Four Integration Paths in Order of Accessibility

<!-- summary -->
> We identify four paths from most-immediate to most-mature.

---

<!-- toc -->
## Содержание

- [5. Four Integration Paths in Order of Accessibility](#5-four-integration-paths-in-order-of-accessibility)
  - [5.1. Path 1 — InGit Project in Cowork (Immediate)](#51-path-1-ingit-project-in-cowork-immediate)
  - [5.2. Path 2 — InGit MCP Server (Short-Term)](#52-path-2-ingit-mcp-server-short-term)
  - [5.3. Path 3 — InGit Cowork Project Template (Medium-Term)](#53-path-3-ingit-cowork-project-template-medium-term)
  - [5.4. Path 4 — Deep Cowork Integration (Long-Term)](#54-path-4-deep-cowork-integration-long-term)
  - [5.5. Sequencing Logic](#55-sequencing-logic)

---

<!-- tags: rag, orchestration, architecture, anthropic -->




## 5. Four Integration Paths in Order of Accessibility

We identify four paths from most-immediate to most-mature.

### 5.1. Path 1 — InGit Project in Cowork (Immediate)

**No development required. Available now.**

Steps:
1. Open Claude Desktop Cowork tab
2. Create new Project, "Start from scratch"
3. Point Project at existing InGit folder (or empty folder 
   with InGit structure)
4. Add custom instructions describing InGit conventions
5. Add reference documents explaining InGit philosophy
6. Begin work

**What works**:
- Cowork reads InGit structure
- Custom instructions inform Cowork of conventions
- Cowork can create/edit files following conventions
- Persistent memory builds Project knowledge
- Git operations work through shell commands

**What's missing**:
- No automatic validation (Cowork might create invalid YAML)
- No InGit-specific operations
- Manual Git workflow

**Effort**: One day to set up. Zero ongoing development.

**Recommendation**: **Do this now**. Use it for current 
Nautilus/OKWF document series. Generates immediate learning 
about what works and what's missing.

### 5.2. Path 2 — InGit MCP Server (Short-Term)

**Development required. 2-4 weeks for basic version.**

Build `ingit-mcp-server` exposing InGit operations:

```
Knowledge Base operations:
- ingit_search_wiki(query)
- ingit_read_document(path)
- ingit_create_document(template, metadata, content)
- ingit_list_recent_documents(days)
- ingit_get_document_metadata(path)

Task operations:
- ingit_list_tasks(filters)
- ingit_create_task(metadata, description)
- ingit_update_task(id, updates)
- ingit_decompose_task(id, subtasks)

Validation operations:
- ingit_validate_yaml(content, schema)
- ingit_validate_project_structure(path)

Git operations:
- ingit_commit(message, files)
- ingit_get_recent_changes(days)
- ingit_branch(name, from)

Project operations:
- ingit_get_project_structure()
- ingit_create_subproject(name, type)
```

Cowork users add this MCP server to their Project. Cowork 
calls these tools instead of generic file operations.

**What works that Path 1 doesn't**:
- Validation enforced automatically
- InGit-specific operations available
- Domain knowledge encapsulated in server
- Cleaner Cowork instructions (less convention explanation)

**Effort**: 2-4 weeks development. Open source release.

**Recommendation**: **Begin after one month of Path 1 usage**. 
Real usage informs MCP tool design. Avoid premature design.

### 5.3. Path 3 — InGit Cowork Project Template (Medium-Term)

**Requires Anthropic to expose Project template API publicly.**

Once Anthropic enables third-party Project templates, InGit 
publishes template:
- Pre-configured folder structure
- Pre-written custom instructions
- Optional pre-installed MCP server
- Sample content explaining conventions
- Quick start documentation

Users get working InGit + Cowork setup in one click.

**What works that Path 2 doesn't**:
- Massive reduction in setup friction
- Discoverable by Cowork users
- Standard configuration across users
- Easier to share between team members (when team sharing 
  available)

**Effort when API available**: 1-2 weeks for template 
creation.

**Recommendation**: **Watch for API availability**. Anthropic 
will likely enable this; timing uncertain. Be ready when it 
opens.

### 5.4. Path 4 — Deep Cowork Integration (Long-Term)

**Speculative, depends on Cowork API maturation.**

When Cowork exposes deeper APIs:
- Custom UI elements within Cowork
- Cowork-aware validation flow
- Native InGit task integration
- Shared memory across Cowork and InGit operations
- Cooperative scheduling

This is most ambitious. Requires Anthropic to enable 
substantial third-party extension. Timing entirely outside 
InGit author's control.

**Effort when possible**: 3-6 months for full integration.

**Recommendation**: **Don't plan around this**. Take 
opportunities as they arise. Don't depend on it.

### 5.5. Sequencing Logic

The four paths are not parallel options. They are sequential, 
each building on the previous:

- Path 1 generates **usage learning**
- Path 2 builds **automation** based on learning
- Path 3 enables **distribution** when API available
- Path 4 deepens **integration** when API matures

Skipping ahead is risky. Path 2 without Path 1 risks designing 
wrong tools. Path 3 without Path 2 has no value to package. 
Path 4 without ecosystem risks depending on capabilities not 
yet available.

Sequential progression maximizes value at each stage and 
defers complex decisions until evidence is available.

---

<!-- similar-docs -->

---

**Похожие документы:**
- [311-3-what-ingit-provides-that-cowork-lacks](docs/02-anthropic-vacancies/311-3-what-ingit-provides-that-cowork-lacks.md) (сходство 0.16)
- [310-2-what-cowork-provides-that-ingit-doesn-t-need-to-](docs/02-anthropic-vacancies/310-2-what-cowork-provides-that-ingit-doesn-t-need-to-.md) (сходство 0.15)
- [309-1-the-cowork-discovery-and-why-it-changes-everythi](docs/02-anthropic-vacancies/309-1-the-cowork-discovery-and-why-it-changes-everythi.md) (сходство 0.15)


<!-- see-also -->

---

**Смотрите также:**
- [314-6-refined-ingit-scope-with-cowork-in-mind](docs/02-anthropic-vacancies/314-6-refined-ingit-scope-with-cowork-in-mind.md)
- [311-3-what-ingit-provides-that-cowork-lacks](docs/02-anthropic-vacancies/311-3-what-ingit-provides-that-cowork-lacks.md)
- [310-2-what-cowork-provides-that-ingit-doesn-t-need-to-](docs/02-anthropic-vacancies/310-2-what-cowork-provides-that-ingit-doesn-t-need-to-.md)
- [315-7-practical-first-steps-this-month](docs/02-anthropic-vacancies/315-7-practical-first-steps-this-month.md)

<!-- backlinks-auto -->
## Упоминается в

- [Вакансии Anthropic — Анализ по кластерам](docs/02-anthropic-vacancies/README.md)

<!-- related-auto -->
## Связанные документы

- [1. The Cowork Discovery and Why It Changes Everything](docs/02-anthropic-vacancies/309-1-the-cowork-discovery-and-why-it-changes-everythi.md) _37%_
- [2. What Cowork Provides That InGit Doesn't Need to Build](docs/02-anthropic-vacancies/310-2-what-cowork-provides-that-ingit-doesn-t-need-to-.md) _33%_
- [3. What InGit Provides That Cowork Lacks](docs/02-anthropic-vacancies/311-3-what-ingit-provides-that-cowork-lacks.md) _33%_
- [6. Refined InGit Scope with Cowork in Mind](docs/02-anthropic-vacancies/314-6-refined-ingit-scope-with-cowork-in-mind.md) _33%_
- [4. The Symbiotic Architecture](docs/02-anthropic-vacancies/312-4-the-symbiotic-architecture.md) _29%_
- [7. Practical First Steps This Month](docs/02-anthropic-vacancies/315-7-practical-first-steps-this-month.md) _29%_
- [Приложение: Визуализация позиции в серии](docs/02-anthropic-vacancies/303-приложение-визуализация-позиции-в-серии.md) _25%_
- [Table of Contents](docs/02-anthropic-vacancies/308-table-of-contents.md) _25%_
