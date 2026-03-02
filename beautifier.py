#!/usr/bin/env python3
import re, os, sys

doc_dollar_parity = 0
problems = False

def red(s):
    return '\033[31m' + s + '\033[39m'

error_file_path = "bracket_errors.aux"

with open(sys.argv[1], 'r') as f, open(error_file_path, 'w') as error_file:
    for i, line in enumerate(f):
        line_dollar_parity = line.count('$') % 2
        if (doc_dollar_parity == 0 and line_dollar_parity == 1):
            problems = True
            head, tail = line.rsplit('$', 1)
            err_line = '%04d: %s%s' % (i+1, head, red('$' + tail))
            print(err_line, end="")
            error_file.write(err_line + '\n')
        elif doc_dollar_parity == 1 and line_dollar_parity == 0:
            problems = True
            if line.count('$') == 0:
                err_line = '%04d: %s' % (i+1, red(line))
                print(err_line, end="")
                error_file.write(err_line + '\n')
            else:
                head, tail = line.split('$', 1)
                mid, tail = tail.rsplit('$', 1)
                err_line = '%04d: %s%s%s' % (i+1, red(head + '$'), mid, red('$' + tail))
                print(err_line, end="")
                error_file.write(err_line + '\n')
        elif doc_dollar_parity == 1 and line_dollar_parity == 1:
            problems = True
            head, tail = line.split('$', 1)
            err_line = '%04d: %s%s' % (i+1, head, tail)
            print(err_line, end="")
            error_file.write(err_line + '\n')

        doc_dollar_parity += line_dollar_parity
        doc_dollar_parity %= 2

if problems:
    sys.exit("Unmatched $'s found.")

good_delims = lambda x: re.sub(r"\$(.*?)\$", r"\\(\1\\)", x, flags = re.M)

with open(sys.argv[1], 'r+') as f:
    content = []
    inside_tikz = False

    for line in f:
        if "\\begin{tikzpicture}" in line:
            inside_tikz = True
        if "\\end{tikzpicture}" in line:
            inside_tikz = False
            content.append(line)
            continue
        if not inside_tikz:
            line = re.sub(r"\$(.*?)\$", r"\\(\1\\)", line)
        content.append(line)

    f.seek(0)
    f.write(''.join(content))
    f.truncate()

def replace_colon_in_math(content, dry_run=False, filename=""):
    result = []
    i = 0
    lines = content.split('\n')
    
    # mappa offset -> numero di riga
    offset_to_line = {}
    offset = 0
    for lineno, line in enumerate(lines, 1):
        for _ in line:
            offset_to_line[offset] = lineno
            offset += 1
        offset_to_line[offset] = lineno  # il \n
        offset += 1

    findings = []
    i = 0
    while i < len(content):
        if content[i:i+2] == r'\(':
            start = i
            result.append(r'\(')
            i += 2
            math_content = []
            math_start = i
            while i < len(content):
                if content[i:i+2] == r'\)':
                    inner = ''.join(math_content)
                    if ':' in inner:
                        lineno = offset_to_line.get(start, '?')
                        findings.append((lineno, inner.strip()))
                    if not dry_run:
                        result.append(inner.replace(':', r'\colon'))
                    else:
                        result.append(inner)
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

drun = False  # cambia a False per modificare effettivamente

with open(sys.argv[1], 'r+', encoding='utf-8') as f:
    content = f.read()
    content = replace_colon_in_math(content, dry_run=drun, filename=sys.argv[1])
    if not drun:
        f.seek(0)
        f.write(content)
        f.truncate()

with open(sys.argv[1], 'r+', encoding='utf-8') as f:
    content = f.read()
    for punct in [',', '.', ';', ':']:
        content = content.replace(punct + r'\)' , r'\)' + punct)
    f.seek(0)
    f.write(content)
    f.truncate()

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

with open(sys.argv[1], 'r+', encoding='utf-8') as f:
    content = f.read()
    for latex, unicode_char in ACCENTS:
        content = content.replace(latex, unicode_char)
    f.seek(0)
    f.write(content)
    f.truncate()

os.system("latexindent -w " + sys.argv[1] + " > /dev/null 2>&1")
