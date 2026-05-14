"""Structured output parser module for docs-toolkit.

Provides schema definition, extraction, validation and parsing of structured
data from LLM output text.

Example usage::

    from docstoolkit.structured_output import (
        FieldType, FieldSchema, OutputSchema,
        StructuredExtractor, ExtractionResult,
        OutputValidator, ValidationError,
        StructuredOutputParser, ParseConfig, ParseResult,
    )

    schema = OutputSchema(
        name="person",
        fields=[
            FieldSchema("name", FieldType.STRING),
            FieldSchema("age", FieldType.INTEGER),
            FieldSchema("email", FieldType.STRING, required=False, default=""),
        ],
    )
    parser = StructuredOutputParser(schema)
    result = parser.parse('{"name": "Alice", "age": "30"}')
    print(result.is_success())  # True
"""

from docstoolkit.structured_output.schema import FieldType, FieldSchema, OutputSchema
from docstoolkit.structured_output.extractor import ExtractionResult, StructuredExtractor
from docstoolkit.structured_output.validator import ValidationError, OutputValidator
from docstoolkit.structured_output.parser import (
    ParseConfig,
    ParseResult,
    StructuredOutputParser,
)

__all__ = [
    # schema
    "FieldType",
    "FieldSchema",
    "OutputSchema",
    # extractor
    "ExtractionResult",
    "StructuredExtractor",
    # validator
    "ValidationError",
    "OutputValidator",
    # parser
    "ParseConfig",
    "ParseResult",
    "StructuredOutputParser",
]
