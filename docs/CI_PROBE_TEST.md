# CI Probe Test

Тестовый файл для проверки, что workflow-фикс работает корректно:
push в feature-ветку `claude/**` НЕ должен запускать GitHub Actions.

- Дата: 2026-05-14
- Ветка: `claude/debug-hanging-issue-0AzoY`
- Ожидаемое поведение: ни одного check-run после этого коммита
- Если CI всё-таки запустился — значит триггер `claude/**` где-то остался
