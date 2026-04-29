# Release process для docs-toolkit

## Версионирование

Используется [Semantic Versioning 2.0.0](https://semver.org/):

- **MAJOR** (X.0.0) — breaking changes в публичном API (Config, CLI args, plugin contracts)
- **MINOR** (0.X.0) — новые features без breaking
- **PATCH** (0.0.X) — bugfix, документация

## Pre-release checklist

```bash
# 1. Все тесты проходят
cd docs-toolkit
python -m pytest tests/ -v

# 2. CHANGELOG обновлён (Unreleased → версия + дата)
# 3. Версия в pyproject.toml поднята
# 4. Commit changelog/version bumps
git add CHANGELOG.md pyproject.toml
git commit -m "release: docs-toolkit v0.X.Y"

# 5. Локальная сборка проверена
python -m build
twine check dist/*

# 6. Установить локально и smoke-test
pip install --force-reinstall dist/docs_toolkit-*.whl
docstoolkit doctor
docstoolkit doc list-templates
```

## Release tagging

```bash
# Тег формата toolkit-v<major>.<minor>.<patch>
git tag -a toolkit-v0.X.Y -m "release: docs-toolkit v0.X.Y"
git push origin toolkit-v0.X.Y
```

## CI/CD

При push tag `toolkit-v*`:
- `.github/workflows/publish-toolkit.yml` запускается автоматически
- Jobs:
  1. `build` — wheel + sdist + twine check
  2. `test-install` — matrix py3.10/3.11/3.12
  3. `publish-testpypi` — sandbox для проверки
  4. `publish-pypi` — production (требует PYPI_API_TOKEN secret)
  5. `build-docker` — `ghcr.io/<owner>/docs-toolkit:<version>`

Для manual запуска: GitHub Actions → "Publish docs-toolkit" → workflow_dispatch
с выбором target (testpypi | pypi | both).

## Hotfix process

```bash
# Создать hotfix branch от tag
git checkout -b hotfix/0.X.Y+1 toolkit-v0.X.Y

# Зафиксить, обновить CHANGELOG в Unreleased→0.X.Y+1
# Затем PR → main + tag toolkit-v0.X.Y+1
```

## Откат версии

PyPI **не позволяет переиспользовать version number** даже после yank.
Если плохой релиз — `pip install docs-toolkit==<previous>` + бамп до X.Y.Z+1.

```bash
# На PyPI:
twine upload --skip-existing dist/*

# Yank (помечает версию как "не для новых установок")
# Делается через PyPI web UI или: pip install yank-package
```

## После релиза

- [ ] Обновить badge в `docs-toolkit/README.md` с новой версией
- [ ] Анонс в issue / discussions
- [ ] Обновить `docs/REGISTRY.md` с новой версией
- [ ] Создать GitHub Release с автогенерируемыми release notes
