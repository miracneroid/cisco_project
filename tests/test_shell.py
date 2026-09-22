import io
import unittest
import tempfile
from pathlib import Path

from pyshell.context import ShellContext
from pyshell.shell import PyShell
from pyshell.loader import load_command
from pyshell.errors import CommandNotFoundError


class TestShellCore(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root_path = Path(self.temp_dir.name).resolve()
        self.out = io.StringIO()
        self.err = io.StringIO()
        self.context = ShellContext(current_directory=self.root_path, stdout=self.out, stderr=self.err)
        self.shell = PyShell(self.context)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_dynamic_loader_success(self):
        run_func = load_command("pwd")
        self.assertTrue(callable(run_func))

    def test_dynamic_loader_not_found(self):
        with self.assertRaises(CommandNotFoundError):
            load_command("nonexistentcommand")

    def test_shell_invalid_command(self):
        self.shell.execute_line("sdfsdf")
        self.assertIn("`sdfsdf` is an invalid command", self.out.getvalue())

    def test_shell_file_not_found_unhandled(self):
        self.shell.execute_line("ls nonexistent_file_xyz")
        self.assertIn("*** Unhandled `FileNotFoundError` exception:", self.out.getvalue())

    def test_timeit_command(self):
        f = self.root_path / "a.txt"
        f.write_text("hello")
        self.shell.execute_line("timeit cp a.txt b.txt")
        self.assertTrue((self.root_path / "b.txt").exists())
        self.assertIn("took", self.out.getvalue())

    def test_exit_command(self):
        self.shell.execute_line("exit")
        self.assertFalse(self.context.running)
        self.assertIn("PyShell exited.", self.out.getvalue())


if __name__ == "__main__":
    unittest.main()
