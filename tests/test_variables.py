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
        cmnd = export.Command()
        cmnd.run(['export', 'foo', 'bar'], INFO)
        result = INFO.variables.get("foo", None)
        self.assertTrue(result == None, "The variable has been created, but it wasn't supposed to")

    def test_variables_02(self):
        """
        Spelling variable syntax
        """

        from src.core import setup
        from src.settings.info import Info, User, SETTINGS_FILE, SETTINGS_FOLDER
        from src.core.cmd import export

        INFO: Info = setup.setup(User, Info, SETTINGS_FILE, SETTINGS_FOLDER)
        cmnd = export.Command()
        cmnd.run(['export', '$foo'], INFO)
        result = INFO.variables.get("foo", None)
        self.assertTrue(result == None, "The variable has been created, but it wasn't supposed to")

    def test_variables_03(self):
        """
        Spelling variable syntax
        """

        from src.core import setup
        from src.settings.info import Info, User, SETTINGS_FILE, SETTINGS_FOLDER
        from src.core.cmd import export

        INFO: Info = setup.setup(User, Info, SETTINGS_FILE, SETTINGS_FOLDER)
        cmnd = export.Command()
        cmnd.run(['export', '$$', 'bar'], INFO)
        result = INFO.variables.get("$", None)
        self.assertTrue(result == None, "The variable has been created, but it wasn't supposed to")


if __name__ == '__main__':
    unittest.main()
