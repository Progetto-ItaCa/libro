#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
check_deprecated.py

Controllo stilistico per progetti LaTeX.
Segnala parole/regex deprecate con contesto, ignorando commenti e verbatim.
"""

import argparse
import os
import re
import sys
import json

# ============================================================
# Configurazione di default (estendibile via JSON)
# ============================================================

DEFAULT_PATTERNS = [
    {
        "pattern": r"\blettore\b",
        "is_regex": True,
        "flags": "i",
        "message": "E' preferibile usare 'chi legge' al posto di 'lettore'"
    },
    {
        "pattern": r"\bmorfismo\b",
        "is_regex": True,
        "flags": "i",
        "message": "Considerare 'freccia' invece di 'morfismo'."
    }
]

VERBATIM_ENVS = {"verbatim", "Verbatim", "lstlisting", "minted"}

IGNORED_MACROS = {
    "index",
    "label",
    "ref", 
    "eqref", 
    "cite", 
    "pageref",
    "Todo",
    "fosco",
    "paolo",
    "beppe",
    "ivan",
    "enricoV",
    "enricoG"
}
def macro_regex(name):
    return re.compile(
        rf'\\{name}\s*\{{[^{{}}]*\}}',
        re.DOTALL
    )

MACRO_REGEXES = [macro_regex(m) for m in IGNORED_MACROS]

# ============================================================
# Utility regex LaTeX (tutte raw string → no SyntaxWarning)
# ============================================================

RE_BEGIN = re.compile(r'\\begin\{(?P<env>[^\}]+)\}')
RE_END   = re.compile(r'\\end\{(?P<env>[^\}]+)\}')
RE_VERB_INLINE = re.compile(
    r'\\verb(?P<delim>[^a-zA-Z0-9\s]).*?(?P=delim)',
    re.DOTALL
)

# ============================================================
# Funzioni di supporto
# ============================================================

def compile_pattern(pat):
    flags = 0
    for f in pat.get("flags", ""):
        if f == "i":
            flags |= re.IGNORECASE
        elif f == "m":
            flags |= re.MULTILINE
        elif f == "s":
            flags |= re.DOTALL

    if pat.get("is_regex", False):
        return re.compile(pat["pattern"], flags)

    escaped = re.escape(pat["pattern"])
    return re.compile(r"\b" + escaped + r"\b", flags)


def iter_target_files(path, exts):
    """Accetta sia file singolo che directory."""
    if os.path.isfile(path):
        if path.lower().endswith(exts):
            yield path
        return

    for dirpath, _, filenames in os.walk(path):
        for fn in filenames:
            if fn.lower().endswith(exts):
                yield os.path.join(dirpath, fn)


def strip_latex_comments(line):
    """Rimuove commenti LaTeX (%) non escapati."""
    i = 0
    while True:
        i = line.find('%', i)
        if i == -1:
            return line
        bs = 0
        j = i - 1
        while j >= 0 and line[j] == '\\':
            bs += 1
            j -= 1
        if bs % 2 == 0:
            return line[:i]
        i += 1

def remove_ignored_macros(s):
    """Rimuove completamente macro{...} per macro in IGNORED_MACROS."""
    for rx in MACRO_REGEXES:
        s = rx.sub("", s)
    return s

def preprocess_lines(lines):
    cleaned = []
    in_verb = False
    verb_env = None

    for line in lines:
        s = line

        if not in_verb:
            m = RE_BEGIN.search(s)
            if m and m.group("env") in VERBATIM_ENVS:
                in_verb = True
                verb_env = m.group("env")
                s = s[:m.start()]

            s = RE_VERB_INLINE.sub("", s)
            s = remove_ignored_macros(s)
            s = strip_latex_comments(s)
            cleaned.append(s)
        else:
            m = RE_END.search(s)
            if m and m.group("env") == verb_env:
                in_verb = False
                verb_env = None
                remainder = s[m.end():]
                remainder = RE_VERB_INLINE.sub("", remainder)
                remainder = remove_ignored_macros(remainder)
                remainder = strip_latex_comments(remainder)
                cleaned.append(remainder)
            else:
                cleaned.append("")

    return cleaned


def context(lines, i):
    prev = lines[i - 1].rstrip("\n") if i > 0 else ""
    curr = lines[i].rstrip("\n")
    nxt = lines[i + 1].rstrip("\n") if i + 1 < len(lines) else ""
    return prev, curr, nxt


def format_output(path, lineno, prev, curr, nxt, rule):
    out = []
    out.append(f"{path}:L{lineno}")
    # out.append(f"Riga: {lineno}")
    out.append(f"[DEPRECATO] {rule.get('message', '')}\n")
    if prev:
        out.append(f"{lineno-1:6d}: {prev}")
    out.append(f"{lineno:6d}: >>> {curr} <<<")
    if nxt:
        out.append(f"{lineno+1:6d}: {nxt}")
    out.append("-" * 80)
    return "\n".join(out)


def load_patterns(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError("Il file di config deve contenere una lista JSON.")
    return data

# ============================================================
# Main
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="Controllo stilistico LaTeX.")
    parser.add_argument("target", help="File o directory da analizzare.")
    parser.add_argument("-c", "--config", help="File JSON con pattern personalizzati.")
    parser.add_argument("-e", "--extensions", nargs="*", default=[".tex", ".sty", ".bib", ".cls", ".txt"])
    parser.add_argument("--write-aux", action="store_true", help="Scrive deprecated.aux.")
    parser.add_argument("--show-zero", action="store_true")
    args = parser.parse_args()

    if not os.path.exists(args.target):
        print(f"Errore: '{args.target}' non esiste.", file=sys.stderr)
        sys.exit(2)

    patterns = load_patterns(args.config) if args.config else DEFAULT_PATTERNS
    compiled = [(compile_pattern(p), p) for p in patterns]

    outputs = []
    found = False
    exts = tuple(args.extensions)

    for path in iter_target_files(args.target, exts):
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            original = f.readlines()

        cleaned = preprocess_lines(original)

        for i, line in enumerate(cleaned):
            for cre, rule in compiled:
                if cre.search(line):
                    prev, curr, nxt = context(original, i)
                    outputs.append(
                        format_output(path, i + 1, prev, curr, nxt, rule)
                    )
                    found = True

    if outputs:
        text = "\n".join(outputs)
        print(text)
        if args.write_aux:
            with open("deprecated.aux", "w", encoding="utf-8") as f:
                f.write(text + "\n")
    elif args.show_zero:
        print("Nessuna occorrenza trovata.")

    sys.exit(1 if found else 0)


if __name__ == "__main__":
    main()
