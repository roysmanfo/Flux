import unittest, os
from dotenv import load_dotenv

class Test_EnvVariables(unittest.TestCase):
    def test_CMD_variables_type(self):

        load_dotenv(verbose=False)

        WINDOWS = os.getenv("WINDOWS").split(", ")
        LINUX = os.getenv("LINUX").split(", ")

        result = [type(WINDOWS)== type(LINUX)]
        
        self.assertTrue(all(result))

    


if __name__ == '__main__':
    unittest.main()
    