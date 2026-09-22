import getpass
from pyshell.context import ShellContext


def run(args: list[str], context: ShellContext) -> None:
    """Print current username."""
    context.print(getpass.getuser())
