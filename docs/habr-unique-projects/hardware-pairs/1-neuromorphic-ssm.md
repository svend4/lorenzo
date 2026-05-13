# Пара 1 — Нейроморфные процессоры × State Space Models (Mamba)

<!-- toc-auto -->
## Contents

- [Использование](#использование)
- [Смотрите также](#смотрите-также)
- [Кто ссылается на этот документ (3)](#кто-ссылается-на-этот-документ-3)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Поиск уникальных проектов на Хабре для совместной разработки - Claude` (корень репозитория).
**Проекты:** Svyazi, Yodoca

---
<!-- tags: memory, knowledge, ingestion, collaboration -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.





> Источник: MHTML‑снимок `Поиск уникальных проектов на Хабре для совместной разработки - Claude` (корень репозитория).

Понял идею. Соберу пять hardware-near родительских пар, от каждой — веер детей с разными нишами. Везде пары устроены так, что одна технология даёт «биологию» (что считаем), вторая — «физику» (как считаем), а от их скрещивания рождается несколько по-разному ориентированных потомков.

Пара 1. Нейроморфные процессоры × State Space Models (Mamba/Mamba-2)

Родители: нейроморфные чипы с STDP-пластичностью (российский «Алтай», Intel Loihi, IBM TrueNorth, BrainScaleS, SpiNNaker — habr.com/ru/companies/yadro/articles/648119/) и селективные SSM (Mamba — habr.com/ru/articles/786278/, habr.com/ru/companies/sberdevices/articles/855080/). Биология: spike-timing-dependent plasticity и разреженные импульсные сети дают энергоэффективность в 1000× по сравнению с GPU. Физика: Mamba с её селективным state evolution — это уже почти recurrent dynamics, которые просто просятся в spike-форму.

Дети:

Spiking Mamba — селективные параметры (A, B, C, Δ) как зависящие от входа функции реализуются прямо синапсами мемристорного crossbar'а; STDP заменяет градиентное обучение selective scan; consolidation идёт сама собой через долговременную пластичность. Это ребёнок про длинный контекст + энергоэффективность + in-memory computing.

Hardware-Hebbian Svyazi — то, что в прошлых ответах было «хеббовский граф людей-навыков-идей», физически живёт в crossbar мемристоров: участник сообщества = нейрон, связь = синапс, со-активация двух участников при упоминании одной темы физически усиливает их синапс. «Карточка коллаборации» Wi-Fi-инженера с питерским разработчиком — это просто потенциация одного синапса до порога выявляемости.

Spike-driven consolidator — Yodoca-style ночная консолидация эпизодов в долговременные факты, но без LLM-агента-консолидатора: эпизоды бьют импульсами в SNN, стабильные паттерны активации сами кристаллизуются как факты. Снимает основную стоимость Yodoca (вызовы консолидаторской LLM ночью), потому что физика дешевле LLM на четыре порядка.

<!-- see-also -->

---

## Использование
```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "Пара 1 Нейроморфные процессоры State"
```

## Смотрите также
- [6-bonus-rram-memristor](6-bonus-rram-memristor.md)
- 5-tinyml-[mcp-skills](5-tinyml-mcp-skills.md)
- [4-riscv-privacy](4-riscv-privacy.md)
- [01-yodoca](../key-findings/01-yodoca.md)


<!-- backlinks -->

---

## Кто ссылается на этот документ (3)
- [components-by-name](../../glossary/components-by-name.md)
- [concepts](../../glossary/concepts.md)
- [README](README.md)


<!-- similar-docs -->

---

**Похожие документы:**
- [1-neuromorphic-ssm](../../obsidian/habr-unique-projects/hardware-pairs/1-neuromorphic-ssm.md) (сходство 0.97)
- [5-tinyml-mcp-skills](5-tinyml-mcp-skills.md) (сходство 0.20)
- [5-tinyml-mcp-skills](../../obsidian/habr-unique-projects/hardware-pairs/5-tinyml-mcp-skills.md) (сходство 0.19)

