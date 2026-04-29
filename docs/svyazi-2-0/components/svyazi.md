# Svyazi

- **Автор:** Андрей Чуян
- **Источник:** Хабр citeturn41search0
- **Лицензия:** код закрыт. citeturn41search0
- **Maturity:** активный закрытый авторский прототип. citeturn41search0
- **Релевантность к Svyazi‑2.0:** очень высокая — это базовый ingest/normalize/discovery‑слой.

## Описание

Гибридная система извлечения структурированных профилей участников сообщества из свободного текста; уже показала кейс «карточек коллабораций».

## Ключевые компоненты и паттерны

- 6 слоёв (ingest, extract, normalize, dedup, index, discover)
- YAML
- SHA256‑дедупликация
- Ollama + Qwen
- LLM + детерминированный код
- CardIndex
- Privacy by design
