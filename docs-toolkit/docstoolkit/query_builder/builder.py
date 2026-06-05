"""Fluent SQL-like query builder that compiles to parameterized SQLite queries.

The :class:`QueryBuilder` provides a chainable API for assembling SELECT
statements (with JOIN / WHERE / GROUP BY / HAVING / ORDER BY / LIMIT / OFFSET
support) plus convenience methods for INSERT, UPDATE and DELETE.

Builders are reusable: ``reset()`` clears state and ``clone()`` produces an
independent copy.  ``build()`` returns ``(sql, params)`` for use with
``sqlite3``; ``to_sql()`` renders an inline representation that should only be
used for display/debugging.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, List, Optional, Tuple


class JoinType(Enum):
    """SQL JOIN types."""

    INNER = "INNER JOIN"
    LEFT = "LEFT JOIN"
    RIGHT = "RIGHT JOIN"
    FULL = "FULL JOIN"
    CROSS = "CROSS JOIN"


class OrderDir(Enum):
    """ORDER BY direction."""

    ASC = "ASC"
    DESC = "DESC"


_BINARY_OPS = {"=", "!=", "<", "<=", ">", ">=", "LIKE"}
_LIST_OPS = {"IN", "NOT IN"}
_RANGE_OPS = {"BETWEEN"}
_NULL_OPS = {"IS NULL", "IS NOT NULL"}
_ALL_OPS = _BINARY_OPS | _LIST_OPS | _RANGE_OPS | _NULL_OPS


@dataclass
class Condition:
    """A single WHERE/HAVING predicate."""

    column: str
    op: str
    value: Any = None

    def __post_init__(self) -> None:
        if self.op not in _ALL_OPS:
            raise ValueError(f"Unsupported operator: {self.op!r}")


@dataclass
class JoinClause:
    """A single JOIN clause."""

    join_type: JoinType
    table: str
    on: str


# Sentinel for OR groupings inside the WHERE list.
@dataclass
class _OrCondition:
    condition: Condition


def _render_condition(cond: Condition) -> Tuple[str, List[Any]]:
    """Render a Condition into a SQL fragment + parameter list."""

    op = cond.op
    if op in _BINARY_OPS:
        return f"{cond.column} {op} ?", [cond.value]
    if op in _LIST_OPS:
        values = list(cond.value) if cond.value is not None else []
        if not values:
            # SQLite rejects ``IN ()`` — emit a guaranteed false / true predicate
            if op == "IN":
                return "0", []
            return "1", []
        placeholders = ", ".join(["?"] * len(values))
        return f"{cond.column} {op} ({placeholders})", list(values)
    if op == "BETWEEN":
        low, high = cond.value
        return f"{cond.column} BETWEEN ? AND ?", [low, high]
    if op in _NULL_OPS:
        return f"{cond.column} {op}", []
    raise ValueError(f"Unsupported operator: {op!r}")  # pragma: no cover


def _format_literal(value: Any) -> str:
    """Render a Python value as a SQL literal (display only)."""

    if value is None:
        return "NULL"
    if isinstance(value, bool):
        return "1" if value else "0"
    if isinstance(value, (int, float)):
        return str(value)
    text = str(value).replace("'", "''")
    return f"'{text}'"


class QueryBuilder:
    """Fluent builder that compiles to a parameterised SQLite query."""

    def __init__(self) -> None:
        self._select: List[str] = []
        self._distinct: bool = False
        self._from: Optional[str] = None
        self._joins: List[JoinClause] = []
        self._where: List[object] = []  # Condition | _OrCondition
        self._group_by: List[str] = []
        self._having: List[Condition] = []
        self._order_by: List[Tuple[str, OrderDir]] = []
        self._limit: Optional[int] = None
        self._offset: Optional[int] = None

    # ------------------------------------------------------------------ SELECT
    def select(self, *columns: str) -> "QueryBuilder":
        self._select.extend(columns)
        return self

    def distinct(self) -> "QueryBuilder":
        self._distinct = True
        return self

    def from_table(self, table: str) -> "QueryBuilder":
        self._from = table
        return self

    # ------------------------------------------------------------------- WHERE
    def where(self, column: str, op: str, value: Any = None) -> "QueryBuilder":
        self._where.append(Condition(column, op, value))
        return self

    def and_where(self, column: str, op: str, value: Any = None) -> "QueryBuilder":
        return self.where(column, op, value)

    def or_where(self, column: str, op: str, value: Any = None) -> "QueryBuilder":
        self._where.append(_OrCondition(Condition(column, op, value)))
        return self

    def where_in(self, column: str, values: list) -> "QueryBuilder":
        self._where.append(Condition(column, "IN", list(values)))
        return self

    def where_between(self, column: str, low: Any, high: Any) -> "QueryBuilder":
        self._where.append(Condition(column, "BETWEEN", (low, high)))
        return self

    def where_null(self, column: str) -> "QueryBuilder":
        self._where.append(Condition(column, "IS NULL"))
        return self

    def where_not_null(self, column: str) -> "QueryBuilder":
        self._where.append(Condition(column, "IS NOT NULL"))
        return self

    # -------------------------------------------------------------------- JOIN
    def join(
        self,
        table: str,
        on: str,
        join_type: JoinType = JoinType.INNER,
    ) -> "QueryBuilder":
        self._joins.append(JoinClause(join_type, table, on))
        return self

    def left_join(self, table: str, on: str) -> "QueryBuilder":
        return self.join(table, on, JoinType.LEFT)

    # ----------------------------------------------------------- GROUP / HAVING
    def group_by(self, *columns: str) -> "QueryBuilder":
        self._group_by.extend(columns)
        return self

    def having(self, column: str, op: str, value: Any = None) -> "QueryBuilder":
        self._having.append(Condition(column, op, value))
        return self

    # ----------------------------------------------------------------- ORDER
    def order_by(
        self, column: str, direction: OrderDir = OrderDir.ASC
    ) -> "QueryBuilder":
        self._order_by.append((column, direction))
        return self

    # ---------------------------------------------------------------- LIMIT
    def limit(self, n: int) -> "QueryBuilder":
        self._limit = int(n)
        return self

    def offset(self, n: int) -> "QueryBuilder":
        self._offset = int(n)
        return self

    # ---------------------------------------------------------------- RESET
    def reset(self) -> "QueryBuilder":
        self.__init__()
        return self

    def clone(self) -> "QueryBuilder":
        other = QueryBuilder()
        other._select = list(self._select)
        other._distinct = self._distinct
        other._from = self._from
        other._joins = list(self._joins)
        other._where = list(self._where)
        other._group_by = list(self._group_by)
        other._having = list(self._having)
        other._order_by = list(self._order_by)
        other._limit = self._limit
        other._offset = self._offset
        return other

    # ----------------------------------------------------------------- BUILD
    def _build_where(self) -> Tuple[str, List[Any]]:
        if not self._where:
            return "", []
        parts: List[str] = []
        params: List[Any] = []
        for idx, item in enumerate(self._where):
            if isinstance(item, _OrCondition):
                frag, p = _render_condition(item.condition)
                connector = " OR " if idx > 0 else ""
                parts.append(f"{connector}{frag}")
                params.extend(p)
            else:
                frag, p = _render_condition(item)
                connector = " AND " if idx > 0 else ""
                parts.append(f"{connector}{frag}")
                params.extend(p)
        return "WHERE " + "".join(parts), params

    def _build_having(self) -> Tuple[str, List[Any]]:
        if not self._having:
            return "", []
        parts: List[str] = []
        params: List[Any] = []
        for idx, cond in enumerate(self._having):
            frag, p = _render_condition(cond)
            connector = " AND " if idx > 0 else ""
            parts.append(f"{connector}{frag}")
            params.extend(p)
        return "HAVING " + "".join(parts), params

    def build(self) -> Tuple[str, List[Any]]:
        if not self._from:
            raise ValueError("from_table() is required before build()")

        cols = ", ".join(self._select) if self._select else "*"
        head = "SELECT DISTINCT" if self._distinct else "SELECT"
        sql_parts: List[str] = [f"{head} {cols} FROM {self._from}"]

        for j in self._joins:
            sql_parts.append(f"{j.join_type.value} {j.table} ON {j.on}")

        params: List[Any] = []
        where_sql, where_params = self._build_where()
        if where_sql:
            sql_parts.append(where_sql)
            params.extend(where_params)

        if self._group_by:
            sql_parts.append("GROUP BY " + ", ".join(self._group_by))

        having_sql, having_params = self._build_having()
        if having_sql:
            sql_parts.append(having_sql)
            params.extend(having_params)

        if self._order_by:
            order_parts = [f"{col} {direction.value}" for col, direction in self._order_by]
            sql_parts.append("ORDER BY " + ", ".join(order_parts))

        if self._limit is not None:
            sql_parts.append(f"LIMIT {self._limit}")
        if self._offset is not None:
            sql_parts.append(f"OFFSET {self._offset}")

        return " ".join(sql_parts), params

    def to_sql(self) -> str:
        """Return SQL with parameters inlined as literals (display only)."""

        sql, params = self.build()
        out: List[str] = []
        param_iter = iter(params)
        for ch in sql:
            if ch == "?":
                try:
                    out.append(_format_literal(next(param_iter)))
                except StopIteration:
                    out.append("?")
            else:
                out.append(ch)
        return "".join(out)

    # ============================================================== MUTATIONS
    def insert(self, table: str, values: dict) -> Tuple[str, List[Any]]:
        if not values:
            raise ValueError("insert() requires at least one column")
        cols = list(values.keys())
        placeholders = ", ".join(["?"] * len(cols))
        sql = (
            f"INSERT INTO {table} ({', '.join(cols)}) "
            f"VALUES ({placeholders})"
        )
        return sql, [values[c] for c in cols]

    def update(
        self,
        table: str,
        values: dict,
        where: Optional[List[Condition]] = None,
    ) -> Tuple[str, List[Any]]:
        if not values:
            raise ValueError("update() requires at least one column")
        cols = list(values.keys())
        set_clause = ", ".join(f"{c} = ?" for c in cols)
        params: List[Any] = [values[c] for c in cols]
        sql = f"UPDATE {table} SET {set_clause}"
        if where:
            parts: List[str] = []
            for idx, cond in enumerate(where):
                frag, p = _render_condition(cond)
                connector = " AND " if idx > 0 else ""
                parts.append(f"{connector}{frag}")
                params.extend(p)
            sql += " WHERE " + "".join(parts)
        return sql, params

    def delete_from(
        self,
        table: str,
        where: Optional[List[Condition]] = None,
    ) -> Tuple[str, List[Any]]:
        sql = f"DELETE FROM {table}"
        params: List[Any] = []
        if where:
            parts: List[str] = []
            for idx, cond in enumerate(where):
                frag, p = _render_condition(cond)
                connector = " AND " if idx > 0 else ""
                parts.append(f"{connector}{frag}")
                params.extend(p)
            sql += " WHERE " + "".join(parts)
        return sql, params


__all__ = [
    "JoinType",
    "OrderDir",
    "Condition",
    "JoinClause",
    "QueryBuilder",
]
