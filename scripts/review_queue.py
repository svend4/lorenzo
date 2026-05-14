#!/usr/bin/env python3
"""
Review Queue UI — Streamlit-интерфейс для просмотра и одобрения карточек знаний.

Реализует Review Record из PROTOTYPE_SPEC §3.5:
  - Показывает карточки со статусом proposal / raw (требуют ревью)
  - Позволяет одобрить (approved), отклонить (rejected) или отложить (deferred)
  - Записывает Review Record в YAML frontmatter карточки
  - Интегрируется с gateway: карточки добавленные через POST /api/cards
    попадают в очередь с source: gateway

Запуск:
    pip install streamlit
    streamlit run scripts/review_queue.py

Или через gateway (запустить оба):
    python scripts/gateway.py &
    streamlit run scripts/review_queue.py
"""

import json
import re
import subprocess
from datetime import datetime
from pathlib import Path

try:
    import streamlit as st
except ImportError:
    st = None  # type: ignore  # UI functions only; non-UI helpers work without it

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

# ── Константы ───────────────────────────────────────────────────────────────

SECTIONS = {
    "01-svyazi":               "Svyazi 2.0 — архитектура",
    "02-anthropic-vacancies":  "Вакансии Anthropic",
    "03-technology-combinations": "Комбинации технологий",
    "04-ai-collaborations":    "AI коллаборации",
    "05-habr-projects":        "Хабр-проекты",
    "contacts":                "Контакты",
    "letters":                 "Письма",
}

STATE_COLORS = {
    "raw":        "🟡",
    "normalized": "🔵",
    "proposal":   "🟠",
    "approved":   "🟢",
    "rejected":   "🔴",
    "decayed":    "⚫",
}

# ── Парсинг карточек ────────────────────────────────────────────────────────

def _parse_frontmatter(text: str) -> dict:
    """Извлечь YAML frontmatter из .md файла."""
    fm: dict = {}
    if not text.startswith("---"):
        return fm
    end = text.find("\n---", 3)
    if end == -1:
        return fm
    block = text[3:end].strip()
    for line in block.splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip()
    return fm


def _write_frontmatter(path: Path, updates: dict) -> None:
    """Обновить поля в YAML frontmatter файла."""
    text = path.read_text(encoding="utf-8")
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            block = text[3:end]
            for k, v in updates.items():
                pattern = rf"^({re.escape(k)}:\s*).*$"
                replacement = rf"\g<1>{v}"
                if re.search(pattern, block, re.MULTILINE):
                    block = re.sub(pattern, replacement, block, flags=re.MULTILINE)
                else:
                    block += f"\n{k}: {v}"
            text = "---" + block + text[end:]
            path.write_text(text, encoding="utf-8")
            return
    # Нет frontmatter — добавляем
    fm_lines = "\n".join(f"{k}: {v}" for k, v in updates.items())
    path.write_text(f"---\n{fm_lines}\n---\n\n" + text, encoding="utf-8")


def load_queue(filter_state: str | None = None, filter_section: str | None = None) -> list[dict]:
    """Загрузить все карточки, отфильтровать по состоянию и секции."""
    cards = []
    search_root = DOCS / filter_section if filter_section else DOCS

    for f in sorted(search_root.rglob("*.md")):
        # Пропустить авто-генерированные файлы
        if f.name in {
            "search_index.json", "README.md", "GATEWAY.md", "SENTINEL.md",
            "SCORING.md", "HEALTH.md", "METRICS.md", "PROGRESS.md",
        }:
            continue
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        fm = _parse_frontmatter(text)
        state  = fm.get("state", "raw")
        source = fm.get("source", "")
        date   = fm.get("date", "")

        if filter_state and state != filter_state:
            continue

        # Извлечь первые 400 символов контента (после frontmatter)
        body_start = text.find("\n---\n", 3)
        body = text[body_start + 5:].strip() if body_start != -1 else text.strip()
        preview = body[:400].replace("\n", " ")

        # Секция из пути
        parts = f.relative_to(DOCS).parts
        section = parts[0] if parts else "other"

        cards.append({
            "path":    f,
            "rel":     str(f.relative_to(ROOT)),
            "name":    f.stem,
            "section": section,
            "state":   state,
            "source":  source,
            "date":    date,
            "title":   fm.get("title", f.stem),
            "tags":    fm.get("tags", ""),
            "preview": preview,
            "fm":      fm,
        })

    return cards


def approve_card(path: Path, reason: str = "") -> None:
    _write_frontmatter(path, {
        "state":           "approved",
        "reviewed_at":     datetime.now().strftime("%Y-%m-%d"),
        "reviewer_role":   "human",
        "review_decision": "approved",
        "review_reason":   reason or "Одобрено через Review Queue UI",
    })


def reject_card(path: Path, reason: str = "") -> None:
    _write_frontmatter(path, {
        "state":           "rejected",
        "reviewed_at":     datetime.now().strftime("%Y-%m-%d"),
        "reviewer_role":   "human",
        "review_decision": "rejected",
        "review_reason":   reason or "Отклонено через Review Queue UI",
    })


def defer_card(path: Path, reason: str = "") -> None:
    _write_frontmatter(path, {
        "state":           "proposal",
        "reviewed_at":     datetime.now().strftime("%Y-%m-%d"),
        "reviewer_role":   "human",
        "review_decision": "deferred",
        "review_reason":   reason or "Отложено на потом",
    })


def run_index_update() -> str:
    """Обновить search_index.json после изменений."""
    try:
        r = subprocess.run(
            ["python3", str(ROOT / "scripts" / "improve_index_update.py")],
            cwd=ROOT, capture_output=True, text=True, timeout=30,
        )
        return r.stdout.strip() or "Индекс обновлён."
    except Exception as e:
        return f"Ошибка: {e}"

# ── Streamlit UI ─────────────────────────────────────────────────────────────

def main() -> None:
    st.set_page_config(
        page_title="Review Queue — Lorenzo",
        page_icon="📋",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # ── Заголовок ──────────────────────────────────────────────────────────
    st.title("📋 Review Queue — Lorenzo / Svyazi 2.0")
    st.caption(
        "Очередь проверки карточек знаний. "
        "Одобряйте, отклоняйте или откладывайте предложенные карточки."
    )

    # ── Боковая панель ─────────────────────────────────────────────────────
    with st.sidebar:
        st.header("Фильтры")

        filter_state = st.selectbox(
            "Состояние карточки",
            options=["все", "raw", "proposal", "normalized", "approved", "rejected", "decayed"],
            index=0,
        )
        state_arg = None if filter_state == "все" else filter_state

        filter_section = st.selectbox(
            "Раздел",
            options=["все разделы"] + list(SECTIONS.keys()),
            index=0,
        )
        section_arg = None if filter_section == "все разделы" else filter_section

        st.divider()

        st.header("Статистика")
        all_cards = load_queue()
        state_counts: dict[str, int] = {}
        for c in all_cards:
            state_counts[c["state"]] = state_counts.get(c["state"], 0) + 1

        for state, count in sorted(state_counts.items(), key=lambda x: -x[1]):
            icon = STATE_COLORS.get(state, "⚪")
            st.write(f"{icon} **{state}**: {count}")

        st.divider()
        st.metric("Всего карточек", len(all_cards))

        st.divider()
        if st.button("🔄 Обновить индекс", use_container_width=True):
            msg = run_index_update()
            st.success(msg)

    # ── Основная область ────────────────────────────────────────────────────
    cards = load_queue(filter_state=state_arg, filter_section=section_arg)

    if not cards:
        st.info(
            f"Нет карточек с фильтром: состояние=«{filter_state}», "
            f"раздел=«{filter_section}»"
        )
        return

    st.write(f"**{len(cards)} карточек** по текущему фильтру")
    st.divider()

    # ── Сортировка ──────────────────────────────────────────────────────────
    sort_by = st.radio(
        "Сортировать по",
        options=["дате (новые)", "названию", "разделу"],
        horizontal=True,
    )
    if sort_by == "дате (новые)":
        cards.sort(key=lambda c: c["date"] or "", reverse=True)
    elif sort_by == "названию":
        cards.sort(key=lambda c: c["title"])
    else:
        cards.sort(key=lambda c: c["section"])

    # ── Список карточек ─────────────────────────────────────────────────────
    for card in cards:
        state_icon = STATE_COLORS.get(card["state"], "⚪")
        section_label = SECTIONS.get(card["section"], card["section"])

        with st.expander(
            f"{state_icon} **{card['title']}**  ·  `{section_label}`  ·  {card['date']}",
            expanded=(card["state"] in {"proposal", "raw"} and len(cards) <= 10),
        ):
            col_meta, col_content = st.columns([1, 2])

            with col_meta:
                st.markdown("**Метаданные**")
                st.code(
                    f"state:   {card['state']}\n"
                    f"source:  {card['source'] or '—'}\n"
                    f"tags:    {card['tags'] or '—'}\n"
                    f"date:    {card['date'] or '—'}",
                    language="yaml",
                )
                st.caption(f"`{card['rel']}`")

            with col_content:
                st.markdown("**Предпросмотр**")
                st.markdown(card["preview"] + "…" if len(card["preview"]) == 400 else card["preview"])

            # Полный текст
            with st.expander("Полный текст"):
                try:
                    full = card["path"].read_text(encoding="utf-8", errors="ignore")
                    st.markdown(full[:8000])
                except Exception as e:
                    st.error(str(e))

            # Кнопки действий (только для неодобренных)
            if card["state"] not in {"approved", "rejected", "decayed"}:
                st.markdown("---")
                reason = st.text_input(
                    "Комментарий (необязательно)",
                    key=f"reason_{card['rel']}",
                    placeholder="Причина решения…",
                )
                btn_col1, btn_col2, btn_col3, btn_col4 = st.columns(4)
                with btn_col1:
                    if st.button("✅ Одобрить", key=f"approve_{card['rel']}", type="primary"):
                        approve_card(card["path"], reason)
                        st.success(f"Одобрено: {card['title']}")
                        st.rerun()
                with btn_col2:
                    if st.button("❌ Отклонить", key=f"reject_{card['rel']}"):
                        reject_card(card["path"], reason)
                        st.warning(f"Отклонено: {card['title']}")
                        st.rerun()
                with btn_col3:
                    if st.button("⏸ Отложить", key=f"defer_{card['rel']}"):
                        defer_card(card["path"], reason)
                        st.info(f"Отложено: {card['title']}")
                        st.rerun()
                with btn_col4:
                    st.link_button(
                        "📂 Открыть файл",
                        url=f"vscode://file/{card['path']}",
                    )
            else:
                review_decision = card["fm"].get("review_decision", "")
                review_reason   = card["fm"].get("review_reason", "")
                reviewed_at     = card["fm"].get("reviewed_at", "")
                if review_decision:
                    st.caption(
                        f"Решение: **{review_decision}** · {reviewed_at} · {review_reason}"
                    )

    # ── Нижний колонтитул ───────────────────────────────────────────────────
    st.divider()
    st.caption(
        "Lorenzo Review Queue v1.0 · Svyazi 2.0 · "
        "Review Record из PROTOTYPE_SPEC §3.5 · "
        f"Всего карточек в корпусе: {len(all_cards)}"
    )


if __name__ == "__main__":
    main()
