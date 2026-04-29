"""Multi-language support для docs-toolkit.

Модули:
  - detect.py — определение языка текста (по соотношению ru/en букв)
  - i18n.py — словарь переводов сообщений
  - readability.py — language-aware Flesch-Kincaid (ru / en коэффициенты)

Использование:
    from docstoolkit.lang import detect_language, t, readability_score

    lang = detect_language(text)         # 'ru' | 'en' | 'mixed' | 'unknown'
    msg = t('validation.missing_field', lang='en', field='title')
    score = readability_score(text, lang='ru')
"""
from docstoolkit.lang.detect import detect_language, language_stats
from docstoolkit.lang.i18n import t, set_locale, get_locale, available_locales
from docstoolkit.lang.readability import readability_score, syllables_estimate

__all__ = [
    "detect_language", "language_stats",
    "t", "set_locale", "get_locale", "available_locales",
    "readability_score", "syllables_estimate",
]
