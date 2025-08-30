import unittest
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file
from functions.config import MAX_CHARS

class TestRunPyFile(unittest.TestCase):
    def test_runCalcHelp(self):
        result = run_python_file("calculator", "main.py")
        expectation = 'STDOUT: Calculator App\nUsage: python main.py "<expression>"\nExample: python main.py "3 + 5"\n'
        self.assertEqual(result, expectation)
        print(result)
    
    def test_runCalcMath(self):
        result = run_python_file("calculator", "main.py", ["3 + 5"])
        expectation = 'STDOUT: ┌─────────┐\n│  3 + 5  │\n│         │\n│  =      │\n│         │\n│  8      │\n└─────────┘\n'
        self.assertEqual(result, expectation)
        print(result)

    def test_runCalcTests(self):
        result = run_python_file("calculator", "tests.py")
        expectation = 'STDERR: .........\n----------------------------------------------------------------------\nRan 9 tests in 0.002s\n\nOK\n'
        self.assertTrue('OK' in result)
        print(result)

    def test_runOutside(self):
        result = run_python_file("calculator", "../main.py")
        expectation = 'Error: Cannot execute "../main.py" as it is outside the permitted working directory'
        self.assertEqual(result, expectation)
        print(result)

    def test_nonexist(self):
        result = run_python_file("calculator", "nonexistent.py")
        expectation = 'Error: File "nonexistent.py" not found.'
        self.assertEqual(result, expectation)
        print(result)

if __name__ == "__main__":
    unittest.main()
