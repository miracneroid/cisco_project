import importlib
from typing import Callable, Any
from pyshell.errors import CommandNotFoundError


def load_command(command_name: str) -> Callable[..., Any]:
    """Dynamically import a command module from pyshell.commands and return its run function."""
    module_name = f"pyshell.commands.{command_name}"
    try:
        module = importlib.import_module(module_name)
    except ModuleNotFoundError as e:
        # Verify if missing module is the command itself or an internal import error
        if e.name == module_name or e.name == command_name:
            raise CommandNotFoundError(command_name) from e
        raise e

    if not hasattr(module, "run") or not callable(getattr(module, "run")):
        raise AttributeError(f"Command module '{command_name}' does not export a callable 'run' function.")

    return getattr(module, "run")
