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

class Test_TestStringToList(unittest.TestCase):

    def test_01(self):
        cmd = transform.string_to_list("ls")
        self.assertTrue(cmd == ["ls"], cmd)

    def test_02(self):
        cmd = transform.string_to_list("   ls   ")
        self.assertTrue(cmd == ["ls"], cmd)

    def test_03(self):
        cmd = transform.string_to_list("LS -h")
        self.assertTrue(cmd == ["ls", "-h"], cmd)

    def test_04(self):
        cmd = transform.string_to_list("LS -R")
        self.assertTrue(cmd == ["ls", "-R"], cmd)

    def test_05(self):
        cmd = transform.string_to_list("ls >> file")
        self.assertTrue(cmd == ["ls", ">>", "file"], cmd)

    def test_06(self):
        cmd = transform.string_to_list("ls 2>/dev/null")
        self.assertTrue(cmd == ["ls", "2>", "/dev/null"], cmd)

    def test_07(self):
        cmd = transform.string_to_list("LS << Input.txt")
        self.assertTrue(cmd == ["ls", "<<", "Input.txt"], cmd)

    def test_08(self):
        cmd = transform.string_to_list("echo test | ls")
        self.assertTrue(cmd == ["echo", "test", "|", "ls"], cmd)


if __name__ == '__main__':
    unittest.main()
