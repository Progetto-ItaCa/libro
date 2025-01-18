import re, os, sys

doc_dollar_parity = 0
problems = False

def red(s):
    return '\033[31m' + s + '\033[39m'

with open (sys.argv[1], 'r') as f:
    for i, line in enumerate(f):
        line_dollar_parity = line.count('$') % 2
        if (doc_dollar_parity == 0 and line_dollar_parity == 1):
            problems = True
            head, tail = line.rsplit('$', 1)
            print('%04d: %s%s' % (i+1, head, red('$' + tail)), end="")
        if doc_dollar_parity == 1 and line_dollar_parity == 0:
            problems = True
            if line.count('$') == 0:
                print('%04d: %s' % (i+1,red(line)), end="")
            else:
                head, tail = line.split('$', 1)
                mid, tail = tail.rsplit('$', 1)
                print('%04d: %s%s%s' % (i+1, red(head + '$'), mid, red('$' + tail)), end="")
        if doc_dollar_parity == 1 and line_dollar_parity == 1:
            problems = True
            head, tail = line.split('$', 1)
            print('%04d: %s%s' % (i+1, head, tail), end="")
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


os.system("latexindent -w " + sys.argv[1])