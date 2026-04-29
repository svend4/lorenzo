"""CLI точка входа: docstoolkit ..."""
import argparse
import json
import sys
from datetime import date
from pathlib import Path

from docstoolkit.config import load_config
from docstoolkit.frontmatter import extract_frontmatter


def cmd_init(args):
    """Создать docstoolkit.toml в текущей папке."""
    config_path = Path("docstoolkit.toml")
    if config_path.exists() and not args.force:
        print(f"❌ {config_path} уже существует. --force для перезаписи.")
        return 1
    config_path.write_text(EXAMPLE_CONFIG, encoding="utf-8")
    print(f"✅ Создан {config_path}")
    return 0


def cmd_doc_new(args):
    """Создать документ из шаблона."""
    cfg = load_config()
    template_path = cfg.templates_dir / f"{args.type}.md"
    if not template_path.exists():
        print(f"❌ Шаблон '{args.type}' не найден в {cfg.templates_dir}")
        return 1

    content = template_path.read_text(encoding="utf-8")

    # Применить переменные
    vars_dict: dict[str, str] = {}
    for kv in args.vars or []:
        if "=" in kv:
            k, v = kv.split("=", 1)
            vars_dict[k.strip()] = v.strip()

    # Заменить frontmatter поля
    import re
    today = date.today().isoformat()
    fm_match = re.match(r'\A---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if fm_match:
        fm_text = fm_match.group(1)
        for k, v in vars_dict.items():
            yaml_v = f'"{v}"' if not v.lstrip("-").isdigit() else v
            fm_text = re.sub(
                rf'^({re.escape(k)})\s*:\s*.+$',
                lambda m, val=yaml_v: f"{m.group(1)}: {val}",
                fm_text, count=1, flags=re.MULTILINE
            )
        fm_text = re.sub(r'^created:\s*[\d-]+$', f'created: {today}', fm_text, flags=re.MULTILINE)
        fm_text = re.sub(r'^date:\s*[\d-]+$', f'date: {today}', fm_text, flags=re.MULTILINE)
        content = content[:fm_match.start(1)] + fm_text + content[fm_match.end(1):]

    # Body placeholders
    for k, v in vars_dict.items():
        content = content.replace(f"[{k}]", v)

    out_path = Path(args.slug)
    if not out_path.suffix:
        out_path = out_path.with_suffix(".md")
    if out_path.exists() and not args.force:
        print(f"❌ {out_path} существует. --force для перезаписи.")
        return 1

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(content, encoding="utf-8")
    print(f"✅ Создан {out_path}")
    return 0


def cmd_doc_validate(args):
    """Валидация документов по JSON-схемам."""
    cfg = load_config()
    schemas_dir = cfg.schemas_dir
    if not schemas_dir.exists():
        print(f"❌ Нет схем в {schemas_dir}")
        return 1

    schemas: dict[str, dict] = {}
    for sp in schemas_dir.glob("*.json"):
        try:
            schemas[sp.stem] = json.loads(sp.read_text(encoding="utf-8"))
        except Exception:
            continue

    base = Path(args.section) if args.section else cfg.docs_dir
    if not base.is_absolute():
        base = cfg.root / base

    files = sorted(base.rglob("*.md"))
    skip_dirs = set(cfg.validation.get("skip_dirs", []))

    # i18n: выбираем локаль по cfg или auto
    from docstoolkit.lang import t, set_locale
    set_locale(cfg.language.get("primary", "en"))

    valid = 0
    errors_count = 0
    for f in files:
        if any(d in f.parts for d in skip_dirs):
            continue
        text = f.read_text(encoding="utf-8")
        fm, _ = extract_frontmatter(text)
        if not fm or "template" not in fm:
            continue
        template = fm["template"]
        if template not in schemas:
            print(f"⚠️  {f.relative_to(cfg.root)}: schema {template!r} not found")
            continue
        schema = schemas[template]
        errs: list[str] = []
        for req in schema.get("required", []):
            if req not in fm:
                errs.append(t("validation.missing_field", field=req))
        if errs:
            errors_count += 1
            print(f"❌ {f.relative_to(cfg.root)}")
            for e in errs:
                print(f"   — {e}")
        else:
            valid += 1

    n_total = valid + errors_count
    if cfg.language.get("primary") == "ru":
        print(f"\nВалидно: {valid}, с ошибками: {errors_count}")
    else:
        print(f"\nValid: {valid}, with errors: {errors_count}")
    return 1 if errors_count and cfg.validation.get("strict") else 0


def cmd_ingest(args):
    """Ингестия файла (PDF/EPUB/HTML/MHTML/DOCX/Jupyter/MD) → markdown."""
    from docstoolkit.ingest import ingest_file, ingest_dir, list_plugins

    src = Path(args.path)
    if not src.exists():
        print(f"❌ Не существует: {src}")
        return 1

    if args.list_plugins:
        plugins = sorted(list_plugins())
        print(f"Доступных плагинов: {len(plugins)}")
        for p in plugins:
            print(f"  .{p}")
        return 0

    docs = []
    if src.is_dir():
        docs = ingest_dir(src, recursive=args.recursive)
    else:
        try:
            docs = [ingest_file(src)]
        except Exception as e:
            print(f"❌ {e}")
            return 1

    if not docs:
        print("⚠️ Ничего не извлечено.")
        return 1

    out_dir = Path(args.output) if args.output else None

    for doc in docs:
        # Frontmatter
        fm = {
            "ingested_from": str(doc.source.path),
            "format": doc.source.format,
            "title": doc.title,
        }
        if doc.metadata:
            for k, v in doc.metadata.items():
                if isinstance(v, (str, int, float, bool)) and v not in (None, ""):
                    fm[k] = v
        md = doc.to_markdown(frontmatter=fm)

        if out_dir:
            out_dir.mkdir(parents=True, exist_ok=True)
            slug = doc.source.path.stem
            target = out_dir / f"{slug}.md"
            target.write_text(md, encoding="utf-8")
            print(f"✅ {doc.source.path.name} → {target} ({doc.word_count} слов)")
        else:
            print(f"\n{'=' * 60}")
            print(f"# {doc.title} ({doc.word_count} слов)")
            print(f"From: {doc.source.path}")
            print(f"{'=' * 60}\n")
            print(md[:2000])
            if len(md) > 2000:
                print(f"\n... (обрезано, всего {len(md)} символов)")

    return 0


def cmd_doc_list_templates(args):
    """Список доступных шаблонов."""
    cfg = load_config()
    if not cfg.templates_dir.exists():
        print(f"Templates dir не найден: {cfg.templates_dir}")
        return 1
    items = []
    for p in sorted(cfg.templates_dir.glob("*.md")):
        if p.name == "README.md":
            continue
        schema = cfg.schemas_dir / f"{p.stem}.json"
        desc = ""
        if schema.exists():
            try:
                desc = json.loads(schema.read_text(encoding="utf-8")).get("description", "")
            except Exception:
                pass
        items.append((p.stem, desc))
    print(f"Доступных шаблонов: {len(items)}")
    for name, desc in items:
        print(f"  {name:25s} {desc[:60]}")
    return 0


EXAMPLE_CONFIG = """# docstoolkit configuration

[paths]
docs = "docs"
templates = "docs/templates"
schemas = "docs/templates/_schemas"
tasks = "tasks"
skills = ".claude/skills"

[validation]
strict = false
skip_dirs = ["templates", "_schemas", "node_modules", ".git"]

[language]
primary = "en"

[sections]
# Секции монорепо: имя папки → читаемое название
# "01-svyazi" = "Svyazi 2.0"
"""


def main():
    parser = argparse.ArgumentParser(prog="docstoolkit",
                                     description="Universal markdown documentation toolkit")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_init = sub.add_parser("init", help="Создать docstoolkit.toml")
    p_init.add_argument("--force", action="store_true")
    p_init.set_defaults(func=cmd_init)

    p_doc = sub.add_parser("doc", help="Документы")
    p_doc_sub = p_doc.add_subparsers(dest="doc_cmd", required=True)

    p_new = p_doc_sub.add_parser("new", help="Создать из шаблона")
    p_new.add_argument("--type", required=True)
    p_new.add_argument("--slug", required=True)
    p_new.add_argument("--vars", nargs="*", default=[])
    p_new.add_argument("--force", action="store_true")
    p_new.set_defaults(func=cmd_doc_new)

    p_val = p_doc_sub.add_parser("validate", help="Валидация документов")
    p_val.add_argument("--section", default="")
    p_val.set_defaults(func=cmd_doc_validate)

    p_list = p_doc_sub.add_parser("list-templates", help="Список шаблонов")
    p_list.set_defaults(func=cmd_doc_list_templates)

    p_ing = sub.add_parser("ingest", help="Ингестия PDF/EPUB/HTML/DOCX/Jupyter → markdown")
    p_ing.add_argument("path", help="Файл или директория")
    p_ing.add_argument("-o", "--output", help="Куда писать markdown (по умолчанию stdout)")
    p_ing.add_argument("-r", "--recursive", action="store_true", help="Рекурсивно для директории")
    p_ing.add_argument("--list-plugins", action="store_true", help="Список доступных плагинов")
    p_ing.set_defaults(func=cmd_ingest)

    p_serve = sub.add_parser("serve", help="Запустить веб-дашборд (HTTP)")
    p_serve.add_argument("--port", type=int, default=8000)
    p_serve.add_argument("--bind", default="127.0.0.1")
    p_serve.set_defaults(func=cmd_serve)

    p_doc_doctor = sub.add_parser("doctor", help="Диагностика установки и конфига")
    p_doc_doctor.add_argument("--json", action="store_true", help="JSON вывод")
    p_doc_doctor.set_defaults(func=cmd_doctor)

    p_search = sub.add_parser("search", help="Поиск по корпусу (keyword/semantic/hybrid)")
    p_search.add_argument("query", help="Поисковый запрос")
    p_search.add_argument("-k", "--top", type=int, default=10, help="Top-K")
    p_search.add_argument("--method", choices=["keyword", "semantic", "hybrid"],
                          default="keyword")
    p_search.add_argument("--model", default="paraphrase-multilingual-MiniLM-L12-v2")
    p_search.add_argument("--json", action="store_true", help="JSON вывод")
    p_search.set_defaults(func=cmd_search)

    p_plugins = sub.add_parser("plugins", help="Управление плагинами")
    p_plugins_sub = p_plugins.add_subparsers(dest="plugins_cmd", required=True)

    p_plugins_list = p_plugins_sub.add_parser("list", help="Список плагинов")
    p_plugins_list.set_defaults(func=cmd_plugins_list)

    p_plugins_inspect = p_plugins_sub.add_parser("inspect", help="Инфо о плагине")
    p_plugins_inspect.add_argument("group")
    p_plugins_inspect.add_argument("name")
    p_plugins_inspect.set_defaults(func=cmd_plugins_inspect)

    p_index = sub.add_parser("index", help="Управление persistent embeddings cache")
    p_index_sub = p_index.add_subparsers(dest="index_cmd", required=True)

    p_idx_build = p_index_sub.add_parser("build", help="Построить кэш с нуля")
    p_idx_build.add_argument("--provider", default="tfidf",
                              choices=["tfidf", "sentence-transformers"])
    p_idx_build.add_argument("--model", default="paraphrase-multilingual-MiniLM-L12-v2")
    p_idx_build.set_defaults(func=cmd_index_build)

    p_idx_update = p_index_sub.add_parser("update", help="Обновить только изменённые файлы")
    p_idx_update.add_argument("--provider", default="tfidf",
                               choices=["tfidf", "sentence-transformers"])
    p_idx_update.set_defaults(func=cmd_index_update)

    p_idx_clear = p_index_sub.add_parser("clear", help="Очистить кэш")
    p_idx_clear.add_argument("--provider", default=None, help="Если не указан — все")
    p_idx_clear.set_defaults(func=cmd_index_clear)

    p_idx_stats = p_index_sub.add_parser("stats", help="Статистика кэша")
    p_idx_stats.set_defaults(func=cmd_index_stats)

    p_skills = sub.add_parser("skills", help="Управление скилами")
    p_skills_sub = p_skills.add_subparsers(dest="skills_cmd", required=True)

    p_skl_list = p_skills_sub.add_parser("list", help="Список доступных скилов")
    p_skl_list.set_defaults(func=cmd_skills_list)

    p_skl_test = p_skills_sub.add_parser("test", help="Запустить golden tests для скилов")
    p_skl_test.add_argument("--skill", default="", help="Фильтр по имени")
    p_skl_test.add_argument("--golden-dir", default=".claude/skills/_golden",
                             help="Директория с *.test.yaml")
    p_skl_test.add_argument("--strict", action="store_true",
                             help="Exit 1 если есть failed")
    p_skl_test.set_defaults(func=cmd_skills_test)

    args = parser.parse_args()
    return args.func(args)


def cmd_skills_list(args):
    from docstoolkit.skills import list_skills
    skills = list_skills()
    print(f"Найдено скилов: {len(skills)}")
    for name, path in sorted(skills.items()):
        print(f"  {name:30s} {path}")
    return 0


def cmd_skills_test(args):
    from docstoolkit.skills import run_golden_tests
    from docstoolkit.skills.testing import render_results

    cfg = load_config()
    golden = Path(args.golden_dir)
    if not golden.is_absolute():
        golden = cfg.root / golden

    if not golden.exists():
        print(f"❌ {golden} не существует")
        return 1

    results = run_golden_tests(golden, skill_filter=args.skill)
    print(render_results(results))

    failed = sum(1 for r in results if r.status == "fail")
    if args.strict and failed:
        return 1
    return 0


def _open_cache():
    from docstoolkit.embeddings.cache import EmbeddingCache
    cfg = load_config()
    cache_dir = cfg.root / ".docstoolkit" / "cache"
    return EmbeddingCache(cache_dir / "embeddings.sqlite")


def _load_index_docs():
    cfg = load_config()
    index_path = cfg.docs_dir / "search_index.json"
    if not index_path.exists():
        return None, None
    docs = json.loads(index_path.read_text(encoding="utf-8"))
    if isinstance(docs, dict):
        docs = docs.get("docs", [])
    return cfg, docs


def cmd_index_build(args):
    cfg, docs = _load_index_docs()
    if not docs:
        print("❌ search_index.json не найден")
        return 1
    cache = _open_cache()
    cache.invalidate(args.provider)  # очистить старое

    from docstoolkit.embeddings import get_provider
    if args.provider == "sentence-transformers":
        try:
            prov = get_provider("sentence-transformers", model=args.model)
        except ImportError as e:
            print(f"❌ {e}")
            return 1
        prov_name = "sentence-transformers"
    else:
        from docstoolkit.embeddings.tfidf import TFIDFProvider
        prov = TFIDFProvider(cache=cache)
        prov_name = "tfidf"

    print(f"Building cache: provider={prov_name}, docs={len(docs)}")

    if prov_name == "tfidf":
        prov.fit([d.get("content", "") + " " + d.get("title", "") for d in docs], force=True)
        print(f"  ✓ IDF saved ({len(prov._idf)} tokens)")

    # Vectorize each doc
    import time
    t0 = time.time()
    n_saved = 0
    for d in docs:
        text = d.get("content", "") + " " + d.get("title", "")
        if not text.strip():
            continue
        doc_id = d.get("path", d.get("id", ""))
        if not doc_id:
            continue
        vec = prov.encode([text])[0]
        cache.save_vector(prov_name, doc_id, text, vec,
                          dim=len(vec) if isinstance(vec, list) else 0)
        n_saved += 1
        if n_saved % 100 == 0:
            print(f"  {n_saved} vectorized...")
    duration = time.time() - t0
    print(f"\n✅ Cached {n_saved} vectors in {duration:.1f}s")
    print(f"   ({n_saved/duration:.1f} docs/sec)")
    cache.close()
    return 0


def cmd_index_update(args):
    """Только новые/изменённые файлы."""
    cfg, docs = _load_index_docs()
    if not docs:
        print("❌ search_index.json не найден")
        return 1
    cache = _open_cache()
    from docstoolkit.embeddings.cache import hash_content

    if args.provider == "sentence-transformers":
        from docstoolkit.embeddings import get_provider
        try:
            prov = get_provider("sentence-transformers")
        except ImportError as e:
            print(f"❌ {e}")
            return 1
        prov_name = "sentence-transformers"
    else:
        from docstoolkit.embeddings.tfidf import TFIDFProvider
        prov = TFIDFProvider(cache=cache)
        prov_name = "tfidf"

    skipped = 0
    updated = 0
    for d in docs:
        text = d.get("content", "") + " " + d.get("title", "")
        if not text.strip():
            continue
        doc_id = d.get("path", "")
        if not doc_id:
            continue
        if cache.has_vector(prov_name, doc_id, text):
            skipped += 1
            continue
        vec = prov.encode([text])[0]
        cache.save_vector(prov_name, doc_id, text, vec,
                          dim=len(vec) if isinstance(vec, list) else 0)
        updated += 1

    print(f"✅ {updated} обновлено, {skipped} в кэше уже актуальны")
    cache.close()
    return 0


def cmd_index_clear(args):
    cache = _open_cache()
    if args.provider:
        cache.invalidate(args.provider)
        print(f"✓ Кэш '{args.provider}' очищен")
    else:
        cache.clear_all()
        print("✓ Весь кэш очищен")
    cache.close()
    return 0


def cmd_index_stats(args):
    cache = _open_cache()
    stats = cache.stats()
    print("# Embedding cache stats")
    print(f"  Размер БД: {stats['db_size_kb']} KB")
    print(f"  Всего векторов: {stats['total_vectors']}")
    print(f"  IDF провайдеры: {', '.join(stats['idf_providers']) or '(нет)'}")
    if stats['per_provider']:
        print("\n  По провайдерам:")
        for prov, n in stats['per_provider'].items():
            print(f"    {prov:30s} {n}")
    cache.close()
    return 0


def cmd_plugins_list(args):
    from docstoolkit.plugins import list_plugin_groups, SUPPORTED_GROUPS
    groups = list_plugin_groups()
    print(f"# Плагины (entry_points)\n")
    print(f"Поддерживаемых групп: {len(SUPPORTED_GROUPS)}\n")
    for group, names in groups.items():
        print(f"## {group} ({len(names)})")
        for n in names:
            print(f"  - {n}")
        if not names:
            print("  (нет зарегистрированных)")
        print()
    return 0


def cmd_plugins_inspect(args):
    from docstoolkit.plugins import inspect_plugin
    info = inspect_plugin(args.group, args.name)
    print(json.dumps(info, ensure_ascii=False, indent=2))
    return 0


def cmd_serve(args):
    """Запустить встроенный HTTP-сервер."""
    from docstoolkit.serve import serve
    serve(port=args.port, bind=args.bind)
    return 0


def cmd_doctor(args):
    """Запуск диагностики."""
    from docstoolkit.doctor import doctor
    return doctor(as_json=args.json)


def cmd_search(args):
    """Поиск по корпусу."""
    from docstoolkit.embeddings import get_provider, HybridSearcher
    from docstoolkit.config import load_config

    cfg = load_config()
    index_path = cfg.docs_dir / "search_index.json"
    if not index_path.exists():
        print(f"❌ {index_path} не найден")
        return 1

    docs = json.loads(index_path.read_text(encoding="utf-8"))
    if isinstance(docs, dict):
        docs = docs.get("docs", [])

    keyword = get_provider("tfidf")
    keyword.fit([(d.get("content", "") + " " + d.get("title", "")) for d in docs])

    if args.method == "keyword":
        results = keyword.search(args.query, docs, top_k=args.top)
    elif args.method == "semantic":
        try:
            semantic = get_provider("sentence-transformers", model=args.model)
            results = semantic.search(args.query, docs, top_k=args.top)
        except ImportError as e:
            print(f"❌ {e}")
            return 1
    else:
        semantic = None
        try:
            semantic = get_provider("sentence-transformers", model=args.model)
        except ImportError:
            print("⚠️  semantic недоступен — fallback на keyword only")
        searcher = HybridSearcher(keyword=keyword, semantic=semantic)
        results = searcher.search(args.query, docs, top_k=args.top)

    if args.json:
        print(json.dumps(
            [{"score": r.score, "title": r.title, "path": r.path,
              "snippet": r.snippet} for r in results],
            ensure_ascii=False, indent=2
        ))
    else:
        print(f"# Поиск: {args.query!r} ({args.method})")
        print(f"Найдено: {len(results)}\n")
        for r in results:
            print(f"  [{r.score:.3f}] {r.title}")
            print(f"          {r.path}")
            if r.snippet:
                print(f"          > {r.snippet[:120]}...")
            print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
