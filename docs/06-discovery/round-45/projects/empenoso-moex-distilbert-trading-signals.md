# DistilBERT для торговых сигналов на Московской бирже (MOEX)

**Автор:** empenoso (Михаил Шардин)  
**Хабр:** https://habr.com/ru/articles/955612/  
**GitHub:** https://github.com/empenoso/llm-stock-market-predictor  
**Слой:** analytics  
**Дата:** октябрь 2025  
**Уникальность:** Первая русскоязычная статья на Хабре с полным воспроизводимым экспериментом применения трансформер-модели (DistilBERT) к данным MOEX для предсказания направления цены акций. Ключевой паттерн: OHLCV-данные → текстовые описания → DistilBERT fine-tuning → binary classification. Walk-forward валидация на 227+ акциях; AUC-ROC средний ~0.53, лучшие AFLT 0.72 / RTSB 0.70 / PIKK 0.70. Честный анализ ограничений: эффективный рынок делает задачу фундаментально сложной.

## Проблема: можно ли применить LLM к биржевым данным MOEX?

```
Традиционные подходы к предсказанию цен:
  → Технический анализ: MA, RSI, MACD — общеизвестны, арбитраж съеден
  → ML на числовых данных: XGBoost, LSTM — не учитывают контекст
  → Гипотеза: LLM обучены на текстах о рынках → перенесут знания?

Эксперимент:
  → Данные: OHLCV акций MOEX (227+ эмитентов)
  → Задача: бинарная классификация (цена завтра вырастет/упадёт?)
  → Модель: DistilBERT (трансформер-энкодер, HuggingFace)
  → Ключевая идея: числа → естественный язык → LLM

Исследовательский вопрос:
  → Может ли языковая модель, обученная на финансовых текстах,
    "читать" паттерны в ценовых данных через их текстовое описание?
```

## OHLCV → Текст → DistilBERT

```python
# empenoso: LLM для торговых сигналов MOEX
# habr.com/ru/articles/955612
# github.com/empenoso/llm-stock-market-predictor

import pandas as pd
import numpy as np
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import torch
from torch.utils.data import Dataset, DataLoader

def ohlcv_to_text(df: pd.DataFrame, ticker: str) -> str:
    """
    Ключевой паттерн: числовые данные → текстовое описание.
    DistilBERT работает с текстом → перевести OHLCV в слова.

    Три окна наблюдения:
    - short_term: последние 3 дня (краткосрочная динамика)
    - medium_term: последние 7 дней (среднесрочный тренд)
    - momentum: изменение скорости + объём
    """
    last_row = df.iloc[-1]
    prev_3d = df.iloc[-4:-1]
    prev_7d = df.iloc[-8:-1]

    # Краткосрочная динамика (3 дня)
    short_change = (df['close'].iloc[-1] - df['close'].iloc[-4]) / df['close'].iloc[-4]
    short_desc = _describe_change(short_change)

    # Среднесрочный тренд (7 дней)
    medium_change = (df['close'].iloc[-1] - df['close'].iloc[-8]) / df['close'].iloc[-8]
    medium_desc = _describe_change(medium_change)

    # Объём
    avg_volume = prev_7d['volume'].mean()
    vol_ratio = last_row['volume'] / avg_volume
    volume_desc = _describe_volume(vol_ratio)

    # Близость к уровням (High/Low)
    range_pos = (last_row['close'] - df['low'].min()) / (df['high'].max() - df['low'].min())
    level_desc = _describe_level(range_pos)

    text = (
        f"Акция {ticker}. "
        f"За последние 3 дня цена {short_desc}. "
        f"За последние 7 дней тренд {medium_desc}. "
        f"Объём торгов {volume_desc}. "
        f"Цена находится {level_desc} относительно диапазона."
    )
    return text


def _describe_change(pct: float) -> str:
    if pct > 0.05:  return "растёт сильно"
    if pct > 0.02:  return "растёт умеренно"
    if pct > 0:     return "слегка растёт"
    if pct > -0.02: return "слегка снижается"
    if pct > -0.05: return "снижается умеренно"
    return "падает сильно"


def _describe_volume(ratio: float) -> str:
    if ratio > 2.0: return "значительно выше среднего"
    if ratio > 1.3: return "выше среднего"
    if ratio > 0.7: return "на уровне среднего"
    return "ниже среднего"


def _describe_level(pos: float) -> str:
    if pos > 0.8: return "вблизи максимумов"
    if pos > 0.6: return "выше середины диапазона"
    if pos > 0.4: return "около середины диапазона"
    if pos > 0.2: return "ниже середины диапазона"
    return "вблизи минимумов"


class MOEXStockDataset(Dataset):
    """
    PyTorch Dataset: текстовые описания OHLCV → binary labels.
    label=1: цена выросла на следующий день
    label=0: цена упала или не изменилась
    """

    def __init__(self, texts: list[str], labels: list[int],
                  tokenizer: DistilBertTokenizer, max_length: int = 128):
        self.encodings = tokenizer(
            texts,
            truncation=True,
            padding=True,
            max_length=max_length,
            return_tensors="pt"
        )
        self.labels = torch.tensor(labels, dtype=torch.long)

    def __len__(self) -> int:
        return len(self.labels)

    def __getitem__(self, idx: int) -> dict:
        return {
            "input_ids": self.encodings["input_ids"][idx],
            "attention_mask": self.encodings["attention_mask"][idx],
            "labels": self.labels[idx]
        }
```

## Fine-tuning и Walk-Forward валидация

```python
class MOEXDistilBERTTrainer:
    """
    Fine-tuning DistilBERT для предсказания направления цены.
    Walk-forward валидация: обучение на прошлом, тест на будущем.
    """

    TRAINING_CONFIG = {
        "base_model": "distilbert-base-multilingual-cased",
        "learning_rate": 2e-5,
        "batch_size": 32,
        "epochs": 2,           # короткое обучение — мало данных на окно
        "fp16": True,          # смешанная точность
        "early_stopping": True,
        "hardware": "RTX 5060 Ti (CUDA 12.8 nightly для Blackwell)"
    }

    WALK_FORWARD_CONFIG = {
        "train_window": 252,   # 252 торговых дня ≈ 1 год обучения
        "test_window": 21,     # 21 день ≈ 1 месяц теста
        "step": 21,            # сдвиг окна на 21 день
        "description": "Walk-forward: модель переобучается на каждом шаге"
    }

    def walk_forward_validate(self, ticker_data: dict[str, pd.DataFrame]) -> dict:
        """
        Walk-forward валидация:
        1. Обучить на train_window торговых дней
        2. Предсказать на test_window
        3. Сдвинуть окно на step дней
        4. Повторить → усредненный AUC-ROC

        Честная оценка: никогда не используем будущее для обучения.
        """
        results = {}

        for ticker, df in ticker_data.items():
            ticker_aucs = []
            n = len(df)
            train_w = self.WALK_FORWARD_CONFIG["train_window"]
            test_w = self.WALK_FORWARD_CONFIG["test_window"]
            step = self.WALK_FORWARD_CONFIG["step"]

            for start in range(0, n - train_w - test_w, step):
                train_end = start + train_w
                test_end = train_end + test_w

                train_df = df.iloc[start:train_end]
                test_df = df.iloc[train_end:test_end]

                # Построить тексты и метки
                train_texts, train_labels = self._prepare_samples(train_df)
                test_texts, test_labels = self._prepare_samples(test_df)

                # Fine-tune DistilBERT
                model = self._finetune(train_texts, train_labels)

                # Оценить
                auc = self._compute_auc(model, test_texts, test_labels)
                ticker_aucs.append(auc)

            results[ticker] = {
                "mean_auc": np.mean(ticker_aucs),
                "std_auc": np.std(ticker_aucs),
                "n_windows": len(ticker_aucs)
            }

        return results


BENCHMARK_RESULTS = {
    "датасет": "227+ акций MOEX, исторические данные",
    "метрика": "AUC-ROC (бинарная классификация: вырастет/упадёт завтра)",
    "валидация": "Walk-forward (252-дневное обучение, 21-дневный тест)",

    "результаты": {
        "средний_AUC": 0.53,   # лишь немного лучше случайного (0.50)
        "лучшие_тикеры": {
            "AFLT": 0.72,      # Аэрофлот — наибольшая предсказуемость
            "RTSB": 0.70,      # РТС Страхование
            "PIKK": 0.70       # ПИК Group
        },
        "худшие_тикеры": {
            "PLZL": 0.33       # Полюс Золото — хуже случайного
        }
    },

    "выводы": {
        "эффективный_рынок": (
            "AUC ~0.53 — рынок близок к полусильной форме эффективности. "
            "Паттерны быстро арбитражируются участниками."
        ),
        "межтикерная_вариация": (
            "Разброс 0.33–0.72 между тикерами. "
            "Некоторые акции (AFLT) более предсказуемы."
        ),
        "честный_результат": (
            "DistilBERT не 'волшебная пуля'. "
            "Умеренная предиктивная сила на отдельных эмитентах."
        )
    }
}
```

## Ограничения и инженерные вызовы

```python
ENGINEERING_CHALLENGES = {
    "CUDA_12.8_нужен": {
        "проблема": "RTX 5060 Ti (Blackwell) требует CUDA 12.8 nightly",
        "решение": "Docker образ с нужной версией CUDA",
        "урок": "Новое железо = новый стек; проверяй совместимость до обучения"
    },

    "мало_данных_на_окно": {
        "проблема": "252 торговых дня ≈ 500-1000 примеров на тикер — мало для LLM",
        "следствие": "Только 2 эпохи обучения; больше → переобучение",
        "альтернатива": "Few-shot с предобученным финансовым BERT"
    },

    "нет_фундаментального_контекста": {
        "проблема": "Модель видит только OHLCV; не знает о новостях, отчётах, макро",
        "улучшение": "Добавить текстовые новости как дополнительный контекст"
    },

    "transaction_costs": {
        "проблема": "AUC 0.53 → прибыль до комиссий; после комиссий ≈ 0",
        "урок": "Торговая стратегия должна учитывать spread + биржевую комиссию"
    }
}

SYSTEM_PROFILE = {
    "автор": "empenoso (Михаил Шардин, независимый разработчик)",
    "статус": "Open-source эксперимент (не production-система)",
    "лицензия": "GitHub: открытый код",
    "воспроизводимость": "✅ Docker + публичные данные MOEX",
    "модель": "DistilBERT (distilbert-base-multilingual-cased, HuggingFace)",
    "биржа": "MOEX (Московская биржа, 227+ тикеров)"
}
```

## Применение к Lorenzo

```python
# Lorenzo: MOEX-паттерн для аналитики текстовых сигналов

class LorenzoTextSignalAnalyzer:
    """
    empenoso паттерн для Lorenzo:
    Вместо OHLCV-данных → метрики качества docs/.
    Предсказание: "эта тема вырастет в следующем раунде"?

    Аналог walk-forward: тренд по раундам R01–R44 → прогноз R45.
    """

    def topics_to_text(self, round_stats: dict) -> str:
        """
        Статистика раунда → текстовое описание для LLM-анализа.
        Аналог ohlcv_to_text: числа → слова → LLM понимает.
        """
        n_projects = round_stats["n_projects"]
        top_topic = round_stats["top_topic"]
        trend = round_stats["trend"]

        return (
            f"Раунд {round_stats['round']}. "
            f"Найдено {n_projects} проектов. "
            f"Ключевая тема: {top_topic}. "
            f"Интерес к теме {trend}."
        )
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **MOEX DistilBERT + Finam LLM (R26)** | Finam API данных + DistilBERT паттерн текстового описания = улучшенные сигналы |
| **MOEX DistilBERT + T-Bank T-Lite (R42)** | Русскоязычная LLM вместо multilingual DistilBERT → лучше понимает RU финансовый контекст |
| **MOEX DistilBERT + Yandex LLM Eval (R44)** | Walk-forward как time-series benchmark: оценка деградации модели во времени |
| **MOEX DistilBERT + LangFuse (R38)** | Трейсинг каждого предсказания: перплексия по тикеру → когда модель не уверена |
| **MOEX DistilBERT + Synthetic Data (R39)** | Синтетические OHLCV сценарии для аугментации маленьких датасетов по тикерам |

## Контакт

- Статья: https://habr.com/ru/articles/955612/ (октябрь 2025)
- GitHub: https://github.com/empenoso/llm-stock-market-predictor
- Автор: empenoso (Михаил Шардин, независимый разработчик)
- MOEX API: moexalgo.github.io
- Смежная (Finam LLM trading, R26): docs/06-discovery/round-26/
- Смежная (AML LLM advisor, R42): docs/06-discovery/round-42/projects/llm-aml-fraud-contextual-advisor-fintech.md
