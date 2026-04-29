# 13. Reference Implementation

> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Nautilus Portal Protocol v1.0.0-draft RFC (более ранняя версия v1.1).

## 13. Reference Implementation

Reference implementation: `github.com/svend4/nautilus`.

Reference НЕ является нормативной. Альтернативные implementations 
соответствуют NPP если они:

- Корректно парсят `nautilus.json` per раздел 3
- Реализуют BaseAdapter interface per раздел 6
- Вычисляют consensus per раздел 8
- Возвращают QueryResult per раздел 10

---
