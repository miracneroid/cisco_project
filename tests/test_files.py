import io
import unittest
import tempfile
from pathlib import Path

from pyshell.context import ShellContext
from pyshell.commands import cat, cp, mv, rm, sizeof


class TestFileCommands(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root_path = Path(self.temp_dir.name).resolve()
        self.out = io.StringIO()
        self.err = io.StringIO()
        self.context = ShellContext(current_directory=self.root_path, stdout=self.out, stderr=self.err)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_cat(self):
        file_path = self.root_path / "a.txt"
        file_path.write_text("hello world\nsecond line\n")

        cat.run(["a.txt"], self.context)
        self.assertEqual(self.out.getvalue().strip(), "hello world\nsecond line")

    def test_cp(self):
        file_path = self.root_path / "a.txt"
        file_path.write_text("hello")
        (self.root_path / "target_dir").mkdir()

        cp.run(["a.txt", "target_dir"], self.context)
        copied_file = self.root_path / "target_dir" / "a.txt"
        self.assertTrue(copied_file.exists())
        self.assertEqual(copied_file.read_text(), "hello")

    def test_mv(self):
        file_path = self.root_path / "a.txt"
        file_path.write_text("hello")

        mv.run(["a.txt", "b.txt"], self.context)
        self.assertFalse((self.root_path / "a.txt").exists())
        self.assertTrue((self.root_path / "b.txt").exists())

    def test_rm_single_file(self):
        file_path = self.root_path / "a.txt"
        file_path.write_text("hello")

        rm.run(["a.txt"], self.context)
        self.assertFalse((self.root_path / "a.txt").exists())

    def test_rm_recursive_directory(self):
        dir_path = self.root_path / "folder"
        dir_path.mkdir()
        (dir_path / "sub.txt").write_text("sub")

        rm.run(["-r", "folder"], self.context)
        self.assertFalse(dir_path.exists())

    def test_sizeof(self):
        file_path = self.root_path / "a.txt"
        file_path.write_bytes(b"1234567890")  # 10 bytes

        sizeof.run(["a.txt"], self.context)
        self.assertIn("10 bytes", self.out.getvalue())


if __name__ == "__main__":
    unittest.main()
