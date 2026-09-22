import shlex
from typing import List, Tuple


def parse_line(line: str) -> Tuple[str, List[str]]:
    """Parse a raw shell command line into a command name and argument list using shlex."""
    line = line.strip()
    if not line:
        return "", []
    try:
        tokens = shlex.split(line)
    except ValueError as e:
        # Handle unclosed quotes or syntax errors in shlex gracefully
        tokens = line.split()

    if not tokens:
        return "", []
    return tokens[0], tokens[1:]
