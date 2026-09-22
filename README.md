# PyShell - Modular UNIX-like Shell in Python

`PyShell` is a modular, scalable UNIX-like shell implemented purely in Python using standard-library APIs. It demonstrates a dynamic plugin-like command architecture without executing external Unix binary processes or subprocesses.

---

## 🏗️ Architecture & Core Principles

- **Pure Standard Library**: Built entirely using Python's standard library (`pathlib`, `shutil`, `os`, `re`, `datetime`, `getpass`, `socket`, `shlex`, `importlib`, `argparse`, `time`, `unittest`).
- **Dynamic Plugin Loader**: Commands are dynamically loaded from `pyshell/commands/<cmd>.py` at runtime via `importlib`.
- **Decoupled Engine**:
  - `context.py`: Maintains session state (working directory, I/O streams, execution status).
  - `parser.py`: Shell line tokenization via `shlex.split()`.
  - `loader.py`: Dynamic module importer and entry point validator.
  - `shell.py`: Interactive REPL engine and error handling.
  - `commands/*.py`: Self-contained command logic implementing `run(args, context)`.

---

## 📁 Project Structure

```text
cisco_project/
├── pyshell/
│   ├── __init__.py
│   ├── main.py          # Entrypoint script
│   ├── shell.py         # REPL engine
│   ├── parser.py        # Line parsing with shlex
│   ├── loader.py        # Dynamic command importer
│   ├── context.py       # Shell state container
│   ├── errors.py        # Custom exceptions
│   └── commands/
│       ├── __init__.py
│       ├── ls.py
│       ├── mkdir.py
│       ├── pwd.py
│       ├── rmdir.py
│       ├── cd.py
│       ├── cat.py
│       ├── cp.py
│       ├── rm.py
│       ├── mv.py
│       ├── grep.py
│       ├── head.py
│       ├── tail.py
│       ├── sizeof.py
│       ├── search.py
│       ├── date.py
│       ├── whoami.py
│       ├── hostname.py
│       ├── timeit.py
│       └── exit.py
├── tests/
│   ├── __init__.py
│   ├── test_navigation.py
│   ├── test_files.py
│   ├── test_commands.py
│   └── test_shell.py
├── README.md
└── requirements.txt
```

---

## 💻 Supported Commands

| Category | Command | Description / Supported Flags |
| :--- | :--- | :--- |
| **Directory** | `ls [path]` | List contents of current or specified directory |
| | `mkdir <dir>` | Create directory (warns if directory exists) |
| | `pwd` | Print current working directory |
| | `rmdir <dir>` | Remove directory (error if directory is non-empty) |
| | `cd <dir>` | Change working directory (`..`, `/`, relative/absolute) |
| **File** | `cat <file>` | Print file contents |
| | `cp <src> <dest>` | Copy file or directory tree |
| | `rm [-r] <path>` | Remove file or recursively delete directory (`-r`) |
| | `mv <src> <dest>` | Move or rename file or directory |
| | `grep [-n] <pattern> <file>` | Regular expression search (`-n` outputs line numbers) |
| | `head [-N] <file>` | Output first N lines of a file |
| | `tail [-N] <file>` | Output last N lines of a file |
| | `sizeof <file>` | Print file size in bytes |
| | `search [--in=<dir>] [--file=<pattern>]` | Recursive file search |
| **System** | `date` | Output current date and time |
| | `whoami` | Output current logged-in username |
| | `hostname` | Output system network hostname |
| | `timeit <cmd ...>` | Measure and print elapsed execution time of command |
| | `exit` | Terminate the shell session |

---

## 🚀 Running PyShell

To start the interactive shell, run:

```bash
python3 -m pyshell.main
```

---

## 🧪 Running Unit Tests

Run the full `unittest` suite using standard Python:

```bash
python3 -m unittest discover -s tests -p "test_*.py"
```

---

## 🧩 How to Add a New Command

To add a new command (e.g. `touch`):

1. Create a new file in `pyshell/commands/touch.py`:
   ```python
   from pathlib import Path
   from pyshell.context import ShellContext

   def run(args: list[str], context: ShellContext) -> None:
       if not args:
           context.print("touch: missing file operand")
           return
       target = (Path(args[0]) if Path(args[0]).is_absolute() else context.current_directory / args[0]).resolve()
       target.touch()
   ```
2. Save the file.
3. Start `PyShell`. The command `touch` is instantly available without editing any core shell code!

---

## 📝 Example Session

```text
PyShell> pwd
/Users/developer/cisco_project

PyShell> mkdir testfolder

PyShell> cd testfolder

PyShell> pwd
/Users/developer/cisco_project/testfolder

PyShell> cd ..

PyShell> sizeof py_project1.html
9936 bytes

PyShell> timeit ls /
bin dev etc home lib opt root sbin tmp usr
`ls /` took 0.00042 seconds.

PyShell> sdfsdf
`sdfsdf` is an invalid command

PyShell> exit
PyShell exited.
```
