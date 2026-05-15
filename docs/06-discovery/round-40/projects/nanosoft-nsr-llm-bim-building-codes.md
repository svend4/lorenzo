---
date: 2026-05-15
tags: [rag, orchestration, knowledge, ingestion, architecture]
state: normalized
---

# NSR Specification: LLM для автоматической проверки BIM по строительным нормам

<!-- toc-auto -->
<!-- tags: nanosoft-nsr-llm-bim-building-codes, docs -->


<!-- summary -->
> Автор: nanocad (Нанософт) Хабр: https://habr.com/ru/companies/nanosoft/articles/947304/
Хабр: https://habr.com/ru/companies/nanosoft/articles/947304/  
GitHub: нет (коммерческая разработка)  
Слой: analytics / orchestration  
Дата: сентябрь 2025  
Уникальность: Единственная российская система автоматического


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Автор:** nanocad (Нанософт)  
**Хабр:** https://habr.com/ru/companies/nanosoft/articles/947304/  
**GitHub:** нет (коммерческая разработка)  
**Слой:** analytics / orchestration  
**Дата:** сентябрь 2025  
**Уникальность:** Единственная российская система автоматического преобразования текста строительных нормативов (СНиПы, СП) в машиночитаемые правила проверки BIM/ЦИМ-моделей. LLM парсит каждое требование нормы в триплет Subject→Object→Property, из которого генерируется правило-чекер. Гибридная архитектура: LLM для семантической разметки + ручная верификация (LLM точность 50-60%). Форматы IFC/CDE, поддержка CADLib/Larix/nanoCAD/BIMIT.

## Проблема: строительные нормы написаны для людей, не для машин

```
Строительный норматив (СП 55.13330.2011):
  "Высота жилых помещений должна составлять не менее 2,5 м"
  → Это предложение на русском языке
  → BIM-модель: объект Floor с атрибутом Height = 2.4
  → Нет автоматической связи между нормой и моделью

Текущий процесс:
  → Эксперт-нормировщик читает СП вручную
  → Вручную программирует правило проверки в BIMIT/Solibri
  → 1000+ требований в СП → месяцы работы

NSR Specification:
  → LLM читает СП → триплеты Subject → Object → Property
  → Триплет → правило-чекер в NSR Specification формате
  → Автоматическая проверка BIM-модели по правилам
```

## Архитектура: LLM → Триплеты → NSR Rules

```python
# Нанософт NSR Specification: семантическая разметка норм

from dataclasses import dataclass
from typing import Optional
import json

@dataclass
class NormativeTriple:
    """
    Subject → Object → Property: машиночитаемое требование нормы.
    Из каждого требования СП извлекается один или несколько триплетов.
    """
    subject: str        # "жилое помещение", "несущая стена"
    object_attr: str    # "высота", "толщина", "расстояние"
    property_value: str # "не менее 2.5 м", "от 200 мм до 300 мм"
    condition: Optional[str] = None  # "при высоте здания > 5 этажей"
    source_sp: str = ""  # "СП 55.13330.2011 п.6.2"
    confidence: float = 0.0  # LLM уверенность (0.5-0.6 в среднем)


class NormativeParser:
    """
    LLM-парсер строительных норм → триплеты → NSR правила.
    Точность на этапе суждений: 50-60% (требует верификации).
    """

    PARSE_PROMPT = """Ты — эксперт по строительным нормам.
Извлеки из текста требования нормы структурированные триплеты.

Каждый триплет = {subject, object, property_value, condition}.

Текст нормы: {norm_text}
Источник: {source}

Сложные случаи:
- Таблицы: каждая строка = отдельный триплет
- Исключения: условие записывается в поле condition
- Относительные значения: "не менее X" → property_value = "≥ X"
- Неявные условия: "в жилых помещениях" → добавить в condition

Верни JSON массив триплетов."""

    def parse_norm_text(self, norm_text: str,
                         source: str) -> list[NormativeTriple]:
        """
        LLM парсинг одного пункта нормы.
        Результат проходит верификацию перед добавлением в NSR.
        """
        response = self.llm.generate(
            self.PARSE_PROMPT.format(
                norm_text=norm_text,
                source=source
            )
        )

        try:
            triples_raw = json.loads(response)
            return [
                NormativeTriple(
                    subject=t.get("subject", ""),
                    object_attr=t.get("object", ""),
                    property_value=t.get("property_value", ""),
                    condition=t.get("condition"),
                    source_sp=source,
                    confidence=t.get("confidence", 0.5)
                )
                for t in triples_raw
            ]
        except json.JSONDecodeError:
            return []  # 40-50% случаев требуют ручной корректировки

    def process_sp_document(self, sp_path: str) -> list[NormativeTriple]:
        """
        Обработать весь СП документ.
        Чанкинг: каждый пункт нормы = отдельный запрос к LLM.
        """
        norms = self.extract_norm_paragraphs(sp_path)
        all_triples = []

        for norm in norms:
            triples = self.parse_norm_text(norm.text, norm.source_ref)
            # Фильтр по confidence и базовая валидация
            valid = [t for t in triples
                     if t.confidence >= 0.5 and t.subject and t.object_attr]
            all_triples.extend(valid)

        return all_triples
```

## NSR Specification: формат машиночитаемых правил

```python
class NSRRuleGenerator:
    """
    Из триплетов генерировать правила проверки BIM-модели.
    NSR Specification = собственный формат Нанософт для BIM-чекеров.
    Мировые аналоги: buildingSMART mvdXML/IDS, Solibri rules.
    """

    def triple_to_nsr_rule(self,
                            triple: NormativeTriple) -> dict:
        """
        NormativeTriple → NSR Rule для проверки IFC-модели.
        """
        # Парсинг property_value в оператор и значение
        operator, value = self._parse_constraint(triple.property_value)

        rule = {
            "rule_id": f"NSR_{triple.source_sp.replace(' ', '_')}",
            "description": f"{triple.source_sp}: {triple.subject} {triple.object_attr} {triple.property_value}",
            "source": triple.source_sp,

            # Фильтр: какие объекты BIM-модели проверять
            "scope": {
                "ifc_types": self._map_subject_to_ifc(triple.subject),
                # "жилое помещение" → ["IfcSpace", "IfcRoom"]
                "condition": triple.condition
            },

            # Что проверять
            "check": {
                "attribute": self._map_object_to_ifc_attr(triple.object_attr),
                # "высота" → "Height"
                "operator": operator,  # "≥", "≤", "=", "between"
                "value": value,        # 2.5 (в метрах)
                "unit": self._extract_unit(triple.property_value)
            },

            # Что выводить при нарушении
            "violation": {
                "severity": "error",
                "message": f"Нарушение {triple.source_sp}: {triple.object_attr} {triple.property_value}"
            }
        }
        return rule

    def _map_subject_to_ifc(self, subject: str) -> list[str]:
        """
        Маппинг русскоязычного субъекта нормы → IFC типы.
        Самая сложная часть: требует экспертной базы знаний.
        """
        SUBJECT_TO_IFC = {
            "жилое помещение":     ["IfcSpace"],
            "несущая стена":       ["IfcWall"],
            "перекрытие":          ["IfcSlab"],
            "лестница":            ["IfcStair", "IfcStairFlight"],
            "оконный проём":       ["IfcWindow"],
            "дверной проём":       ["IfcDoor"],
            "коридор":             ["IfcSpace"],  # с доп. условием
        }
        return SUBJECT_TO_IFC.get(subject.lower(), ["IfcBuildingElement"])


class BIMModelChecker:
    """
    Проверка IFC-модели по набору NSR правил.
    Поддерживаемые BIM-платформы: CADLib, Larix, Tangle, BIMIT, nanoCAD.
    """

    def check_model(self, ifc_path: str,
                     nsr_rules: list[dict]) -> list[dict]:
        """
        Загрузить IFC → применить NSR правила → вернуть нарушения.
        """
        import ifcopenshell

        model = ifcopenshell.open(ifc_path)
        violations = []

        for rule in nsr_rules:
            # Найти элементы нужного типа
            for ifc_type in rule["scope"]["ifc_types"]:
                elements = model.by_type(ifc_type)

                for element in elements:
                    # Проверить условие scope
                    if not self._matches_condition(element,
                                                    rule["scope"]["condition"]):
                        continue

                    # Получить значение атрибута
                    actual_value = self._get_attribute(
                        element, rule["check"]["attribute"]
                    )

                    # Применить проверку
                    if actual_value is not None:
                        if not self._check_constraint(
                            actual_value,
                            rule["check"]["operator"],
                            rule["check"]["value"]
                        ):
                            violations.append({
                                "rule_id": rule["rule_id"],
                                "element_id": element.GlobalId,
                                "element_type": ifc_type,
                                "actual_value": actual_value,
                                "required": f"{rule['check']['operator']} {rule['check']['value']}",
                                "message": rule["violation"]["message"],
                                "source": rule["source"]
                            })

        return violations
```

## Метрики и мировые аналоги

```python
NSR_SYSTEM_PROFILE = {
    "статус": "Разработка, релиз модуля планировался осень 2025",
    "организация": "Нанософт (российский разработчик САПР/BIM)",

    "точность_llm": {
        "на_этапе_суждений": "50-60%",
        "комментарий": "Честно признана: 'чистое ИИ пока не справляется'",
        "архитектура": "Гибрид: LLM-разметка + ручная верификация"
    },

    "поддерживаемые_форматы": ["IFC", "CDE"],
    "поддерживаемые_системы": ["CADLib", "Larix", "Tangle", "BIMIT", "nanoCAD"],

    "сложные_случаи": [
        "Таблицы с размерными рядами",
        "Исключения из общих правил",
        "Относительные значения ('не менее X')",
        "Неявные условия применимости"
    ],

    "мировые_аналоги": {
        "buildingSMART": "mvdXML + IDS (Industry Foundation Classes)",
        "Solibri": "Коммерческий BIM-чекер с rule editor",
        "CORENET": "e-PlanCheck (Сингапур) — автоматическая экспертиза",
        "ICC SmartCodes": "Цифровые строительные нормы США",
        "RASE": "Requirements, Applicability, Selection, Exception подход",
        "отличие_NSR": "Фокус на русской нормативной базе (СП, СНиП)"
    }
}
```

## Применение к Lorenzo

```python
# Lorenzo анализирует документы.
# NSR паттерн: извлечение структурированных правил из нормативных текстов

class LorenzoNormativeExtractor:
    """
    Применить NSR паттерн к любым нормативным документам:
    правила, регламенты, стандарты → машиночитаемые проверки.

    Пример: извлечь правила из CLAUDE.md и проверить
    что improve_*.py скрипты им следуют.
    """

    def extract_rules_from_doc(self, doc_path: str) -> list[dict]:
        norms = self.chunker.extract_norm_paragraphs(doc_path)
        rules = []
        for norm in norms:
            triples = self.parser.parse_norm_text(norm.text, norm.source)
            rules.extend([
                self.generator.triple_to_rule(t)
                for t in triples
                if t.confidence >= 0.6
            ])
        return rules
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **NSR + ASCON NLP (R39)** | ASCON извлекает требования из ГОСТов → NSR генерирует BIM-правила |
| **NSR + CV Guard (R37)** | CV Guard верифицирует геометрические параметры BIM через компьютерное зрение |
| **NSR + Agentfs (R01)** | Файловая система AgentFS для хранения NSR правил с версионированием |
| **NSR + Graph RAG (R38)** | Граф нормативных требований → NSR правила через Skeleton Indexing |
| **NSR + LLAMATOR (R33)** | Red-teaming NSR: атаки на LLM-парсер нормативов через adversarial примеры |

## Контакт

- Статья: https://habr.com/ru/companies/nanosoft/articles/947304/ (сентябрь 2025)
- Нанософт: nanocad.ru
- IFC: buildingsmart.org/standards/bsi-standards/industry-foundation-classes/
- Смежная (RAG для строительных нормативов): https://habr.com/ru/articles/992348/
- Смежная (ML в строительстве, Magnus Tech): https://habr.com/ru/companies/magnus-tech/articles/867756/

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
- [Решения](../../../DECISIONS.md)
