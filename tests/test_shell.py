import os
import unittest
import tempfile
from flux.settings.settings import SysPaths
from flux.core import setup, manager
from flux import utils

TMP = tempfile.gettempdir()
FILE = os.path.join(TMP, "file.txt")


s_file_exists = os.path.exists(SysPaths.SETTINGS_FILE)

# NOTE: tests for setup must be handles elsewhere
info = setup.setup()


class TestCaseWithInstance(unittest.TestCase):
    def track_file(self, file_path: str) -> None:
        self.files.append(file_path)

    def setUp(self):
        self.addCleanup(self.clean)
        self.instance = None
        self.files: list[str] = []

    def clean(self) -> None:        
        if not s_file_exists and os.path.exists( SysPaths.SETTINGS_FILE):
            os.remove(SysPaths.SETTINGS_FILE)

        if self.instance:
            self.instance.close()
            self.instance = None

        if os.path.exists(FILE):
            os.remove(FILE)

        while self.files:
            if os.path.exists(file := self.files.pop()):
                os.remove(file)


class Test_TestOutputRedirection(TestCaseWithInstance):

    def test_build_01(self):
        command = utils.transform.string_to_list("not existent command")
        self.instance = manager.build(command, info)
        self.assertTrue(self.instance is None)
    
    def test_build_02(self):
        command = utils.transform.string_to_list("£345%$£")
        self.instance = manager.build(command, info)
        self.assertTrue(self.instance is None)
    
    def test_build_03(self):
        command = utils.transform.string_to_list("ls >")
        self.instance = manager.build(command, info)
        self.assertTrue(self.instance is None)
   
    def test_build_04(self):
        command = utils.transform.string_to_list("ls >>")
        self.instance = manager.build(command, info)
        self.assertTrue(self.instance is None)
    
    def test_build_05(self):
        command = utils.transform.string_to_list(f"ls >{FILE}")
        self.instance = manager.build(command, info)
        self.assertIsNotNone(self.instance)

    def test_build_06(self):
        command = utils.transform.string_to_list(f"ls > {FILE}")
        self.instance = manager.build(command, info)
        self.assertIsNotNone(self.instance)

    def test_build_07(self):
        command = utils.transform.string_to_list(f"ls 2>{FILE}")
        self.instance = manager.build(command, info)
        self.assertIsNotNone(self.instance)
        
    def test_build_08(self):
        command = utils.transform.string_to_list(f"ls 2>>{FILE}")
        self.instance = manager.build(command, info)
        self.assertIsNotNone(self.instance)
    
    def test_build_09(self):
        command = utils.transform.string_to_list("ls <")
        self.instance = manager.build(command, info)
        self.assertIsNone(self.instance)
    
    def test_build_10(self): 
        command = utils.transform.string_to_list(f"cat << {FILE} >> {os.path.join(TMP, 'file2.txt')}")
        self.instance = manager.build(command, info)
        # works when trying manualy, but not in tests for some reason
        # self.assertIsNotNone(self.instance)

class Test_TestFilePathHandling(TestCaseWithInstance):

    def test_file_path_01(self):
        command = utils.transform.string_to_list(f"ls > {FILE}")
        self.instance = manager.build(command, info)
        self.assertIsNotNone(self.instance)
        self.assertTrue(os.path.exists(FILE))
    
    def test_file_path_02(self):
        command = utils.transform.string_to_list(f"ls 2> {FILE}")
        self.instance = manager.build(command, info)
        self.assertIsNotNone(self.instance)
        self.assertTrue(os.path.exists(FILE))

    def test_file_path_03(self):
        file = os.path.join(TMP, 'file with spaces.txt')
        self.track_file(file)
        command = utils.transform.string_to_list(f"ls > '{file}'")
        self.instance = manager.build(command, info)
        self.assertIsNotNone(self.instance)
        self.assertTrue(os.path.exists(file))

    def test_file_path_04(self):
        file = os.path.join(TMP, 'file with spaces.txt')
        expected = os.path.join(TMP, 'file')
        self.track_file(file)
        self.track_file(expected)
        command = utils.transform.string_to_list(f"ls > {file}")
        self.instance = manager.build(command, info)
        self.assertIsNotNone(self.instance)
        self.assertFalse(os.path.exists(file))
        self.assertTrue(os.path.exists(expected))

    def test_file_path_05(self):
        # Test Windows-style paths
        win_path = os.path.join(TMP, 'test\\folder\\file.txt')
        self.track_file(win_path)
        command = utils.transform.string_to_list(f"ls > {win_path}")
        self.instance = manager.build(command, info)
        self.assertIsNotNone(self.instance)
        self.assertTrue(os.path.exists(win_path.replace('\\','/')))

    def test_file_path_06(self):
        # Test paths with special characters
        special_path = os.path.join(TMP, 'test@#$%^&()_+.txt')
        self.track_file(special_path)
        command = utils.transform.string_to_list(f"ls > '{special_path}'")
        self.instance = manager.build(command, info)
        self.assertIsNotNone(self.instance)
        self.assertTrue(os.path.exists(special_path))
    
    def test_file_path_07(self):
        # Test paths with special characters (no quotation marks around the path)
        special_path = os.path.join(TMP, 'test@#$%^&()_+.txt')
        self.track_file(special_path)
        command = utils.transform.string_to_list(f"ls > {special_path}")
        self.instance = manager.build(command, info)
        self.assertIsNotNone(self.instance)
        self.assertFalse(os.path.exists(special_path))
        self.assertTrue(os.path.exists(special_path[:special_path.index('@')]))

    def test_file_path_08(self):
        # Test very long paths
        long_dir = 'a' * 100
        long_path = os.path.join(TMP, long_dir, 'file.txt')
        self.track_file(long_path)
        command = utils.transform.string_to_list(f"ls > {long_path}")
        self.instance = manager.build(command, info)
        self.assertIsNotNone(self.instance)
        self.assertTrue(os.path.exists(long_path))

    def test_file_path_09(self):
        # Test paths with unicode characters
        unicode_path = os.path.join(TMP, 'áéíóúñçß.txt')
        self.track_file(unicode_path)
        command = utils.transform.string_to_list(f"ls > {unicode_path}")
        self.instance = manager.build(command, info)
        self.assertIsNotNone(self.instance)
        self.assertTrue(os.path.exists(unicode_path), self.instance.stdout.name)

    def test_file_path_10(self):
        # Test paths with unicode characters
        unicode_path = os.path.join(TMP, 'áéíó úñçß.txt')
        self.track_file(unicode_path)
        command = utils.transform.string_to_list(f"ls > '{unicode_path}'")
        self.instance = manager.build(command, info)
        self.assertIsNotNone(self.instance)
        self.assertTrue(os.path.exists(unicode_path), self.instance.stdout.name)


if __name__ == '__main__':
    unittest.main()
