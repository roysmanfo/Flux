import unittest
from src.utils import transform


class Test_TestUtils(unittest.TestCase):

    def test_returns_a_list(self):
        """
        Check if the command.py util works properly
        """

        test = "   Hello   World!   "
        formatted = transform.string_to_list(test)
        self.assertFalse(formatted == ["Hello", "World!"])

    def test_returns_a_list_2(self):
        """
        Check if the command.py util works properly
        """

        test = "   Hello   World!   "
        formatted = transform.string_to_list(test)
        self.assertTrue(formatted == ["hello", "World!"])


if __name__ == '__main__':
    unittest.main()
