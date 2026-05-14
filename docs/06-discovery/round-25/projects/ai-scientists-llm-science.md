# AI-учёные уже здесь: LLM меняют фундаментальную науку

**Автор:** независимый автор (Хабр, 2025)  
**Хабр:** https://habr.com/ru/articles/938638/ (обзор) + https://habr.com/ru/articles/954612/ (практика)  
**GitHub:** разные проекты (AlphaFold, TxGemma, OpenAI o3-mini для науки)  
**Слой:** knowledge / orchestration / analytics  
**Дата:** 2025  
**Уникальность:** Систематический обзор применения LLM в науке: от биохимии (AlphaFold 4, TxGemma) до физики и материаловедения. Ключевая проблема: AI-учёные галлюцинируют — генерируют несуществующие химические реакции и белковые структуры. Паттерны решения: grounded generation, peer-review от другой LLM, "не знаю" как валидный ответ.

## Масштаб изменений в 2025

```
Традиционный цикл исследования:
  Гипотеза → Дизайн эксперимента → Эксперимент (месяцы) → Анализ → Публикация
  Время: 2-5 лет до валидного открытия

С AI (2025):
  Гипотеза (LLM) → Симуляция (ML) → Анализ (LLM) → Публикация
  Время: недели до первичного открытия, эксперимент — параллельно

Примеры в 2025:
  AlphaFold 4: предсказание структур белков + нуклеиновых кислот
  TxGemma (Google): разработка лекарств, ADMET-свойства
  GNoME: 2.2M новых стабильных материалов (DeepMind)
  AI-математики: IMO-задачи уровня "золото" (AlphaProof, Gemini)
```

## Домены и специализированные модели

```python
SCIENCE_AI_LANDSCAPE = {
    "biology": {
        "task": "Структуры белков, взаимодействия, drug design",
        "models": ["AlphaFold 4", "ESMFold", "RFDiffusion"],
        "use_case": "Предсказать как белок-мишень взаимодействует с кандидатом",
        "maturity": "Production (клинические исследования используют)"
    },
    "chemistry": {
        "task": "Предсказание реакций, свойств молекул, синтез",
        "models": ["TxGemma (Google)", "ChemBERTa", "Chemformer"],
        "use_case": "ADMET: токсичность, растворимость, биодоступность",
        "maturity": "Beta (используется в Big Pharma)"
    },
    "materials": {
        "task": "Поиск новых материалов с заданными свойствами",
        "models": ["GNoME (DeepMind)", "M3GNet", "MEGNet"],
        "use_case": "Обратный дизайн: 'нужен материал с проводимостью X и прочностью Y'",
        "maturity": "Research (2.2M кандидатов, проверяются)"
    },
    "general_research": {
        "task": "Литературный обзор, гипотезы, планирование",
        "models": ["Gemini 2.0 Pro", "Claude Sonnet", "o3"],
        "use_case": "18-tool research agent: PubMed + код + анализ данных",
        "maturity": "Emerging (нужен grounding)"
    }
}
```

## Ключевая проблема: галлюцинации в науке = катастрофа

```
В обычном тексте: галлюцинация = неверный факт → неприятно
В науке: галлюцинация = потеря месяца эксперимента + миллионы рублей

Примеры реальных проблем:
  1. LLM генерирует несуществующую химическую реакцию
     → исследователь тратит 2 месяца синтезируя невозможное

  2. LLM "находит" несуществующую статью в PubMed
     → ссылки на фантомные источники в черновике

  3. LLM предлагает "новую" гипотезу, которая уже опровергнута
     → дублирование давно закрытой темы

Требования к AI-ассистентам в науке:
  ✅ Grounded: ответ должен быть привязан к конкретным источникам
  ✅ "Не знаю" как валидный ответ (не придумывать)
  ✅ Верификация: проверка через другую модель или поиск
  ✅ Неопределённость: "высокая уверенность" vs "предположение"
```

## Паттерн: Research Agent с 18 инструментами

```python
# Gemini 2.0 Pro-based research agent (описан в статье)
RESEARCH_TOOLS = [
    "pubmed_search",           # поиск статей по ключевым словам
    "arxiv_search",            # препринты
    "doi_fetch",               # полный текст по DOI
    "citation_graph",          # кто цитирует кто
    "python_executor",         # выполнить код анализа данных
    "plot_generator",          # графики из данных
    "hypothesis_generator",    # предложить гипотезы
    "experiment_designer",     # спланировать эксперимент
    "statistic_calculator",    # статистический анализ
    "molecule_viewer",         # визуализация молекул
    "protein_structure",       # AlphaFold API
    "database_query",          # базы химических соединений
    # ... ещё 6 инструментов
]

# Агент планирует многошаговые исследования:
# "Найди ингибиторы белка X → проверь ADMET → предложи синтез → оцени патентную чистоту"
```

## Обратный дизайн материалов

```python
# Традиционный подход: у меня материал → каковы его свойства?
# AI-подход: мне нужны эти свойства → какой материал?

def inverse_design(target_properties: dict) -> list[Material]:
    """
    target_properties = {
        "conductivity": ">1e6 S/m",
        "tensile_strength": ">500 MPa",
        "synthesis_temperature": "<800°C",
        "cost_per_kg": "<$100"
    }
    """
    # 1. Embedding запроса в пространстве свойств материалов
    # 2. GNoME / M3GNet предсказывает стабильные кандидаты
    # 3. DFT-симуляция проверяет свойства (Quantum ESPRESSO)
    # 4. Ranking по вероятности синтеза

    return material_db.inverse_search(target_properties, top_k=10)
```

## Как LLM помогают в НЕ-биологических науках

```
Математика:
  AlphaProof (DeepMind): решает IMO-задачи уровня "золото"
  Lean4 верификация: доказательства проверяются формально (не галлюцинации)
  WolframAlpha + LLM: символьная математика + контекст

Физика:
  AI Feynman: открывает физические законы из данных экспериментов
  Neural ODE: моделирование динамических систем
  Surrogate models: заменяют дорогие симуляции (CFD, FEM)

Климатология:
  WeatherBench: предсказание погоды лучше NWP (GraphCast)
  CarbonTrack: AI-мониторинг выбросов CO₂

Астрономия:
  Classifier AI: автоматическая классификация галактик (Hubble data)
  Anomaly detection: поиск новых объектов в radio telescope data
```

## Применение к Lorenzo

Lorenzo = Knowledge OS для AI-исследований.  
Science AI паттерн = **Knowledge Discovery Pipeline**:

```python
# improve_research_assistant.py (паттерн):
class LorenzoResearchAssistant:
    """Scientific paper → structured knowledge extraction"""

    def process_paper(self, paper_path: str) -> ResearchNote:
        text = read_doc(paper_path)

        return llm.extract({
            "hypothesis": "Что авторы исследовали и доказали?",
            "methodology": "Какие методы использовались?",
            "results": "Ключевые численные результаты",
            "limitations": "Что авторы признают ограничением",
            "future_work": "Что планируют исследовать дальше",
            "connections": "Связи с другими работами",
        })
    # Применение: обрабатывать Хабр-статьи как научные работы
    # → автоматически строить knowledge graph из discovery-раундов
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Science AI + Graph RAG (R22)** | Научный Knowledge Graph: гипотезы → методы → результаты → связи через Neo4j |
| **Science AI + Agentic RAG (R18)** | Research Agent: агент сам выбирает инструменты из RESEARCH_TOOLS |
| **Science AI + Synthetic Data (R18)** | TxGemma генерирует синтетические молекулярные данные для fine-tuning |
| **Science AI + LLM Wiki (R17)** | Живая научная вики: автообновление при новых публикациях |
| **Science AI + Reasoning LLM (R20)** | o3/DeepSeek-R1 для сложных гипотез: thinking перед предложением эксперимента |

## Контакт

- Обзор AI-учёных: https://habr.com/ru/articles/938638/ (2025)
- Практика LLM в науке: https://habr.com/ru/articles/954612/
- AlphaFold 4: deepmind.google/alphafold
- TxGemma: research.google/blog/txgemma (Apache 2.0)
- GNoME: deepmind.google/gnome (2.2M новых материалов)
- OpenAI o3 science evals: openai.com/o3
