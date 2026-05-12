# OpenCode (open-source coding agent)

**Автор:** @anomalyco  
**Хабр:** https://habr.com/ru/news/1013022/  
**GitHub:** https://github.com/anomalyco/opencode  
**Сайт:** https://opencode.ai  
**Слой:** developer-tools / coding-agent / CLI  
**Зрелость:** 126k+ звёзд на GitHub, production  
**Уникальность:** Полностью открытый coding agent в терминале: **не привязан к одному провайдеру**, поддерживает любые LLM. TypeScript + Bun. LSP-интеграция (понимание кода), git-интеграция, плагины. Возник как альтернатива Claude Code после того, как Anthropic заблокировал доступ через сторонние инструменты (январь 2026).

## Что умеет

- Редактирование файлов, выполнение команд, git-интеграция
- LSP-интеграция — понимает код как IDE (go-to-definition, references)
- Мультипровайдер: Claude, GPT, Gemini, локальные модели через ollama
- Плагины и экстеншны (awesome-opencode экосистема)
- Работает в терминале, без GUI

## Технический стек

```
TypeScript 55.2% + MDX 40.8% + CSS 3.1% + Rust 0.5%
Runtime: Bun
Install: npm i -g opencode-ai@latest
```

## Контекст появления

В январе 2026 Anthropic заблокировал использование подписок Claude через сторонние инструменты.  
OpenCode стал лучшей альтернативой: те же возможности, но мультипровайдерный.  
За 8 месяцев — один из самых популярных AI coding tools в мире.

## Почему важно для Lorenzo/Svyazi

Lorenzo использует Claude Code как основной интерфейс. OpenCode — прямая альтернатива.  
Мультипровайдерность + LSP = понимание 159 скриптов Lorenzo без SocratiCode.  
Применимо: запускать OpenCode с локальной моделью для бесплатного improve_*.py workflow.

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **OpenCode + SocratiCode (R08)** | LSP + граф зависимостей → максимальное понимание кодовой базы |
| **OpenCode + 9-агентный паттерн (R07)** | OpenCode с разными моделями для разных задач |
| **OpenCode + DevClaw (R06)** | GitHub Issues → OpenCode исполняет → PR без Claude Code |
| **OpenCode + openLight (R07)** | Skill catalog → OpenCode как исполнитель вместо CLI |

## Контакт

- GitHub: https://github.com/anomalyco/opencode
- npm: `npm i -g opencode-ai@latest`
- Хабр: https://habr.com/ru/news/1013022/
