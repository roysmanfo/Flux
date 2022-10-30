import unittest

class Test_TestUser(unittest.TestCase):
    def test_user_has_correct_attributes(self):
        from src.settings.info import User, Path
        USER = User()
        types = [
            type(USER.email) == str,
            type(USER.language) == str,
            type(USER.language_audio) == str,
            type(USER.language_text) == str,
            isinstance(USER.paths, type(Path))
        ]
        result = all(types)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()