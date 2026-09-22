from pathlib import Path
from pyshell.context import ShellContext


def run(args: list[str], context: ShellContext) -> None:
    """Remove empty directory."""
    if not args:
        context.print("rmdir: missing operand")
        return

    folder_name = args[0]
    target = (
        Path(folder_name) if Path(folder_name).is_absolute() else (context.current_directory / folder_name).resolve()
    )

    if not target.exists():
        raise FileNotFoundError(f"[Errno 2] No such file or directory: '{folder_name}'")
    if not target.is_dir():
        raise NotADirectoryError(f"[Errno 20] Not a directory: '{folder_name}'")

    if any(target.iterdir()):
        context.print(f"rmdir: `{folder_name}` is not empty.")
        return

    target.rmdir()
