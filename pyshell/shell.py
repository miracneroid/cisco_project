from typing import Optional
from pyshell.context import ShellContext
from pyshell.parser import parse_line
from pyshell.loader import load_command
from pyshell.errors import CommandNotFoundError, PyShellError


class PyShell:
    """Main execution engine for the PyShell application."""

    def __init__(self, context: Optional[ShellContext] = None):
        self.context = context or ShellContext()

    def execute_line(self, line: str) -> Optional[int]:
        """Parse and execute a single line of shell input."""
        line = line.strip()
        if not line:
            return None

        cmd_name, args = parse_line(line)
        if not cmd_name:
            return None

        try:
            run_func = load_command(cmd_name)
            return run_func(args, self.context)
        except CommandNotFoundError as e:
            self.context.print(str(e))
        except FileNotFoundError as e:
            self.context.print(f"*** Unhandled `FileNotFoundError` exception: {e}")
        except PyShellError as e:
            self.context.print(str(e))
        except Exception as e:
            exc_name = type(e).__name__
            self.context.print(f"*** Unhandled `{exc_name}` exception: {e}")

        return None

    def run(self) -> None:
        """Run the interactive REPL loop."""
        while self.context.running:
            try:
                line = input("PyShell> ")
                self.execute_line(line)
            except (EOFError, KeyboardInterrupt):
                self.context.print("\nPyShell exited.")
                break
