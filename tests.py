from functions.get_file_content import get_file_content
from functions.config import MAX_CHARS

cases = [
    ("calculator", "lorem.txt"),
    ("calculator", "main.py"),
    ("calculator", "pkg/calculator.py"),
    ("calculator", "/bin/cat"),
    ("calculator", "pkg/does_not_exist.py")
]

def run_cases(target, file):
    print(f"--- Getting content of '{file}' in '{target}' ---")
    print(get_file_content(target, file))

for case in cases:
    run_cases(*case)