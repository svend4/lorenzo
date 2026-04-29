# 12. Onboarding Paths (Normative)

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

1. Написать `adapters/<format>.py`, наследуясь от `BaseAdapter`
2. Написать `passports/<format>.md`
3. Зарегистрировать адаптер в `adapters/__init__.py`
4. Добавить импорт в `portal.py` в конструктор
5. Добавить запись в `nautilus.json`

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
зависит от index в nautilus.json target-репо.

1. В целевом репо создать `nautilus.json` в корне с полем `index`
2. В portal-репо добавить запись `{"adapter": "auto", "repo": "..."}`
3. Portal автоматически использует AutoAdapter

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
**Минусы**: нужны GitHub токены с правами на оба репо, Q6 всё равно 
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
