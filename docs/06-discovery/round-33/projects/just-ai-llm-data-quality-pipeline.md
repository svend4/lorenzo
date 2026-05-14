# LLM в Data Quality: генерация правил и диагностика инцидентов без потери контроля

**Автор:** Арина Макунина, Just AI (Хабр, апрель 2026)  
**Хабр:** https://habr.com/ru/companies/just_ai/articles/1011428/  
**GitHub:** не опубликован (production-система Just AI)  
**Слой:** orchestration / analytics  
**Дата:** апрель 2026  
**Уникальность:** Трёхуровневая архитектура DQ+LLM: Data Platform → DQ Application → LLM Platform gateway (Caila). LLM не имеет прямого доступа к БД — только pre-structured context. Два режима: Zero-Shot генерация YAML-правил для новых таблиц + автодиагностика инцидентов (root cause + SQL запрос). "Verifiable artifacts only" принцип. Claude Sonnet 4 в production.

## Проблема: Data Quality без LLM vs с LLM

```
Традиционный подход:
  Новая таблица → инженер вручную пишет DQ правила:
    - unique check для primary key
    - not_null для обязательных полей
    - format_check для email/INN
    - date_range для временных полей
  → 2-4 часа на таблицу × N таблиц в месяц

Инцидент DQ:
  check_failed(table="orders", column="status", rule="not_null")
  → Инженер пишет SELECT вручную → анализирует → гипотезы
  → 30-60 мин на диагностику

С LLM:
  → Генерация starter rules: < 5 минут + ревью
  → Диагностика: LLM даёт топ-3 гипотезы + SQL за < 30 сек
  → >80% экономии времени (по данным Just AI)
```

## Трёхуровневая архитектура: LLM без прямого доступа к БД

```python
# Принцип: LLM видит только pre-structured context, не сырые данные

class DQArchitecture:
    """
    Уровень 1: Data Platform
        → DDL таблиц, профилирование (min/max/nulls/cardinality)
        → Выборки данных (anonymized samples)

    Уровень 2: DQ Application
        → Генерация правил, хранение результатов проверок
        → Формирование контекста для LLM

    Уровень 3: LLM Platform (Caila)
        → Роутинг запросов к модели
        → Rate limiting, аудит, смена модели без изменения кода
        → Claude Sonnet 4 (через Caila gateway)

    Критично: LLM → только JSON предложения → человек одобряет
    LLM не может: читать таблицы, запускать SQL, менять пайплайн
    """
```

## Режим 1: Zero-Shot генерация DQ правил

```python
class DQRuleGenerator:
    """
    Новая таблица → автоматически предложить starter DQ правила.
    """

    def build_context(self, table_name: str) -> dict:
        """
        Собрать контекст из Data Platform (без сырых данных).
        """
        return {
            "ddl": self.data_platform.get_ddl(table_name),
            "column_profiles": self.data_platform.get_profiles(table_name),
            # Профиль = {column: {type, null_rate, cardinality, min, max, sample_values}}
            "table_description": self.data_platform.get_description(table_name),
            "similar_tables_rules": self.get_similar_tables_rules(table_name)
            # Few-shot: правила похожих таблиц как пример
        }

    RULE_GENERATION_PROMPT = """
Ты — эксперт по качеству данных. Сгенерируй DQ правила для таблицы.

DDL таблицы:
{ddl}

Профиль колонок:
{column_profiles}

Правила похожих таблиц (для примера):
{similar_tables_rules}

Верни ТОЛЬКО JSON в формате:
{{
  "rules": [
    {{
      "column": "column_name",
      "rule_type": "unique|not_null|format_check|date_range|value_range|custom",
      "parameters": {{}},
      "severity": "critical|warning|info",
      "reasoning": "почему это правило важно"
    }}
  ],
  "coverage_comment": "что не покрыто и почему"
}}

Маскируй PII в параметрах. Не предлагай правила для системных полей (_etl_*).
"""

    def generate_rules(self, table_name: str) -> DQRuleProposal:
        context = self.build_context(table_name)

        # Персональные данные маскируются ПЕРЕД отправкой в LLM
        masked_context = self.pii_masker.mask(context)

        response = self.llm.complete(
            prompt=self.RULE_GENERATION_PROMPT.format(**masked_context),
            model="claude-sonnet-4-6",
            response_format={"type": "json_object"},
            temperature=0.1
        )

        proposal = json.loads(response.content)
        # Proposal → инженер проверяет → утверждает/редактирует → production
        return DQRuleProposal(table=table_name, rules=proposal["rules"])
```

## Режим 2: Автодиагностика DQ инцидентов

```python
class DQIncidentDiagnoser:
    """
    check_failed → LLM анализирует контекст → root cause + SQL.
    """

    def build_incident_context(self, incident: DQIncident) -> dict:
        """
        Собрать структурированный контекст инцидента.
        """
        return {
            "failing_rule": {
                "table": incident.table,
                "column": incident.column,
                "rule_type": incident.rule_type,
                "expected": incident.expected,
                "actual": incident.actual_value
            },
            "column_stats": self.get_current_stats(
                incident.table, incident.column
            ),
            # Динамика: как менялась статистика
            "historical_stats": self.get_historical_stats(
                incident.table, incident.column, days=7
            ),
            "recent_check_results": self.get_recent_results(
                incident.table, limit=10
            ),
            # Контекст пайплайна (без данных!)
            "upstream_jobs": self.get_upstream_jobs(incident.table),
            "last_etl_run": self.get_last_etl_metadata(incident.table)
        }

    INCIDENT_DIAGNOSIS_PROMPT = """
Проанализируй сбой DQ проверки и предложи диагностику.

Инцидент:
{failing_rule}

Статистика колонки (текущая vs история):
{column_stats}
{historical_stats}

Последние результаты проверок:
{recent_check_results}

Метаданные ETL:
{last_etl_run}
{upstream_jobs}

Верни JSON:
{{
  "root_cause_hypotheses": [
    {{
      "hypothesis": "что могло произойти",
      "probability": "high|medium|low",
      "evidence": "на чём основана гипотеза"
    }}
  ],
  "diagnostic_sql": "SELECT ... -- запрос для проверки гипотезы №1",
  "recommended_action": "что сделать прямо сейчас",
  "escalation_needed": true|false
}}
"""

    def diagnose(self, incident: DQIncident) -> IncidentDiagnosis:
        context = self.build_incident_context(incident)
        masked = self.pii_masker.mask(context)

        response = self.llm.complete(
            prompt=self.INCIDENT_DIAGNOSIS_PROMPT.format(**masked),
            model="claude-sonnet-4-6",
            response_format={"type": "json_object"}
        )

        diagnosis = json.loads(response.content)
        # SQL запрос предлагается инженеру, не выполняется автоматически
        return IncidentDiagnosis(**diagnosis)
```

## "Verifiable Artifacts Only": принцип безопасности

```python
LLM_SAFETY_PRINCIPLES = {
    "no_direct_db_access": {
        "правило": "LLM никогда не подключается к БД напрямую",
        "реализация": "только pre-structured JSON context через DQ Application",
        "зачем": "предотвратить утечку данных и неконтролируемые запросы"
    },

    "verifiable_artifacts_only": {
        "правило": "LLM возвращает только JSON предложения",
        "реализация": "строгая JSON Schema валидация ответов",
        "зачем": "всё что предложил LLM → человек читает и одобряет"
    },

    "pii_masking_before_llm": {
        "правило": "персональные данные маскируются до отправки в LLM",
        "реализация": "PII masker на уровне DQ Application",
        "зачем": "152-ФЗ, GDPR, корпоративная безопасность"
    },

    "caila_gateway": {
        "правило": "все LLM запросы через Caila gateway",
        "реализация": "единая точка: rate limit, audit log, model swap",
        "зачем": "смена модели без изменения кода, полный аудит"
    },

    "human_approval": {
        "правило": "LLM предложения → не в production без ревью",
        "реализация": "DQ UI: инженер одобряет/редактирует правила",
        "зачем": "LLM может ошибаться; правила влияют на pipeline"
    }
}
```

## Caila: LLM Gateway для enterprise

```python
# Caila = Just AI's LLM platform gateway
# Аналог LiteLLM Proxy, но с enterprise-фичами

CAILA_FEATURES = {
    "model_routing": "Claude Sonnet 4 / GPT-4o / GigaChat через единый API",
    "rate_limiting": "per-team, per-model квоты",
    "audit_log": "все запросы логируются (compliance)",
    "cost_tracking": "расход токенов по командам",
    "model_swap": "сменить модель в конфиге — код не меняется",
    "fallback": "если Claude недоступен → fallback на GigaChat"
}

# Интеграция:
import requests

def call_llm_via_caila(prompt: str, schema: dict) -> dict:
    response = requests.post(
        "https://caila.just-ai.com/api/v1/completions",
        headers={"Authorization": f"Bearer {CAILA_TOKEN}"},
        json={
            "model": "claude-sonnet-4-6",  # Caila роутит
            "messages": [{"role": "user", "content": prompt}],
            "response_format": {"type": "json_object"},
            "json_schema": schema  # строгая валидация
        }
    )
    return response.json()
```

## Применение к Lorenzo

```python
# improve_data_quality_llm.py (паттерн):

class LorenzoDataQuality:
    """
    Lorenzo = база документов.
    Применить DQ паттерн к документальному качеству:
    - Генерировать правила для новых документов (шаблон?)
    - Диагностировать аномалии (пустые секции, битые ссылки)
    """

    def generate_quality_rules(self, doc_path: str) -> QualityRules:
        profile = self.profiler.profile(doc_path)  # длина, секции, ссылки
        return self.llm.generate_rules(
            context=profile,
            similar_docs=self.get_similar_docs(doc_path)
        )

    def diagnose_quality_issue(self, issue: QualityIssue) -> Diagnosis:
        return self.llm.diagnose(
            issue=issue,
            history=self.get_quality_history(issue.doc_path)
        )
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **DQ LLM + Enterprise RAG (R32)** | RAG по истории DQ инцидентов → LLM диагностирует по прецедентам |
| **DQ LLM + HITL (R30)** | LLM предлагает исправление инцидента → HITL перед применением |
| **DQ LLM + Synthetic Data (R30)** | Синтетические DQ нарушения для обучения диагностической модели |
| **DQ LLM + Meta-Monitor (R29)** | Meta-Monitor видит аномалии пайплайна → DQ LLM диагностирует |
| **DQ LLM + LLM Judge (R28)** | Judge оценивает качество сгенерированных DQ правил |

## Контакт

- Статья: https://habr.com/ru/companies/just_ai/articles/1011428/ (апрель 2026)
- Just AI: just-ai.com (Caila platform, conversational AI)
- Смежная (AIDA, dbt агенты, Газпромбанк): https://habr.com/ru/companies/gazprombank/articles/975026/
- Claude Sonnet 4: anthropic.com/claude
- Caila: caila.just-ai.com
