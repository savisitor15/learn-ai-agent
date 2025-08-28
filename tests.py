import unittest
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.config import MAX_CHARS

class TestGetFilesInfo(unittest.TestCase):
    def test_calcpath(self):
        result = get_files_info("calculator", ".")
        expectation = "Result for current directory:\n"
        expectation += " - main.py: file_size=580 bytes, is_dir=False\n" 
        expectation += " - tests.py: file_size=1347 bytes, is_dir=False\n"
        expectation += " - pkg: file_size=44 bytes, is_dir=True\n"
        expectation += " - lorem.txt: file_size=20065 bytes, is_dir=False\n"
        print(result)
        self.assertEqual(result, expectation)

    def test_calcsubpath(self):
        result = get_files_info("calculator", "pkg")
        expectation = "Result for 'pkg' directory:\n"
        expectation += " - calculator.py: file_size=1746 bytes, is_dir=False\n"
        expectation += " - render.py: file_size=767 bytes, is_dir=False\n"
        print(result)
        self.assertEqual(result, expectation)

    def test_boundries(self):
        result = get_files_info("calculator", "/bin")
        expectation = 'Error: Cannot list "/bin" as it is outside the permitted working directory'
        print(result)
        self.assertEqual(result, expectation)

    def test_relativeboundries(self):
        result = get_files_info("calculator", "../")
        expectation = "Result for '../' directory:\n"
        expectation += 'Error: Cannot list "../" as it is outside the permitted working directory'

class TestGetFileContent(unittest.TestCase):
    def test_lorem(self):
        result = get_file_content("calculator", "lorem.txt")
        expectation = '[...File "lorem.txt" truncated at 10000 characters]'
        self.assertEqual(len(result), MAX_CHARS)
        self.assertTrue(result.endswith(expectation))

    def test_main(self):
        result = get_file_content("calculator", "main.py")
        expectation = ""
        with open("calculator/main.py") as fp:
            expectation = fp.read()
        self.assertEqual(result, expectation)
        print(result)

    def test_calculator(self):
        result = get_file_content("calculator", "pkg/calculator.py")
        expectation = ""
        expectation = ""
        with open("calculator/pkg/calculator.py") as fp:
            expectation = fp.read()
        self.assertTrue(result.endswith(expectation))
        print(result)

    def test_safety_error(self):
        result = get_file_content("calculator", "/bin/cat")
        expectation = 'Error: Cannot read "/bin/cat" as it is outside the permitted working directory'
        self.assertEqual(result, expectation)
        print(result)

    def test_not_found(self):
        result = get_file_content("calculator", "pkg/does_not_exist.py")
        expectation = 'Error: File not found or is not a regular file: "pkg/does_not_exist.py"'
        self.assertEqual(result, expectation)
        print(result)


if __name__ == "__main__":
    unittest.main()
