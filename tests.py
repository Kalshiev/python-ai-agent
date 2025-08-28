from functions.get_files_info import *

cases = [
    ("calculator", "."),
    ("calculator", "pkg"),
    ("calculator", "/bin"),
    ("calculator", "../")
]

def run_cases(target, dir):
    if dir == ".":
        print("\n".join(
            [f"Result for current directory:", get_files_info(target, dir)]
        ))
    else:
        print("\n".join(
            [f"Result for '{dir}' directory:", get_files_info(target, dir)]
        ))

for case in cases:
    run_cases(*case)