# Обучение эмбеддингов GitHub репозиториев: персонализация без backend

**Автор:** Puzer (Дмитрий)  
**Хабр:** https://habr.com/ru/articles/983080/  
**GitHub:** https://github.com/Puzer/github-repo-embeddings  
**Demo:** https://puzer.github.io/github_recommender (client-side WASM)  
**Слой:** analytics / knowledge  
**Дата:** январь 2025  
**Уникальность:** Гибридные embeddings: Qwen3-Embedding-0.6B (MRL, 128 dims) из README.md → дообучение через collaborative filtering на 4M GitHub Stars. Cold-start решён через среднее векторов starred репозиториев пользователя. Весь inference в браузере через WASM-скомпилированный USearch (ANN по 2.5M items). Zero backend infrastructure.

## Проблема: холодный старт и приватность

```
Стандартные рекомендательные системы:
  → Нужен backend: хранить user history, считать рекомендации
  → Cold start: новый пользователь → нет истории → нет рекомендаций
  → Приватность: все взаимодействия пользователя уходят на сервер

Решение Puzer:
  → Cold start: GitHub Stars = готовая история (публичная!)
  → Inference: WASM в браузере → данные не покидают клиент
  → Backend: не нужен совсем (статический хостинг + WASM)

Demo: puzer.github.io/github_recommender
  → Ввести GitHub username → мгновенные рекомендации
  → 2.5M репозиториев, 100% client-side
```

## Двухэтапное обучение: текст + поведение

```python
# github-repo-embeddings: двухфазный pipeline обучения

# Фаза 1: Text embeddings из README.md

from transformers import AutoModel, AutoTokenizer
import torch

class RepoTextEmbedder:
    """
    Начальные embeddings из README.md через Qwen3-Embedding-0.6B.
    MRL (Matryoshka Representation Learning): 128-dim проекция из 1024-dim.
    MRL позволяет truncate до меньших размеров без переобучения.
    """

    def __init__(self):
        self.model = AutoModel.from_pretrained("Qwen/Qwen3-Embedding-0.6B")
        self.tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen3-Embedding-0.6B")

    def embed_repo(self, readme_text: str) -> torch.Tensor:
        # Truncate README до 512 токенов
        inputs = self.tokenizer(
            readme_text[:2000],
            return_tensors="pt",
            max_length=512,
            truncation=True
        )
        with torch.no_grad():
            output = self.model(**inputs)
        # Mean pooling → L2 normalize
        embedding = output.last_hidden_state.mean(dim=1)
        embedding = torch.nn.functional.normalize(embedding, dim=-1)
        return embedding  # shape: (1, 1024)


# Фаза 2: Collaborative Filtering дообучение

class CollaborativeFilteringTrainer:
    """
    Данные: 4 миллиона GitHub Stars (user → starred repos)
    Метод: metric learning (contrastive loss)

    Идея: репозитории, которые часто starred вместе,
    должны быть близко в embedding пространстве.
    """

    def __init__(self, embed_dim: int = 128):
        self.embed_dim = embed_dim
        self.projection = torch.nn.Linear(1024, embed_dim)

    def contrastive_loss(self, anchor: torch.Tensor,
                         positive: torch.Tensor,
                         negative: torch.Tensor,
                         margin: float = 0.5) -> torch.Tensor:
        """
        anchor: embedding репо A
        positive: репо B, которое часто starred вместе с A
        negative: случайный репо (не связан с A)

        Цель: dist(anchor, positive) << dist(anchor, negative)
        """
        d_pos = torch.nn.functional.cosine_similarity(anchor, positive)
        d_neg = torch.nn.functional.cosine_similarity(anchor, negative)
        loss = torch.clamp(margin - d_pos + d_neg, min=0)
        return loss.mean()

    def build_training_pairs(self, user_stars: dict) -> list:
        """
        Из истории stars пользователей строим обучающие пары.

        user A starred: [pytorch, numpy, sklearn]
        → пары: (pytorch, numpy), (pytorch, sklearn), (numpy, sklearn)
        → для каждой пары: добавить negative (случайный репо)
        """
        pairs = []
        for user, starred_repos in user_stars.items():
            for i, repo_a in enumerate(starred_repos):
                for repo_b in starred_repos[i+1:]:
                    # Positive pair
                    negative = self._sample_negative(starred_repos)
                    pairs.append((repo_a, repo_b, negative))
        return pairs
```

## Cold Start: профиль пользователя из Stars

```python
import requests
import numpy as np

class UserProfileBuilder:
    """
    Ключевой insight: не нужна история взаимодействий!
    GitHub Stars = бесплатная публичная история интересов.

    Профиль пользователя = среднее векторов starred репозиториев.
    Новый пользователь (даже без истории на нашем сайте)
    → мгновенный профиль из его публичного GitHub аккаунта.
    """

    def build_profile(self, github_username: str) -> np.ndarray:
        # Получить starred repos через GitHub API (публичные, без auth)
        starred = self._fetch_starred(github_username)

        if not starred:
            # True cold start: нет stars → популярные репо
            return self._popular_repos_centroid()

        # Профиль = среднее эмбеддингов starred repos
        embeddings = [self.repo_embeddings[repo] for repo in starred
                      if repo in self.repo_embeddings]

        if not embeddings:
            return self._popular_repos_centroid()

        profile = np.mean(embeddings, axis=0)
        profile = profile / np.linalg.norm(profile)  # L2 normalize
        return profile  # 128-dim вектор

    def _fetch_starred(self, username: str) -> list[str]:
        """GitHub API: starred repos без авторизации (до 100 шт.)"""
        url = f"https://api.github.com/users/{username}/starred"
        response = requests.get(url, params={"per_page": 100})
        return [repo["full_name"] for repo in response.json()]


class RecommendationEngine:
    """
    Рекомендации = ближайшие соседи профиля в embedding пространстве.
    """

    def recommend(self, user_profile: np.ndarray,
                  top_k: int = 20,
                  exclude: set = None) -> list[str]:
        # ANN search через FAISS / USearch
        scores, indices = self.index.search(
            user_profile.reshape(1, -1),
            k=top_k + len(exclude or [])
        )

        recommendations = []
        for idx, score in zip(indices[0], scores[0]):
            repo_name = self.idx_to_repo[idx]
            if exclude and repo_name in exclude:
                continue
            recommendations.append({
                "repo": repo_name,
                "score": float(score)
            })
            if len(recommendations) >= top_k:
                break

        return recommendations
```

## WASM Client-Side Inference: нет backend

```javascript
// puzer.github.io/github_recommender
// Весь inference в браузере через WebAssembly

// USearch WASM: approximate nearest neighbor search
// github.com/unum-cloud/usearch

import { newIndexFromSerialized } from 'usearch-wasm';

class ClientSideRecommender {
    async initialize() {
        // Загрузить предвычисленный индекс (2.5M repos × 128 dims)
        // Размер: ~1.3 GB (компрессированный)
        const indexBuffer = await fetch('/data/repos_index.bin')
            .then(r => r.arrayBuffer());

        this.index = await newIndexFromSerialized(indexBuffer);
        this.repoNames = await fetch('/data/repo_names.json')
            .then(r => r.json());
    }

    async recommend(githubUsername) {
        // 1. Получить starred repos через GitHub API
        const starred = await this.fetchStarred(githubUsername);

        // 2. Загрузить их embeddings из локального кэша
        const embeddings = await this.loadEmbeddings(starred);

        // 3. Посчитать профиль (среднее) — всё в браузере
        const profile = this.meanVector(embeddings);

        // 4. ANN search через USearch WASM
        const results = await this.index.search(profile, 20);

        return results.map(idx => this.repoNames[idx]);
    }
}

// Результат:
// - 0 запросов к backend для inference
// - Данные пользователя не покидают браузер
// - Latency: ~100 мс на ANN search по 2.5M items
```

## Качество: +10% от collaborative filtering

```python
QUALITY_COMPARISON = {
    "только text (Qwen3 README)": {
        "Recall@10": 0.31,
        "описание": "Похожие репо по описанию, но без учёта поведения"
    },
    "только collaborative filtering": {
        "Recall@10": 0.38,
        "описание": "Поведенческие паттерны, холодный старт плохой"
    },
    "hybrid (text + CF)": {
        "Recall@10": 0.42,  # +10% vs лучшего одиночного
        "описание": "Лучший результат: текст решает cold start, CF улучшает качество"
    }
}

# Метрика: Recall@10 на held-out test set
# Test: у пользователей убрали 20% starred repos → предсказать их
```

## Применение к Lorenzo

```python
# Рекомендации проектов из базы знаний Lorenzo:

class LorenzoProjectRecommender:
    """
    Lorenzo собирает 140+ проектов.
    Паттерн Puzer: embeddings + collaborative filtering
    для рекомендации похожих проектов.

    Пользователь читает: agentfs.md
    → Система рекомендует: agent-memory-mcp.md, yodoca.md, rufler.md
    """

    def recommend_similar(self, current_project: str,
                          user_history: list[str]) -> list[str]:
        # Профиль = среднее векторов прочитанных проектов
        profile = np.mean([self.embeddings[p] for p in user_history], axis=0)
        return self.ann_search(profile, top_k=5)
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **GitHub Embeddings + Enterprise RAG (R32)** | Embeddings из документов корпоративной базы → персонализированный RAG |
| **GitHub Embeddings + Cognitive Memory (R31)** | Memory nodes хранят историю взаимодействий → персональный профиль |
| **GitHub Embeddings + Collab Finder Lorenzo** | Улучшить поиск партнёрских проектов: hybrid text+behavior |
| **GitHub Embeddings + MT-Bench RU (R34)** | Рекомендовать учебные материалы на основе профиля студента |
| **GitHub Embeddings + HITL (R30)** | HITL feedback от пользователя → обновление весов collaborative filtering |

## Контакт

- Статья: https://habr.com/ru/articles/983080/ (январь 2025)
- GitHub: https://github.com/Puzer/github-repo-embeddings
- Live demo: https://puzer.github.io/github_recommender
- Qwen3-Embedding: huggingface.co/Qwen/Qwen3-Embedding-0.6B
- USearch WASM: github.com/unum-cloud/usearch
- Смежная (рекомендации фильмов cold start + GPT): https://habr.com/ru/articles/1029318/
