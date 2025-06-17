import unittest
import os

class MyTestRunner(unittest.TextTestRunner):
    def run(self, test):
        result = super().run(test)
        print(f"\nRésumé des tests:")
        print(f"Total des tests: {result.testsRun}")
        print(f"Réussis: {result.testsRun - len(result.errors) - len(result.failures)}")
        print(f"Erreurs: {len(result.errors)}")
        print(f"Echecs: {len(result.failures)}")
        return result

def run_test_suite():
    """
    Discover and run all test cases in the current directory.
    """
    # Get the current directory
    start_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Discover all test files (files that start with 'test')
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir, pattern="test_*.py")
    
    # Run the test suite with our custom runner
    runner = MyTestRunner(verbosity=2)
    runner.run(suite)

if __name__ == '__main__':
    run_test_suite()
