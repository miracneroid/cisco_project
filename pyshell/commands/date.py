import datetime
from pyshell.context import ShellContext


def run(args: list[str], context: ShellContext) -> None:
    """Print current date and time."""
    now = datetime.datetime.now()
    context.print(now.strftime("%a %b %d %H:%M:%S %Y"))
