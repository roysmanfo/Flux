import unittest


class Test_Variables(unittest.TestCase):

    def test_variables_01(self):
        """
        Spelling variable syntax
        """

        from src.core import setup
        from src.settings.info import Info
        from src.core.cmd import export

        INFO: Info = setup.setup()
        cmnd = export.Command(INFO, ['export', 'foo', 'bar'], False)
        cmnd.run()
        result = INFO.variables.get("foo")
        self.assertTrue(result is None, "The variable has been created, but it wasn't supposed to")

    def test_variables_02(self):
        """
        Spelling variable syntax
        """

        from src.core import setup
        from src.settings.info import Info
        from src.core.cmd import export

        INFO: Info = setup.setup()
        cmnd = export.Command(INFO, ['export', '$foo'], False)
        cmnd.run()
        result = INFO.variables.get("foo")
        self.assertTrue(result is None, "The variable has been created, but it wasn't supposed to")

    def test_variables_03(self):
        """
        Spelling variable syntax
        """

        from src.core import setup
        from src.settings.info import Info
        from src.core.cmd import export

        INFO: Info = setup.setup()
        cmnd = export.Command(INFO, ['export', '$$', 'bar'], False)
        cmnd.run()
        result = INFO.variables.get("$")
        self.assertTrue(result is None, "The variable has been created, but it wasn't supposed to")


if __name__ == '__main__':
    unittest.main()
