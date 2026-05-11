# Сломанные внутренние ссылки

<!-- summary -->
> Сломанных ссылок: **0**, пропущено: 0

<!-- tags: quality, links, validation, broken-links -->

<!-- toc-auto -->
## Содержание

- [Сломанные ссылки](#сломанные-внутренние-ссылки)
- [Общие показатели](#общие-показатели)
- [Внешние URL](#внешние-url)
- [Использование](#использование)
- [Смотрите также](#смотрите-также)

> [!TIP]
> Все внутренние ссылки рабочие!

<!-- alert-added -->

**Найдено:** 0 проблем, 0 пропущено (длинный путь)


Скрипт `improve_broken_links.py` проверяет все внутренние ссылки в папке `docs/`, исключая автоматически генерируемые разделы: `obsidian/`, `confluence/`, `templates/` и `autofilled/`. Проверяются ссылки на файлы (существование пути) и якоря (существование заголовка). Ссылки с путём длиннее 240 символов пропускаются из-за ограничений операционной системы и сохраняются в `bad_links.json`.

Якоря проверяются по алгоритму GitHub-style: заголовки переводятся в нижний регистр, удаляются специальные символы, пробелы заменяются дефисами. Дублирующиеся заголовки получают суффиксы `-1`, `-2` аналогично GitHub.


Автоматическое исправление (`--fix`) ищет файл с таким же именем в `docs/` и заменяет ссылку правильным относительным путём. Режим `--dry-run` показывает запланированные исправления без записи в файлы. Флаг `--section РАЗДЕЛ` ограничивает проверку конкретной подпапкой. Результаты записываются в `docs/BROKEN_LINKS.md` и опционально в `docs/bad_links.json`.


## Общие показатели

- Проверено файлов: большинство `.md` в `docs/`
- Сломанных ссылок: **0**
- Пропущено (длинный путь): **0**
- Внешние URL не проверяются (список формируется без запросов)

✅ Все внутренние ссылки рабочие!


## Внешние URL (349 уникальных)

_Внешние ссылки не проверяются автоматически — требуют ручной проверки._

- http://localhost:8000
- http://localhost:8000`
- http://localhost:8000``
- http://localhost:8000```
- http://localhost:8000````
- http://localhost:8000`````
- http://localhost:8080
- http://localhost:8080`
- http://localhost:8080``
- http://localhost:8080```
- http://localhost:8080````
- http://localhost:8080`````
- https://...install.sh
- https://...install.sh`
- https://3dnews.ru/1140248/glava-[anthropic
- https://3dnews.ru/1140248/glava-[anthropic`
- https://3dnews.ru/1140248/glava-anthropic-predryok-ischeznovenie-inzhe`
- https://3dnews.ru/1140248/glava-anthropic-predryok-ischeznovenie-inzhenernykh-pr`
- https://3dnews.ru/1140248/glava-anthropic-predryok-ischeznovenie-inzhenernykh-professiy-i-otkryl-429-vakansiy-s-zarplatoy-do-405000
- https://3dnews.ru/1140248/glava-anthropic-predryok-ischeznovenie-inzhenernykh-professiy-i-otkryl-429-vakans…
- https://activitypub.rocks/
- https://activitypub.rocks/`
- https://api.github.com/users/svend4/repos?per_page=100&sort=updated
- https://api.github.com/users/svend4/repos?per_page=100&sort=updated&type=owner
- https://api.github.com/users/svend4/repos?per_page=100&sort=updated&type=owner`
- https://api.github.com/users/svend4/repos?per_page=100&sort=updated`
- https://claude.ai/code/session_0179jSZDgmKgh9eLH72HRLuv
- https://claude.ai/code/session_0179jSZDgmKgh9eLH72HRLuv`
- https://claude.ai/code/session_01Dz4rhQWcqu2afRsJ5LqHpz
- https://claude.ai/code/session_01Dz4rhQWcqu2afRsJ5LqHpz`

## Использование

```bash
python scripts/improve_broken_links.py
```

```bash
# Автоматическое исправление битых ссылок
python scripts/improve_broken_links.py --fix
```


## Смотрите также

- [HEALTH](HEALTH.md) — общее здоровье репозитория
- [METRICS](METRICS.md) — метрики качества документов
- [VALIDATION](VALIDATION.md) — валидация структуры
