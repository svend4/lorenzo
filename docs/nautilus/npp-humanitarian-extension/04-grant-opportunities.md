---
state: approved
---

# Horizon Europe Cluster 3 — Civil Security for Society — пересекается с «access t…

<!-- toc-auto -->
## Contents

- [Содержание](#содержание)
- [Использование](#использование)
- [Смотрите также](#смотрите-также)


<!-- toc -->
## Содержание

- [Contents](#contents)
- [Использование](#использование)
- [Смотрите также](#смотрите-также)

---


> [!TIP]
> Документ содержит практические рекомендации и лучшие практики.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — применение NPP к гуманитарным документам (юридические, социальные).

---
<!-- tags: architecture, roadmap, anthropic, collaboration -->




> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — применение NPP к гуманитарным документам (юридические, социальные).

Horizon Europe Cluster 3 — Civil Security for Society — пересекается с «access to social rights»

Mozilla Foundation Fellowships — open-source tooling для гражданской инфраструктуры

German Ministry of Justice digital grants — Digitale Justiz Initiative

Aktion Mensch — поддерживает disability-related tech specifically. Для вашего профиля (GdB 70, личный опыт Sozialgericht proceedings) это выглядит очень естественно.

Ваше сочетание экспертизы (active Sozialgericht proceedings, deep SGB IX/XII/SGG knowledge, существующая Writing OS с 300+ tools) + технических возможностей (70 репозиториев, Claude Code workflow, трёхфазная review methodology) + уникальная disability-informed perspective — это defensible moat для такого проекта, которого не будет у обычных legal-tech стартапов.

9. Практический roadmap для humanities-extension Nautilus

Если решите двигаться в эту сторону, вот как это может выглядеть поэтапно:

Фаза 1 — Proof of Concept (2 недели). Создать legal-nautilus как fork от svend4/nautilus. Написать один адаптер — SGBAdapter — для одной книги SGB (например, SGB XII). Использовать открытые публичные тексты законов с www.gesetze-im-internet.de. Проверить, что цепочка работает: query → adapter → PortalEntry → MCP → Claude Desktop отвечает на юридический вопрос. Deliverable: работающий MCP server с одним legal-адаптером.

Фаза 2 — Multiple Legal Sources (4 недели). Расширить до 4-5 адаптеров: SGB XII, SGG, Dresden-SG-decisions (public те, что доступны), Sozialamt-schemas, ICD-10-mapping. Это уже демонстрация federated legal knowledge. Deliverable: публичный demo на конкретных социальных кейсах.

Фаза 3 — Private Case Files (4 недели). Добавить адаптеры для ваших приватных soz* репо. Реализовать auth layer, encryption-at-rest, audit log. Это превращает Nautilus из demo в рабочий tool для вашей практики. Deliverable: вы используете Legal-Nautilus в реальной работе над S 6 SO 58/26 ER.

Фаза 4 — Extension to General Humanities (ongoing). Добавить адаптеры для medical reports (ICD-10), educational records, institutional profiles. Это делает проект не только "legal", а humanities knowledge federation.

Фаза 5 — Public Launch & Grant Applications (после Фазы 3). Paper в arxiv + Show HN + submission в EIC Pathfinder или Aktion Mensch. Deliverable: externally visible project with funding track.

10. Конкретный следующий шаг, если заинтересовало

Могу сделать прямо сейчас одну из трёх вещей:

Первое — написать PORTAL-PROTOCOL-HUMANITIES-EXTENSION.md — informative приложение к NPP v1.1, которое формализует всё выше описанное: humanity-specific format types, conventional metadata keys, temporal metadata ADR, Q6 mapping example, GDPR considerations. Это 10–15 страниц formal-stile документа, который может идти вместе с основным PORTAL-PROTOCOL.md. Полезно для arxiv-paper или grant application.

Второе — написать SGBAdapter.py как reference implementation — рабочий адаптер для одной книги SGB, подключающийся к публичным текстам с gesetze-im-internet.de. Это ~200 LOC Python + passport. Полезно как proof-of-concept.

Третье — набросок grant application — структурированный пропозал для одной из программ (EIC Pathfinder, Aktion Mensch, Horizon Europe), увязывающий Nautilus-core + humanities-extension + ваш личный disability-context. Полезно, если видите в этом возможность реальной монетизации работы.

<!-- see-also -->

---

## Использование
```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "Horizon Europe Cluster 3 Civil Security"
```

## Смотрите также
- [04-what-i-can-do-now](../privacy-federation/04-what-i-can-do-now.md)
- [03-what-this-gives-technically](../privacy-federation/03-what-this-gives-technically.md)
- [03-what-doesnt-exist-on-market](03-what-doesnt-exist-on-market.md)
- [04-proposed-infrastructure](../okwf-concept/04-proposed-infrastructure.md)


<!-- backlinks -->

---

**Кто ссылается на этот документ (9):**
- [CONCEPTS](../../CONCEPTS.md)
- [OUTLINE](../../OUTLINE.md)
- [READABILITY](../../READABILITY.md)
- [READING_TIME](../../READING_TIME.md)
- [SEARCH](../../SEARCH.md)
- [README](README.md)
- [02-two-tier-publication](../privacy-federation/02-two-tier-publication.md)
- [03-what-this-gives-technically](../privacy-federation/03-what-this-gives-technically.md)
- _...ещё 1_


<!-- similar-docs -->

---

**Похожие документы:**
- [04-grant-opportunities](../../obsidian/nautilus/npp-humanitarian-extension/04-grant-opportunities.md) (сходство 0.99)
- [04-what-i-can-do-now](../privacy-federation/04-what-i-can-do-now.md) (сходство 0.23)
- [04-what-i-can-do-now](../../obsidian/nautilus/privacy-federation/04-what-i-can-do-now.md) (сходство 0.23)

