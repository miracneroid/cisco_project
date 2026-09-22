from pathlib import Path
from pyshell.context import ShellContext


def run(args: list[str], context: ShellContext) -> None:
    """Print file size in bytes."""
    if not args:
        context.print("sizeof: missing file operand")
        return

    target_str = args[0]
    target = (
        Path(target_str) if Path(target_str).is_absolute() else (context.current_directory / target_str).resolve()
    )

    if not target.exists():
        raise FileNotFoundError(f"[Errno 2] No such file or directory: '{target_str}'")

    size = target.stat().st_size
    context.print(f"{size} bytes")
