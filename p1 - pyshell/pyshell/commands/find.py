from pyshell.commands import search
from pyshell.context import ShellContext


def run(args: list[str], context: ShellContext) -> None:
    """Find files matching a pattern (alias for search)."""
    search.run(args, context)
