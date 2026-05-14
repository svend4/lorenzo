"""Tests for docstoolkit.feature_flags module."""
import hashlib
import pytest

from docstoolkit.feature_flags import (
    FeatureFlag, FlagStatus, RolloutStrategy,
    FlagEvaluator, EvaluationContext, EvalResult,
    FlagStore,
)


# ---------------------------------------------------------------------------
# FlagStatus enum
# ---------------------------------------------------------------------------

class TestFlagStatus:
    def test_enabled_value(self):
        assert FlagStatus.ENABLED.value == "enabled"

    def test_disabled_value(self):
        assert FlagStatus.DISABLED.value == "disabled"

    def test_rollout_value(self):
        assert FlagStatus.ROLLOUT.value == "rollout"

    def test_three_members(self):
        assert len(FlagStatus) == 3

    def test_is_str_subclass(self):
        assert isinstance(FlagStatus.ENABLED, str)


# ---------------------------------------------------------------------------
# RolloutStrategy enum
# ---------------------------------------------------------------------------

class TestRolloutStrategy:
    def test_all_value(self):
        assert RolloutStrategy.ALL.value == "all"

    def test_none_value(self):
        assert RolloutStrategy.NONE.value == "none"

    def test_percentage_value(self):
        assert RolloutStrategy.PERCENTAGE.value == "percentage"

    def test_allowlist_value(self):
        assert RolloutStrategy.ALLOWLIST.value == "allowlist"

    def test_four_members(self):
        assert len(RolloutStrategy) == 4

    def test_is_str_subclass(self):
        assert isinstance(RolloutStrategy.ALL, str)


# ---------------------------------------------------------------------------
# FeatureFlag
# ---------------------------------------------------------------------------

class TestFeatureFlagDefaults:
    def test_name_required(self):
        f = FeatureFlag(name="my-flag")
        assert f.name == "my-flag"

    def test_default_status_disabled(self):
        f = FeatureFlag(name="x")
        assert f.status == FlagStatus.DISABLED

    def test_default_rollout_pct_zero(self):
        f = FeatureFlag(name="x")
        assert f.rollout_pct == 0.0

    def test_default_strategy_none(self):
        f = FeatureFlag(name="x")
        assert f.strategy == RolloutStrategy.NONE

    def test_default_allowlist_empty(self):
        f = FeatureFlag(name="x")
        assert f.allowlist == []

    def test_default_description_empty(self):
        f = FeatureFlag(name="x")
        assert f.description == ""

    def test_default_tags_empty(self):
        f = FeatureFlag(name="x")
        assert f.tags == []

    def test_allowlist_not_shared(self):
        f1 = FeatureFlag(name="a")
        f2 = FeatureFlag(name="b")
        f1.allowlist.append("u1")
        assert f2.allowlist == []

    def test_tags_not_shared(self):
        f1 = FeatureFlag(name="a")
        f2 = FeatureFlag(name="b")
        f1.tags.append("beta")
        assert f2.tags == []


class TestFeatureFlagMethods:
    def test_is_globally_enabled_true(self):
        f = FeatureFlag(name="x", status=FlagStatus.ENABLED)
        assert f.is_globally_enabled() is True

    def test_is_globally_enabled_false_when_disabled(self):
        f = FeatureFlag(name="x", status=FlagStatus.DISABLED)
        assert f.is_globally_enabled() is False

    def test_is_globally_enabled_false_when_rollout(self):
        f = FeatureFlag(name="x", status=FlagStatus.ROLLOUT)
        assert f.is_globally_enabled() is False

    def test_is_disabled_true(self):
        f = FeatureFlag(name="x", status=FlagStatus.DISABLED)
        assert f.is_disabled() is True

    def test_is_disabled_false_when_enabled(self):
        f = FeatureFlag(name="x", status=FlagStatus.ENABLED)
        assert f.is_disabled() is False

    def test_is_disabled_false_when_rollout(self):
        f = FeatureFlag(name="x", status=FlagStatus.ROLLOUT)
        assert f.is_disabled() is False


class TestFeatureFlagSerialization:
    def _make_flag(self):
        return FeatureFlag(
            name="dark-mode",
            status=FlagStatus.ROLLOUT,
            rollout_pct=42.5,
            strategy=RolloutStrategy.PERCENTAGE,
            allowlist=["u1", "u2"],
            description="Enable dark mode",
            tags=["ui", "beta"],
        )

    def test_to_dict_name(self):
        assert self._make_flag().to_dict()["name"] == "dark-mode"

    def test_to_dict_status(self):
        assert self._make_flag().to_dict()["status"] == "rollout"

    def test_to_dict_rollout_pct(self):
        assert self._make_flag().to_dict()["rollout_pct"] == 42.5

    def test_to_dict_strategy(self):
        assert self._make_flag().to_dict()["strategy"] == "percentage"

    def test_to_dict_allowlist(self):
        assert self._make_flag().to_dict()["allowlist"] == ["u1", "u2"]

    def test_to_dict_description(self):
        assert self._make_flag().to_dict()["description"] == "Enable dark mode"

    def test_to_dict_tags(self):
        assert self._make_flag().to_dict()["tags"] == ["ui", "beta"]

    def test_round_trip(self):
        original = self._make_flag()
        restored = FeatureFlag.from_dict(original.to_dict())
        assert restored.name == original.name
        assert restored.status == original.status
        assert restored.rollout_pct == original.rollout_pct
        assert restored.strategy == original.strategy
        assert restored.allowlist == original.allowlist
        assert restored.description == original.description
        assert restored.tags == original.tags

    def test_from_dict_defaults(self):
        f = FeatureFlag.from_dict({"name": "minimal"})
        assert f.status == FlagStatus.DISABLED
        assert f.rollout_pct == 0.0
        assert f.strategy == RolloutStrategy.NONE
        assert f.allowlist == []
        assert f.description == ""
        assert f.tags == []

    def test_from_dict_parses_enums(self):
        d = {"name": "x", "status": "enabled", "strategy": "allowlist"}
        f = FeatureFlag.from_dict(d)
        assert f.status == FlagStatus.ENABLED
        assert f.strategy == RolloutStrategy.ALLOWLIST


# ---------------------------------------------------------------------------
# EvaluationContext
# ---------------------------------------------------------------------------

class TestEvaluationContext:
    def test_default_user_id_empty(self):
        ctx = EvaluationContext()
        assert ctx.user_id == ""

    def test_default_attributes_dict(self):
        ctx = EvaluationContext()
        assert ctx.attributes == {}

    def test_attributes_not_shared(self):
        ctx1 = EvaluationContext()
        ctx2 = EvaluationContext()
        ctx1.attributes["k"] = "v"
        assert ctx2.attributes == {}

    def test_custom_user_id(self):
        ctx = EvaluationContext(user_id="alice")
        assert ctx.user_id == "alice"

    def test_custom_attributes(self):
        ctx = EvaluationContext(attributes={"plan": "pro"})
        assert ctx.attributes["plan"] == "pro"


# ---------------------------------------------------------------------------
# EvalResult
# ---------------------------------------------------------------------------

class TestEvalResult:
    def test_bool_true_when_enabled(self):
        r = EvalResult("flag", True, "globally_enabled")
        assert bool(r) is True

    def test_bool_false_when_disabled(self):
        r = EvalResult("flag", False, "disabled")
        assert bool(r) is False

    def test_reason_stored(self):
        r = EvalResult("flag", True, "allowlist")
        assert r.reason == "allowlist"

    def test_flag_name_stored(self):
        r = EvalResult("my-flag", False, "rollout_excluded")
        assert r.flag_name == "my-flag"


# ---------------------------------------------------------------------------
# FlagEvaluator
# ---------------------------------------------------------------------------

@pytest.fixture
def evaluator():
    return FlagEvaluator()

@pytest.fixture
def anon_ctx():
    return EvaluationContext()

@pytest.fixture
def alice_ctx():
    return EvaluationContext(user_id="alice")


class TestFlagEvaluatorDisabled:
    def test_disabled_flag_is_false(self, evaluator, anon_ctx):
        flag = FeatureFlag(name="f", status=FlagStatus.DISABLED)
        result = evaluator.evaluate(flag, anon_ctx)
        assert result.enabled is False

    def test_disabled_flag_reason(self, evaluator, anon_ctx):
        flag = FeatureFlag(name="f", status=FlagStatus.DISABLED)
        result = evaluator.evaluate(flag, anon_ctx)
        assert result.reason == "disabled"

    def test_disabled_flag_name(self, evaluator, anon_ctx):
        flag = FeatureFlag(name="my-flag", status=FlagStatus.DISABLED)
        result = evaluator.evaluate(flag, anon_ctx)
        assert result.flag_name == "my-flag"


class TestFlagEvaluatorEnabled:
    def test_enabled_flag_is_true(self, evaluator, anon_ctx):
        flag = FeatureFlag(name="f", status=FlagStatus.ENABLED)
        result = evaluator.evaluate(flag, anon_ctx)
        assert result.enabled is True

    def test_enabled_flag_reason(self, evaluator, anon_ctx):
        flag = FeatureFlag(name="f", status=FlagStatus.ENABLED)
        result = evaluator.evaluate(flag, anon_ctx)
        assert result.reason == "globally_enabled"

    def test_enabled_bool_truthy(self, evaluator, anon_ctx):
        flag = FeatureFlag(name="f", status=FlagStatus.ENABLED)
        assert evaluator.evaluate(flag, anon_ctx)


class TestFlagEvaluatorRolloutAll:
    def test_rollout_all_is_true(self, evaluator, anon_ctx):
        flag = FeatureFlag(name="f", status=FlagStatus.ROLLOUT, strategy=RolloutStrategy.ALL)
        result = evaluator.evaluate(flag, anon_ctx)
        assert result.enabled is True

    def test_rollout_all_reason(self, evaluator, alice_ctx):
        flag = FeatureFlag(name="f", status=FlagStatus.ROLLOUT, strategy=RolloutStrategy.ALL)
        result = evaluator.evaluate(flag, alice_ctx)
        assert result.reason == "rollout_all"


class TestFlagEvaluatorRolloutNone:
    def test_rollout_none_is_false(self, evaluator, anon_ctx):
        flag = FeatureFlag(name="f", status=FlagStatus.ROLLOUT, strategy=RolloutStrategy.NONE)
        result = evaluator.evaluate(flag, anon_ctx)
        assert result.enabled is False

    def test_rollout_none_reason(self, evaluator, alice_ctx):
        flag = FeatureFlag(name="f", status=FlagStatus.ROLLOUT, strategy=RolloutStrategy.NONE)
        result = evaluator.evaluate(flag, alice_ctx)
        assert result.reason == "rollout_none"


class TestFlagEvaluatorAllowlist:
    def _make_flag(self, allowlist):
        return FeatureFlag(
            name="f",
            status=FlagStatus.ROLLOUT,
            strategy=RolloutStrategy.ALLOWLIST,
            allowlist=allowlist,
        )

    def test_user_in_allowlist_enabled(self, evaluator):
        flag = self._make_flag(["alice", "bob"])
        ctx = EvaluationContext(user_id="alice")
        result = evaluator.evaluate(flag, ctx)
        assert result.enabled is True

    def test_user_in_allowlist_reason(self, evaluator):
        flag = self._make_flag(["alice"])
        ctx = EvaluationContext(user_id="alice")
        result = evaluator.evaluate(flag, ctx)
        assert result.reason == "allowlist"

    def test_user_not_in_allowlist_disabled(self, evaluator):
        flag = self._make_flag(["alice"])
        ctx = EvaluationContext(user_id="charlie")
        result = evaluator.evaluate(flag, ctx)
        assert result.enabled is False

    def test_user_not_in_allowlist_reason(self, evaluator):
        flag = self._make_flag(["alice"])
        ctx = EvaluationContext(user_id="charlie")
        result = evaluator.evaluate(flag, ctx)
        assert result.reason == "not_in_allowlist"

    def test_empty_user_id_not_in_allowlist(self, evaluator):
        flag = self._make_flag(["alice"])
        ctx = EvaluationContext(user_id="")
        result = evaluator.evaluate(flag, ctx)
        assert result.enabled is False

    def test_second_user_in_list(self, evaluator):
        flag = self._make_flag(["alice", "bob"])
        ctx = EvaluationContext(user_id="bob")
        result = evaluator.evaluate(flag, ctx)
        assert result.enabled is True


class TestFlagEvaluatorPercentage:
    def _make_pct_flag(self, pct):
        return FeatureFlag(
            name="pct-flag",
            status=FlagStatus.ROLLOUT,
            strategy=RolloutStrategy.PERCENTAGE,
            rollout_pct=pct,
        )

    def test_100_pct_always_enabled(self, evaluator):
        flag = self._make_pct_flag(100.0)
        for uid in ["alice", "bob", "charlie", "dave", "eve"]:
            ctx = EvaluationContext(user_id=uid)
            assert evaluator.evaluate(flag, ctx).enabled is True

    def test_0_pct_always_disabled(self, evaluator):
        flag = self._make_pct_flag(0.0)
        for uid in ["alice", "bob", "charlie", "dave", "eve"]:
            ctx = EvaluationContext(user_id=uid)
            assert evaluator.evaluate(flag, ctx).enabled is False

    def test_100_pct_reason_rollout_pct(self, evaluator):
        flag = self._make_pct_flag(100.0)
        ctx = EvaluationContext(user_id="alice")
        assert evaluator.evaluate(flag, ctx).reason == "rollout_pct"

    def test_0_pct_reason_rollout_excluded(self, evaluator):
        flag = self._make_pct_flag(0.0)
        ctx = EvaluationContext(user_id="alice")
        assert evaluator.evaluate(flag, ctx).reason == "rollout_excluded"

    def test_deterministic_same_user(self, evaluator):
        flag = self._make_pct_flag(50.0)
        ctx = EvaluationContext(user_id="test-user-xyz")
        r1 = evaluator.evaluate(flag, ctx)
        r2 = evaluator.evaluate(flag, ctx)
        assert r1.enabled == r2.enabled

    def test_hash_matches_expected_bucket(self, evaluator):
        """Verify the hash logic directly so we can test a known inclusion."""
        flag_name = "pct-flag"
        user_id = "known-user"
        key = f"{flag_name}:{user_id}"
        bucket = int(hashlib.md5(key.encode()).hexdigest(), 16) % 100
        # If bucket < 50, user should be included with 50% rollout
        flag = self._make_pct_flag(50.0)
        ctx = EvaluationContext(user_id=user_id)
        result = evaluator.evaluate(flag, ctx)
        if bucket < 50:
            assert result.enabled is True
            assert result.reason == "rollout_pct"
        else:
            assert result.enabled is False
            assert result.reason == "rollout_excluded"

    def test_different_users_may_differ(self, evaluator):
        """With 50% rollout over many users, both outcomes should appear."""
        flag = self._make_pct_flag(50.0)
        results = set()
        for i in range(200):
            ctx = EvaluationContext(user_id=f"user-{i}")
            results.add(evaluator.evaluate(flag, ctx).enabled)
        assert True in results
        assert False in results


class TestFlagEvaluatorEvaluateAll:
    def test_returns_dict_keyed_by_name(self, evaluator, anon_ctx):
        flags = [
            FeatureFlag(name="alpha", status=FlagStatus.ENABLED),
            FeatureFlag(name="beta", status=FlagStatus.DISABLED),
        ]
        results = evaluator.evaluate_all(flags, anon_ctx)
        assert set(results.keys()) == {"alpha", "beta"}

    def test_values_are_eval_results(self, evaluator, anon_ctx):
        flags = [FeatureFlag(name="x", status=FlagStatus.ENABLED)]
        results = evaluator.evaluate_all(flags, anon_ctx)
        assert isinstance(results["x"], EvalResult)

    def test_mixed_enabled_disabled(self, evaluator, anon_ctx):
        flags = [
            FeatureFlag(name="on", status=FlagStatus.ENABLED),
            FeatureFlag(name="off", status=FlagStatus.DISABLED),
        ]
        results = evaluator.evaluate_all(flags, anon_ctx)
        assert results["on"].enabled is True
        assert results["off"].enabled is False

    def test_empty_list(self, evaluator, anon_ctx):
        results = evaluator.evaluate_all([], anon_ctx)
        assert results == {}

    def test_single_flag(self, evaluator, alice_ctx):
        flags = [FeatureFlag(name="solo", status=FlagStatus.ENABLED)]
        results = evaluator.evaluate_all(flags, alice_ctx)
        assert len(results) == 1
        assert results["solo"].enabled is True


# ---------------------------------------------------------------------------
# FlagStore
# ---------------------------------------------------------------------------

@pytest.fixture
def store():
    s = FlagStore()  # in-memory
    yield s
    s.close()


class TestFlagStoreBasic:
    def test_save_and_get(self, store):
        flag = FeatureFlag(name="my-flag", status=FlagStatus.ENABLED)
        store.save(flag)
        retrieved = store.get("my-flag")
        assert retrieved is not None
        assert retrieved.name == "my-flag"
        assert retrieved.status == FlagStatus.ENABLED

    def test_get_missing_returns_none(self, store):
        assert store.get("nonexistent") is None

    def test_save_preserves_all_fields(self, store):
        flag = FeatureFlag(
            name="full-flag",
            status=FlagStatus.ROLLOUT,
            rollout_pct=33.3,
            strategy=RolloutStrategy.PERCENTAGE,
            allowlist=["u1", "u2"],
            description="Test flag",
            tags=["t1", "t2"],
        )
        store.save(flag)
        r = store.get("full-flag")
        assert r.rollout_pct == pytest.approx(33.3)
        assert r.strategy == RolloutStrategy.PERCENTAGE
        assert r.allowlist == ["u1", "u2"]
        assert r.description == "Test flag"
        assert r.tags == ["t1", "t2"]

    def test_save_upserts(self, store):
        flag = FeatureFlag(name="upd", status=FlagStatus.DISABLED)
        store.save(flag)
        flag2 = FeatureFlag(name="upd", status=FlagStatus.ENABLED)
        store.save(flag2)
        assert store.get("upd").status == FlagStatus.ENABLED

    def test_count_empty(self, store):
        assert store.count() == 0

    def test_count_after_saves(self, store):
        store.save(FeatureFlag(name="a"))
        store.save(FeatureFlag(name="b"))
        store.save(FeatureFlag(name="c"))
        assert store.count() == 3

    def test_count_upsert_no_increment(self, store):
        store.save(FeatureFlag(name="x"))
        store.save(FeatureFlag(name="x", status=FlagStatus.ENABLED))
        assert store.count() == 1


class TestFlagStoreList:
    def test_list_all_empty(self, store):
        assert store.list_flags() == []

    def test_list_all_returns_all(self, store):
        store.save(FeatureFlag(name="a", status=FlagStatus.ENABLED))
        store.save(FeatureFlag(name="b", status=FlagStatus.DISABLED))
        store.save(FeatureFlag(name="c", status=FlagStatus.ROLLOUT))
        flags = store.list_flags()
        assert len(flags) == 3

    def test_list_all_sorted_by_name(self, store):
        store.save(FeatureFlag(name="z-flag"))
        store.save(FeatureFlag(name="a-flag"))
        store.save(FeatureFlag(name="m-flag"))
        names = [f.name for f in store.list_flags()]
        assert names == sorted(names)

    def test_list_by_status_enabled(self, store):
        store.save(FeatureFlag(name="on1", status=FlagStatus.ENABLED))
        store.save(FeatureFlag(name="on2", status=FlagStatus.ENABLED))
        store.save(FeatureFlag(name="off1", status=FlagStatus.DISABLED))
        enabled = store.list_flags(status=FlagStatus.ENABLED)
        assert len(enabled) == 2
        assert all(f.status == FlagStatus.ENABLED for f in enabled)

    def test_list_by_status_disabled(self, store):
        store.save(FeatureFlag(name="on1", status=FlagStatus.ENABLED))
        store.save(FeatureFlag(name="off1", status=FlagStatus.DISABLED))
        disabled = store.list_flags(status=FlagStatus.DISABLED)
        assert len(disabled) == 1
        assert disabled[0].name == "off1"

    def test_list_by_status_rollout(self, store):
        store.save(FeatureFlag(name="r1", status=FlagStatus.ROLLOUT))
        store.save(FeatureFlag(name="d1", status=FlagStatus.DISABLED))
        rollout = store.list_flags(status=FlagStatus.ROLLOUT)
        assert len(rollout) == 1
        assert rollout[0].name == "r1"

    def test_list_by_status_none_match(self, store):
        store.save(FeatureFlag(name="a", status=FlagStatus.DISABLED))
        enabled = store.list_flags(status=FlagStatus.ENABLED)
        assert enabled == []


class TestFlagStoreDelete:
    def test_delete_existing_returns_true(self, store):
        store.save(FeatureFlag(name="del-me"))
        assert store.delete("del-me") is True

    def test_delete_removes_flag(self, store):
        store.save(FeatureFlag(name="del-me"))
        store.delete("del-me")
        assert store.get("del-me") is None

    def test_delete_missing_returns_false(self, store):
        assert store.delete("ghost") is False

    def test_delete_decrements_count(self, store):
        store.save(FeatureFlag(name="a"))
        store.save(FeatureFlag(name="b"))
        store.delete("a")
        assert store.count() == 1

    def test_delete_only_target(self, store):
        store.save(FeatureFlag(name="keep"))
        store.save(FeatureFlag(name="remove"))
        store.delete("remove")
        assert store.get("keep") is not None
        assert store.get("remove") is None
