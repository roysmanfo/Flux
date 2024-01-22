import os
import unittest
from src.settings.info import SysPaths
from src.core import setup, manager

s_file_exists = os.path.exists(SysPaths.SETTINGS_FILE)

# NOTE: tests for setup must be handles elsewhere
info = setup.setup()

class Test_TestShell(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.addCleanup(self.clean)
    
    @staticmethod
    def clean() -> None:
        if not s_file_exists and os.path.exists( SysPaths.SETTINGS_FILE):
            os.remove(SysPaths.SETTINGS_FILE)

    def test_build_01(self):
        command = ["not existent command"]
        c_instance = manager.build(command, info)
        self.assertTrue(c_instance is None, "Command instance should be none")
    
    def test_build_02(self):
        command = ["£345%$£"]
        c_instance = manager.build(command, info)
        self.assertTrue(c_instance is None, "Command instance should be none")
    
    def test_build_03(self):
        command = ["ls", ">"]
        c_instance = manager.build(command, info)
        self.assertTrue(c_instance is None, "Command instance should be none")

if __name__ == '__main__':
    unittest.main()
