# docs-toolkit Deployment Recipes

Готовые рецепты для запуска `docs-toolkit serve` в production. Phase VIII
of [`DEVELOPMENT_STATUS.md`](../DEVELOPMENT_STATUS.md).

---

## Quick deploy options

| Способ | Время | Сложность | Когда использовать |
|---|---|---|---|
| `python -m docstoolkit serve` | секунды | ★ | local dev |
| `docker compose up` | минуты | ★★ | single-host, staging |
| Helm chart на k8s | десятки минут | ★★★ | production cluster |

---

## 1. Docker compose

```bash
cd docs-toolkit/deploy
docker compose up -d
# http://localhost:8083  → dashboard
# http://localhost:8083/api/health
# http://localhost:8083/api/ask?q=...&trace=1
```

### С BGE reranker

```bash
docker compose --profile bge up -d
# Дополнительный сервис на :8084 с бакетным BGE
```

### С Prometheus

```bash
docker compose --profile monitor up -d
# Prometheus на :9090, scrape /metrics с serve
```

---

## 2. Helm

```bash
helm install docs-toolkit ./helm/docs-toolkit \
    --set image.tag=0.3.0 \
    --set persistence.size=5Gi

# или с overrides:
helm install docs-toolkit ./helm/docs-toolkit -f my-values.yaml
```

### Что включено в chart

- `Deployment` — образ + healthcheck + non-root SecurityContext
- `Service` — ClusterIP, port 8083
- `PVC` — для `/work` (docs corpus + SQLite caches)
- Prometheus scrape-аннотации (если `metrics.enabled=true`)
- Liveness + readiness probes на `/api/health`

### Опции values.yaml

Смотрите [`helm/docs-toolkit/values.yaml`](helm/docs-toolkit/values.yaml).
Основные:
- `image.tag` — версия образа (`0.3.0` / `bge` / latest)
- `replicaCount` — горизонтальное масштабирование (помните: SQLite
  не шардится — для multi-replica deploy подключайте Postgres-backend
  для shared state, пока что non-goal)
- `persistence.size` — размер тома; зависит от размера корпуса
- `resources.limits.memory` — поднимите до 4Gi для крупных корпусов
- `env.ANTHROPIC_API_KEY` — лучше через `--set-string` + k8s Secret

---

## 3. Образы

| Тег | Размер | Что внутри |
|---|---|---|
| `latest`, `0.3.0` | ~150 MB | core toolkit, все extras |
| `bge`, `0.3.0-bge` | ~1.6 GB | + BGE cross-encoder pre-downloaded |

Build:

```bash
docker build -t docs-toolkit:0.3.0 -f Dockerfile ..
docker build -t docs-toolkit:0.3.0-bge -f Dockerfile.bge ..
```

CI публикация в GHCR — добавится в Phase VIII.1.

---

## 4. Что нужно для production

- [ ] Secrets management (LLM API keys через Vault / SealedSecrets / SOPS)
- [ ] Backup стратегия для `/work/.docstoolkit/` (SQLite snapshot или WAL replication)
- [ ] Rate limiting (есть в `docstoolkit.rate_limiter`, но требует настройки на edge)
- [ ] TLS termination (Ingress + cert-manager)
- [ ] Log aggregation (`/metrics` + traces в `result.trace`)
- [ ] Alerting (Prometheus AlertManager на ошибки `/api/ask`)

---

## 5. OpenAI-compatible gateway

Текущий `/api/ask` — proprietary JSON. Phase VIII.3 добавит
`/v1/chat/completions` для совместимости с OpenAI SDK; это позволит
переключить любой OpenAI-клиент на docs-toolkit без правок кода.

См. backlog в [`DEVELOPMENT_STATUS.md`](../DEVELOPMENT_STATUS.md) §VIII.3.
