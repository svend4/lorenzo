"""Часть 4: разбивка deep-research-report (1) и (3) в docs/01-svyazi/."""
from part1_utils import ROOT, DOCS, write_doc
from part2_split_md import split_by_h2

# Сопоставление H2-заголовков отчёта 1 → имена файлов
REPORT1_MAP = {
    'Executive summary':                         '01-executive-summary.md',
    'Методика и рамка отбора':                   '02-methodology.md',
    'Карта найденных проектов и паттернов':       '03-component-catalog.md',
    'Приоритетные ансамбли':                     '04-ensembles-overview.md',
    'План прототипа и возможные контакты':        '07-mvp-planning.md',
    'Безопасность, приватность и бюджетный роутинг': '06-security-privacy.md',
    'Выводы':                                    '08-conclusions.md',
}

# Сопоставление H2-заголовков отчёта 3 → имена файлов
REPORT3_MAP = {
    'Что это продолжение добавляет':             '00-intro-part2.md',
    'Архитектурные зазоры, которые важнее новых инструментов': '09-architectural-gaps.md',
    'Новые ансамбли следующего шага':            '10-second-order-ensembles.md',
    'Интеграционный контракт, который стоит зафиксировать сразу': '11-integration-contracts.md',
    'Дорожная карта прототипа следующей итерации': '12-roadmap.md',
    'Контактная стратегия и узкие вопросы для авторов': '13-contacts.md',
    'Ограничения, лицензии и что пока лучше не склеивать': '14-limitations.md',
}


def process_report(md_path, section_map, out_dir):
    """Читает Markdown, делит по H2, пишет по карте."""
    text = md_path.read_text(encoding='utf-8')
    sections = split_by_h2(text)

    written = 0
    for title, body in sections:
        # Ищем совпадение в карте (частичное)
        target = None
        for key, fname in section_map.items():
            if key.lower() in title.lower() or title.lower() in key.lower():
                target = fname
                break

        if target:
            dest = out_dir / target
            # Не перезаписывать, если файл уже существует
            if dest.exists():
                print(f"  skip (exists): {dest.name}")
            else:
                write_doc(dest, body)
                written += 1

    print(f"  {written} files written from {md_path.name}")


def run():
    out = DOCS / "01-svyazi"

    r1 = ROOT / "deep-research-report (1).md"
    r3 = ROOT / "deep-research-report (3).md"

    print("\n--- Report 1 ---")
    process_report(r1, REPORT1_MAP, out)

    print("\n--- Report 3 ---")
    process_report(r3, REPORT3_MAP, out)


if __name__ == '__main__':
    run()
