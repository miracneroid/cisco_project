from pyshell.context import ShellContext


def run(args: list[str], context: ShellContext) -> None:
    """Clear terminal screen and scrollback buffer."""
    context.stdout.write("\033[2J\033[H\033[3J")
    context.stdout.flush()

