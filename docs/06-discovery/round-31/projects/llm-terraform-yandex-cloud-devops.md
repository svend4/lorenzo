---
date: 2026-06-05
tags: [memory, orchestration, security, ingestion, architecture]
state: normalized
---

# Автоматизация деплоя контейнеров в Yandex Cloud с помощью Terraform и LLM

<!-- toc-auto -->
<!-- tags: llm-terraform-yandex-cloud-devops, docs -->


<!-- summary -->
> Реальный production-паттерн event-driven автодеплоя: docker push → триггер → Go-функция → Yandex Cloud API → новая ревизия контейнера без ручных шагов.


> [!TIP]
> Этот документ описывает MVP-подход. Начните с него для быстрого прототипа.

<!-- alert-added -->

**Автор:** sshaplygin (Хабр, апрель 2026)  
**Хабр:** https://habr.com/ru/articles/1020612/  
**GitHub:** github.com/sshaplygin (Terraform + Go Cloud Function, ссылка в статье)  
**Слой:** orchestration / ingestion  
**Дата:** апрель 2026  
**Уникальность:** Практическая демонстрация AI-первого IaC: Claude Code генерирует полную Terraform-конфигурацию для Yandex Cloud (Cloud Function на Go + Container Registry Trigger + IAM). Реальный production-паттерн event-driven автодеплоя: docker push → триггер → Go-функция → Yandex Cloud API → новая ревизия контейнера без ручных шагов.

## Проблема: ручной деплой в современном CI/CD

```
Без автоматизации (типичный сценарий):
  1. Разработчик собирает Docker образ
  2. Пушит в Container Registry
  3. Вручную заходит в консоль Yandex Cloud
  4. Обновляет Serverless Container → выбирает новый образ
  5. Ждёт деплоя → проверяет здоровье
  → Рутина, ошибки, задержки

С LLM-generated IaC:
  docker push → автоматически:
    Container Registry Trigger → Cloud Function (Go)
    → Yandex Cloud API → новая ревизия контейнера
  → Нет ручных шагов, воспроизводимо, версионировано в Git
```

## Архитектура: три компонента Terraform

```hcl
# Сгенерировано Claude Code на основе описания на естественном языке:
# "Хочу: при пуше нового Docker образа в Container Registry
#  автоматически обновлялась Serverless Container ревизия"

# 1. Cloud Function (Go runtime) — обработчик триггера
resource "yandex_function" "container_redeployer" {
  name        = "container-redeployer"
  runtime     = "golang121"
  entrypoint  = "main.Handler"
  memory      = 128
  user_hash   = data.archive_file.handler.output_base64sha256

  environment = {
    CONTAINER_ID = var.serverless_container_id
    FOLDER_ID    = var.folder_id
  }

  service_account_id = yandex_iam_service_account.redeployer_sa.id
}

# 2. Container Registry Trigger — слушает события пуша
resource "yandex_function_trigger" "registry_push" {
  name = "registry-push-trigger"

  container_registry {
    registry_id = var.registry_id
    image_name  = var.image_name
    tag         = "latest"
    batch_size  = 1

    # Реагировать только на CREATE_IMAGE_TAG (новый пуш)
    event_types = ["CREATE_IMAGE_TAG"]
  }

  function {
    id                 = yandex_function.container_redeployer.id
    service_account_id = yandex_iam_service_account.invoker_sa.id
  }
}

# 3. IAM: сервисные аккаунты с минимальными правами
resource "yandex_iam_service_account" "redeployer_sa" {
  name = "container-redeployer-sa"
}

resource "yandex_resourcemanager_folder_iam_member" "redeployer_serverless" {
  folder_id = var.folder_id
  role      = "serverless.containers.editor"
  member    = "serviceAccount:${yandex_iam_service_account.redeployer_sa.id}"
}
```

## Go Cloud Function: обработчик события реестра

```go
// main.go — сгенерировано Claude Code, доработано автором
package main

import (
    "context"
    "encoding/json"
    "fmt"
    "os"

    ycsdk "github.com/yandex-cloud/go-sdk"
    "github.com/yandex-cloud/go-sdk/gen/serverless/containers"
)

// RegistryEvent — структура события от Container Registry
type RegistryEvent struct {
    Messages []struct {
        Details struct {
            ImageID   string `json:"imageId"`
            ImageURL  string `json:"imageUrl"`
            Tag       string `json:"tag"`
        } `json:"details"`
    } `json:"messages"`
}

func Handler(ctx context.Context, event []byte) (string, error) {
    var e RegistryEvent
    if err := json.Unmarshal(event, &e); err != nil {
        return "", fmt.Errorf("unmarshal: %w", err)
    }

    if len(e.Messages) == 0 {
        return "no messages", nil
    }

    newImageURL := e.Messages[0].Details.ImageURL
    containerID := os.Getenv("CONTAINER_ID")
    folderID    := os.Getenv("FOLDER_ID")

    // Инициализация SDK с IAM-токеном из метаданных функции
    sdk, err := ycsdk.Build(ctx, ycsdk.Config{
        Credentials: ycsdk.InstanceServiceAccount(),
    })
    if err != nil {
        return "", fmt.Errorf("sdk init: %w", err)
    }

    // Создать новую ревизию контейнера с обновлённым образом
    op, err := sdk.Serverless().Containers().Container().DeployRevision(ctx,
        &containers.DeployRevisionRequest{
            ContainerId: containerID,
            Resources: &containers.Resources{
                Memory:       134217728, // 128 MB
                Cores:        1,
                CoreFraction: 100,
            },
            Image: &containers.ImageSpec{
                ImageUrl: newImageURL,
            },
        },
    )
    if err != nil {
        return "", fmt.Errorf("deploy revision: %w", err)
    }

    return fmt.Sprintf("Deployed: operation %s", op.Id), nil
}
```

## Паттерн: диалог с LLM для генерации IaC

```python
# Как выглядел процесс работы с Claude Code (из статьи):

# Шаг 1: Описание задачи на русском языке
NATURAL_LANGUAGE_REQUEST = """
Мне нужна Terraform конфигурация для Yandex Cloud:
- При пуше нового Docker образа в Container Registry
  автоматически обновляется Serverless Container
- Использовать Cloud Function на Go как обработчик
- Минимальные IAM права (principle of least privilege)
- Выходные переменные: function_id, trigger_id, service_account_emails
"""

# Шаг 2: Claude Code генерирует план + код
# → tf/main.tf, tf/variables.tf, tf/outputs.tf
# → handler/main.go

# Шаг 3: Итерация — уточнение проблем
FOLLOWUP = """
terraform plan показывает:
Error: Error creating IAM Binding: 403 Forbidden
    - Нет прав на yandex_resourcemanager_folder_iam_member
Как исправить? Покажи правки только затронутых файлов.
"""

# Рефлексия автора из статьи:
# "Чрезмерная зависимость от ИИ при изучении нового
#  может ослаблять формирование навыков.
#  Claude Code ускоряет прототипирование, но понять
#  что он сгенерировал — ответственность разработчика."
```

## DevOps AI Patterns: что демонстрирует статья

```python
DEVOPS_AI_PATTERNS = {
    "IaC generation": {
        "описание": "LLM генерирует Terraform/Pulumi/CDK из NL-описания",
        "применение": "Новые проекты, стандартные паттерны (функция + триггер + IAM)",
        "ограничения": [
            "Сложные multi-account конфигурации требуют проверки",
            "IAM политики требуют аудита безопасности",
            "Специфика провайдера (Yandex Cloud) хуже GPT-4 чем AWS/GCP"
        ]
    },

    "Conversational debugging": {
        "описание": "Ошибки деплоя → LLM предлагает фикс",
        "применение": "terraform plan/apply errors → targeted patches",
        "ограничения": ["Нужно понять контекст ошибки перед применением"]
    },

    "Event-driven automation": {
        "описание": "Триггер → функция → API → обновление ресурса",
        "применение": "CI/CD без Jenkins/GitHub Actions для простых сценариев",
        "ограничения": ["Cold start функции, лимиты trigers в Yandex Cloud"]
    }
}
```

## Tech Radar (DevOpsConf 2026 context)

```python
# Из статьи DevOpsConf 2026 Tech Radar (1029442):
DEVOPS_TECH_RADAR_2026 = {
    "ADOPT": [
        "GitOps (Argo CD, Flux)",
        "Everything as Code",
        "Platform Engineering",
        "SRE-подходы"
    ],
    "TRIAL": [
        "AI-assistants для IaC-генерации",  # ← тема статьи
        "Model Context Protocol (MCP) для DevOps",
        "AI Engineering практики"
    ],
    "ASSESS": [
        "LLM-driven incident analysis",
        "Predictive autoscaling через ML"
    ],
    "HOLD": [
        "ClickOps в production"
    ]
}
# Вывод: LLM-generated IaC — Trial, не Adopt.
# Годится для прототипов и стандартных паттернов.
# Требует review перед production.
```

## Применение к Lorenzo

```python
# improve_infra_codegen.py (паттерн):

class LorenzoInfraCodegen:
    """
    Если Lorenzo управляет своей инфраструктурой —
    LLM может генерировать конфиги для частых операций.
    """

    SUPPORTED_PATTERNS = {
        "add_mcp_server": {
            "template": "Docker Compose service + volume mount + env",
            "prompt": "Добавь MCP-сервер {name} на порту {port} с volume {volume}"
        },
        "backup_policy": {
            "template": "cron + rclone/restic backup script",
            "prompt": "Создай backup политику для {path} в {destination} каждые {interval}"
        },
        "monitoring": {
            "template": "Prometheus scrape config + Grafana dashboard JSON",
            "prompt": "Добавь мониторинг для {service} с алертом при {condition}"
        }
    }

    def generate(self, pattern: str, params: dict) -> GeneratedConfig:
        template_config = self.SUPPORTED_PATTERNS[pattern]
        return self.llm.generate(
            prompt=template_config["prompt"].format(**params),
            template=template_config["template"],
            review_required=True  # Human review before apply
        )
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Terraform+LLM + HITL (R30)** | LLM генерирует конфиг → HITL checkpoint перед `terraform apply` |
| **Terraform+LLM + Meta-Monitor (R29)** | AI мониторит дрейф инфраструктуры → автогенерация fix-коммита |
| **Terraform+LLM + AIOps Sber (R24)** | AIOps видит аномалию → LLM генерирует remediation Terraform |
| **Terraform+LLM + Orchestrator (R27)** | 5-фазный оркестратор: plan-review-approve-apply-verify |
| **Terraform+LLM + Coreness Flow (R30)** | Composable IaC: каждый модуль = plugin с config.json + .tf файлами |

## Контакт

- Статья: https://habr.com/ru/articles/1020612/ (апрель 2026)
- Хабр-аккаунт: habr.com/ru/users/sshaplygin/
- Смежная (Tech Radar DevOpsConf 2026): https://habr.com/ru/companies/oleg-bunin/articles/1029442/
- Смежная (DevOps в 2026, Platform Engineering): https://habr.com/ru/companies/habr_career/articles/979270/
- Yandex Cloud Go SDK: github.com/yandex-cloud/go-sdk
- Terraform Yandex Provider: registry.terraform.io/providers/yandex-cloud/yandex

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
- [Решения](../../../DECISIONS.md)
