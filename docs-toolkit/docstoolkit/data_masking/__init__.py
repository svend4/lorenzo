"""E103 Data Masking module for docs-toolkit.

Provides stdlib-only field-level data masking and redaction for dicts:

  - ``MaskStrategy`` — enum of available strategies (REDACT, PARTIAL, HASH,
    NULLIFY, FIXED)
  - ``MaskRule``     — regex pattern + strategy + parameters for one rule
  - ``MaskConfig``   — collection of rules plus recursive/mask_keys flags
  - ``DataMasker``   — applies rules to dicts (or individual values)

Usage::

    from docstoolkit.data_masking import (
        DataMasker, MaskConfig, MaskRule, MaskStrategy,
    )

    masker = DataMasker(MaskConfig(rules=[
        MaskRule("password",  MaskStrategy.REDACT),
        MaskRule(".*_token",  MaskStrategy.HASH),
        MaskRule("email",     MaskStrategy.PARTIAL, partial_show=3),
        MaskRule("api_key",   MaskStrategy.FIXED,   fixed_value="<hidden>"),
        MaskRule("ssn",       MaskStrategy.NULLIFY),
    ]))

    result = masker.mask({
        "username": "alice",
        "password": "s3cr3t",
        "auth_token": "abc123xyz",
        "email": "alice@example.com",
    })
    # {
    #   "username": "alice",
    #   "password": "***",
    #   "auth_token": "<sha256-hex[:16]>",
    #   "email": "ali**************om",
    # }
"""
from docstoolkit.data_masking.masker import (
    MaskStrategy,
    MaskRule,
    MaskConfig,
    DataMasker,
)

__all__ = [
    "MaskStrategy",
    "MaskRule",
    "MaskConfig",
    "DataMasker",
]
