import unittest


class Test_Variables(unittest.TestCase):

    def test_variables_01(self):
        """
        Spelling variable syntax
        """

        from src.core import setup
        from src.settings.info import Info, User, SETTINGS_FILE, SETTINGS_FOLDER
        from src.core.cmd import export

        INFO: Info = setup.setup(User, Info, SETTINGS_FILE, SETTINGS_FOLDER)
        cmnd = export.Command(INFO, False)
        cmnd.run(['export', 'foo', 'bar'])
        result = INFO.variables.get("foo")
        self.assertTrue(result is None, "The variable has been created, but it wasn't supposed to")

    def test_variables_02(self):
        """
        Spelling variable syntax
        """

        from src.core import setup
        from src.settings.info import Info, User, SETTINGS_FILE, SETTINGS_FOLDER
        from src.core.cmd import export

        INFO: Info = setup.setup(User, Info, SETTINGS_FILE, SETTINGS_FOLDER)
        cmnd = export.Command(INFO, False)
        cmnd.run(['export', '$foo'])
        result = INFO.variables.get("foo")
        self.assertTrue(result is None, "The variable has been created, but it wasn't supposed to")

    def test_variables_03(self):
        """
        Spelling variable syntax
        """

        from src.core import setup
        from src.settings.info import Info, User, SETTINGS_FILE, SETTINGS_FOLDER
        from src.core.cmd import export

        INFO: Info = setup.setup(User, Info, SETTINGS_FILE, SETTINGS_FOLDER)
        cmnd = export.Command(INFO, False)
        cmnd.run(['export', '$$', 'bar'])
        result = INFO.variables.get("$")
        self.assertTrue(result is None, "The variable has been created, but it wasn't supposed to")


if __name__ == '__main__':
    unittest.main()
