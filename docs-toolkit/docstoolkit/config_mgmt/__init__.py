"""Config management module — sources, manager, and validator."""
from docstoolkit.config_mgmt.source import (
    ConfigSource,
    DictSource,
    EnvSource,
    IniFileSource,
    JsonFileSource,
)
from docstoolkit.config_mgmt.manager import ConfigManager
from docstoolkit.config_mgmt.validator import ConfigRule, ConfigValidator

__all__ = [
    # Sources
    "ConfigSource",
    "DictSource",
    "EnvSource",
    "JsonFileSource",
    "IniFileSource",
    # Manager
    "ConfigManager",
    # Validator
    "ConfigRule",
    "ConfigValidator",
]
