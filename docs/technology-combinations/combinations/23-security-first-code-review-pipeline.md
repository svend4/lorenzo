# Комбинация 23: Security-First Code Review Pipeline

<!-- toc-auto -->
## Contents

- [Смотрите также](#смотрите-также)


> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Комбинирование технологий для новых свойств - Claude` (корень репозитория).

---
<!-- tags: orchestration -->

> [!WARNING]
> Документ описывает ограничения, риски или требования безопасности.





> Источник: MHTML‑снимок `Комбинирование технологий для новых свойств - Claude` (корень репозитория).

Родители:

CyberCodeReview (российский open-source, security-focused)

Adversarial review (Opus writes, Codex reviews)

Sequential Protocol (chain of specialists, 44% quality boost)

Дети:

Multi-stage security review with Russian compliance

Writer Agent: Claude Opus 4.6
↓
Sequential Review Chain:
1. CyberCodeReview → SQL injections, XSS, CVEs
2. Style Reviewer → Code standards (Russian ГОСТ если требуется)
3. Logic Reviewer → Business logic, edge cases
4. Compliance → ФСТЭК requirements (для критической инфраструктуры)
↓
Adversarial loop: Writer fixes → Re-review

Russian regulatory compliance automation

CyberCodeReview detects ФСТЭК violations

Sequential chain validates against ГОСТ standards

Adversarial ensures writer understands security context

Use case: Government contractors, critical infrastructure

ROI: Automated compliance vs manual audit (weeks → minutes)

Уникальность: First pipeline combining international AI (Claude) with Russian security standards (CyberCodeReview, ФСТЭК). Critical for Russian enterprises requiring certification.

<!-- see-also -->

---

## Использование

```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "Комбинация 23 Security First Code"
```

## Смотрите также
- [16-adversarial-multi-agent-code-review](16-adversarial-multi-agent-code-review.md)
- [28-pydantic-enforced-legal-workflows](28-pydantic-enforced-legal-workflows.md)
- [20-24-final](../synthesis-tables/20-24-final.md)
- [12-multi-agent-observability-stack](12-multi-agent-observability-stack.md)

Документ индексирован в базе знаний репозитория. Навигация возможна через семантический поиск и граф концептов репозитория Lorenzo. Материал доступен для семантического поиска, BM25-поиска и навигации через граф концептов. Используйте скрипты группы reports для получения актуальной статистики по разделу. Рекомендуется начинать с основных документов раздела и переходить к деталям через внутренние ссылки. Все связанные документы доступны через граф концептов и поисковый индекс репозитория Lorenzo. Документ индексирован в базе знаний репозитория.

<!-- backlinks -->

---

**Кто ссылается на этот документ (9):**
- [OUTLINE](../../OUTLINE.md)
- [READABILITY](../../READABILITY.md)
- [READING_TIME](../../READING_TIME.md)
- [SEARCH](../../SEARCH.md)
- [TABLES](../../TABLES.md)
- [16-adversarial-multi-agent-code-review](16-adversarial-multi-agent-code-review.md)
- [28-pydantic-enforced-legal-workflows](28-pydantic-enforced-legal-workflows.md)
- [README](README.md)
- _...ещё 1_

