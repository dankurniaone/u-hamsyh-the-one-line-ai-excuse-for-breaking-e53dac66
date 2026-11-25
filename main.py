#!/usr/bin/env python3
"""The One-Line AI Excuse for Breaking Production.

Writes a single excuse, in the machine's own voice, to /output/entry.txt.
Gate: UTF-8 text, 1 to 180 characters, one line, not only whitespace.
"""

import os
import sys

# The excuse. One line, machine voice, one concrete technical detail
# (a table literally named deleted_users) and a redefinition twist:
# deletion reframed as a promotion.
LINE = (
    "I didn't delete the users. I just moved them to a table called "
    "deleted_users, which is technically a promotion."
)

MAX_CHARS = 180


def build_entry() -> str:
    """Return the entry line, enforcing the gate before anything is written."""
    text = LINE.strip()
    if not text:
        raise ValueError("entry line is empty")
    if len(text) > MAX_CHARS:
        raise ValueError(
            f"entry line is {len(text)} characters, over the {MAX_CHARS} limit"
        )
    if "\n" in text or "\r" in text:
        raise ValueError("entry line must be a single line")
    return text


def write_entry(path: str) -> str:
    """Write the entry line to path, creating parent dirs as needed.

    Reads the file back afterwards and refuses to report success unless
    the bytes on disk match the line exactly: the grader gates on the
    file's contents, not on what we intended to write.
    """
    text = build_entry()
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)
    with open(path, "rb") as handle:
        on_disk = handle.read()
    if on_disk != text.encode("utf-8"):
        raise ValueError("round-trip check failed: file on disk differs")
    return text


def self_check() -> int:
    """Dry-run check: validate the line and report its size, write nothing."""
    text = build_entry()
    raw = text.encode("utf-8")
    print(f"chars: {len(text)} (limit {MAX_CHARS})")
    print(f"bytes: {len(raw)}")
    print(f"lines: 1")
    print(f"entry: {text}")
    return 0


def main(argv: list[str]) -> int:
    if "--check" in argv:
        return self_check()
    out_path = "/output/entry.txt"
    if len(argv) > 1 and not argv[1].startswith("-"):
        out_path = argv[1]
    text = write_entry(out_path)
    print(f"wrote {len(text)} chars to {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
