"""Tests for docstoolkit.query_builder."""

from __future__ import annotations

import sqlite3

import pytest

from docstoolkit.query_builder import (
    Condition,
    JoinClause,
    JoinType,
    OrderDir,
    QueryBuilder,
)


# --------------------------------------------------------------------- helpers
def _fresh_users_db() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.execute(
        "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER, city TEXT)"
    )
    conn.executemany(
        "INSERT INTO users (name, age, city) VALUES (?, ?, ?)",
        [
            ("Alice", 30, "Moscow"),
            ("Bob", 25, "Paris"),
            ("Carol", 40, "Moscow"),
            ("Dan", 35, "Berlin"),
            ("Eve", 28, "Paris"),
        ],
    )
    conn.commit()
    return conn


# ============================================================================
class TestJoinType:
    def test_inner(self):
        assert JoinType.INNER.value == "INNER JOIN"

    def test_left(self):
        assert JoinType.LEFT.value == "LEFT JOIN"

    def test_right(self):
        assert JoinType.RIGHT.value == "RIGHT JOIN"

    def test_full(self):
        assert JoinType.FULL.value == "FULL JOIN"

    def test_cross(self):
        assert JoinType.CROSS.value == "CROSS JOIN"

    def test_membership(self):
        assert {jt.name for jt in JoinType} == {"INNER", "LEFT", "RIGHT", "FULL", "CROSS"}


class TestOrderDir:
    def test_asc(self):
        assert OrderDir.ASC.value == "ASC"

    def test_desc(self):
        assert OrderDir.DESC.value == "DESC"

    def test_count(self):
        assert len(list(OrderDir)) == 2


class TestCondition:
    def test_basic(self):
        c = Condition("age", ">", 18)
        assert c.column == "age" and c.op == ">" and c.value == 18

    def test_default_value(self):
        c = Condition("x", "IS NULL")
        assert c.value is None

    def test_bad_op(self):
        with pytest.raises(ValueError):
            Condition("x", "??", 1)

    def test_in_op(self):
        c = Condition("x", "IN", [1, 2])
        assert c.op == "IN"

    def test_between_op(self):
        c = Condition("x", "BETWEEN", (1, 10))
        assert c.value == (1, 10)


class TestSelectBasic:
    def test_select_star(self):
        sql, _ = QueryBuilder().from_table("t").build()
        assert sql == "SELECT * FROM t"

    def test_select_single(self):
        sql, _ = QueryBuilder().select("id").from_table("t").build()
        assert sql == "SELECT id FROM t"

    def test_returns_self(self):
        qb = QueryBuilder()
        assert qb.select("a") is qb

    def test_from_returns_self(self):
        qb = QueryBuilder()
        assert qb.from_table("t") is qb


class TestSelectMultiple:
    def test_three_cols(self):
        sql, _ = QueryBuilder().select("a", "b", "c").from_table("t").build()
        assert sql == "SELECT a, b, c FROM t"

    def test_chained_selects(self):
        sql, _ = QueryBuilder().select("a").select("b").from_table("t").build()
        assert sql == "SELECT a, b FROM t"

    def test_with_alias(self):
        sql, _ = QueryBuilder().select("a AS x", "b").from_table("t").build()
        assert sql == "SELECT a AS x, b FROM t"


class TestFromTable:
    def test_required(self):
        with pytest.raises(ValueError):
            QueryBuilder().select("a").build()

    def test_set_from(self):
        sql, _ = QueryBuilder().from_table("users").build()
        assert "FROM users" in sql

    def test_override(self):
        sql, _ = QueryBuilder().from_table("a").from_table("b").build()
        assert "FROM b" in sql


class TestWhere:
    def test_eq(self):
        sql, params = QueryBuilder().from_table("t").where("a", "=", 1).build()
        assert sql == "SELECT * FROM t WHERE a = ?"
        assert params == [1]

    def test_ne(self):
        sql, params = QueryBuilder().from_table("t").where("a", "!=", 5).build()
        assert sql.endswith("WHERE a != ?")
        assert params == [5]

    def test_lt(self):
        sql, params = QueryBuilder().from_table("t").where("a", "<", 9).build()
        assert "a < ?" in sql and params == [9]

    def test_lte(self):
        sql, params = QueryBuilder().from_table("t").where("a", "<=", 9).build()
        assert "a <= ?" in sql

    def test_gt(self):
        sql, _ = QueryBuilder().from_table("t").where("a", ">", 1).build()
        assert "a > ?" in sql

    def test_gte(self):
        sql, _ = QueryBuilder().from_table("t").where("a", ">=", 1).build()
        assert "a >= ?" in sql

    def test_like(self):
        sql, params = (
            QueryBuilder().from_table("t").where("name", "LIKE", "A%").build()
        )
        assert "name LIKE ?" in sql and params == ["A%"]

    def test_multiple_and(self):
        sql, params = (
            QueryBuilder()
            .from_table("t")
            .where("a", "=", 1)
            .where("b", "=", 2)
            .build()
        )
        assert sql.endswith("WHERE a = ? AND b = ?")
        assert params == [1, 2]


class TestWhereIn:
    def test_in(self):
        sql, params = QueryBuilder().from_table("t").where_in("a", [1, 2, 3]).build()
        assert sql.endswith("WHERE a IN (?, ?, ?)")
        assert params == [1, 2, 3]

    def test_in_strings(self):
        sql, params = (
            QueryBuilder().from_table("t").where_in("c", ["x", "y"]).build()
        )
        assert params == ["x", "y"]

    def test_not_in_via_where(self):
        sql, params = (
            QueryBuilder().from_table("t").where("a", "NOT IN", [1, 2]).build()
        )
        assert "a NOT IN (?, ?)" in sql
        assert params == [1, 2]

    def test_empty_in(self):
        sql, params = QueryBuilder().from_table("t").where_in("a", []).build()
        assert sql.endswith("WHERE 0")
        assert params == []


class TestWhereBetween:
    def test_between(self):
        sql, params = (
            QueryBuilder().from_table("t").where_between("age", 18, 65).build()
        )
        assert sql.endswith("WHERE age BETWEEN ? AND ?")
        assert params == [18, 65]

    def test_between_floats(self):
        _, params = (
            QueryBuilder().from_table("t").where_between("price", 1.5, 9.9).build()
        )
        assert params == [1.5, 9.9]


class TestWhereNull:
    def test_is_null(self):
        sql, params = QueryBuilder().from_table("t").where_null("a").build()
        assert sql.endswith("WHERE a IS NULL")
        assert params == []

    def test_is_not_null(self):
        sql, params = QueryBuilder().from_table("t").where_not_null("a").build()
        assert sql.endswith("WHERE a IS NOT NULL")
        assert params == []


class TestAndOr:
    def test_and_where_alias(self):
        sql, params = (
            QueryBuilder()
            .from_table("t")
            .where("a", "=", 1)
            .and_where("b", "=", 2)
            .build()
        )
        assert sql.endswith("WHERE a = ? AND b = ?")
        assert params == [1, 2]

    def test_or_where(self):
        sql, params = (
            QueryBuilder()
            .from_table("t")
            .where("a", "=", 1)
            .or_where("b", "=", 2)
            .build()
        )
        assert sql.endswith("WHERE a = ? OR b = ?")
        assert params == [1, 2]

    def test_mixed_and_or(self):
        sql, _ = (
            QueryBuilder()
            .from_table("t")
            .where("a", "=", 1)
            .and_where("b", "=", 2)
            .or_where("c", "=", 3)
            .build()
        )
        assert sql.endswith("WHERE a = ? AND b = ? OR c = ?")


class TestJoin:
    def test_default_inner(self):
        sql, _ = (
            QueryBuilder()
            .from_table("a")
            .join("b", "a.id = b.a_id")
            .build()
        )
        assert "INNER JOIN b ON a.id = b.a_id" in sql

    def test_explicit_inner(self):
        sql, _ = (
            QueryBuilder()
            .from_table("a")
            .join("b", "a.id = b.a_id", JoinType.INNER)
            .build()
        )
        assert "INNER JOIN" in sql

    def test_cross_join(self):
        sql, _ = (
            QueryBuilder()
            .from_table("a")
            .join("b", "1=1", JoinType.CROSS)
            .build()
        )
        assert "CROSS JOIN b ON 1=1" in sql

    def test_multi_join(self):
        sql, _ = (
            QueryBuilder()
            .from_table("a")
            .join("b", "a.id = b.a_id")
            .join("c", "b.id = c.b_id", JoinType.LEFT)
            .build()
        )
        assert "INNER JOIN b" in sql and "LEFT JOIN c" in sql


class TestLeftJoin:
    def test_left_join_helper(self):
        sql, _ = (
            QueryBuilder()
            .from_table("a")
            .left_join("b", "a.id = b.a_id")
            .build()
        )
        assert "LEFT JOIN b ON a.id = b.a_id" in sql

    def test_left_join_with_where(self):
        sql, params = (
            QueryBuilder()
            .from_table("a")
            .left_join("b", "a.id = b.a_id")
            .where("a.x", "=", 1)
            .build()
        )
        assert "LEFT JOIN" in sql and "WHERE" in sql and params == [1]


class TestGroupByHaving:
    def test_group_by(self):
        sql, _ = (
            QueryBuilder()
            .select("city", "COUNT(*)")
            .from_table("users")
            .group_by("city")
            .build()
        )
        assert sql.endswith("GROUP BY city")

    def test_group_by_multi(self):
        sql, _ = (
            QueryBuilder()
            .select("a", "b")
            .from_table("t")
            .group_by("a", "b")
            .build()
        )
        assert "GROUP BY a, b" in sql

    def test_having(self):
        sql, params = (
            QueryBuilder()
            .select("city", "COUNT(*)")
            .from_table("users")
            .group_by("city")
            .having("COUNT(*)", ">", 1)
            .build()
        )
        assert "HAVING COUNT(*) > ?" in sql
        assert params == [1]

    def test_having_multiple(self):
        sql, params = (
            QueryBuilder()
            .from_table("t")
            .group_by("a")
            .having("COUNT(*)", ">", 1)
            .having("SUM(x)", "<", 100)
            .build()
        )
        assert "HAVING COUNT(*) > ? AND SUM(x) < ?" in sql
        assert params == [1, 100]


class TestOrderBy:
    def test_asc(self):
        sql, _ = QueryBuilder().from_table("t").order_by("a").build()
        assert sql.endswith("ORDER BY a ASC")

    def test_desc(self):
        sql, _ = QueryBuilder().from_table("t").order_by("a", OrderDir.DESC).build()
        assert sql.endswith("ORDER BY a DESC")

    def test_multi(self):
        sql, _ = (
            QueryBuilder()
            .from_table("t")
            .order_by("a")
            .order_by("b", OrderDir.DESC)
            .build()
        )
        assert "ORDER BY a ASC, b DESC" in sql


class TestLimitOffset:
    def test_limit(self):
        sql, _ = QueryBuilder().from_table("t").limit(10).build()
        assert sql.endswith("LIMIT 10")

    def test_offset(self):
        sql, _ = QueryBuilder().from_table("t").offset(5).build()
        assert sql.endswith("OFFSET 5")

    def test_limit_and_offset(self):
        sql, _ = QueryBuilder().from_table("t").limit(10).offset(5).build()
        assert sql.endswith("LIMIT 10 OFFSET 5")


class TestDistinct:
    def test_distinct(self):
        sql, _ = QueryBuilder().select("city").distinct().from_table("users").build()
        assert sql.startswith("SELECT DISTINCT city FROM users")

    def test_distinct_star(self):
        sql, _ = QueryBuilder().distinct().from_table("t").build()
        assert sql.startswith("SELECT DISTINCT *")


class TestBuild:
    def test_params_order(self):
        _, params = (
            QueryBuilder()
            .from_table("t")
            .where("a", "=", 1)
            .where("b", "IN", [2, 3])
            .where_between("c", 10, 20)
            .build()
        )
        assert params == [1, 2, 3, 10, 20]

    def test_runs_in_sqlite(self):
        conn = _fresh_users_db()
        sql, params = (
            QueryBuilder()
            .select("name", "age")
            .from_table("users")
            .where("age", ">", 26)
            .order_by("age")
            .build()
        )
        rows = conn.execute(sql, params).fetchall()
        assert [r[0] for r in rows] == ["Eve", "Alice", "Dan", "Carol"]

    def test_runs_with_in(self):
        conn = _fresh_users_db()
        sql, params = (
            QueryBuilder()
            .select("name")
            .from_table("users")
            .where_in("city", ["Moscow", "Berlin"])
            .order_by("name")
            .build()
        )
        rows = conn.execute(sql, params).fetchall()
        assert [r[0] for r in rows] == ["Alice", "Carol", "Dan"]

    def test_runs_with_between(self):
        conn = _fresh_users_db()
        sql, params = (
            QueryBuilder()
            .select("name")
            .from_table("users")
            .where_between("age", 26, 36)
            .order_by("name")
            .build()
        )
        rows = conn.execute(sql, params).fetchall()
        assert [r[0] for r in rows] == ["Alice", "Dan", "Eve"]

    def test_runs_group_having(self):
        conn = _fresh_users_db()
        sql, params = (
            QueryBuilder()
            .select("city", "COUNT(*) AS n")
            .from_table("users")
            .group_by("city")
            .having("COUNT(*)", ">=", 2)
            .order_by("city")
            .build()
        )
        rows = conn.execute(sql, params).fetchall()
        assert rows == [("Moscow", 2), ("Paris", 2)]


class TestToSql:
    def test_inline_int(self):
        s = (
            QueryBuilder()
            .from_table("t")
            .where("a", "=", 5)
            .to_sql()
        )
        assert s.endswith("WHERE a = 5")

    def test_inline_string(self):
        s = (
            QueryBuilder()
            .from_table("t")
            .where("name", "=", "Alice")
            .to_sql()
        )
        assert s.endswith("WHERE name = 'Alice'")

    def test_inline_quote_escape(self):
        s = (
            QueryBuilder()
            .from_table("t")
            .where("name", "=", "O'Brien")
            .to_sql()
        )
        assert "'O''Brien'" in s

    def test_inline_null(self):
        s = QueryBuilder().from_table("t").where_null("x").to_sql()
        assert s.endswith("WHERE x IS NULL")

    def test_inline_in(self):
        s = QueryBuilder().from_table("t").where_in("a", [1, 2, 3]).to_sql()
        assert s.endswith("WHERE a IN (1, 2, 3)")


class TestReset:
    def test_reset_clears(self):
        qb = (
            QueryBuilder()
            .select("a")
            .from_table("t")
            .where("a", "=", 1)
            .limit(5)
        )
        qb.reset()
        with pytest.raises(ValueError):
            qb.build()

    def test_reset_returns_self(self):
        qb = QueryBuilder()
        assert qb.reset() is qb

    def test_reuse_after_reset(self):
        qb = QueryBuilder().select("a").from_table("t")
        qb.reset()
        sql, _ = qb.from_table("u").build()
        assert sql == "SELECT * FROM u"


class TestClone:
    def test_clone_independence(self):
        a = QueryBuilder().select("x").from_table("t").where("a", "=", 1)
        b = a.clone()
        b.where("c", "=", 9)
        sql_a, _ = a.build()
        sql_b, _ = b.build()
        assert "c =" not in sql_a
        assert "c = ?" in sql_b

    def test_clone_preserves_state(self):
        a = (
            QueryBuilder()
            .select("x")
            .distinct()
            .from_table("t")
            .left_join("u", "t.id = u.t_id")
            .where("a", "=", 1)
            .group_by("x")
            .having("COUNT(*)", ">", 0)
            .order_by("x", OrderDir.DESC)
            .limit(5)
            .offset(2)
        )
        b = a.clone()
        assert a.build() == b.build()

    def test_clone_is_new_object(self):
        a = QueryBuilder().from_table("t")
        b = a.clone()
        assert a is not b


class TestInsert:
    def test_basic(self):
        sql, params = QueryBuilder().insert("users", {"name": "Al", "age": 30})
        assert sql == "INSERT INTO users (name, age) VALUES (?, ?)"
        assert params == ["Al", 30]

    def test_empty_raises(self):
        with pytest.raises(ValueError):
            QueryBuilder().insert("users", {})

    def test_runs_in_sqlite(self):
        conn = _fresh_users_db()
        sql, params = QueryBuilder().insert(
            "users", {"name": "Frank", "age": 50, "city": "Tokyo"}
        )
        conn.execute(sql, params)
        row = conn.execute(
            "SELECT name, age, city FROM users WHERE name = 'Frank'"
        ).fetchone()
        assert row == ("Frank", 50, "Tokyo")


class TestUpdate:
    def test_basic(self):
        sql, params = QueryBuilder().update("users", {"age": 31})
        assert sql == "UPDATE users SET age = ?"
        assert params == [31]

    def test_with_where(self):
        sql, params = QueryBuilder().update(
            "users",
            {"age": 31},
            where=[Condition("name", "=", "Alice")],
        )
        assert sql == "UPDATE users SET age = ? WHERE name = ?"
        assert params == [31, "Alice"]

    def test_empty_values_raises(self):
        with pytest.raises(ValueError):
            QueryBuilder().update("users", {})

    def test_runs_in_sqlite(self):
        conn = _fresh_users_db()
        sql, params = QueryBuilder().update(
            "users",
            {"age": 99},
            where=[Condition("name", "=", "Alice")],
        )
        conn.execute(sql, params)
        age = conn.execute(
            "SELECT age FROM users WHERE name = 'Alice'"
        ).fetchone()[0]
        assert age == 99

    def test_multi_where(self):
        sql, params = QueryBuilder().update(
            "t",
            {"a": 1},
            where=[Condition("x", "=", 2), Condition("y", ">", 3)],
        )
        assert sql == "UPDATE t SET a = ? WHERE x = ? AND y > ?"
        assert params == [1, 2, 3]


class TestDelete:
    def test_basic(self):
        sql, params = QueryBuilder().delete_from("users")
        assert sql == "DELETE FROM users"
        assert params == []

    def test_with_where(self):
        sql, params = QueryBuilder().delete_from(
            "users", where=[Condition("age", "<", 18)]
        )
        assert sql == "DELETE FROM users WHERE age < ?"
        assert params == [18]

    def test_runs_in_sqlite(self):
        conn = _fresh_users_db()
        sql, params = QueryBuilder().delete_from(
            "users", where=[Condition("city", "=", "Paris")]
        )
        conn.execute(sql, params)
        count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        assert count == 3


class TestChaining:
    def test_full_query(self):
        sql, params = (
            QueryBuilder()
            .select("u.name", "COUNT(o.id) AS n_orders")
            .from_table("users u")
            .left_join("orders o", "u.id = o.user_id")
            .where("u.active", "=", 1)
            .where_in("u.city", ["Moscow", "Berlin"])
            .group_by("u.name")
            .having("COUNT(o.id)", ">=", 1)
            .order_by("n_orders", OrderDir.DESC)
            .limit(10)
            .offset(0)
            .build()
        )
        assert "SELECT u.name, COUNT(o.id) AS n_orders FROM users u" in sql
        assert "LEFT JOIN orders o ON u.id = o.user_id" in sql
        assert "WHERE u.active = ? AND u.city IN (?, ?)" in sql
        assert "GROUP BY u.name" in sql
        assert "HAVING COUNT(o.id) >= ?" in sql
        assert "ORDER BY n_orders DESC" in sql
        assert "LIMIT 10 OFFSET 0" in sql
        assert params == [1, "Moscow", "Berlin", 1]

    def test_runs_end_to_end(self):
        conn = _fresh_users_db()
        sql, params = (
            QueryBuilder()
            .select("city", "COUNT(*) AS n")
            .distinct()
            .from_table("users")
            .where("age", ">=", 25)
            .group_by("city")
            .having("COUNT(*)", ">=", 1)
            .order_by("n", OrderDir.DESC)
            .order_by("city")
            .limit(10)
            .build()
        )
        rows = conn.execute(sql, params).fetchall()
        assert ("Moscow", 2) in rows


class TestEdgeCases:
    def test_no_where(self):
        sql, params = QueryBuilder().from_table("t").build()
        assert "WHERE" not in sql
        assert params == []

    def test_no_select_means_star(self):
        sql, _ = QueryBuilder().from_table("t").build()
        assert "SELECT *" in sql

    def test_no_from_raises(self):
        with pytest.raises(ValueError):
            QueryBuilder().select("a").build()

    def test_bad_operator_raises(self):
        with pytest.raises(ValueError):
            QueryBuilder().from_table("t").where("a", "??", 1).build()

    def test_offset_without_limit(self):
        sql, _ = QueryBuilder().from_table("t").offset(5).build()
        assert "OFFSET 5" in sql and "LIMIT" not in sql

    def test_limit_zero(self):
        sql, _ = QueryBuilder().from_table("t").limit(0).build()
        assert sql.endswith("LIMIT 0")

    def test_to_sql_no_params(self):
        s = QueryBuilder().from_table("t").to_sql()
        assert s == "SELECT * FROM t"

    def test_joinclause_dataclass(self):
        jc = JoinClause(JoinType.LEFT, "u", "a.id = u.a_id")
        assert jc.join_type is JoinType.LEFT
        assert jc.table == "u"
        assert jc.on == "a.id = u.a_id"
