import os
import fnmatch
from pathlib import Path
from pyshell.context import ShellContext


def run(args: list[str], context: ShellContext) -> None:
    """Recursively search for files matching a pattern."""
    search_dir = str(context.current_directory)
    file_pattern = "*"

    idx = 0
    while idx < len(args):
        arg = args[idx]
        if arg.startswith("--in="):
            search_dir = arg.split("=", 1)[1]
        elif arg == "--in" and idx + 1 < len(args):
            search_dir = args[idx + 1]
            idx += 1
        elif arg.startswith("--file="):
            file_pattern = arg.split("=", 1)[1]
        elif arg == "--file" and idx + 1 < len(args):
            file_pattern = args[idx + 1]
            idx += 1
        elif not arg.startswith("-"):
            file_pattern = arg
        idx += 1

    target_root = (
        Path(search_dir) if Path(search_dir).is_absolute() else (context.current_directory / search_dir).resolve()
    )

    if not target_root.exists():
        raise FileNotFoundError(f"[Errno 2] No such file or directory: '{search_dir}'")

    for root, dirs, files in os.walk(target_root, onerror=lambda err: None):
        for f in files:
            if f == file_pattern or fnmatch.fnmatch(f, file_pattern):
                full_path = os.path.join(root, f)
                context.print(full_path)
