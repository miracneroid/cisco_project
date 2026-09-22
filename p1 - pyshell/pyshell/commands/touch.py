from pathlib import Path
from pyshell.context import ShellContext


def run(args: list[str], context: ShellContext) -> None:
    """Create empty file or update timestamp."""
    if not args:
        context.print("touch: missing file operand")
        return

    for filename in args:
        target = (
            Path(filename) if Path(filename).is_absolute() else (context.current_directory / filename)
        ).resolve()
        target.touch()
