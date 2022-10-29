import unittest, sys

class Test_TestUser(unittest.TestCase):
    def test_user_has_all_attributes(self):
        from src.settings.info import User
        USER = User()
        types = [
            type(USER.email) == str,
            type(USER.language) == str,
            type(USER.language_audio) == str,
            type(USER.language_text) == str,
            type(USER.paths) == dict,
        ]
        result = all(types)
        self.assertTrue(result)

    def test_decrement(self):
        pass

if __name__ == '__main__':
    unittest.main()