import unittest


class Test_TestUser(unittest.TestCase):
    
    def test_user_has_correct_attributes(self):
        """
        Check if all attributes heve the desired type
        """

        import os
        from flux.settings.settings import Path, SysPaths
        from flux.core import setup

        s_file_exists = os.path.exists(SysPaths.SETTINGS_FILE)

        info = setup.setup()
        USER = info.user
        types = [
            type(USER.email) == str,
            type(USER.paths) == Path,
        ]
        result = all(types)

        if not s_file_exists:
            # check if it has been created before deleting
            if os.path.exists( SysPaths.SETTINGS_FILE):
                os.remove(SysPaths.SETTINGS_FILE)

        self.assertTrue(
            result, "1 or more attributes are identified with the wrong type")


if __name__ == '__main__':
    unittest.main()
