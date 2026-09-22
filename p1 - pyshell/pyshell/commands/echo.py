from pathlib import Path
from pyshell.context import ShellContext


def run(args: list[str], context: ShellContext) -> None:
    """Print text to terminal or write/append text to a file."""
    if not args:
        context.print("")
        return

    append_mode = False
    target_file = None
    content_words = []

    if ">>" in args:
        idx = args.index(">>")
        append_mode = True
        content_words = args[:idx]
        if idx + 1 < len(args):
            target_file = args[idx + 1]
    elif ">" in args:
        idx = args.index(">")
        append_mode = False
        content_words = args[:idx]
        if idx + 1 < len(args):
            target_file = args[idx + 1]
    elif len(args) >= 2:
        # Check if last argument looks like a target filename (e.g. echo "text" file.txt)
        potential_path = (
            Path(args[-1]) if Path(args[-1]).is_absolute() else (context.current_directory / args[-1])
        )
        if not potential_path.is_dir() and (potential_path.parent.exists() or potential_path.exists()):
            content_words = args[:-1]
            target_file = args[-1]
        else:
            content_words = args
    else:
        content_words = args

    text = " ".join(content_words)

    if target_file:
        target_path = (
            Path(target_file) if Path(target_file).is_absolute() else (context.current_directory / target_file)
        ).resolve()
        mode = "a" if append_mode else "w"
        with target_path.open(mode, encoding="utf-8") as f:
            f.write(text + "\n")
        context.print(f"Written to `{target_file}`.")
    else:
        context.print(text)
