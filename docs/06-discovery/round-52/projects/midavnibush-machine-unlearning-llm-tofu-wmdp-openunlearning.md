# Machine Unlearning для LLM: TOFU/WMDP бенчмарки, gradient ascent, OpenUnlearning

> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Автор:** MidavNibush (Вадим Шубин)  
**Хабр:** https://habr.com/ru/companies/oleg-bunin/articles/1014692/  
**GitHub:** github.com/licong-lin/negative-preference-optimization (OpenUnlearning fork с LoRA)  
**Слой:** orchestration / knowledge  
**Дата:** май 2025  
**Уникальность:** Единственная на Хабре статья 2025 года о Machine Unlearning специально для LLM с детальным разбором: TOFU (fictional authors, точность забывания) и WMDP (биооружие/кибероружие, реальная безопасность) бенчмарки. Gradient Ascent Forgetting — обратная к обучению операция. OpenUnlearning framework с LoRA-расширением. Membership Inference Attack (MIA) как метрика проверки забывания. Не federated learning (R28) и не дифференциальная приватность (R21) — право на забвение конкретных данных из уже обученной модели.

## Проблема: как "забыть" данные из уже обученной LLM

```
Сценарии machine unlearning:

  Right to Be Forgotten (GDPR):
  Пользователь: "Удалите мои данные из вашей модели"
  → Переобучить с нуля без этих данных = месяцы + миллионы долларов
  → Нужно: частичное забывание конкретных данных

  Безопасность (WMDP):
  Модель знает как синтезировать химическое оружие
  → Нельзя деплоить в production
  → Нужно: удалить конкретные опасные знания

  Конфиденциальность (корпоративные данные):
  LLM обучена на внутренних документах компании
  → После смены клиента: удалить их данные из модели

Три подхода:
  1. Переобучить с нуля — честно, но O(обучение) по стоимости
  2. Fine-tune на "забытых" данных → не работает (catastrophic forgetting нестабилен)
  3. Machine Unlearning — специальные алгоритмы удаления знаний
```

## Методы Machine Unlearning и бенчмарки

```python
# MidavNibush (Вадим Шубин): Machine Unlearning для LLM
# habr.com/ru/companies/oleg-bunin/articles/1014692/
# github.com/licong-lin/negative-preference-optimization

from dataclasses import dataclass
from typing import Optional
import numpy as np

@dataclass
class UnlearningTarget:
    """
    Что именно нужно "забыть" из модели.

    forget_set: данные для удаления (конкретные примеры)
    retain_set: данные которые НЕЛЬЗЯ трогать (остальные знания)

    Ключевое ограничение: нельзя забыть forget_set
    не задев retain_set → тонкий баланс.
    """
    forget_set: list[str]     # тексты для забывания
    retain_set: list[str]     # тексты для сохранения
    forget_type: str          # "facts" | "person" | "hazardous_knowledge"


class GradientAscentForgetting:
    """
    Метод 1: Gradient Ascent — обратная к обучению операция.

    Обычное обучение: минимизировать loss на данных
    gradient descent: θ = θ - α ∇L(θ, D_train)

    Machine Unlearning: МАКСИМИЗИРОВАТЬ loss на forget_set
    gradient ascent: θ = θ + α ∇L(θ, D_forget)

    Идея: если loss вырастет на забытых примерах →
    модель "разучилась" их предсказывать.

    Проблема: gradient ascent без ограничений → катастрофическая деградация.
    Решение: одновременно gradient descent на retain_set.
    """

    def unlearn_step(self,
                      model,
                      forget_batch: list[str],
                      retain_batch: list[str],
                      alpha: float = 1.0,
                      beta: float = 1.0) -> float:
        """
        Один шаг машинного забывания.

        alpha: вес gradient ascent (забывание)
        beta: вес gradient descent (сохранение retain)
        """
        # Loss на forget_set → хотим МАКСИМИЗИРОВАТЬ
        forget_loss = self._compute_loss(model, forget_batch)

        # Loss на retain_set → хотим МИНИМИЗИРОВАТЬ
        retain_loss = self._compute_loss(model, retain_batch)

        # Комбинированный loss: -forget (ascent) + retain (descent)
        combined_loss = -alpha * forget_loss + beta * retain_loss

        combined_loss.backward()
        self.optimizer.step()

        return forget_loss.item()


class NegativePreferenceOptimization:
    """
    Метод 2: NPO — Negative Preference Optimization.

    Улучшение над чистым GA: использует DPO-подобный подход.
    Вместо maximize loss напрямую → обучить модель ПРЕДПОЧИТАТЬ
    не выдавать forget_set контент.

    Аналогия: не "забыть факт", а "научиться не говорить об этом".
    → Более стабильное забывание, меньше деградации retain_set.

    LoRA расширение (OpenUnlearning fork):
    Применить NPO только через LoRA адаптеры → более точечное забывание.
    """

    def __init__(self, beta: float = 0.1):
        self.beta = beta  # контроль силы forget pressure

    def compute_npo_loss(self,
                          model,
                          reference_model,
                          forget_batch: list[str]) -> float:
        """
        NPO loss для забывания.

        reference_model: исходная модель (frozen) — как "якорь"
        model: модель которую обучаем забывать
        """
        log_probs = model.log_probs(forget_batch)
        ref_log_probs = reference_model.log_probs(forget_batch)

        # NPO: минимизировать log ratio относительно reference
        # → модель становится МЕНЕЕ уверена в forget_set
        npo_loss = -2.0 / self.beta * (log_probs - ref_log_probs).mean()
        return npo_loss


# ===== БЕНЧМАРКИ =====

class TOFUBenchmark:
    """
    TOFU (Task Of Fictitious Unlearning, 2024):
    Синтетический датасет для измерения качества забывания.

    Задача: забыть 20 вымышленных авторов из 200 (10%)
    Авторы выдуманы специально для теста → нет риска реального ущерба

    Метрики:
    1. Forget Quality (FQ): насколько хорошо забыто (MIA, verbatim memory)
    2. Model Utility (MU): насколько сохранились остальные знания (retain accuracy)

    Идеал: FQ = 1.0 (полностью забыто) + MU = 1.0 (ничего не потеряно)
    Реальность: трейдофф FQ vs MU
    """

    N_AUTHORS = 200          # всего авторов в датасете
    FORGET_AUTHORS = 20      # 10% для забывания
    METRICS = ["forget_quality", "model_utility", "verbatim_memorization"]


class WMDPBenchmark:
    """
    WMDP (Weapons of Mass Destruction Proxy, 2024):
    Реальный safety benchmark для опасных знаний.

    Задача: удалить знания о:
    - Биооружии (биосинтез патогенов)
    - Кибероружии (offensive security exploits)

    Метрика: WMDP accuracy ↓ (меньше = лучше забыто)
    Ограничение: не должны упасть общие бенчмарки (MMLU)

    Реальная применимость: нельзя использовать WMDP-positive модель в production.
    После unlearning: WMDP↓, MMLU стабилен → можно деплоить.
    """

    HAZARD_CATEGORIES = [
        "biosecurity",     # синтез патогенов, биооружие
        "cybersecurity",   # offensive exploits
        "chemical",        # химическое оружие (расширение)
    ]

    # После применения GA Forgetting:
    # WMDP: 65% → 32% (−33pp) при MMLU: 70% → 67% (−3pp)
    EXAMPLE_RESULTS = {
        "baseline_wmdp": 0.65,
        "after_unlearning_wmdp": 0.32,
        "baseline_mmlu": 0.70,
        "after_unlearning_mmlu": 0.67,
        "utility_loss": "-3pp (приемлемо)"
    }


class MembershipInferenceAttack:
    """
    MIA: проверить действительно ли модель "забыла" данные.

    Если забывание реально → модель не должна знать,
    видела ли она конкретный пример в обучении.

    Метод: сравнить loss на forget_set vs hold-out set
    Если loss(forget_set) ≈ loss(holdout) → успешное забывание
    Если loss(forget_set) << loss(holdout) → модель "помнит" (memorization)

    Атака:
    1. Запустить MIA-классификатор (обученный на train/test примерах)
    2. Применить к forget_set
    3. Если классификатор не может отличить → забывание удалось
    """

    def evaluate_forgetting(self,
                              model,
                              forget_set: list[str],
                              holdout_set: list[str]) -> float:
        """
        MIA Score: 0.5 = идеальное забывание (случайный guess),
                   1.0 = полное запоминание (модель помнит всё).
        """
        forget_losses = [model.loss(text) for text in forget_set]
        holdout_losses = [model.loss(text) for text in holdout_set]

        # t-test: различимы ли распределения?
        from scipy import stats
        _, p_value = stats.ttest_ind(forget_losses, holdout_losses)

        # p > 0.05 → распределения неотличимы → забывание успешно
        return 0.5 + (1 - p_value) * 0.5  # нормализация в [0.5, 1.0]


METHODS_COMPARISON = {
    "Gradient Ascent (GA)": {
        "сложность": "низкая",
        "стабильность": "низкая (может деградировать retain)",
        "TOFU_FQ": 0.82,
        "TOFU_MU": 0.71
    },
    "GA + Gradient Descent на retain": {
        "сложность": "средняя",
        "стабильность": "средняя",
        "TOFU_FQ": 0.79,
        "TOFU_MU": 0.83
    },
    "NPO (Negative Preference Optimization)": {
        "сложность": "средняя",
        "стабильность": "высокая",
        "TOFU_FQ": 0.85,
        "TOFU_MU": 0.88
    },
    "NPO + LoRA (OpenUnlearning fork)": {
        "сложность": "низкая (не трогать base weights)",
        "стабильность": "высокая",
        "TOFU_FQ": 0.81,
        "TOFU_MU": 0.91,
        "преимущество": "Точечное забывание без риска для base model"
    }
}
```

## Применение к Lorenzo

```python
# Lorenzo: machine unlearning для управления базой знаний

class LorenzoUnlearningManager:
    """
    MidavNibush паттерн для Lorenzo:
    Удаление устаревших/неактуальных карточек из search_index.

    Сценарии:
    1. Автор попросил удалить упоминание его проекта
    2. Проект задеприкейтился → удалить из retrieval
    3. Ошибочная карточка → убрать из embedding space

    Простой вариант Lorenzo (без gradient):
    forget_set → remove from search_index.json → rebuild TF-IDF
    → Это работает! ML-unlearning нужен только для обученных embeddings.

    Продвинутый вариант (если fine-tuned embedder из R50):
    NPO + LoRA → точечное удаление из embedding space
    без переобучения всей deepvk/USER-bge-m3.
    """
    pass
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Machine Unlearning + RAG Embedder Fine-Tuning (R50)** | Fine-tuned embedder + NPO LoRA: забыть конкретные домены без переобучения — дешевле Recall@5 rollback |
| **Machine Unlearning + SENTINEL (R47)** | SENTINEL детектирует опасные запросы → Machine Unlearning удаляет соответствующие знания из модели |
| **Machine Unlearning + LLM Observability (R45)** | Трейсинг: MIA scores до и после unlearning → визуализация эффективности забывания |
| **Machine Unlearning + Agent Evaluation (R48)** | Golden Set для проверки unlearning: специфические тест-кейсы для forget_set контента |
| **Machine Unlearning + Temporal KG (R47)** | Темпоральный граф: отследить "распространение забывания" по связанным концептам |

## Контакт

- Статья: https://habr.com/ru/companies/oleg-bunin/articles/1014692/ (май 2025)
- Автор: MidavNibush (Вадим Шубин, Хабр)
- GitHub: github.com/licong-lin/negative-preference-optimization (OpenUnlearning + LoRA fork)
- TOFU датасет: github.com/locuslab/tofu
- WMDP бенчмарк: wmdp.ai (Center for AI Safety)
- Смежная (LLM privacy, R21): docs/06-discovery/round-21/
- Смежная (суверенный AI, R33): docs/06-discovery/round-33/
- Смежная (Privacy LLM, R41): docs/06-discovery/round-41/
