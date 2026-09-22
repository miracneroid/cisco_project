import shutil
from pathlib import Path
from pyshell.context import ShellContext


def run(args: list[str], context: ShellContext) -> None:
    """Move/rename file or directory."""
    if len(args) < 2:
        context.print("mv: missing file operand")
        return

    src_path = args[0]
    dest_path = args[1]
    src = Path(src_path) if Path(src_path).is_absolute() else (context.current_directory / src_path).resolve()
    dest = Path(dest_path) if Path(dest_path).is_absolute() else (context.current_directory / dest_path).resolve()

    if not src.exists():
        raise FileNotFoundError(f"[Errno 2] No such file or directory: '{src_path}'")

    shutil.move(str(src), str(dest))
