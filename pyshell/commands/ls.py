from pathlib import Path
from pyshell.context import ShellContext


def run(args: list[str], context: ShellContext) -> None:
    """List directory contents (supports -r or -R for recursive listing)."""
    recursive = False
    clean_args = []
    for arg in args:
        if arg in ("-r", "-R", "-recursive"):
            recursive = True
        else:
            clean_args.append(arg)

    if not clean_args:
        target_dir = context.current_directory
    else:
        path_str = clean_args[0]
        target_dir = (
            Path(path_str) if Path(path_str).is_absolute() else (context.current_directory / path_str).resolve()
        )

    if not target_dir.exists():
        raise FileNotFoundError(f"[Errno 2] No such file or directory: '{clean_args[0] if clean_args else '.'}'")

    if target_dir.is_file():
        context.print(target_dir.name)
        return

    if not recursive:
        items = sorted([item.name for item in target_dir.iterdir()])
        context.print(" ".join(items))
    else:
        def list_recursive(d: Path, prefix: str = ""):
            context.print(f"{d}:")
            items = sorted(list(d.iterdir()), key=lambda x: x.name)
            context.print(" ".join([item.name for item in items]))
            context.print()
            for item in items:
                if item.is_dir():
                    list_recursive(item)

        list_recursive(target_dir)
