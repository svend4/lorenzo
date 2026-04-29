# Комментарий: дизайн-решения NPP v1.0

> [!IMPORTANT]
> Ключевой документ для понимания архитектуры. Рекомендуется прочитать в первую очередь.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Nautilus Portal Protocol v1.0.0-draft RFC (более ранняя версия v1.1).

---
<!-- tags: security, architecture, anthropic, collaboration -->




> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Nautilus Portal Protocol v1.0.0-draft RFC (более ранняя версия v1.1).

Комментарий к документу

Несколько слов о том, что я сознательно сделал в этом draft:

Стиль написан как реальная W3C/IETF specification. С разделами MUST/SHOULD/MAY, numbered sections, glossary, appendix'ами, ADR'ами. Это даёт документу серьёзный вид в глазах внешних читателей (researchers, open-source maintainers) и одновременно операционную полезность: каждое MUST можно превратить в unit test.

Я включил два раздела, которых не было в embedded README. Первое — ADR-001 с явным обоснованием federation vs merging. Второе — раздел 11 Security Considerations, где явно обозначена проблема с приватными репо (это прямо связано с вашими soz* репо). Оба раздела добавляют защиту от критики в будущих review и подачах — всегда спрашивают «почему именно так?» и «как насчёт безопасности?»

Три поля в схеме registry, которые я формализовал явно: angle, compatibility_level, bridges. В embedded-версии они упоминались, но без строгой схемы. Теперь они — нормативные.

В разделе 8 consensus я намеренно сделал v1.0 простым (string matching). Это важно: спецификация должна быть простой и реализуемой, а сложные алгоритмы (embeddings, semantic similarity) — отнесены в v2.0. Это следует принципу «worse is better» и предотвращает застревание на perfect algorithm вместо рабочей системы.

Appendix A с minimal working example — это критично. Внешний читатель должен быть способен посмотреть на 30 строк кода и понять, что такое адаптер. Без этого спецификация слишком абстрактна.

Чего тут нет сознательно:

Нет описания MCP-интерфейса. Это отдельное расширение протокола, и оно должно жить в отдельном документе (MCP-EXTENSION.md в v1.1), чтобы не смешивать core protocol и transport layer.

Нет описания glyph_adapter.py роли. Это внутренняя деталь вашей реализации, не часть протокола. Если позже станет ясно, что glyph-адаптеры — это обобщённый концепт (мета-адаптер над native-адаптерами), это попадёт в v1.1 как formal concept.

Нет UI/UX specification. Web interface, CLI format output — это implementation details reference portal, не нормативные.

Что сделать с этим документом:

Сохранить в github.com/svend4/nautilus/PORTAL-PROTOCOL.md

Добавить ссылку из README standalone-репо

Прочитать целиком, отметить места, где нужна доработка под ваши реалии (например, пересмотреть compatibility levels если нужны другие категории)

Использовать как reference для написания адаптеров и для обсуждений с external contributors

Готов переходить ко второму артефакту — passport-шаблонам для info1/pro2/meta. Они будут существенно короче (1 страница каждый), human-readable, и опираются на разделы 4 и 15 этого PORTAL-PROTOCOL. Делаю?

Du hast gesagt: Да

<!-- see-also -->

---

**Смотрите также:**
- [34-appendix-b-change-log](docs/02-anthropic-vacancies/34-appendix-b-change-log.md)
- [03-registry](docs/nautilus/npp-v1-1/03-registry.md)
- [07-portal-entry](docs/nautilus/npp-v1-1/07-portal-entry.md)
- [22-glossary](docs/nautilus/npp-v1-1/22-glossary.md)

