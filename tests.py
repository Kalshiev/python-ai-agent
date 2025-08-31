from functions.run_python import run_python_file as run

cases = [
    ("calculator", "main.py"),
    ("calculator", "main.py", ["3 + 5"]),
    ("calculator", "tests.py"),
    ("calculator", "../main.py"),
    ("calculator", "nonexistent.py")
]

def run_cases(workspace, file, args=[]):
    print(run(workspace, file, args))

for case in cases:
    run_cases(*case)