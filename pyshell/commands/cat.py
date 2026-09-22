from pathlib import Path
from pyshell.context import ShellContext


def run(args: list[str], context: ShellContext) -> None:
    """Print contents of a file."""
    if not args:
        context.print("cat: missing file operand")
        return

    path_str = args[0]
    target = (
        Path(path_str) if Path(path_str).is_absolute() else (context.current_directory / path_str).resolve()
    )

    if not target.exists():
        raise FileNotFoundError(f"[Errno 2] No such file or directory: '{path_str}'")
    if target.is_dir():
        raise IsADirectoryError(f"[Errno 21] Is a directory: '{path_str}'")

    with target.open("r", encoding="utf-8", errors="replace") as f:
        content = f.read()
        context.print(content, end="" if content.endswith("\n") else "\n")
