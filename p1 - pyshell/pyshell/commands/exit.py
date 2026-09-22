from pyshell.context import ShellContext


def run(args: list[str], context: ShellContext) -> None:
    """Exit the shell."""
    context.running = False
    context.print("PyShell exited.")
