import re
from pathlib import Path
from pyshell.context import ShellContext


def run(args: list[str], context: ShellContext) -> None:
    """Search for matching regex patterns in a file."""
    if not args:
        context.print("grep: missing pattern and file operand")
        return

    show_line_numbers = False
    clean_args = []
    for arg in args:
        if arg == "-n":
            show_line_numbers = True
        else:
            clean_args.append(arg)

    if len(clean_args) < 2:
        context.print("grep: missing pattern or file operand")
        return

    pattern = clean_args[0]
    filename = clean_args[1]

    target = (
        Path(filename) if Path(filename).is_absolute() else (context.current_directory / filename).resolve()
    )

    if not target.exists():
        raise FileNotFoundError(f"[Errno 2] No such file or directory: '{filename}'")
    if target.is_dir():
        raise IsADirectoryError(f"[Errno 21] Is a directory: '{filename}'")

    compiled = re.compile(pattern)
    with target.open("r", encoding="utf-8", errors="replace") as f:
        for line_no, line in enumerate(f, start=1):
            line_str = line.rstrip("\r\n")
            if compiled.search(line_str):
                if show_line_numbers:
                    context.print(f"{filename}:{line_no}:{line_str}")
                else:
                    context.print(line_str)
