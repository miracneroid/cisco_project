import sys
from pyshell.shell import PyShell
from pyshell.context import ShellContext


def main() -> None:
    context = ShellContext()
    shell = PyShell(context)
    shell.run()


if __name__ == "__main__":
    main()
