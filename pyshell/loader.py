import importlib
from pathlib import Path
from typing import Callable, Any, List
from pyshell.errors import CommandNotFoundError


def get_available_commands() -> List[str]:
    """Return a list of all available command names in the commands directory."""
    commands = set()
    # Check pyshell/commands directory
    pkg_cmd_dir = Path(__file__).parent / "commands"
    if pkg_cmd_dir.exists():
        for f in pkg_cmd_dir.glob("*.py"):
            if f.name != "__init__.py":
                commands.add(f.stem)

    # Check root commands directory if present
    root_cmd_dir = Path.cwd() / "commands"
    if root_cmd_dir.exists():
        for f in root_cmd_dir.glob("*.py"):
            if f.name != "__init__.py":
                commands.add(f.stem)

    return sorted(list(commands))


def load_command(command_name: str) -> Callable[..., Any]:
    """Dynamically import a command module from pyshell.commands or commands and return its run function."""
    module_names = [f"pyshell.commands.{command_name}", f"commands.{command_name}"]

    module = None
    last_exception = None

    for m_name in module_names:
        try:
            module = importlib.import_module(m_name)
            break
        except ModuleNotFoundError as e:
            last_exception = e
            continue

    if module is None:
        raise CommandNotFoundError(command_name) from last_exception

    if not hasattr(module, "run") or not callable(getattr(module, "run")):
        raise AttributeError(f"Command module '{command_name}' does not export a callable 'run' function.")

    return getattr(module, "run")
