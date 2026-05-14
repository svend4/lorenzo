# SherlockOps: LLM-агент автоматического расследования алертов

**Автор:** asvata (Тимур Наурузбаев + Алексей Щепетков, DevOps)  
**Хабр:** https://habr.com/ru/articles/1022830/  
**GitHub:** https://github.com/Duops/SherlockOps  
**Слой:** orchestration / analytics  
**Дата:** апрель 2026  
**Уникальность:** Production-развёрнутый Go-агент автоматического расследования инфраструктурных алертов с ~50 интеграциями (VictoriaMetrics, Kubernetes, Loki, ArgoCD, Yandex Cloud). При срабатывании алерта автономно запрашивает метрики, логи и состояние кластера → строит гипотезу первопричины → публикует RCA + нумерованные шаги устранения в Slack/Telegram. Начинался как n8n/MCP воркфлоу, переписан в автономный Go-бинарь. Использует Claude с extended thinking mode.

## Проблема: алерт в 3:00 — дежурный не знает с чего начать

```
Традиционный SRE-процесс при алерте:
  → Алертменеджер: "Pod CrashLoopBackOff в prod-namespace"
  → Дежурный просыпается в 3:00
  → Проверяет: kubectl logs → kubectl describe → метрики → логи
  → 15-30 мин на понимание: "а, OOMKilled, нужно увеличить limit"

Проблемы масштаба:
  → 50+ микросервисов → инструментов столько же
  → Каждый тип алерта требует свою последовательность действий
  → Runbook'и устаревают быстрее чем обновляются
  → Шум: 80% алертов — flapping, ложные срабатывания

SherlockOps:
  → Алерт → SherlockOps получает webhook
  → Агент автономно: metrics → k8s state → pod logs → ArgoCD
  → Стоп-условия: нашёл "OOMKilled" → RCA готов
  → Результат в Slack: причина + 3 шага для исправления
  → Дежурный видит готовое расследование, не сырые данные
```

## Архитектура Go-агента

```python
# SherlockOps: architecture summary (оригинал на Go)
# github.com/Duops/SherlockOps

# Концептуальный Python-эквивалент для иллюстрации

from dataclasses import dataclass
from typing import Optional
import datetime

@dataclass
class Alert:
    """Входящий алерт из Alertmanager / Grafana / Zabbix."""
    source: str           # "alertmanager" / "grafana" / "zabbix"
    severity: str         # "critical" / "warning"
    environment: str      # "prod" / "staging" / "dev"
    service: str          # "payment-service"
    message: str          # "Pod CrashLoopBackOff"
    labels: dict          # prometheus labels
    fired_at: datetime.datetime


class SherlockOpsAgent:
    """
    Автономный агент расследования.
    Последовательность: фиксированная, останавливается при crash-сигнале.
    """

    # Порядок инструментов расследования (не меняется)
    INVESTIGATION_SEQUENCE = [
        "get_recent_metrics",    # VictoriaMetrics: CPU/RAM/RPS тренды
        "get_k8s_pod_status",    # kubectl describe pod
        "get_pod_logs",          # Loki: последние 200 строк логов
        "get_argocd_status",     # последний деплой и его статус
        "get_k8s_events",        # Kubernetes events в namespace
        "get_yandex_cloud_status" # статус облачных ресурсов
    ]

    # Сигналы остановки: нашли причину → дальше не идём
    CRASH_SIGNALS = [
        "OOMKilled",
        "CrashLoopBackOff",
        "ImagePullBackOff",
        "Insufficient memory",
        "Connection refused",
        "certificate has expired"
    ]

    def investigate(self, alert: Alert,
                     max_tool_calls: int = 5) -> dict:
        """
        Автономное расследование.
        Останавливается при: crash-сигнал OR max_tool_calls достигнут.
        """
        context = {"alert": alert, "findings": []}

        for i, tool_name in enumerate(self.INVESTIGATION_SEQUENCE):
            if i >= max_tool_calls:
                break

            # Вызов инструмента через MCP
            result = self.mcp_client.call(
                tool=tool_name,
                environment=alert.environment,
                service=alert.service
            )
            context["findings"].append(result)

            # Проверка стоп-условий
            for signal in self.CRASH_SIGNALS:
                if signal in str(result):
                    context["root_cause_signal"] = signal
                    return self._synthesize_rca(context)

        # Синтез даже без явного сигнала
        return self._synthesize_rca(context)

    def _synthesize_rca(self, context: dict) -> dict:
        """
        Claude (extended thinking mode) анализирует собранные данные.
        Extended thinking: глубокое размышление перед ответом.
        """
        findings_text = "\n".join([
            f"[{f['tool']}]: {f['summary']}"
            for f in context["findings"]
        ])

        prompt = f"""Ты — Senior SRE. Проанализируй данные расследования алерта.

Алерт: {context['alert'].message}
Сервис: {context['alert'].service}
Окружение: {context['alert'].environment}

Собранные данные:
{findings_text}

Сформулируй:
1. Первопричина (1 предложение)
2. Последовательность событий (2-3 шага)
3. Конкретные шаги устранения (нумерованный список)
4. Профилактика (1-2 рекомендации)

Формат: Markdown для Slack/Telegram."""

        # Claude с extended thinking для глубокого анализа
        rca = self.claude.complete(
            prompt=prompt,
            model="claude-opus-4-7",
            thinking={"type": "enabled", "budget_tokens": 5000}
        )

        return {
            "rca": rca,
            "root_cause_signal": context.get("root_cause_signal"),
            "tool_calls_used": len(context["findings"])
        }
```

## ~50 интеграций через MCP

```python
INTEGRATIONS = {
    "метрики": {
        "VictoriaMetrics": "CPU/RAM/RPS тренды через PromQL",
        "Prometheus": "alerts + recording rules"
    },

    "kubernetes": {
        "k8s_mcp": "pod status, events, describe, logs",
        "ArgoCD": "deployment status, последний релиз, rollback"
    },

    "логи": {
        "Loki": "структурированные логи по label selector",
        "Elasticsearch": "поиск по error patterns"
    },

    "инфраструктура": {
        "Yandex Cloud API": "статус MDB, VPC, IAM, Load Balancer",
        "Terraform state": "drift detection"
    },

    "routing": {
        "X-Environment_header": "prod/staging/dev → разные кластеры",
        "multi_cluster": "один агент → несколько k8s контекстов"
    }
}

EVOLUTION = {
    "v1": "n8n воркфлоу + MCP серверы (быстрый прототип)",
    "v2": "standalone Go-бинарь (production-ready)",
    "причина_v2": "n8n: сложно поддерживать сложную логику условий",
    "llm_tested": {
        "claude": "Выбран: надёжная MCP поддержка",
        "gemini": "Отклонён: сбои MCP протокола"
    }
}

SYSTEM_PROMPT_TEMPLATE = """Ты — SherlockOps, AI-ассистент для DevOps.
Твоя задача: расследовать инфраструктурный алерт.

Правила:
1. Используй доступные инструменты последовательно
2. Останавливайся, когда нашёл первопричину
3. НЕ предлагай действия разрушительные (kubectl delete, terraform destroy)
4. Отвечай на русском языке в Slack Markdown
5. Максимум 5 вызовов инструментов на одно расследование

Текущий алерт:
{alert_details}"""
```

## ChatOps доставка результатов

```python
class ChatOpsDelivery:
    """
    Форматирование RCA для Slack/Telegram.
    """

    SLACK_TEMPLATE = """
:rotating_light: *Алерт расследован: {service}* ({severity})

*Первопричина:* {root_cause}

*Хронология:*
{timeline}

*Шаги устранения:*
{remediation_steps}

*Профилактика:*
{prevention}

---
_SherlockOps | Инструментов вызвано: {tool_calls} | Время: {duration}s_
"""

    def post_to_slack(self, rca: dict, channel: str) -> None:
        message = self.SLACK_TEMPLATE.format(**rca)
        self.slack_client.chat_postMessage(channel=channel, text=message)
```

## Применение к Lorenzo

```python
# Lorenzo: SherlockOps паттерн для автоматической диагностики

class LorenzoHealthSherlock:
    """
    SherlockOps паттерн для Lorenzo:
    При сбое скриптов или деградации метрик — автономное расследование.
    """

    INVESTIGATION_SEQUENCE = [
        "check_script_exit_codes",   # какие improve_*.py упали?
        "check_docs_health",         # HEALTH.md метрики снизились?
        "check_search_index",        # search_index.json актуален?
        "check_mcp_server",          # MCP-сервер отвечает?
        "check_git_log"              # последний коммит что изменил?
    ]

    def diagnose(self, alert: str) -> str:
        """При деградации → автономный сбор данных → LLM-диагноз."""
        findings = []
        for tool in self.INVESTIGATION_SEQUENCE:
            findings.append(self.run_tool(tool))
            if self._found_root_cause(findings):
                break
        return self.llm.synthesize_rca(alert, findings)
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **SherlockOps + Kaspersky MCP (R40)** | SherlockOps читает OpenSearch логи безопасности + codegen анализ инцидентов |
| **SherlockOps + LangFuse (R38)** | Трейсинг каждого расследования: tool_calls, thinking tokens, latency |
| **SherlockOps + Sequential (R38)** | Ансамбль SRE-агентов обсуждает сложный инцидент без координатора |
| **SherlockOps + Agent Distillation (R39)** | Дистилляция трасс расследований SherlockOps → специализированный SRE LLM |
| **SherlockOps + Lorenzo Gateway** | /api/diagnose → SherlockOps расследует проблемы Lorenzo Pipeline |

## Контакт

- Статья: https://habr.com/ru/articles/1022830/ (апрель 2026)
- GitHub: https://github.com/Duops/SherlockOps
- Claude API: anthropic.com/api
- VictoriaMetrics: victoriametrics.com
- Смежная (RAG-агент инцидент-менеджмент): https://habr.com/ru/companies/otus/articles/912228/
- Смежная (AIOps Sberbank): https://habr.com/ru/companies/sber/articles/780648/
