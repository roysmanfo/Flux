import unittest
from flux.utils import transform


class Test_Utils(unittest.TestCase):

    def test_returns_a_list(self):
        test = "   Hello   World!   "
        formatted = transform.string_to_list(test)
        self.assertFalse(formatted == ["Hello", "World!"])

    def test_returns_a_list_2(self):
        test = "   Hello   World!   "
        formatted = transform.string_to_list(test)
        self.assertTrue(formatted == ["hello", "World!"])

class Test_StringToList(unittest.TestCase):

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
    
    def test_09(self):
        cmd = transform.string_to_list("echo test ; ls")
        self.assertTrue(cmd == ["echo", "test", ";", "ls"], cmd)

class Test_CommandSeparator(unittest.TestCase):
    
    def test_01(self):
        cmd = transform.split_commands("echo test ; ls")
        self.assertTrue(cmd == [["echo", "test"], ["ls"]], cmd)
    
    def test_02(self):
        cmd = transform.split_commands("echo test; ls")
        self.assertTrue(cmd == [["echo", "test"], ["ls"]], cmd)
    
    def test_03(self):
        cmd = transform.split_commands("echo test;ls")
        self.assertTrue(cmd == [["echo", "test"], ["ls"]], cmd)
    
    def test_04(self):
        cmd = transform.split_commands("echo test;ls;")
        self.assertTrue(cmd == [["echo", "test"], ["ls"]], cmd)

    def test_05(self):
        cmd = transform.split_commands(";echo test;ls;")
        self.assertTrue(cmd == [["echo", "test"], ["ls"]], cmd)

    def test_06(self):
        cmd = transform.split_commands("echo test;ls;;")
        self.assertTrue(cmd == [["echo", "test"], ["ls"]], cmd)

    def test_07(self):
        cmd = transform.split_commands("echo test;;;;ls;;")
        self.assertTrue(cmd == [["echo", "test"], ["ls"]], cmd)

    def test_08(self):
        cmd = transform.split_commands("echo test;ls ..;")
        self.assertTrue(cmd == [["echo", "test"], ["ls", ".."]], cmd)

    def test_10(self):
        cmd = transform.split_commands("echo test;ls  ..;echo null")
        self.assertTrue(cmd == [["echo", "test"], ["ls", ".."], ["echo", "null"]], cmd)

    def test_11(self):
        cmd = transform.split_commands("echo test | cat")
        self.assertTrue(cmd == [["echo", "test", "|", "cat"]], cmd)

    def test_11(self):
        cmd = transform.split_commands("echo test | cat; ls ..")
        self.assertTrue(cmd == [["echo", "test", "|", "cat"], ["ls", ".."]], cmd)
    
    def test_12(self):
        cmd = transform.split_commands("echo test |cat;ls ..")
        self.assertTrue(cmd == [["echo", "test", "|", "cat"], ["ls", ".."]], cmd)


class Test_PipeSeparator(unittest.TestCase):
    def test_01(self):
        cmd = transform.split_pipe("echo test | ls")
        self.assertTrue(cmd == [["echo", "test"], ["ls"]], cmd)
    
    def test_02(self):
        cmd = transform.split_pipe("echo test| ls")
        self.assertTrue(cmd == [["echo", "test"], ["ls"]], cmd)
    
    def test_03(self):
        cmd = transform.split_pipe("echo test|ls")
        self.assertTrue(cmd == [["echo", "test"], ["ls"]], cmd)



if __name__ == '__main__':
    unittest.main()
