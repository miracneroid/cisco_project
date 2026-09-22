from pyshell.context import ShellContext


def run(args: list[str], context: ShellContext) -> None:
    """Print working directory."""
    context.print(str(context.current_directory))
