import sys
from pathlib import Path
from typing import TextIO, Optional


class ShellContext:
    """Maintains state for a PyShell session, including working directory and I/O streams."""

    def __init__(
        self,
        current_directory: Optional[Path] = None,
        stdout: Optional[TextIO] = None,
        stderr: Optional[TextIO] = None,
    ):
        self.current_directory: Path = (current_directory or Path.cwd()).resolve()
        self.running: bool = True
        self.stdout: TextIO = stdout if stdout is not None else sys.stdout
        self.stderr: TextIO = stderr if stderr is not None else sys.stderr

    def print(self, *args, **kwargs) -> None:
        """Helper to print to stdout (or context standard output stream)."""
        kwargs.setdefault("file", self.stdout)
        print(*args, **kwargs)

    def print_err(self, *args, **kwargs) -> None:
        """Helper to print to stderr (or context error output stream)."""
        kwargs.setdefault("file", self.stderr)
        print(*args, **kwargs)
