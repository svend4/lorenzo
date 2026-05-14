"""Query rewriting module: rule-based rewriting and synonym expansion."""
from docstoolkit.query_rewrite.rules import RewriteRule, RuleSet
from docstoolkit.query_rewrite.expander import ExpansionConfig, QueryExpander
from docstoolkit.query_rewrite.rewriter import RewriteConfig, RewriteResult, QueryRewriter

__all__ = [
    # rules
    "RewriteRule",
    "RuleSet",
    # expander
    "ExpansionConfig",
    "QueryExpander",
    # rewriter
    "RewriteConfig",
    "RewriteResult",
    "QueryRewriter",
]
