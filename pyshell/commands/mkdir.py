from pathlib import Path
from pyshell.context import ShellContext


def run(args: list[str], context: ShellContext) -> None:
    """Create directory."""
    if not args:
        context.print("mkdir: missing operand")
        return

    folder_name = args[0]
    target = (
        Path(folder_name) if Path(folder_name).is_absolute() else (context.current_directory / folder_name).resolve()
    )

    if target.exists():
        context.print(f"mkdir: `{folder_name}` already exists.")
        return

    target.mkdir(parents=False, exist_ok=False)
