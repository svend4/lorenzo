"""i18n — простая система переводов через словарь.

Расширение через docstoolkit.toml:
  [i18n]
  default_locale = "ru"
  custom_messages = "i18n/custom.json"  # путь к доп. словарю
"""
import re
from typing import Any


_MESSAGES: dict[str, dict[str, str]] = {
    "en": {
        "validation.missing_field": "Missing required field: {field}",
        "validation.missing_section": "Missing required section: ## {section}",
        "validation.bad_enum": "Field {field}: value {value!r} not in {allowed}",
        "validation.bad_pattern": "Field {field}: value {value!r} does not match pattern {pattern!r}",
        "validation.bad_type": "Field {field}: type {actual} != expected {expected}",
        "validation.bad_date": "Field {field}: invalid date {value!r}, expected YYYY-MM-DD",
        "validation.too_short": "Field {field}: length {length} < minLength={min}",
        "validation.below_min": "Field {field}: {value} < minimum={min}",
        "validation.above_max": "Field {field}: {value} > maximum={max}",
        "doctor.summary": "{ok} ok, {warn} warnings, {error} errors",
        "search.no_results": "No results for {query!r}",
        "search.found_n": "Found {n} results",
    },
    "ru": {
        "validation.missing_field": "Отсутствует обязательное поле: {field}",
        "validation.missing_section": "Отсутствует обязательная секция: ## {section}",
        "validation.bad_enum": "Поле {field}: значение {value!r} не в {allowed}",
        "validation.bad_pattern": "Поле {field}: значение {value!r} не соответствует pattern {pattern!r}",
        "validation.bad_type": "Поле {field}: тип {actual} != ожидался {expected}",
        "validation.bad_date": "Поле {field}: некорректная дата {value!r}, нужен формат YYYY-MM-DD",
        "validation.too_short": "Поле {field}: длина {length} < minLength={min}",
        "validation.below_min": "Поле {field}: {value} < minimum={min}",
        "validation.above_max": "Поле {field}: {value} > maximum={max}",
        "doctor.summary": "{ok} ok, {warn} предупреждений, {error} ошибок",
        "search.no_results": "Ничего не найдено по запросу {query!r}",
        "search.found_n": "Найдено: {n}",
    },
}


_current_locale = "en"


def available_locales() -> list[str]:
    return sorted(_MESSAGES)


def set_locale(locale: str):
    """Устанавливает текущую локаль (ru | en)."""
    global _current_locale
    if locale not in _MESSAGES:
        # Fallback на en
        locale = "en"
    _current_locale = locale


def get_locale() -> str:
    return _current_locale


def t(key: str, locale: str | None = None, **kwargs: Any) -> str:
    """Возвращает локализованную строку с подстановкой kwargs.

    Если ключ не найден в выбранной локали — fallback на en.
    Если не найден нигде — возвращает сам ключ (debug).
    """
    loc = locale or _current_locale
    msg = _MESSAGES.get(loc, {}).get(key)
    if msg is None:
        msg = _MESSAGES.get("en", {}).get(key)
    if msg is None:
        return key
    try:
        return msg.format(**kwargs)
    except KeyError:
        return msg


def register_messages(locale: str, messages: dict[str, str]):
    """Регистрирует доп. сообщения (для плагинов)."""
    if locale not in _MESSAGES:
        _MESSAGES[locale] = {}
    _MESSAGES[locale].update(messages)
