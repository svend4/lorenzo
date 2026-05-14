"""table_parser — parse and manipulate markdown tables (stdlib only)."""
from __future__ import annotations

import csv
import io
import re
from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class TableCell:
    """A single cell in a markdown table."""
    value: str
    column: int
    row: int


@dataclass
class TableRow:
    """A single row in a markdown table."""
    cells: list[TableCell]
    row_num: int
    is_header: bool = False


@dataclass
class Table:
    """Parsed markdown table."""
    headers: list[str]
    rows: list[TableRow]
    line_start: int = 1  # 1-based line number where the table starts

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def row_count(self) -> int:
        """Number of data rows (excludes header)."""
        return len(self.rows)

    @property
    def col_count(self) -> int:
        """Number of columns."""
        return len(self.headers)

    # ------------------------------------------------------------------
    # Access helpers
    # ------------------------------------------------------------------

    def get_column(self, name: str) -> list[str]:
        """Return all values in the named column."""
        if name not in self.headers:
            raise KeyError(f"Column {name!r} not found in table headers")
        col_idx = self.headers.index(name)
        return [
            row.cells[col_idx].value if col_idx < len(row.cells) else ""
            for row in self.rows
        ]

    def get_row(self, index: int) -> list[str]:
        """Return cell values of the data row at *index* (0-based)."""
        row = self.rows[index]
        return [cell.value for cell in row.cells]

    # ------------------------------------------------------------------
    # Serialisation
    # ------------------------------------------------------------------

    def to_dict_list(self) -> list[dict]:
        """Return each data row as {header: value}."""
        result = []
        for row in self.rows:
            d: dict[str, str] = {}
            for col_idx, header in enumerate(self.headers):
                d[header] = row.cells[col_idx].value if col_idx < len(row.cells) else ""
            result.append(d)
        return result

    def to_csv(self) -> str:
        """Return CSV representation of the table."""
        buf = io.StringIO()
        writer = csv.writer(buf)
        writer.writerow(self.headers)
        for row in self.rows:
            writer.writerow([cell.value for cell in row.cells])
        return buf.getvalue()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_SEPARATOR_RE = re.compile(r'^\s*\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)*\|?\s*$')


def _is_separator_row(line: str) -> bool:
    """Return True if *line* is a markdown table separator row."""
    return bool(_SEPARATOR_RE.match(line))


def _split_cells(line: str) -> list[str]:
    """Split a markdown table row into stripped cell values."""
    # strip optional leading/trailing pipes
    stripped = line.strip()
    if stripped.startswith('|'):
        stripped = stripped[1:]
    if stripped.endswith('|'):
        stripped = stripped[:-1]
    return [cell.strip() for cell in stripped.split('|')]


def _is_table_row(line: str) -> bool:
    """Return True if *line* looks like a markdown table row (contains |)."""
    return '|' in line


# ---------------------------------------------------------------------------
# Main parser
# ---------------------------------------------------------------------------

class TableParser:
    """Parse markdown tables from text."""

    # ------------------------------------------------------------------
    # Parsing
    # ------------------------------------------------------------------

    def parse(self, text: str) -> list[Table]:
        """Find and parse all markdown tables in *text*."""
        lines = text.splitlines()
        tables: list[Table] = []
        i = 0
        while i < len(lines):
            # look for a header row + separator pair
            if _is_table_row(lines[i]) and not _is_separator_row(lines[i]):
                # peek ahead: is the next non-empty line a separator?
                j = i + 1
                while j < len(lines) and lines[j].strip() == '':
                    j += 1
                if j < len(lines) and _is_separator_row(lines[j]):
                    # we found a table — collect header, separator, and data rows
                    header_line = lines[i]
                    line_start = i + 1  # 1-based
                    headers = _split_cells(header_line)

                    # advance past separator
                    k = j + 1
                    data_rows: list[TableRow] = []
                    row_num = 0
                    while k < len(lines) and _is_table_row(lines[k]) and not _is_separator_row(lines[k]):
                        cells_vals = _split_cells(lines[k])
                        # pad or truncate cells to match header count
                        while len(cells_vals) < len(headers):
                            cells_vals.append("")
                        cells_vals = cells_vals[:len(headers)]
                        cells = [
                            TableCell(value=v, column=col_idx, row=row_num)
                            for col_idx, v in enumerate(cells_vals)
                        ]
                        data_rows.append(TableRow(cells=cells, row_num=row_num, is_header=False))
                        row_num += 1
                        k += 1

                    tables.append(Table(headers=headers, rows=data_rows, line_start=line_start))
                    i = k
                    continue
            i += 1
        return tables

    def parse_first(self, text: str) -> Optional[Table]:
        """Return the first markdown table found in *text*, or None."""
        tables = self.parse(text)
        return tables[0] if tables else None

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------

    def to_markdown(self, table: Table) -> str:
        """Render *table* as a markdown string with a separator row."""
        # compute column widths
        col_widths = [max(3, len(h)) for h in table.headers]
        for row in table.rows:
            for col_idx, cell in enumerate(row.cells):
                if col_idx < len(col_widths):
                    col_widths[col_idx] = max(col_widths[col_idx], len(cell.value))

        def _fmt_row(values: list[str]) -> str:
            parts = [v.ljust(col_widths[i]) for i, v in enumerate(values)]
            return '| ' + ' | '.join(parts) + ' |'

        lines: list[str] = []
        lines.append(_fmt_row(table.headers))
        # separator
        sep_parts = ['-' * col_widths[i] for i in range(len(table.headers))]
        lines.append('| ' + ' | '.join(sep_parts) + ' |')
        for row in table.rows:
            values = [cell.value for cell in row.cells]
            # pad if needed
            while len(values) < len(table.headers):
                values.append("")
            lines.append(_fmt_row(values))
        return '\n'.join(lines) + '\n'

    # ------------------------------------------------------------------
    # Manipulation
    # ------------------------------------------------------------------

    def filter_rows(self, table: Table, column: str, value: str) -> Table:
        """Return a new Table containing only rows where *column* == *value*."""
        if column not in table.headers:
            raise KeyError(f"Column {column!r} not found")
        col_idx = table.headers.index(column)
        matching: list[TableRow] = []
        for new_row_num, row in enumerate(table.rows):
            cell_val = row.cells[col_idx].value if col_idx < len(row.cells) else ""
            if cell_val == value:
                new_cells = [
                    TableCell(value=c.value, column=c.column, row=new_row_num)
                    for c in row.cells
                ]
                matching.append(TableRow(cells=new_cells, row_num=new_row_num, is_header=False))
        return Table(headers=list(table.headers), rows=matching, line_start=table.line_start)

    def sort_rows(self, table: Table, column: str, reverse: bool = False) -> Table:
        """Return a new Table with rows sorted by *column* (string sort)."""
        if column not in table.headers:
            raise KeyError(f"Column {column!r} not found")
        col_idx = table.headers.index(column)

        def _key(row: TableRow) -> str:
            return row.cells[col_idx].value if col_idx < len(row.cells) else ""

        sorted_data = sorted(table.rows, key=_key, reverse=reverse)
        new_rows: list[TableRow] = []
        for new_row_num, row in enumerate(sorted_data):
            new_cells = [
                TableCell(value=c.value, column=c.column, row=new_row_num)
                for c in row.cells
            ]
            new_rows.append(TableRow(cells=new_cells, row_num=new_row_num, is_header=False))
        return Table(headers=list(table.headers), rows=new_rows, line_start=table.line_start)

    def add_row(self, table: Table, values: list[str]) -> Table:
        """Return a new Table with a new data row appended."""
        new_row_num = len(table.rows)
        # pad or truncate to match column count
        padded = list(values)
        while len(padded) < table.col_count:
            padded.append("")
        padded = padded[:table.col_count]
        cells = [
            TableCell(value=v, column=col_idx, row=new_row_num)
            for col_idx, v in enumerate(padded)
        ]
        new_row = TableRow(cells=cells, row_num=new_row_num, is_header=False)
        # rebuild existing rows with correct row numbers (they stay the same)
        new_rows = list(table.rows) + [new_row]
        return Table(headers=list(table.headers), rows=new_rows, line_start=table.line_start)

    def add_column(self, table: Table, name: str, values: list[str]) -> Table:
        """Return a new Table with a new column appended.

        If *values* is shorter than the row count the missing cells are filled
        with empty strings; extra values are silently truncated.
        """
        new_headers = list(table.headers) + [name]
        new_col_idx = len(table.headers)
        new_rows: list[TableRow] = []
        for row in table.rows:
            extra_val = values[row.row_num] if row.row_num < len(values) else ""
            new_cells = list(row.cells) + [
                TableCell(value=extra_val, column=new_col_idx, row=row.row_num)
            ]
            new_rows.append(TableRow(cells=new_cells, row_num=row.row_num, is_header=False))
        return Table(headers=new_headers, rows=new_rows, line_start=table.line_start)
