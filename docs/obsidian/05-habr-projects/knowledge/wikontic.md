---
title: "Wikontic: семантический граф"
tags:
  - ingestion
  - collaboration
  - habr-projects
date: 2026-05-11
---

# Wikontic: семантический граф

<!-- toc-auto -->
## Contents

- [Статус](#статус)
- [Похожие документы](#похожие-документы)
- [Использование](#использование)
- [Смотрите также](#смотрите-также)
- [Упоминается в](#упоминается-в)
- [Упоминается в](#упоминается-в-1)
- [Связанные документы](#связанные-документы)
- [Связанные документы](#связанные-документы-1)
- [Кто ссылается на этот документ (3)](#кто-ссылается-на-этот-документ-3)


> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

<!-- abstract-auto -->
> **Абстракт** (авто)
>
> 🎯 **Проблема:** Решает буквально тот же класс проблем, что у Чуяна на слое 3 (нормализация — kubernetes / k8s / кубер → одна сущность), но не через ручной skillssynonyms.yml , а через автоматическ
> 🏷️ **Ключевые слова:** `projects`, `memory`, `readme`, `yodoca`, `wikontic`, `https`, `companies`, `articles`
>


<!-- autofill-status -->
## Статус

| Параметр | Значение |
|----------|---------|
| Теги | — |
| Упоминаний в репо | 90 |
| Слой | knowledge/graph |
| Контакт | [[vitalyoborin|@VitalyOborin]] |
| Статус связи | не писали |

_Обновлено: 2026-04-29_


<!-- summary -->
> Wikontic — Алла Чепурова (AIRI, лаборатория Cognitive AI Systems) https://habr.com/ru/companies/airi/articles/1000720/ И её более ранняя статья: https://habr.com/ru/companies/airi/articles/855128/ Пай
**Проекты:** Wikontic

---
<!-- tags: ingestion, collaboration -->




Wikontic — Алла Чепурова (AIRI, лаборатория Cognitive AI Systems) https://habr.com/ru/companies/airi/articles/1000720/ И её более ранняя статья: https://habr.com/ru/companies/airi/articles/855128/ Пайплайн построения графов знаний из текста с использованием онтологии Wikidata, дедупликацией и типизацией сущностей. Решает буквально тот же класс проблем, что у Чуяна на слое 3 (нормализация — kubernetes / k8s / кубер → одна сущность), но не через ручной skills_synonyms.yml , а через автоматическую сверку с онтологией. У Чуяна — справочник на сотню строк, который он дополняет вручную; Алла построила то, что делает это автоматически.
3.

<!-- similar-docs -->

---

## Похожие документы
- [[README]] (сходство 0.19)
- [[ngt-memory]] (сходство 0.10)


<!-- see-also -->

---

## Использование
```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "Wikontic семантический граф"
```

## Смотрите также
- [[yodoca]]
- [[ngt-memory]]
- [[02-collaboration-partners]]
- [[01-synthesis]]

<!-- backlinks-auto -->
## Упоминается в

- [NGT[^ngt] Memory: ассоциативный граф](../memory/ngt-memory.md)
- [Yodoca[^yodoca]: консолидация и забывание](../memory/yodoca.md)
- [[02-collaboration-partners|Авторы и контакты]]
- [[01-synthesis|Синтез: как проекты собираются вместе]]
- [[README|Системы знаний]]
## Упоминается в

- [[README|Системы знаний]]

<!-- related-auto -->
## Связанные документы

- [[01-synthesis|Синтез: как проекты собираются вместе]] _29%_
- [NGT[^ngt] Memory: ассоциативный граф](../memory/ngt-memory.md) _29%_
- [Yodoca[^yodoca]: консолидация и забывание](../memory/yodoca.md) _25%_
- [[02-collaboration-partners|Авторы и контакты]] _21%_
- [[README|Уникальные проекты с Хабра]] _17%_
- [[README|Системы памяти]] _16%_
## Связанные документы

- [[README|Системы знаний]] _42%_
- [[01-synthesis|Синтез: как проекты собираются вместе]] _21%_
- [[README|Уникальные проекты с Хабра]] _21%_
- [NGT[^ngt] Memory: ассоциативный граф](docs/05-habr-projects/memory/ngt-memory.md) _21%_
- [[README|Системы памяти]] _17%_
- [Yodoca[^yodoca]: консолидация и забывание](docs/05-habr-projects/memory/yodoca.md) _17%_

<!-- backlinks -->

---

## Кто ссылается на этот документ (3)
- [[01-synthesis]]
- [[README]]
- [[yodoca]]

