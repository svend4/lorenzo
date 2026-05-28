---
date: 2026-05-28
tags: [rag, orchestration, security, ingestion, architecture]
state: normalized
---

# Design by Contract + LLM: формальные контракты для криптографии на STM32

<!-- toc-auto -->
<!-- tags: miller83-design-by-contract-llm-crypto-hardware, docs -->


<!-- summary -->
> `miller83-design-by-contract-llm-crypto-hardware` — раздел документации проекта Lorenzo.


> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Автор:** Miller83 (Сергей Васильев)  
**Хабр:** https://habr.com/ru/articles/1025244/  
**GitHub:** github.com/vasilievsv/hw.pki-on-box  
**Слой:** orchestration / knowledge  
**Дата:** апрель 2026  
**Уникальность:** Единственная Хабр-статья 2026 года где LLM используется не для генерации кода, а как **реализатор формальных спецификаций**: 10-строчные YAML-контракты (PRE/POST/INV) → LLM генерирует имплементацию + параллельный набор contract-validation тестов. PKI-система на STM32/RK3328 (ARM64): HMAC-DRBG, RSA-PSS/ECDSA, AES-256-GCM, X.509+CRL. Поймано 2 критические уязвимости до продакшена (неправильный padding + не тот AES-режим), которые стандартные unit-тесты и компилятор пропустили.

## Проблема: LLM генерирует код, который компилируется, но небезопасен

```
Стандартный AI-assisted dev:
  Промпт: "напиши RSA-шифрование"
  → LLM: код компилируется ✓, тесты проходят ✓, работает ✓
  → Но: использует PKCS#1 v1.5 padding вместо PSS ❌
         (PKCS#1 v1.5 уязвим к padding oracle attacks с 1998!)
  → Компилятор: ОК
  → Unit-тест: ОК (тест проверяет "шифрует/дешифрует?", не "какой padding?")

Design by Contract (Бертран Мейер, 1986):
  Контракт = PRE + POST + INV
  PRE: что должно быть истинно ДО вызова (предусловие)
  POST: что должно быть истинно ПОСЛЕ (постусловие)
  INV: что должно быть истинно всегда (инвариант класса)

  RSA-контракт:
  PRE:  padding IN {RSA-PSS, RSA-OAEP}
  POST: output_len == key_len_bytes
  INV:  PKCS1_v15 NOT IN used_paddings  ← явный запрет!

Miller83 паттерн:
  10 строк YAML-контракта → LLM генерирует:
    1. Имплементацию, удовлетворяющую контракту
    2. Тесты, верифицирующие контракт
  → Контракты поймали то, что unit-тесты пропустили
```

## Архитектура Contract-Driven LLM Development

```python
# Miller83: Design by Contract + LLM для PKI
# habr.com/ru/articles/1025244/
# github.com/vasilievsv/hw.pki-on-box

from dataclasses import dataclass, field
from typing import Any
import yaml

@dataclass
class FormalContract:
    """
    Формальный контракт в стиле Мейера для одного модуля.

    Ключевое: контракт пишет ЧЕЛОВЕК (10 строк YAML).
    LLM читает контракт и пишет:
    1. Имплементацию, соответствующую PRE/POST/INV
    2. Тесты, верифицирующие PRE/POST/INV

    Выгода: LLM-агент получает формальную спецификацию,
    а не ambiguous текстовый промпт.
    """
    module: str                    # имя модуля
    preconditions: list[str]       # что должно быть ДО вызова
    postconditions: list[str]      # что должно быть ПОСЛЕ вызова
    invariants: list[str]          # что должно быть ВСЕГДА
    forbidden: list[str] = field(default_factory=list)  # явные запреты
    nist_refs: list[str] = field(default_factory=list)  # стандарты (NIST SP 800-*)


# Пример контрактов из PKI-системы Miller83

RSA_CONTRACT = FormalContract(
    module="RSAEncryptor",
    preconditions=[
        "padding IN {RSA-PSS, RSA-OAEP}",
        "key_size >= 2048",
        "plaintext_len <= key_len - 2*hash_len - 2"
    ],
    postconditions=[
        "ciphertext_len == key_len_bytes",
        "decrypt(encrypt(m)) == m"
    ],
    invariants=[
        "private_key NEVER leaves secure enclave",
        "key_material NEVER in logs"
    ],
    forbidden=[
        "PKCS1_v15",          # уязвим к padding oracle (1998)
        "ECB_MODE",            # нет семантической безопасности
        "MD5", "SHA1"          # устаревшие хеш-функции
    ],
    nist_refs=["NIST SP 800-131A", "FIPS 186-5"]
)

AES_CONTRACT = FormalContract(
    module="AESKeyStorage",
    preconditions=[
        "mode IN {GCM, CCM}",  # аутентифицированное шифрование
        "key_size == 256",
        "nonce_len == 12"       # GCM рекомендует 96 бит
    ],
    postconditions=[
        "output INCLUDES authentication_tag",
        "authentication_tag_len == 16"
    ],
    invariants=[
        "nonce NEVER reused with same key",  # GCM nonce reuse → катастрофа
        "key NEVER stored in plaintext RAM"
    ],
    forbidden=[
        "AES-ECB", "AES-CBC",  # без аутентификации
        "CTR_without_MAC"       # уязвим к bit flipping
    ],
    nist_refs=["NIST SP 800-38D"]
)

ENTROPY_CONTRACT = FormalContract(
    module="EntropySource",
    preconditions=[
        "hardware_rng_available == True",
        "adc_noise_source_healthy == True"
    ],
    postconditions=[
        "entropy_rate >= 0.9 bits/bit",     # NIST 800-90B требование
        "output_len >= requested_bytes"
    ],
    invariants=[
        "HMAC-DRBG reseed_counter < 2^48",   # NIST 800-90A лимит
        "health_test_passed == True"
    ],
    forbidden=["time()", "rand()", "pseudo_random_only"],
    nist_refs=["NIST SP 800-90A", "NIST SP 800-90B"]
)


class ContractDrivenLLMDeveloper:
    """
    LLM-агент, который реализует код по формальному контракту.

    Отличие от обычного code generation:
    Обычно: "напиши RSA" → LLM импровизирует
    DbC: YAML-контракт → LLM генерирует код + тесты,
         которые механически проверяют каждое условие контракта

    Результат: тесты не проверяют "работает ли?",
               а проверяют "соответствует ли контракту?"
    """

    async def generate_module(self, contract: FormalContract) -> dict:
        """
        Сгенерировать реализацию + тесты по контракту.
        """
        contract_yaml = yaml.dump(contract.__dict__, allow_unicode=True)

        # Промпт: контракт как спецификация
        implementation_prompt = f"""Реализуй Python модуль, строго соответствующий этому контракту.

КОНТРАКТ (обязателен к выполнению):
{contract_yaml}

Требования:
1. Каждое precondition должно проверяться в начале метода (assert или raise)
2. Каждое postcondition должно проверяться перед return
3. Каждый invariant должен поддерживаться всеми методами класса
4. forbidden — использование ЗАПРЕЩЕНО, даже если "работает"
5. Ссылки nist_refs — реализация должна соответствовать этим стандартам

Сгенерируй:
a) Реализацию класса {contract.module}
b) Набор contract-тестов (по одному тесту на каждое условие)"""

        implementation = await self.llm.generate(implementation_prompt)

        # Тесты специфически проверяют контракт
        test_prompt = f"""Для модуля {contract.module} с контрактом:
{contract_yaml}

Сгенерируй тесты, которые верифицируют КАЖДОЕ условие контракта:
- test_precondition_X для каждого precondition
- test_postcondition_X для каждого postcondition
- test_forbidden_X для каждого forbidden (убедиться что НЕЛЬЗЯ использовать)
- test_invariant_X для каждого invariant

Тесты должны ПАДАТЬ если контракт нарушен."""

        tests = await self.llm.generate(test_prompt)

        return {
            "implementation": implementation,
            "contract_tests": tests,
            "contract": contract
        }


# Два пойманных уязвимости (production-блокеры)
CAUGHT_VULNERABILITIES = [
    {
        "модуль": "RSAEncryptor",
        "ошибка": "Неправильный padding",
        "что_было": "PKCS#1 v1.5 (дефолт в большинстве библиотек)",
        "что_должно": "RSA-PSS (требование контракта)",
        "почему_опасно": "Padding oracle attack (Bleichenbacher 1998) → расшифровка без ключа",
        "как_поймали": "test_forbidden_PKCS1_v15 упал → ошибка найдена до продакшена",
        "стандартный_тест": "ПРОПУСТИЛ (тест проверял encrypt/decrypt roundtrip, не padding)"
    },
    {
        "модуль": "AESKeyStorage",
        "ошибка": "Неправильный режим AES",
        "что_было": "AES-CBC (архитектурно валиден, но нет аутентификации)",
        "что_должно": "AES-GCM (требование контракта: mode IN {GCM, CCM})",
        "почему_опасно": "CBC без MAC → bit flipping attack, нет защиты целостности",
        "как_поймали": "test_forbidden_AES_CBC упал → ошибка найдена до продакшена",
        "стандартный_тест": "ПРОПУСТИЛ (тест проверял шифрование/расшифровку, не режим)"
    }
]

SYSTEM_STATS = {
    "платформа": ["STM32 (ARM Cortex-M)", "RK3328 (ARM64)"],
    "стек_криптографии": {
        "rng": "HMAC-DRBG (NIST SP 800-90A) + ADC thermal noise (NIST 800-90B)",
        "asymmetric": "RSA-PSS, RSA-OAEP, ECDSA",
        "symmetric": "AES-256-GCM",
        "pki": "X.509 + CRL"
    },
    "метрики_разработки": {
        "контракт_тестов": 62,
        "hardware_тестов": 15,
        "nist_аудит_точек": "12/12 закрыто",
        "коммитов": 131,
        "дней_разработки": 11,
        "стоимость_compute": "~$16 (≈1780₽)",
        "стоимость_железа": "~$129"
    }
}
```

## Применение к Lorenzo

```python
# Lorenzo: Contract-Driven development для gateway.py и scripts/

class LorenzoContractSpec:
    """
    Miller83 паттерн для Lorenzo:
    Формальные контракты для критических компонентов.

    Пример: gateway.py /api/cards endpoint

    CONTRACT для add_card():
    PRE:
      - content_len IN [100, 10000]
      - section IN VALID_SECTIONS
      - title NOT empty
    POST:
      - card_id != None
      - search_index UPDATED
      - review_queue HAS new_entry IF content_len > 5000
    INV:
      - duplicate_titles FORBIDDEN
      - total_cards <= 50000
    FORBIDDEN:
      - SQL injection patterns in title/content
      - Empty body cards

    Выгода: LLM-ассистент при добавлении нового эндпоинта
    читает контракт → генерирует имплементацию + тесты.
    """
    pass
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **DbC + SENTINEL (R47)** | Контракты как формальная спецификация безопасности для SENTINEL детекторов: INV = "prompt injection NOT в input" |
| **DbC + Agent Evaluation (R48)** | Golden Set = contract tests: каждый тест-кейс = одно условие контракта → формальная верификация агентного поведения |
| **DbC + LangGraph (R44)** | LangGraph узлы с контрактами: PRE-условие проверяется перед входом в узел, POST — после выхода |
| **DbC + LLM Observability (R45)** | Трейсинг нарушений контракта: когда LLM-генерация нарушает invariant → alert в observability стеке |
| **DbC + GBNF (R49)** | GBNF как синтаксический контракт (структура вывода) + DbC как семантический (правила домена) = двухуровневая верификация |

## Контакт

- Статья: https://habr.com/ru/articles/1025244/ (апрель 2026)
- Автор: Miller83 (Сергей Васильев, Habr)
- GitHub: github.com/vasilievsv/hw.pki-on-box
- Design by Contract: Bertrand Meyer, "Object-Oriented Software Construction" (1988)
- NIST SP 800-90A/B: csrc.nist.gov (DRBG + entropy source требования)
- Смежная (SENTINEL безопасность, R47): docs/06-discovery/round-47/projects/dmitriila-sentinel-llm-immune-system-3ms.md
- Смежная (LLM code review v2, R33): docs/06-discovery/round-33/
- Смежная (LLM AppSec, R22): docs/06-discovery/round-22/

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
- [Решения](../../../DECISIONS.md)
