"""NER без зависимостей — regex + heuristics.

Извлекает 4 типа сущностей:
  - PERSON: «Имя Фамилия» (CapWord CapWord) или @handle
  - PROJECT: CamelCase / kebab-case / known list
  - CONCEPT: Capitalized термины 1+ слов
  - DATE: YYYY-MM-DD, DD.MM.YYYY, "июль 2024"
"""
import re
from collections import Counter
from dataclasses import dataclass


class EntityKinds:
    PERSON = "person"
    PROJECT = "project"
    CONCEPT = "concept"
    DATE = "date"


_PERSON_RE = re.compile(r'\b([А-ЯA-Z][а-яa-z]+(?:[\s-][А-ЯA-Z][а-яa-z]+)+)\b')
_HANDLE_RE = re.compile(r'@([\w-]{2,})')
# CamelCase: Foo+Bar или Foo+ABBR (AgentFS, NgtMemory, RAGSystem)
_CAMEL_RE = re.compile(r'\b([A-Z][a-z]+(?:[A-Z][a-z]+|[A-Z]{2,})+)\b')
_KEBAB_RE = re.compile(r'\b([a-z]+(?:-[a-z]+){1,3})\b')  # kebab-case
_DATE_ISO = re.compile(r'\b(\d{4}-\d{2}-\d{2})\b')
_DATE_DOT = re.compile(r'\b(\d{1,2}\.\d{1,2}\.\d{4})\b')
_DATE_RU = re.compile(r'\b((?:январь|февраль|март|апрель|май|июнь|июль|'
                       r'август|сентябрь|октябрь|ноябрь|декабрь|'
                       r'января|февраля|марта|апреля|мая|июня|июля|'
                       r'августа|сентября|октября|ноября|декабря)'
                       r'\s+\d{4})\b', re.IGNORECASE)


# Стоп-слова для CONCEPT и PROJECT — избегать ложных срабатываний
_STOP_CAPITAL = {
    "Это", "При", "Как", "Что", "Все", "Для", "Без", "Это", "Также", "Если",
    "The", "And", "But", "For", "With", "From", "About", "Then",
}


@dataclass
class Entity:
    text: str
    kind: str
    count: int = 1


def extract_entities(text: str,
                     min_text_len: int = 100) -> dict[str, list[Entity]]:
    """Возвращает {kind: [Entity, ...]}, сгруппировано и отсортировано по count.

    min_text_len: если text короче — возвращает пустые (избегает шума на header'ах).
    """
    if len(text) < min_text_len:
        return {kind: [] for kind in
                (EntityKinds.PERSON, EntityKinds.PROJECT,
                 EntityKinds.CONCEPT, EntityKinds.DATE)}

    persons: Counter = Counter()
    projects: Counter = Counter()
    concepts: Counter = Counter()
    dates: Counter = Counter()

    # Persons: CapWord CapWord
    for m in _PERSON_RE.finditer(text):
        name = m.group(1)
        if name.split()[0] not in _STOP_CAPITAL:
            persons[name] += 1
    # @handles
    for m in _HANDLE_RE.finditer(text):
        persons[f"@{m.group(1)}"] += 1

    # Projects: CamelCase
    for m in _CAMEL_RE.finditer(text):
        word = m.group(1)
        if word in _STOP_CAPITAL:
            continue
        projects[word] += 1

    # Projects: kebab-case (только из 2+ частей)
    for m in _KEBAB_RE.finditer(text):
        word = m.group(1)
        if "-" in word and len(word.split("-")) >= 2:
            projects[word] += 1

    # Concepts: «Big Letter Word» в тексте — 1-3 заглавных слова подряд (не PERSON)
    # Чтобы не дублироваться с persons, ищем одинарные заглавные слова
    for m in re.finditer(r'\b([А-ЯA-Z][а-яa-zё]{4,})\b', text):
        word = m.group(1)
        if word in _STOP_CAPITAL:
            continue
        if word in persons or word in projects:
            continue
        concepts[word] += 1

    # Dates
    for re_pat in (_DATE_ISO, _DATE_DOT, _DATE_RU):
        for m in re_pat.finditer(text):
            dates[m.group(1).strip()] += 1

    def to_entities(counter: Counter, kind: str) -> list[Entity]:
        return [Entity(text=t, kind=kind, count=n)
                for t, n in counter.most_common()
                if n > 0]

    return {
        EntityKinds.PERSON: to_entities(persons, EntityKinds.PERSON),
        EntityKinds.PROJECT: to_entities(projects, EntityKinds.PROJECT),
        EntityKinds.CONCEPT: to_entities(concepts, EntityKinds.CONCEPT),
        EntityKinds.DATE: to_entities(dates, EntityKinds.DATE),
    }
