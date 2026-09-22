import socket
from pyshell.context import ShellContext


def run(args: list[str], context: ShellContext) -> None:
    """Print system hostname."""
    context.print(socket.gethostname())
