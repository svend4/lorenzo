# 12. Onboarding Paths (Normative)

<!-- toc -->
## Содержание

- [Contents](#contents)
- [12. Onboarding Paths (Normative)](#12-onboarding-paths-normative)
  - [12.1. Path A — Manual Adapter](#121-path-a-manual-adapter)
  - [12.2. Path B — generate_passport.py Wizard](#122-path-b-generate_passportpy-wizard)
  - [12.3. Path C — Self-Declaring Repo (AutoAdapter)](#123-path-c-self-declaring-repo-autoadapter)
  - [12.4. Path D — Auto-Scanner](#124-path-d-auto-scanner)
  - [12.5. Path E — GitHub Actions Webhook](#125-path-e-github-actions-webhook)
  - [12.6. Path Selection Guidance](#126-path-selection-guidance)

---


<!-- abstract-auto -->
> **Абстракт** (авто)
>
> 🎯 **Проблема:** Portal автоматически использует AutoAdapter Ключевое свойство: repo регистрирует себя сам, portal не требует изменений кода.
> ✅ **Результат:** Результат: - passports/<format.md — авто-заполнен по структуре - adapters/<format.py — статика из найденных файлов - autoreport.json — детальный отчёт Сканер — отправная точка, рез
> 🏷️ **Ключевые слова:** `github`, `portal`, `nautilus`, `repos`, `adapter`, `время`, `автоматизация`, `качество`
>


<!-- toc-auto -->
## Contents

- [12. Onboarding Paths (Normative)](#12-onboarding-paths-normative)
  - [12.1. Path A — Manual Adapter](#121-path-a-manual-adapter)
  - [12.2. Path B — generatepassport.py Wizard](#122-path-b-generatepassportpy-wizard)
  - [12.3. Path C — Self-Declaring Repo (AutoAdapter)](#123-path-c-self-declaring-repo-autoadapter)
  - [12.4. Path D — Auto-Scanner](#124-path-d-auto-scanner)
  - [12.5. Path E — [GitHub](../docs/01-svyazi/03-component-catalog.md) Actions Webhook](#125-path-e-github-actions-webhook)
  - [12.6. Path Selection Guidance](#126-path-selection-guidance)


<!-- summary -->
> NPP v1.1 формализует пять путей подключения нового Repo как

---
<!-- tags: architecture, collaboration -->




## 12. Onboarding Paths (Normative)

NPP v1.1 формализует пять путей подключения нового Repo как 
equivalent-рангованные стратегии. Каждая имеет свой trade-off между 
автоматизацией и качеством.

### 12.1. Path A — Manual Adapter

**Время**: 10–20 минут. **Автоматизация**: 0%. **Качество**: высокое.

1. Написать `adapters/<format>.py`, наследуясь от `[BaseAdapter](../docs/02-anthropic-vacancies/01-интегральный-анализ-профиля-svend4.md)`
2. Написать `passports/<format>.md`
3. Зарегистрировать адаптер в `adapters/__init__.py`
4. Добавить импорт в `portal.py` в конструктор
5. Добавить запись в `[nautilus](../docs/05-habr-projects/memory/memnet.md).json`

### 12.2. Path B — generate_passport.py Wizard

**Время**: 2–5 минут. **Автоматизация**: ~50%. **Качество**: 
требует доработки.

```bash
python generate_passport.py --repo owner/repo --format myformat --adapter
```

Генерирует заготовки passport и adapter. Дальше вручную:

- Заполнить `_static_entries()` реальными концептами
- Дописать Q6-отображение в паспорте
- Добавить мосты к другим Repos

### 12.3. Path C — Self-Declaring Repo (AutoAdapter)

**Время**: 10 минут. **Автоматизация**: ~80%. **Качество**: 
зависит от index в [nautilus](../docs/05-habr-projects/memory/memnet.md).json target-репо.

1. В целевом репо создать `[nautilus](../docs/05-habr-projects/memory/memnet.md).json` в корне с полем `index`
2. В portal-репо добавить запись `{"adapter": "auto", "repo": "..."}`
3. Portal автоматически использует [AutoAdapter](../docs/02-anthropic-vacancies/141-4-nautilus-portal-as-reference-substrate.md)

**Ключевое свойство**: repo регистрирует себя сам, portal не 
требует изменений кода. Это enables federation без координации.

### 12.4. Path D — Auto-Scanner

**Время**: 2 минуты. **Автоматизация**: ~95%. **Качество**: низкое 
(только структура).

```bash
python scan_repo.py owner/repo-name
```

Результат:
- `passports/<format>.md` — авто-заполнен по структуре
- `adapters/<format>.py` — статика из найденных файлов  
- `auto_report.json` — детальный отчёт

Сканер — **отправная точка**, результат всё равно нужно проверить 
и уточнить Q6-маппинг вручную.

### 12.5. Path E — GitHub Actions Webhook

**Время**: 30 минут настройки, далее полностью автоматически. 
**Автоматизация**: 100%. **Качество**: низкое без Q6-маппинга.

1. В целевом репо создать `.github/workflows/register_nautilus.yml`
2. При push в target-репо — `repository_dispatch` event в portal-репо
3. В portal-репо `.github/workflows/auto_update.yml` запускает 
   `scan_repo.py` + `generate_passport.py` + commit

**Плюсы**: полностью автоматически.  
**Минусы**: нужны [GitHub](../docs/01-svyazi/03-component-catalog.md) токены с правами на оба репо, Q6 всё равно 
требует ручной проверки.

### 12.6. Path Selection Guidance

| Вариант | Когда использовать |
|---------|-------------------|
| **A** | Когда хорошо знаете структуру Repo и хотите high-quality |
| **B** | Стартовая точка для большинства новых Repos |
| **C** | Для Repos, которые автор хочет сам декларировать |
| **D** | Для быстрой первой интеграции незнакомых Repos |
| **E** | Для автоматической fleet-federation многих Repos |

**Рекомендуемый путь для типового Repo**: B → доработать вручную. 
Для federation новых Repos в будущем — C.

---

<!-- see-also -->

---

**Смотрите также:**
- [07-2-terminology](docs/02-anthropic-vacancies/07-2-terminology.md)
- [78-3-registry-[nautilus](../docs/05-habr-projects/memory/memnet.md)-json](docs/02-anthropic-vacancies/78-3-registry-nautilus-json.md)
- [77-2-terminology](docs/02-anthropic-vacancies/77-2-terminology.md)


<!-- similar-docs -->

---

**Похожие документы:**
- [07-2-terminology](docs/02-anthropic-vacancies/07-2-terminology.md) (сходство 0.16)
- [80-5-compatibility-levels](docs/02-anthropic-vacancies/80-5-compatibility-levels.md) (сходство 0.16)
- [77-2-terminology](docs/02-anthropic-vacancies/77-2-terminology.md) (сходство 0.15)

