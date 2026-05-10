"""
improve_card_index.py — CLI для управления CardEnvelope-карточками.

Превращает docs/ в карточный индекс (CardStore) согласно PROTOTYPE_SPEC.md.
Каждый .md файл → одна CardEnvelope с типом, состоянием, payload и рёбрами.

Команды:
  --build [--section РАЗДЕЛ] [--incremental]  построить/обновить индекс
  --stats                      статистика: сколько карточек, по типам/статусам
  --search "запрос"            поиск по карточкам
  --get <card_id>              показать одну карточку
  --link <from> <to> [--rel ...]  добавить связь между карточками
  --approve <card_id>          перевести карточку в state=approved
  --decay <card_id>            перевести карточку в state=decayed
  --export [--fmt json|md|csv] экспортировать все карточки
  --dry-run                    показать план без изменений

Флаги:
  --incremental  пропустить файлы, не изменившиеся с последней сборки
  --verbose      подробный вывод (для --build)

Запуск:
    python scripts/improve_card_index.py --build --dry-run
    python scripts/improve_card_index.py --build
    python scripts/improve_card_index.py --build --incremental
    python scripts/improve_card_index.py --stats
    python scripts/improve_card_index.py --search "Yodoca память"
    python scripts/improve_card_index.py --export --fmt csv
"""
import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT    = Path(__file__).parent.parent
DOCS    = ROOT / "docs"
CARDS   = ROOT / "cards"
SCRIPTS = ROOT / "scripts"

SKIP_FILES = {
    "BACKLINKS.md", "SUMMARIES.md", "KNOWLEDGE_MAP.md", "SIMILAR_PASSAGES.md",
    "HEADING_AUDIT.md", "LANGUAGE_STATS.md", "PASSIVE_VOICE.md",
    "EMPTY_SECTIONS.md", "SEARCH_RESULTS.md", "README.md",
}

sys.path.insert(0, str(SCRIPTS))
from utils_card_envelope import CardEnvelope, EvidenceEnvelope, CardStore


# ─────────────────────────────────────────────────────────────────────
# Извлечение рёбер из внутренних ссылок
# ─────────────────────────────────────────────────────────────────────

def _extract_internal_links(text: str, base: Path) -> list[str]:
    links = []
    for m in re.finditer(r'\[([^\]]+)\]\(([^)#]+\.md[^)]*)\)', text):
        href = m.group(2).strip().split("#")[0]
        if href.startswith("http") or len(href) > 250:
            continue
        try:
            target = (base.parent / href).resolve()
            if target.exists():
                rel = str(target.relative_to(ROOT))
                links.append(rel)
        except Exception:
            pass
    return links


# ─────────────────────────────────────────────────────────────────────
# Команды
# ─────────────────────────────────────────────────────────────────────

def _file_mtime_iso(path: Path) -> str:
    """Возвращает mtime файла в ISO-8601 формате."""
    import os
    return datetime.utcfromtimestamp(os.path.getmtime(path)).strftime("%Y-%m-%dT%H:%M:%S+00:00")


def cmd_build(section: str = "", dry_run: bool = False,
              incremental: bool = False, verbose: bool = False) -> None:
    store = CardStore(CARDS)

    root = DOCS / section if section else DOCS
    md_files = [f for f in sorted(root.rglob("*.md"))
                if f.name not in SKIP_FILES and not any(
                    p.name.startswith(".") for p in f.parents)]

    # Инкрементальный режим: загружаем существующие карточки для сравнения
    existing: dict[str, str] = {}  # card_id → updated_at
    if incremental and not dry_run:
        for card in store.all():
            existing[card.card_id] = card.updated_at

    mode_label = "[dry-run]" if dry_run else ("Директория: " + str(CARDS.relative_to(ROOT)))
    if incremental:
        mode_label += " [incremental]"

    print(f"\n{'='*60}")
    print(f"  Построение CardStore из {len(md_files)} файлов")
    print(f"  {mode_label}")
    print(f"{'='*60}\n")

    built = skipped = linked = unchanged = 0
    for path in md_files:
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as e:
            print(f"  ⚠ {path.name}: {e}")
            skipped += 1
            continue

        try:
            card = CardEnvelope.from_file(path, root=ROOT)
        except Exception as e:
            print(f"  ⚠ {path.name}: {e}")
            skipped += 1
            continue

        # Инкрементальная проверка: пропустить, если файл не изменился
        if incremental and card.card_id in existing:
            file_mtime = _file_mtime_iso(path)
            card_ts    = existing[card.card_id]
            if file_mtime <= card_ts:
                unchanged += 1
                if verbose:
                    print(f"  ⏩ {path.name} (без изменений)")
                continue

        # Добавляем рёбра из внутренних ссылок
        try:
            links = _extract_internal_links(text, path)
            for link in links[:10]:
                card.add_edge(link, rel="references")
                linked += 1
        except Exception:
            pass

        if dry_run:
            title = card.payload.get("title", path.name)[:45]
            print(f"  {card.card_type:10} {card.card_id[:18]}  {title}")
        else:
            store.put(card)
            if verbose:
                title = card.payload.get("title", path.name)[:40]
                print(f"  ✅ {card.card_type:8} {title}")
        built += 1

    inc_note = f", пропущено (без изм.): {unchanged}" if incremental else ""
    print(f"\n  {'[dry-run] ' if dry_run else ''}Карточек: {built}, рёбер: {linked}, ошибок: {skipped}{inc_note}")
    if dry_run:
        print(f"  Добавьте --build без --dry-run чтобы записать в {CARDS.relative_to(ROOT)}/")
    else:
        print(f"  Записано в {CARDS.relative_to(ROOT)}/")


def cmd_stats() -> None:
    if not CARDS.exists() or not any(CARDS.glob("*.json")):
        print("  CardStore пуст. Запустите: --build")
        return
    store = CardStore(CARDS)
    print(f"\n{store.stats()}")

    # Топ рёбер
    cards = store.all()
    linked = sum(len(c.edges) for c in cards)
    print(f"\nВсего рёбер:  {linked}")
    top_linked = sorted(cards, key=lambda c: -len(c.edges))[:5]
    if top_linked:
        print("Топ-5 связанных:")
        for c in top_linked:
            title = c.payload.get("title", c.card_id[:16])[:45]
            print(f"  {len(c.edges):3d} рёбер  {title}")


def cmd_search(query: str, top: int = 10) -> None:
    if not CARDS.exists():
        print("  CardStore пуст. Запустите: --build")
        return
    store = CardStore(CARDS)
    results = store.search(query, top=top)
    if not results:
        print(f"  Ничего не найдено: «{query}»")
        return
    print(f"\n  Поиск «{query}» — {len(results)} результатов:\n")
    for score, card in results:
        title = card.payload.get("title", card.card_id[:20])[:55]
        path  = card.payload.get("path", "")
        print(f"  [{score:.0f}] {card.card_type:10} {title}")
        if path:
            print(f"        {path}")
    print()


def cmd_get(card_id: str) -> None:
    if not CARDS.exists():
        print("  CardStore пуст. Запустите: --build")
        return
    store = CardStore(CARDS)
    card = store.get(card_id)
    if not card:
        # Попробуем частичный поиск
        all_cards = store.all()
        matches = [c for c in all_cards if card_id.lower() in
                   (c.payload.get("title", "") + c.payload.get("path", "")).lower()]
        if matches:
            print(f"\n  Найдено {len(matches)} совпадений:")
            for c in matches[:5]:
                print(f"  {c.card_id}  {c.payload.get('title','')[:50]}")
        else:
            print(f"  Карточка не найдена: {card_id}")
        return
    print(f"\n{card.to_json()}")


def cmd_link(from_id: str, to_path: str, rel: str = "related",
             dry_run: bool = False) -> None:
    if not CARDS.exists():
        print("  CardStore пуст. Запустите: --build")
        return
    store = CardStore(CARDS)
    card = store.get(from_id)
    if not card:
        # Поиск по title/path
        matches = [c for c in store.all() if from_id.lower() in
                   (c.payload.get("title", "") + c.payload.get("path", "")).lower()]
        if not matches:
            print(f"  Карточка не найдена: {from_id}")
            return
        card = matches[0]
        print(f"  Найдена карточка: {card.payload.get('title','')[:50]}")

    card.add_edge(to_path, rel=rel)  # type: ignore
    print(f"  Добавлено ребро: {card.card_id[:16]} → {to_path}  [{rel}]")
    if not dry_run:
        store.put(card)
        print("  Сохранено.")
    else:
        print("  [dry-run] Не сохранено.")


def cmd_approve(card_id: str, dry_run: bool = False) -> None:
    _transition(card_id, "approved", dry_run)


def cmd_decay(card_id: str, dry_run: bool = False) -> None:
    _transition(card_id, "decayed", dry_run)


def _transition(card_id: str, new_state: str, dry_run: bool) -> None:
    if not CARDS.exists():
        print("  CardStore пуст. Запустите: --build")
        return
    store = CardStore(CARDS)
    card = store.get(card_id)
    if not card:
        print(f"  Карточка не найдена: {card_id}")
        return
    old = card.state
    card.state = new_state  # type: ignore
    print(f"  {card.payload.get('title','')[:50]}")
    print(f"  state: {old} → {new_state}")
    if not dry_run:
        store.put(card)
        print("  Сохранено.")
    else:
        print("  [dry-run] Не сохранено.")


def cmd_export(fmt: str = "json") -> None:
    if not CARDS.exists():
        print("  CardStore пуст. Запустите: --build")
        return
    store = CardStore(CARDS)
    cards = store.all()
    if not cards:
        print("  Карточек нет.")
        return

    if fmt == "json":
        out = CARDS / "index.json"
        data = [c.to_dict() for c in cards]
        out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"  Записано {len(cards)} карточек → {out.relative_to(ROOT)}")

    elif fmt == "md":
        out_dir = CARDS / "md"
        out_dir.mkdir(exist_ok=True)
        for c in cards:
            c.save(out_dir, fmt="md")
        print(f"  Записано {len(cards)} .md файлов → {out_dir.relative_to(ROOT)}/")

    elif fmt == "csv":
        import csv, io
        buf = io.StringIO()
        w = csv.writer(buf)
        w.writerow(["card_id", "card_type", "state", "title", "path", "wc", "edges", "tags"])
        for c in cards:
            p = c.payload
            w.writerow([
                c.card_id, c.card_type, c.state,
                p.get("title", "")[:60],
                p.get("path", ""),
                p.get("wc", 0),
                len(c.edges),
                "|".join(p.get("tags", [])),
            ])
        out = CARDS / "index.csv"
        out.write_text(buf.getvalue(), encoding="utf-8")
        print(f"  Записано {len(cards)} строк → {out.relative_to(ROOT)}")
    else:
        print(f"  Неизвестный формат: {fmt}. Доступные: json, md, csv")


# ─────────────────────────────────────────────────────────────────────
# main
# ─────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="CLI для управления CardEnvelope-индексом (Svyazi 2.0 прототип)"
    )
    parser.add_argument("--build",   action="store_true",
                        help="Построить/обновить CardStore из docs/")
    parser.add_argument("--stats",   action="store_true",
                        help="Статистика CardStore")
    parser.add_argument("--search",  metavar="ЗАПРОС",
                        help="Поиск по карточкам")
    parser.add_argument("--get",     metavar="CARD_ID",
                        help="Показать одну карточку")
    parser.add_argument("--link",    nargs=2, metavar=("FROM", "TO"),
                        help="Добавить ребро FROM → TO")
    parser.add_argument("--approve", metavar="CARD_ID",
                        help="Перевести карточку в state=approved")
    parser.add_argument("--decay",   metavar="CARD_ID",
                        help="Перевести карточку в state=decayed")
    parser.add_argument("--export",  action="store_true",
                        help="Экспортировать все карточки")
    parser.add_argument("--section", metavar="РАЗДЕЛ",
                        help="Обработать только один раздел docs/ (для --build)")
    parser.add_argument("--rel",     default="related",
                        help="Тип связи (для --link): references|contradicts|extends|related")
    parser.add_argument("--fmt",     default="json",
                        choices=["json", "md", "csv"],
                        help="Формат экспорта (для --export)")
    parser.add_argument("--top",     type=int, default=10,
                        help="Число результатов (для --search)")
    parser.add_argument("--dry-run",     action="store_true",
                        help="Показать план без записи файлов")
    parser.add_argument("--incremental", action="store_true",
                        help="Пропустить файлы без изменений (для --build)")
    parser.add_argument("--verbose",     action="store_true",
                        help="Подробный вывод (для --build)")
    args = parser.parse_args()

    dry_run = args.dry_run

    if args.build:
        cmd_build(section=args.section or "", dry_run=dry_run,
                  incremental=args.incremental, verbose=args.verbose)
    elif args.stats:
        cmd_stats()
    elif args.search:
        cmd_search(args.search, top=args.top)
    elif args.get:
        cmd_get(args.get)
    elif args.link:
        cmd_link(args.link[0], args.link[1], rel=args.rel, dry_run=dry_run)
    elif args.approve:
        cmd_approve(args.approve, dry_run=dry_run)
    elif args.decay:
        cmd_decay(args.decay, dry_run=dry_run)
    elif args.export:
        cmd_export(fmt=args.fmt)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
