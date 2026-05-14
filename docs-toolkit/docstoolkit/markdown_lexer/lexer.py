"""Markdown lexer — tokenizes markdown text into typed tokens.

Pure stdlib. Provides block-level and inline-level tokenization.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Iterator, Optional


class TokenType(Enum):
    """Types of tokens produced by the markdown lexer."""

    HEADING = "HEADING"
    PARAGRAPH = "PARAGRAPH"
    CODE_BLOCK = "CODE_BLOCK"
    CODE_INLINE = "CODE_INLINE"
    LIST_ITEM = "LIST_ITEM"
    NUMBERED_ITEM = "NUMBERED_ITEM"
    BLOCKQUOTE = "BLOCKQUOTE"
    HORIZONTAL_RULE = "HORIZONTAL_RULE"
    LINK = "LINK"
    IMAGE = "IMAGE"
    BOLD = "BOLD"
    ITALIC = "ITALIC"
    STRIKETHROUGH = "STRIKETHROUGH"
    TABLE_ROW = "TABLE_ROW"
    FRONTMATTER = "FRONTMATTER"
    COMMENT = "COMMENT"
    NEWLINE = "NEWLINE"
    TEXT = "TEXT"


@dataclass
class Token:
    """A single markdown token."""

    token_type: TokenType
    value: str
    line_num: int
    column: int = 0
    metadata: dict = field(default_factory=dict)


# Block-level patterns
_RE_HEADING = re.compile(r"^(#{1,6})\s+(.+)$")
_RE_LIST_ITEM = re.compile(r"^[\*\-\+]\s+(.*)$")
_RE_NUMBERED_ITEM = re.compile(r"^(\d+)\.\s+(.*)$")
_RE_BLOCKQUOTE = re.compile(r"^>\s*(.*)$")
_RE_HORIZONTAL_RULE = re.compile(r"^(?:---+|\*\*\*+)$")
_RE_TABLE_ROW = re.compile(r"^\|.*\|$")
_RE_CODE_FENCE = re.compile(r"^```(.*)$")
_RE_FRONTMATTER_DELIM = re.compile(r"^---\s*$")
_RE_COMMENT_FULL = re.compile(r"^<!--(.*?)-->\s*$", re.DOTALL)
_RE_COMMENT_OPEN = re.compile(r"^<!--")
_RE_COMMENT_CLOSE = re.compile(r"-->\s*$")

# Inline patterns
_RE_INLINE_IMAGE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)(?:\s+\"([^\"]*)\")?\)")
_RE_INLINE_LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)(?:\s+\"([^\"]*)\")?\)")
_RE_INLINE_BOLD_STAR = re.compile(r"\*\*([^*]+)\*\*")
_RE_INLINE_BOLD_UNDER = re.compile(r"__([^_]+)__")
_RE_INLINE_STRIKE = re.compile(r"~~([^~]+)~~")
_RE_INLINE_CODE = re.compile(r"`([^`]+)`")
_RE_INLINE_ITALIC_STAR = re.compile(r"(?<!\*)\*([^*\s][^*]*?)\*(?!\*)")
_RE_INLINE_ITALIC_UNDER = re.compile(r"(?<!_)_([^_\s][^_]*?)_(?!_)")


class MarkdownLexer:
    """Tokenize markdown text into a stream of typed tokens."""

    def tokenize(self, text: str) -> list[Token]:
        """Block-level tokenization of full markdown document."""
        if not text:
            return []

        tokens: list[Token] = []
        lines = text.split("\n")
        i = 0
        n = len(lines)

        # Frontmatter at start of document
        if n > 0 and _RE_FRONTMATTER_DELIM.match(lines[0]):
            # Find closing ---
            end = None
            for j in range(1, n):
                if _RE_FRONTMATTER_DELIM.match(lines[j]):
                    end = j
                    break
            if end is not None:
                fm_content = "\n".join(lines[1:end])
                tokens.append(
                    Token(
                        token_type=TokenType.FRONTMATTER,
                        value=fm_content,
                        line_num=1,
                        column=0,
                        metadata={"end_line": end + 1},
                    )
                )
                i = end + 1

        while i < n:
            line = lines[i]
            line_num = i + 1

            # Code fence block
            m_fence = _RE_CODE_FENCE.match(line)
            if m_fence:
                language = m_fence.group(1).strip()
                code_lines: list[str] = []
                start_line = line_num
                i += 1
                while i < n:
                    if _RE_CODE_FENCE.match(lines[i]):
                        i += 1
                        break
                    code_lines.append(lines[i])
                    i += 1
                tokens.append(
                    Token(
                        token_type=TokenType.CODE_BLOCK,
                        value="\n".join(code_lines),
                        line_num=start_line,
                        column=0,
                        metadata={"language": language},
                    )
                )
                continue

            # Multi-line HTML comment
            if _RE_COMMENT_OPEN.match(line):
                # Single line comment
                if _RE_COMMENT_FULL.match(line):
                    m = _RE_COMMENT_FULL.match(line)
                    tokens.append(
                        Token(
                            token_type=TokenType.COMMENT,
                            value=m.group(1).strip(),
                            line_num=line_num,
                            column=0,
                            metadata={},
                        )
                    )
                    i += 1
                    continue
                # Multi-line comment
                start_line = line_num
                buffer = [line]
                i += 1
                while i < n:
                    buffer.append(lines[i])
                    if _RE_COMMENT_CLOSE.search(lines[i]):
                        i += 1
                        break
                    i += 1
                joined = "\n".join(buffer)
                inner = joined
                if inner.startswith("<!--"):
                    inner = inner[4:]
                if inner.endswith("-->"):
                    inner = inner[:-3]
                tokens.append(
                    Token(
                        token_type=TokenType.COMMENT,
                        value=inner.strip(),
                        line_num=start_line,
                        column=0,
                        metadata={},
                    )
                )
                continue

            # Single-line block dispatch
            tok = self.tokenize_block(line, line_num)
            if tok is not None:
                tokens.append(tok)
            i += 1

        return tokens

    def tokenize_block(self, line: str, line_num: int) -> Optional[Token]:
        """Tokenize a single line as a block-level token.

        Returns None if no token (e.g. empty input could still produce NEWLINE).
        """
        # Blank / whitespace-only → NEWLINE
        if line.strip() == "":
            return Token(
                token_type=TokenType.NEWLINE,
                value="",
                line_num=line_num,
                column=0,
                metadata={},
            )

        # HEADING
        m = _RE_HEADING.match(line)
        if m:
            level = len(m.group(1))
            content = m.group(2).strip()
            return Token(
                token_type=TokenType.HEADING,
                value=content,
                line_num=line_num,
                column=0,
                metadata={"level": level},
            )

        # HORIZONTAL_RULE
        if _RE_HORIZONTAL_RULE.match(line.strip()):
            return Token(
                token_type=TokenType.HORIZONTAL_RULE,
                value=line.strip(),
                line_num=line_num,
                column=0,
                metadata={},
            )

        # NUMBERED_ITEM
        m = _RE_NUMBERED_ITEM.match(line)
        if m:
            number = int(m.group(1))
            content = m.group(2)
            return Token(
                token_type=TokenType.NUMBERED_ITEM,
                value=content,
                line_num=line_num,
                column=0,
                metadata={"number": number},
            )

        # LIST_ITEM
        m = _RE_LIST_ITEM.match(line)
        if m:
            return Token(
                token_type=TokenType.LIST_ITEM,
                value=m.group(1),
                line_num=line_num,
                column=0,
                metadata={},
            )

        # BLOCKQUOTE
        m = _RE_BLOCKQUOTE.match(line)
        if m:
            return Token(
                token_type=TokenType.BLOCKQUOTE,
                value=m.group(1),
                line_num=line_num,
                column=0,
                metadata={},
            )

        # TABLE_ROW
        if _RE_TABLE_ROW.match(line):
            cells = [c.strip() for c in line.strip("|").split("|")]
            return Token(
                token_type=TokenType.TABLE_ROW,
                value=line,
                line_num=line_num,
                column=0,
                metadata={"cells": cells},
            )

        # Inline single-line comment
        m = _RE_COMMENT_FULL.match(line)
        if m:
            return Token(
                token_type=TokenType.COMMENT,
                value=m.group(1).strip(),
                line_num=line_num,
                column=0,
                metadata={},
            )

        # PARAGRAPH (default)
        return Token(
            token_type=TokenType.PARAGRAPH,
            value=line,
            line_num=line_num,
            column=0,
            metadata={},
        )

    def tokenize_inline(self, text: str, line_num: int = 1) -> list[Token]:
        """Inline-only tokenization (bold/italic/link/code/etc).

        Returns a stream of inline tokens (BOLD, ITALIC, CODE_INLINE, LINK,
        IMAGE, STRIKETHROUGH, TEXT) preserving order.
        """
        if not text:
            return []

        # Find all matches with positions, then weave with TEXT segments.
        matches: list[tuple[int, int, Token]] = []

        # Priority order: image, link, code, bold, strikethrough, italic
        # Images first (so ![] isn't consumed by [])
        for m in _RE_INLINE_IMAGE.finditer(text):
            tok = Token(
                token_type=TokenType.IMAGE,
                value=m.group(1),
                line_num=line_num,
                column=m.start(),
                metadata={"alt": m.group(1), "url": m.group(2), "title": m.group(3) or ""},
            )
            matches.append((m.start(), m.end(), tok))

        # Mark image spans to exclude from link matches
        image_spans = [(s, e) for s, e, _ in matches]

        def _in_image(pos: int) -> bool:
            return any(s <= pos < e for s, e in image_spans)

        for m in _RE_INLINE_LINK.finditer(text):
            # Skip if this link match is part of an image (preceded by !)
            if m.start() > 0 and text[m.start() - 1] == "!":
                continue
            if _in_image(m.start()):
                continue
            tok = Token(
                token_type=TokenType.LINK,
                value=m.group(1),
                line_num=line_num,
                column=m.start(),
                metadata={"text": m.group(1), "url": m.group(2), "title": m.group(3) or ""},
            )
            matches.append((m.start(), m.end(), tok))

        # Code inline — protect from other inline matches
        code_spans: list[tuple[int, int]] = []
        for m in _RE_INLINE_CODE.finditer(text):
            tok = Token(
                token_type=TokenType.CODE_INLINE,
                value=m.group(1),
                line_num=line_num,
                column=m.start(),
                metadata={},
            )
            matches.append((m.start(), m.end(), tok))
            code_spans.append((m.start(), m.end()))

        def _in_code(pos: int) -> bool:
            return any(s <= pos < e for s, e in code_spans)

        def _overlaps_existing(s: int, e: int) -> bool:
            for ms, me, _ in matches:
                if s < me and ms < e:
                    return True
            return False

        # Bold (**...** and __...__)
        for regex in (_RE_INLINE_BOLD_STAR, _RE_INLINE_BOLD_UNDER):
            for m in regex.finditer(text):
                if _in_code(m.start()) or _overlaps_existing(m.start(), m.end()):
                    continue
                tok = Token(
                    token_type=TokenType.BOLD,
                    value=m.group(1),
                    line_num=line_num,
                    column=m.start(),
                    metadata={},
                )
                matches.append((m.start(), m.end(), tok))

        # Strikethrough
        for m in _RE_INLINE_STRIKE.finditer(text):
            if _in_code(m.start()) or _overlaps_existing(m.start(), m.end()):
                continue
            tok = Token(
                token_type=TokenType.STRIKETHROUGH,
                value=m.group(1),
                line_num=line_num,
                column=m.start(),
                metadata={},
            )
            matches.append((m.start(), m.end(), tok))

        # Italic (*...* and _..._)
        for regex in (_RE_INLINE_ITALIC_STAR, _RE_INLINE_ITALIC_UNDER):
            for m in regex.finditer(text):
                if _in_code(m.start()) or _overlaps_existing(m.start(), m.end()):
                    continue
                tok = Token(
                    token_type=TokenType.ITALIC,
                    value=m.group(1),
                    line_num=line_num,
                    column=m.start(),
                    metadata={},
                )
                matches.append((m.start(), m.end(), tok))

        # Sort matches by start position; drop overlapping (keep earlier)
        matches.sort(key=lambda x: (x[0], -x[1]))
        non_overlapping: list[tuple[int, int, Token]] = []
        last_end = -1
        for s, e, tok in matches:
            if s >= last_end:
                non_overlapping.append((s, e, tok))
                last_end = e

        # Weave with TEXT tokens for unmatched stretches
        result: list[Token] = []
        cursor = 0
        for s, e, tok in non_overlapping:
            if s > cursor:
                segment = text[cursor:s]
                if segment:
                    result.append(
                        Token(
                            token_type=TokenType.TEXT,
                            value=segment,
                            line_num=line_num,
                            column=cursor,
                            metadata={},
                        )
                    )
            result.append(tok)
            cursor = e
        if cursor < len(text):
            segment = text[cursor:]
            if segment:
                result.append(
                    Token(
                        token_type=TokenType.TEXT,
                        value=segment,
                        line_num=line_num,
                        column=cursor,
                        metadata={},
                    )
                )

        if not result:
            # Pure text with no inline markup
            result.append(
                Token(
                    token_type=TokenType.TEXT,
                    value=text,
                    line_num=line_num,
                    column=0,
                    metadata={},
                )
            )

        return result

    def iter_tokens(self, text: str) -> Iterator[Token]:
        """Generator version of `tokenize`."""
        for tok in self.tokenize(text):
            yield tok

    def filter_by_type(
        self, tokens: list[Token], token_type: TokenType
    ) -> list[Token]:
        """Return only tokens of a given type."""
        return [t for t in tokens if t.token_type == token_type]

    def to_dict_list(self, tokens: list[Token]) -> list[dict]:
        """Convert tokens to serializable dict list."""
        return [
            {
                "token_type": t.token_type.value,
                "value": t.value,
                "line_num": t.line_num,
                "column": t.column,
                "metadata": dict(t.metadata),
            }
            for t in tokens
        ]
