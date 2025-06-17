import unittest
import pytest
import sys
import os
import logging
from datetime import datetime

# Configure logging for the test suite
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("test_suite_results.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("TestSuite")

# Import test modules
from test_web_api_integration import TestWebAPIIntegration
from test_web_api_client import TestWebAPIClient
from test_api_endpoints import TestAPIEndpoints

class TestSuite:
    """
    Test Suite for Web API Integration Tests
    
    This class organizes and runs all test cases for the web API integration.
    It provides functionality to run specific test groups or all tests.
    """
    
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.test_loader = unittest.TestLoader()
        self.test_suite = unittest.TestSuite()
        self.test_runner = unittest.TextTestRunner(verbosity=2)
        self.results = {}
        
    def add_test_case(self, test_case_class):
        """Add a test case class to the suite"""
        tests = self.test_loader.loadTestsFromTestCase(test_case_class)
        self.test_suite.addTest(tests)
        logger.info(f"Added {test_case_class.__name__} with {tests.countTestCases()} test cases")
        
    def run_all_tests(self):
        """Run all tests in the suite"""
        logger.info("Starting test suite execution")
        self.start_time = datetime.now()
        
        result = self.test_runner.run(self.test_suite)
        
        self.end_time = datetime.now()
        self.results = {
            "run": result.testsRun,
            "failures": len(result.failures),
            "errors": len(result.errors),
            "skipped": len(result.skipped) if hasattr(result, 'skipped') else 0,
            "duration": (self.end_time - self.start_time).total_seconds()
        }
        
        self._log_results()
        return result
    
    def run_specific_tests(self, test_pattern):
        """Run tests matching a specific pattern"""
        logger.info(f"Running tests matching pattern: {test_pattern}")
        self.start_time = datetime.now()
        
        specific_tests = self.test_loader.loadTestsFromName(test_pattern)
        result = self.test_runner.run(specific_tests)
        
        self.end_time = datetime.now()
        self.results = {
            "run": result.testsRun,
            "failures": len(result.failures),
            "errors": len(result.errors),
            "skipped": len(result.skipped) if hasattr(result, 'skipped') else 0,
            "duration": (self.end_time - self.start_time).total_seconds()
        }
        
        self._log_results()
        return result
    
    def _log_results(self):
        """Log the test results"""
        logger.info("=" * 70)
        logger.info(f"Test Suite Results:")
        logger.info(f"  Start time: {self.start_time}")
        logger.info(f"  End time: {self.end_time}")
        logger.info(f"  Duration: {self.results['duration']:.2f} seconds")
        logger.info(f"  Tests run: {self.results['run']}")
        logger.info(f"  Failures: {self.results['failures']}")
        logger.info(f"  Errors: {self.results['errors']}")
        logger.info(f"  Skipped: {self.results['skipped']}")
        logger.info("=" * 70)
        
        # Generate a summary file
        with open("test_summary.txt", "w") as f:
            f.write("Test Suite Summary\n")
            f.write("=================\n\n")
            f.write(f"Date: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Duration: {self.results['duration']:.2f} seconds\n")
            f.write(f"Tests run: {self.results['run']}\n")
            f.write(f"Failures: {self.results['failures']}\n")
            f.write(f"Errors: {self.results['errors']}\n")
            f.write(f"Skipped: {self.results['skipped']}\n")
            
            success_rate = ((self.results['run'] - self.results['failures'] - self.results['errors']) / 
                           self.results['run'] * 100) if self.results['run'] > 0 else 0
            f.write(f"Success rate: {success_rate:.2f}%\n")


def main():
    """Main function to run the test suite"""
    # Create a test suite
    suite = TestSuite()
    
    # Add test cases
    suite.add_test_case(TestWebAPIIntegration)
    suite.add_test_case(TestWebAPIClient)
    suite.add_test_case(TestAPIEndpoints)
    
    # Check if a specific test pattern was provided
    if len(sys.argv) > 1:
        pattern = sys.argv[1]
        suite.run_specific_tests(pattern)
    else:
        # Run all tests
        suite.run_all_tests()


if __name__ == "__main__":
    main()
