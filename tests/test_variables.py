import unittest

class Test_Variables(unittest.TestCase):

    def test_variables_01(self):
        """
        Spelling variable syntax
        """

        from src.core import setup
        from src.settings.info import Info, User, SETTINGS_FILE, SETTINGS_FOLDER
        from src.core.cmd import set


        INFO: Info = setup.setup(User, Info, SETTINGS_FILE, SETTINGS_FOLDER)
        result = set.set_user_variable({"variables": ['foo', 'bar']}, INFO)

        self.assertFalse(result, "The variable has been created, but it wasn't supposed to")

if __name__ == '__main__':
    unittest.main()
