import os
import sys
from typing import Optional
import unittest

from flux import utils
from flux.core import manager, setup
from flux.core.system.variables import Variable
from flux.settings.info import SysPaths

s_file_exists = os.path.exists(SysPaths.SETTINGS_FILE)
info = setup.setup()

class Test_Variables(unittest.TestCase):
    
    def setUp(self):
        self.addCleanup(self.clean)
        self.instance = None

    def clean(self) -> None:        
        if not s_file_exists and os.path.exists(SysPaths.SETTINGS_FILE):
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

    def _capture_output(self) -> None:
        if self.instance:
            self.instance.stdout = None
            self.instance.stderr = None
            self.instance.stdin = None
    
    def _run_test(self, command: str, var_to_get: str) -> Optional[Variable]:
        cmd = utils.transform.string_to_list(command)
        self.instance = manager.build(cmd, info)
        self._capture_output()
        manager.call(self.instance)
        return info.variables.get(var_to_get)

    def test_variables_01(self):
        self.assertTrue(self._run_test("export foo bar", "foo") is None)

    def test_variables_02(self):
        self.assertTrue(self._run_test("export $foo", "foo") is None)

    def test_variables_03(self):
        self.assertTrue(self._run_test("export $$ bar", "$") is None)



if __name__ == '__main__':
    unittest.main()
