"""Main parser combining extraction and validation."""

from __future__ import annotations

from dataclasses import dataclass, field

from docstoolkit.structured_output.extractor import ExtractionResult, StructuredExtractor
from docstoolkit.structured_output.schema import OutputSchema
from docstoolkit.structured_output.validator import OutputValidator, ValidationError


@dataclass
class ParseConfig:
    """Configuration for the StructuredOutputParser."""

    try_json: bool = True
    try_markdown_table: bool = True
    try_key_value: bool = True
    strict: bool = False


@dataclass
class ParseResult:
    """Result of a full parse (extraction + validation)."""

    extracted: ExtractionResult
    validated: list[ValidationError]
    schema_name: str

    def is_success(self) -> bool:
        """Return True if extraction is complete and no validation errors exist."""
        return self.extracted.is_complete() and len(self.validated) == 0


class StructuredOutputParser:
    """Parse unstructured text into validated structured data.

    Tries extraction methods in order (JSON → Markdown table → key-value)
    and validates the result against the provided schema.
    """

    def __init__(self, schema: OutputSchema, config: ParseConfig | None = None) -> None:
        self.schema = schema
        self.config = config if config is not None else ParseConfig()
        self._extractor = StructuredExtractor()
        self._validator = OutputValidator()

    def parse(self, text: str) -> ParseResult:
        """Parse text and validate against schema.

        Tries enabled extraction strategies in order:
          1. JSON object extraction
          2. Markdown table (uses first row as single record)
          3. Key-value lines

        Returns a ParseResult with the best attempt found.
        """
        data: dict = {}
        parse_errors: list[str] = []
        extraction_method = "none"

        if self.config.try_json:
            json_data = self._extractor.extract_json(text)
            if json_data is not None:
                data = json_data
                extraction_method = "json"

        if not data and self.config.try_markdown_table:
            rows = self._extractor.extract_markdown_table(text)
            if rows:
                # Use the first row as the data record
                data = rows[0]
                extraction_method = "markdown_table"

        if not data and self.config.try_key_value:
            kv_data = self._extractor.extract_key_value(text)
            if kv_data:
                data = kv_data
                extraction_method = "key_value"

        # Determine missing required fields
        required_names = {f.name for f in self.schema.required_fields()}
        missing_fields = [name for name in required_names if name not in data]

        # Apply defaults for optional fields that are absent
        for f in self.schema.optional_fields():
            if f.name not in data and f.default is not None:
                data[f.name] = f.default

        extraction_result = ExtractionResult(
            data=data,
            missing_fields=missing_fields,
            parse_errors=parse_errors,
            raw_text=text,
        )

        # Validate (skip validation of fields with errors already)
        validation_errors = self._validator.validate(data, self.schema)

        return ParseResult(
            extracted=extraction_result,
            validated=validation_errors,
            schema_name=self.schema.name,
        )
