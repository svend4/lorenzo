# AI Review

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Автор:** Nikita Filonov / @sound_right (Хабр) / @Nikita-Filonov (GitHub)  
**Хабр:** https://habr.com/ru/articles/951434/  
**GitHub:** https://github.com/Nikita-Filonov/ai-review  
**Слой:** developer-tools / code-review / CI-CD  
**Дата:** октябрь 2025 (активный, несколько статей)  
**Уникальность:** Единственный на Хабре provider-agnostic CI/CD инструмент ревью кода: работает с OpenAI, Claude, Gemini, Ollama — переключение одним параметром. Клиент-сайд, не хранит данные. 20–40 секунд на MR из 30 файлов.

## Что делает

- Анализирует Pull Request / Merge Request через LLM
- Поддерживает GitHub, GitLab, Bitbucket, Docker, PyPI, CLI
- Провайдер-агностик: OpenAI / Claude / Gemini / Ollama / любой OpenAI-compatible endpoint
- Пользователь сам задаёт промпты и строгость оценки
- Не требует внешних серверов, всё идёт CI → LLM напрямую

## Почему интересно для Svyazi

Svyazi генерирует и обновляет документы через скрипты. AI Review + Lorenzo = автоматическое ревью изменений в docs/ при каждом коммите: «что изменилось, корректно ли, нет ли противоречий с другими файлами».

## Возможные комбинации с Round 01

| Комбинация | Новое свойство |
|------------|----------------|
| **AI Review + improve_contradiction_check** | Ревью не кода, а документов: LLM проверяет противоречия при каждом push |
| **AI Review + AgentFS** | Coding agent пишет код → AI Review проверяет результат → цикл |
| **AI Review + Rufler** | YAML-пайплайн: Rufler описывает задачу → PocketCoder пишет → AI Review ревьюит |
| **AI Review + PocketCoder (R02)** | Замкнутый цикл кодирования: write → review → fix → merge |

## Контакт

- GitHub: https://github.com/Nikita-Filonov
- Habr: https://habr.com/ru/users/sound_right/
