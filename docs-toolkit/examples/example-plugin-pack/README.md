# Example Plugin Pack

Пример того, как написать пакет-расширение для `docs-toolkit`. Демонстрирует
все 4 типа точек расширения: ingest, embeddings, skills, templates.

## Что внутри

```
example-plugin-pack/
├── pyproject.toml                  # entry_points регистрация
├── README.md
└── docstoolkit_example/
    ├── __init__.py
    ├── ingest_csv.py               # пример ingest-плагина (.csv → markdown)
    ├── embeddings_random.py        # пример embedding-провайдера (демо)
    ├── skills/
    │   └── translate.md            # пример скила
    └── templates/
        └── api-spec.md             # пример шаблона
```

## Как это работает

`pyproject.toml` объявляет `[project.entry-points.<group>]`. После `pip install`
этого пакета `docstoolkit autoload_all()` подключает все плагины.

### Группы entry_points

| Группа | Что регистрирует |
|---|---|
| `docstoolkit.ingest` | callable `ingest(path: Path) → Document` |
| `docstoolkit.embeddings` | класс `EmbeddingProvider` |
| `docstoolkit.skills` | путь к `.md` скила (директория) |
| `docstoolkit.templates` | путь к `.md` шаблона + `.json` схеме |

## Установка для разработки

```bash
cd docs-toolkit/examples/example-plugin-pack
pip install -e .

# Проверить что плагины подключились
docstoolkit plugins list
```

## Создание собственного пакета

1. Скопируйте структуру.
2. Замените `docstoolkit_example` на имя своего пакета.
3. Обновите `pyproject.toml` → `[project]` и `[project.entry-points...]`.
4. Реализуйте плагины как функции/классы.
5. `pip install -e .`
6. `docstoolkit plugins list` должен показать ваши.
