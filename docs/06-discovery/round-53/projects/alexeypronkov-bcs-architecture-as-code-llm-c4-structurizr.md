---
date: 2026-06-05
tags: [orchestration, security, ingestion, architecture, anthropic]
state: normalized
---

# Architecture as Code + LLM: 5 ролей архитектурного ревью через Claude + Structurizr DSL

<!-- toc-auto -->
<!-- tags: alexeypronkov-bcs-architecture-as-code-llm-c4-structurizr, docs -->


<!-- summary -->
> `alexeypronkov-bcs-architecture-as-code-llm-c4-structurizr` — раздел документации проекта Lorenzo.


> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Автор:** AlexeyPronkov (Алексей Прончев, BCS FinTech AI)  
**Хабр:** https://habr.com/ru/companies/bcs_company/articles/1006944/  
**GitHub:** нет (production кейс)  
**Слой:** orchestration / knowledge  
**Дата:** март 2025  
**Уникальность:** Architecture as Code + LLM на уровне архитектурной документации, не MR-диффов: Claude Code + Structurizr DSL (C4 Model) + 5 кастомных скиллов-ревьюеров (Solution Architect, Enterprise Architect, Security Engineer, Business Analyst, Stakeholder). LLM валидирует C4-диаграммы в коде, генерирует ADR-черновики, резолвит Git merge conflicts в DSL-файлах. Цикл архревью: 2–3 недели → 1 неделя; автоматизация pre-review валидации ~98%.

## Проблема: архитектурный долг накапливается быстрее чем ревьюируется

```
BCS FinTech: финансовые сервисы, сложная архитектура микросервисов

Традиционный Architecture Review:
  → Созвать 5 специалистов (Solution Arch, Enterprise Arch, Security, BA, Stakeholder)
  → Изучить архитектурные документы (2-3 часа каждый)
  → Провести ревью сессию (несколько часов)
  → Цикл: 2-3 НЕДЕЛИ от начала до финального решения

Архитектура как код (Architecture as Code):
  → Structurizr DSL: система описана в текстовых файлах
  → C4 Model: Context → Container → Component → Code
  → Git история: изменения архитектуры отслеживаются как код
  → НО: DSL-файлы требуют всё того же ручного ревью

LLM + Architecture as Code:
  → LLM читает DSL → понимает архитектуру
  → 5 кастомных скиллов = 5 ролей ревьюеров
  → Pre-review валидация: 98% автоматически
  → Цикл: 2-3 недели → 1 неделя
```

## 5 архитектурных ревьюеров на Claude Code Skills

```python
# AlexeyPronkov (BCS FinTech): Architecture as Code + LLM
# habr.com/ru/companies/bcs_company/articles/1006944/

from dataclasses import dataclass
from typing import Literal
from enum import Enum

class ReviewerRole(Enum):
    """5 ролей архитектурного ревью, реализованных как Claude Skills."""
    SOLUTION_ARCHITECT = "solution"       # паттерны, принципы, технологические решения
    ENTERPRISE_ARCHITECT = "enterprise"   # соответствие enterprise-стандартам
    SECURITY_ENGINEER = "security"        # threat modeling, attack surfaces
    BUSINESS_ANALYST = "analyst"          # бизнес-требования, value delivery
    STAKEHOLDER = "stakeholder"           # ясность для нетехнических участников


@dataclass
class ArchitectureReview:
    """Результат архитектурного ревью одной роли."""
    role: ReviewerRole
    findings: list[str]          # найденные проблемы/риски
    recommendations: list[str]   # рекомендации
    adr_draft: str | None        # черновик ADR если нужен
    severity: str                # "critical" | "major" | "minor" | "info"


@dataclass
class C4DiagramFile:
    """Файл архитектуры в Structurizr DSL (C4 Model)."""
    path: str
    content: str     # текст DSL
    level: str       # "context" | "container" | "component" | "code"
    system: str      # имя системы

    # Пример DSL содержимого:
    # workspace {
    #   model {
    #     user = person "Пользователь"
    #     system = softwareSystem "BCS Trading System" {
    #       webApp = container "Web App" {
    #         technology "React"
    #       }
    #       api = container "Trading API" {
    #         technology "Python FastAPI"
    #       }
    #     }
    #   }
    # }


class ArchitectureCodeReviewer:
    """
    LLM-ревьюер архитектуры через Claude Code Skills.

    Ключевое отличие от MR-code-review (R47, R33, R15):
    → MR ревью: анализировать ИЗМЕНЕНИЯ в коде (diff)
    → Architecture review: анализировать ВСЮ архитектурную систему (DSL)

    Не "что изменилось в этом коммите",
    а "правильно ли спроектирована система в целом?"

    5 Skills в .claude/skills/:
    - review-architecture-solution.md
    - review-architecture-enterprise.md
    - review-architecture-security.md
    - review-architecture-analyst.md
    - review-architecture-stakeholder.md
    """

    def load_architecture(self, repo_path: str) -> list[C4DiagramFile]:
        """Загрузить все DSL-файлы архитектуры из репозитория."""
        import glob
        dsl_files = glob.glob(f"{repo_path}/**/*.dsl", recursive=True)
        return [self._parse_dsl(path) for path in dsl_files]

    async def review_as_solution_architect(
            self, diagrams: list[C4DiagramFile]) -> ArchitectureReview:
        """
        Роль: Solution Architect.
        Фокус: архитектурные паттерны, принципы SOLID/DRY,
               технологический стек, coupling/cohesion.
        """
        dsl_content = "\n\n".join([d.content for d in diagrams])

        prompt = f"""Ты опытный Solution Architect с 15+ лет опыта в финансовых системах.
Проанализируй архитектуру системы, описанную в Structurizr DSL:

{dsl_content}

Проверь:
1. Соответствие архитектурным паттернам (Microservices, Event-Driven, CQRS, Saga)
2. Single Responsibility между сервисами
3. Coupling между контейнерами (слишком тесная связь?)
4. Технологический стек: есть ли противоречия?
5. Масштабируемость при 10× нагрузке

Выдай: список проблем + рекомендации + severity (critical/major/minor)."""

        result = await self.claude.run_skill(
            skill="review-architecture-solution",
            context={"dsl": dsl_content}
        )
        return self._parse_review(result, ReviewerRole.SOLUTION_ARCHITECT)

    async def review_as_security_engineer(
            self, diagrams: list[C4DiagramFile]) -> ArchitectureReview:
        """
        Роль: Security Engineer.
        Фокус: threat modeling (STRIDE), attack surfaces,
               data flows с чувствительными данными, аутентификация.
        """
        prompt_additions = """
Дополнительно проверь:
1. Все data flows с PII/финансовыми данными → зашифрованы?
2. Authentication/Authorization на каждой границе сервисов
3. STRIDE threat modeling: Spoofing, Tampering, Repudiation, Information Disclosure, DoS, Elevation
4. Единые точки отказа с security-последствиями
5. Соответствие PCI DSS / ФЗ-152 для финансовых данных"""

        result = await self.claude.run_skill("review-architecture-security",
                                              dsl=diagrams)
        return self._parse_review(result, ReviewerRole.SECURITY_ENGINEER)

    async def generate_adr(self,
                            decision: str,
                            context: str,
                            options: list[str]) -> str:
        """
        Генерировать черновик ADR (Architecture Decision Record).

        ADR формат: Context → Decision → Status → Consequences
        LLM заполняет из архитектурного контекста.
        """
        prompt = f"""Создай Architecture Decision Record (ADR) в формате MADR:

Контекст: {context}
Решение для документирования: {decision}
Рассмотренные варианты: {options}

Формат ADR:
# ADR-XXX: [Название]
## Status: Proposed
## Context: [Описание ситуации]
## Decision: [Выбранное решение]
## Rationale: [Почему выбрано]
## Consequences: [Последствия, trade-offs]
## Considered Alternatives: [Что ещё рассматривали и почему отвергли]"""

        return await self.claude.generate(prompt)

    async def resolve_dsl_merge_conflict(self,
                                          conflict_file: str) -> str:
        """
        Резолвить Git merge conflict в Structurizr DSL файле.

        Обычные merge tools не понимают семантику DSL.
        LLM понимает что означают изменения архитектурно
        → выбирает правильный merge с учётом смысла изменений.

        <<<<<<< HEAD
        container "API Gateway" { technology "nginx" }
        =======
        container "API Gateway" { technology "Kong" }
        >>>>>>> feature/kong-migration
        """
        prompt = f"""Резолви merge conflict в Structurizr DSL файле архитектуры.
Учти архитектурный смысл изменений, а не только текстовое различие.

Файл с конфликтом:
{conflict_file}

Выбери правильный вариант merge (или объедини) с объяснением."""

        return await self.claude.generate(prompt)


PRODUCTION_RESULTS = {
    "метрики_до_после": {
        "создание_диаграммы": {
            "до": "2-3 часа", "после": "минуты", "экономия": "~95%"
        },
        "черновик_документации": {
            "до": "2-3 часа", "после": "минуты", "экономия": "~80%"
        },
        "pre_review_валидация": {
            "автоматизировано": "~98%"
        },
        "цикл_ревью": {
            "до": "2-3 недели", "после": "1 неделя", "ускорение": "2-3×"
        },
        "архитектурный_анализ": "~30% экономии времени"
    },
    "стек": {
        "llm": "Claude Code (Anthropic)",
        "architecture_dsl": "Structurizr DSL",
        "model": "C4 Model (Context/Container/Component/Code)",
        "skills": [
            "review-architecture-solution.md",
            "review-architecture-enterprise.md",
            "review-architecture-security.md",
            "review-architecture-analyst.md",
            "review-architecture-stakeholder.md"
        ]
    },
    "задачи_автоматизированы": [
        "Валидация C4-диаграмм по правилам",
        "Генерация черновиков ADR",
        "Извлечение таблиц инфраструктурных ресурсов",
        "Резолвинг Git merge conflicts в DSL-файлах"
    ]
}
```

## Применение к Lorenzo

```python
# Lorenzo: Architecture as Code для самого Lorenzo

class LorenzoArchitectureReview:
    """
    AlexeyPronkov паттерн для Lorenzo:
    Architecture review самого репозитория Lorenzo через Skills.

    DSL описание Lorenzo:
    - scripts/ → 159 скриптов как "модули"
    - gateway.py → API Gateway компонент
    - mcp_server.py → MCP компонент
    - CardStore → Data Store

    5 ролей для Lorenzo:
    Solution: правильно ли организованы скрипты?
    Security: нет ли injection уязвимостей в gateway.py?
    BA: покрывают ли скрипты все бизнес-требования Svyazi?
    Stakeholder: понятна ли архитектура новому участнику?
    Enterprise: соответствует ли Lorenzo стандартам Knowledge OS?

    → /architecture-review скилл для самодиагностики Lorenzo
    """
    pass
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Architecture as Code + MTS Code Review (R47)** | R47: MR-level review; R53: system-level review — два уровня ревью в едином пайплайне |
| **Architecture as Code + Temporal KG (R47)** | Темпоральный граф эволюции архитектуры: как C4-диаграммы менялись с каждым ADR |
| **Architecture as Code + Design by Contract (R51)** | DbC контракты на уровне сервисов + C4 архитектура = формальная спецификация всей системы |
| **Architecture as Code + LLM Observability (R45)** | Трейсинг: какая из 5 ролей находит больше критических проблем в каких типах сервисов |
| **Architecture as Code + Coordination Harness (R46)** | 5 архитектурных агентов как coordination harness: fidelity передачи findings между ролями |

## Контакт

- Статья: https://habr.com/ru/companies/bcs_company/articles/1006944/ (март 2025)
- Автор: AlexeyPronkov (Алексей Прончев, BCS FinTech AI)
- Structurizr DSL: structurizr.com/dsl
- C4 Model: c4model.com (Simon Brown)
- Claude Code Skills: docs.anthropic.com/claude-code
- Смежная (MTS LLM code review, R47): docs/06-discovery/round-47/projects/mts-evgzor-llm-code-review-gitlab-n8n-ollama.md
- Смежная (AI code agents v2, R33): docs/06-discovery/round-33/
- Смежная (Design by Contract, R51): docs/06-discovery/round-51/projects/miller83-design-by-contract-llm-crypto-hardware.md

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
- [Решения](../../../DECISIONS.md)
