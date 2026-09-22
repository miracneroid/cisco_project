from pathlib import Path
from pyshell.context import ShellContext


def run(args: list[str], context: ShellContext) -> None:
    """Change current directory."""
    if not args:
        target = Path.home()
    else:
        path_str = args[0]
        if path_str == "/":
            target = Path("/")
        else:
            target = (
                Path(path_str) if Path(path_str).is_absolute() else (context.current_directory / path_str).resolve()
            )

    if not target.exists():
        raise FileNotFoundError(f"[Errno 2] No such file or directory: '{args[0]}'")
    if not target.is_dir():
        raise NotADirectoryError(f"[Errno 20] Not a directory: '{args[0]}'")

    context.current_directory = target.resolve()
