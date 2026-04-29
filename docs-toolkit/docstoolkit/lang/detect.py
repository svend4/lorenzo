"""Детектор языка — без зависимостей, по соотношению букв.

Поддерживаемые языки:
  - ru (кириллица)
  - en (латиница)
  - mixed (≥30% обоих)
  - unknown (мало текста / непонятно)
"""
import re


_RU_LETTER = re.compile(r'[а-яё]', re.IGNORECASE)
_EN_LETTER = re.compile(r'[a-z]', re.IGNORECASE)


def language_stats(text: str) -> dict:
    """Возвращает {ru_chars, en_chars, ru_ratio, en_ratio, total}."""
    ru = len(_RU_LETTER.findall(text))
    en = len(_EN_LETTER.findall(text))
    total = ru + en
    return {
        "ru_chars": ru,
        "en_chars": en,
        "ru_ratio": ru / total if total else 0,
        "en_ratio": en / total if total else 0,
        "total": total,
    }


def detect_language(text: str, threshold_mixed: float = 0.3) -> str:
    """Определяет язык: 'ru' | 'en' | 'mixed' | 'unknown'.

    threshold_mixed: если оба языка имеют долю ≥ threshold_mixed, вернёт 'mixed'.
    """
    stats = language_stats(text)
    if stats["total"] < 5:
        return "unknown"

    ru_r, en_r = stats["ru_ratio"], stats["en_ratio"]

    if ru_r >= threshold_mixed and en_r >= threshold_mixed:
        return "mixed"
    if ru_r > en_r:
        return "ru"
    if en_r > ru_r:
        return "en"
    return "unknown"
