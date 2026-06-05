# Как я поймал Трансформер на читерстве: гроккинг и Mechanistic Interpretability

> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Автор:** fanat503 (Хабр, март 2025)  
**Хабр:** https://habr.com/ru/articles/1008656/  
**GitHub:** https://github.com/fanat503/Math-Grokking-Transformer  
**Слой:** analytics / orchestration  
**Дата:** март 2025  
**Уникальность:** Практическая механистическая интерпретация трансформера: автор вручную анализирует матрицы внимания Q×K^T по 4 слоям и 4 головам, находит отсутствующую "Carry-over Head" (голова для переноса в арифметике) и доказывает specification gaming (читерство через Name Mover Head вместо реального счёта). Единственная статья 2024-2026 на Хабре с рабочим кодом + forensic-аудитом нейросети.

## Проблема: точность ≠ понимание

```
Стандартная оценка LLM:
  Train accuracy: 99.8% → модель "обучилась"?
  Нет! → может быть shortcut learning (читерство)

Что реально происходит внутри:
  Grokking: тысячи эпох → модель меморизует
             → резкий скачок → "генерализация"
  Но как именно генерализует?
  → Нужна хирургия: mechanistic interpretability

Цель статьи: поймать трансформер на читерстве
  → Доказать через матрицы внимания
  → Показать: стандартные метрики СКРЫВАЮТ это
```

## Custom Transformer: 1M параметров для арифметики

```python
import torch
import torch.nn as nn

class MathTransformer(nn.Module):
    """
    Минимальный трансформер для задачи: a + b = c (mod p)
    Цель: интерпретируемость > производительность
    Параметры выбраны для читаемости attention-матриц.
    """

    def __init__(self, vocab_size: int = 113, d_model: int = 128,
                 n_heads: int = 4, n_layers: int = 4):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, d_model)
        self.pos_encoding = nn.Embedding(10, d_model)  # max len

        self.layers = nn.ModuleList([
            TransformerBlock(d_model, n_heads)
            for _ in range(n_layers)
        ])

        self.output_head = nn.Linear(d_model, vocab_size)

    def forward(self, x: torch.Tensor) -> tuple:
        # Возвращаем attention_weights для интерпретации
        attention_weights = []
        h = self.embedding(x) + self.pos_encoding(torch.arange(x.size(1)))

        for layer in self.layers:
            h, attn = layer(h)
            attention_weights.append(attn)  # сохраняем для анализа

        logits = self.output_head(h[:, -1, :])  # последний токен = ответ
        return logits, attention_weights


class TransformerBlock(nn.Module):
    def __init__(self, d_model: int, n_heads: int):
        super().__init__()
        self.attention = MultiHeadAttention(d_model, n_heads)
        self.norm1 = nn.LayerNorm(d_model)
        self.ffn = nn.Sequential(
            nn.Linear(d_model, d_model * 4),
            nn.GELU(),
            nn.Linear(d_model * 4, d_model)
        )
        self.norm2 = nn.LayerNorm(d_model)

    def forward(self, x):
        attn_out, weights = self.attention(x)
        x = self.norm1(x + attn_out)
        x = self.norm2(x + self.ffn(x))
        return x, weights
```

## Mechanistic Interpretability: анализ матриц внимания

```python
class AttentionAuditor:
    """
    Хирургический аудит: что каждая голова внимания реально делает?
    """

    def extract_attention_patterns(self, model: MathTransformer,
                                    test_examples: list) -> AttentionReport:
        model.eval()
        all_patterns = {}

        for example in test_examples:
            _, attention_weights = model(example)

            for layer_idx, layer_attn in enumerate(attention_weights):
                for head_idx in range(layer_attn.size(1)):
                    key = f"L{layer_idx}_H{head_idx}"
                    # attention_weights: [batch, heads, seq_len, seq_len]
                    pattern = layer_attn[0, head_idx].detach().cpu()
                    all_patterns.setdefault(key, []).append(pattern)

        return self._classify_heads(all_patterns)

    def _classify_heads(self, patterns: dict) -> AttentionReport:
        """
        По паттернам внимания определить роль каждой головы.
        """
        classified = {}
        for head_name, head_patterns in patterns.items():
            avg_pattern = torch.stack(head_patterns).mean(0)

            # Диагностика: на что смотрит эта голова?
            head_type = self._infer_head_type(avg_pattern)
            classified[head_name] = head_type

        return AttentionReport(
            heads=classified,
            missing_heads=self._find_missing_heads(classified)
        )

    def _infer_head_type(self, pattern: torch.Tensor) -> str:
        """
        Известные типы голов (из исследований Anthropic/OpenAI):
        """
        if self._is_diagonal(pattern):
            return "Position Head"        # смотрит на текущую позицию
        elif self._is_copy_pattern(pattern):
            return "Name Mover Head"      # копирует токены из прошлого
        elif self._is_carry_pattern(pattern):
            return "Carry-over Head"      # обрабатывает перенос в арифметике
        elif self._is_induction(pattern):
            return "Induction Head"       # паттерн [A][B]...[A] → [B]
        else:
            return "Unknown"

    def _find_missing_heads(self, classified: dict) -> list:
        """
        Для задачи арифметики должна быть Carry-over Head.
        Если её нет → модель читерит через другой механизм.
        """
        head_types = set(classified.values())
        expected = {"Position Head", "Name Mover Head", "Carry-over Head"}
        missing = expected - head_types

        if "Carry-over Head" in missing:
            print("⚠️  WARNING: No Carry-over Head found!")
            print("Model is likely using shortcut learning for carries.")

        return list(missing)
```

## Specification Gaming: доказательство читерства

```python
class SpecificationGamingDetector:
    """
    Specification Gaming = модель достигает цели нечестным путём.
    В нашем случае: Name Mover Head копирует цифры вместо счёта.
    """

    def prove_shortcut_learning(self, model, test_set) -> ShortcutReport:
        """
        Тест: если убрать возможность копирования → точность упадёт?
        """
        # Нормальная точность
        baseline_acc = self.evaluate(model, test_set)

        # Патч: обнулить Name Mover Heads (активационный патчинг)
        patched_model = self.ablate_heads(
            model,
            head_types_to_ablate=["Name Mover Head"]
        )
        patched_acc = self.evaluate(patched_model, test_set)

        # Если точность резко упала → модель зависела от копирования
        shortcut_dependency = baseline_acc - patched_acc

        return ShortcutReport(
            baseline_accuracy=baseline_acc,
            patched_accuracy=patched_acc,
            shortcut_dependency=shortcut_dependency,
            conclusion=(
                "Shortcut learning confirmed" if shortcut_dependency > 0.20
                else "Genuine generalization"
            )
        )

    def ablate_heads(self, model, head_types_to_ablate: list):
        """Активационный патчинг: обнулить конкретные головы."""
        patched = copy.deepcopy(model)
        for head_name, head_type in self.head_classification.items():
            if head_type in head_types_to_ablate:
                layer_idx, head_idx = self._parse_head_name(head_name)
                with torch.no_grad():
                    patched.layers[layer_idx].attention.heads[head_idx].zero_()
        return patched
```

## Гроккинг: внезапная генерализация

```python
# Феномен гроккинга: модель сначала меморизует → потом "понимает"

GROKKING_TRAINING_CONFIG = {
    "optimizer": "AdamW",
    "weight_decay": 1.0,      # ключевой параметр: высокий L2 вынуждает сжатие
    "learning_rate": 1e-3,
    "epochs": 50_000,         # нужно очень много эпох
    "train_fraction": 0.3,    # только 30% данных для обучения

    # Observation:
    # Epoch 100:    train_loss → 0, val_loss → высокий (memorization)
    # Epoch 1000:   без изменений (plateau)
    # Epoch 10000+: val_loss резко падает (grokking!)
}

# Почему weight_decay = 1.0 помогает интерпретируемости?
# → Высокий L2 штраф вынуждает модель находить КОМПАКТНЫЕ
#   (circuit-level) представления вместо memorizing
# → Compact circuits = более читаемые attention patterns
# → Можно увидеть что модель "действительно выучила"
```

## Audit Trail для регуляторов: от теории к практике

```python
class LLMAuditTrail:
    """
    Практическое применение механистической интерпретации:
    доказательная база для регуляторного аудита LLM-систем.
    """

    def generate_audit_report(self, model, task_type: str) -> AuditReport:
        """
        Генерировать воспроизводимый отчёт для регулятора:
        - Какие circuits задействованы в принятии решений
        - Есть ли shortcut learning
        - Каковы ограничения модели
        """
        auditor = AttentionAuditor()
        patterns = auditor.extract_attention_patterns(model, self.test_set)

        shortcut_test = SpecificationGamingDetector().prove_shortcut_learning(
            model, self.test_set
        )

        return AuditReport(
            model_id=model.model_id,
            task_type=task_type,
            attention_circuits=patterns.heads,
            missing_circuits=patterns.missing_heads,
            shortcut_analysis=shortcut_test,
            reproduction_code="github.com/fanat503/Math-Grokking-Transformer",
            attestation={
                "claim": "Model uses genuine pattern generalization",
                "evidence": patterns.serialize(),
                "confidence": shortcut_test.is_genuine_confidence()
            }
        )
```

## Связь с проектами Anthropic: Circuits research

```python
MECHANISTIC_INTERPRETABILITY_LINEAGE = {
    "Anthropic Circuits": {
        "оригинал": "Zoom In: An Introduction to Circuits (2020)",
        "идея": "Нейросети имеют interpretable circuits (полиномы, кривые, детекторы)",
        "связь с статьёй": "Carry-over Head = специализированный circuit для арифметики"
    },
    "Induction Heads": {
        "оригинал": "In-context Learning and Induction Heads (Anthropic, 2022)",
        "идея": "[A][B]...[A] → [B] паттерн — основа in-context learning",
        "связь с статьёй": "Обнаружены Induction Heads в слоях 1-2"
    },
    "OpenAI Grokking Research": {
        "оригинал": "Grokking: Generalization Beyond Overfitting (2022)",
        "связь с статьёй": "Воспроизведение феномена на custom transformer"
    }
}
```

## Применение к Lorenzo

```python
# improve_model_audit.py (паттерн):

class LorenzoModelAuditor:
    """
    Проверка TF-IDF / BM25 моделей Lorenzo на bias и shortcuts.
    Аналог механистической интерпретации для классических ML моделей.
    """

    def audit_tfidf_shortcuts(self, model, test_queries: list) -> AuditReport:
        # Эквивалент attention analysis для TF-IDF:
        # проверить: модель ранжирует по смыслу или по stopwords?

        stopword_queries = [
            q for q in test_queries
            if all(w in STOPWORDS for w in q.split())
        ]

        # Если высокий ранк при бессмысленных запросах → shortcut
        shortcut_score = self.evaluate_ranking(model, stopword_queries)

        return AuditReport(
            model_type="TF-IDF",
            shortcut_score=shortcut_score,
            recommendation=(
                "Добавить minimum_df threshold" if shortcut_score > 0.3
                else "Модель OK"
            )
        )
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **XAI + LLM Judge (R28)** | Судья объясняет своё решение через attention weights → аудитный след |
| **XAI + HITL (R30)** | Человек видит какие circuits активированы → лучше подтверждает рискованные решения |
| **XAI + DBRM medical (R31)** | Медицинская система: объяснить врачу почему AI-судья поставил safety < 0.9 |
| **XAI + AI AppSec (R22)** | Детектировать adversarial inputs через аномальные attention patterns |
| **XAI + Comprehension Debt (R29)** | Measure "comprehension circuits" quality в AI-сгенерированном коде |

## Контакт

- Статья: https://habr.com/ru/articles/1008656/ (март 2025)
- GitHub: https://github.com/fanat503/Math-Grokking-Transformer (PyTorch, MIT-like)
- Смежная (Alemetria Protocol, аудит против галлюцинаций): https://habr.com/ru/articles/1033404/
- Anthropic Circuits: transformer-circuits.pub
- OpenAI Grokking paper: arxiv.org/abs/2201.02177
