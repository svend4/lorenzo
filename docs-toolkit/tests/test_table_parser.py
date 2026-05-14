"""Tests for the table_parser module — ≥45 tests."""
from __future__ import annotations

import dataclasses

import pytest

from docstoolkit.table_parser import Table, TableCell, TableParser, TableRow


# ---------------------------------------------------------------------------
# Fixtures / helpers
# ---------------------------------------------------------------------------

SIMPLE_TABLE = """\
| Name   | Age | City    |
|--------|-----|---------|
| Alice  | 30  | London  |
| Bob    | 25  | Paris   |
| Carol  | 35  | Berlin  |
"""

SINGLE_COL_TABLE = """\
| Item    |
|---------|
| Apple   |
| Banana  |
"""

HEADER_ONLY_TABLE = """\
| X | Y | Z |
|---|---|---|
"""

MULTISPACE_TABLE = """\
|  First Name  |  Last Name  |
|-------------|-------------|
|  John       |  Doe        |
|  Jane       |  Smith      |
"""

TWO_TABLES_TEXT = """\
Some intro text.

| Col1 | Col2 |
|------|------|
| a    | b    |
| c    | d    |

Middle text.

| X | Y | Z |
|---|---|---|
| 1 | 2 | 3 |
"""

NO_TABLE_TEXT = """\
Just plain text.
No pipes here at all.
The end.
"""

ALIGNED_SEP_TABLE = """\
| Left | Center | Right |
|:-----|:------:|------:|
| L1   | C1     | R1    |
| L2   | C2     | R2    |
"""


def _make_simple_table() -> Table:
    parser = TableParser()
    return parser.parse_first(SIMPLE_TABLE)


# ===========================================================================
# 1. TestTableDataclass
# ===========================================================================

class TestTableDataclass:
    def test_row_count_simple(self):
        t = _make_simple_table()
        assert t.row_count == 3

    def test_row_count_header_only(self):
        parser = TableParser()
        t = parser.parse_first(HEADER_ONLY_TABLE)
        assert t.row_count == 0

    def test_col_count_simple(self):
        t = _make_simple_table()
        assert t.col_count == 3

    def test_col_count_single_col(self):
        parser = TableParser()
        t = parser.parse_first(SINGLE_COL_TABLE)
        assert t.col_count == 1

    def test_get_column_values(self):
        t = _make_simple_table()
        assert t.get_column("Name") == ["Alice", "Bob", "Carol"]

    def test_get_column_age(self):
        t = _make_simple_table()
        assert t.get_column("Age") == ["30", "25", "35"]

    def test_get_column_missing_raises(self):
        t = _make_simple_table()
        with pytest.raises(KeyError):
            t.get_column("NonExistent")

    def test_get_row_zero(self):
        t = _make_simple_table()
        assert t.get_row(0) == ["Alice", "30", "London"]

    def test_get_row_last(self):
        t = _make_simple_table()
        assert t.get_row(2) == ["Carol", "35", "Berlin"]

    def test_headers_list(self):
        t = _make_simple_table()
        assert t.headers == ["Name", "Age", "City"]

    def test_line_start_is_one_based(self):
        t = _make_simple_table()
        # SIMPLE_TABLE starts on line 1
        assert t.line_start == 1

    def test_table_is_dataclass(self):
        assert dataclasses.is_dataclass(Table)

    def test_tablerow_is_dataclass(self):
        assert dataclasses.is_dataclass(TableRow)

    def test_tablecell_is_dataclass(self):
        assert dataclasses.is_dataclass(TableCell)

    def test_cell_attributes(self):
        t = _make_simple_table()
        cell = t.rows[0].cells[0]
        assert cell.value == "Alice"
        assert cell.column == 0
        assert cell.row == 0

    def test_cell_column_index(self):
        t = _make_simple_table()
        city_cell = t.rows[0].cells[2]
        assert city_cell.column == 2

    def test_row_is_not_header(self):
        t = _make_simple_table()
        for row in t.rows:
            assert row.is_header is False


# ===========================================================================
# 2. TestToDictList
# ===========================================================================

class TestToDictList:
    def test_length(self):
        t = _make_simple_table()
        result = t.to_dict_list()
        assert len(result) == 3

    def test_first_row_keys(self):
        t = _make_simple_table()
        assert set(t.to_dict_list()[0].keys()) == {"Name", "Age", "City"}

    def test_first_row_values(self):
        t = _make_simple_table()
        assert t.to_dict_list()[0] == {"Name": "Alice", "Age": "30", "City": "London"}

    def test_last_row_values(self):
        t = _make_simple_table()
        assert t.to_dict_list()[-1] == {"Name": "Carol", "Age": "35", "City": "Berlin"}

    def test_empty_table_gives_empty_list(self):
        parser = TableParser()
        t = parser.parse_first(HEADER_ONLY_TABLE)
        assert t.to_dict_list() == []


# ===========================================================================
# 3. TestToCsv
# ===========================================================================

class TestToCsv:
    def test_csv_contains_headers(self):
        t = _make_simple_table()
        csv_text = t.to_csv()
        first_line = csv_text.splitlines()[0]
        assert "Name" in first_line
        assert "Age" in first_line
        assert "City" in first_line

    def test_csv_row_count(self):
        t = _make_simple_table()
        # header + 3 data rows
        lines = [l for l in t.to_csv().splitlines() if l.strip()]
        assert len(lines) == 4

    def test_csv_data_values(self):
        t = _make_simple_table()
        csv_text = t.to_csv()
        assert "Alice" in csv_text
        assert "London" in csv_text

    def test_csv_is_string(self):
        t = _make_simple_table()
        assert isinstance(t.to_csv(), str)


# ===========================================================================
# 4. TestParserBasic
# ===========================================================================

class TestParserBasic:
    def test_parse_returns_list(self):
        parser = TableParser()
        result = parser.parse(SIMPLE_TABLE)
        assert isinstance(result, list)

    def test_parse_single_table(self):
        parser = TableParser()
        result = parser.parse(SIMPLE_TABLE)
        assert len(result) == 1

    def test_headers_parsed(self):
        parser = TableParser()
        t = parser.parse(SIMPLE_TABLE)[0]
        assert t.headers == ["Name", "Age", "City"]

    def test_data_row_count(self):
        parser = TableParser()
        t = parser.parse(SIMPLE_TABLE)[0]
        assert t.row_count == 3

    def test_values_stripped(self):
        parser = TableParser()
        t = parser.parse(MULTISPACE_TABLE)[0]
        assert t.rows[0].cells[0].value == "John"
        assert t.rows[0].cells[1].value == "Doe"

    def test_aligned_separator_parsed(self):
        """Alignment colons in separator are handled correctly."""
        parser = TableParser()
        t = parser.parse_first(ALIGNED_SEP_TABLE)
        assert t is not None
        assert t.row_count == 2
        assert t.headers == ["Left", "Center", "Right"]

    def test_line_start_in_multiline_text(self):
        parser = TableParser()
        tables = parser.parse(TWO_TABLES_TEXT)
        # first table starts at line 3
        assert tables[0].line_start == 3


# ===========================================================================
# 5. TestParserMultipleTables
# ===========================================================================

class TestParserMultipleTables:
    def test_two_tables_found(self):
        parser = TableParser()
        result = parser.parse(TWO_TABLES_TEXT)
        assert len(result) == 2

    def test_first_table_headers(self):
        parser = TableParser()
        result = parser.parse(TWO_TABLES_TEXT)
        assert result[0].headers == ["Col1", "Col2"]

    def test_second_table_headers(self):
        parser = TableParser()
        result = parser.parse(TWO_TABLES_TEXT)
        assert result[1].headers == ["X", "Y", "Z"]

    def test_second_table_row_count(self):
        parser = TableParser()
        result = parser.parse(TWO_TABLES_TEXT)
        assert result[1].row_count == 1


# ===========================================================================
# 6. TestParserNoTable
# ===========================================================================

class TestParserNoTable:
    def test_no_table_returns_empty(self):
        parser = TableParser()
        assert parser.parse(NO_TABLE_TEXT) == []

    def test_empty_string_returns_empty(self):
        parser = TableParser()
        assert parser.parse("") == []

    def test_whitespace_only_returns_empty(self):
        parser = TableParser()
        assert parser.parse("   \n\n   ") == []


# ===========================================================================
# 7. TestParseFirst
# ===========================================================================

class TestParseFirst:
    def test_parse_first_returns_table(self):
        parser = TableParser()
        t = parser.parse_first(SIMPLE_TABLE)
        assert isinstance(t, Table)

    def test_parse_first_returns_none_on_no_table(self):
        parser = TableParser()
        assert parser.parse_first(NO_TABLE_TEXT) is None

    def test_parse_first_returns_first_of_two(self):
        parser = TableParser()
        t = parser.parse_first(TWO_TABLES_TEXT)
        assert t.headers == ["Col1", "Col2"]


# ===========================================================================
# 8. TestToMarkdown
# ===========================================================================

class TestToMarkdown:
    def test_to_markdown_returns_string(self):
        parser = TableParser()
        t = _make_simple_table()
        assert isinstance(parser.to_markdown(t), str)

    def test_to_markdown_contains_headers(self):
        parser = TableParser()
        md = parser.to_markdown(_make_simple_table())
        assert "Name" in md
        assert "Age" in md
        assert "City" in md

    def test_to_markdown_contains_separator(self):
        parser = TableParser()
        md = parser.to_markdown(_make_simple_table())
        lines = md.splitlines()
        assert any('---' in l for l in lines)

    def test_to_markdown_contains_data(self):
        parser = TableParser()
        md = parser.to_markdown(_make_simple_table())
        assert "Alice" in md
        assert "London" in md

    def test_roundtrip_parse_markdown_parse(self):
        """parse → to_markdown → parse should preserve structure."""
        parser = TableParser()
        original = _make_simple_table()
        md = parser.to_markdown(original)
        recovered = parser.parse_first(md)
        assert recovered is not None
        assert recovered.headers == original.headers
        assert recovered.row_count == original.row_count
        assert recovered.get_row(0) == original.get_row(0)

    def test_roundtrip_values_preserved(self):
        parser = TableParser()
        original = _make_simple_table()
        md = parser.to_markdown(original)
        recovered = parser.parse_first(md)
        assert recovered.to_dict_list() == original.to_dict_list()


# ===========================================================================
# 9. TestFilterRows
# ===========================================================================

class TestFilterRows:
    def test_filter_returns_table(self):
        parser = TableParser()
        t = _make_simple_table()
        result = parser.filter_rows(t, "Name", "Alice")
        assert isinstance(result, Table)

    def test_filter_single_match(self):
        parser = TableParser()
        t = _make_simple_table()
        result = parser.filter_rows(t, "Name", "Alice")
        assert result.row_count == 1
        assert result.get_row(0)[0] == "Alice"

    def test_filter_no_match(self):
        parser = TableParser()
        t = _make_simple_table()
        result = parser.filter_rows(t, "Name", "Zara")
        assert result.row_count == 0

    def test_filter_headers_preserved(self):
        parser = TableParser()
        t = _make_simple_table()
        result = parser.filter_rows(t, "City", "Paris")
        assert result.headers == t.headers

    def test_filter_multiple_matches(self):
        parser = TableParser()
        t = _make_simple_table()
        # Add duplicate city
        t2 = parser.add_row(t, ["Dave", "28", "London"])
        result = parser.filter_rows(t2, "City", "London")
        assert result.row_count == 2

    def test_filter_bad_column_raises(self):
        parser = TableParser()
        t = _make_simple_table()
        with pytest.raises(KeyError):
            parser.filter_rows(t, "NoSuchCol", "x")


# ===========================================================================
# 10. TestSortRows
# ===========================================================================

class TestSortRows:
    def test_sort_returns_table(self):
        parser = TableParser()
        t = _make_simple_table()
        result = parser.sort_rows(t, "Name")
        assert isinstance(result, Table)

    def test_sort_ascending(self):
        parser = TableParser()
        t = _make_simple_table()
        result = parser.sort_rows(t, "Name")
        names = result.get_column("Name")
        assert names == sorted(names)

    def test_sort_descending(self):
        parser = TableParser()
        t = _make_simple_table()
        result = parser.sort_rows(t, "Name", reverse=True)
        names = result.get_column("Name")
        assert names == sorted(names, reverse=True)

    def test_sort_preserves_row_count(self):
        parser = TableParser()
        t = _make_simple_table()
        result = parser.sort_rows(t, "Age")
        assert result.row_count == t.row_count

    def test_sort_preserves_headers(self):
        parser = TableParser()
        t = _make_simple_table()
        result = parser.sort_rows(t, "City")
        assert result.headers == t.headers

    def test_sort_bad_column_raises(self):
        parser = TableParser()
        t = _make_simple_table()
        with pytest.raises(KeyError):
            parser.sort_rows(t, "NoPeek")


# ===========================================================================
# 11. TestAddRow
# ===========================================================================

class TestAddRow:
    def test_add_row_increases_count(self):
        parser = TableParser()
        t = _make_simple_table()
        t2 = parser.add_row(t, ["Dave", "40", "Rome"])
        assert t2.row_count == t.row_count + 1

    def test_add_row_values_correct(self):
        parser = TableParser()
        t = _make_simple_table()
        t2 = parser.add_row(t, ["Dave", "40", "Rome"])
        assert t2.get_row(-1) == ["Dave", "40", "Rome"]

    def test_add_row_does_not_mutate_original(self):
        parser = TableParser()
        t = _make_simple_table()
        original_count = t.row_count
        parser.add_row(t, ["Dave", "40", "Rome"])
        assert t.row_count == original_count

    def test_add_row_headers_unchanged(self):
        parser = TableParser()
        t = _make_simple_table()
        t2 = parser.add_row(t, ["Dave", "40", "Rome"])
        assert t2.headers == t.headers

    def test_add_row_pads_short_values(self):
        parser = TableParser()
        t = _make_simple_table()
        t2 = parser.add_row(t, ["Eve"])  # only 1 of 3 values
        row = t2.get_row(-1)
        assert row[0] == "Eve"
        assert row[1] == ""
        assert row[2] == ""


# ===========================================================================
# 12. TestAddColumn
# ===========================================================================

class TestAddColumn:
    def test_add_column_increases_col_count(self):
        parser = TableParser()
        t = _make_simple_table()
        t2 = parser.add_column(t, "Country", ["UK", "FR", "DE"])
        assert t2.col_count == t.col_count + 1

    def test_add_column_new_header(self):
        parser = TableParser()
        t = _make_simple_table()
        t2 = parser.add_column(t, "Country", ["UK", "FR", "DE"])
        assert "Country" in t2.headers

    def test_add_column_values(self):
        parser = TableParser()
        t = _make_simple_table()
        t2 = parser.add_column(t, "Country", ["UK", "FR", "DE"])
        assert t2.get_column("Country") == ["UK", "FR", "DE"]

    def test_add_column_does_not_mutate_original(self):
        parser = TableParser()
        t = _make_simple_table()
        original_col_count = t.col_count
        parser.add_column(t, "Country", ["UK", "FR", "DE"])
        assert t.col_count == original_col_count

    def test_add_column_short_values_padded(self):
        parser = TableParser()
        t = _make_simple_table()
        t2 = parser.add_column(t, "Score", ["10"])  # only 1 value for 3 rows
        vals = t2.get_column("Score")
        assert vals[0] == "10"
        assert vals[1] == ""
        assert vals[2] == ""

    def test_add_column_extra_values_truncated(self):
        parser = TableParser()
        t = _make_simple_table()
        t2 = parser.add_column(t, "Extra", ["a", "b", "c", "d", "e"])
        assert t2.get_column("Extra") == ["a", "b", "c"]


# ===========================================================================
# 13. TestEdgeCases
# ===========================================================================

class TestEdgeCases:
    def test_header_only_table_row_count_zero(self):
        parser = TableParser()
        t = parser.parse_first(HEADER_ONLY_TABLE)
        assert t is not None
        assert t.row_count == 0

    def test_header_only_col_count(self):
        parser = TableParser()
        t = parser.parse_first(HEADER_ONLY_TABLE)
        assert t.col_count == 3

    def test_header_only_to_dict_list_empty(self):
        parser = TableParser()
        t = parser.parse_first(HEADER_ONLY_TABLE)
        assert t.to_dict_list() == []

    def test_single_column_table(self):
        parser = TableParser()
        t = parser.parse_first(SINGLE_COL_TABLE)
        assert t is not None
        assert t.col_count == 1
        assert t.row_count == 2

    def test_single_column_values(self):
        parser = TableParser()
        t = parser.parse_first(SINGLE_COL_TABLE)
        assert t.get_column("Item") == ["Apple", "Banana"]

    def test_spaces_in_values_stripped(self):
        parser = TableParser()
        t = parser.parse_first(MULTISPACE_TABLE)
        assert t.rows[0].cells[0].value == "John"

    def test_table_in_larger_document(self):
        text = "# Title\n\nSome paragraph.\n\n" + SIMPLE_TABLE + "\nMore text.\n"
        parser = TableParser()
        tables = parser.parse(text)
        assert len(tables) == 1
        assert tables[0].headers == ["Name", "Age", "City"]

    def test_filter_returns_new_table_instance(self):
        parser = TableParser()
        t = _make_simple_table()
        t2 = parser.filter_rows(t, "Name", "Alice")
        assert t2 is not t

    def test_sort_returns_new_table_instance(self):
        parser = TableParser()
        t = _make_simple_table()
        t2 = parser.sort_rows(t, "Name")
        assert t2 is not t

    def test_add_row_returns_new_table_instance(self):
        parser = TableParser()
        t = _make_simple_table()
        t2 = parser.add_row(t, ["X", "1", "Y"])
        assert t2 is not t

    def test_add_column_returns_new_table_instance(self):
        parser = TableParser()
        t = _make_simple_table()
        t2 = parser.add_column(t, "Extra", [])
        assert t2 is not t
