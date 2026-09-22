import io
import unittest
import tempfile
from pathlib import Path

from pyshell.context import ShellContext
from pyshell.commands import grep, head, tail, search, date, whoami, hostname


class TestTextAndMiscCommands(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root_path = Path(self.temp_dir.name).resolve()
        self.out = io.StringIO()
        self.err = io.StringIO()
        self.context = ShellContext(current_directory=self.root_path, stdout=self.out, stderr=self.err)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_grep(self):
        f = self.root_path / "sample.txt"
        f.write_text("line one\nline two\nline seven\n")

        grep.run(["seven", "sample.txt"], self.context)
        self.assertEqual(self.out.getvalue().strip(), "line seven")

    def test_grep_with_line_number(self):
        f = self.root_path / "sample.txt"
        f.write_text("line one\nline two\nline seven\n")

        grep.run(["-n", "seven", "sample.txt"], self.context)
        self.assertEqual(self.out.getvalue().strip(), "sample.txt:3:line seven")

    def test_head(self):
        f = self.root_path / "sample.txt"
        f.write_text("line1\nline2\nline3\nline4\nline5\n")

        head.run(["-3", "sample.txt"], self.context)
        self.assertEqual(self.out.getvalue().strip(), "line1\nline2\nline3")

    def test_tail(self):
        f = self.root_path / "sample.txt"
        f.write_text("line1\nline2\nline3\nline4\nline5\n")

        tail.run(["-2", "sample.txt"], self.context)
        self.assertEqual(self.out.getvalue().strip(), "line4\nline5")

    def test_search(self):
        sub_dir = self.root_path / "subdir"
        sub_dir.mkdir()
        target_file = sub_dir / "target.txt"
        target_file.write_text("content")

        search.run([f"--in={self.root_path}", "--file=target.txt"], self.context)
        self.assertIn("target.txt", self.out.getvalue())

    def test_misc_commands(self):
        date.run([], self.context)
        self.assertTrue(len(self.out.getvalue().strip()) > 0)

        self.out.seek(0)
        self.out.truncate(0)
        whoami.run([], self.context)
        self.assertTrue(len(self.out.getvalue().strip()) > 0)

        self.out.seek(0)
        self.out.truncate(0)
        hostname.run([], self.context)
        self.assertTrue(len(self.out.getvalue().strip()) > 0)


if __name__ == "__main__":
    unittest.main()
