import unittest
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.config import MAX_CHARS

class Test_WriteFile(unittest.TestCase):
    def test_calculator_lorem(self):
        result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
        expectation = 'Successfully wrote to "lorem.txt" (28 characters written)'
        print(result)
        self.assertEqual(result, expectation)

    def test_calculator_morelorem(self):
        result = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
        expectation = expectation = 'Successfully wrote to "pkg/morelorem.txt" (26 characters written)'
        print(result)
        self.assertEqual(result, expectation)

    def test_failure(self):
        result = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
        expectation = 'Error: Cannot write to "/tmp/temp.txt" as it is outside the permitted working directory'
        print(result)
        self.assertEqual(result, expectation)

if __name__ == "__main__":
    unittest.main()
