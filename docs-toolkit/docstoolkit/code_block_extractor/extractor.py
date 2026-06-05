"""CodeBlockExtractor — extracts and analyses fenced code blocks from Markdown, stdlib only."""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class CodeBlock:
    """A single fenced code block found in a Markdown document.

    Attributes
    ----------
    language:
        Language identifier from the opening fence (e.g. ``"python"``, ``"bash"``).
        Empty string when none is specified.
    code:
        The raw code content between the fences (without fence lines).
    line_start:
        1-based line number of the *opening* fence line.
    line_end:
        1-based line number of the *closing* fence line.
    fence_char:
        The character used for fencing: `` ` `` (backtick) or ``~`` (tilde).
    fence_width:
        Number of fence characters in the opening fence (3 or more).
    """

    language: str
    code: str
    line_start: int
    line_end: int
    fence_char: str
    fence_width: int

    @property
    def line_count(self) -> int:
        """Number of lines in the code body (0 for an empty block)."""
        if not self.code:
            return 0
        return len(self.code.splitlines())

    @property
    def is_empty(self) -> bool:
        """True when the code body is empty or contains only whitespace."""
        return not self.code.strip()


@dataclass
class ExtractionStats:
    """Aggregate statistics for code blocks found in a document.

    Attributes
    ----------
    total_blocks:
        Total number of fenced code blocks.
    by_language:
        Mapping ``language -> count`` for every language seen.
        Unspecified-language blocks are counted under the empty string ``""``.
    total_lines:
        Sum of :attr:`CodeBlock.line_count` across all blocks.
    """

    total_blocks: int
    by_language: dict[str, int]
    total_lines: int

    @property
    def most_common_language(self) -> str:
        """Language with the most blocks; returns ``""`` when there are none."""
        if not self.by_language:
            return ""
        return max(self.by_language, key=lambda lang: self.by_language[lang])

    @property
    def unique_languages(self) -> set[str]:
        """Set of all languages seen (may include ``""``)."""
        return set(self.by_language.keys())


class CodeBlockExtractor:
    """Extracts fenced code blocks from Markdown text.

    Only *fenced* code blocks (``` ` `` or ``~~~``) are recognised.
    Indented (4-space) code blocks are intentionally ignored.

    Nesting rules (as per CommonMark):
    - A backtick fence can contain tilde sequences of any length without
      closing, and vice-versa.
    - A closing fence must use the *same* fence character as the opener and
      have at least as many characters.
    """

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def extract(self, text: str) -> list[CodeBlock]:
        """Return all fenced code blocks found in *text*, in document order."""
        return list(self._iter_blocks(text))

    def extract_by_language(self, text: str, language: str) -> list[CodeBlock]:
        """Return only those blocks whose language matches *language*.

        The comparison is case-sensitive and the empty string matches
        blocks with no language specifier.
        """
        return [b for b in self.extract(text) if b.language == language]

    def stats(self, text: str) -> ExtractionStats:
        """Compute aggregate statistics for *text*."""
        blocks = self.extract(text)
        by_language: dict[str, int] = {}
        total_lines = 0
        for block in blocks:
            by_language[block.language] = by_language.get(block.language, 0) + 1
            total_lines += block.line_count
        return ExtractionStats(
            total_blocks=len(blocks),
            by_language=by_language,
            total_lines=total_lines,
        )

    def strip_code_blocks(self, text: str) -> str:
        """Return *text* with every fenced code block removed.

        The fence lines themselves and the code body are all removed.
        Consecutive newlines introduced by the removal are left as-is.
        """
        blocks = self.extract(text)
        if not blocks:
            return text

        lines = text.splitlines(keepends=True)
        # Mark every line that belongs to a block (inclusive of fence lines)
        remove: set[int] = set()
        for block in blocks:
            for lineno in range(block.line_start, block.line_end + 1):
                remove.add(lineno)  # 1-based

        kept = [line for idx, line in enumerate(lines, start=1) if idx not in remove]
        return "".join(kept)

    def replace_code_block(self, text: str, block: CodeBlock, new_code: str) -> str:
        """Replace the code body of *block* in *text* with *new_code*.

        Only the code body is replaced; the opening fence line (including the
        language tag) and closing fence line are preserved unchanged.

        Parameters
        ----------
        text:
            The original document text.
        block:
            A :class:`CodeBlock` previously returned by :meth:`extract` for
            this *text*.
        new_code:
            The replacement code string.  A trailing newline is added
            automatically when *new_code* is non-empty and does not already
            end with ``\\n``.
        """
        lines = text.splitlines(keepends=True)

        # Lines inside the code block (between fences, exclusive)
        code_start = block.line_start      # 1-based, index = line_start - 1 + 1
        code_end = block.line_end - 1      # 1-based, exclusive of closing fence

        # Build replacement: new_code as lines with a trailing newline guarantee
        if new_code and not new_code.endswith("\n"):
            new_code = new_code + "\n"

        new_lines = new_code.splitlines(keepends=True) if new_code else []

        # Splice: [0 .. line_start-1) + opening fence + new_lines + closing fence + rest
        result = (
            lines[: block.line_start - 1]           # before opening fence
            + [lines[block.line_start - 1]]          # opening fence line
            + new_lines                               # replacement code
            + [lines[block.line_end - 1]]            # closing fence line
            + lines[block.line_end :]                # everything after
        )
        return "".join(result)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _iter_blocks(self, text: str) -> list[CodeBlock]:
        """Yield CodeBlock objects by scanning *text* line by line."""
        lines = text.splitlines(keepends=True)
        blocks: list[CodeBlock] = []
        i = 0
        n = len(lines)

        while i < n:
            raw_line = lines[i]
            stripped = raw_line.rstrip("\r\n")
            fence_char, fence_width, language = _parse_opening_fence(stripped)
            if fence_char is None:
                i += 1
                continue

            # Found an opening fence at line i (1-based: i+1)
            open_lineno = i + 1
            code_lines: list[str] = []
            i += 1

            while i < n:
                raw_inner = lines[i]
                inner = raw_inner.rstrip("\r\n")
                if _is_closing_fence(inner, fence_char, fence_width):
                    close_lineno = i + 1
                    # Assemble code: strip one trailing newline from the joined body
                    code = "".join(code_lines)
                    # Remove the final trailing newline that comes from the last
                    # code line (the line itself ends with \n before the closing fence)
                    if code.endswith("\n"):
                        code = code[:-1]
                    blocks.append(
                        CodeBlock(
                            language=language,
                            code=code,
                            line_start=open_lineno,
                            line_end=close_lineno,
                            fence_char=fence_char,
                            fence_width=fence_width,
                        )
                    )
                    i += 1
                    break
                code_lines.append(raw_inner)
                i += 1
            # If we ran out of lines without a closing fence, the block is
            # unclosed and we discard it (not appended).

        return blocks


# ---------------------------------------------------------------------------
# Module-level fence parsing helpers
# ---------------------------------------------------------------------------

def _parse_opening_fence(line: str) -> tuple[str | None, int, str]:
    """Parse *line* as a potential opening fence.

    Returns ``(fence_char, fence_width, language)`` on success, or
    ``(None, 0, "")`` when *line* is not an opening fence.

    Only lines that start at column 0 are accepted (no leading spaces
    before the fence characters), which matches common Markdown parsers for
    the purpose of this implementation.
    """
    if not line:
        return None, 0, ""

    fence_char = line[0]
    if fence_char not in ("`", "~"):
        return None, 0, ""

    width = 0
    for ch in line:
        if ch == fence_char:
            width += 1
        else:
            break

    if width < 3:
        return None, 0, ""

    # The remainder after the fence characters is the info string (language)
    info = line[width:].strip()
    # Language is the first word of the info string
    language = info.split()[0] if info else ""

    return fence_char, width, language


def _is_closing_fence(line: str, fence_char: str, min_width: int) -> bool:
    """Return True when *line* is a valid closing fence.

    A closing fence must consist solely of *fence_char* repeated at least
    *min_width* times (possibly followed by trailing spaces).
    """
    stripped = line.strip()
    if not stripped:
        return False
    if stripped[0] != fence_char:
        return False
    if not all(ch == fence_char for ch in stripped):
        return False
    return len(stripped) >= min_width
