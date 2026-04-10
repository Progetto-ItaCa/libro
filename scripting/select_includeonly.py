#!/usr/bin/env python3
# -*- coding: utf-8 -*-

r"""select_includeonly.py

Blunt helper for local builds.

Edits main.tex in-place, inside the argument of \includeonly{...}, commenting
all entries except the selected chapter.

Usage:
  python3 select_includeonly.py cap/02-limiti
  python3 select_includeonly.py cap/02-limiti.tex
"""

from __future__ import annotations

import sys
from pathlib import Path


MAIN = Path("main.tex")


def _normalize_ch(ch: str) -> str:
    ch = ch.strip()
    if ch.endswith(".tex"):
        ch = ch[:-4]
    return ch


def _is_include_line(s: str) -> bool:
    t = s.strip()
    if not t:
        return False
    if t.startswith("%"):
        t = t[1:].lstrip()
    # most lines are like: cap/02-limiti,
    return t.startswith("cap/")


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: python3 select_includeonly.py cap/02-limiti", file=sys.stderr)
        return 2

    target = _normalize_ch(argv[1])
    if not MAIN.exists():
        print("Error: main.tex not found", file=sys.stderr)
        return 2

    text = MAIN.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)

    start = None
    end = None
    for i, line in enumerate(lines):
        if "\\includeonly" in line and start is None:
            start = i
            continue
        if start is not None and i > start and line.lstrip().startswith("}"):
            end = i
            break

    if start is None or end is None or end <= start:
        print("Error: could not locate \\includeonly{...} block in main.tex", file=sys.stderr)
        return 2

    found = False
    for i in range(start + 1, end):
        line = lines[i]
        if not _is_include_line(line):
            continue

        prefix_ws = line[: len(line) - len(line.lstrip(" \t"))]
        body = line[len(prefix_ws) :]
        is_commented = body.lstrip().startswith("%")
        body_uncommented = body
        if is_commented:
            # remove first % after indentation
            stripped = body.lstrip()
            body_uncommented = stripped[1:].lstrip()

        # drop trailing comma/whitespace for comparison
        cmp = body_uncommented.strip()
        if cmp.endswith(","):
            cmp = cmp[:-1].rstrip()

        if cmp == target:
            found = True
            # ensure uncommented
            new_body = body_uncommented
        else:
            # ensure commented
            new_body = "% " + body_uncommented

        lines[i] = prefix_ws + new_body
        if not lines[i].endswith("\n") and line.endswith("\n"):
            lines[i] += "\n"

    if not found:
        print(f"Error: chapter `{target}` not found in \\includeonly list", file=sys.stderr)
        return 2

    MAIN.write_text("".join(lines), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
