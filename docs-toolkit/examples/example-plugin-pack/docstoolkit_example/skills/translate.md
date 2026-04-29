# translate

Переводит документ между ru/en (демо-скилл из example plugin pack).

## Когда использовать

- "переведи документ"
- "translate this file"
- "сделай RU версию"
- "make EN version"

## Шаги

1. Определить язык исходника через `detect_language`
2. Если RU → перевести на EN, и наоборот
3. Сохранить в `<original>.<target_lang>.md`
4. Обновить frontmatter: `language: <new_lang>`, `translated_from: <orig>`

## Связанные скилы
- [`search`](../search.md) — найти документы для перевода
