from pathlib import Path
from pyshell.context import ShellContext


def run(args: list[str], context: ShellContext) -> None:
    """List directory contents."""
    if not args:
        target_dir = context.current_directory
    else:
        path_str = args[0]
        target_dir = (
            Path(path_str) if Path(path_str).is_absolute() else (context.current_directory / path_str).resolve()
        )

    if not target_dir.exists():
        raise FileNotFoundError(f"[Errno 2] No such file or directory: '{args[0]}'")

    if target_dir.is_file():
        context.print(target_dir.name)
        return

    items = sorted([item.name for item in target_dir.iterdir()])
    context.print(" ".join(items))
