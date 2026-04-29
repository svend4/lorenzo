"""Читаемость для русского и английского.

Flesch-Kincaid Reading Ease для разных языков:
  - en: 206.835 - 1.015 × (words/sentences) - 84.6 × (syllables/words)
  - ru: 206.835 - 1.3 × (words/sentences) - 60.1 × (syllables/words)
    (по Оборневой, 2006 — адаптация для русского)

Возвращает score 0-100:
  90-100: very easy (5th grade)
  60-70:  standard (8-9th grade)
  30-50:  difficult (university)
  0-30:   very difficult (academic)
"""
import re


_RU_VOWELS = "аеёиоуыэюя"
_EN_VOWELS = "aeiouy"


def syllables_estimate(word: str, lang: str = "en") -> int:
    """Оценка слогов в слове."""
    word = word.lower().strip()
    if not word:
        return 0

    vowels = _RU_VOWELS if lang == "ru" else _EN_VOWELS
    count = 0
    prev_vowel = False
    for ch in word:
        is_vowel = ch in vowels
        if is_vowel and not prev_vowel:
            count += 1
        prev_vowel = is_vowel

    # en: убираем silent 'e' в конце
    if lang == "en" and word.endswith("e") and count > 1:
        count -= 1

    return max(count, 1)


def _split_sentences(text: str) -> list[str]:
    sentences = re.split(r'[.!?]+\s+', text)
    return [s.strip() for s in sentences if len(s.strip()) > 5]


def _split_words(text: str, lang: str = "en") -> list[str]:
    if lang == "ru":
        return re.findall(r'[а-яё]+', text.lower())
    return re.findall(r'[a-z]+', text.lower())


def readability_score(text: str, lang: str = "auto") -> dict:
    """Возвращает {score, grade_level, words, sentences, avg_syllables}.

    lang: "ru" | "en" | "auto" (auto-detect через detect_language).
    """
    if lang not in ("ru", "en"):
        from docstoolkit.lang.detect import detect_language
        detected = detect_language(text)
        lang = "ru" if detected == "ru" else "en"

    sentences = _split_sentences(text)
    words = _split_words(text, lang)
    n_sent = len(sentences)
    n_words = len(words)
    if n_words == 0 or n_sent == 0:
        return {"score": 0, "grade_level": "?", "words": 0, "sentences": 0,
                "avg_syllables": 0, "lang": lang}

    syllables = sum(syllables_estimate(w, lang) for w in words)
    avg_syl = syllables / n_words
    asl = n_words / n_sent  # avg sentence length

    if lang == "ru":
        score = 206.835 - 1.3 * asl - 60.1 * avg_syl
    else:
        score = 206.835 - 1.015 * asl - 84.6 * avg_syl

    score = max(0, min(100, score))

    if score >= 90:
        grade = "очень легко" if lang == "ru" else "very easy"
    elif score >= 70:
        grade = "легко" if lang == "ru" else "easy"
    elif score >= 50:
        grade = "стандарт" if lang == "ru" else "standard"
    elif score >= 30:
        grade = "сложно" if lang == "ru" else "difficult"
    else:
        grade = "очень сложно" if lang == "ru" else "very difficult"

    return {
        "score": round(score, 1),
        "grade_level": grade,
        "words": n_words,
        "sentences": n_sent,
        "avg_syllables": round(avg_syl, 2),
        "lang": lang,
    }
