import os
import sys
import glob
from typing import Optional
from pyshell.context import ShellContext
from pyshell.parser import parse_line
from pyshell.loader import load_command, get_available_commands
from pyshell.errors import CommandNotFoundError, PyShellError

try:
    import readline
except ImportError:
    readline = None


class PyShellCompleter:
    """Tab completion handler for PyShell (completes commands and file paths)."""

    def __init__(self, context: ShellContext):
        self.context = context

    def complete(self, text: str, state: int) -> Optional[str]:
        buffer = readline.get_line_buffer() if readline else ""
        tokens = buffer.lstrip().split()

        # Completing command name (first word)
        if not tokens or (len(tokens) == 1 and not buffer.endswith(" ")):
            commands = get_available_commands()
            matches = [cmd for cmd in commands if cmd.startswith(text)]
        else:
            # Completing file / directory path
            pattern = text + "*"
            raw_matches = glob.glob(pattern)
            matches = []
            for path_str in raw_matches:
                if os.path.isdir(path_str):
                    matches.append(path_str + "/")
                else:
                    matches.append(path_str)

        if state < len(matches):
            return matches[state]
        return None


class PyShell:
    """Main execution engine for the PyShell application."""

    def __init__(self, context: Optional[ShellContext] = None):
        self.context = context or ShellContext()
        self._init_readline()

    def _init_readline(self) -> None:
        """Configure readline for arrow key command history and tab autocompletion."""
        if readline is None:
            return

        completer = PyShellCompleter(self.context)
        readline.set_completer(completer.complete)

        # Tab completion binding
        if sys.platform == "darwin":
            readline.parse_and_bind("bind ^I rl_complete")
        else:
            readline.parse_and_bind("tab: complete")

        # Command history file
        history_file = os.path.expanduser("~/.pyshell_history")
        try:
            if os.path.exists(history_file):
                readline.read_history_file(history_file)
            import atexit
            atexit.register(lambda: readline.write_history_file(history_file))
        except Exception:
            pass

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
