import os
import sys
import unittest
import tempfile
from flux.settings.info import SysPaths
from flux.core import setup, manager
from flux import utils

TMP = tempfile.gettempdir()
FILE = os.path.join(TMP, "file.txt")


s_file_exists = os.path.exists(SysPaths.SETTINGS_FILE)

# NOTE: tests for setup must be handles elsewhere
info = setup.setup()

class Test_TestShell(unittest.TestCase):

    def setUp(self):
        self.addCleanup(self.clean)
        self.instance = None

    def clean(self) -> None:        
        if not s_file_exists and os.path.exists( SysPaths.SETTINGS_FILE):
            os.remove(SysPaths.SETTINGS_FILE)
        
        if self.instance:
            if self.instance.stdout and self.instance.stdout != sys.stdout:
                if not self.instance.stdout.closed:
                    self.instance.stdout.close()

            if self.instance.stderr and self.instance.stderr != sys.stderr:
                if not self.instance.stderr.closed:
                    self.instance.stderr.close()

            if self.instance.stdin and self.instance.stdin != sys.stdin:
                if not self.instance.stdin.closed:
                    self.instance.stdin.close()
            
            self.instance = None

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
        self.assertFalse(self.instance is None)

    def test_build_06(self):
        command = utils.transform.string_to_list(f"ls > {FILE}")
        self.instance = manager.build(command, info)
        self.assertFalse(self.instance is None)

    def test_build_07(self):
        command = utils.transform.string_to_list(f"ls 2>{FILE}")
        self.instance = manager.build(command, info)
        self.assertFalse(self.instance is None)
        
    def test_build_08(self):
        command = utils.transform.string_to_list(f"ls 2>>{FILE}")
        self.instance = manager.build(command, info)
        self.assertFalse(self.instance is None)
    
    def test_build_09(self):
        command = utils.transform.string_to_list("ls <")
        self.instance = manager.build(command, info)
        print(command, self.instance)
        self.assertTrue(self.instance is None)

if __name__ == '__main__':
    unittest.main()
