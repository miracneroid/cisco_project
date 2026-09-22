import io
import unittest
import tempfile
from pathlib import Path

from pyshell.context import ShellContext
from pyshell.commands import pwd, cd, ls, mkdir, rmdir


class TestNavigationCommands(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root_path = Path(self.temp_dir.name).resolve()
        self.out = io.StringIO()
        self.err = io.StringIO()
        self.context = ShellContext(current_directory=self.root_path, stdout=self.out, stderr=self.err)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_pwd(self):
        pwd.run([], self.context)
        self.assertEqual(self.out.getvalue().strip(), str(self.root_path))

    def test_mkdir_and_ls(self):
        mkdir.run(["testfolder"], self.context)
        self.assertTrue((self.root_path / "testfolder").is_dir())

        self.out.seek(0)
        self.out.truncate(0)

        ls.run([], self.context)
        self.assertEqual(self.out.getvalue().strip(), "testfolder")

    def test_mkdir_already_exists(self):
        mkdir.run(["testfolder"], self.context)
        self.out.seek(0)
        self.out.truncate(0)

        mkdir.run(["testfolder"], self.context)
        self.assertIn("mkdir: `testfolder` already exists.", self.out.getvalue())

    def test_cd_and_pwd(self):
        mkdir.run(["testfolder"], self.context)
        cd.run(["testfolder"], self.context)
        self.assertEqual(self.context.current_directory, (self.root_path / "testfolder").resolve())

        cd.run([".."], self.context)
        self.assertEqual(self.context.current_directory, self.root_path)

    def test_rmdir_empty(self):
        mkdir.run(["empty_folder"], self.context)
        rmdir.run(["empty_folder"], self.context)
        self.assertFalse((self.root_path / "empty_folder").exists())

    def test_rmdir_non_empty(self):
        mkdir.run(["non_empty"], self.context)
        (self.root_path / "non_empty" / "file.txt").write_text("hello")
        
        self.out.seek(0)
        self.out.truncate(0)

        rmdir.run(["non_empty"], self.context)
        self.assertIn("rmdir: `non_empty` is not empty.", self.out.getvalue())
        self.assertTrue((self.root_path / "non_empty").exists())


if __name__ == "__main__":
    unittest.main()
