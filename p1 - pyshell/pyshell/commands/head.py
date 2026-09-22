from pathlib import Path
from pyshell.context import ShellContext


def run(args: list[str], context: ShellContext) -> None:
    """Print first N lines of a file."""
    if not args:
        context.print("head: missing file operand")
        return

    num_lines = 10
    filename = None

    idx = 0
    while idx < len(args):
        arg = args[idx]
        if arg.startswith("-") and arg[1:].isdigit():
            num_lines = int(arg[1:])
        elif arg == "-n" and idx + 1 < len(args) and args[idx + 1].isdigit():
            num_lines = int(args[idx + 1])
            idx += 1
        else:
            filename = arg
        idx += 1

    if not filename:
        context.print("head: missing file operand")
        return

    target = (
        Path(filename) if Path(filename).is_absolute() else (context.current_directory / filename).resolve()
    )

    if not target.exists():
        raise FileNotFoundError(f"[Errno 2] No such file or directory: '{filename}'")
    if target.is_dir():
        raise IsADirectoryError(f"[Errno 21] Is a directory: '{filename}'")

    lines = []
    with target.open("r", encoding="utf-8", errors="replace") as f:
        for _ in range(num_lines):
            line = f.readline()
            if not line:
                break
            lines.append(line.rstrip("\r\n"))

    for l in lines:
        context.print(l)
