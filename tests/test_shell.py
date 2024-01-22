import os
import sys
import unittest
from src.settings.info import SysPaths
from src.core import setup, manager

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
            if self.instance.stdout != sys.stdout:
                if not self.instance.stdout.closed:
                    self.instance.stdout.close()

            if self.instance.stderr != sys.stderr:
                if not self.instance.stderr.closed:
                    self.instance.stderr.close()

            if self.instance.stdin != sys.stdin:
                if not self.instance.stdin.closed:
                    self.instance.stdin.close()
            
            self.instance = None

    def test_build_01(self):
        command = ["not existent command"]
        self.instance = manager.build(command, info)
        self.assertTrue(self.instance is None)
    
    def test_build_02(self):
        command = ["£345%$£"]
        self.instance = manager.build(command, info)
        self.assertTrue(self.instance is None)
    
    def test_build_03(self):
        command = ["ls", ">"]
        self.instance = manager.build(command, info)
        self.assertTrue(self.instance is None)
   
    def test_build_04(self):
        command = ["ls", ">>"]
        self.instance = manager.build(command, info)
        self.assertTrue(self.instance is None)
    
    def test_build_05(self):
        command = ["ls", ">/file"]
        self.instance = manager.build(command, info)
        self.assertTrue(self.instance is not None)

    def test_build_06(self):
        command = ["ls", ">", "/file"]
        self.instance = manager.build(command, info)
        self.assertTrue(self.instance is not None)

    def test_build_07(self):
        command = ["ls", "2>/file"]
        self.instance = manager.build(command, info)
        self.assertTrue(self.instance is not None)
        
    def test_build_08(self):
        command = ["ls", "2>>/file"]
        self.instance = manager.build(command, info)
        self.assertTrue(self.instance is not None)
    
    def test_build_09(self):
        command = ["ls", "<"]
        self.instance = manager.build(command, info)
        self.assertTrue(self.instance is None)

if __name__ == '__main__':
    unittest.main()
