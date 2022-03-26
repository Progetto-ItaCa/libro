#!/usr/bin/env python3
import re, os, sys

good_delims = lambda x: re.sub(r"\$(.*?)\$", r"\\(\1\\)", x, flags = re.M)

with open (sys.argv[1], 'r+' ) as f:
    content = f.read()
    content = good_delims(content)
    f.seek(0)
    f.write(content)
    f.truncate()

os.system("latexindent -w " + sys.argv[1])