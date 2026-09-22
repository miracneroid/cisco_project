class PyShellError(Exception):
    """Base exception for PyShell errors."""
    pass


class CommandNotFoundError(PyShellError):
    """Exception raised when a requested command module cannot be found."""

    def __init__(self, command_name: str):
        self.command_name = command_name
        super().__init__(f"`{command_name}` is an invalid command")
