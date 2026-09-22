import shutil
from pathlib import Path
from pyshell.context import ShellContext


def run(args: list[str], context: ShellContext) -> None:
    """Remove files or directories (with -r switch)."""
    if not args:
        context.print("rm: missing operand")
        return

    recursive = False
    targets = []
    for arg in args:
        if arg in ("-r", "-R", "-rf", "-fr"):
            recursive = True
        else:
            targets.append(arg)

    if not targets:
        context.print("rm: missing operand")
        return

    for target_str in targets:
        target = (
            Path(target_str) if Path(target_str).is_absolute() else (context.current_directory / target_str).resolve()
        )

        if not target.exists():
            raise FileNotFoundError(f"[Errno 2] No such file or directory: '{target_str}'")

        if target.is_dir():
            if not recursive:
                context.print(f"rm: {target_str}: is a directory")
                return
            shutil.rmtree(target)
        else:
            target.unlink()
