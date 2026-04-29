# packages/

Этот каталог зарезервирован для workspace-пакетов монорепозитория. Сейчас он пустой — добавляйте сюда отдельные пакеты по мере появления кода.

Пример будущей структуры:

```
packages/
├── svyazi-core/         # ядро CardIndex и normalization
├── svyazi-evidence/     # evidence envelope + viewer
├── svyazi-memory/       # memory layer (NGT/Yodoca-стиль)
├── svyazi-orchestrator/ # multi-agent orchestration
└── svyazi-ui/           # пользовательский интерфейс
```

Корневой `package.json` уже содержит `workspaces: ["packages/*"]` и `pnpm-workspace.yaml`. Любой пакет, добавленный сюда с собственным `package.json`, автоматически попадёт в workspace.
