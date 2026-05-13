"""Config validation — rules and ConfigValidator."""
from dataclasses import dataclass, field


@dataclass
class ConfigRule:
    """Describes a single validation rule for one config key.

    Parameters
    ----------
    key:
        Dot-notation key to validate (e.g. ``"db.host"``).
    required:
        If ``True`` and the key is absent, an error is produced.
    type_:
        If given, the resolved value must be an instance of this type.
        ``None`` skips the type check.
    validator:
        Optional callable ``(value) -> bool``.  Called only when the key
        is present.  Should return ``True`` if valid, ``False`` otherwise.
    description:
        Human-readable description used in error messages.
    """

    key: str
    required: bool = False
    type_: type = None
    validator: callable = None
    description: str = ""


_SENTINEL = object()  # distinct from None for "key absent" detection


class ConfigValidator:
    """Validates a :class:`~docstoolkit.config_mgmt.manager.ConfigManager`
    against a set of :class:`ConfigRule` objects.

    Usage::

        v = ConfigValidator([
            ConfigRule("db.host", required=True, type_=str),
            ConfigRule("db.port", required=True, type_=int,
                       validator=lambda p: 1 <= p <= 65535),
        ])
        errors = v.validate(manager)
        if errors:
            raise SystemExit("\\n".join(errors))
    """

    def __init__(self, rules: list = None) -> None:
        self._rules: list[ConfigRule] = list(rules) if rules else []

    def add_rule(self, rule: ConfigRule) -> None:
        """Append *rule* to the validator."""
        self._rules.append(rule)

    def validate(self, config) -> list:
        """Run all rules against *config* (a ``ConfigManager``).

        Returns a list of error strings.  An empty list means all rules
        passed.

        Checks performed for each rule (in order):
        1. **required** — key must be present (not ``None``).
        2. **type_** — value must be an instance of the given type.
        3. **validator** — custom callable must return truthy.
        """
        errors: list[str] = []

        for rule in self._rules:
            value = config.get(rule.key, _SENTINEL)
            is_present = value is not _SENTINEL and value is not None

            # 1. Required check
            if rule.required and not is_present:
                desc = f" ({rule.description})" if rule.description else ""
                errors.append(f"Missing required config key: '{rule.key}'{desc}")
                # No point running further checks for an absent key
                continue

            # Skip type / validator checks for absent optional keys
            if not is_present:
                continue

            # 2. Type check
            if rule.type_ is not None and not isinstance(value, rule.type_):
                desc = f" ({rule.description})" if rule.description else ""
                errors.append(
                    f"Config key '{rule.key}' must be of type "
                    f"{rule.type_.__name__}, got {type(value).__name__}{desc}"
                )

            # 3. Custom validator
            if rule.validator is not None:
                try:
                    ok = rule.validator(value)
                except Exception as exc:  # noqa: BLE001
                    desc = f" ({rule.description})" if rule.description else ""
                    errors.append(
                        f"Config key '{rule.key}' validator raised an exception: "
                        f"{exc}{desc}"
                    )
                    continue
                if not ok:
                    desc = f" ({rule.description})" if rule.description else ""
                    errors.append(
                        f"Config key '{rule.key}' failed custom validation{desc}"
                    )

        return errors
