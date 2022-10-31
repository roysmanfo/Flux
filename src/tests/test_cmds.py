import unittest


class Test_TestCommandProcessing(unittest.TestCase):

    def test_command_arguments_classification_1(self):
        """
        Check if command arguments are classified correctly
        """

        from src.core.manager import classify_arguments
        command = ["sortfiles", "/reverse"]
        result = classify_arguments(command)
        expected = {"command": "sortfiles", "flags": [],
                    "variables": [], "options": ["/reverse"]}

        self.assertEqual(result, expected, "Arguments classified incorrectly")

    def test_command_arguments_classification_2(self):
        """
        Check if command arguments are classified correctly
        """

        from src.core.manager import classify_arguments
        command = ["sortfiles"]
        result = classify_arguments(command)
        expected = {"command": "sortfiles",
                    "flags": [], "variables": [], "options": []}

        self.assertEqual(result, expected, "Arguments classified incorrectly")

    def test_command_arguments_classification_3(self):
        """
        Check if command arguments are classified correctly
        """

        from src.core.manager import classify_arguments
        command = ["sortfiles", "-f", "sort_rules.json"]
        result = classify_arguments(command)
        expected = {"command": "sortfiles", "flags": [
            "-f"], "variables": ["sort_rules.json"], "options": []}

        self.assertEqual(result, expected, "Arguments classified incorrectly")


if __name__ == '__main__':
    unittest.main()
