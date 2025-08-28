import unittest
from functions.get_files_info import get_files_info

class TestGetFilesInfo(unittest.TestCase):
    def test_calcpath(self):
        result = get_files_info("calculator", ".")
        expectation = "Result for current directory:\n"
        expectation += " - main.py: file_size=580 bytes, is_dir=False\n" 
        expectation += " - tests.py: file_size=1347 bytes, is_dir=False\n"
        expectation += " - pkg: file_size=44 bytes, is_dir=True\n"
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

if __name__ == "__main__":
    unittest.main()
