# Пассивный vs активный: разделение ролей (библиотека vs research team)

<!-- toc-auto -->
## Contents

- [Смотрите также](#смотрите-также)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — анализ комбинирования пассивного Nautilus с активным CAMEL framework.

---
<!-- tags: architecture, anthropic -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.





> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — анализ комбинирования пассивного Nautilus с активным CAMEL framework.

Сначала разделение ролей: пассивный vs активный

Вы точно identifuei разницу:

Nautilus — это passive coordination layer. Он собирает information across repositories, federates queries через Portal Protocol, но не executes ничего. Это infrastructure для discovery and federation, не для action. Метафора: библиотека с card catalog. Catalog tells вам где что находится, но не reads books для вас.

CAMEL — это active execution framework. Когда вы создаёте ChatAgent или RolePlaying setup, agents actively выполняют tasks: search the web, write code, analyze documents, coordinate с друг другом. Метафора: research team. Team actually does work.

Это complementary, не competing functions.

<!-- see-also -->

---

## Использование

```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "Пассивный vs активный разделение ролей"
```

## Смотрите также
- [00-question-camel-vs-nautilus](00-question-camel-vs-nautilus.md)
- [08-difference-3-federation-missing](../hermes-comparison/08-difference-3-federation-missing.md)
- [17-appendix-b-change-log](../../nautilus/npp-v1-0/17-appendix-b-change-log.md)
- [03-sgb-advocate-colleague-example](03-sgb-advocate-colleague-example.md)

Документ индексирован в базе знаний репозитория. Навигация возможна через семантический поиск и граф концептов репозитория Lorenzo. Материал доступен для семантического поиска, BM25-поиска и навигации через граф концептов. Используйте скрипты группы reports для получения актуальной статистики по разделу. Рекомендуется начинать с основных документов раздела и переходить к деталям через внутренние ссылки. Все связанные документы доступны через граф концептов и поисковый индекс репозитория Lorenzo. Документы раздела индексированы в поисковой базе и доступны для семантического поиска и BM25.
