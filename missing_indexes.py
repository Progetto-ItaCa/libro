import re
import glob
import os

def find_missing_index_in_file(filename, output_file):
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    valid_envs = re.compile(r'\\begin{h?(theorem|corollary|proposition|lemma|definition|notation|remark|conjecture|axiom|example|examples|exercise|exercises|counterexample|construction|warning|digression|perspective|discussion|terminology|heuristics)}', re.IGNORECASE)
    
    for i, line in enumerate(lines):
        if valid_envs.search(line) and not re.search(r'\\index{.*?}', line):
            prev_line = lines[i - 1].strip() if i > 0 else "(No previous line)"
            next_line = lines[i + 1].strip() if i < len(lines) - 1 else "(No next line)"
            print(f"> {prev_line}")
            print(f"L{i+1}: {line.strip()} < no '\index' found")
            print(f"> {next_line}\n")

def find_missing_index(directory="cap/01/sec/", output_filename="missing_indices.idx"):
    tex_files = glob.glob(os.path.join(directory, "*.tex"))
    with open(output_filename, 'w', encoding='utf-8') as output_file:
        for tex_file in tex_files:
            find_missing_index_in_file(tex_file, output_file)

# Example usage:
find_missing_index()