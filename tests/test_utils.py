import unittest


class Test_TestUtils(unittest.TestCase):

    def test_returns_a_list(self):
        """
        Check if the command.py util works properly
        """
        from src.utils import transform

        test = "   Hello   World!   "
        formatted = transform.string_to_list(test)
        ERROR_MSG = "transform.string_to_list() should return a list with distributed elements and heading and trailing spaces removed"
        self.assertFalse(formatted == ["Hello", "World!"], ERROR_MSG)

    def test_returns_a_list_2(self):
        """
        Check if the command.py util works properly
        """
        from src.utils import transform

        test = "   Hello   World!   "
        formatted = transform.string_to_list(test)
        ERROR_MSG = "command.string_to_list() should return a list with distributed elements and heading and trailing spaces removed"
        self.assertTrue(formatted == ["hello", "World!"], ERROR_MSG)


if __name__ == '__main__':
    unittest.main()
