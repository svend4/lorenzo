# Генерация юнит-тестов с LLM — пайплайн Одноклассников

**Автор:** команда Одноклассники (VK), инженеры backend  
**Хабр:** https://habr.com/ru/companies/vk/articles/921410/  
**GitHub:** не опубликован (внутренний инструмент, архитектура описана полностью)  
**Слой:** orchestration / quality / knowledge  
**Дата:** июнь 2025  
**Уникальность:** Не «попроси LLM написать тесты» — а **multi-level pipeline с мутационным тестированием как финальным фильтром**. Реальные числа из production: +20% coverage, Meta TestGen-LLM + MUTGEN 2025 как теоретическая база. Ключевой инсайт: LLM-тест без мутационного тестирования = тест ради метрики coverage, не ради качества.

## Проблема: тесты ради метрики

```
Наивный подход:
  LLM.generate("напиши тесты для класса X")
  → код компилируется ✅
  → coverage растёт ✅
  → тест проходит ✅
  → но тест не проверяет ничего важного ❌
        ↓
Production баг проходит незамеченным
```

**Мутационное тестирование** — единственный способ проверить, нужен ли тест вообще.

## Multi-level pipeline

```
Stage 1: LLM Test Generation
  → prompt: класс + его зависимости + существующие тесты как few-shot
  → output: N кандидатов тестов
        ↓ (~N тестов)
Stage 2: Compilation Filter
  → компилятор проверяет синтаксис + импорты
  → отбраковка: ~20-25% кандидатов
        ↓ (~0.75N тестов)
Stage 3: Green Run Filter
  → запустить тест: должен проходить (green)
  → отбраковка: ещё ~15-20%
        ↓ (~0.60N тестов)
Stage 4: Mutation Testing (ключевой этап!)
  → запустить Pitest / MutPy: вносим мутации в код
  → тест должен УБИТЬ мутацию (поймать изменение)
  → тесты, не убивающие мутации → отброс
        ↓ (~0.40N тестов — все ценные)
Stage 5: Deduplicate + Merge
  → убрать семантически одинаковые тесты
  → смёрджить в тест-файл проекта
```

## Мутационное тестирование — детально

```java
// Оригинальный код:
public int add(int a, int b) {
    return a + b;
}

// Мутация 1: замена оператора
public int add(int a, int b) {
    return a - b;  // мутант
}

// Мутация 2: замена константы
public int add(int a, int b) {
    return a + 0;  // мутант
}

// Хороший тест УБЬЁТ обе мутации:
assertEquals(5, add(2, 3));   // 2-3=-1≠5 → мутант 1 убит
assertEquals(5, add(2, 3));   // 2+0=2≠5  → мутант 2 убит

// Плохой тест (ради coverage):
assertNotNull(add(0, 0));  // 0-0=0, 0+0=0 → оба мутанта выживают!
```

## Prompt engineering для тест-генерации

```python
PROMPT_TEMPLATE = """
Ты — опытный Java-разработчик. Напиши JUnit5 тесты для метода:

## Метод (исходник):
{method_source}

## Контекст класса:
{class_context}

## Существующие тесты (few-shot):
{existing_tests}

## Требования:
- Каждый тест проверяет ровно один аспект поведения
- Используй assertEquals, assertThrows для edge cases
- Не используй моки там, где можно без них
- Тест должен падать при изменении логики метода

Сгенерируй {N} разных тестов.
"""
```

## Результаты (Одноклассники production)

- **+20% coverage** ключевых модулей
- **Скорость**: разработчики не пишут рутинные тесты вручную
- **Качество**: мутационный фильтр отсеял ~60% сгенерированного мусора
- **Meta TestGen-LLM benchmark**: LLM-тесты покрывают 87% валидных кейсов

## Теоретическая база

| Работа | Вклад |
|--------|-------|
| Meta TestGen-LLM | Первый большой эксперимент: LLM → тесты в production |
| MUTGEN 2025 | Мутационное тестирование как фильтр LLM-тестов |
| EvoSuite | Классический search-based test generation (baseline) |

## Применение к Lorenzo

Lorenzo имеет `scripts/improve_*.py` (159+ скриптов) — ни один не покрыт тестами.  
Pipeline Одноклассников применим напрямую:

```python
# improve_test_gen.py (не существует, но вот архитектура):
for script in glob("scripts/improve_*.py"):
    tests = llm.generate_tests(script)          # Stage 1
    tests = filter_compiles(tests)              # Stage 2
    tests = filter_green(tests)                 # Stage 3
    tests = filter_mutation_kills(tests)        # Stage 4 (pytest-mutagen)
    save_tests(f"tests/test_{script.stem}.py")
```

Связь с AI Review CI/CD (R15): авто-тесты из LLM → `improve_ci_config.py` → GitHub Actions.

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **LLM Tests + AI Review (R15)** | Авто-тест → авто-ревью в одном CI-pipeline |
| **LLM Tests + Langfuse (R13)** | Langfuse трейсит каждый этап pipeline: где теряются тесты |
| **LLM Tests + DSPy (R14)** | DSPy оптимизирует prompt для генерации тестов |
| **LLM Tests + Reasoning LLM (R20)** | Reasoning-модель находит edge cases лучше, чем обычная |
| **LLM Tests + Synthetic Data (R18)** | Distilabel генерирует diverse test inputs |

## Контакт

- Статья: https://habr.com/ru/companies/vk/articles/921410/ (июнь 2025)
- Смежная (87% валидных тест-кейсов): https://habr.com/ru/companies/otus/articles/904222/
- Pitest (Java mutation testing): https://pitest.org
- pytest-mutagen: https://github.com/Tejaswi-Goel/pytest-mutagen
- Meta TestGen-LLM paper: arxiv.org/abs/2402.09171
