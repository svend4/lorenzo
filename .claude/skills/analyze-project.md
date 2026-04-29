# Скилл: analyze-project

## Когда использовать
Когда пользователь спрашивает о конкретном компоненте проекта Svyazi:
- "Расскажи про AgentFS"
- "Что такое NGT-memory?"
- "Как работает SENTINEL?"
- "Какой статус у Yodoca?"

## Алгоритм

1. Найди файл компонента в `docs/05-habr-projects/` или `docs/04-ai-collaborations/ensembles/`
2. Прочитай его содержимое
3. Найди упоминания в `docs/ENTITIES.md`, `docs/CONCEPTS.md`, `docs/TAGS.md`
4. Проверь связи в `docs/NETWORK.md`
5. Найди оценку в `docs/SCORING.md`

## Формат ответа

```markdown
## {Название компонента}

**Тип:** OSS-проект / инструмент / протокол
**Лицензия:** MIT / Apache 2.0 / BSL 1.1
**Автор:** @github-handle

### Назначение
[1-2 предложения]

### Ключевые функции
- ...
- ...

### Место в Svyazi
[Как используется в ансамблях]

### Статус
[Активно / Экспериментально / Планируется]
```

## Полезные команды
```bash
python scripts/improve_entities.py   # обновить индекс сущностей
python scripts/improve_network.py    # обновить граф связей
```
