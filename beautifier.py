#!/usr/bin/env python3
import re
import os
import sys

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

ACCENTS = [
    (r"\`a", "à"),
    (r"\`e", "è"),
    (r"\'e", "é"),
    (r"\`u", "ù"),
    (r"\`o", "ò"),
    (r"\`i", "ì"),
    (r"\`A", "À"),
    (r"\`E", "È"),
    (r"\'E", "É"),
    (r"\`U", "Ù"),
    (r"\`O", "Ò"),
]

PUNCTUATION = [',', '.', ';', ':']

ERROR_FILE = "bracket_errors.aux"
DRY_RUN_COLON = False  # set to True to preview colon replacements without editing

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def red(s):
    return '\033[31m' + s + '\033[39m'


def die(msg):
    sys.exit(f"Error: {msg}")


# ---------------------------------------------------------------------------
# Step 1: Check for unmatched dollar signs
# ---------------------------------------------------------------------------

def check_dollar_parity(path):
    doc_dollar_parity = 0
    problems = False

    with open(path, 'r', encoding='utf-8') as f, \
         open(ERROR_FILE, 'w', encoding='utf-8') as error_file:

        for i, line in enumerate(f):
            line_dollar_parity = line.count('$') % 2

            if doc_dollar_parity == 0 and line_dollar_parity == 1:
                problems = True
                head, tail = line.rsplit('$', 1)
                err_line = '%04d: %s%s' % (i + 1, head, red('$' + tail))
                print(err_line, end="")
                error_file.write(err_line + '\n')

            elif doc_dollar_parity == 1 and line_dollar_parity == 0:
                problems = True
                if line.count('$') == 0:
                    err_line = '%04d: %s' % (i + 1, red(line))
                    print(err_line, end="")
                    error_file.write(err_line + '\n')
                else:
                    head, tail = line.split('$', 1)
                    mid, tail = tail.rsplit('$', 1)
                    err_line = '%04d: %s%s%s' % (
                        i + 1, red(head + '$'), mid, red('$' + tail)
                    )
                    print(err_line, end="")
                    error_file.write(err_line + '\n')

            elif doc_dollar_parity == 1 and line_dollar_parity == 1:
                problems = True
                head, tail = line.split('$', 1)
                err_line = '%04d: %s%s' % (i + 1, head, tail)
                print(err_line, end="")
                error_file.write(err_line + '\n')

            doc_dollar_parity = (doc_dollar_parity + line_dollar_parity) % 2

    if problems:
        die("Unmatched $'s found. See bracket_errors.aux for details.")


# ---------------------------------------------------------------------------
# Step 2: Replace $ / $$ with \(...\) / \[...\], skip tikzpicture environments
# ---------------------------------------------------------------------------

def replace_dollar_delimiters(path):
    lines = []
    inside_tikz = False

    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if "\\begin{tikzpicture}" in line:
                inside_tikz = True
            if "\\end{tikzpicture}" in line:
                inside_tikz = False
                lines.append(line)
                continue
            if not inside_tikz:
                line = re.sub(r'\$\$(.*?)\$\$', r'\\[\1\\]', line, flags=re.DOTALL)
                line = re.sub(r'\$(.*?)\$',     r'\\(\1\\)', line)
            lines.append(line)

    # Fix any \(\)...\(\) leftovers from previous bad runs (may span multiple lines)
    joined = ''.join(lines)
    joined = re.sub(r'\\\(\\\)(.*?)\\\(\\\)', r'\\[\1\\]', joined, flags=re.DOTALL)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(joined)


# ---------------------------------------------------------------------------
# Step 3: Replace bare colons inside \(...\) with \colon
# ---------------------------------------------------------------------------

def replace_colon_in_math(content, dry_run=False, filename=""):
    result = []
    lines = content.split('\n')

    # Build offset -> line number map
    offset_to_line = {}
    offset = 0
    for lineno, line in enumerate(lines, 1):
        for _ in line:
            offset_to_line[offset] = lineno
            offset += 1
        offset_to_line[offset] = lineno  # the \n itself
        offset += 1

    findings = []
    i = 0
    while i < len(content):
        if content[i:i+2] == r'\(':
            start = i
            result.append(r'\(')
            i += 2
            math_content = []
            while i < len(content):
                if content[i:i+2] == r'\)':
                    inner = ''.join(math_content)
                    if ':' in inner:
                        lineno = offset_to_line.get(start, '?')
                        findings.append((lineno, inner.strip()))
                    result.append(inner if dry_run else inner.replace(':', r'\colon'))
                    result.append(r'\)')
                    i += 2
                    break
                math_content.append(content[i])
                i += 1
        else:
            result.append(content[i])
            i += 1

    if dry_run and findings:
        for lineno, math in findings:
            print(f"{filename}:L{lineno}: \\({math}\\)")

    return ''.join(result)


def apply_colon_replacement(path, dry_run=False):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    content = replace_colon_in_math(content, dry_run=dry_run, filename=path)

    if not dry_run:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)


# ---------------------------------------------------------------------------
# Step 4: Move punctuation outside \), replace LaTeX accents with Unicode
# ---------------------------------------------------------------------------

def cleanup_punctuation_and_accents(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    for punct in PUNCTUATION:
        content = content.replace(punct + r'\)', r'\)' + punct)

    for latex, unicode_char in ACCENTS:
        content = content.replace(latex, unicode_char)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)


# ---------------------------------------------------------------------------
# Step 5: Run latexindent
# ---------------------------------------------------------------------------

def run_latexindent(path):
    os.system(f"latexindent -w {path} > /dev/null 2>&1")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) != 2:
        die(f"Usage: {sys.argv[0]} <file.tex>")

    path = sys.argv[1]

    if not os.path.isfile(path):
        die(f"File not found: {path}")

    print(f"Processing {path}...")

    check_dollar_parity(path)
    replace_dollar_delimiters(path)
    apply_colon_replacement(path, dry_run=DRY_RUN_COLON)
    cleanup_punctuation_and_accents(path)
    run_latexindent(path)

    print("Done.")


if __name__ == '__main__':
    main()